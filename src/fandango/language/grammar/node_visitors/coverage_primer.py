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

Context = tuple[Symbol, ...]
StateKey = tuple[int, Context]


class _CoveragePrimerFrame:
    def __init__(self, node: Node, context: Context, index: int):
        self.node = node
        self.context = context
        self.index = index
        self.children: Iterator[tuple[Node, Context]] = iter(())
        self.results: list[float] = []
        self.low = float("inf")


class CoveragePrimerVisitor:
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
        self._cache: dict[StateKey, float] = {}

    def prime(self) -> None:
        """Set the `min_distance_to_coverage` attribute of every node in the rules."""
        self._cache.clear()
        for symbol, rule in self._rules.items():
            context = self._extend((), symbol)
            work = [rule]
            while work:
                node = work.pop()
                node.min_distance_to_coverage = self.visit(node, context)
                if not isinstance(node, NonTerminalNode):
                    work.extend(node.children())

    def visit(self, node: Node, context: Context = ()) -> float:
        """Return the nodes needed below `context` to generate every k-path at or below `node`."""
        root_results: list[float] = []
        stack: list[_CoveragePrimerFrame] = []
        on_stack: dict[StateKey, int] = {}
        self._enter(node, context, stack, on_stack, root_results)
        while stack:
            frame = stack[-1]
            child = next(frame.children, None)
            if child is not None:
                low = self._enter(*child, stack, on_stack, frame.results)
                frame.low = min(frame.low, low)
                continue
            stack.pop()
            key = (id(frame.node), frame.context)
            del on_stack[key]
            distance = self._distance(frame.node, frame.results)
            # Cutoffs at nodes further up make the result depend on the path here.
            if frame.low >= frame.index:
                self._cache[key] = distance
            if stack:
                stack[-1].results.append(distance)
                stack[-1].low = min(stack[-1].low, frame.low)
            else:
                root_results.append(distance)
        return root_results[0]

    def _enter(
        self,
        node: Node,
        context: Context,
        stack: list[_CoveragePrimerFrame],
        on_stack: dict[StateKey, int],
        results: list[float],
    ) -> float:
        """Push `node` onto `stack`, or append its known distance to `results`; return the cutoff index."""
        key = (id(node), context)
        if key in self._cache:
            results.append(self._cache[key])
            return float("inf")
        if key in on_stack:
            results.append(node.distance_to_completion)
            return float(on_stack[key])
        frame = _CoveragePrimerFrame(node, context, len(stack))
        frame.children = iter(self._children(node, context))
        on_stack[key] = frame.index
        stack.append(frame)
        return float("inf")

    def _extend(self, context: Context, symbol: Symbol) -> Context:
        if self._k == 1:
            return ()
        return (context + (symbol,))[-(self._k - 1) :]

    def _children(self, node: Node, context: Context) -> list[tuple[Node, Context]]:
        if isinstance(node, NonTerminalNode):
            return [(self._rules[node.symbol], self._extend(context, node.symbol))]
        return [(child, context) for child in node.children()]

    def _distance(self, node: Node, child_distances: list[float]) -> float:
        if isinstance(node, Alternative):
            return 1 + max(child_distances)
        if isinstance(node, Concatenation):
            completions = [child.distance_to_completion for child in node.nodes]
            return (
                1
                + sum(completions)
                + max(
                    (d - c for d, c in zip(child_distances, completions, strict=True)),
                    default=0.0,
                )
            )
        if isinstance(node, Repetition):
            repetitions = max(node.min, 1)
            return (
                1
                + child_distances[0]
                + (repetitions - 1) * node.node.distance_to_completion
            )
        if isinstance(node, NonTerminalNode):
            return 1 + child_distances[0]
        if isinstance(node, TerminalNode):
            return 1.0
        if isinstance(node, CharSet):
            raise NotImplementedError("CharSet not implemented.")
        raise TypeError(f"Unexpected node type: {type(node).__name__}")
