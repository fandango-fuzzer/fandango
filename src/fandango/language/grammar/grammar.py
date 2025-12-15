import random
from collections.abc import Generator, Iterator
from collections import defaultdict
from typing import Any, cast, Optional, Iterable
from collections.abc import Sequence
import warnings


from fandango.errors import FandangoValueError, FandangoParseError
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language.grammar import FuzzingMode, ParsingMode, closest_match
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.literal_generator import LiteralGenerator
from fandango.language.grammar.node_visitors.disambiguator import Disambiguator
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
import fandango.language.grammar.nodes as nodes
from fandango.language.grammar.nodes.repetition import (
    Option,
    Plus,
    Repetition,
    Star,
)
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.parser.parser import Parser
from fandango.language.tree import DerivationTree, TreeTuple
from fandango.language.symbols import Symbol, Terminal, NonTerminal
from fandango.language.tree_value import TreeValueType
from fandango.logger import LOGGER

KPath = tuple[Symbol, ...]


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
        self._k_path_cache: dict[
            tuple[NonTerminal, bool], list[set[tuple[Symbol, ...]]]
        ] = dict()
        self._tree_k_path_cache: dict[int, set[tuple[Symbol, ...]]] = dict()

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
            for child in generated_param.children:
                self.populate_sources(child)
            args.append(generated_param)
        args.pop(0)
        return args

    def derive_generator_output(self, tree: DerivationTree) -> list[DerivationTree]:
        generated = self.generate(tree.nonterminal, tree.sources)
        return generated.children

    def populate_sources(self, tree: DerivationTree) -> None:
        self._rec_remove_sources(tree)
        self._populate_sources(tree)

    def _populate_sources(self, tree: DerivationTree) -> None:
        if self.is_use_generator(tree):
            tree.sources = self.derive_sources(tree)
            for child in tree.children:
                child.set_all_read_only(True)
            return
        for child in tree.children:
            self._populate_sources(child)

    def _rec_remove_sources(self, tree: DerivationTree) -> None:
        tree.sources = []
        for child in tree.children:
            self._rec_remove_sources(child)

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
                "Returning a tree in the shape of a tuple from a generator is deprecated, as it is parsed into a tree, then immediately stringified and parsed against the grammar. You should instead return a str/bytes directly"
            )
            string = str(DerivationTree.from_tree(string))
        tree = self.parse(string, symbol)
        if tree is None:
            raise FandangoParseError(
                f"Could not parse {string!r} (generated by {self.generators[symbol]}) into {symbol.format_as_spec()}"
            )
        tree.sources = [p.deepcopy(copy_parent=False) for p in sources]
        return tree

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        return self._parser.collapse(tree)

    def fuzz(
        self,
        start: str | NonTerminal = "<start>",
        max_nodes: int = 50,
        prefix_node: Optional[DerivationTree] = None,
    ) -> DerivationTree:
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

    def get_protocol_messages(
        self, start_symbol=NonTerminal("<start>")
    ) -> set[PacketNonTerminal]:
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
        return "\n".join(
            [
                f"{key.name()} ::= {value.format_as_spec()}{' := ' + str(self.generators[key]) if key in self.generators else ''}"
                for key, value in self.rules.items()
            ]
        )

    def msg_parties(self, *, include_recipients: bool = True) -> set[str]:
        parties: set[str] = set()
        for rule in self.rules.values():
            parties |= rule.msg_parties(
                grammar=self, include_recipients=include_recipients
            )
        return parties

    def get_repr_for_rule(self, symbol: str | NonTerminal) -> str:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return (
            f"{symbol.format_as_spec()} ::= {self.rules[symbol].format_as_spec()}"
            f"{' := ' + str(self.generators[symbol]) if symbol in self.generators else ''}"
        )

    @staticmethod
    def dummy() -> "Grammar":
        return Grammar(grammar_settings=[], rules={})

    def set_generator(
        self,
        symbol: str | NonTerminal,
        param: str,
        searches_map: dict[str, NonTerminalNode] = {},
    ) -> None:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators[symbol] = LiteralGenerator(
            call=param, nonterminals=searches_map
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

    def get_uncovered_k_paths(
        self,
        derivation_trees: list[DerivationTree],
        k: int,
        non_terminal: NonTerminal = NonTerminal("<start>"),
        overlap_to_root: bool = False,
    ) -> list[tuple[Symbol, ...]]:
        """
        Returns a list of uncovered k-paths in the grammar given a set of derivation trees.
        """
        all_k_paths = self.generate_all_k_paths(
            k=k, non_terminal=non_terminal, overlap_to_root=overlap_to_root
        )
        covered_k_paths = set()
        for tree in derivation_trees:
            covered_k_paths.update(
                self._extract_k_paths_from_tree(tree, k, overlap_to_root)
            )

        uncovered_k_paths = all_k_paths.difference(covered_k_paths)
        return list(uncovered_k_paths)

    def compute_kpath_coverage(
        self,
        derivation_trees: list[DerivationTree],
        k: int,
        non_terminal: NonTerminal = NonTerminal("<start>"),
        overlap_to_root: bool = False,
    ) -> float:
        """
        Computes the k-path coverage of the grammar given a set of derivation trees.
        Returns a score between 0 and 1 representing the fraction of k-paths covered.
        """
        # Generate all possible k-paths in the grammar
        all_k_paths = self.generate_all_k_paths(
            k=k, non_terminal=non_terminal, overlap_to_root=overlap_to_root
        )

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            covered_k_paths.update(
                self._extract_k_paths_from_tree(tree, k, overlap_to_root)
            )
            if len(covered_k_paths) == len(all_k_paths):
                return 1.0

        # Compute coverage score
        if not all_k_paths:
            return 1.0  # If there are no k-paths, coverage is 100%
        return len(covered_k_paths) / len(all_k_paths)

    @staticmethod
    def filter_k_paths(
        included_symbols: set[Symbol],
        k_paths: Iterable[KPath],
        allow_partial_matches: bool = True,
    ) -> set[KPath]:
        filtered_k_paths: set[KPath] = set()
        for k_path in k_paths:
            remaining_path = k_path
            start_idx = 0
            end_idx = len(k_path)
            for idx, symbol in enumerate(remaining_path):
                if symbol not in included_symbols:
                    if not allow_partial_matches:
                        break
                    if idx == start_idx:
                        start_idx += 1
                    else:
                        end_idx = idx
                        break
            if start_idx != len(k_path) and (
                not allow_partial_matches or start_idx == 0 and end_idx == len(k_path)
            ):
                filtered_k_paths.add(k_path[start_idx:end_idx])
        return filtered_k_paths

    def generate_all_k_paths(
        self,
        *,
        k: int,
        non_terminal: NonTerminal = NonTerminal("<start>"),
        overlap_to_root: bool = False,
    ) -> set[KPath]:
        """
        Computes the *k*-paths for this grammar, constructively. See: doi.org/10.1109/ASE.2019.00027

        :param k: The length of the paths.
        :param non_terminal: The non-terminal from which to start generating paths.
        :param overlap_to_root: Whether to include paths that contain the starting symbol but are overlapping with symbols towards the root direction.
        :return: All paths of length up to *k* within this grammar.
        """
        if (non_terminal, overlap_to_root) in self._k_path_cache:
            cache_work = self._k_path_cache[(non_terminal, overlap_to_root)]
            if len(cache_work) >= k:
                return cache_work[k - 1]

        initial: set[Node] = set()
        initial_work: list[Node] = [
            NonTerminalNode(non_terminal, self._grammar_settings)
        ]
        while initial_work:
            node = initial_work.pop(0)
            if node in initial:
                continue
            initial.add(node)
            initial_work.extend(node.descendents(self, filter_controlflow=True))
        work: list[set[tuple[Node, ...]]] = [set((x,) for x in initial)]

        for _ in range(len(work), k):
            next_work = set(work[-1])
            for base in work[-1]:
                for descendent in base[-1].descendents(self, filter_controlflow=True):
                    next_work.add(base + (descendent,))
            work.append(next_work)

        symbol_work = []
        for work_k in work:
            symbol_work_k: set[tuple[Symbol, ...]] = set()
            symbol_work.append(symbol_work_k)
            for path in work_k:
                symbol_work_k.add(tuple(node.to_symbol() for node in path))

        if overlap_to_root:
            all_k_paths = self.generate_all_k_paths(k=k)
            for k_path in all_k_paths:
                if non_terminal in k_path:
                    for idx in range(len(k_path) - 1, k):
                        symbol_work[idx].add(k_path)

        self._k_path_cache[(non_terminal, overlap_to_root)] = symbol_work

        return symbol_work[k - 1]

    def _extract_k_paths_from_tree(
        self, tree: DerivationTree, k: int, overlap_to_root: bool = False
    ) -> set[tuple[Symbol, ...]]:
        """
        Extracts all k-length paths (k-paths) from a derivation tree.
        """

        overlap_parent = tree
        if overlap_to_root:
            for _ in range(k - 1):
                if overlap_parent.parent is not None:
                    overlap_parent = overlap_parent.parent

        hash_key = hash((tree, overlap_parent, k, overlap_to_root))
        if hash_key in self._tree_k_path_cache:
            k_paths = self._tree_k_path_cache[hash_key]
            return k_paths

        start_nodes: list[tuple[Optional[NonTerminal], DerivationTree]] = []

        def collect_start_nodes(tree_root: DerivationTree):
            if not isinstance(tree_root.symbol, NonTerminal):
                return
            for child in tree_root.children:
                start_nodes.append((tree_root.symbol, child))
                collect_start_nodes(child)

        collect_start_nodes(tree)
        start_nodes.append((None, tree))

        paths: list[set[tuple[Symbol, ...]]] = [set() for _ in range(k)]

        def traverse(
            parent_symbol: Optional[NonTerminal], tree_node: DerivationTree, path
        ):
            tree_symbol = tree_node.symbol
            assert isinstance(tree_symbol, (Terminal, NonTerminal))
            if isinstance(tree_symbol, Terminal):
                if parent_symbol is None:
                    raise RuntimeError(
                        "Received a Terminal with no parent symbol when computing k-path!"
                    )
                symbol_value: str | bytes | int
                if tree_symbol.value().is_type(TreeValueType.STRING):
                    symbol_value = tree_symbol.value().to_string()
                elif tree_symbol.value().is_type(TreeValueType.BYTES):
                    symbol_value = tree_symbol.value().to_bytes()
                else:
                    symbol_value = tree_symbol.value().to_int()

                parent_rule_nodes = NonTerminalNode(
                    parent_symbol, self.grammar_settings
                ).descendents(self, filter_controlflow=True)
                parent_rule_terminals = [
                    x for x in parent_rule_nodes if isinstance(x, TerminalNode)
                ]
                random.shuffle(parent_rule_terminals)
                for rule_node in parent_rule_terminals:
                    if rule_node.symbol.check(symbol_value, False)[0]:
                        paths[len(path)].add(path + (rule_node.symbol,))
                return
            new_path = path + (tree_symbol,)
            if len(new_path) <= k:
                paths[len(new_path) - 1].add(new_path)
                if len(new_path) == k:
                    return
            for child in tree_node.children:
                traverse(tree_symbol, child, new_path)

        for parent, node in start_nodes:
            traverse(parent, node, tuple())

        k_paths = set()
        for path_set in paths:
            k_paths.update(path_set)

        if overlap_to_root:
            for path in self._extract_k_paths_from_tree(overlap_parent, k, False):
                if tree.symbol in path:
                    k_paths.add(path)

        self._tree_k_path_cache[hash_key] = k_paths
        return k_paths

    def prime(self) -> None:
        LOGGER.debug("Priming grammar")
        nodes: list[Node] = sum(
            [self.visit(self.rules[symbol]) for symbol in self.rules], []
        )
        while nodes:
            node = nodes.pop(0)
            if isinstance(node, TerminalNode):
                continue
            elif isinstance(node, NonTerminalNode):
                if node.symbol not in self.rules:
                    raise FandangoValueError(
                        f"Symbol {node.symbol.format_as_spec()} not found in grammar"
                    )
                if self.rules[node.symbol].distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        self.rules[node.symbol].distance_to_completion + 1
                    )
            elif isinstance(node, Alternative):
                node.distance_to_completion = (
                    min([n.distance_to_completion for n in node.alternatives]) + 1
                )
                if node.distance_to_completion == float("inf"):
                    nodes.append(node)
            elif isinstance(node, Concatenation):
                if any([n.distance_to_completion == float("inf") for n in node.nodes]):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        sum([n.distance_to_completion for n in node.nodes]) + 1
                    )
            elif isinstance(node, Repetition):
                if node.node.distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        node.node.distance_to_completion * node.min + 1
                    )
            else:
                raise FandangoValueError(f"Unknown node type {node.node_type}")

    def slice_parties(self, parties: list[str]) -> None:
        """
        Returns a new grammar that only contains the rules that are relevant to the given parties.
        """
        for expansion in self.rules.values():
            expansion.slice_parties(parties)
        self.fuzzing_mode = FuzzingMode.COMPLETE

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
            for tree, path in zip(
                tree.children, disambiguation[tuple(c.symbol for c in tree.children)]
            ):
                self.traverse_derivation(tree, disambiguator, paths, cur_path + path)
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
