import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Optional

from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.node import Node
from fandango.language.symbols import NonTerminal, Symbol, Terminal
from fandango.language.tree import DerivationTree


@dataclass(frozen=True)
class Decay:
    """A decay `factor` set while `uncovered` k-paths were left; it weakens as they get covered."""

    factor: float
    uncovered: int

    def factor_at(self, uncovered: int) -> float:
        return math.pow(self.factor, min(1.0, uncovered / self.uncovered))


class AlternativeWeights:
    """Weights the alternatives of a rule by the share of their k-paths that are not covered yet."""

    def __init__(
        self,
        grammar: Grammar,
        k: int,
        start_symbol: Optional[NonTerminal] = None,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
        covered_weight: float = 0.3,
        failure_decay: float = 0.98,
        decay_floor: float = 0.2,
    ):
        self._grammar = grammar
        self._covered_weight = covered_weight
        self._failure_decay = failure_decay
        self._decay_floor = decay_floor
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
        self._decays: dict[tuple[Node, KPath], Decay] = {}
        self._alternatives_in_rule: dict[
            Symbol, list[list[tuple[Node, frozenset[Symbol]]]]
        ] = {}

    def add_covered(self, k_paths: set[KPath]) -> None:
        """Count `k_paths` as covered, too."""
        new = k_paths - self._covered
        self._covered |= new
        self._shift_uncovered(new, -1)

    def sync(self, covered: set[KPath]) -> None:
        """Count exactly the k-paths in `covered` as covered."""
        lost = self._covered - covered
        self._covered -= lost
        self._shift_uncovered(lost, 1)
        self.add_covered(covered)

    def apply_decay(self, tree: DerivationTree) -> None:
        """Decay the uncovered share of each alternative `tree` derives that still has uncovered k-paths."""
        for alternative, context in self._derived_alternatives(tree):
            key = (alternative, context)
            if self._uncovered_share(alternative, context) == 0:
                self._decays.pop(key, None)
                continue
            uncovered = self._uncovered(alternative, context)
            factor = self._decay_factor(alternative, context) * self._failure_decay
            self._decays[key] = Decay(max(self._decay_floor, factor), uncovered)

    def reset(self) -> None:
        """Count no k-path as covered and drop all decay."""
        self._covered.clear()
        self._decays.clear()
        for alternative, paths in self._below.items():
            self._below_uncovered[alternative] = len(paths)
        for key, paths in self._crossing.items():
            self._crossing_uncovered[key] = len(paths)

    def weights(
        self, alternatives: Sequence[Node], parent: DerivationTree
    ) -> list[float]:
        """Return the weight of each alternative fuzzed below `parent`."""
        return self._weights(alternatives, self._context(parent))

    def choose(self, alternatives: Sequence[Node], parent: DerivationTree) -> Node:
        """Pick one of `alternatives` by weight."""
        weights = self.weights(alternatives, parent)
        if not any(weights):
            return random.choice(alternatives)
        return random.choices(alternatives, weights)[0]

    def _weights(self, alternatives: Sequence[Node], context: KPath) -> list[float]:
        return [
            self._covered_weight
            + self._uncovered_share(alternative, context)
            * self._decay_factor(alternative, context)
            for alternative in alternatives
        ]

    def _decay_factor(self, alternative: Node, context: KPath) -> float:
        decay = self._decays.get((alternative, context))
        if decay is None:
            return 1.0
        return decay.factor_at(self._uncovered(alternative, context))

    def _derived_alternatives(self, tree: DerivationTree) -> set[tuple[Node, KPath]]:
        """Return the alternatives each node of `tree` derives its children from, with the node's context."""
        derived: set[tuple[Node, KPath]] = set()
        pending = [tree]
        while pending:
            node = pending.pop()
            if not isinstance(node.symbol, NonTerminal):
                continue
            pending.extend(node.children)
            child_symbols = self._child_symbols(node)
            context = self._context(node)
            for choices in self._rule_alternatives(node.symbol):
                for alternative in self._best_matching(choices, child_symbols):
                    derived.add((alternative, context))
        return derived

    @staticmethod
    def _best_matching(
        choices: list[tuple[Node, frozenset[Symbol]]], child_symbols: set[Symbol]
    ) -> list[Node]:
        """Return the choices sharing the most symbols with `child_symbols`, then lacking the fewest."""
        scored: list[tuple[tuple[int, int], Node]] = []
        for alternative, symbols in choices:
            shared = len(symbols & child_symbols)
            if shared:
                scored.append(((shared, -len(symbols - child_symbols)), alternative))
        if not scored:
            return []
        best = max(score for score, _alternative in scored)
        return [alternative for score, alternative in scored if score == best]

    def _child_symbols(self, node: DerivationTree) -> set[Symbol]:
        """Return the symbols of the children of `node`, with terminals as the rule's terminals that match them."""
        assert isinstance(node.symbol, NonTerminal)
        symbols: set[Symbol] = set()
        for child in node.children:
            if isinstance(child.symbol, Terminal):
                symbols.update(
                    self._grammar._rule_terminals_matching(node.symbol, child.symbol)
                )
            else:
                symbols.add(child.symbol)
        return symbols

    def _rule_alternatives(
        self, symbol: NonTerminal
    ) -> list[list[tuple[Node, frozenset[Symbol]]]]:
        """Return the choices of each alternative node inside the rule of `symbol`, each with the symbols it derives directly."""
        alternatives = self._alternatives_in_rule.get(symbol)
        if alternatives is None:
            alternatives = []
            pending: list[Node] = (
                [self._grammar.rules[symbol]] if symbol in self._grammar.rules else []
            )
            while pending:
                node = pending.pop()
                if isinstance(node, Alternative):
                    choices: list[tuple[Node, frozenset[Symbol]]] = []
                    for alternative in node.alternatives:
                        symbols = frozenset(
                            first.to_symbol()
                            for first in self._first_nodes(alternative)
                        )
                        choices.append((alternative, symbols))
                    alternatives.append(choices)
                pending.extend(node.children())
            self._alternatives_in_rule[symbol] = alternatives
        return alternatives

    def _shift_uncovered(self, k_paths: set[KPath], change: int) -> None:
        if not k_paths:
            return
        for alternative, paths in self._below.items():
            if count := len(k_paths & paths):
                self._below_uncovered[alternative] += change * count
        for key, paths in self._crossing.items():
            if count := len(k_paths & paths):
                self._crossing_uncovered[key] += change * count

    def _uncovered(self, alternative: Node, context: KPath) -> int:
        return (
            self._below_uncovered[alternative]
            + self._crossing_uncovered[(alternative, context)]
        )

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
        return self._uncovered(alternative, context) / total

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
