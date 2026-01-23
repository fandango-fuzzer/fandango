from typing import Optional

from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Star, Plus, Option
from fandango.language.grammar.nodes.terminal import TerminalNode


class PacketTruncator(NodeVisitor[bool, bool]):
    def __init__(
        self,
        grammar: "Grammar",
        keep_parties: set[str],
        ignore_receivers: bool = False,
        delete_rules: Optional[set[NonTerminal]] = None,
    ):
        self.grammar = grammar
        self.keep_msg_parties = keep_parties
        self.ignore_receivers = ignore_receivers
        if delete_rules is None:
            delete_rules = set()
        self.delete_rules = delete_rules

    def visitStar(self, node: Star) -> bool:
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus) -> bool:
        return self.visitRepetition(node)

    def visitOption(self, node: Option) -> bool:
        return self.visitRepetition(node)

    def visitAlternative(self, node: Alternative) -> bool:
        for child in list(node.children()):
            if self.visit(child):
                node.alternatives.remove(child)
        if len(node.alternatives) == 0:
            return True
        return False

    def visitRepetition(self, node: Repetition) -> bool:
        for child in list(node.children()):
            if self.visit(child):
                return True
        return False

    def visitConcatenation(self, node: Concatenation) -> bool:
        for child in list(node.children()):
            if self.visit(child):
                node.nodes.remove(child)
        if len(node.nodes) == 0:
            return True
        return False

    def visitNonTerminalNode(self, node: NonTerminalNode) -> bool:
        if node.symbol in self.delete_rules:
            return True
        if self.ignore_receivers:
            if node.sender is None:
                return False
        else:
            if node.sender is None or node.recipient is None:
                return False
        truncatable = True
        if node.sender in self.keep_msg_parties:
            truncatable = False
        if node.recipient in self.keep_msg_parties and not self.ignore_receivers:
            truncatable = False
        return truncatable

    def visitTerminalNode(self, node: TerminalNode) -> bool:
        return False
