from collections.abc import Callable
from typing import Optional

from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.coverage.kpath_coverage import KPathCoverage
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class CoverageTracker:
    """
    Measures k-path coverage of the current and past protocol runs.
    """

    def __init__(
        self,
        coverage: KPathCoverage,
        model: ProtocolModel,
        start_symbol: NonTerminal,
        input_parties: Callable[[], set[str]],
        history: Callable[[], DerivationTree],
        past_derivations: Callable[[], list[DerivationTree]],
        coverage_goal: CoverageGoal,
    ):
        self._coverage = coverage
        self._model = model
        self._start_symbol = start_symbol
        self._input_parties = input_parties
        self._history = history
        self._past_derivations = past_derivations
        self._coverage_goal = coverage_goal
        self._coverage_scores: Optional[list[tuple[NonTerminal, float]]] = None

    def invalidate(self) -> None:
        self._coverage_scores = None

    def set_coverage_goal(self, goal: CoverageGoal) -> None:
        self._coverage_goal = goal

    def uncovered_paths(self) -> list[KPath]:
        return self._coverage.uncovered(
            self._all_trees(),
            self._start_symbol,
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )

    def coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_coverage_scores()
        return self._coverage_scores

    def coverage_percent(self) -> float:
        uncovered = self.uncovered_paths()
        if len(uncovered) == 0:
            return 1.0
        all_paths = self._coverage.all_k_paths(
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        if len(all_paths) == 0:
            return 1.0
        return 1.0 - (len(uncovered) / len(all_paths))

    def _all_trees(self) -> list[DerivationTree]:
        return self._past_derivations() + [self._history()]

    def _compute_coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        """Per-NonTerminal coverage score: covered / total k-paths."""
        messages_by_nt = self._model.group_messages_by_nt(self._all_trees())
        nt_coverage: dict[NonTerminal, float] = {}
        for symbol in self._model.state_grammar_symbols:
            if symbol not in messages_by_nt:
                nt_coverage[symbol] = 0.0
            else:
                nt_coverage[symbol] = self._coverage.ratio(
                    messages_by_nt[symbol], symbol
                )
        return list(sorted(nt_coverage.items(), key=lambda x: (x[1], x[0].name())))
