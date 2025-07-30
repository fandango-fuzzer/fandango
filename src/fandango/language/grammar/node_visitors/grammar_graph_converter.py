import abc
from typing import Optional

from fandango import FandangoError
from fandango.language import NonTerminal, Terminal, Symbol, DerivationTree
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor, AggregateType
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Plus, Option, Star
from fandango.language.grammar.nodes.terminal import TerminalNode

class GrammarGraphNode(abc.ABC):
    def __init__(self, node: Node):
        self.node = node

    def consumes(self) -> Optional[Terminal]:
        if isinstance(self.node, TerminalNode):
            return self.node.symbol
        return None

    def is_lazy(self):
        return False

    @abc.abstractmethod
    def add_egress(self, node: "GrammarGraphNode"):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def reaches(self) -> list["GrammarGraphNode"]:
        raise NotImplementedError()

class EagerGrammarGraphNode(GrammarGraphNode):
    def __init__(self, node: Node, reaches: list["GrammarGraphNode"]):
        super().__init__(node)
        self._reaches = reaches

    def add_egress(self, node: "GrammarGraphNode"):
        self._reaches.append(node)

    @property
    def reaches(self):
        return self._reaches

class LazyGrammarGraphNode(GrammarGraphNode):
    def __init__(self, node: NonTerminalNode, grammar_rules: dict[NonTerminal, Node]):
        super().__init__(node)
        self.grammar_rules = grammar_rules
        self._chain_end_egress = list()
        self._reaches: Optional[list[GrammarGraphNode]] = None

    def is_lazy(self):
        return True

    def add_egress(self, node: GrammarGraphNode):
        if self._reaches is None:
            self._chain_end_egress.append(node)
        else:
            self._reaches.append(node)

    @property
    def reaches(self):
        if self._reaches is not None:
            return self._reaches
        assert isinstance(self.node, NonTerminalNode)
        graph_converter = GrammarGraphConverterVisitor(self.grammar_rules, self.node.symbol)
        start_node, end_nodes = graph_converter.visit(self.node)
        self._reaches = [start_node]
        for end_node in end_nodes:
            self.add_egress(end_node)
        return self._reaches

class GrammarGraph:
    def __init__(self, start: GrammarGraphNode):
        self.start = start
        self.id_to_state: dict[str, GrammarGraphNode] = {}

    def walk(self, tree_root: DerivationTree):
        return self._walk(self.start, [tree_root], 0)

    def _walk(self, graph_node: GrammarGraphNode, tree_nodes: list[DerivationTree], tree_nodes_idx: int):
        if issubclass(graph_node.node.__class__, (Concatenation, Repetition, Alternative)):
            node_id = graph_node.node.id
            node_type = graph_node.node.node_type
            symbol = f"__{node_type}:{node_id}"
        elif isinstance(graph_node.node, (TerminalNode, NonTerminalNode)):
            symbol = graph_node.node.symbol

        tree_node = tree_nodes[tree_nodes_idx]
        if len(tree_node.children) == 0:
            return graph_node

        current_graph_node = graph_node
        for idx, child in enumerate(tree_node.children):
            found_node = False
            for current_graph_node in graph_node.reaches:
                try:
                    current_graph_node = self._walk(current_graph_node, tree_node.children, idx)
                    found_node = True
                    break
                except NoChildMatchError:
                    continue
            if not found_node:
                raise FandangoError(f"Grammar graph doesn't match tree structure.")
        return current_graph_node




class GrammarGraphConverterVisitor(NodeVisitor):

    def __init__(self, grammar_rules: dict[NonTerminal, Node], start_symbol: NonTerminal):
        self.rules = grammar_rules
        self.start_symbol = start_symbol
        self.parent_chain: list[NonTerminal] = []

    def process(self):
        start_node, end_nodes = self.visit(self.rules[self.start_symbol])
        graph = GrammarGraph(start_node)
        return graph

    def visit(self, node: Node) -> tuple[GrammarGraphNode, list[GrammarGraphNode]]:
        visited = super().visit(node)
        return visited

    @staticmethod
    def _set_next(node: GrammarGraphNode, next_nodes: list[GrammarGraphNode]):
        for next_child in next_nodes:
            node.add_egress(next_child)

    def visitAlternative(self, node: Alternative):
        chain_start = list()
        chain_end = list()
        next_nodes = [ self.visit(child) for child in node.children() ]
        for start_node, end_nodes in next_nodes:
            chain_start.append(start_node)
            for end_node in end_nodes:
                chain_end.append(end_node)
        return EagerGrammarGraphNode(node, chain_start), chain_end

    def visitRepetition(self, node: Repetition):
        chain_start = None
        chain_end = list()
        intermediate_end = None

        for idx in range(node.max):
            if chain_start is None:
                chain_start, intermediate_end = self.visit(node.node)
            else:
                next_node, next_end_nodes = self.visit(node.node)
                for end_node in intermediate_end:
                    self._set_next(end_node, [next_node])
                intermediate_end = next_end_nodes
            if idx >= node.min:
                for node in intermediate_end:
                    chain_end.append(node)
        if chain_start is None:
            chain_start = EagerGrammarGraphNode(node, list())
        return EagerGrammarGraphNode(node, [chain_start]), chain_end

    def visitConcatenation(self, node: Concatenation):
        chain_start = None
        chain_end = list()
        for child in node.children():
            if chain_start is None:
                next_node, chain_end = self.visit(child)
                chain_start = EagerGrammarGraphNode(node, [next_node])
            else:
                next_node, next_end_nodes = self.visit(child)
                for end_node in chain_end:
                    self._set_next(end_node, [next_node])
                chain_end = next_end_nodes
        return chain_start, chain_end

    def visitTerminalNode(self, node: TerminalNode):
        graph_node = EagerGrammarGraphNode(node, list())
        return graph_node, [graph_node]

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol in self.parent_chain:
            graph_node = LazyGrammarGraphNode(node, self.rules)
            return graph_node, [graph_node]
        else:
            self.parent_chain.append(node.symbol)
            to_visit = self.rules[node.symbol]
            chain_start, chain_end = self.visit(to_visit)
            graph_node = EagerGrammarGraphNode(node, [chain_start])
            self.parent_chain.pop()
            return graph_node, chain_end

    def visitPlus(self, node: Plus):
        return self.visitRepetition(node)

    def visitOption(self, node: Option):
        return self.visitRepetition(node)

    def visitStar(self, node: Star):
        return self.visitRepetition(node)