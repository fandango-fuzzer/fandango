from typing import List, Set, Tuple, Optional

from ordered_set import OrderedSet

from fandango.language.grammar import (
    Node,
    NodeVisitor,
    Concatenation,
    Repetition,
    NonTerminalNode,
    Star,
    Plus,
    Option,
    TerminalNode,
)
from fandango.language.symbol import NonTerminal, Terminal, Symbol
from fandango.language.tree import DerivationTree


class State:
    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: Tuple[Symbol],
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
            isinstance(other, State)
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
        return State(
            self.nonterminal,
            position or self.position,
            self.symbols,
            self._dot + 1,
            self.children[:],
        )


class Parser(NodeVisitor):
    def __init__(self, grammar):
        self.grammar = grammar
        self._rules = {}
        self._implicit_rules = {}
        self._process()

    def _process(self):
        for nonterminal in self.grammar.rules:
            self._rules[nonterminal] = {
                tuple(a) for a in self.visit(self.grammar.rules[nonterminal])
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

    def predict(self, state: State, table: List[Set[State]], k: int):
        if state.dot in self._rules:
            table[k].update(
                {State(state.dot, k, rule, 0) for rule in self._rules[state.dot]}
            )
        elif state.dot in self._implicit_rules:
            table[k].update(
                {
                    State(state.dot, k, rule, 0)
                    for rule in self._implicit_rules[state.dot]
                }
            )

    @staticmethod
    def scan(state: State, word: str, table: List[Set[State]], k: int):
        if state.dot.check(word[k:]):
            s = state.next()
            s.children.append(DerivationTree(state.dot))
            table[k + len(state.dot)].add(s)

    def complete(self, state: State, table: List[Set[State]], k: int):
        for s in list(table[state.position]):
            if s.dot == state.nonterminal:
                s = s.next()
                table[k].add(s)
                if state.nonterminal in self._rules:
                    s.children.append(DerivationTree(state.nonterminal, state.children))
                else:
                    s.children.extend(state.children)

    def parse_table(self, word, start: str | NonTerminal = "<start>"):
        if isinstance(start, str):
            start = NonTerminal(start)
        table = [OrderedSet() for _ in range(len(word) + 1)]
        table[0].add(State(NonTerminal("<*start*>"), 0, (start,)))
        for k in range(len(word) + 1):
            visited = set()
            while len(visited) < len(table[k]):
                remaining: Set[State] = table[k] - visited
                state: State = remaining.pop()
                visited.add(state)
                if state.finished():
                    self.complete(state, table, k)
                else:
                    if state.next_symbol_is_nonterminal():
                        self.predict(state, table, k)
                    else:
                        self.scan(state, word, table, k)
        return table

    def parse(self, word: str, start: str | NonTerminal = "<start>"):
        if isinstance(start, str):
            start = NonTerminal(start)
        table = [OrderedSet() for _ in range(len(word) + 1)]
        implicit_start = NonTerminal("<*start*>")
        table[0].add(State(implicit_start, 0, (start,)))
        for k in range(len(word) + 1):
            visited = set()
            while len(visited) < len(table[k]):
                remaining: Set[State] = table[k] - visited
                state: State = remaining.pop()
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
