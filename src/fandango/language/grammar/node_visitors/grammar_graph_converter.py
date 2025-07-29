from fandango.language import NonTerminal, Terminal
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor, AggregateType
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Plus, Option, Star
from fandango.language.grammar.nodes.terminal import TerminalNode

class GrammarGraphNode:
    def __init__(self, node: Node, reaches: set["GrammarGraphNode"]):
        self.node = node
        self.reaches = reaches

class GrammarGraph:
    def __init__(self, start: GrammarGraphNode):
        self.start = start
        self.id_to_state: dict[str, GrammarGraphNode] = {}


class GrammarGraphConverterVisitor(NodeVisitor):

    def __init__(self):
        self.rules = None
        self.start_symbol = None

    def process(self, grammar_rules: dict[NonTerminal, Node], start_symbol: NonTerminal):
        self.rules = grammar_rules
        self.start_symbol = start_symbol
        start_node, end_nodes = self.visit(self.rules[start_symbol])
        return start_node

    def visit(self, node: Node) -> tuple[GrammarGraphNode, set[GrammarGraphNode]]:
        return super().visit(node)

    @staticmethod
    def _set_next(node: GrammarGraphNode, next_nodes: set[GrammarGraphNode]):
        for next_child in next_nodes:
            node.reaches.add(next_child)

    def visitAlternative(self, node: Alternative):
        chain_start = set()
        chain_end = set()
        next_nodes = { self.visit(child) for child in node.children() }
        for start_node, end_nodes in next_nodes:
            chain_start.add(start_node)
            for end_node in end_nodes:
                chain_end.add(end_node)
        return GrammarGraphNode(node, chain_start), chain_end

    def visitRepetition(self, node: Repetition):
        chain_start = None
        chain_end = set()
        intermediate_end = None

        for idx in range(node.max):
            if chain_start is None:
                chain_start, intermediate_end = self.visit(node.node)
            else:
                next_node, next_end_nodes = self.visit(node.node)
                for end_node in intermediate_end:
                    self._set_next(end_node, {next_node})
                intermediate_end = next_end_nodes
            if idx >= node.min:
                for node in intermediate_end:
                    chain_end.add(node)
        if chain_start is None:
            chain_start = GrammarGraphNode(node, set())
        return GrammarGraphNode(node, {chain_start}), chain_end

    def visitConcatenation(self, node: Concatenation):
        chain_start = None
        chain_end = set()
        for child in node.children():
            if chain_start is None:
                next_node, chain_end = self.visit(child)
                chain_start = GrammarGraphNode(node, {next_node})
            else:
                next_node, next_end_nodes = self.visit(child)
                for end_node in chain_end:
                    self._set_next(end_node, {next_node})
                chain_end = next_end_nodes
        return chain_start, chain_end

    def visitTerminalNode(self, node: TerminalNode):
        graph_node = GrammarGraphNode(node, set())
        return graph_node, {graph_node}

    def visitNonTerminalNode(self, node: NonTerminalNode):
        graph_node = GrammarGraphNode(node, set())
        to_visit = self.rules[node.symbol]
        chain_start, chain_end = self.visit(to_visit)
        self._set_next(graph_node, {chain_start})
        return graph_node, chain_end

    def visitPlus(self, node: Plus):
        return self.visitRepetition(node)

    def visitOption(self, node: Option):
        return self.visitRepetition(node)

    def visitStar(self, node: Star):
        return self.visitRepetition(node)

    def visitChildren(self, node: Node) -> AggregateType:
        pass