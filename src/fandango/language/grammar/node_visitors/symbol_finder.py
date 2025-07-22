from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode


class SymbolFinder(NodeVisitor):
    def __init__(self):
        self.terminalNodes = []
        self.nonTerminalNodes = []

    def visitNonTerminalNode(self, node: NonTerminalNode):
        self.nonTerminalNodes.append(node)

    def visitTerminalNode(self, node: TerminalNode):
        self.terminalNodes.append(node)
