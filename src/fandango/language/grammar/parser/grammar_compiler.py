from typing import Optional, cast

from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.parser.parse_state import (
    ParserStateSymbolContent,
    RuleAlternative,
)
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import TreeValueType

GrammarCompilerReturnType = list[list[ParserStateSymbolContent]]


class GrammarCompiler(
    NodeVisitor[
        GrammarCompilerReturnType,
        GrammarCompilerReturnType,
    ]
):
    """
    Compiling a grammar into the rule tables the Earley parser works on.
    """

    def __init__(self, grammar_rules: dict[NonTerminal, Node]):
        self.grammar_rules: dict[NonTerminal, Node] = grammar_rules
        self._rules: dict[NonTerminal, set[RuleAlternative]] = {}
        self._implicit_rules: dict[NonTerminal, set[RuleAlternative]] = {}
        self._draft_implicit_rules: dict[NonTerminal, GrammarCompilerReturnType] = {}
        self._context_rules: dict[
            NonTerminal, tuple[Node, ParserStateSymbolContent]
        ] = dict()
        self._tmp_rules: dict[NonTerminal, set[RuleAlternative]] = {}
        #: Control-flow nodes by the name of the symbol standing in for them.
        self._nodes: dict[str, Node] = {}
        self._columns_per_byte_cache: dict[NonTerminal, int] = {}
        self._process()

    def compile_bounded_repetition(
        self,
        node: Repetition,
        nonterminal: ParserStateSymbolContent,
        tree: DerivationTree,
    ) -> ParserStateSymbolContent:
        """
        Recompile a repetition whose bounds depend on the context of the already parsed tree.
        """
        [[symbol]] = self.visitRepetition(node, nonterminal, tree)
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

    def set_rule(
        self, nonterminal: NonTerminal, rule: GrammarCompilerReturnType
    ) -> None:
        self._rules[nonterminal] = {tuple(a) for a in rule}

    def set_implicit_rule(
        self, rule: GrammarCompilerReturnType
    ) -> ParserStateSymbolContent:
        nonterminal = NonTerminal(f"<*{len(self._draft_implicit_rules)}*>")
        self._draft_implicit_rules[nonterminal] = rule
        return (nonterminal, frozenset())

    def set_context_rule(
        self, node: Node, non_terminal: ParserStateSymbolContent
    ) -> NonTerminal:
        nonterminal = NonTerminal(f"<*ctx_{len(self._context_rules)}*>")
        self._context_rules[nonterminal] = (node, non_terminal)
        return nonterminal

    def set_tmp_rule(self, rule: GrammarCompilerReturnType) -> ParserStateSymbolContent:
        nonterminal = NonTerminal(f"<*tmp_{len(self._tmp_rules)}*>")
        self._tmp_rules[nonterminal] = {tuple(a) for a in rule}
        return (nonterminal, frozenset())

    def _clear_tmp(self) -> None:
        self._tmp_rules.clear()

    def default_result(self) -> GrammarCompilerReturnType:
        return []

    def aggregate_results(
        self,
        aggregate: GrammarCompilerReturnType,
        result: GrammarCompilerReturnType,
    ) -> GrammarCompilerReturnType:
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative) -> GrammarCompilerReturnType:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result = self.visitChildren(node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitConcatenation(self, node: Concatenation) -> GrammarCompilerReturnType:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: GrammarCompilerReturnType = [[]]
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
        nt: Optional[ParserStateSymbolContent] = None,
        tree: Optional[DerivationTree] = None,
    ) -> GrammarCompilerReturnType:
        repetition_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[repetition_nt.name()] = node
        is_context = node.bounds_constraint is not None

        if nt is None:
            alternatives = self.visit(node.node)
            nt = self.set_implicit_rule(alternatives)

            if is_context:
                i_nt = self.set_context_rule(node, nt)
                self.set_rule(repetition_nt, [[(i_nt, frozenset())]])
                return [[(repetition_nt, frozenset())]]

        prev = None
        if node.bounds_constraint is not None:
            assert tree is not None
            right_most_node = tree
            while len(right_most_node.children) != 0:
                right_most_node = right_most_node.children[-1]
            node_min, _ = node.bounds_constraint.min(right_most_node)
            node_max, _ = node.bounds_constraint.max(right_most_node)
        else:
            node_min = node.min
            node_max = node.max
        for _rep in range(node_min, node_max):
            alts = [[nt]]
            if prev is not None:
                alts.append([nt, prev])
            if is_context:
                prev = self.set_tmp_rule(alts)
            else:
                prev = self.set_implicit_rule(alts)
        alts = [node_min * [nt]]
        if prev is not None:
            alts.append(node_min * [nt] + [prev])
        if is_context:
            return [[self.set_tmp_rule(alts)]]
        min_nt = self.set_implicit_rule(alts)
        self.set_rule(repetition_nt, [[min_nt]])
        return [[(repetition_nt, frozenset())]]

    def visitStar(self, node: Star) -> GrammarCompilerReturnType:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: GrammarCompilerReturnType = [[]]
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitPlus(self, node: Plus) -> GrammarCompilerReturnType:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: GrammarCompilerReturnType = []
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r)
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitOption(self, node: Option) -> GrammarCompilerReturnType:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: GrammarCompilerReturnType = [[]] + self.visit(node.node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitNonTerminalNode(self, node: NonTerminalNode) -> GrammarCompilerReturnType:
        params = dict()
        if node.sender is not None:
            params["sender"] = node.sender
        if node.recipient is not None:
            params["recipient"] = node.recipient
        parameters = frozenset(params.items())
        return [[(node.symbol, parameters)]]

    def visitTerminalNode(self, node: TerminalNode) -> GrammarCompilerReturnType:
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
                for entry in alternative:
                    symbol = entry[0]
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
