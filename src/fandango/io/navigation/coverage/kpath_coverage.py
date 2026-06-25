from typing import Optional

from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class KPathCoverage:
    """k-path coverage of derivation trees over multiple protocol runs against the grammar."""

    def __init__(self, grammar: Grammar, diversity_k: int):
        self._grammar = grammar
        self._diversity_k = diversity_k

    def uncovered(
        self,
        trees: list[DerivationTree],
        non_terminal: Optional[NonTerminal] = None,
        *,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> list[KPath]:
        """Grammar k-paths not yet covered by the trees."""
        return self._grammar.get_uncovered_k_paths(
            trees,
            self._diversity_k,
            non_terminal,
            overlap_to_root=overlap_to_root,
            coverage_goal=coverage_goal,
            input_parties=input_parties,
        )

    def ratio(
        self,
        trees: list[DerivationTree],
        non_terminal: Optional[NonTerminal] = None,
        *,
        overlap_to_root: bool = False,
    ) -> float:
        """Covered / total k-paths for the trees."""
        return self._grammar.compute_kpath_coverage(
            trees, self._diversity_k, non_terminal, overlap_to_root
        )

    def all_k_paths(
        self,
        non_terminal: Optional[NonTerminal] = None,
        *,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        """All k-paths the grammar can produce."""
        return self._grammar.generate_all_k_paths(
            k=self._diversity_k,
            non_terminal=non_terminal,
            coverage_goal=coverage_goal,
            input_parties=input_parties,
        )
