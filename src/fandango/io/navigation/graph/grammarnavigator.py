from collections.abc import Iterable
from typing import NamedTuple, Optional, Union

from astar import AStar

from fandango.errors import FandangoError
from fandango.io.navigation.graph.reachability_checker import (
    ReachabilityChecker,
    ReachabilityResult,
)
from fandango.language import DerivationTree, Grammar
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    EagerGrammarGraphNode,
    GrammarGraphConverter,
    GrammarGraphNode,
)
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol


class NavigatorTimedOutError(FandangoError):
    pass


def nearer(first: Optional[int], second: Optional[int]) -> Optional[int]:
    if first is None:
        return second
    if second is None:
        return first
    return min(first, second)


class ChainSummary(NamedTuple):
    length: int
    shared_with_forbidden_path: int
    recent_matched_lengths: tuple[int, ...]
    closest_target_distances: tuple[Optional[int], ...]


class GrammarNavigator(AStar[GrammarGraphNode]):
    def __init__(self, grammar: Grammar, start_symbol: Optional[NonTerminal] = None):
        if start_symbol is None:
            start_symbol = NonTerminal("<start>")
        graph_converter = GrammarGraphConverter(grammar.rules, start_symbol)
        self.grammar = grammar
        self.graph = graph_converter.process()
        self.message_cost = 0
        self.non_terminal_cost = 0
        self.node_cost = 0
        self.max_comparisons = 10_000_000
        self.comparisons = 0
        self.search_symbols: Optional[list[Symbol]] = None
        self.is_search_end_node = False
        # The realized path of the existing derivation, recorded only when the
        # k-path cannot be completed by extension. The heuristic ignores whatever
        # leading prefix a node's chain shares with this dead-end path, so the
        # match it already provides is not mistaken for progress.
        self._forbidden_path: tuple[Symbol, ...] = tuple()
        self._dist_cache: dict[str, dict[str, int]] = {}
        # One distance map per symbol of the ACTIVE target k-path, so the
        # heuristic can guide toward whichever k-path symbol is needed next.
        self._target_dists: Optional[list[dict[str, int]]] = None
        # Reference graph. Shows which symbols directly reference which others.
        self._ref_fwd: Optional[dict[str, set[str]]] = None
        self._chain_symbols: dict[GrammarGraphNode, Optional[Symbol]] = {}
        self._chain_summaries: dict[GrammarGraphNode, ChainSummary] = {}
        self._heuristic_costs: dict[GrammarGraphNode, int] = {}
        self._search_fallbacks: list[int] = []

    _SUB_UNREACHABLE = 100_000
    ANCESTOR_LOOKBACK = 6

    def _reference_graph(self) -> dict[str, set[str]]:
        """symbol -> set of non-terminals it directly references in its rule body."""
        if self._ref_fwd is not None:
            return self._ref_fwd

        def references(body: Node) -> set[str]:
            out: set[str] = set()
            stack = [body]
            seen: set[int] = set()
            while stack:
                n = stack.pop()
                if id(n) in seen:
                    continue
                seen.add(id(n))
                if isinstance(n, (NonTerminalNode, TerminalNode)):
                    out.add(str(n.symbol))
                    continue
                for child in n.children():
                    stack.append(child)
            return out

        fwd: dict[str, set[str]] = {}
        for nt, body in self.grammar.rules.items():
            fwd[str(nt)] = references(body)
        self._ref_fwd = fwd
        return fwd

    def _symbol_distances_to(self, target: Symbol) -> dict[str, int]:
        """Distance (in rule references) from every symbol to ``target``."""
        key = str(target)
        cached = self._dist_cache.get(key)
        if cached is not None:
            return cached

        from collections import deque

        fwd = self._reference_graph()
        rev: dict[str, set[str]] = {}
        for a, outs in fwd.items():
            for b in outs:
                rev.setdefault(b, set()).add(a)

        # Perform breadth-first search from target to every reachable symbol,
        # record the shortest nr of hops to reach each symbol.
        dist: dict[str, int] = {key: 0}
        dq = deque([key])
        while dq:
            s = dq.popleft()
            for p in rev.get(s, ()):
                if p not in dist:
                    dist[p] = dist[s] + 1
                    dq.append(p)
        self._dist_cache[key] = dist
        return dist

    def astar(
        self,
        start: GrammarGraphNode,
        goal: GrammarGraphNode,
        reverse_path: bool = False,
    ) -> Union[Iterable[GrammarGraphNode], None]:
        """
        Overloaded method. Don't call this directly, use astar_tree or astar_search_end instead.
        """
        self.comparisons = 0
        return super().astar(start, goal, reverse_path)

    def neighbors(self, n: GrammarGraphNode) -> list[GrammarGraphNode]:
        return n.reaches

    def set_message_cost(self, cost: int) -> None:
        self.message_cost = cost

    def set_non_terminal_cost(self, cost: int) -> None:
        self.non_terminal_cost = cost

    def set_node_costs(self, cost: int) -> None:
        self.node_cost = cost

    def distance_between(self, n1: GrammarGraphNode, n2: GrammarGraphNode) -> int:
        if isinstance(n2.node, NonTerminalNode):
            if n2.node.sender is not None:
                return self.message_cost
            else:
                return self.non_terminal_cost
        return self.node_cost

    def _chain_symbol(self, node: GrammarGraphNode) -> Optional[Symbol]:
        if node not in self._chain_symbols:
            self._chain_symbols[node] = (
                None if node.node.is_controlflow else node.node.to_symbol()
            )
        return self._chain_symbols[node]

    def _chain(self, node: GrammarGraphNode) -> tuple[Symbol, ...]:
        symbols = []
        current: Optional[GrammarGraphNode] = node
        while current is not None:
            symbol = self._chain_symbol(current)
            if symbol is not None:
                symbols.append(symbol)
            current = current.parent
        return tuple(reversed(symbols))

    def _start_search(
        self,
        search_symbols: Optional[list[Symbol]],
        forbidden_path: tuple[Symbol, ...],
        target_dists: Optional[list[dict[str, int]]],
    ) -> None:
        self.search_symbols = search_symbols
        self._forbidden_path = forbidden_path
        self._target_dists = target_dists
        self._search_fallbacks = self._prefix_fallbacks(search_symbols or [])
        self._chain_summaries.clear()
        self._heuristic_costs.clear()

    @staticmethod
    def _prefix_fallbacks(pattern: list[Symbol]) -> list[int]:
        fallbacks = [0] * len(pattern)
        matched = 0
        for i in range(1, len(pattern)):
            while matched > 0 and pattern[i] != pattern[matched]:
                matched = fallbacks[matched - 1]
            if pattern[i] == pattern[matched]:
                matched += 1
            fallbacks[i] = matched
        return fallbacks

    def _matched_length_after(self, matched: int, symbol: Symbol) -> int:
        assert self.search_symbols is not None
        if matched == len(self.search_symbols):
            matched = self._search_fallbacks[matched - 1]
        while matched > 0 and self.search_symbols[matched] != symbol:
            matched = self._search_fallbacks[matched - 1]
        if self.search_symbols[matched] == symbol:
            matched += 1
        return matched

    def _extended_summary(
        self, summary: ChainSummary, symbol: Optional[Symbol]
    ) -> ChainSummary:
        if symbol is None:
            return summary
        length = summary.length + 1
        if (
            summary.shared_with_forbidden_path == summary.length
            and summary.length < len(self._forbidden_path)
            and symbol == self._forbidden_path[summary.length]
        ):
            return summary._replace(length=length, shared_with_forbidden_path=length)
        previous_matched = (
            summary.recent_matched_lengths[-1] if summary.recent_matched_lengths else 0
        )
        matched = self._matched_length_after(previous_matched, symbol)
        name = str(symbol)
        return ChainSummary(
            length,
            summary.shared_with_forbidden_path,
            (summary.recent_matched_lengths + (matched,))[-self.ANCESTOR_LOOKBACK :],
            tuple(
                nearer(closest, target.get(name))
                for closest, target in zip(
                    summary.closest_target_distances,
                    self._target_dists or [],
                    strict=True,
                )
            ),
        )

    def _chain_summary(self, node: GrammarGraphNode) -> ChainSummary:
        unsummarised = []
        current: Optional[GrammarGraphNode] = node
        while current is not None and current not in self._chain_summaries:
            unsummarised.append(current)
            current = current.parent
        if current is None:
            summary = ChainSummary(0, 0, (), (None,) * len(self._target_dists or []))
        else:
            summary = self._chain_summaries[current]
        for graph_node in reversed(unsummarised):
            summary = self._extended_summary(summary, self._chain_symbol(graph_node))
            self._chain_summaries[graph_node] = summary
        return summary

    def _heuristic_cost(self, summary: ChainSummary) -> int:
        assert self.search_symbols is not None
        if summary.length == 0:
            return 1
        search_len = len(self.search_symbols)
        recent = summary.recent_matched_lengths
        if recent and recent[-1] == search_len:
            return 0

        # Inside an exchange the chain ends with symbols below the state, so the
        # suffix no longer matches the k-path and every transition looks like a
        # step back. Rate the node by the best match among its nearest ancestors.
        # The goal test above stays exact.
        strict = min(max(recent, default=0), search_len - 1)

        # Sub-gradient toward search_symbols[strict] (the next symbol that would
        # extend the live suffix) via the static reference distance, taken as min
        # over the chain. Reaching an on-path state usually requires detouring
        # through OFF-path symbols first.
        BIG = 1_000_000
        sub = self._SUB_UNREACHABLE
        if self._target_dists is not None and strict < len(self._target_dists):
            closest = summary.closest_target_distances[strict]
            if closest is not None:
                sub = closest
        # Never return 0 here
        return max((search_len - strict) * BIG + sub, 1)

    def heuristic_cost_estimate(
        self, current: GrammarGraphNode, goal: GrammarGraphNode
    ) -> int:
        if not self.search_symbols:
            return 1
        cost = self._heuristic_costs.get(current)
        if cost is None:
            cost = self._heuristic_cost(self._chain_summary(current))
            self._heuristic_costs[current] = cost
        return cost

    def is_goal_reached(
        self, current: GrammarGraphNode, goal: GrammarGraphNode
    ) -> bool:
        self.comparisons += 1
        if self.comparisons > self.max_comparisons:
            raise NavigatorTimedOutError(
                f"Couldn't find route to target NonTerminal after {self.comparisons} comparisons. Giving up. Does the grammar contain unbreakable cycles?"
            )
        if self.is_search_end_node:
            return current.is_accepting

        return self.heuristic_cost_estimate(current, goal) == 0

    def check_reachability_w_controlflow(
        self, *, tree: Optional[DerivationTree] = None, destination_k_path: KPath
    ) -> ReachabilityResult:
        checker = ReachabilityChecker(self.grammar)
        return checker.find_reachability(tree=tree, k_path_to_reach=destination_k_path)

    def astar_tree_w_controlflow(
        self, *, tree: Optional[DerivationTree] = None, destination_k_path: KPath
    ) -> Optional[list[GrammarGraphNode | None]]:
        if len(destination_k_path) == 0:
            return []
        reachability = self.check_reachability_w_controlflow(
            destination_k_path=destination_k_path, tree=tree
        )
        if not reachability.path_reachable:
            if not self.check_reachability_w_controlflow(
                destination_k_path=destination_k_path
            ).path_reachable and destination_k_path[0] != NonTerminal("<start>"):
                raise FandangoError(
                    f"Symbol {destination_k_path} is not reachable in grammar."
                )
            path: list[GrammarGraphNode | None] = list(
                self.astar_search_end_w_controlflow(tree)
            )
            path.append(None)
            from_start_path = self.astar_tree_w_controlflow(
                destination_k_path=destination_k_path
            )
            assert from_start_path is not None
            path.extend(from_start_path)
            return path
        self.is_search_end_node = False
        if tree is not None:
            start_nav_node = self.graph.walk(tree)
        else:
            start_nav_node = self.graph.start
        # Record the realized derivation path as forbidden only when there is an
        # existing derivation whose match cannot be completed by extension.
        # Static reference distances to each symbol of the k-path give the
        # heuristic a gradient toward whichever symbol is needed next (not just
        # the first). Crossing message-state plateaus between two k-path symbols
        # otherwise degenerates to brute force.
        self._start_search(
            list(destination_k_path),
            self._chain(start_nav_node)
            if tree is not None and not reachability.completable_by_extension
            else tuple(),
            [self._symbol_distances_to(s) for s in destination_k_path],
        )
        a_star_path = self.astar(
            start_nav_node,
            EagerGrammarGraphNode(NonTerminalNode(NonTerminal("<dummy>"), []), []),
        )
        if a_star_path is None:
            return None
        return list(a_star_path)

    def astar_tree(
        self, *, tree: DerivationTree, destination_k_path: KPath
    ) -> Optional[list[GrammarGraphNode | None]]:
        return self.astar_tree_w_controlflow(
            tree=tree, destination_k_path=destination_k_path
        )

    def astar_search_end_w_controlflow(
        self, tree: Optional[DerivationTree]
    ) -> Iterable[GrammarGraphNode]:
        if tree is None:
            return []
        start_node = self.graph.walk(tree)
        if start_node.is_accepting:
            return []
        self._start_search(None, tuple(), None)
        self.is_search_end_node = True
        a_star_path = self.astar(start_node, start_node)
        if a_star_path is None:
            return []
        return a_star_path

    def astar_search_end(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        return self.astar_search_end_w_controlflow(tree)
