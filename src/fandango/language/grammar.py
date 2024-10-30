import abc
import enum
import random
from typing import Dict, List, Optional, Tuple, Set, Any, Iterable

from ordered_set import OrderedSet

from fandango.language.symbol import NonTerminal, Terminal, Symbol
from fandango.language.tree import DerivationTree

MAX_REPETITIONS = 5


class NodeType(enum.Enum):
    ALTERNATIVE = 0
    CONCATENATION = 1
    REPETITION = 2
    STAR = 3
    PLUS = 4
    OPTION = 5
    NON_TERMINAL = 6
    TERMINAL = 7
    CHAR_SET = 8


class Node(abc.ABC):
    def __init__(
        self, node_type: NodeType, distance_to_completion: float = float("inf")
    ):
        self.node_type = node_type
        self.distance_to_completion = distance_to_completion

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        return []

    @abc.abstractmethod
    def accept(self, visitor: "NodeVisitor"):
        raise NotImplementedError("accept method not implemented")

    def children(self):
        return []

    def __repr__(self):
        return ""

    def __str__(self):
        return self.__repr__()

    def descendents(self, rules: Dict[str, "Node"]) -> Iterable["Node"]:
        """
        Returns an iterable of the descendents of this node.

        :param rules: The rules upon which to base non-terminal lookups
        :return An iterator over the descendent nodes.
        """
        yield from ()


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        super().__init__(NodeType.ALTERNATIVE)
        self.alternatives = alternatives

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        if self.distance_to_completion >= max_nodes:
            return min(self.alternatives, key=lambda x: x.distance_to_completion).fuzz(
                grammar, 0
            )
        return random.choice(self.alternatives).fuzz(grammar, max_nodes - 1)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitAlternative(self)

    def children(self):
        return self.alternatives

    def __getitem__(self, item):
        return self.alternatives.__getitem__(item)

    def __len__(self):
        return len(self.alternatives)

    def __repr__(self):
        return "(" + "|".join(map(repr, self.alternatives)) + ")"

    def descendents(self, rules: Dict[str, "Node"]) -> Iterable["Node"]:
        yield from self.alternatives


class Concatenation(Node):
    def __init__(self, nodes: list[Node]):
        super().__init__(NodeType.CONCATENATION)
        self.nodes = nodes

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        trees = []
        for node in self.nodes:
            if node.distance_to_completion >= max_nodes:
                tree = node.fuzz(grammar, 0)
            else:
                tree = node.fuzz(grammar, max_nodes - 1)
            trees.extend(tree)
            max_nodes -= sum(t.size() for t in tree)
        return trees

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitConcatenation(self)

    def children(self):
        return self.nodes

    def __getitem__(self, item):
        return self.nodes.__getitem__(item)

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        return " ".join(map(repr, self.nodes))

    def descendents(self, rules: Dict[str, "Node"]) -> Iterable["Node"]:
        yield from self.nodes


class Repetition(Node):
    def __init__(self, node: Node, min_: int = 0, max_: int = MAX_REPETITIONS):
        super().__init__(NodeType.REPETITION)
        if min_ < 0:
            raise ValueError(
                f"Minimum repetitions {min_} must be greater than or equal to 0"
            )
        if max_ <= 0 or max_ < min_:
            raise ValueError(
                f"Maximum repetitions {max_} must be greater than 0 or greater than min {min_}"
            )
        self.node = node
        self.min = min_
        self.max = max_

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitRepetition(self)

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        trees = []
        for rep in range(random.randint(self.min, self.max)):
            if self.node.distance_to_completion >= max_nodes:
                if rep > self.min:
                    break
                tree = self.node.fuzz(grammar, 0)
            else:
                tree = self.node.fuzz(grammar, max_nodes - 1)
            trees.extend(tree)
            max_nodes -= sum(t.size() for t in tree)
        return trees

    def __repr__(self):
        return f"{self.node}{{{self.min},{self.max}}}"

    def descendents(self, rules: Dict[str, "Node"]) -> Iterable["Node"]:
        yield self.node


class Star(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 0)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitStar(self)

    def __repr__(self):
        return f"{self.node}*"


class Plus(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 1)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitPlus(self)

    def __repr__(self):
        return f"{self.node}+"


class Option(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 0, 1)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitOption(self)

    def __repr__(self):
        return f"{self.node}?"

    def descendents(self, rules: Dict[str, "Node"]) -> Iterable["Node"]:
        yield from (self.node, Terminal(""))


class NonTerminalNode(Node):
    def __init__(self, symbol: NonTerminal):
        super().__init__(NodeType.NON_TERMINAL)
        self.symbol = symbol

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        if self.symbol not in grammar:
            raise ValueError(f"Symbol {self.symbol} not found in grammar")
        if self.symbol in grammar.generators:
            return [grammar.generate(self.symbol)]
        children = grammar[self.symbol].fuzz(grammar, max_nodes - 1)
        return [DerivationTree(self.symbol, children)]

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitNonTerminalNode(self)

    def __repr__(self):
        return self.symbol.__repr__()

    def __eq__(self, other):
        return isinstance(other, NonTerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def descendents(self, rules: Dict[str, "Node"]) -> Iterable["Node"]:
        yield from rules[self.symbol].descendents(rules)


class TerminalNode(Node):
    def __init__(self, symbol: Terminal):
        super().__init__(NodeType.TERMINAL, 0)
        self.symbol = symbol

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        return [DerivationTree(self.symbol)]

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitTerminalNode(self)

    def __repr__(self):
        return self.symbol.__repr__()

    def __eq__(self, other):
        return isinstance(other, TerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class CharSet(Node):
    def __init__(self, chars: str):
        super().__init__(NodeType.CHAR_SET, 0)
        self.chars = chars

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        raise NotImplementedError("CharSet fuzzing not implemented")

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitCharSet(self)

    def descendents(self, rules: Dict[str, "Node"]) -> Iterable["Node"]:
        yield from self.chars


class NodeVisitor(abc.ABC):
    def visit(self, node: Node):
        return node.accept(self)

    def default_result(self):
        pass

    def aggregate_results(self, aggregate, result):
        pass

    def visitChildren(self, node: Node) -> Any:
        # noinspection PyNoneFunctionAssignment
        result = self.default_result()
        for child in node.children():
            # noinspection PyNoneFunctionAssignment
            result = self.aggregate_results(result, self.visit(child))
        return result

    def visitAlternative(self, node: Alternative):
        return self.visitChildren(node)

    def visitConcatenation(self, node: Concatenation):
        return self.visitChildren(node)

    def visitRepetition(self, node: Repetition):
        return self.visit(node.node)

    def visitStar(self, node: Star):
        return self.visit(node.node)

    def visitPlus(self, node: Plus):
        return self.visit(node.node)

    def visitOption(self, node: Option):
        return self.visit(node.node)

    # noinspection PyUnusedLocal
    def visitNonTerminalNode(self, node: NonTerminalNode):
        return self.default_result()

    # noinspection PyUnusedLocal
    def visitTerminalNode(self, node: TerminalNode):
        return self.default_result()

    # noinspection PyUnusedLocal
    def visitCharSet(self, node: CharSet):
        return self.default_result()


class ParseState:
    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: Tuple[Symbol, ...],
        dot: int = 0,
        children: Optional[List[DerivationTree]] = None,
    ):
        self.nonterminal = nonterminal
        self.position = position
        self.symbols = symbols
        self._dot = dot
        self.children = children or []

    @property
    def dot(self):
        return self.symbols[self._dot] if self._dot < len(self.symbols) else None

    def finished(self):
        return self._dot >= len(self.symbols)

    def next_symbol_is_nonterminal(self):
        return self._dot < len(self.symbols) and self.symbols[self._dot].is_non_terminal

    def next_symbol_is_terminal(self):
        return self._dot < len(self.symbols) and self.symbols[self._dot].is_terminal

    def __hash__(self):
        return hash((self.nonterminal, self.position, self.symbols, self._dot))

    def __eq__(self, other):
        return (
            isinstance(other, ParseState)
            and self.nonterminal == other.nonterminal
            and self.position == other.position
            and self.symbols == other.symbols
            and self._dot == other._dot
        )

    def __repr__(self):
        return (
            f"({self.nonterminal} -> "
            + "".join(
                [
                    f"{'*' if i == self._dot else ''}{s.symbol}"
                    for i, s in enumerate(self.symbols)
                ]
            )
            + ("*" if self.finished() else "")
            + f", {self.position})"
        )

    def next(self, position: Optional[int] = None):
        return ParseState(
            self.nonterminal,
            position or self.position,
            self.symbols,
            self._dot + 1,
            self.children[:],
        )


class Column:
    def __init__(self, states: Optional[List[ParseState]] = None):
        self.states = states or []
        self.unique = set(self.states)

    def __iter__(self):
        index = 0
        while index < len(self.states):
            yield self.states[index]
            index += 1

    def __len__(self):
        return len(self.states)

    def __getitem__(self, item):
        return self.states[item]

    def __setitem__(self, key, value):
        self.states[key] = value

    def __delitem__(self, key):
        del self.states[key]

    def __contains__(self, item):
        return item in self.unique

    def add(self, state: ParseState):
        if state not in self.unique:
            self.states.append(state)
            self.unique.add(state)
            return True
        return False

    def update(self, states: Set[ParseState]):
        for state in states:
            self.add(state)


class Grammar(NodeVisitor):
    class Parser(NodeVisitor):
        def __init__(self, rules: Dict[NonTerminal, Node]):
            self.grammar_rules = rules
            self._rules = {}
            self._implicit_rules = {}
            self._process()

        def _process(self):
            for nonterminal in self.grammar_rules:
                self._rules[nonterminal] = {
                    tuple(a) for a in self.visit(self.grammar_rules[nonterminal])
                }
            for nonterminal in self._implicit_rules:
                self._implicit_rules[nonterminal] = {
                    tuple(a) for a in self._implicit_rules[nonterminal]
                }

        def get_new_name(self):
            return NonTerminal(f"<*{len(self._implicit_rules)}*>")

        def set_implicit_rule(self, rule: List[List[Node]]) -> NonTerminalNode:
            nonterminal = self.get_new_name()
            self._implicit_rules[nonterminal] = rule
            return nonterminal

        def default_result(self):
            return []

        def aggregate_results(self, aggregate, result):
            aggregate.extend(result)
            return aggregate

        def visitConcatenation(self, node: Concatenation):
            result = [[]]
            for child in node.children():
                to_add = self.visit(child)
                new_result = []
                for r in result:
                    for a in to_add:
                        new_result.append(r + a)
                result = new_result
            return result

        def visitRepetition(self, node: Repetition):
            results = []
            for r in self.visit(node.node):
                for rep in range(node.min, node.max + 1):
                    results.append(r * rep)
            return results

        def visitStar(self, node: Star):
            alternatives = [[]]
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r + [nt])
            return [[nt]]

        def visitPlus(self, node: Plus):
            alternatives = []
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r)
                alternatives.append(r + [nt])
            return [[nt]]

        def visitOption(self, node: Option):
            return [[Terminal("")]] + self.visit(node.node)

        def visitNonTerminalNode(self, node: NonTerminalNode):
            return [[node.symbol]]

        def visitTerminalNode(self, node: TerminalNode):
            return [[node.symbol]]

        def predict(self, state: ParseState, table: List[Set[ParseState]], k: int):
            if state.dot in self._rules:
                table[k].update(
                    {
                        ParseState(state.dot, k, rule, 0)
                        for rule in self._rules[state.dot]
                    }
                )
            elif state.dot in self._implicit_rules:
                table[k].update(
                    {
                        ParseState(state.dot, k, rule, 0)
                        for rule in self._implicit_rules[state.dot]
                    }
                )

        @staticmethod
        def scan(state: ParseState, word: str, table: List[Set[ParseState]], k: int):
            if state.dot.check(word[k:]):
                s = state.next()
                s.children.append(DerivationTree(state.dot))
                table[k + len(state.dot)].add(s)

        def complete(self, state: ParseState, table: List[Set[ParseState]], k: int):
            for s in list(table[state.position]):
                if s.dot == state.nonterminal:
                    s = s.next()
                    table[k].add(s)
                    if state.nonterminal in self._rules:
                        s.children.append(
                            DerivationTree(state.nonterminal, state.children)
                        )
                    else:
                        s.children.extend(state.children)

        def parse_table(self, word, start: str | NonTerminal = "<start>"):
            if isinstance(start, str):
                start = NonTerminal(start)
            table = [Column() for _ in range(len(word) + 1)]
            table[0].add(ParseState(NonTerminal("<*start*>"), 0, (start,)))
            for k in range(len(word) + 1):
                for state in table[k]:
                    if state.finished():
                        self.complete(state, table, k)
                    else:
                        if state.next_symbol_is_nonterminal():
                            self.predict(state, table, k)
                        else:
                            self.scan(state, word, table, k)
            return table

        def parse_forest(self, word: str, start: str | NonTerminal = "<start>"):
            if isinstance(start, str):
                start = NonTerminal(start)
            table = [OrderedSet() for _ in range(len(word) + 1)]
            implicit_start = NonTerminal("<*start*>")
            table[0].add(ParseState(implicit_start, 0, (start,)))
            for k in range(len(word) + 1):
                visited = set()
                while len(visited) < len(table[k]):
                    state: ParseState = list(table[k] - visited)[0]
                    visited.add(state)
                    if state.finished():
                        if state.nonterminal == implicit_start and k == len(word):
                            for child in state.children:
                                yield child
                        self.complete(state, table, k)
                    else:
                        if state.next_symbol_is_nonterminal():
                            self.predict(state, table, k)
                        else:
                            self.scan(state, word, table, k)

        def parse(self, word: str, start: str | NonTerminal = "<start>"):
            for tree in self.parse_forest(word, start):
                return tree
            return None

    def __init__(
        self,
        rules: Optional[Dict[NonTerminal, Node]] = None,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        self.rules = rules or {}
        self.generators = {}
        self._parser = Grammar.Parser(self.rules)
        self._local_variables = local_variables or {}
        self._global_variables = global_variables or {}
        self._visited = set()

    def generate_string(self, symbol: str | NonTerminal = "<start>") -> str:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return eval(
            self.generators[symbol], self._global_variables, self._local_variables
        )

    def generate(self, symbol: str | NonTerminal = "<start>") -> str:
        string = self.generate_string(symbol)
        tree = self.parse(string, symbol)
        if tree is None:
            raise ValueError(
                f"Failed to parse generated string: {string} for {symbol} with generator {self.generators[symbol]}"
            )
        return tree

    def fuzz(
        self, start: str | NonTerminal = "<start>", max_nodes: int = 50
    ) -> DerivationTree:
        if isinstance(start, str):
            start = NonTerminal(start)
        return NonTerminalNode(start).fuzz(self, max_nodes=max_nodes)[0]

    def update(self, grammar: "Grammar" | Dict[NonTerminal, Node]):
        if isinstance(grammar, Grammar):
            generators = grammar.generators
            grammar = grammar.rules
        else:
            generators = {}
        self.rules.update(grammar)
        self.generators.update(generators)
        self._parser = Grammar.Parser(self.rules)
        self.prime()

    def parse(self, word: str, start: str | NonTerminal = "<start>"):
        return self._parser.parse(word, start)

    def __contains__(self, item: str | NonTerminal):
        if isinstance(item, str):
            item = NonTerminal(item)
        return item in self.rules

    def __getitem__(self, item: str | NonTerminal):
        if isinstance(item, str):
            item = NonTerminal(item)
        return self.rules[item]

    def __setitem__(self, key: str | NonTerminal, value: Node):
        if isinstance(key, str):
            key = NonTerminal(key)
        self.rules[key] = value

    def __delitem__(self, key: str | NonTerminal):
        if isinstance(key, str):
            key = NonTerminal(key)
        del self.rules[key]

    def __iter__(self):
        return iter(self.rules)

    def __len__(self):
        return len(self.rules)

    def __repr__(self):
        return "\n".join(
            [
                f"{key} ::= {value}{' :: ' + self.generators[key] if key in self.generators else ''};"
                for key, value in self.rules.items()
            ]
        )

    def get_repr_for_rule(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return (
            f"{symbol} ::= {self.rules[symbol]}"
            f"{' :: ' + self.generators[symbol] if symbol in self.generators else ''};"
        )

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def dummy():
        return Grammar({})

    def set_generator(self, symbol: str | NonTerminal, param: str):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators[symbol] = param

    def has_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return symbol in self.generators

    def get_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return self.generators.get(symbol, None)

    def update_parser(self):
        self._parser = Grammar.Parser(self.rules)

    def compute_kpath_coverage(
        self, derivation_trees: List[DerivationTree], k: int
    ) -> float:
        """
        Computes the k-path coverage of the grammar given a set of derivation trees.
        Returns a score between 0 and 1 representing the fraction of k-paths covered.
        """
        # Generate all possible k-paths in the grammar
        all_k_paths = self._generate_all_k_paths(k)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            covered_k_paths.update(self._extract_k_paths_from_tree(tree, k))

        # Compute coverage score
        if not all_k_paths:
            return 1.0  # If there are no k-paths, coverage is 100%
        return len(covered_k_paths) / len(all_k_paths)

    def _generate_all_k_paths(self, k: int) -> Set[Tuple[str, ...]]:
        """
        Computes the *k*-paths for this grammar, constructively. See: doi.org/10.1109/ASE.2019.00027

        :param k: The length of the paths.
        :return: All *k*-paths of this grammar.
        """

        initial = set()
        initial_work: [Node] = [NonTerminalNode(name) for name in self.rules.keys()]
        while initial_work:
            node = initial_work.pop(0)
            if node in initial:
                continue
            initial.add(node)
            initial_work.extend(node.descendents(self.rules))

        work: [[Node]] = [[x] for x in initial]

        for _ in range(1, k):
            next_work = []
            for base in work:
                for descendent in base[-1].descendents(self.rules):
                    path = base.copy()
                    path.append(descendent)
                    next_work.append(path)
            work = next_work

        return work

    @staticmethod
    def _extract_k_paths_from_tree(
        tree: DerivationTree, k: int
    ) -> Set[Tuple[str, ...]]:
        """
        Extracts all k-length paths (k-paths) from a derivation tree.
        """
        paths = set()

        def traverse(node: DerivationTree, current_path: Tuple[str, ...]):
            new_path = current_path + (node.symbol.symbol,)
            if len(new_path) == k:
                paths.add(new_path)
                # Do not traverse further to keep path length at k
                return
            for child in node.children:
                traverse(child, new_path)

        traverse(tree, ())
        return paths

    def prime(self):
        nodes = sum([self.visit(self.rules[symbol]) for symbol in self.rules], [])
        while nodes:
            node = nodes.pop(0)
            if node.node_type == NodeType.TERMINAL:
                continue
            elif node.node_type == NodeType.NON_TERMINAL:
                if node.symbol not in self.rules:
                    raise ValueError(f"Symbol {node.symbol} not found in grammar")
                if self.rules[node.symbol].distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        self.rules[node.symbol].distance_to_completion + 1
                    )
            elif node.node_type == NodeType.ALTERNATIVE:
                node.distance_to_completion = (
                    min([n.distance_to_completion for n in node.alternatives]) + 1
                )
                if node.distance_to_completion == float("inf"):
                    nodes.append(node)
            elif node.node_type == NodeType.CONCATENATION:
                if any([n.distance_to_completion == float("inf") for n in node.nodes]):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        sum([n.distance_to_completion for n in node.nodes]) + 1
                    )
            elif node.node_type == NodeType.REPETITION:
                if node.node.distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        node.node.distance_to_completion * node.min + 1
                    )
            else:
                raise ValueError(f"Unknown node type {node.node_type}")

    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative):
        return self.visitChildren(node) + [node]

    def visitConcatenation(self, node: Concatenation):
        return self.visitChildren(node) + [node]

    def visitRepetition(self, node: Repetition):
        return self.visit(node.node) + [node]

    def visitStar(self, node: Star):
        return self.visit(node.node) + [node]

    def visitPlus(self, node: Plus):
        return self.visit(node.node) + [node]

    def visitOption(self, node: Option):
        return self.visit(node.node) + [node]

    def visitNonTerminalNode(self, node: NonTerminalNode):
        return [node]

    def visitTerminalNode(self, node: TerminalNode):
        return []

    def visitCharSet(self, node: CharSet):
        return []

    def compute_k_paths(self, k: int) -> Set[Tuple[str, ...]]:
        """
        Computes all possible k-paths in the grammar.

        :param k: The length of the paths.
        :return: A set of tuples, each tuple representing a k-path as a sequence of symbols.
        """
        all_paths = set()
        for start_symbol in self.rules:
            self._compute_paths_from_symbol(start_symbol, k, all_paths)
        return all_paths

    def _compute_paths_from_symbol(
        self, symbol: NonTerminal, k: int, all_paths: Set[Tuple[str, ...]]
    ):
        """
        Computes all k-paths starting from a given symbol.

        :param symbol: The starting NonTerminal symbol.
        :param k: The length of the paths.
        :param all_paths: A set to store the resulting paths.
        """
        visited = set()
        self._compute_k_paths_recursive(symbol, [], all_paths, k, visited)

    def _compute_k_paths_recursive(
        self,
        symbol: Symbol,
        current_path: List[str],
        all_paths: Set[Tuple[str, ...]],
        k: int,
        visited: Set[int],
    ):
        """
        Recursively computes k-paths from the given symbol.

        :param symbol: The current symbol being processed.
        :param current_path: The current path of symbols.
        :param all_paths: A set to store the resulting paths.
        :param k: The desired path length.
        :param visited: A set of visited node IDs to avoid infinite recursion.
        """
        if len(current_path) == k:
            all_paths.add(tuple(current_path))
            return

        current_path.append(symbol.symbol)

        if len(current_path) == k:
            all_paths.add(tuple(current_path))
            current_path.pop()
            return

        if isinstance(symbol, NonTerminal) and symbol in self.rules:
            node = self.rules[symbol]
            self._traverse_node(node, current_path, all_paths, k, visited)
        else:
            # Terminal symbol or undefined NonTerminal; cannot expand further
            if len(current_path) == k:
                all_paths.add(tuple(current_path))
        current_path.pop()

    def _traverse_node(
        self,
        node: Node,
        current_path: List[str],
        all_paths: Set[Tuple[str, ...]],
        k: int,
        visited: Set[int],
    ):
        """
        Traverses a grammar node to compute k-paths.

        :param node: The grammar node to traverse.
        :param current_path: The current path of symbols.
        :param all_paths: A set to store the resulting paths.
        :param k: The desired path length.
        :param visited: A set of visited node IDs to avoid infinite recursion.
        """
        if len(current_path) == k:
            all_paths.add(tuple(current_path))
            return

        node_id = id(node)
        if node_id in visited:
            return
        visited.add(node_id)

        if isinstance(node, Alternative):
            for alternative in node.alternatives:
                self._traverse_node(
                    alternative, current_path, all_paths, k, visited.copy()
                )
        elif isinstance(node, Concatenation):
            for child in node.nodes:
                self._traverse_node(child, current_path, all_paths, k, visited.copy())
        elif isinstance(node, Repetition):
            # For repetitions, consider minimum repetitions to limit paths
            min_reps = max(1, node.min) if node.min > 0 else 1
            for _ in range(min_reps):
                self._traverse_node(
                    node.node, current_path, all_paths, k, visited.copy()
                )
        elif isinstance(node, NonTerminalNode):
            self._compute_k_paths_recursive(
                node.symbol, current_path, all_paths, k, visited.copy()
            )
        elif isinstance(node, TerminalNode):
            current_path.append(node.symbol.symbol)
            if len(current_path) == k:
                all_paths.add(tuple(current_path))
            else:
                # Cannot expand further from a terminal symbol
                pass
            current_path.pop()
        elif isinstance(node, Option):
            # Optionally include the node
            self._traverse_node(node.node, current_path, all_paths, k, visited.copy())
        elif isinstance(node, Star) or isinstance(node, Plus):
            # Similar to Repetition
            self._traverse_node(node.node, current_path, all_paths, k, visited.copy())
        # Add handling for other node types if necessary

        visited.remove(node_id)

    def compute_grammar_coverage(
        self, derivation_trees: List[DerivationTree], k: int
    ) -> float:
        """
        Compute the coverage of k-paths in the grammar based on the given derivation trees.

        :param derivation_trees: A list of derivation trees (solutions produced by FANDANGO).
        :param k: The length of the paths (k).
        :return: A float between 0 and 1 representing the coverage.
        """
        # Compute all possible k-paths in the grammar
        all_k_paths = self.compute_k_paths(k)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            covered_k_paths.update(tree.extract_k_paths(k))

        # Compute coverage
        if not all_k_paths:
            raise ValueError("No k-paths found in the grammar")

        coverage = 0
        for path in all_k_paths:
            if path in covered_k_paths:
                coverage += 1
        coverage /= len(all_k_paths)
        return coverage
