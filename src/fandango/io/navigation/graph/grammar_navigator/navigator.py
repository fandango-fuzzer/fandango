from collections.abc import Iterable
from typing import Optional

from fandango.errors import FandangoError
from fandango.io.navigation.graph.grammar_navigator.grammar_graph_converter import (
    GrammarGraphConverter,
    GrammarGraphNode,
)
from fandango.io.navigation.graph.grammar_navigator.path_search import (
    PathSearch,
    SearchTarget,
)
from fandango.io.navigation.graph.grammar_navigator.rule_costs import RuleCosts
from fandango.io.navigation.graph.grammar_navigator.search_targets import (
    KPathTarget,
    RunEndTarget,
)
from fandango.io.navigation.graph.reachability_checker import (
    ReachabilityChecker,
    ReachabilityResult,
)
from fandango.language import DerivationTree, Grammar
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols import NonTerminal, Symbol


class GrammarNavigator:
    """
    Finds the cheapest path through the graph of a grammar,
    from the end of a derivation to a k-path or to the end of the run.
    """

    def __init__(self, grammar: Grammar, start_symbol: Optional[NonTerminal] = None):
        if start_symbol is None:
            start_symbol = NonTerminal("<start>")
        self.grammar = grammar
        self._start_symbol = start_symbol
        self.graph = GrammarGraphConverter(grammar.rules, start_symbol).process()
        self.max_comparisons = 10_000_000
        self.comparisons = 0
        self.set_message_cost(0)

    def set_message_cost(self, cost: int) -> None:
        self.message_cost = cost
        # Without message costs the distances count references, so searches still have a direction.
        self._costs = RuleCosts(self.grammar.rules, self._message_cost_of, cost == 0)

    def _message_cost_of(self, node: Node) -> int:
        """Returns the cost of the message that node sends."""
        if isinstance(node, NonTerminalNode) and node.sender is not None:
            return self.message_cost
        return 0

    def check_reachability_w_controlflow(
        self, *, tree: Optional[DerivationTree] = None, destination_k_path: KPath
    ) -> ReachabilityResult:
        checker = ReachabilityChecker(self.grammar)
        return checker.find_reachability(tree=tree, k_path_to_reach=destination_k_path)

    def astar_tree(
        self, *, tree: DerivationTree, destination_k_path: KPath
    ) -> Optional[list[GrammarGraphNode | None]]:
        return self.astar_tree_w_controlflow(
            tree=tree, destination_k_path=destination_k_path
        )

    def astar_tree_w_controlflow(
        self, *, tree: Optional[DerivationTree] = None, destination_k_path: KPath
    ) -> Optional[list[GrammarGraphNode | None]]:
        """
        Returns the cheapest path from the end of tree, or from the start symbol, to the k-path.
        If the k-path is only reachable in a new run, the path leads to the end of this run first, marked by None.
        """
        if len(destination_k_path) == 0:
            return []
        reachability = self.check_reachability_w_controlflow(
            destination_k_path=destination_k_path, tree=tree
        )
        if not reachability.path_reachable:
            return self._path_through_new_run(tree, destination_k_path)
        start = self.graph.start if tree is None else self.graph.walk(tree)
        # The chain of the existing derivation is forbidden only if it matches
        # the k-path in a way that extending the derivation cannot complete.
        forbidden_chain: tuple[Symbol, ...] = ()
        if tree is not None and not reachability.completable_by_extension:
            forbidden_chain = start.chain()
        path = self._search(
            start, KPathTarget(destination_k_path, self._costs, forbidden_chain)
        )
        return None if path is None else list(path)

    def _path_through_new_run(
        self, tree: Optional[DerivationTree], destination_k_path: KPath
    ) -> list[GrammarGraphNode | None]:
        """Returns the path to the end of the run of tree, None, and the path from the start symbol to the k-path."""
        if (
            tree is None
            or not self.check_reachability_w_controlflow(
                destination_k_path=destination_k_path
            ).path_reachable
        ):
            raise FandangoError(
                f"Symbol {destination_k_path} is not reachable in grammar."
            )
        to_end = self.astar_search_end_w_controlflow(tree)
        from_start = self.astar_tree_w_controlflow(
            destination_k_path=destination_k_path
        )
        assert from_start is not None
        return [*to_end, None, *from_start]

    def astar_search_end(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        return self.astar_search_end_w_controlflow(tree)

    def astar_search_end_w_controlflow(
        self, tree: Optional[DerivationTree]
    ) -> Iterable[GrammarGraphNode]:
        """Returns the cheapest path from the end of tree to the end of the run."""
        if tree is None:
            return []
        start = self.graph.walk(tree)
        if start.is_accepting:
            self._clear_graph()
            return []
        return self._search(start, RunEndTarget()) or []

    def _search(
        self, start: GrammarGraphNode, target: SearchTarget
    ) -> Optional[list[GrammarGraphNode]]:
        """Returns the cheapest path from start to target. Leaves a fresh graph, as a search unfolds it."""
        search = PathSearch(
            target,
            lambda graph_node: self._message_cost_of(graph_node.node),
            self.max_comparisons,
        )
        try:
            return search.cheapest_path(start)
        finally:
            self.comparisons = search.comparisons
            self._clear_graph()

    def _clear_graph(self) -> None:
        self.graph = GrammarGraphConverter(
            self.grammar.rules, self._start_symbol
        ).process()
