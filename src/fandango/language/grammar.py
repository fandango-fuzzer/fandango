import abc
import enum
import random
import typing
from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Set, Any, Union, Iterator

from fandango.language.symbol import NonTerminal, Terminal, Symbol, Implicit
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

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        """
        Returns an iterator of the descendents of this node.

        :param rules: The rules upon which to base non-terminal lookups.
        :return An iterator over the descendent nodes.
        """
        yield from ()


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        super().__init__(NodeType.ALTERNATIVE)
        self.alternatives = alternatives

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
        if self.distance_to_completion >= max_nodes:
            min_ = min(self.alternatives, key=lambda x: x.distance_to_completion)
            return random.choice(
                [
                    a
                    for a in self.alternatives
                    if a.distance_to_completion <= min_.distance_to_completion
                ]
            ).fuzz(grammar, 0)
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

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
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

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        yield from self.nodes


class Repetition(Node):
    # TODO: Shouldn't a children() method return [self.node]? -- AZ
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

    def descendents(self, rules: Dict[NonTerminal, "Node"] | None) -> Iterator["Node"]:
        base = []
        if self.min == 0:
            base.append(TerminalNode(Terminal("")))
        if self.min <= 1 <= self.max:
            base.append(self.node)
        yield Alternative(
            base
            + [
                Concatenation([self.node] * r)
                for r in range(max(2, self.min), self.max + 1)
            ]
        )


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

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        yield from (self.node, TerminalNode(Terminal("")))


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

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        yield rules[self.symbol]


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

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        for char in self.chars:
            yield TerminalNode(Terminal(char))


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


class Disambiguator(NodeVisitor):
    def __init__(self):
        self.known_disambiguations = {}

    def visit(
        self, node: Node
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        if node in self.known_disambiguations:
            return self.known_disambiguations[node]
        result = super().visit(node)
        self.known_disambiguations[node] = result
        return result

    def visitAlternative(
        self, node: Alternative
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        child_endpoints = {}
        for child in node.children():
            endpoints: Dict[
                Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]
            ] = self.visit(child)
            for children in endpoints:
                # prepend the alternative to all paths
                if not children in child_endpoints:
                    child_endpoints[children] = []
                # join observed paths (these are impossible to disambiguate)
                child_endpoints[children].extend(
                    (node,) + path for path in endpoints[children]
                )

        return child_endpoints

    def visitConcatenation(
        self, node: Concatenation
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        child_endpoints = {(): []}
        for child in node.children():
            next_endpoints = {}
            endpoints: Dict[
                Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]
            ] = self.visit(child)
            for children in endpoints:
                for existing in child_endpoints:
                    concatenation = existing + children
                    if not concatenation in next_endpoints:
                        next_endpoints[concatenation] = []
                    next_endpoints[concatenation].extend(child_endpoints[existing])
                    next_endpoints[concatenation].extend(endpoints[children])
            child_endpoints = next_endpoints

        return {
            children: [(node,) + path for path in child_endpoints[children]]
            for children in child_endpoints
        }

    def visitRepetition(
        self, node: Repetition
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        # repetitions are alternatives over concatenations
        implicit_alternative = next(node.descendents(None))
        return self.visit(implicit_alternative)

    def visitStar(
        self, node: Star
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitPlus(
        self, node: Plus
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitOption(
        self, node: Option
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        implicit_alternative = Alternative(
            [Concatenation([]), Concatenation([node.node])]
        )
        return self.visit(implicit_alternative)

    def visitNonTerminalNode(
        self, node: NonTerminalNode
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitTerminalNode(
        self, node: TerminalNode
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitCharSet(
        self, node: CharSet
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(Terminal(c),): [(node, TerminalNode(Terminal(c)))] for c in node.chars}


class ParseState:
    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: Tuple[Symbol, ...],
        dot: int = 0,
        children: Optional[List[DerivationTree]] = None,
        is_incomplete: bool = False,
    ):
        self.nonterminal = nonterminal
        self.position = position
        self.symbols = symbols
        self._dot = dot
        self.children = children or []
        self.is_incomplete = is_incomplete

    @property
    def dot(self):
        return self.symbols[self._dot] if self._dot < len(self.symbols) else None

    def finished(self):
        return self._dot >= len(self.symbols) and not self.is_incomplete

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

    def __repr__(self):
        return f"Column({self.states})"


class Grammar(NodeVisitor):
    class Parser(NodeVisitor):
        def __init__(
            self,
            rules: Dict[NonTerminal, Node],
        ):
            self.grammar_rules = rules
            self._rules = {}
            self._implicit_rules = {}
            self._process()
            self._cache: Dict[Tuple[str, NonTerminal], DerivationTree] = {}
            self._incomplete = set()

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
            alternatives = self.visit(node.node)
            nt = self.set_implicit_rule(alternatives)
            prev = None
            for rep in range(node.min, node.max):
                alts = [[nt]]
                if prev is not None:
                    alts.append([nt, prev])
                prev = self.set_implicit_rule(alts)
            alts = [node.min * [nt]]
            if prev is not None:
                alts.append(node.min * [nt] + [prev])
            min_nt = self.set_implicit_rule(alts)
            return [[min_nt]]

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

        def complete(
            self,
            state: ParseState,
            table: List[Set[ParseState]],
            k: int,
            use_implicit: bool = False,
        ):
            for s in list(table[state.position]):
                if s.dot == state.nonterminal:
                    s = s.next()
                    table[k].add(s)
                    if state.nonterminal in self._rules:
                        s.children.append(
                            DerivationTree(state.nonterminal, state.children)
                        )
                    else:
                        if use_implicit and state.nonterminal in self._implicit_rules:
                            s.children.append(
                                DerivationTree(
                                    Implicit(state.nonterminal.symbol), state.children
                                )
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

        def parse_forest(
            self,
            word: str,
            start: str | NonTerminal = "<start>",
            allow_incomplete: bool = False,
        ):
            if isinstance(start, str):
                start = NonTerminal(start)
            table = [Column() for _ in range(len(word) + 1)]
            implicit_start = NonTerminal("<*start*>")
            table[0].add(ParseState(implicit_start, 0, (start,)))
            for k in range(len(word) + 1):
                s = 0
                for state in table[k]:
                    s += 1
                    if k == len(word):
                        if allow_incomplete:
                            if state.nonterminal == implicit_start:
                                self._incomplete.update(state.children)
                            state.is_incomplete = True
                            self.complete(
                                state,
                                table,
                                k,
                            )
                    if state.finished():
                        if state.nonterminal == implicit_start and k == len(word):
                            for child in state.children:
                                yield child
                        self.complete(state, table, k)
                    elif not state.is_incomplete:
                        if state.next_symbol_is_nonterminal():
                            self.predict(state, table, k)
                        else:
                            self.scan(state, word, table, k)

        def parse(
            self,
            word: str,
            start: str | NonTerminal = "<start>",
        ):
            if isinstance(start, str):
                start = NonTerminal(start)
            if (word, start) in self._cache:
                return deepcopy(self._cache[(word, start)])
            for tree in self.parse_forest(word, start):
                self._cache[(word, start)] = tree
                return tree
            return None

        def parse_incomplete(
            self,
            word: str,
            start: str | NonTerminal = "<start>",
        ):
            if isinstance(start, str):
                start = NonTerminal(start)
            self._incomplete = set()
            for tree in self.parse_forest(word, start, allow_incomplete=True):
                self._cache[(word, start)] = tree
                yield tree
            for tree in self._incomplete:
                yield tree

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

    def generate_string(self, symbol: str | NonTerminal = "<start>") -> str | Tuple:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return eval(
            self.generators[symbol], self._global_variables, self._local_variables
        )

    def generate(self, symbol: str | NonTerminal = "<start>") -> DerivationTree:
        string = self.generate_string(symbol)
        if not (isinstance(string, str) or isinstance(string, tuple)):
            raise TypeError(
                f"Generator {self.generators[symbol]} must return string or tuple"
            )

        if isinstance(string, tuple):
            return DerivationTree.from_tree(string)
        else:
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

    def parse(
        self,
        word: str,
        start: str | NonTerminal = "<start>",
    ):
        return self._parser.parse(word, start)

    def parse_incomplete(
        self,
        word: str,
        start: str | NonTerminal = "<start>",
    ):
        return self._parser.parse_incomplete(word, start)

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
                f"{key} ::= {value}{' = ' + self.generators[key] if key in self.generators else ''};"
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

    def _generate_all_k_paths(self, k: int) -> Set[Tuple[Node, ...]]:
        """
        Computes the *k*-paths for this grammar, constructively. See: doi.org/10.1109/ASE.2019.00027

        :param k: The length of the paths.
        :return: All paths of length up to *k* within this grammar.
        """

        initial = set()
        initial_work: [Node] = [NonTerminalNode(name) for name in self.rules.keys()]
        while initial_work:
            node = initial_work.pop(0)
            if node in initial:
                continue
            initial.add(node)
            initial_work.extend(node.descendents(self.rules))

        work: List[Set[Tuple[Node]]] = [set((x,) for x in initial)]

        for _ in range(1, k):
            next_work = set()
            for base in work[-1]:
                for descendent in base[-1].descendents(self.rules):
                    next_work.add(base + (descendent,))
            work.append(next_work)

        # return set.union(*work)
        return work[-1]

    @staticmethod
    def _extract_k_paths_from_tree(
        tree: DerivationTree, k: int
    ) -> Set[Tuple[Node, ...]]:
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

    def compute_k_paths(self, k: int) -> Set[Tuple[Node, ...]]:
        """
        Computes all possible k-paths in the grammar.

        :param k: The length of the paths.
        :return: A set of tuples, each tuple representing a k-path as a sequence of symbols.
        """
        return self._generate_all_k_paths(k)

    def traverse_derivation(
        self,
        tree: DerivationTree,
        disambiguator: Disambiguator = Disambiguator(),
        paths: Set[Tuple[Node, ...]] = None,
        cur_path: Tuple[Node, ...] = None,
    ) -> Set[Tuple[Node, ...]]:
        if paths is None:
            paths = set()
        if tree.symbol.is_terminal:
            if cur_path is None:
                cur_path = (TerminalNode(tree.symbol),)
            paths.add(cur_path)
        else:
            if cur_path is None:
                cur_path = (NonTerminalNode(tree.symbol),)
            assert tree.symbol == typing.cast(NonTerminalNode, cur_path[-1]).symbol
            disambiguation = disambiguator.visit(self.rules[tree.symbol])
            for tree, path in zip(
                tree.children, disambiguation[tuple(c.symbol for c in tree.children)]
            ):
                self.traverse_derivation(tree, disambiguator, paths, cur_path + path)
        return paths

    def compute_grammar_coverage(
        self, derivation_trees: List[DerivationTree], k: int
    ) -> Tuple[float, int, int]:
        """
        Compute the coverage of k-paths in the grammar based on the given derivation trees.

        :param derivation_trees: A list of derivation trees (solutions produced by FANDANGO).
        :param k: The length of the paths (k).
        :return: A float between 0 and 1 representing the coverage.
        """

        # Compute all possible k-paths in the grammar
        all_k_paths = self.compute_k_paths(k)

        disambiguator = Disambiguator()

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            for path in self.traverse_derivation(tree, disambiguator):
                # for length in range(1, k + 1):
                for window in range(len(path) - k + 1):
                    covered_k_paths.add(path[window : window + k])

        # Compute coverage
        if not all_k_paths:
            raise ValueError("No k-paths found in the grammar")

        return (
            len(covered_k_paths) / len(all_k_paths),
            len(covered_k_paths),
            len(all_k_paths),
        )
