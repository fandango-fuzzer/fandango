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
        self.search_symbol = None
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

    def heuristic_cost_estimate(self, current, goal):
        return 1

    def is_goal_reached(self, current: GrammarGraphNode, goal: GrammarGraphNode):
        self.comparisons += 1
        if self.comparisons > self.max_comparisons:
            raise NavigatorTimedOutError(
                f"Couldn't find route to target NonTerminal after {self.comparisons} comparisons. Giving up. Does the grammar contain unbreakable cycles?"
            )
        if self.is_search_end_node:
            return current.is_accepting

        if not isinstance(current.node, (NonTerminalNode, TerminalNode)):
            return False
        if current.node.symbol == self.search_symbol:
            return True
        if isinstance(current.node, NonTerminalNode):
            return NonTerminal(f"<{current.node.symbol.name()[9:]}") == self.search_symbol
        return False

    def check_reachability_w_controlflow(self, *, tree: DerivationTree, destination_symbols: list[Symbol]) -> bool:
        checker = ReachabilityChecker(self.grammar)
        return checker.find_reachability(tree=tree, symbol_chain_to_reach=destination_symbols)


    def astar_tree_w_controlflow(
        self,
        *,
        tree: DerivationTree,
        destination_symbols: list[Symbol]
    ):
        if len(destination_symbols) == 0:
            return []
        if not self.check_reachability_w_controlflow(
            destination_symbols=destination_symbols, tree=tree
        ):
            empty_tree = DerivationTree(NonTerminal("<start>"))
            if not self.check_reachability_w_controlflow(
                    destination_symbols=destination_symbols, tree=empty_tree
            ) and destination_symbols[0] != NonTerminal("<start>"):
                raise FandangoError(
                    f"Symbol {destination_symbols} is not reachable in grammar."
                )
            path: list[GrammarGraphNode | None] = list(self.astar_search_end_w_controlflow(tree))
            path.append(None)
            if destination_symbols[0] != NonTerminal("<start>"):
                path.extend(self.astar_tree_w_controlflow(tree=empty_tree, destination_symbols=destination_symbols))
            else:
                path.append(EagerGrammarGraphNode(NonTerminalNode(NonTerminal("<start>"), []), []))
            return path
        self.is_search_end_node = False
        nav_path = []
        start_nav_node = self.graph.walk(tree)
        for symbol in destination_symbols:
            if isinstance(symbol, NonTerminal):
                symbol_node = NonTerminalNode(symbol, [])
            elif isinstance(symbol, Terminal):
                symbol_node = TerminalNode(symbol, [])
            else:
                raise ValueError(f"Unsupported symbol type: {type(symbol)}")
            self.search_symbol = symbol
            current_part_nav = list(self.astar(start_nav_node, EagerGrammarGraphNode(symbol_node, [])))
            nav_path.extend(current_part_nav[1:])
            if len(nav_path) > 0:
                start_nav_node = nav_path[-1]
        return nav_path

    def astar_tree(
            self,
            *,
            tree: DerivationTree,
            destination_symbols: list[Symbol]
    ):
        return self.astar_tree_w_controlflow(tree=tree, destination_symbols=destination_symbols)

    def astar_search_end_w_controlflow(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        start_node = self.graph.walk(tree)
        if start_node.is_accepting:
            return []
        self.search_symbol = None
        self.is_search_end_node = True
        return self.astar(start_node, start_node)


    def astar_search_end(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        return self.astar_search_end_w_controlflow(tree)
