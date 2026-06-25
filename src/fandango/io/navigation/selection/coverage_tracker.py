from collections.abc import Callable
from typing import Optional

from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class CoverageTracker:
    """Measures reached k-path coverage of the current and past protocol runs.

    Each completed run is folded once into bounded k-path sets (``add_completed_tree``)
    instead of retaining the trees; queries combine that basis with the live history
    tree. Whole-tree coverage honours ``coverage_goal``/``input_parties``; the
    per-NonTerminal coverage uses the grammar defaults (mirroring ``compute_kpath_coverage``).
    """

    def __init__(
        self,
        grammar: Grammar,
        diversity_k: int,
        model: ProtocolModel,
        start_symbol: NonTerminal,
        input_parties: Callable[[], set[str]],
        history: Callable[[], DerivationTree],
        coverage_goal: CoverageGoal,
    ):
        self._grammar = grammar
        self._diversity_k = diversity_k
        self._model = model
        self._start_symbol = start_symbol
        self._input_parties = input_parties
        self._history = history
        self._coverage_goal = coverage_goal
        self._whole_covered: set[KPath] = set()
        self._message_covered: dict[NonTerminal, set[KPath]] = {}
        self._coverage_scores: Optional[list[tuple[NonTerminal, float]]] = None

    def add_completed_tree(self, tree: DerivationTree) -> None:
        """Fold a finished run into the coverage basis."""
        self._whole_covered |= self._covered(
            [tree],
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        for symbol, subtrees in self._model.group_messages_by_nt([tree]).items():
            self._message_covered.setdefault(symbol, set()).update(
                self._covered(subtrees)
            )
        self._coverage_scores = None

    def reset(self) -> None:
        self._whole_covered.clear()
        self._message_covered.clear()
        self._coverage_scores = None

    def invalidate(self) -> None:
        self._coverage_scores = None

    def set_coverage_goal(self, goal: CoverageGoal) -> None:
        # coverage_goal feeds whole-tree extraction, so the folded basis is invalid.
        self._coverage_goal = goal
        self._whole_covered.clear()
        self._coverage_scores = None

    def uncovered_paths(self) -> list[KPath]:
        all_paths = self._all_k_paths(
            self._start_symbol,
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        return list(all_paths.difference(self._whole_covered_paths()))

    def coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_coverage_scores()
        return self._coverage_scores

    def coverage_percent(self) -> float:
        uncovered = self.uncovered_paths()
        if len(uncovered) == 0:
            return 1.0
        all_paths = self._all_k_paths(
            self._start_symbol,
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        if len(all_paths) == 0:
            return 1.0
        return 1.0 - (len(uncovered) / len(all_paths))

    def _covered(
        self,
        trees: list[DerivationTree],
        *,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        """k-paths covered by the trees (union of the per-tree extraction)."""
        result: set[KPath] = set()
        for tree in trees:
            result |= self._grammar._extract_k_paths_from_tree(
                tree,
                self._diversity_k,
                overlap_to_root,
                coverage_goal,
                input_parties=input_parties,
            )
        return result

    def _all_k_paths(
        self,
        non_terminal: NonTerminal,
        *,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        return self._grammar.generate_all_k_paths(
            k=self._diversity_k,
            non_terminal=non_terminal,
            coverage_goal=coverage_goal,
            input_parties=input_parties,
        )

    def _whole_covered_paths(self) -> set[KPath]:
        """Folded basis plus the in-progress history tree."""
        covered = set(self._whole_covered)
        covered |= self._covered(
            [self._history()],
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        return covered

    def _compute_coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        """Per-NonTerminal coverage score: covered / total k-paths."""
        history_messages = self._model.group_messages_by_nt([self._history()])
        nt_coverage: dict[NonTerminal, float] = {}
        for symbol in self._model.state_grammar_symbols:
            if symbol not in self._message_covered and symbol not in history_messages:
                nt_coverage[symbol] = 0.0
                continue
            covered = set(self._message_covered.get(symbol, ()))
            covered |= self._covered(history_messages.get(symbol, []))
            all_paths = self._all_k_paths(symbol)
            if len(all_paths) == 0:
                nt_coverage[symbol] = 1.0
            else:
                nt_coverage[symbol] = len(covered) / len(all_paths)
        return list(sorted(nt_coverage.items(), key=lambda x: (x[1], x[0].name())))
