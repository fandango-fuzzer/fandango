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
    def __init__(self, node: Node, reaches: set[Node]):
        self.node = node
        self.reaches = reaches

class GrammarGraph:
    def __init__(self, start: GrammarGraphNode):
        self.start = start
        self.id_to_state: dict[str, GrammarGraphNode] = {}



class GrammarGraphConverterVisitor(NodeVisitor):

    def visit(self, node: Node):
        pass

    def visitAlternative(self, node: Alternative):
        pass

    def visitRepetition(self, node: Repetition):
        pass

    def visitConcatenation(self, node: Concatenation):
        pass

    def visitTerminalNode(self, node: TerminalNode):
        pass

    def visitNonTerminalNode(self, node: NonTerminalNode):
        pass

    def visitPlus(self, node: Plus):
        pass

    def visitOption(self, node: Option):
        pass

    def visitStar(self, node: Star):
        pass

    def visitChildren(self, node: Node) -> AggregateType:
        pass