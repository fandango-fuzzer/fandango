from fandango.errors import FandangoValueError
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
    """
    Computes the `distance_to_completion` of every node reachable from a set of
    grammar rules: the number of nodes to call to create the smallest possible subtree
    derivable from that node.
    """

    def __init__(self, rules: dict[NonTerminal, Node]):
        self._rules = rules
        self._seen: set[int] = set()
        self._inf_loops: set[Node] = set()
        self._changed = False

    def prime(self, raise_on_inf_loops: bool = True) -> None:
        """
        Sets the `distance_to_completion` attribute of every node reachable from the
        rules.

        :param raise_on_inf_loops: If there are NonTerminals in the grammar that cannot
            be completed (distance_to_completion == float("inf")), raise a `FandangoValueError`.
        """
        self._seen.clear()
        self._inf_loops.clear()
        self._changed = False
        for rule in self._rules.values():
            self.visit(rule)
        while self._changed:
            self._changed = False
            for rule in self._rules.values():
                self.visit(rule)
        self._inf_loops = {
            n for n in self._inf_loops if n.distance_to_completion == float("inf")
        }
        if raise_on_inf_loops and self._inf_loops:
            raise FandangoValueError(
                f"Grammar contains unbreakable, infinite loops: {self._inf_loops}"
            )

    @property
    def inf_loops(self) -> frozenset[Node]:
        return frozenset(self._inf_loops)

    def visit(self, node: Node) -> float:
        if id(node) in self._seen:
            return node.distance_to_completion
        self._seen.add(id(node))
        dist = super().visit(node)
        if node.distance_to_completion > dist:
            self._changed = True
            node.distance_to_completion = dist
        if dist == float("inf"):
            self._inf_loops.add(node)
        self._seen.remove(id(node))
        return dist

    def visitAlternative(self, node: Alternative) -> float:
        return 1 + min(self.visit(child) for child in node.children())

    def visitConcatenation(self, node: Concatenation) -> float:
        return 1 + sum(self.visit(child) for child in node.children())

    def visitRepetition(self, node: Repetition) -> float:
        child_dist = self.visit(node.node)
        return 1 + (node.min * child_dist)

    def visitStar(self, node: Star) -> float:
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus) -> float:
        return self.visitRepetition(node)

    def visitOption(self, node: Option) -> float:
        return self.visitRepetition(node)

    def visitNonTerminalNode(self, node: NonTerminalNode) -> float:
        return 1 + self.visit(self._rules[node.symbol])

    def visitTerminalNode(self, node: TerminalNode) -> float:
        return 1.0

    def visitCharSet(self, node: CharSet) -> float:
        raise NotImplementedError("ChatSet not implemented.")
