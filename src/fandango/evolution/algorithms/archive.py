"""Archive classes for tracking coverage goals during evolutionary search."""

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

from beartype.typing import Iterable, List, Optional

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.evolution.chromosomes import Chromosome
from fandango.evolution.chromosomes.individual import Individual
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal


@dataclass(frozen=True)
class _ConstraintGoal:
    """A goal representing one hard constraint that must be satisfied."""

    index: int  # position in hard_constraints list


@dataclass(frozen=True)
class _SoftConstraintGoal:
    """A goal representing one soft constraint to be optimised."""

    index: int  # position in soft_constraints list


class Archive(ABC):
    """Abstract base class for coverage archives."""

    @abstractmethod
    def update(self, individuals: Iterable[Chromosome]) -> bool:
        """Update archive; return True iff any change was made."""

    @property
    @abstractmethod
    def solutions(self) -> List[Chromosome]:
        """Deduplicated list of best Individuals (highest combined score), one per covered goal."""

    @property
    @abstractmethod
    def covered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        """Set of k-paths that have been covered."""

    @property
    @abstractmethod
    def uncovered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
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
        self._goals: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = {
            g
            for g in (
                grammar.generate_all_k_paths(k=k, non_terminal=start_symbol)
                if start_symbol in grammar.rules
                else set()
            )
        }
        self._covered: dict[
            KPath | _ConstraintGoal | _SoftConstraintGoal, Chromosome
        ] = {}
        self._uncovered: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = (
            self._goals
        )

    def update(self, individuals: Iterable[Chromosome]) -> bool:
        """
        Update the archive with a collection of individuals.

        Returns True iff at least one change was made (new goal covered or
        a shorter individual replaced the current best for a goal).
        As each goal is a k-path, taking the shortest individual is okay.

        TODO(lk): Also consider hard and soft constraints
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
    def covered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        """Goals that have been covered by at least one individual."""
        return set(self._covered.keys())

    @property
    def uncovered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        """Goals not yet covered by any individual."""
        return self._goals - self.covered_goals


class MIOArchive(Archive):
    """
    Archive for the MIO algorithm.

    Maintains a best individual (highest combined score) per covered goal.
    Each goal is treated independently of each other, i.e. a individual might satisfy a k-path goal while not satisfying (all) hard constraints.
    This adaption was made to achieve diversity during search.
    """

    def __init__(
        self,
        grammar: Grammar,
        n: int = 10,
        k: int = 2,
        start_symbol: NonTerminal = NonTerminal("<start>"),
        hard_constraints: List[Constraint] = [],
        soft_constraints: List[SoftValue] = [],
    ) -> None:
        super().__init__()
        self._grammar = grammar
        self._k = k
        self._n = n
        self._hard_constraints: List[Constraint] = list(hard_constraints)
        self._soft_constraints: List[SoftValue] = list(soft_constraints)
        self._goals: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = {
            g
            for g in (
                grammar.generate_all_k_paths(k=k, non_terminal=start_symbol)
                if start_symbol in grammar.rules
                else set()
            )
        }
        for i in range(len(hard_constraints)):
            self._goals.add(_ConstraintGoal(i))
        for i in range(len(soft_constraints)):
            self._goals.add(_SoftConstraintGoal(i))
        self._covered: dict[
            KPath | _ConstraintGoal | _SoftConstraintGoal, Chromosome
        ] = {}
        self._uncovered_populations: dict[
            KPath | _ConstraintGoal | _SoftConstraintGoal, list[Chromosome]
        ] = {}

    def _satisfies_mandatory(self, individual: Individual) -> bool:
        """Return True if individual satisfies every hard constraint."""
        return all(
            c.fitness(individual.tree).fitness() >= 1.0 for c in self._hard_constraints
        )

    def _soft_covered_by(self, individual: Individual, index: int) -> bool:
        """Return True if individual covers soft_constraint[index] (score >= 0.5)."""
        soft = self._soft_constraints[index]
        raw = soft.fitness(individual.tree).fitness()
        soft.tdigest.update(raw)
        normalized = soft.tdigest.score(raw)
        score = normalized if soft.optimization_goal == "max" else 1 - normalized
        return score >= 0.5

    def _combined_score(self, individual: Chromosome) -> float:
        """
        Compute a combined quality score in [0.0, 1.0] for tiebreaking.

        Equal weight is given to:
          1. K-path coverage fraction: fraction of grammar k-path goals covered
             by this individual.
          2. Average normalised soft score: mean percentile score across all
             soft constraints (0.0 for non-Individual chromosomes or no soft
             constraints).
        """
        # --- K-path coverage fraction ---
        kpath_goals: set[KPath] = {g for g in self._goals if isinstance(g, tuple)}
        if kpath_goals:
            trees = individual.to_derivation_trees()
            ind_paths: set[KPath] = {
                path
                for tree in trees
                for path in self._grammar._extract_k_paths_from_tree(tree, k=self._k)
            }
            kpath_fraction = len(ind_paths & kpath_goals) / len(kpath_goals)
        else:
            kpath_fraction = 0.0

        # --- Average normalised soft score ---
        if self._soft_constraints and isinstance(individual, Individual):
            scores = []
            for soft in self._soft_constraints:
                raw = soft.fitness(individual.tree).fitness()
                soft.tdigest.update(raw)
                normalized = soft.tdigest.score(raw)
                score = (
                    normalized if soft.optimization_goal == "max" else 1 - normalized
                )
                scores.append(score)
            avg_soft_score = sum(scores) / len(scores)
        else:
            avg_soft_score = 0.0

        return (kpath_fraction + avg_soft_score) / 2.0

    def _try_cover(
        self,
        goal: KPath | _ConstraintGoal | _SoftConstraintGoal,
        individual: Chromosome,
    ) -> bool:
        """
        Cover goal with individual if not yet covered, or replace the incumbent
        if individual has a higher combined score. Returns True if changed.
        """
        if goal not in self._covered:
            self._covered[goal] = individual
            self._uncovered_populations.pop(goal, None)
            return True
        if self._combined_score(individual) > self._combined_score(self._covered[goal]):
            self._covered[goal] = individual
            return True
        return False

    def _process_soft_goals(self, individual: Individual) -> bool:
        """Evaluate all soft-constraint goals for individual. Returns True if any changed."""
        changed = False
        for i, _ in enumerate(self._soft_constraints):
            s_goal = _SoftConstraintGoal(i)
            if s_goal in self._goals and self._soft_covered_by(individual, i):
                changed |= self._try_cover(s_goal, individual)
        return changed

    def update(self, individuals: Iterable[Chromosome]) -> bool:
        """Update archive with new individuals. Returns True if any change was made."""
        changed = False
        for individual in individuals:
            # --- Hard constraint goals ---
            if isinstance(individual, Individual):
                for i, hard in enumerate(self._hard_constraints):
                    h_goal = _ConstraintGoal(i)
                    if (
                        h_goal in self._goals
                        and hard.fitness(individual.tree).fitness() >= 1.0
                    ):
                        changed |= self._try_cover(h_goal, individual)

            # --- K-path goals ---
            trees = individual.to_derivation_trees()
            paths = {
                path
                for tree in trees
                for path in self._grammar._extract_k_paths_from_tree(tree, k=self._k)
            }
            for path in paths & self._goals:
                changed |= self._try_cover(path, individual)

            # --- Soft constraint goals ---
            if isinstance(individual, Individual):
                changed |= self._process_soft_goals(individual)

        return changed

    def get_solution(self) -> Optional[Chromosome]:
        """Return a random candidate from uncovered goal populations."""
        goals_with_candidates = [
            g for g in self.uncovered_goals if self._uncovered_populations.get(g)
        ]
        if not goals_with_candidates:
            return None
        goal = random.choice(goals_with_candidates)
        return random.choice(self._uncovered_populations[goal])

    def shrink_solutions(self, n: int) -> None:
        """Reduce uncovered pools to at most n candidates (keep shortest)."""
        self._n = n
        for goal in list(self._uncovered_populations):
            pool = self._uncovered_populations[goal]
            if len(pool) > n:
                pool.sort(key=lambda p: p.size())
                self._uncovered_populations[goal] = pool[:n]

    @property
    def num_covered_targets(self) -> int:
        return len(self._covered)

    @property
    def all_hard_goals_covered(self) -> bool:
        """True iff every hard-constraint goal has been covered by at least one individual."""
        return all(
            _ConstraintGoal(i) in self._covered
            for i in range(len(self._hard_constraints))
        )

    @property
    def search_complete(self) -> bool:
        """True when the termination criterion is met.

        With hard constraints: done when every hard-constraint goal is covered.
        Without hard constraints: done when all goals (k-paths, soft) are covered.
        """
        if self._hard_constraints:
            return self.all_hard_goals_covered
        return not self.uncovered_goals

    @property
    def valid_solutions(self) -> List[Chromosome]:
        """Solutions filtered to only those satisfying all hard constraints.

        When no hard constraints are present, returns all solutions.
        """
        if not self._hard_constraints:
            return self.solutions
        return [
            ind
            for ind in self.solutions
            if isinstance(ind, Individual) and self._satisfies_mandatory(ind)
        ]

    @property
    def solutions(self) -> List[Chromosome]:
        """Deduplicated individuals covering at least one goal, highest combined score wins."""
        return list(dict.fromkeys(self._covered.values()))

    @property
    def covered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        """Goals that have been covered by at least one individual."""
        return set(self._covered.keys())

    @property
    def uncovered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        """Goals not yet covered by any individual."""
        return self._goals - self.covered_goals
