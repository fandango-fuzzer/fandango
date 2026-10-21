from collections.abc import Iterable, Sequence
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
    AnyTarget,
    CostBasedTarget,
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


class UnreachableTargetError(FandangoError):
    pass


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

    def _entering_cost(self, graph_node: GrammarGraphNode) -> int:
        """Returns what stepping onto the graph node costs a path."""
        return self._message_cost_of(graph_node.node)

    def _check_reachability(
        self, *, tree: Optional[DerivationTree] = None, destination_k_path: KPath
    ) -> ReachabilityResult:
        checker = ReachabilityChecker(self.grammar)
        return checker.find_reachability(tree=tree, k_path_to_reach=destination_k_path)

    def astar_tree(
        self,
        *,
        controlflow_tree: Optional[DerivationTree] = None,
        destination_k_path: KPath,
    ) -> Optional[list[GrammarGraphNode | None]]:
        """
        Returns the cheapest path from the end of controlflow_tree, or from the start symbol, to the k-path.
        If the k-path is only reachable in a new run, the path leads to the end of this run first, marked by None.
        controlflow_tree is a derivation of the grammar with its control-flow nodes, as parsed with include_controlflow.
        """
        return self._astar_tree_to_any(
            tree=controlflow_tree, destination_k_paths=[destination_k_path]
        )

    def _astar_tree_to_any(
        self,
        *,
        tree: Optional[DerivationTree] = None,
        destination_k_paths: Sequence[KPath],
    ) -> Optional[list[GrammarGraphNode | None]]:
        """
        Returns the cheapest path from the end of tree, or from the start symbol, to any of the k-paths.
        Only if no path reaches them in this run, the path leads to the end of this run first, marked by None.
        """
        if any(len(k_path) == 0 for k_path in destination_k_paths):
            return []
        reachable = self._reachable_k_paths(tree, destination_k_paths)
        if reachable:
            path = self._astar_in_run(tree, reachable)
            # A path the search target rules out within this run may still be open in a new one.
            if path is not None or tree is None:
                return path
        try:
            return self._path_through_new_run(tree, destination_k_paths)
        except UnreachableTargetError:
            if reachable:
                return None
            raise

    def _reachable_k_paths(
        self, tree: Optional[DerivationTree], k_paths: Sequence[KPath]
    ) -> list[tuple[KPath, ReachabilityResult]]:
        """The k-paths reachable from the end of tree, or from the start symbol, with how."""
        reachable = []
        for k_path in k_paths:
            reachability = self._check_reachability(
                destination_k_path=k_path, tree=tree
            )
            if reachability.path_reachable:
                reachable.append((k_path, reachability))
        return reachable

    def _astar_in_run(
        self,
        tree: Optional[DerivationTree],
        reachable: list[tuple[KPath, ReachabilityResult]],
    ) -> Optional[list[GrammarGraphNode | None]]:
        """Returns the cheapest path from the end of tree, or from the start symbol, to any of the reachable k-paths."""
        start = self.graph.start if tree is None else self.graph.walk(tree)
        targets = []
        for k_path, reachability in reachable:
            # The chain of the existing derivation is forbidden only if it matches
            # the k-path in a way that extending the derivation cannot complete.
            forbidden_chain: tuple[Symbol, ...] = ()
            if tree is not None and not reachability.completable_by_extension:
                forbidden_chain = start.chain()
            targets.append(KPathTarget(k_path, self._costs, forbidden_chain))
        target: CostBasedTarget = (
            targets[0] if len(targets) == 1 else AnyTarget(targets)
        )
        path = self._search(start, self._search_target(target, tree))
        return None if path is None else list(path)

    def _search_target(
        self, target: CostBasedTarget, tree: Optional[DerivationTree]
    ) -> SearchTarget:
        """The target as searched from the end of tree, or from the start symbol if tree is None."""
        return target

    def _path_through_new_run(
        self, tree: Optional[DerivationTree], destination_k_paths: Sequence[KPath]
    ) -> list[GrammarGraphNode | None]:
        """Returns the path to the end of the run of tree, None, and the path from the start symbol to any k-path."""
        from_start = None
        if tree is not None:
            reachable = self._reachable_k_paths(None, destination_k_paths)
            if reachable:
                from_start = self._astar_in_run(None, reachable)
        if from_start is None:
            raise UnreachableTargetError(
                f"Symbols {list(destination_k_paths)} are not reachable in grammar."
            )
        to_end = self.astar_search_end(tree)
        return [*to_end, None, *from_start]

    def astar_search_end(
        self, controlflow_tree: Optional[DerivationTree]
    ) -> Iterable[GrammarGraphNode]:
        """Returns the cheapest path from the end of controlflow_tree to the end of the run."""
        if controlflow_tree is None:
            return []
        start = self.graph.walk(controlflow_tree)
        if start.is_accepting:
            self._clear_graph()
            return []
        searched = self._search_target(RunEndTarget(self._costs), controlflow_tree)
        path = self._search(start, searched)
        if path is None and not isinstance(searched, RunEndTarget):
            # Ending the run outweighs avoiding what the searched target rules out
            path = self._search(
                self.graph.walk(controlflow_tree), RunEndTarget(self._costs)
            )
        return path or []

    def _search(
        self, start: GrammarGraphNode, target: SearchTarget
    ) -> Optional[list[GrammarGraphNode]]:
        """Returns the cheapest path from start to target. Leaves a fresh graph, as a search unfolds it."""
        search = PathSearch(
            target,
            self._entering_cost,
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
