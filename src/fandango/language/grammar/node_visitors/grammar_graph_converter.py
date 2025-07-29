from typing import Optional

from fandango.language import NonTerminal, Terminal, Symbol
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor, AggregateType
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Plus, Option, Star
from fandango.language.grammar.nodes.terminal import TerminalNode

class GrammarGraphNode:
    def __init__(self, node: Node):
        self.node = node

    def consumes(self) -> Optional[Terminal]:
        if isinstance(self.node, TerminalNode):
            return self.node.symbol
        return None

    def add_egress(self, node: "GrammarGraphNode"):
        raise NotImplementedError()

    @property
    def reaches(self) -> set["GrammarGraphNode"]:
        raise NotImplementedError()

class EagerGrammarGraphNode(GrammarGraphNode):
    def __init__(self, node: Node, reaches: set["GrammarGraphNode"]):
        super().__init__(node)
        self._reaches = reaches

    def add_egress(self, node: "GrammarGraphNode"):
        self._reaches.add(node)

    @property
    def reaches(self):
        return self._reaches

class LazyGrammarGraphNode(GrammarGraphNode):
    def __init__(self, node: NonTerminalNode, grammar_rules: dict[NonTerminal, Node]):
        super().__init__(node)
        self.grammar_rules = grammar_rules
        self._chain_end_egress = set()
        self._reaches: Optional[set[GrammarGraphNode]] = None

    def add_egress(self, node: GrammarGraphNode):
        if self._reaches is None:
            self._chain_end_egress.add(node)
        else:
            self._reaches.add(node)

    @property
    def reaches(self):
        if self._reaches is not None:
            return self._reaches
        graph_converter = GrammarGraphConverterVisitor()
        assert isinstance(self.node, NonTerminalNode)
        #Todo initialize process
        # graph_converter.process(self.grammar_rules, self.node.symbol)
        start_node, end_nodes = graph_converter.visit(self.node)
        self._reaches = {start_node}
        for end_node in end_nodes:
            self.add_egress(end_node)
        return self._reaches

class GrammarGraph:
    def __init__(self, start: GrammarGraphNode):
        self.start = start
        self.id_to_state: dict[str, GrammarGraphNode] = {}


class GrammarGraphConverterVisitor(NodeVisitor):

    def __init__(self):
        self.rules = None
        self.start_symbol = None
        self.parent_chain: list[NonTerminal] = []

    def process(self, grammar_rules: dict[NonTerminal, Node], start_symbol: NonTerminal):
        self.rules = grammar_rules
        self.start_symbol = start_symbol
        start_node, end_nodes = self.visit(self.rules[start_symbol])
        return start_node

    def visit(self, node: Node) -> tuple[GrammarGraphNode, set[GrammarGraphNode]]:
        visited = super().visit(node)
        return visited

    @staticmethod
    def _set_next(node: GrammarGraphNode, next_nodes: set[GrammarGraphNode]):
        for next_child in next_nodes:
            node.add_egress(next_child)

    def visitAlternative(self, node: Alternative):
        chain_start = set()
        chain_end = set()
        next_nodes = { self.visit(child) for child in node.children() }
        for start_node, end_nodes in next_nodes:
            chain_start.add(start_node)
            for end_node in end_nodes:
                chain_end.add(end_node)
        return EagerGrammarGraphNode(node, chain_start), chain_end

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
            chain_start = EagerGrammarGraphNode(node, set())
        return EagerGrammarGraphNode(node, {chain_start}), chain_end

    def visitConcatenation(self, node: Concatenation):
        chain_start = None
        chain_end = set()
        for child in node.children():
            if chain_start is None:
                next_node, chain_end = self.visit(child)
                chain_start = EagerGrammarGraphNode(node, {next_node})
            else:
                next_node, next_end_nodes = self.visit(child)
                for end_node in chain_end:
                    self._set_next(end_node, {next_node})
                chain_end = next_end_nodes
        return chain_start, chain_end

    def visitTerminalNode(self, node: TerminalNode):
        graph_node = EagerGrammarGraphNode(node, set())
        return graph_node, {graph_node}

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol in self.parent_chain:
            graph_node = LazyGrammarGraphNode(node, self.rules)
            return graph_node, {graph_node}
        else:
            self.parent_chain.append(node.symbol)
            to_visit = self.rules[node.symbol]
            chain_start, chain_end = self.visit(to_visit)
            graph_node = EagerGrammarGraphNode(node, {chain_start})
            self.parent_chain.pop()
            return graph_node, {chain_end}

    def visitPlus(self, node: Plus):
        return self.visitRepetition(node)

    def visitOption(self, node: Option):
        return self.visitRepetition(node)

    def visitStar(self, node: Star):
        return self.visitRepetition(node)