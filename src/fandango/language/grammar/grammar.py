import itertools
import warnings
from collections import defaultdict
from collections.abc import Generator, Iterator, Sequence
from typing import Any, Optional, cast

import fandango.language.grammar.nodes as nodes
from fandango.errors import FandangoGeneratorError, FandangoValueError
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language.grammar import FuzzingMode, ParsingMode, closest_match
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.k_paths import GrammarKPaths
from fandango.language.grammar.k_paths import KPath as KPath  # re-exported
from fandango.language.grammar.literal_generator import LiteralGenerator
from fandango.language.grammar.node_visitors.disambiguator import Disambiguator
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.node_visitors.primer import PrimerVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.parser.parser import Parser
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree, TreeTuple
from fandango.language.tree_value import TreeValueType
from fandango.logger import LOGGER


class Grammar(NodeVisitor[list[Node], list[Node]]):
    """Represent a grammar."""

    def __init__(
        self,
        grammar_settings: Sequence[HasSettings],
        rules: Optional[dict[NonTerminal, Node]] = None,
        fuzzing_mode: Optional[FuzzingMode] = FuzzingMode.COMPLETE,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ):
        self._grammar_settings = grammar_settings
        self.rules: dict[NonTerminal, Node] = rules or {}
        self.generators: dict[NonTerminal, LiteralGenerator] = {}
        self.fuzzing_mode = fuzzing_mode
        self._local_variables = local_variables or {}
        self._global_variables = global_variables or {}
        self._parser = Parser(self.rules)
        self.k_paths = GrammarKPaths(self)

    @property
    def grammar_settings(self) -> Sequence[HasSettings]:
        return self._grammar_settings

    @staticmethod
    def _topological_sort(
        graph: dict[NonTerminal, set[NonTerminal]],
    ) -> list[NonTerminal]:
        indegree: dict[Any, int] = defaultdict(int)
        queue = []

        for node in graph:
            for neighbour in graph[node]:
                indegree[neighbour] += 1
        for node in graph:
            if indegree[node] == 0:
                queue.append(node)

        topological_order = []
        while queue:
            node = queue.pop(0)
            topological_order.append(node)

            for neighbour in graph[node]:
                indegree[neighbour] -= 1

                if indegree[neighbour] == 0:
                    queue.append(neighbour)

        if len(topological_order) != len(graph):
            print("Cycle exists")
        return topological_order[::-1]

    def is_use_generator(self, tree: DerivationTree) -> bool:
        symbol = tree.symbol
        if not symbol.is_non_terminal:
            return False
        nt = cast(NonTerminal, symbol)
        if nt not in self.generators:
            return False
        if tree is None:
            path = set()
        else:
            path = set(map(lambda x: x.symbol, tree.get_path()))
        generator_dependencies = self.generator_dependencies(nt)
        intersection = path.intersection(set(generator_dependencies))
        return len(intersection) == 0

    def derive_sources(self, tree: DerivationTree) -> list[DerivationTree]:
        gen_symbol = tree.symbol
        if not gen_symbol.is_non_terminal:
            raise FandangoValueError(
                f"Tree {gen_symbol.format_as_spec()} is not a nonterminal"
            )
        if tree.symbol not in self.generators:
            raise FandangoValueError(
                f"No generator found for tree {gen_symbol.format_as_spec()}"
            )

        if not self.is_use_generator(tree):
            return []

        assert isinstance(gen_symbol, NonTerminal)
        dependent_generators: dict[NonTerminal, set[NonTerminal]] = {gen_symbol: set()}
        for val in self.generators[gen_symbol].nonterminals.values():
            if val.symbol not in self.rules:
                closest = closest_match(str(val), [x.name() for x in self.rules.keys()])
                raise FandangoValueError(
                    f"Symbol {val.symbol.format_as_spec()} not defined in grammar. Did you mean {closest}?"
                )

            if val.symbol not in self.generators:
                raise FandangoValueError(
                    f"{val.symbol.format_as_spec()}: Missing converter from {gen_symbol.format_as_spec()} ({val.symbol.format_as_spec()} ::= ... := f({gen_symbol.format_as_spec()}))"
                )

            dependent_generators[val.symbol] = self.generator_dependencies(val.symbol)
        dependent_gens = self._topological_sort(dependent_generators)
        dependent_gens.remove(gen_symbol)

        args = [tree]
        for symbol in dependent_gens:
            try:
                generated_param = self.generate(symbol, args)
            except Exception as e:
                raise e
            generated_param.sources = []
            generated_param._parent = tree
            # If this symbol would've been used with a generator, set its children to RO
            if self.is_use_generator(generated_param):
                for child in generated_param.children:
                    child.set_all_read_only(True)
            for child in generated_param.children:
                self.populate_sources(child)
            args.append(generated_param)
        args.pop(0)
        return args

    def derive_generator_output(self, tree: DerivationTree) -> list[DerivationTree]:
        generated = self.generate(tree.nonterminal, tree.sources)
        return generated.children

    def populate_sources(self, tree: DerivationTree) -> None:
        for node in tree.flattened():
            node.sources = []
        self._populate_sources(tree)

    def _populate_sources(self, tree: DerivationTree) -> None:
        stack = [tree]
        while stack:
            node = stack.pop()
            if self.is_use_generator(node):
                node.sources = self.derive_sources(node)
                for child in node.children:
                    child.set_all_read_only(True)
                continue
            stack.extend(reversed(node.children))

    def generate_string(
        self,
        symbol: str | NonTerminal = "<start>",
        sources: Optional[list[DerivationTree]] = None,
    ) -> tuple[list[DerivationTree], str | bytes | TreeTuple[str]]:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        if self.generators[symbol] is None:
            raise ValueError(f"{symbol.format_as_spec()}: no generator")

        sources_: dict[Symbol, DerivationTree]
        if sources is None:
            sources_ = dict()
        else:
            sources_ = {tree.symbol: tree for tree in sources}
        generator = self.generators[symbol]

        local_variables = self._local_variables.copy()
        for id, nonterminal in generator.nonterminals.items():
            if nonterminal.symbol not in sources_:
                raise FandangoValueError(
                    f"{nonterminal.symbol}: missing generator parameter"
                )
            local_variables[id] = sources_[nonterminal.symbol]

        return list(sources_.values()), eval(
            generator.call, self._global_variables, local_variables
        )

    def generator_dependencies(
        self, symbol: str | NonTerminal = "<start>"
    ) -> set[NonTerminal]:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        if self.generators[symbol] is None:
            return set()
        return {x.symbol for x in self.generators[symbol].nonterminals.values()}

    def generate(
        self,
        symbol: str | NonTerminal = "<start>",
        sources: Optional[list[DerivationTree]] = None,
        hookin_parent: Optional[DerivationTree] = None,
    ) -> DerivationTree:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        sources, string = self.generate_string(symbol, sources)
        if not (isinstance(string, (str, bytes, int, tuple))):
            raise TypeError(
                f"Generator {self.generators[symbol]} must return string, bytes, int, or tuple (returned {string!r})"
            )

        if isinstance(string, tuple):
            warnings.warn(
                "Returning a tree in the shape of a tuple from a generator is deprecated, as it is parsed into a tree, then immediately stringified and parsed against the grammar. You should instead return a str/bytes directly",
                stacklevel=2,
            )
            string = str(DerivationTree.from_tree(string))
        tree = self.parse(string, symbol, hookin_parent=hookin_parent)
        if tree is None:
            raise FandangoGeneratorError(
                f"Could not parse {string!r} (generated by {self.generators[symbol]}) into {symbol.format_as_spec()}",
                symbol.format_as_spec(),
            )
        tree.sources = [p.deepcopy(copy_parent=False) for p in sources]
        return tree

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        return self._parser.collapse(tree)

    def node_limit(self, symbol: str | NonTerminal, max_nodes: int) -> int:
        """The most nodes a tree of `symbol` may have: `max_nodes` on top of the nodes it needs at least."""
        return max_nodes + int(self[symbol].distance_to_completion)

    def fuzz(
        self,
        start: str | NonTerminal = "<start>",
        max_nodes: int = 50,
        prefix_node: Optional[DerivationTree] = None,
    ) -> DerivationTree:
        """
        Generate a random derivation tree from the grammar.
        :raise FandangoGeneratorError: If a called generator could not be parsed into the symbol, it applies to.
        """
        if isinstance(start, str):
            start = NonTerminal(start)
        if prefix_node is None:
            root = DerivationTree(start)
        else:
            root = prefix_node
        fuzzed_idx = len(root.children)
        NonTerminalNode(start, self._grammar_settings).fuzz(
            root, self, max_nodes=max_nodes
        )
        root = root.children[fuzzed_idx]
        root._parent = None
        return root

    def update(
        self, grammar: "Grammar | dict[NonTerminal, Node]", prime: bool = True
    ) -> None:
        generators: dict[NonTerminal, LiteralGenerator]
        local_variables: dict[str, Any]
        global_variables: dict[str, Any]
        if isinstance(grammar, Grammar):
            generators = grammar.generators
            local_variables = grammar._local_variables
            global_variables = grammar._global_variables
            rules = grammar.rules
            fuzzing_mode = grammar.fuzzing_mode
        else:
            rules = grammar
            generators = {}
            local_variables = {}
            global_variables = {}
            fuzzing_mode = FuzzingMode.COMPLETE

        self.rules.update(rules)
        self.fuzzing_mode = fuzzing_mode
        self.generators.update(generators)

        for symbol in rules.keys():
            # We're updating from a grammar with a rule, but no generator,
            # so we should remove the generator if it exists
            if symbol not in generators and symbol in self.generators:
                del self.generators[symbol]

        self._parser = Parser(self.rules)
        self._local_variables.update(local_variables)
        self._global_variables.update(global_variables)
        if prime:
            self.prime()

    def finalize_globals(self) -> None:
        """Finalize global variables by evaluating any callables."""
        for _key, value in self._global_variables.items():
            if "__globals__" in dir(value):
                value.__globals__.update(self._global_variables)

    def get_protocol_messages(
        self, start_symbol: Optional[NonTerminal] = None
    ) -> set[PacketNonTerminal]:
        if start_symbol is None:
            start_symbol = NonTerminal("<start>")
        work = set()
        work.add(self.rules[start_symbol])
        seen = set()
        while len(work) > 0:
            current = work.pop()
            for node in current.descendents(self):
                if node in seen:
                    continue
                seen.add(node)
                work.add(node)
        seen_nt = {n for n in seen if isinstance(n, NonTerminalNode)}
        msg_nt: set[NonTerminalNode] = {n for n in seen_nt if n.sender is not None}
        messages_set: set[PacketNonTerminal] = set()
        for n in msg_nt:
            assert n.sender is not None
            messages_set.add(PacketNonTerminal(n.sender, n.recipient, n.symbol))
        return messages_set

    def parse(
        self,
        word: str | bytes | int | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        include_controlflow: bool = False,
    ) -> Optional[DerivationTree]:
        return self._parser.parse(
            word,
            start,
            mode=mode,
            hookin_parent=hookin_parent,
            include_controlflow=include_controlflow,
        )

    def parse_forest(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        include_controlflow: bool = False,
    ) -> Generator[DerivationTree, None, None]:
        return self._parser.parse_forest(
            word, start, mode=mode, include_controlflow=include_controlflow
        )

    def parse_multiple(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        include_controlflow: bool = False,
    ) -> Generator[DerivationTree, None, None]:
        return self._parser.parse_multiple(
            word, start, mode=mode, include_controlflow=include_controlflow
        )

    def max_position(self) -> int:
        """Return the maximum position reached during last parsing."""
        return self._parser._iter_parser.max_position()

    def nodes(self) -> set[Node]:
        """Return a map of all nodes in the grammar."""
        node_set = set()
        for node in self.rules.values():
            node_set.add(node)
            node_set.update(node.descendents(self, filter_controlflow=False))
        return node_set

    def __contains__(self, item: str | NonTerminal) -> bool:
        if not isinstance(item, NonTerminal):
            item = NonTerminal(item)
        return item in self.rules

    def __getitem__(self, item: str | NonTerminal) -> Node:
        if not isinstance(item, NonTerminal):
            item = NonTerminal(item)
        return self.rules[item]

    def __setitem__(self, key: str | NonTerminal, value: Node) -> None:
        if not isinstance(key, NonTerminal):
            key = NonTerminal(key)
        self.rules[key] = value

    def __delitem__(self, key: str | NonTerminal) -> None:
        if not isinstance(key, NonTerminal):
            key = NonTerminal(key)
        del self.rules[key]

    def __iter__(self) -> Iterator[NonTerminal]:
        return iter(self.rules)

    def __len__(self) -> int:
        return len(self.rules)

    def __repr__(self) -> str:
        """Return a (canonical) string representation of the grammar."""
        return "\n".join(
            [
                f"{key.name()} ::= {value.format_as_spec()}{' := ' + self.generators[key].format_as_spec() if key in self.generators else ''}"
                for key, value in self.rules.items()
            ]
        )

    # Formats for to_states()
    STATE_FORMAT = "state"
    MERMAID_FORMAT = "mermaid"
    DOT_FORMAT = "dot"

    def to_states(
        self, *, start_symbol: str = "<start>", format: str = STATE_FORMAT
    ) -> str:
        """Convert into a (textual) finite state machine representation."""

        if format not in {self.STATE_FORMAT, self.MERMAID_FORMAT, self.DOT_FORMAT}:
            raise ValueError(
                f"Unknown format: {format}; must be one of {self.STATE_FORMAT}, {self.MERMAID_FORMAT}, {self.DOT_FORMAT}"
            )

        def paths(node: Node) -> list[list[Node]]:
            """Return all possible paths starting from this node."""
            if isinstance(node, Concatenation):
                children_paths = []
                for child in node.children():
                    children_paths.append(paths(child))

                all_paths = []
                for product in itertools.product(*children_paths):
                    p = []
                    for subpath in product:
                        p += subpath
                    all_paths.append(p)
                return all_paths

            if isinstance(node, Alternative):
                return [p for child in node.children() for p in paths(child)]

            if isinstance(node, (Repetition, Plus, Star, Option)):
                # For simplicity, we assume one repetition
                return paths(node.children()[0])

            return [[node]]

        def node(s: str) -> str:
            """Escape special characters for Mermaid."""
            if format == self.MERMAID_FORMAT:
                s = s.replace(":", "#colon;")
                s = s.replace("<", "#lt;")
                s = s.replace(">", "#gt;")
            return s

        def entry() -> str:
            """Return the entry symbol for the given format."""
            match format:
                case self.MERMAID_FORMAT:
                    return "[*]"
                case self.DOT_FORMAT:
                    return "_start"
                case _:
                    return "[*]"

        def exit() -> str:
            """Return the entry symbol for the given format."""
            match format:
                case self.MERMAID_FORMAT:
                    return "[*]"
                case self.DOT_FORMAT:
                    return "_end"
                case _:
                    return "[*]"

        def transition(a: str, b: str, label: Optional[str] = None) -> str:
            """Return a transition line for the given format."""
            match format:
                case self.MERMAID_FORMAT:
                    line = f"{a} --> {b}"
                    if label:
                        line += f": {label}"
                    return line
                case self.DOT_FORMAT:
                    line = f'"{a}" -> "{b}"'
                    if label:
                        line += f' [label="{label}"]'
                    return line
                case _:
                    line = f"{a} --> {b}"
                    if label:
                        line += f": {label}"
                    return line

        def transition_sep() -> str:
            """Return the transition separator for the given format."""
            match format:
                case self.DOT_FORMAT:
                    return "\\n"
                case _:
                    return " "

        lines = []

        def add_line(line: str) -> None:
            if format in {self.MERMAID_FORMAT, self.DOT_FORMAT}:
                line = "    " + line
            lines.append(line)

        if format == self.MERMAID_FORMAT:
            lines.append("stateDiagram")
        elif format == self.DOT_FORMAT:
            lines.append("digraph finite_state_machine {")
            # Style for start and end nodes
            lines.append('    node [shape=point,width=0.2,label=""]_start;')
            lines.append('    node [shape=doublecircle,label=""]_end;')
            # Default style for all other nodes; \N inserts the node name
            # Color and fonts are the same as in Mermaid
            lines.append(
                '    node [shape=ellipse,style=filled,fontname="Calibri",fillcolor="#ececfe",label="\\N"];'
            )
            lines.append('    edge [fontname="Calibri"];')

        add_line(transition(entry(), node(start_symbol)))
        states_seen = set()
        start_nt = NonTerminal(start_symbol)
        work: list[Symbol] = [start_nt]

        while work:
            from_state = work.pop()
            if from_state in states_seen:
                continue
            if from_state not in self.rules:
                continue

            assert isinstance(from_state, NonTerminal)

            states_seen.add(from_state)
            value = self.rules[from_state]

            all_paths = paths(value)

            for p in all_paths:
                to_state = p[-1]
                from_str = node(from_state.format_as_spec())

                if isinstance(to_state, NonTerminalNode):
                    to_str = node(to_state.format_as_spec())
                else:
                    # Last element is not a nonterminal, so it's an end state
                    to_str = node(exit())

                label = None
                transitions = p[:-1]
                if transitions:
                    label = transition_sep().join(
                        node(n.format_as_spec()) for n in transitions
                    )

                add_line(transition(from_str, to_str, label))
                next_symbol = to_state.to_symbol()
                work.append(next_symbol)

        if format == self.DOT_FORMAT:
            lines.append("}")

        return "\n".join(lines)

    def msg_parties(self, *, include_recipients: bool = True) -> set[str]:
        parties: set[str] = set()
        seen_nts: set[tuple[Optional[str], Optional[str], Symbol]] = set()
        for rule in self.rules.values():
            parties |= rule.msg_parties(
                grammar=self, seen_nts=seen_nts, include_recipients=include_recipients
            )
        return parties

    def get_repr_for_rule(self, symbol: str | NonTerminal) -> str:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return (
            f"{symbol.format_as_spec()} ::= {self.rules[symbol].format_as_spec()}"
            f"{' := ' + self.generators[symbol].format_as_spec() if symbol in self.generators else ''}"
        )

    @staticmethod
    def dummy() -> "Grammar":
        return Grammar(grammar_settings=[], rules={})

    def set_generator(
        self,
        symbol: str | NonTerminal,
        param: str,
        searches_map: Optional[dict[str, NonTerminalNode]] = None,
    ) -> None:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators[symbol] = LiteralGenerator(
            call=param, nonterminals=(searches_map or {})
        )

    def remove_generator(self, symbol: str | NonTerminal) -> None:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators.pop(symbol)

    def has_generator(self, symbol: str | NonTerminal) -> bool:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return symbol in self.generators

    def get_generator(self, symbol: str | NonTerminal) -> Optional[LiteralGenerator]:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return self.generators.get(symbol, None)

    def update_parser(self) -> None:
        self._parser = Parser(self.rules)

    def generate_all_k_paths(
        self,
        *,
        k: int,
        non_terminal: Optional[NonTerminal] = None,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        """All k-paths of this grammar, see `GrammarKPaths.generate_all`."""
        return self.k_paths.generate_all(
            k=k,
            non_terminal=non_terminal,
            overlap_to_root=overlap_to_root,
            coverage_goal=coverage_goal,
            input_parties=input_parties,
        )

    def _extract_k_paths_from_tree(
        self,
        tree: DerivationTree,
        k: int,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        """The k-paths found in a derivation tree, see `GrammarKPaths.extract_from_tree`."""
        return self.k_paths.extract_from_tree(
            tree, k, overlap_to_root, coverage_goal, input_parties
        )

    def prime(self) -> None:
        LOGGER.debug("Priming grammar")
        primer = PrimerVisitor(self.rules)
        primer.prime()

    def default_result(self) -> list[Node]:
        return []

    def aggregate_results(
        self, aggregate: list[Node], result: list[Node]
    ) -> list[Node]:
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative) -> list[Node]:
        return self.visitChildren(node) + [node]

    def visitConcatenation(self, node: Concatenation) -> list[Node]:
        return self.visitChildren(node) + [node]

    def visitRepetition(self, node: Repetition) -> list[Node]:
        return self.visit(node.node) + [node]

    def visitStar(self, node: Star) -> list[Node]:
        return self.visit(node.node) + [node]

    def visitPlus(self, node: Plus) -> list[Node]:
        return self.visit(node.node) + [node]

    def visitOption(self, node: Option) -> list[Node]:
        return self.visit(node.node) + [node]

    def visitNonTerminalNode(self, node: NonTerminalNode) -> list[Node]:
        return [node]

    def visitTerminalNode(self, node: TerminalNode) -> list[Node]:
        return []

    def visitCharSet(self, node: CharSet) -> list[Node]:
        return []

    def traverse_derivation(
        self,
        tree: DerivationTree,
        disambiguator: Optional[Disambiguator] = None,
        paths: Optional[set[tuple[Node, ...]]] = None,
        cur_path: Optional[tuple[Node, ...]] = None,
    ) -> set[tuple[Node, ...]]:
        if disambiguator is None:
            disambiguator = Disambiguator(self, self._grammar_settings)
        if paths is None:
            paths = set()
        if tree.symbol.is_terminal:
            if cur_path is None:
                cur_path = (TerminalNode(tree.terminal, self._grammar_settings),)
            paths.add(cur_path)
        elif isinstance(tree.symbol, NonTerminal):
            if cur_path is None:
                cur_path = (NonTerminalNode(tree.nonterminal, self._grammar_settings),)
            assert tree.symbol == cast(NonTerminalNode, cur_path[-1]).symbol
            disambiguation = disambiguator.visit(self.rules[tree.nonterminal])
            for inner_tree, path in zip(
                tree.children,
                disambiguation[tuple(c.symbol for c in tree.children)],
                strict=False,
            ):
                self.traverse_derivation(
                    inner_tree, disambiguator, paths, cur_path + path
                )
        else:
            raise FandangoValueError(
                f"Unknown symbol type: {type(tree.symbol)}: {tree.symbol}"
            )
        return paths

    def compute_grammar_coverage(
        self, derivation_trees: list[DerivationTree], k: int
    ) -> tuple[float, int, int]:
        """
        Compute the coverage of k-paths in the grammar based on the given derivation trees.

        :param derivation_trees: A list of derivation trees (solutions produced by FANDANGO).
        :param k: The length of the paths (k).
        :return: A float between 0 and 1 representing the coverage.
        """

        # Compute all possible k-paths in the grammar
        all_k_paths = self.generate_all_k_paths(k=k)

        disambiguator = Disambiguator(self, self._grammar_settings)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            for path in self.traverse_derivation(tree, disambiguator):
                # for length in range(1, k + 1):
                for window in range(len(path) - k + 1):
                    covered_k_paths.add(path[window : window + k])

        # Compute coverage
        if not all_k_paths:
            raise FandangoValueError("No k-paths found in the grammar")

        return (
            len(covered_k_paths) / len(all_k_paths),
            len(covered_k_paths),
            len(all_k_paths),
        )

    def get_spec_env(self) -> tuple[dict[str, Any], dict[str, Any]]:
        return self._global_variables, self._local_variables

    def contains_type(
        self, tp: TreeValueType, *, start: str | NonTerminal = "<start>"
    ) -> bool:
        """
        Return true if the grammar can produce an element of type `tp` (say, `int` or `bytes`).
        * `start`: a start symbol other than `<start>`.
        """
        if isinstance(tp, TreeValueType):
            tvt = tp
        else:
            if isinstance(tp, str):
                tvt = TreeValueType.STRING
            elif isinstance(tp, bytes):
                tvt = TreeValueType.BYTES
            elif isinstance(tp, int):
                tvt = TreeValueType.TRAILING_BITS_ONLY
            else:
                raise FandangoValueError(f"Invalid type: {type(tp)}")

        if isinstance(start, str):
            start = NonTerminal(start)

        if start not in self.rules:
            raise FandangoValueError(f"Start symbol {start} not defined in grammar")

        # We start on the right hand side of the start symbol
        start_node = self.rules[start]
        seen = set()

        def node_matches(node: Node) -> bool:
            if node in seen:
                return False
            seen.add(node)

            if isinstance(node, TerminalNode):
                if node.symbol.is_type(tvt):
                    return True
            if any(node_matches(child) for child in node.children()):
                return True
            if isinstance(node, NonTerminalNode):
                return node_matches(self.rules[node.symbol])
            return False

        return node_matches(start_node)

    def contains_bits(self, *, start: str = "<start>") -> bool:
        """
        Return true iff the grammar can produce a bit element (0 or 1).
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(TreeValueType.TRAILING_BITS_ONLY, start=start)

    def contains_bytes(self, *, start: str = "<start>") -> bool:
        """
        Return true iff the grammar can produce a bytes element.
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(TreeValueType.BYTES, start=start)

    def set_max_repetition(self, max_rep: int) -> None:
        nodes.MAX_REPETITIONS = max_rep

    def get_max_repetition(self) -> int:
        return nodes.MAX_REPETITIONS
