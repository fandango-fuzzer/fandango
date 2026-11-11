from collections.abc import Iterator

from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.symbols.symbol import Symbol


class MinDistanceToCoverageVisitor:
    """
    Computes the `min_distance_to_coverage` of every node reachable from a set of
    grammar rules.
    min_distance_to_coverage describes the minimum number of nodes required per tree to produce every k-path
    syntactically using multiple DerivationTrees.
    """

    def __init__(self, rules: dict[NonTerminal, Node], k: int):
        assert k >= 1, "k must be at least 1"
        self._rules = rules
        self._k = k
        self._reaches: dict[int, dict[Symbol, float]] = {}
        self._windows: dict[tuple[int, int], float] = {}
        self._visited_ids: set[int] = set()
        self._lowered = False

    def prime(self) -> None:
        """Sets the `min_distance_to_coverage` attribute of every node in the rules."""
        self._reaches.clear()
        self._windows.clear()
        self._lowered = True
        while self._lowered:
            self._lowered = False
            self._visited_ids.clear()
            for rule in self._rules.values():
                self._visit_reaches(rule)
        for rule in self._rules.values():
            work = [rule]
            while work:
                node = work.pop()
                node.min_distance_to_coverage = self._coverage(node)
                if not isinstance(node, NonTerminalNode):
                    work.extend(node.children())

    def _coverage(self, node: Node) -> float:
        """Returns the number of nodes needed below `node` to produce each k-path in its subtree."""
        # A k-path starting at the rule's nonterminal has one symbol left before `node`.
        coverage = self._window(node, self._k - 1)
        for symbol, distance in self._reaches[id(node)].items():
            coverage = max(coverage, distance + self._symbol_window(symbol))
        return coverage

    def _carriers(self, node: Node) -> list[tuple[Node, float]]:
        """
        Returns the children a path can continue in, each with the number of nodes
        needed to complete the rest of `node` minimally.
        """
        if isinstance(node, NonTerminalNode):
            return [(self._rules[node.symbol], 1.0)]
        if isinstance(node, Alternative):
            return [(alternative, 1.0) for alternative in node.alternatives]
        if isinstance(node, Concatenation):
            total = 1 + sum(child.distance_to_completion for child in node.nodes)
            return [
                (child, total - child.distance_to_completion) for child in node.nodes
            ]
        if isinstance(node, Repetition):
            completed = max(node.min, 1) - 1
            return [(node.node, 1 + completed * node.node.distance_to_completion)]
        if isinstance(node, TerminalNode):
            return []
        if isinstance(node, CharSet):
            raise NotImplementedError("CharSet not implemented.")
        raise TypeError(f"Unexpected node type: {type(node).__name__}")

    def _visit_reaches(self, node: Node) -> None:
        stack: list[tuple[Node, Iterator[tuple[Node, float]]]] = []
        self._enter(node, stack)
        while stack:
            current, carriers = stack[-1]
            carrier = next(carriers, None)
            if carrier is not None:
                self._enter(carrier[0], stack)
                continue
            stack.pop()
            self._lower_reaches(current)

    def _enter(
        self, node: Node, stack: list[tuple[Node, Iterator[tuple[Node, float]]]]
    ) -> None:
        """Pushes `node` onto `stack` if this pass has not visited it yet."""
        node_id = id(node)
        if node_id in self._visited_ids:
            return
        self._visited_ids.add(node_id)
        stack.append((node, iter(self._carriers(node))))

    def _lower_reaches(self, node: Node) -> None:
        """Updates, for each symbol, the fewest nodes `node` needs to contain that symbol."""
        reaches = self._reaches.setdefault(id(node), {})
        candidates: list[tuple[Symbol, float]] = []
        if isinstance(node, (NonTerminalNode, TerminalNode)):
            candidates.append((node.symbol, 0.0))
        for child, others in self._carriers(node):
            for symbol, distance in self._reaches.get(id(child), {}).items():
                candidates.append((symbol, others + distance))
        for symbol, distance in candidates:
            if distance < reaches.get(symbol, float("inf")):
                reaches[symbol] = distance
                self._lowered = True

    def _symbol_window(self, symbol: Symbol) -> float:
        """Returns the number of nodes needed to produce the most expensive k-path starting at `symbol`."""
        if isinstance(symbol, NonTerminal):
            return 1 + self._window(self._rules[symbol], self._k - 1)
        return 1.0

    def _window(self, node: Node, depth: int) -> float:
        """Returns the number of nodes needed below `node` to produce its most expensive path of `depth` symbols."""
        if depth == 0:
            return node.distance_to_completion
        key = (id(node), depth)
        if key not in self._windows:
            child_depth = depth - 1 if isinstance(node, NonTerminalNode) else depth
            self._windows[key] = max(
                (
                    others + self._window(child, child_depth)
                    for child, others in self._carriers(node)
                ),
                default=1.0,
            )
        return self._windows[key]
