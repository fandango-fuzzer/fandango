import abc
import random
from typing import Dict, List, Optional, Tuple, Set, Any

from ordered_set import OrderedSet

from fandango.language.symbol import NonTerminal, Terminal, Symbol
from fandango.language.tree import DerivationTree

MAX_REPETITIONS = 50


class Node(abc.ABC):
    def fuzz(self, grammar: "Grammar") -> List[DerivationTree]:
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


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        self.alternatives = alternatives

    def fuzz(self, grammar: "Grammar") -> List[DerivationTree]:
        return random.choice(self.alternatives).fuzz(grammar)

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


class Concatenation(Node):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def fuzz(self, grammar: "Grammar") -> List[DerivationTree]:
        return sum([node.fuzz(grammar) for node in self.nodes], [])

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


class Repetition(Node):
    def __init__(self, node: Node, min_: int = 0, max_: int = MAX_REPETITIONS):
        if min_ < 0:
            raise ValueError("Minimum repetitions must be greater than or equal to 0")
        if max_ <= 0:
            raise ValueError("Maximum repetitions must be greater than 0")
        self.node = node
        self.min = min_
        self.max = max_

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitRepetition(self)

    def fuzz(self, grammar: "Grammar") -> List[DerivationTree]:
        return sum(
            [
                self.node.fuzz(grammar)
                for _ in range(random.randint(self.min, self.max))
            ],
            [],
        )

    def __repr__(self):
        return f"{self.node}{{{self.min},{self.max}}}"


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


class NonTerminalNode(Node):
    def __init__(self, symbol: NonTerminal):
        self.symbol = symbol

    def fuzz(self, grammar: "Grammar") -> List[DerivationTree]:
        if self.symbol not in grammar:
            raise ValueError(f"Symbol {self.symbol} not found in grammar")
        if self.symbol in grammar.generators:
            return [grammar.generate(self.symbol)]
        children = grammar[self.symbol].fuzz(grammar)
        return [DerivationTree(self.symbol, children)]

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitNonTerminalNode(self)

    def __repr__(self):
        return self.symbol.__repr__()

    def __eq__(self, other):
        return isinstance(other, NonTerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class TerminalNode(Node):
    def __init__(self, symbol: Terminal):
        self.symbol = symbol

    def fuzz(self, grammar: "Grammar") -> List[DerivationTree]:
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
        self.chars = chars

    def fuzz(self, grammar: "Grammar") -> List[DerivationTree]:
        raise NotImplementedError("CharSet fuzzing not implemented")

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitCharSet(self)


class NodeVisitor(abc.ABC):
    def visit(self, node: Node):
        return node.accept(self)

    def default_result(self):
        pass

    def aggregate_results(self, aggregate, result):
        pass

    def visitChildren(self, node: Node):
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


class Grammar:
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
            table = [OrderedSet() for _ in range(len(word) + 1)]
            table[0].add(ParseState(NonTerminal("<*start*>"), 0, (start,)))
            for k in range(len(word) + 1):
                visited = set()
                while len(visited) < len(table[k]):
                    remaining: Set[ParseState] = table[k] - visited
                    state: ParseState = remaining.pop()
                    visited.add(state)
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

    def fuzz(self, start: str | NonTerminal = "<start>") -> DerivationTree:
        if isinstance(start, str):
            start = NonTerminal(start)
        return NonTerminalNode(start).fuzz(self)[0]

    def update(self, grammar: "Grammar" | Dict[NonTerminal, Node]):
        if isinstance(grammar, Grammar):
            generators = grammar.generators
            grammar = grammar.rules
        else:
            generators = {}
        self.rules.update(grammar)
        self.generators.update(generators)
        self._parser = Grammar.Parser(self.rules)

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