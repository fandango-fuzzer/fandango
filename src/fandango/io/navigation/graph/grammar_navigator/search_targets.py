from collections.abc import Hashable, Sequence
from typing import NamedTuple, Optional

from fandango.io.navigation.graph.grammar_navigator.future_keys import FutureKeys
from fandango.io.navigation.graph.grammar_navigator.grammar_graph_converter import (
    GrammarGraphNode,
)
from fandango.io.navigation.graph.grammar_navigator.path_search import SearchTarget
from fandango.io.navigation.graph.grammar_navigator.rule_costs import RuleCosts
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols import Symbol


class RunEndTarget(SearchTarget):
    """The end of the run as target of a path search: reached by a node at which the run may end."""

    def __init__(self) -> None:
        self._futures = FutureKeys()

    def is_reached(self, node: GrammarGraphNode) -> bool:
        return node.is_accepting

    def estimate(self, node: GrammarGraphNode) -> int:
        return 1

    def state(self, node: GrammarGraphNode) -> Hashable:
        return self._futures.key(node)


class KPathMatcher:
    """Tells how many leading symbols of a k-path a sequence of symbols ends with, one symbol at a time."""

    def __init__(self, k_path: Sequence[Symbol]):
        self._k_path = list(k_path)
        # Per matched length, the next shorter length that the matched symbols also end with.
        self._fallbacks = [0] * len(self._k_path)
        matched = 0
        for i in range(1, len(self._k_path)):
            while matched > 0 and self._k_path[i] != self._k_path[matched]:
                matched = self._fallbacks[matched - 1]
            if self._k_path[i] == self._k_path[matched]:
                matched += 1
            self._fallbacks[i] = matched

    def matched_after(self, matched: int, symbol: Symbol) -> int:
        """Returns the matched length after symbol is appended to a sequence with the given matched length."""
        if matched == len(self._k_path):
            matched = self._fallbacks[matched - 1]
        while matched > 0 and self._k_path[matched] != symbol:
            matched = self._fallbacks[matched - 1]
        if self._k_path[matched] == symbol:
            matched += 1
        return matched


class ChainSummary(NamedTuple):
    """What a k-path search knows about the chain of a graph node."""

    # Symbols on the chain.
    length: int
    # Leading symbols of the chain that follow the forbidden chain.
    shared_with_forbidden_path: int
    # Matched lengths of the k-path at the last symbols of the chain, the node's own last.
    recent_matched_lengths: tuple[int, ...]
    # Cheapest cost from the end of the node to each symbol of the k-path.
    costs_after: tuple[int, ...]


class KPathTarget(SearchTarget):
    """A k-path as target of a path search: reached by a node whose chain ends with the k-path."""

    ANCESTOR_LOOKBACK = 6
    # Outweighs every cost, so matching one more symbol of the k-path always comes first.
    UNMATCHED_SYMBOL_COST = 1_000_000

    def __init__(
        self,
        k_path: KPath,
        costs: RuleCosts,
        forbidden_chain: tuple[Symbol, ...] = (),
    ):
        """
        forbidden_chain is the chain of an existing derivation whose match of the k-path cannot be completed.
        Whatever a chain shares with it from the start does not count as progress.
        """
        self._k_path = k_path
        self._matcher = KPathMatcher(k_path)
        self._costs = costs
        # One distance map per symbol of the k-path, so the estimate aims at whichever symbol is needed next.
        self._distances = [costs.distances_to(symbol) for symbol in k_path]
        self._forbidden_chain = forbidden_chain
        self._futures = FutureKeys()
        self._summaries: dict[GrammarGraphNode, ChainSummary] = {}
        self._estimates: dict[GrammarGraphNode, int] = {}

    def is_reached(self, node: GrammarGraphNode) -> bool:
        return self.estimate(node) == 0

    def estimate(self, node: GrammarGraphNode) -> int:
        estimate = self._estimates.get(node)
        if estimate is None:
            estimate = self._estimate(self._summary(node), node)
            self._estimates[node] = estimate
        return estimate

    def state(self, node: GrammarGraphNode) -> Hashable:
        summary = self._summary(node)
        if summary.shared_with_forbidden_path < summary.length:
            return (
                self._futures.key(node),
                summary.recent_matched_lengths,
                summary.costs_after,
            )
        return (self._futures.key(node), summary)

    def _estimate(self, summary: ChainSummary, graph_node: GrammarGraphNode) -> int:
        if summary.length == 0:
            return 1
        recent = summary.recent_matched_lengths
        if recent and recent[-1] == len(self._k_path):
            return 0

        # Inside an exchange the chain ends with symbols below the state, so the
        # suffix no longer matches the k-path and every transition looks like a
        # step back. Rate the node by the best match among its nearest ancestors.
        # The goal test above stays exact.
        matched = min(max(recent, default=0), len(self._k_path) - 1)

        # Sub-gradient toward the next symbol that would extend the match:
        # the cheapest cost of the messages still to send until it begins,
        # below the node or after its end.
        cost_to_next_symbol = min(
            RuleCosts.UNREACHABLE,
            self._costs.cost_from(
                graph_node.node, self._distances[matched], summary.costs_after[matched]
            ),
        )
        unmatched = len(self._k_path) - matched
        # Never return 0 here
        return max(unmatched * self.UNMATCHED_SYMBOL_COST + cost_to_next_symbol, 1)

    def _summary(self, node: GrammarGraphNode) -> ChainSummary:
        unsummarised = []
        current: Optional[GrammarGraphNode] = node
        while current is not None and current not in self._summaries:
            unsummarised.append(current)
            current = current.parent
        if current is None:
            summary = ChainSummary(
                0, 0, (), (RuleCosts.UNREACHABLE,) * len(self._k_path)
            )
        else:
            summary = self._summaries[current]
        for graph_node in reversed(unsummarised):
            summary = self._extended_summary(summary, graph_node)
            self._summaries[graph_node] = summary
        return summary

    def _extended_summary(
        self, summary: ChainSummary, graph_node: GrammarGraphNode
    ) -> ChainSummary:
        """Returns the summary of graph_node, given the summary of its parent."""
        parent = graph_node.parent
        if parent is not None:
            costs_after = self._costs.costs_after(
                graph_node.node, parent.node, self._distances, summary.costs_after
            )
            if costs_after is not summary.costs_after:
                summary = summary._replace(costs_after=costs_after)
        symbol = graph_node.chain_symbol()
        if symbol is None:
            return summary
        length = summary.length + 1
        if (
            summary.shared_with_forbidden_path == summary.length
            and summary.length < len(self._forbidden_chain)
            and symbol == self._forbidden_chain[summary.length]
        ):
            return summary._replace(length=length, shared_with_forbidden_path=length)
        previous_matched = (
            summary.recent_matched_lengths[-1] if summary.recent_matched_lengths else 0
        )
        matched = self._matcher.matched_after(previous_matched, symbol)
        return summary._replace(
            length=length,
            recent_matched_lengths=(summary.recent_matched_lengths + (matched,))[
                -self.ANCESTOR_LOOKBACK :
            ],
        )
