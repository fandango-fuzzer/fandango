from astar import AStar

from fandango.language.grammar.node_visitors.grammar_graph_converter import GrammarGraphNode, GrammarGraph
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode


class PacketNavigator(AStar[GrammarGraphNode]):

    def __init__(self, graph: GrammarGraph):
        self.graph = graph

    def neighbors(self, n: GrammarGraphNode):
        return n.reaches

    def distance_between(self, n1: GrammarGraphNode, n2: GrammarGraphNode):
        if isinstance(n2.node, NonTerminalNode):
            if n2.node.sender is not None:
                return 1
        return 0

    def heuristic_cost_estimate(self, current, goal):
        return 1

    def is_goal_reached(self, current: GrammarGraphNode, goal: GrammarGraphNode):
        if isinstance(current.node, TerminalNode) and isinstance(goal.node, TerminalNode):
            return current.node.symbol == goal.node.symbol
        return False