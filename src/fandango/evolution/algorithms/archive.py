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
        """Deduplicated list of best (shortest) Individuals, one per covered goal."""

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

    Maintains a best (shortest) individual per covered goal, and a bounded
    pool of candidate individuals per uncovered goal for focused mutation.
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

    def update(self, individuals: Iterable[Chromosome]) -> bool:
        """Update archive with new individuals. Returns True if any change was made."""
        changed = False
        for individual in individuals:
            # --- Hard constraint goals (mandatory) ---
            if isinstance(individual, Individual):
                for i, _ in enumerate(self._hard_constraints):
                    h_goal = _ConstraintGoal(i)
                    if h_goal in self._goals:
                        covered = (
                            self._hard_constraints[i].fitness(individual.tree).fitness()
                            >= 1.0
                        )
                        if covered:
                            if h_goal not in self._covered:
                                self._covered[h_goal] = individual
                                self._uncovered_populations.pop(h_goal, None)
                                changed = True
                            elif individual.size() < self._covered[h_goal].size():
                                self._covered[h_goal] = individual
                                changed = True

            # --- K-path goals (gated by hard constraints) ---
            if self._hard_constraints and isinstance(individual, Individual):
                if not self._satisfies_mandatory(individual):
                    # Still process soft constraints before skipping k-paths
                    for i, _ in enumerate(self._soft_constraints):
                        s_goal = _SoftConstraintGoal(i)
                        if s_goal in self._goals and self._soft_covered_by(
                            individual, i
                        ):
                            if s_goal not in self._covered:
                                self._covered[s_goal] = individual
                                self._uncovered_populations.pop(s_goal, None)
                                changed = True
                            elif individual.size() < self._covered[s_goal].size():
                                self._covered[s_goal] = individual
                                changed = True
                    continue

            trees = individual.to_derivation_trees()
            paths = {
                path
                for tree in trees
                for path in self._grammar._extract_k_paths_from_tree(tree, k=self._k)
            }
            for path in paths & self._goals:
                if path in self._covered:
                    if individual.size() < self._covered[path].size():
                        self._covered[path] = individual
                        changed = True
                else:
                    # Newly covered -- update best and clear uncovered pool
                    self._covered[path] = individual
                    self._uncovered_populations.pop(path, None)
                    changed = True

            # --- Soft constraint goals (optional) ---
            if isinstance(individual, Individual):
                for i, _ in enumerate(self._soft_constraints):
                    s_goal = _SoftConstraintGoal(i)
                    if s_goal in self._goals and self._soft_covered_by(individual, i):
                        if s_goal not in self._covered:
                            self._covered[s_goal] = individual
                            self._uncovered_populations.pop(s_goal, None)
                            changed = True
                        elif individual.size() < self._covered[s_goal].size():
                            self._covered[s_goal] = individual
                            changed = True

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
