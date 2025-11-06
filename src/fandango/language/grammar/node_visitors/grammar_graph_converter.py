import abc
from typing import Optional

from fandango.errors import FandangoError
from fandango.language import NonTerminal, Terminal, DerivationTree
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Plus, Option, Star
from fandango.language.grammar.nodes.terminal import TerminalNode


class GrammarWalkError(FandangoError):
    pass


class GrammarGraphNode(abc.ABC):
    def __init__(self, node: Node):
        self.node = node
        self.parent = None

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

    @property
    def is_accepting(self) -> bool:
        if len(self.reaches) == 0:
            return True
        if len(self.reaches) > 1:
            return False
        if not isinstance(self.node, Repetition):
            return False
        return self.node.min == 0

    def walk(self, tree_node: DerivationTree):
        if issubclass(
            self.node.__class__,
            (NonTerminalNode, Concatenation, Repetition, Alternative),
        ):
            if isinstance(self.node, NonTerminalNode):
                symbol = self.node.symbol
            else:
                assert hasattr(self.node, 'id')
                node_id = self.node.id
                symbol = NonTerminal(f"<__{node_id}>")
            if tree_node.symbol != symbol:
                raise GrammarWalkError(
                    f"Grammar graph node {symbol.value()} doesn't match tree node {tree_node.symbol.value()}."
                )
        elif isinstance(self.node, TerminalNode):
            if not self.node.symbol.check(tree_node.symbol.value().to_string())[0]:
                # Todo other tree value types
                raise GrammarWalkError(
                    f"Grammar graph node {self.node.symbol.value()} doesn't match tree node {tree_node.symbol.value()}."
                )
        else:
            raise FandangoError(
                f"Unsupported node type: {self.node.__class__.__name__}"
            )
        if len(tree_node.children) == 0:
            return self
        walked_node = self
        for child in tree_node.children:
            found_node = False
            for current_graph_node in walked_node.reaches:
                try:
                    next_walked_node = current_graph_node.walk(child)
                except GrammarWalkError:
                    next_walked_node = None
                if next_walked_node is not None:
                    found_node = True
                    walked_node = next_walked_node
                    break
            if not found_node:
                raise GrammarWalkError(f"Grammar graph doesn't match tree structure.")
        return walked_node


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
        self._pre_load_reaches: list[GrammarGraphNode] = list()
        self._loaded_reaches: Optional[list[GrammarGraphNode]] = None

    def is_lazy(self):
        return True

    def add_egress(self, node: GrammarGraphNode):
        if self._loaded_reaches is None:
            self._pre_load_reaches.append(node)
        else:
            for end_node in self._loaded_reaches:
                end_node.add_egress(node)

    @property
    def reaches(self):
        if self._loaded_reaches is not None:
            return self._loaded_reaches
        assert isinstance(self.node, NonTerminalNode)
        graph_converter = GrammarGraphConverter(self.grammar_rules, self.node.symbol)
        graph_converter.current_parent.append(self)
        start_node, end_nodes = graph_converter.visit(
            self.grammar_rules[self.node.symbol]
        )
        graph_converter.current_parent.pop()
        self._loaded_reaches = [start_node]
        for end_node in end_nodes:
            for chain_end in self._pre_load_reaches:
                end_node.add_egress(chain_end)

        return self._loaded_reaches


class GrammarGraph:
    def __init__(self, start: GrammarGraphNode):
        self.start = start
        self.id_to_state: dict[str, GrammarGraphNode] = {}

    def walk(self, tree_root: DerivationTree):
        return self.start.walk(tree_root)


class GrammarGraphConverter(NodeVisitor):

    def __init__(
        self, grammar_rules: dict[NonTerminal, Node], start_symbol: NonTerminal
    ):
        self.rules = grammar_rules
        self.start_symbol = start_symbol
        self.current_parent: list[GrammarGraphNode] = []

    def process(self):
        start_node = EagerGrammarGraphNode(NonTerminalNode(self.start_symbol, []), [])
        self.current_parent.append(start_node)
        child_start_node, child_end_nodes = self.visit(self.rules[self.start_symbol])
        self.current_parent.pop()
        start_node.reaches.append(child_start_node)
        graph = GrammarGraph(start_node)
        return graph

    def _get_current_parent(self):
        if len(self.current_parent) == 0:
            return None
        return self.current_parent[-1]

    def visit(self, node: Node) -> tuple[GrammarGraphNode, list[GrammarGraphNode]]:
        start, end_nodes = super().visit(node)
        start.parent = self._get_current_parent()
        return start, end_nodes

    @staticmethod
    def _set_next(node: GrammarGraphNode, next_nodes: list[GrammarGraphNode]):
        for next_child in next_nodes:
            node.add_egress(next_child)

    def visitAlternative(self, node: Alternative):
        chain_start: list[GrammarGraphNode] = list()
        chain_end = list()
        graph_node = EagerGrammarGraphNode(node, chain_start)
        self.current_parent.append(graph_node)
        next_nodes = [self.visit(child) for child in node.children()]
        for start_node, end_nodes in next_nodes:
            chain_start.append(start_node)
            for end_node in end_nodes:
                chain_end.append(end_node)
        self.current_parent.pop()
        return graph_node, chain_end

    def visitRepetition(self, node: Repetition):
        chain_start = None
        chain_end = list()
        intermediate_end = None
        reaches: list[GrammarGraphNode] = list()
        graph_node = EagerGrammarGraphNode(node, reaches)
        self.current_parent.append(graph_node)

        for idx in range(node.max):
            if chain_start is None:
                chain_start, intermediate_end = self.visit(node.node)
            else:
                next_node, next_end_nodes = self.visit(node.node)
                for end_node in intermediate_end:
                    self._set_next(end_node, [next_node])
                intermediate_end = next_end_nodes
            if (idx + 1) >= node.min:
                for end_node in intermediate_end:
                    chain_end.append(end_node)
        if chain_start is not None:
            reaches.append(chain_start)
        if node.min == 0:
            chain_end.append(graph_node)

        self.current_parent.pop()
        return graph_node, chain_end

    def visitConcatenation(self, node: Concatenation):
        chain_end: list[GrammarGraphNode] = list()
        reaches: list[GrammarGraphNode] = list()
        graph_node = EagerGrammarGraphNode(node, reaches)
        self.current_parent.append(graph_node)
        first = True
        for child in node.children():
            if first:
                first = False
                next_node, chain_end = self.visit(child)
                reaches.append(next_node)
            else:
                next_node, next_end_nodes = self.visit(child)
                for end_node in chain_end:
                    self._set_next(end_node, [next_node])
                chain_end = next_end_nodes
        self.current_parent.pop()
        return graph_node, chain_end

    def visitTerminalNode(self, node: TerminalNode):
        graph_node = EagerGrammarGraphNode(node, list())
        return graph_node, [graph_node]

    def visitNonTerminalNode(self, node: NonTerminalNode):
        graph_node = LazyGrammarGraphNode(node, self.rules)
        return graph_node, [graph_node]

    def visitPlus(self, node: Plus):
        return self.visitRepetition(node)

    def visitOption(self, node: Option):
        return self.visitRepetition(node)

    def visitStar(self, node: Star):
        return self.visitRepetition(node)
