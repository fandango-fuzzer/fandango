import random
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional

from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.language.grammar.nodes.node import Node
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    import fandango.language.grammar.grammar

KPath = tuple[Symbol, ...]


class AlternativeWeights:
    """Weights the alternatives of a rule by the share of their k-paths that are not covered yet."""

    def __init__(
        self,
        grammar: "fandango.language.grammar.grammar.Grammar",
        k: int,
        start_symbol: Optional[NonTerminal] = None,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ):
        self._grammar = grammar
        self._k = k
        self._k_paths = grammar.generate_all_k_paths(
            k=k,
            non_terminal=start_symbol,
            coverage_goal=coverage_goal,
            input_parties=input_parties,
        )
        self._starting_with: dict[Symbol, list[KPath]] = {}
        for path in self._k_paths:
            self._starting_with.setdefault(path[0], []).append(path)
        self._covered: set[KPath] = set()
        self._below: dict[Node, frozenset[KPath]] = {}
        self._crossing: dict[tuple[Node, KPath], frozenset[KPath]] = {}
        self._below_uncovered: dict[Node, int] = {}
        self._crossing_uncovered: dict[tuple[Node, KPath], int] = {}
        # Picks of an alternative in a context since its uncovered k-paths last shrank
        self._failures: dict[Node, dict[KPath, int]] = {}

    def add_covered(self, k_paths: set[KPath]) -> None:
        """Count `k_paths` as covered, too."""
        new = k_paths - self._covered
        if not new:
            return
        self._covered |= new
        for alternative, paths in self._below.items():
            if progress := len(new & paths):
                self._below_uncovered[alternative] -= progress
                self._failures.pop(alternative, None)
        for (alternative, context), paths in self._crossing.items():
            if progress := len(new & paths):
                self._crossing_uncovered[(alternative, context)] -= progress
                self._failures.get(alternative, {}).pop(context, None)

    def sync(self, covered: set[KPath]) -> None:
        """Count exactly the k-paths in `covered` as covered."""
        if self._covered <= covered:
            self.add_covered(covered)
            return
        self._covered = set(covered)
        self._failures.clear()
        for alternative, paths in self._below.items():
            self._below_uncovered[alternative] = len(paths - self._covered)
        for key, paths in self._crossing.items():
            self._crossing_uncovered[key] = len(paths - self._covered)

    def weights(
        self,
        alternatives: Sequence[Node],
        parent: DerivationTree,
        covered_weight: float,
        failure_decay: float = 1.0,
        decay_floor: float = 0.0,
    ) -> list[float]:
        """
        Return `covered_weight` plus the uncovered share of k-paths of each alternative fuzzed below `parent`.
        The share shrinks by `failure_decay` per pick without progress, down to `decay_floor` of it.
        """
        return self._weights(
            alternatives,
            self._context(parent),
            covered_weight,
            failure_decay,
            decay_floor,
        )

    def choose(
        self,
        alternatives: Sequence[Node],
        parent: DerivationTree,
        covered_weight: float,
        failure_decay: float,
        decay_floor: float,
    ) -> Node:
        """Pick one of `alternatives` by weight; count the pick as a failure until its k-paths get covered."""
        context = self._context(parent)
        weights = self._weights(
            alternatives, context, covered_weight, failure_decay, decay_floor
        )
        if not any(weights):
            return random.choice(alternatives)
        chosen = random.choices(alternatives, weights)[0]
        if self._uncovered_share(chosen, context) > 0:
            failures = self._failures.setdefault(chosen, {})
            failures[context] = failures.get(context, 0) + 1
        return chosen

    def _weights(
        self,
        alternatives: Sequence[Node],
        context: KPath,
        covered_weight: float,
        failure_decay: float,
        decay_floor: float,
    ) -> list[float]:
        return [
            covered_weight
            + self._uncovered_share(alternative, context)
            * max(
                decay_floor,
                failure_decay ** self._failures.get(alternative, {}).get(context, 0),
            )
            for alternative in alternatives
        ]

    def _context(self, parent: DerivationTree) -> KPath:
        """Return the symbols of `parent` and its ancestors, at most k-1, root first."""
        symbols: list[Symbol] = []
        tree: DerivationTree | None = parent
        while tree is not None and len(symbols) < self._k - 1:
            symbols.append(tree.symbol)
            tree = tree.parent
        return tuple(reversed(symbols))

    def _uncovered_share(self, alternative: Node, context: KPath) -> float:
        below = self._paths_below(alternative)
        crossing = self._paths_crossing(alternative, context)
        total = len(below) + len(crossing)
        if total == 0:
            return 0.0
        uncovered = (
            self._below_uncovered[alternative]
            + self._crossing_uncovered[(alternative, context)]
        )
        return uncovered / total

    def _first_nodes(self, alternative: Node) -> list[Node]:
        """Return the terminals and non-terminals `alternative` derives directly."""
        if not alternative.is_controlflow:
            return [alternative]
        return list(alternative.descendents(self._grammar, filter_controlflow=True))

    def _paths_below(self, alternative: Node) -> frozenset[KPath]:
        """Return the k-paths starting at or below `alternative`."""
        paths = self._below.get(alternative)
        if paths is None:
            seen: set[Node] = set()
            work = self._first_nodes(alternative)
            symbols: set[Symbol] = set()
            while work:
                node = work.pop()
                if node in seen:
                    continue
                seen.add(node)
                symbols.add(node.to_symbol())
                work.extend(node.descendents(self._grammar, filter_controlflow=True))
            paths = frozenset(
                path
                for symbol in symbols
                for path in self._starting_with.get(symbol, [])
            )
            self._below[alternative] = paths
            self._below_uncovered[alternative] = len(paths - self._covered)
        return paths

    def _paths_crossing(self, alternative: Node, context: KPath) -> frozenset[KPath]:
        """Return the k-paths starting in `context` that continue into `alternative`, without those below it."""
        key = (alternative, context)
        paths = self._crossing.get(key)
        if paths is None:
            below = self._paths_below(alternative)
            firsts = {node.to_symbol() for node in self._first_nodes(alternative)}
            crossing: set[KPath] = set()
            for length in range(1, len(context) + 1):
                prefix = context[-length:]
                for first in firsts:
                    for path in self._starting_with.get(first, []):
                        if len(path) + length > self._k:
                            continue
                        candidate = prefix + path
                        if candidate in self._k_paths and candidate not in below:
                            crossing.add(candidate)
            paths = frozenset(crossing)
            self._crossing[key] = paths
            self._crossing_uncovered[key] = len(paths - self._covered)
        return paths
