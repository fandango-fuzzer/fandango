"""
This parser is inspired by the early parser algorithm.
From the Fuzzingbook https://www.fuzzingbook.org/html/Parser.html#The-Earley-Parser"""
import itertools
from typing import Optional, List, Set, Generator

from fandango.constraints.base import Constraint
from fandango.language.grammar import Grammar
from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree


class Column:
    def __init__(self, index, letter):
        self.index, self.letter = index, letter
        self.states, self._unique = [], {}

    def __str__(self):
        return "%s chart[%d]\n%s" % (
            self.letter,
            self.index,
            "\n".join(str(state) for state in self.states if state.finished()),
        )

    def add(self, state):
        if state in self._unique:
            return self._unique[state]
        self._unique[state] = state
        self.states.append(state)
        state.e_col = self
        return self._unique[state]


class Item:
    def __init__(self, name, expr, dot):
        self.name, self.expr, self.dot = name, expr, dot

    def finished(self):
        return self.dot >= len(self.expr)

    def advance(self):
        return Item(self.name, self.expr, self.dot + 1)

    def at_dot(self):
        return self.expr[self.dot] if self.dot < len(self.expr) else None


class State(Item):
    def __init__(self, name, expr, dot, s_col, e_col=None):
        super().__init__(name, expr, dot)
        self.s_col, self.e_col = s_col, e_col

    def __str__(self):
        def idx(var):
            return var.index if var else -1

        return (
            self.name
            + ":= "
            + " ".join(
                [str(p) for p in [*self.expr[: self.dot], "|", *self.expr[self.dot :]]]
            )
            + "(%d,%d)" % (idx(self.s_col), idx(self.e_col))
        )

    def copy(self):
        return State(self.name, self.expr, self.dot, self.s_col, self.e_col)

    def _t(self):
        return self.name, self.expr, self.dot, self.s_col.index

    def __hash__(self):
        return hash(self._t())

    def __eq__(self, other):
        return self._t() == other._t()

    def advance(self):
        return State(self.name, self.expr, self.dot + 1, self.s_col)


class Parser:
    def __init__(
        self,
        grammar: Grammar,
        constraints: Optional[List[Constraint]] = None,
        coalesce: bool = True,
        tokens: Set[str] = None,
    ):
        self.grammar = grammar
        self.constraints = constraints or []
        self.chart: List = []
        self.coalesce_tokens = coalesce
        self.tokens = tokens or set()
        self.table = []

    def parse(self, text, symbol: NonTerminal):
        cursor, states = self.parse_prefix(text, symbol)
        start = next((s for s in states if s.finished()), None)

        if cursor < len(text) or not start:
            raise SyntaxError("at " + repr(text[cursor:]))

        forest = self.parse_forest(self.table, start)
        for tree in self.extract_trees(forest):
            yield self.prune_tree(tree)

    def parse_on(self, text: str, symbol: NonTerminal) -> Generator:
        yield from self.parse(text, symbol)

    def coalesce(self, children: List[DerivationTree]) -> List[DerivationTree]:
        last = ""
        new_lst: List[DerivationTree] = []
        for cn, cc in children:
            if cn not in self.grammar:
                last += cn
            else:
                if last:
                    new_lst.append((last, []))
                    last = ""
                new_lst.append((cn, cc))
        if last:
            new_lst.append((last, []))
        return new_lst

    def prune_tree(self, tree: DerivationTree) -> DerivationTree:
        name, children = tree
        assert isinstance(children, list)

        if self.coalesce_tokens:
            children = self.coalesce(children)
        if name in self.tokens:
            return DerivationTree(name, [str(tree)])
        else:
            return DerivationTree(name, [self.prune_tree(c) for c in children])

    def chart_parse(self, words, start):
        alt = self.grammar[start]
        chart = [Column(i, tok) for i, tok in enumerate([None, *words])]
        chart[0].add(State(start, alt, 0, chart[0]))
        return self.fill_chart(chart)

    def predict(self, col, sym):
        for alt in self.grammar[sym]:
            col.add(State(sym, tuple(alt), 0, col))

    @staticmethod
    def scan(col, state, letter):
        if letter == col.letter:
            col.add(state.advance())

    def complete(self, col, state):
        return self.earley_complete(col, state)

    @staticmethod
    def earley_complete(col, state):
        parent_states = [st for st in state.s_col.states if st.at_dot() == state.name]
        for st in parent_states:
            col.add(st.advance())

    def fill_chart(self, chart):
        for i, col in enumerate(chart):
            for state in col.states:
                if state.finished():
                    self.complete(col, state)
                else:
                    sym = state.at_dot()
                    if sym in self.grammar:
                        self.predict(col, sym)
                    else:
                        if i + 1 >= len(chart):
                            continue
                        self.scan(chart[i + 1], state, sym)
        return chart

    def parse_prefix(self, text, symbol: NonTerminal):
        self.table = self.chart_parse(text, symbol)
        for col in reversed(self.table):
            states = [st for st in col.states if st.name == symbol]
            if states:
                return col.index, states
        return -1, []

    def parse_paths(self, named_expr, chart, frm, til):
        def paths(state, start, k, e):
            if not e:
                return [[(state, k)]] if start == frm else []
            else:
                return [
                    [(state, k)] + r for r in self.parse_paths(e, chart, frm, start)
                ]

        *expr, var = named_expr
        if var not in self.grammar:
            starts = (
                [(var, til - len(var), "t")]
                if til > 0 and chart[til].letter == var
                else []
            )
        else:
            starts = [
                (s, s.s_col.index, "n")
                for s in chart[til].states
                if s.finished() and s.name == var
            ]

        return [p for s, start, k in starts for p in paths(s, start, k, expr)]

    def forest(self, s, kind, chart):
        return self.parse_forest(chart, s) if kind == "n" else (s, [])

    def parse_forest(self, chart, state):
        path_exprs = (
            self.parse_paths(state.expr, chart, state.s_col.index, state.e_col.index)
            if state.expr
            else []
        )
        return state.name, [
            [(v, k, chart) for v, k in reversed(path_expr)] for path_expr in path_exprs
        ]

    def extract_a_tree(self, forest_node):
        name, paths = forest_node
        if not paths:
            return name, []
        return name, [self.extract_a_tree(self.forest(*p)) for p in paths[0]]

    def extract_trees(self, forest_node):
        name, paths = forest_node
        if not paths:
            yield name, []

        for path in paths:
            p_trees = [self.extract_trees(self.forest(*p)) for p in path]
            for p in itertools.product(*p_trees):
                yield name, p
