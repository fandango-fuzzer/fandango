from collections.abc import Sequence
from typing import NamedTuple, Optional

from fandango.io.navigation.step import Step
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols.non_terminal import NonTerminal


class Pruned(NamedTuple):
    node: Optional[Node]
    removes_parent: bool = False


class BlockedStepPruner(NodeVisitor[list[Pruned], Pruned]):
    """
    Removes the blocked steps from a state grammar, and every part of a rule that can only be derived through them.
    An alternative left able to derive nothing is wrapped in an Option with an id of its own, which the original
    grammar does not have. Analyse only trees parsed with the pruned grammar against it, never trees of another grammar.
    """

    def __init__(self, grammar_settings: Sequence[HasSettings]):
        self._grammar_settings = grammar_settings
        self._blocked_edges: set[Step] = set()
        self._emptied_edges: set[Step] = set()
        self._current_blocked_parent: Optional[NonTerminal] = None

    def prune(
        self,
        state_rules: dict[NonTerminal, Node],
        start_symbol: NonTerminal,
        blocked_steps: frozenset[Step],
    ) -> dict[NonTerminal, Node]:
        """
        Returns the state rules without the blocked steps.
        Rules left without a derivation, or no longer reachable from the start symbol, are removed.
        """
        # The blocked steps, and the edges into every rule removed on the way.
        self._blocked_edges = set(blocked_steps)
        # The edges into every rule that can only derive nothing any more.
        self._emptied_edges = set()
        rules = dict(state_rules)
        referring_symbols = self._find_referring_symbols(rules)
        pending = {parent for parent, _child in blocked_steps}
        while pending:
            blocked_parent = pending.pop()
            if blocked_parent not in rules:
                continue
            self._current_blocked_parent = blocked_parent
            body = self.visit(rules[blocked_parent])
            if body.node is not None:
                rules[blocked_parent] = body.node
                continue
            del rules[blocked_parent]
            edges = self._blocked_edges if body.removes_parent else self._emptied_edges
            for referring_symbol in referring_symbols.get(blocked_parent, set()):
                edges.add((referring_symbol, blocked_parent))
                pending.add(referring_symbol)
        return self._reachable_rules(rules, start_symbol)

    @staticmethod
    def _reachable_rules(
        rules: dict[NonTerminal, Node], start_symbol: NonTerminal
    ) -> dict[NonTerminal, Node]:
        reachable_symbols = {start_symbol}
        pending_symbols = [start_symbol]
        while pending_symbols:
            symbol = pending_symbols.pop()
            if symbol not in rules:
                continue
            pending_nodes = [rules[symbol]]
            while pending_nodes:
                node = pending_nodes.pop()
                if isinstance(node, NonTerminalNode):
                    if node.symbol not in reachable_symbols:
                        reachable_symbols.add(node.symbol)
                        pending_symbols.append(node.symbol)
                    continue
                pending_nodes.extend(node.children())
        return {
            symbol: body
            for symbol, body in rules.items()
            if symbol in reachable_symbols
        }

    @staticmethod
    def _find_referring_symbols(
        rules: dict[NonTerminal, Node],
    ) -> dict[NonTerminal, set[NonTerminal]]:
        referring_symbols: dict[NonTerminal, set[NonTerminal]] = {}
        for symbol, body in rules.items():
            pending = [body]
            while pending:
                node = pending.pop()
                if isinstance(node, NonTerminalNode):
                    referring_symbols.setdefault(node.symbol, set()).add(symbol)
                pending.extend(node.children())
        return referring_symbols

    def default_result(self) -> list[Pruned]:
        return []

    def aggregate_results(
        self, aggregate: list[Pruned], result: Pruned
    ) -> list[Pruned]:
        aggregate.append(result)
        return aggregate

    def visitNonTerminalNode(self, node: NonTerminalNode) -> Pruned:
        edge = (self._current_blocked_parent, node.symbol)
        if edge in self._blocked_edges:
            return Pruned(None, removes_parent=True)
        if edge in self._emptied_edges:
            return Pruned(None, removes_parent=False)
        return Pruned(node)

    def visitTerminalNode(self, node: TerminalNode) -> Pruned:
        return Pruned(node)

    def visitCharSet(self, node: CharSet) -> Pruned:
        return Pruned(node)

    def visitConcatenation(self, node: Concatenation) -> Pruned:
        nodes: list[Node] = []
        for child in node.nodes:
            pruned_child = self.visit(child)
            if pruned_child.removes_parent:
                return Pruned(None, removes_parent=True)
            if pruned_child.node is not None:
                nodes.append(pruned_child.node)
        if len(nodes) == 0:
            return Pruned(None, removes_parent=False)
        concatenation = Concatenation(nodes, self._grammar_settings, node.id)
        return Pruned(concatenation)

    def visitAlternative(self, node: Alternative) -> Pruned:
        alternatives: list[Node] = []
        may_derive_nothing = False
        for alternative in node.alternatives:
            pruned_alternative = self.visit(alternative)
            if pruned_alternative.node is not None:
                alternatives.append(pruned_alternative.node)
            elif not pruned_alternative.removes_parent:
                may_derive_nothing = True
        if len(alternatives) == 0:
            return Pruned(None, removes_parent=not may_derive_nothing)
        remaining = Alternative(
            alternatives,
            self._grammar_settings,
            node.id,
            is_permutation=node.is_permutation,
        )
        if may_derive_nothing:
            option = Option(
                remaining, self._grammar_settings, f"{NodeType.OPTION}:{node.id}"
            )
            return Pruned(option)
        return Pruned(remaining)

    def visitRepetition(self, node: Repetition) -> Pruned:
        body = self.visit(node.node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        repetition = Repetition(
            body.node, self._grammar_settings, node.id, node.min, node.internal_max
        )
        repetition.bounds_constraint = node.bounds_constraint
        return Pruned(repetition)

    def visitOption(self, node: Option) -> Pruned:
        body = self.visit(node.node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        option = Option(body.node, self._grammar_settings, node.id)
        return Pruned(option)

    def visitPlus(self, node: Plus) -> Pruned:
        body = self.visit(node.node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        plus = Plus(body.node, self._grammar_settings, node.id)
        return Pruned(plus)

    def visitStar(self, node: Star) -> Pruned:
        body = self.visit(node.node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        star = Star(body.node, self._grammar_settings, node.id)
        return Pruned(star)

    @staticmethod
    def _repetition_without_body(node: Repetition, body: Pruned) -> Pruned:
        """A repetition whose body is gone is removed if it must repeat also propagate removals to parents."""
        return (
            Pruned(None, removes_parent=True)
            if body.removes_parent and node.min > 0
            else Pruned(None, removes_parent=False)
        )
