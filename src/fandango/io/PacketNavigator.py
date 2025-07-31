from astar import AStar

from fandango.language import DerivationTree, Symbol, NonTerminal, Terminal
from fandango.language.grammar.grammar_settings import GrammarSetting
from fandango.language.grammar.node_visitors.grammar_graph_converter import GrammarGraphNode, GrammarGraph, \
    LazyGrammarGraphNode, EagerGrammarGraphNode
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
        if isinstance(current.node, NonTerminalNode) and isinstance(goal.node, NonTerminalNode):
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
        return self.astar(start_node, EagerGrammarGraphNode(symbol_node, []))