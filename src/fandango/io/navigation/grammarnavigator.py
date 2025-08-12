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
        self.search_sender = None
        self.search_recipient = None
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

        if current.node.symbol != self.search_symbol:
            return False
        if self.search_sender is not None and current.node.sender != self.search_sender:
            return False
        if (
            self.search_recipient is not None
            and current.node.recipient != self.search_recipient
        ):
            return False
        return True

    def astar_tree(
        self,
        *,
        tree: DerivationTree,
        symbol: Symbol,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
    ):
        start_node = self.graph.walk(tree)
        if isinstance(symbol, NonTerminal):
            symbol_node = NonTerminalNode(symbol, [])
        elif isinstance(symbol, Terminal):
            symbol_node = TerminalNode(symbol, [])
        else:
            raise ValueError(f"Unsupported symbol type: {type(symbol)}")
        checker = ReachabilityChecker(self.grammar)
        if not checker.find_reachability(
            symbol_to_reach=symbol, sender=sender, recipient=recipient, tree=tree
        ):
            return None
        self.is_search_end_node = False
        self.search_sender = sender
        self.search_recipient = recipient
        self.search_symbol = symbol
        return self.astar(start_node, EagerGrammarGraphNode(symbol_node, []))

    def astar_search_end(self, tree: DerivationTree) -> Iterable[GrammarGraphNode]:
        start_node = self.graph.walk(tree)
        if start_node.is_accepting:
            return []
        self.search_sender = None
        self.search_recipient = None
        self.search_symbol = None
        self.is_search_end_node = True
        return self.astar(start_node, start_node)
