from astar import AStar

from fandango.io.navigation.reachability_checker import ReachabilityChecker
from fandango.language import DerivationTree, Symbol, NonTerminal, Terminal, Grammar
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphNode,
    EagerGrammarGraphNode,
    GrammarGraphConverter,
)
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode


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
        if isinstance(current.node, NonTerminalNode) and isinstance(
            goal.node, NonTerminalNode
        ):
            return current.node.symbol == goal.node.symbol
        if isinstance(current.node, TerminalNode) and isinstance(
            goal.node, TerminalNode
        ):
            return current.node.symbol == goal.node.symbol
        return False

    def astar_tree(self, tree: DerivationTree, symbol: Symbol):
        start_node = self.graph.walk(tree)
        if isinstance(symbol, NonTerminal):
            symbol_node = NonTerminalNode(symbol, [])
        elif isinstance(symbol, Terminal):
            symbol_node = TerminalNode(symbol, [])
        else:
            raise ValueError(f"Unsupported symbol type: {type(symbol)}")
        checker = ReachabilityChecker(self.grammar)
        if not checker.find_reachability(symbol, tree):
            return None
        return self.astar(start_node, EagerGrammarGraphNode(symbol_node, []))
