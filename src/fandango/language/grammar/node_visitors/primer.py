from collections.abc import Iterator

from fandango.errors import FandangoValueError
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols.non_terminal import NonTerminal


class PrimerVisitor:
    """
    Computes the `distance_to_completion` of every node reachable from a set of
    grammar rules: the number of nodes to call to create the smallest possible subtree
    derivable from that node.
    """

    def __init__(self, rules: dict[NonTerminal, Node]):
        self._rules = rules
        self._visited_ids: set[int] = set()
        self._inf_loops: set[Node] = set()
        self._lowered = False

    def prime(self, raise_on_inf_loops: bool = True) -> None:
        """
        Sets the `distance_to_completion` attribute of every node reachable from the
        rules.

        :param raise_on_inf_loops: If there are NonTerminals in the grammar that cannot
            be completed (distance_to_completion == float("inf")), raise a `FandangoValueError`.
        """
        self._inf_loops.clear()
        self._lowered = True
        while self._lowered:
            self._lowered = False
            self._visited_ids.clear()
            for rule in self._rules.values():
                self.visit(rule)
        self._inf_loops = {
            node
            for node in self._inf_loops
            if node.distance_to_completion == float("inf")
        }
        if raise_on_inf_loops and self._inf_loops:
            raise FandangoValueError(
                f"Grammar contains unbreakable, infinite loops: {self._inf_loops}"
            )

    @property
    def inf_loops(self) -> frozenset[Node]:
        return frozenset(self._inf_loops)

    def visit(self, node: Node) -> float:
        root_results: list[float] = []
        stack: list[tuple[Node, Iterator[Node], list[float]]] = []
        self._enter(node, stack, root_results)
        while stack:
            current, children, results = stack[-1]
            child = next(children, None)
            if child is not None:
                self._enter(child, stack, results)
                continue
            stack.pop()
            distance = self._distance(current, results)
            if distance < current.distance_to_completion:
                current.distance_to_completion = distance
                self._lowered = True
            if distance == float("inf"):
                self._inf_loops.add(current)
            (stack[-1][2] if stack else root_results).append(distance)
        return root_results[0]

    def _enter(
        self,
        node: Node,
        stack: list[tuple[Node, Iterator[Node], list[float]]],
        results: list[float],
    ) -> None:
        """Push `node` onto `stack`, or append its known distance to `results`."""
        node_id = id(node)
        if node_id in self._visited_ids:
            results.append(node.distance_to_completion)
            return
        self._visited_ids.add(node_id)
        stack.append((node, iter(self._children(node)), []))

    def _children(self, node: Node) -> list[Node]:
        if isinstance(node, NonTerminalNode):
            return [self._rules[node.symbol]]
        return node.children()

    def _distance(self, node: Node, child_distances: list[float]) -> float:
        if isinstance(node, Alternative):
            return 1 + min(child_distances)
        if isinstance(node, Concatenation):
            return 1 + sum(child_distances)
        if isinstance(node, Repetition):
            if node.min == 0:
                return 1.0
            return 1 + node.min * child_distances[0]
        if isinstance(node, NonTerminalNode):
            return 1 + child_distances[0]
        if isinstance(node, TerminalNode):
            return 1.0
        if isinstance(node, CharSet):
            raise NotImplementedError("CharSet not implemented.")
        raise TypeError(f"Unexpected node type: {type(node).__name__}")
