import heapq
import itertools
from collections.abc import Generator, Hashable, Iterable, Sequence
from typing import NamedTuple, Optional, Union

from fandango.errors import FandangoError
from fandango.io.navigation.graph.reachability_checker import (
    ReachabilityChecker,
    ReachabilityResult,
)
from fandango.io.navigation.nested_steps import run_nested_steps
from fandango.language import DerivationTree, Grammar
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphConverter,
    GrammarGraphNode,
    LazyGrammarGraphNode,
)
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol


class NavigatorTimedOutError(FandangoError):
    pass


class ChainSummary(NamedTuple):
    length: int
    shared_with_forbidden_path: int
    recent_matched_lengths: tuple[int, ...]
    costs_after: tuple[int, ...]


class GrammarNavigator:
    def __init__(self, grammar: Grammar, start_symbol: Optional[NonTerminal] = None):
        if start_symbol is None:
            start_symbol = NonTerminal("<start>")
        self.grammar = grammar
        self._start_symbol = start_symbol
        self.graph = GrammarGraphConverter(grammar.rules, start_symbol).process()
        self.message_cost = 0
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
        # Reference graph. Shows which symbols are referenced by which others, at which cost.
        self._ref_costs: Optional[dict[str, dict[str, int]]] = None
        self._cheapest_costs: dict[NonTerminal, int] = {}
        self._chain_symbols: dict[GrammarGraphNode, Optional[Symbol]] = {}
        self._chain_summaries: dict[GrammarGraphNode, ChainSummary] = {}
        self._heuristic_costs: dict[GrammarGraphNode, int] = {}
        self._search_fallbacks: list[int] = []
        self._future_keys: dict[GrammarGraphNode, Hashable] = {}
        self._continuation_keys: dict[
            GrammarGraphNode, Optional[frozenset[Hashable]]
        ] = {}

    def _clear_graph(self) -> None:
        self.graph = GrammarGraphConverter(
            self.grammar.rules, self._start_symbol
        ).process()
        self._chain_symbols.clear()
        self._future_keys.clear()
        self._continuation_keys.clear()

    _SUB_UNREACHABLE = 100_000
    ANCESTOR_LOOKBACK = 6

    def _message_cost_of(self, node: Node) -> int:
        """Returns the cost of the message that node sends."""
        if isinstance(node, NonTerminalNode) and node.sender is not None:
            return self.message_cost
        return 0

    def _reference_cost(self, node: Node) -> int:
        """Returns the cost of entering the symbol of node: its message, or 1 while messages cost nothing."""
        return self._message_cost_of(node) if self.message_cost else 1

    def _cost_of(self, node: Node) -> int:
        """Returns the cost of the cheapest messages that node derives."""
        if isinstance(node, NonTerminalNode):
            return self._message_cost_of(node) + self._cheapest_costs.get(
                node.symbol, self._SUB_UNREACHABLE
            )
        if isinstance(node, Alternative):
            return min(map(self._cost_of, node.children()))
        if isinstance(node, Repetition):
            return node.min * self._cost_of(node.node)
        return sum(map(self._cost_of, node.children()))

    def _cost_into(self, node: Node, distances: dict[str, int]) -> int:
        """Returns the cheapest cost from before node to the target of distances below node."""
        if isinstance(node, (NonTerminalNode, TerminalNode)):
            return self._reference_cost(node) + distances.get(
                str(node.symbol), self._SUB_UNREACHABLE
            )
        if isinstance(node, Concatenation):
            return self._cost_ahead(node.children(), distances, self._SUB_UNREACHABLE)
        return min(
            (self._cost_into(child, distances) for child in node.children()),
            default=self._SUB_UNREACHABLE,
        )

    def _cost_ahead(
        self, nodes: Sequence[Node], distances: dict[str, int], beyond: int
    ) -> int:
        """
        Returns the cheapest cost to the target of distances:
        below one of the nodes in sequence, or after them at cost beyond.
        """
        cost = self._SUB_UNREACHABLE
        before = 0
        for node in nodes:
            cost = min(cost, before + self._cost_into(node, distances))
            before += self._cost_of(node)
        return min(cost, before + beyond, self._SUB_UNREACHABLE)

    def _reference_graph(self) -> dict[str, dict[str, int]]:
        """symbol -> symbols whose rule references it -> cheapest cost from the start of that rule to the reference."""
        if self._ref_costs is not None:
            return self._ref_costs
        rules = self.grammar.rules
        self._cheapest_costs = {}
        changed = True
        while changed:
            changed = False
            for symbol, body in rules.items():
                cost = self._cost_of(body)
                if cost < self._cheapest_costs.get(symbol, self._SUB_UNREACHABLE):
                    self._cheapest_costs[symbol] = cost
                    changed = True

        costs: dict[str, dict[str, int]] = {}

        def references(rule: str, node: Node, before: int) -> None:
            if isinstance(node, (NonTerminalNode, TerminalNode)):
                cost = before + self._reference_cost(node)
                referencing = costs.setdefault(str(node.symbol), {})
                if cost < referencing.get(rule, self._SUB_UNREACHABLE):
                    referencing[rule] = cost
                return
            for child in node.children():
                references(rule, child, before)
                if isinstance(node, Concatenation):
                    before += self._cost_of(child)

        for symbol, body in rules.items():
            references(str(symbol), body, 0)
        self._ref_costs = costs
        return costs

    def _symbol_distances_to(self, target: Symbol) -> dict[str, int]:
        """Returns the cheapest cost from the start of every symbol's rule to ``target``."""
        key = str(target)
        cached = self._dist_cache.get(key)
        if cached is not None:
            return cached

        referencing = self._reference_graph()
        dist: dict[str, int] = {key: 0}
        nearest = [(0, key)]
        while nearest:
            cost, symbol = heapq.heappop(nearest)
            if cost > dist[symbol]:
                continue
            for rule, reference_cost in referencing.get(symbol, {}).items():
                if cost + reference_cost < dist.get(rule, self._SUB_UNREACHABLE):
                    dist[rule] = cost + reference_cost
                    heapq.heappush(nearest, (dist[rule], rule))
        self._dist_cache[key] = dist
        return dist

    def astar(
        self,
        start: GrammarGraphNode,
    ) -> Union[Iterable[GrammarGraphNode], None]:
        """
        Don't call this directly, use astar_tree or astar_search_end instead.
        """
        self.comparisons = 0
        if self.is_goal_reached(start):
            return [start]
        insertion_order = itertools.count()
        best_costs = {self._search_state(start): 0}
        came_from: dict[GrammarGraphNode, Optional[GrammarGraphNode]] = {start: None}
        closed: set[Hashable] = set()
        frontier = [
            (self.heuristic_cost_estimate(start), next(insertion_order), 0, start)
        ]
        while frontier:
            _, _, cost, current = heapq.heappop(frontier)
            state = self._search_state(current)
            if state in closed or cost > best_costs[state]:
                continue
            if self.is_goal_reached(current):
                path = []
                node: Optional[GrammarGraphNode] = current
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                return list(reversed(path))
            closed.add(state)
            for neighbor in self.neighbors(current):
                neighbor_state = self._search_state(neighbor)
                if neighbor_state in closed:
                    continue
                neighbor_cost = cost + self.distance_between(current, neighbor)
                if neighbor_cost >= best_costs.get(neighbor_state, neighbor_cost + 1):
                    continue
                best_costs[neighbor_state] = neighbor_cost
                came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (
                        neighbor_cost + self.heuristic_cost_estimate(neighbor),
                        next(insertion_order),
                        neighbor_cost,
                        neighbor,
                    ),
                )
        return None

    def _enclosing_instance(self, node: GrammarGraphNode) -> Optional[GrammarGraphNode]:
        current = node.parent
        while current is not None and not isinstance(current, LazyGrammarGraphNode):
            if isinstance(current.node, Repetition):
                return None
            if current.parent is None:
                return current
            current = current.parent
        return current

    def _continuation_key_steps(
        self, instance: GrammarGraphNode
    ) -> Generator[GrammarGraphNode, Hashable, Optional[frozenset[Hashable]]]:
        if not isinstance(instance, LazyGrammarGraphNode):
            return frozenset()
        if instance not in self._continuation_keys:
            self._continuation_keys[instance] = None
            following_keys = []
            for following in instance._pre_load_reaches:
                following_keys.append((yield following))
            self._continuation_keys[instance] = frozenset(following_keys)
        return self._continuation_keys[instance]

    def _future_key_steps(
        self, node: GrammarGraphNode
    ) -> Generator[GrammarGraphNode, Hashable, Hashable]:
        if node not in self._future_keys:
            instance = self._enclosing_instance(node)
            continuation = (
                None
                if instance is None
                else (yield from self._continuation_key_steps(instance))
            )
            self._future_keys[node] = (
                ("instance", id(node))
                if continuation is None
                else (id(node.node), continuation)
            )
        return self._future_keys[node]

    def _future_key(self, node: GrammarGraphNode) -> Hashable:
        return run_nested_steps(self._future_key_steps(node), self._future_key_steps)

    def _search_state(self, node: GrammarGraphNode) -> Hashable:
        if not self.search_symbols:
            return self._future_key(node)
        summary = self._chain_summary(node)
        if summary.shared_with_forbidden_path < summary.length:
            return (
                self._future_key(node),
                summary.recent_matched_lengths,
                summary.costs_after,
            )
        return (self._future_key(node), summary)

    def neighbors(self, n: GrammarGraphNode) -> list[GrammarGraphNode]:
        return n.reaches

    def set_message_cost(self, cost: int) -> None:
        self.message_cost = cost
        self._clear_distances()

    def _clear_distances(self) -> None:
        self._ref_costs = None
        self._dist_cache.clear()

    def distance_between(self, n1: GrammarGraphNode, n2: GrammarGraphNode) -> int:
        return self._message_cost_of(n2.node)

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

    def _costs_after(
        self, graph_node: GrammarGraphNode, after_parent: tuple[int, ...]
    ) -> tuple[int, ...]:
        """Returns the cheapest cost from the end of graph_node to each search symbol, given those of its parent."""
        parent = graph_node.parent
        if parent is None or isinstance(parent.node, (NonTerminalNode, Alternative)):
            return after_parent
        node = graph_node.node
        targets = list(zip(self._target_dists or [], after_parent, strict=True))
        if isinstance(parent.node, Repetition):
            if parent.node.max == 1:
                return after_parent
            # Another round or the end. Ignores how many rounds are left.
            return tuple(
                min(self._cost_into(node, distances), after)
                for distances, after in targets
            )
        siblings = parent.node.children()
        following = siblings[
            next(i for i, sibling in enumerate(siblings) if sibling is node) + 1 :
        ]
        return tuple(
            self._cost_ahead(following, distances, after)
            for distances, after in targets
        )

    def _cost_to(
        self, graph_node: GrammarGraphNode, distances: dict[str, int], after: int
    ) -> int:
        """Returns the cheapest cost from graph_node to the target of distances, below it or after its end."""
        node = graph_node.node
        if isinstance(node, (NonTerminalNode, TerminalNode)):
            # The message of the node itself is sent already.
            below = (
                self._cheapest_costs.get(node.symbol, self._SUB_UNREACHABLE)
                if isinstance(node, NonTerminalNode)
                else 0
            )
            return min(
                distances.get(str(node.symbol), self._SUB_UNREACHABLE), below + after
            )
        return self._cost_ahead([node], distances, after)

    def _extended_summary(
        self, summary: ChainSummary, graph_node: GrammarGraphNode
    ) -> ChainSummary:
        costs_after = self._costs_after(graph_node, summary.costs_after)
        if costs_after is not summary.costs_after:
            summary = summary._replace(costs_after=costs_after)
        symbol = self._chain_symbol(graph_node)
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
        return summary._replace(
            length=length,
            recent_matched_lengths=(summary.recent_matched_lengths + (matched,))[
                -self.ANCESTOR_LOOKBACK :
            ],
        )

    def _chain_summary(self, node: GrammarGraphNode) -> ChainSummary:
        unsummarised = []
        current: Optional[GrammarGraphNode] = node
        while current is not None and current not in self._chain_summaries:
            unsummarised.append(current)
            current = current.parent
        if current is None:
            summary = ChainSummary(
                0, 0, (), (self._SUB_UNREACHABLE,) * len(self._target_dists or [])
            )
        else:
            summary = self._chain_summaries[current]
        for graph_node in reversed(unsummarised):
            summary = self._extended_summary(summary, graph_node)
            self._chain_summaries[graph_node] = summary
        return summary

    def _heuristic_cost(
        self, summary: ChainSummary, graph_node: GrammarGraphNode
    ) -> int:
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
        # extend the live suffix): the cheapest cost of the messages still to send
        # until it begins, below the node or after its end.
        BIG = 1_000_000
        sub = self._SUB_UNREACHABLE
        if self._target_dists is not None and strict < len(self._target_dists):
            cost = self._cost_to(
                graph_node, self._target_dists[strict], summary.costs_after[strict]
            )
            sub = min(sub, cost)
        # Never return 0 here
        return max((search_len - strict) * BIG + sub, 1)

    def heuristic_cost_estimate(self, current: GrammarGraphNode) -> int:
        if not self.search_symbols:
            return 1
        cost = self._heuristic_costs.get(current)
        if cost is None:
            cost = self._heuristic_cost(self._chain_summary(current), current)
            self._heuristic_costs[current] = cost
        return cost

    def is_goal_reached(self, current: GrammarGraphNode) -> bool:
        self.comparisons += 1
        if self.comparisons > self.max_comparisons:
            raise NavigatorTimedOutError(
                f"Couldn't find route to target NonTerminal after {self.comparisons} comparisons. Giving up. Does the grammar contain unbreakable cycles?"
            )
        if self.is_search_end_node:
            return current.is_accepting

        return self.heuristic_cost_estimate(current) == 0

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
            if (
                tree is None
                or not self.check_reachability_w_controlflow(
                    destination_k_path=destination_k_path
                ).path_reachable
            ):
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
        a_star_path = self.astar(start_nav_node)
        self._clear_graph()
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
            self._clear_graph()
            return []
        self._start_search(None, tuple(), None)
        self.is_search_end_node = True
        a_star_path = self.astar(start_node)
        self._clear_graph()
        if a_star_path is None:
            return []
        return a_star_path

    def astar_search_end(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        return self.astar_search_end_w_controlflow(tree)
