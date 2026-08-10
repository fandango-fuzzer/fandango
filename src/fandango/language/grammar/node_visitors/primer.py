from fandango.language.grammar.node_visitors.node_visitor import (
    NodeVisitor,
    ResultType,
)
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.symbols.symbol import Symbol


class PrimerVisitor(NodeVisitor):

    def __init__(self, rules: dict[NonTerminal, Node]):
        self._rules = rules
        self._seen_count: dict[Node, int] = dict()
        self.inf_loops: set[Node] = set()

    def prime(self):
        self._seen_count.clear()
        self.inf_loops.clear()
        for rule in self._rules.values():
            self.visit(rule)
        self.inf_loops = {n for n in self.inf_loops if n.distance_to_completion == float('inf')}

    def visit(self, node: Node) -> ResultType:
        seen_count = self._seen_count.get(node, 0)
        if seen_count > 1:
            return float('inf')
        self._seen_count[node] = seen_count + 1
        dist = super().visit(node)
        node.distance_to_completion = dist
        if dist == float('inf'):
            self.inf_loops.add(node)
        self._seen_count[node] = self._seen_count.get(node, 0) - 1
        return dist

    def visitAlternative(self, node: Alternative) -> ResultType:
        minimal_dist = float('inf')
        for child in node.children():
            child_dist = self.visit(child)
            if minimal_dist > child_dist:
                minimal_dist = child_dist
        return minimal_dist + 1

    def visitConcatenation(self, node: Concatenation) -> ResultType:
        total_dist = 0
        for child in node.children():
            total_dist += self.visit(child)
        return total_dist + 1

    def visitRepetition(self, node: Repetition) -> ResultType:
        child_dist = self.visit(node.node)
        return child_dist + 1

    def visitStar(self, node: Star) -> ResultType:
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus) -> ResultType:
        return self.visitRepetition(node)

    def visitOption(self, node: Option) -> ResultType:
        return self.visitRepetition(node)

    def visitNonTerminalNode(self, node: NonTerminalNode) -> ResultType:
        return self.visit(self._rules[node.symbol])

    def visitTerminalNode(self, node: TerminalNode) -> ResultType:
        return 1

    def visitCharSet(self, node: CharSet) -> ResultType:
        raise NotImplementedError("ChatSet not implemented.")
