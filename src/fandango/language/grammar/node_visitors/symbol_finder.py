from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode


class SymbolFinder(NodeVisitor[None, None]):
    def __init__(self) -> None:
        self.terminalNodes: list[TerminalNode] = []
        self.nonTerminalNodes: list[NonTerminalNode] = []

    def visitNonTerminalNode(self, node: NonTerminalNode) -> None:
        self.nonTerminalNodes.append(node)

    def visitTerminalNode(self, node: TerminalNode) -> None:
        self.terminalNodes.append(node)
