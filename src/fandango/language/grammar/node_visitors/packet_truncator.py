from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Star, Plus, Option
from fandango.language.grammar.nodes.terminal import TerminalNode


class PacketTruncator(NodeVisitor):
    def __init__(self, grammar: "Grammar", keep_parties: set[str]):
        self.grammar = grammar
        self.keep_msg_parties = keep_parties

    def visitStar(self, node: Star):
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus):
        return self.visitRepetition(node)

    def visitOption(self, node: Option):
        return self.visitRepetition(node)

    def visitAlternative(self, node: Alternative):
        for child in list(node.children()):
            if self.visit(child):
                node.alternatives.remove(child)
        if len(node.alternatives) == 0:
            return True
        return False

    def visitRepetition(self, node: Repetition):
        for child in list(node.children()):
            if self.visit(child):
                return True
        return False

    def visitConcatenation(self, node: Concatenation):
        for child in list(node.children()):
            if self.visit(child):
                node.nodes.remove(child)
        if len(node.nodes) == 0:
            return True
        return False

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.sender is None or node.recipient is None:
            return False
        truncatable = True
        if node.sender in self.keep_msg_parties:
            truncatable = False
        if node.recipient in self.keep_msg_parties:
            truncatable = False
        return truncatable

    def visitTerminalNode(self, node: TerminalNode):
        return False
