"""Archive classes for tracking coverage goals during evolutionary search."""

from abc import ABC, abstractmethod

from beartype.typing import Iterable, List

from fandango.evolution.chromosomes import Chromosome
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal


class Archive(ABC):
    """Abstract base class for coverage archives."""

    @abstractmethod
    def update(self, individuals: Iterable[Chromosome]) -> bool:
        """Update archive; return True iff any change was made."""

    @property
    @abstractmethod
    def solutions(self) -> List[Chromosome]:
        """Deduplicated list of best (shortest) Individuals, one per covered goal."""

    @property
    @abstractmethod
    def covered_goals(self) -> set[KPath]:
        """Set of k-paths that have been covered."""

    @property
    @abstractmethod
    def uncovered_goals(self) -> set[KPath]:
        """Set of k-paths not yet covered."""


class CoverageArchive(Archive):
    """
    Coverage archive that tracks k-path goals and the best Individual per goal.

    "Best" is defined as shortest (fewest nodes in the derivation tree).
    """

    def __init__(
        self,
        grammar: Grammar,
        k: int = 2,
        start_symbol: NonTerminal = NonTerminal("<start>"),
    ) -> None:
        super().__init__()
        self._grammar = grammar
        self._k = k
        self._goals: set[KPath] = (
            grammar.generate_all_k_paths(k=k, non_terminal=start_symbol)
            if start_symbol in grammar.rules
            else set()
        )
        self._covered: dict[KPath, Chromosome] = {}
        self._uncovered: set[KPath] = self._goals

    def update(self, individuals: Iterable[Chromosome]) -> bool:
        """
        Update the archive with a collection of individuals.

        Returns True iff at least one change was made (new goal covered or
        a shorter individual replaced the current best for a goal).
        """
        changed = False
        for individual in individuals:
            trees = individual.to_derivation_trees()
            paths = {
                path
                for tree in trees
                for path in self._grammar._extract_k_paths_from_tree(tree, k=self._k)
            }
            for path in paths & self._goals:
                if path not in self._covered:
                    self._covered[path] = individual
                    changed = True
                elif individual.size() < self._covered[path].size():
                    self._covered[path] = individual
                    changed = True
        return changed

    @property
    def solutions(self) -> List[Chromosome]:
        """Deduplicated individuals covering at least one goal, shortest wins."""
        return list(dict.fromkeys(self._covered.values()))

    @property
    def covered_goals(self) -> set[KPath]:
        """Goals that have been covered by at least one individual."""
        return set(self._covered.keys())

    @property
    def uncovered_goals(self) -> set[KPath]:
        """Goals not yet covered by any individual."""
        return self._goals - self.covered_goals
