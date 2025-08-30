from typing import Union, Iterable, Optional

from astar import AStar
from fandango.errors import FandangoError
from fandango.io.navigation.reachability_checker import ReachabilityChecker
from fandango.language import DerivationTree, Symbol, NonTerminal, Terminal, Grammar
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphNode,
    EagerGrammarGraphNode,
    GrammarGraphConverter,
)
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode


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
        self.search_symbols = None
        self.is_search_end_node = False

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

    def neighbors(self, n: GrammarGraphNode):
        return n.reaches

    def set_message_cost(self, cost: int):
        self.message_cost = cost

    def set_non_terminal_cost(self, cost: int):
        self.non_terminal_cost = cost

    def set_node_costs(self, cost: int):
        self.node_cost = cost

    def distance_between(self, n1: GrammarGraphNode, n2: GrammarGraphNode):
        if isinstance(n2.node, NonTerminalNode):
            if n2.node.sender is not None:
                return self.message_cost
            else:
                return self.non_terminal_cost
        return self.node_cost

    def _get_path_symbols(
        self, node: GrammarGraphNode, include_controlflow: bool
    ) -> list[Symbol]:
        chain = [node]
        current = node
        while current.parent is not None:
            current = current.parent
            chain.append(current)
        chain = list(map(lambda x: x.node.to_symbol(), chain))
        chain = chain[::-1]
        if include_controlflow:
            return chain
        deleted = 0
        for idx, symbol in enumerate(list(chain)):
            if isinstance(symbol, NonTerminal) and symbol.name().startswith("<__"):
                del chain[idx - deleted]
                deleted += 1
        return chain

    def heuristic_path_symbols(self, current_chain: list[Symbol]) -> float:
        if not self.search_symbols or not current_chain:
            return 1
        max_overlap = 0
        search_len = len(self.search_symbols)
        chain_len = len(current_chain)
        for i in range(1, min(search_len, chain_len) + 1):
            if current_chain[-i:] == self.search_symbols[:i]:
                max_overlap = i
        return search_len - max_overlap

    def heuristic_cost_estimate(
        self, current: GrammarGraphNode, goal: GrammarGraphNode
    ):
        if self.search_symbols is not None and len(self.search_symbols) > 0:
            chain = self._get_path_symbols(current, False)
            return self.heuristic_path_symbols(chain)
        return 1

    def is_goal_reached(self, current: GrammarGraphNode, goal: GrammarGraphNode):
        self.comparisons += 1
        if self.comparisons > self.max_comparisons:
            raise NavigatorTimedOutError(
                f"Couldn't find route to target NonTerminal after {self.comparisons} comparisons. Giving up. Does the grammar contain unbreakable cycles?"
            )
        if self.is_search_end_node:
            return current.is_accepting

        return self.heuristic_cost_estimate(current, goal) == 0

    def check_reachability_w_controlflow(
        self, *, tree: Optional[DerivationTree] = None, destination_k_path: list[Symbol]
    ) -> bool:
        checker = ReachabilityChecker(self.grammar)
        return checker.find_reachability(
            tree=tree, k_path_to_reach=destination_k_path
        )

    def astar_tree_w_controlflow(
        self, *, tree: Optional[DerivationTree]=None, destination_k_path: list[Symbol]
    ):
        if len(destination_k_path) == 0:
            return []
        if not self.check_reachability_w_controlflow(
            destination_k_path=destination_k_path, tree=tree
        ):
            if not self.check_reachability_w_controlflow(
                destination_k_path=destination_k_path
            ) and destination_k_path[0] != NonTerminal("<start>"):
                raise FandangoError(
                    f"Symbol {destination_k_path} is not reachable in grammar."
                )
            path: list[GrammarGraphNode | None] = list(
                self.astar_search_end_w_controlflow(tree)
            )
            path.append(None)
            path.extend(
                self.astar_tree_w_controlflow(
                    destination_k_path=destination_k_path
                )
            )
            return path
        self.is_search_end_node = False
        if tree is not None:
            start_nav_node = self.graph.walk(tree)
        else:
            start_nav_node = self.graph.start
        self.search_symbols = []
        for symbol in destination_k_path:
            self.search_symbols.append(symbol)
        return list(
            self.astar(
                start_nav_node,
                EagerGrammarGraphNode(NonTerminalNode(NonTerminal("<dummy>"), []), []),
            )
        )

    def astar_tree(self, *, tree: DerivationTree, destination_k_path: list[Symbol]):
        return self.astar_tree_w_controlflow(
            tree=tree, destination_k_path=destination_k_path
        )

    def astar_search_end_w_controlflow(
        self, tree: DerivationTree
    ) -> Iterable[GrammarGraphNode]:
        start_node = self.graph.walk(tree)
        if start_node.is_accepting:
            return []
        self.search_symbol = None
        self.is_search_end_node = True
        return self.astar(start_node, start_node)

    def astar_search_end(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        return self.astar_search_end_w_controlflow(tree)
