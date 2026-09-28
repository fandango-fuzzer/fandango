from typing import Optional

from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.parser.parse_state import (
    RuleAlternative,
    RuleSymbol,
)
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import TreeValueType

DraftAlternatives = list[list[RuleSymbol]]


class GrammarCompiler(
    NodeVisitor[
        DraftAlternatives,
        DraftAlternatives,
    ]
):
    """
    Compiling a grammar into the rule tables the Earley parser works on.
    """

    def __init__(self, grammar_rules: dict[NonTerminal, Node]):
        self.grammar_rules: dict[NonTerminal, Node] = grammar_rules
        self._rules: dict[NonTerminal, set[RuleAlternative]] = {}
        self._implicit_rules: dict[NonTerminal, set[RuleAlternative]] = {}
        self._draft_implicit_rules: dict[NonTerminal, DraftAlternatives] = {}
        self._context_rules: dict[NonTerminal, tuple[Node, RuleSymbol]] = dict()
        self._tmp_rules: dict[NonTerminal, set[RuleAlternative]] = {}
        #: Control-flow nodes by the name of the symbol standing in for them.
        self._nodes: dict[str, Node] = {}
        self._columns_per_byte_cache: dict[NonTerminal, int] = {}
        self._process()

    def compile_bounded_repetition(
        self,
        node: Repetition,
        rule_symbol: RuleSymbol,
        tree: DerivationTree,
    ) -> RuleSymbol:
        """
        Recompile a repetition whose bounds depend on the context of the already parsed tree.
        """
        [[symbol]] = self.visitRepetition(node, rule_symbol, tree)
        return symbol

    def _process(self) -> None:
        self._rules.clear()
        self._implicit_rules.clear()
        self._draft_implicit_rules.clear()
        self._context_rules.clear()
        for nonterminal in self.grammar_rules:
            self.set_rule(nonterminal, self.visit(self.grammar_rules[nonterminal]))

        for nonterminal, alternatives in self._draft_implicit_rules.items():
            self._implicit_rules[nonterminal] = {tuple(a) for a in alternatives}
        self._draft_implicit_rules.clear()

    def set_rule(self, nonterminal: NonTerminal, rule: DraftAlternatives) -> None:
        self._rules[nonterminal] = {tuple(a) for a in rule}

    def set_implicit_rule(self, rule: DraftAlternatives) -> RuleSymbol:
        nonterminal = NonTerminal(f"<*{len(self._draft_implicit_rules)}*>")
        self._draft_implicit_rules[nonterminal] = rule
        return (nonterminal, frozenset())

    def set_context_rule(self, node: Node, rule_symbol: RuleSymbol) -> NonTerminal:
        nonterminal = NonTerminal(f"<*ctx_{len(self._context_rules)}*>")
        self._context_rules[nonterminal] = (node, rule_symbol)
        return nonterminal

    def set_tmp_rule(self, rule: DraftAlternatives) -> RuleSymbol:
        nonterminal = NonTerminal(f"<*tmp_{len(self._tmp_rules)}*>")
        self._tmp_rules[nonterminal] = {tuple(a) for a in rule}
        return (nonterminal, frozenset())

    def _clear_tmp(self) -> None:
        self._tmp_rules.clear()

    def default_result(self) -> DraftAlternatives:
        return []

    def aggregate_results(
        self,
        aggregate: DraftAlternatives,
        result: DraftAlternatives,
    ) -> DraftAlternatives:
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result = self.visitChildren(node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitConcatenation(self, node: Concatenation) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: DraftAlternatives = [[]]
        for child in node.children():
            to_add = self.visit(child)
            new_result = []
            for r in result:
                for a in to_add:
                    new_result.append(r + a)
            result = new_result
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitRepetition(
        self,
        node: Repetition,
        element: Optional[RuleSymbol] = None,
        tree: Optional[DerivationTree] = None,
    ) -> DraftAlternatives:
        repetition_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[repetition_nt.name()] = node
        is_context = node.bounds_constraint is not None

        if element is None:
            alternatives = self.visit(node.node)
            element = self.set_implicit_rule(alternatives)

            if is_context:
                context_nt = self.set_context_rule(node, element)
                self.set_rule(repetition_nt, [[(context_nt, frozenset())]])
                return [[(repetition_nt, frozenset())]]

        more = None
        if node.bounds_constraint is not None:
            assert tree is not None
            rightmost_leaf = tree
            while len(rightmost_leaf.children) != 0:
                rightmost_leaf = rightmost_leaf.children[-1]
            node_min, _ = node.bounds_constraint.min(rightmost_leaf)
            node_max, _ = node.bounds_constraint.max(rightmost_leaf)
        else:
            node_min = node.min
            node_max = node.max
        for _rep in range(node_min, node_max):
            alts = [[element]]
            if more is not None:
                alts.append([element, more])
            if is_context:
                more = self.set_tmp_rule(alts)
            else:
                more = self.set_implicit_rule(alts)
        alts = [node_min * [element]]
        if more is not None:
            alts.append(node_min * [element] + [more])
        if is_context:
            return [[self.set_tmp_rule(alts)]]
        min_symbol = self.set_implicit_rule(alts)
        self.set_rule(repetition_nt, [[min_symbol]])
        return [[(repetition_nt, frozenset())]]

    def visitStar(self, node: Star) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: DraftAlternatives = [[]]
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitPlus(self, node: Plus) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: DraftAlternatives = []
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r)
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitOption(self, node: Option) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: DraftAlternatives = [[]] + self.visit(node.node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitNonTerminalNode(self, node: NonTerminalNode) -> DraftAlternatives:
        params = dict()
        if node.sender is not None:
            params["sender"] = node.sender
        if node.recipient is not None:
            params["recipient"] = node.recipient
        parameters = frozenset(params.items())
        return [[(node.symbol, parameters)]]

    def visitTerminalNode(self, node: TerminalNode) -> DraftAlternatives:
        return [[(node.symbol, frozenset())]]

    def columns_per_byte_for(self, start: NonTerminal) -> int:
        """
        8 if any binary terminal is reachable from `start`, else 1.
        """
        cached = self._columns_per_byte_cache.get(start)
        if cached is not None:
            return cached

        result = 1
        seen: set[NonTerminal] = set()
        stack: list[NonTerminal] = [start]
        while stack:
            nonterminal = stack.pop()
            if nonterminal in seen:
                continue
            seen.add(nonterminal)

            alternatives = self._rules.get(nonterminal)
            if alternatives is None:
                alternatives = self._implicit_rules.get(nonterminal)
            if alternatives is None:
                context = self._context_rules.get(nonterminal)
                if context is not None:
                    inner = context[1][0]
                    if isinstance(inner, NonTerminal):
                        stack.append(inner)
                    continue
                result = 8
                break

            for alternative in alternatives:
                for rule_symbol in alternative:
                    symbol = rule_symbol[0]
                    if symbol.is_terminal:
                        if symbol.is_type(TreeValueType.TRAILING_BITS_ONLY):
                            result = 8
                            stack.clear()
                            break
                    elif isinstance(symbol, NonTerminal):
                        stack.append(symbol)
                if result == 8:
                    break
            if result == 8:
                break

        self._columns_per_byte_cache[start] = result
        return result
