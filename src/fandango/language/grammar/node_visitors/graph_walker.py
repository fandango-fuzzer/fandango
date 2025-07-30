from fandango import DerivationTree
from fandango.language.grammar.node_visitors.grammar_graph_converter import GrammarGraph, GrammarGraphNode
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.terminal import TerminalNode


class GraphWalker:

    def __init__(self, graph: GrammarGraph):
        self.graph = graph

    def walk(self, tree_root: DerivationTree):
        return self._walk(self.start, tree_root)

    def _walk(self, graph_node: GrammarGraphNode, tree_nodes: list[DerivationTree]):
        if issubclass(graph_node.node.__class__, (Concatenation, Repetition, Alternative)):
            node_id = graph_node.node.id
            node_type = graph_node.node.node_type
            symbol = f"__{node_type}:{node_id}"
        elif isinstance(graph_node.node, (TerminalNode, NonTerminalNode)):
            symbol = graph_node.node.symbol
        for graph_child in graph_node.reaches:
            pass

        for tree_node in tree_nodes:
            pass