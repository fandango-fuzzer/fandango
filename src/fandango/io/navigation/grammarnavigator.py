from collections.abc import Iterable
from functools import lru_cache
from typing import Union, Optional

from astar import AStar
from fandango.errors import FandangoError
from fandango.io.navigation.reachability_checker import (
    ReachabilityChecker,
    ReachabilityResult,
)
from fandango.language import DerivationTree, Grammar
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import Symbol, NonTerminal
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphNode,
    EagerGrammarGraphNode,
    GrammarGraphConverter,
)
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode


@lru_cache(maxsize=16384)
def _path_symbols(node: "GrammarGraphNode", include_controlflow: bool) -> list[Symbol]:
    """Cache the symbol chain from a grammar-graph node up to the root."""
    node_chain = [node]
    current = node
    while current.parent is not None:
        current = current.parent
        node_chain.append(current)
    node_chain.reverse()
    if include_controlflow:
        return [n.node.to_symbol() for n in node_chain]
    return [n.node.to_symbol() for n in node_chain if not n.node.is_controlflow]


class NavigatorTimedOutError(FandangoError):
    pass


class GrammarNavigator(AStar[GrammarGraphNode]):
    def __init__(
        self, grammar: Grammar, start_symbol: NonTerminal = NonTerminal("<start>")
    ):
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

    _SUB_UNREACHABLE = 100_000

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

    @staticmethod
    def _get_path_symbols(
        node: GrammarGraphNode, include_controlflow: bool
    ) -> list[Symbol]:
        return _path_symbols(node, include_controlflow)

    def _live_suffix_len(self, current_chain: list[Symbol]) -> int:
        """Longest suffix of ``current_chain`` that is a prefix of the k-path."""
        if not self.search_symbols or not current_chain:
            return 0
        search_len = len(self.search_symbols)
        chain_len = len(current_chain)
        strict = 0
        for i in range(1, min(search_len, chain_len) + 1):
            if current_chain[-i:] == self.search_symbols[:i]:
                strict = i
        return strict

    def _strip_forbidden_prefix(self, current_chain: list[Symbol]) -> list[Symbol]:
        """
        Drop the longest leading run a node's chain shares with the recorded
        dead-end path. Only the part beyond it is genuine progress, so a match
        that merely reproduces (a prefix of) the dead-end path collapses to
        nothing while a fresh occurrence further down keeps its credit.
        """
        if not self._forbidden_path:
            return current_chain
        i = 0
        limit = min(len(current_chain), len(self._forbidden_path))
        while i < limit and current_chain[i] == self._forbidden_path[i]:
            i += 1
        return current_chain[i:]

    def heuristic_path_symbols(self, current_chain: list[Symbol]) -> int:
        if not self.search_symbols or not current_chain:
            return 1
        current_chain = self._strip_forbidden_prefix(current_chain)
        search_len = len(self.search_symbols)

        strict = self._live_suffix_len(current_chain)
        if strict == search_len:
            return 0

        chain_strs = [str(s) for s in current_chain]

        # Sub-gradient toward search_symbols[strict] (the next symbol that would
        # extend the live suffix) via the static reference distance, taken as min
        # over the chain. Reaching an on-path state usually requires detouring
        # through OFF-path symbols first.
        BIG = 1_000_000
        sub = self._SUB_UNREACHABLE
        if (
            strict < search_len
            and self._target_dists is not None
            and strict < len(self._target_dists)
        ):
            dmap = self._target_dists[strict]
            best = None
            for cs in chain_strs:
                d = dmap.get(cs)
                if d is not None and (best is None or d < best):
                    best = d
            if best is not None:
                sub = best
        # Never return 0 here
        return max((search_len - strict) * BIG + sub, 1)

    def heuristic_cost_estimate(
        self, current: GrammarGraphNode, goal: GrammarGraphNode
    ) -> int:
        if self.search_symbols is not None and len(self.search_symbols) > 0:
            chain = self._get_path_symbols(current, False)
            return self.heuristic_path_symbols(chain)
        return 1

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
        self.search_symbols = list(destination_k_path)
        # Record the realized derivation path as forbidden only when there is an
        # existing derivation whose match cannot be completed by extension.
        if tree is not None and not reachability.completable_by_extension:
            self._forbidden_path = tuple(self._get_path_symbols(start_nav_node, False))
        else:
            self._forbidden_path = tuple()
        # Precompute static reference distances to each symbol of the k-path so
        # the heuristic has a gradient toward whichever symbol is needed next
        # (not just the first). Crossing message-state plateaus between two
        # k-path symbols otherwise degenerates to brute force.
        self._target_dists = [self._symbol_distances_to(s) for s in destination_k_path]
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
        self.search_symbols = None
        self.is_search_end_node = True
        a_star_path = self.astar(start_node, start_node)
        if a_star_path is None:
            return []
        return a_star_path

    def astar_search_end(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        return self.astar_search_end_w_controlflow(tree)
