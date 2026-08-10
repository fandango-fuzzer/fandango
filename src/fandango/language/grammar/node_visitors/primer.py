from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols.non_terminal import NonTerminal


class PrimerVisitor(NodeVisitor[float, float]):
    def __init__(self, rules: dict[NonTerminal, Node]):
        self._rules = rules
        self._seen: set[int] = set()
        self.inf_loops: set[Node] = set()
        self._changed = False

    def prime(self) -> None:
        self._seen.clear()
        self.inf_loops.clear()
        self._changed = False
        for rule in self._rules.values():
            self.visit(rule)
        while self._changed:
            self._changed = False
            for rule in self._rules.values():
                self.visit(rule)
        self.inf_loops = {
            n for n in self.inf_loops if n.distance_to_completion == float("inf")
        }

    def visit(self, node: Node) -> float:
        if id(node) in self._seen:
            return node.distance_to_completion
        self._seen.add(id(node))
        dist = super().visit(node)
        if node.distance_to_completion > dist:
            self._changed = True
            node.distance_to_completion = dist
        if dist == float("inf"):
            self.inf_loops.add(node)
        self._seen.remove(id(node))
        return dist

    def visitAlternative(self, node: Alternative) -> float:
        minimal_dist = float("inf")
        for child in node.children():
            child_dist = self.visit(child)
            if minimal_dist > child_dist:
                minimal_dist = child_dist
        return minimal_dist + 1

    def visitConcatenation(self, node: Concatenation) -> float:
        total_dist = 0.0
        for child in node.children():
            total_dist += self.visit(child)
        return total_dist + 1

    def visitRepetition(self, node: Repetition) -> float:
        child_dist = self.visit(node.node)
        if node.min == 0:
            return 1.0
        return (node.min * child_dist) + 1

    def visitStar(self, node: Star) -> float:
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus) -> float:
        return self.visitRepetition(node)

    def visitOption(self, node: Option) -> float:
        return self.visitRepetition(node)

    def visitNonTerminalNode(self, node: NonTerminalNode) -> float:
        return self.visit(self._rules[node.symbol]) + 1

    def visitTerminalNode(self, node: TerminalNode) -> float:
        return 1.0

    def visitCharSet(self, node: CharSet) -> float:
        raise NotImplementedError("ChatSet not implemented.")
