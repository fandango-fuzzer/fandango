"""Dynamic Many-Objective Sorting Algorithm (DynaMOSA)."""

import random

from beartype.typing import List, Optional, Any

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.evolution.algorithms.archive import _ConstraintGoal, _SoftConstraintGoal
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.algorithms.random import _generate_individual
from fandango.evolution.chromosomes import Suite
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.crossover import SimpleSubtreeCrossover
from fandango.evolution.selection import TournamentSelection
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal


class _KPathGoalGraph:
    """K-path prefix-dependency hierarchy for DynaMOSA goal management.

    A k-path of length k can only become active once its (k-1)-length prefix
    has been covered. 1-paths are root goals with no prerequisites.
    """

    def __init__(
        self,
        grammar: Grammar,
        max_k: int,
        start_symbol: NonTerminal = NonTerminal("<start>"),
    ) -> None:
        self._max_k = max_k

        # generate_all_k_paths(k=max_k) returns all paths of lengths 1..max_k
        if start_symbol in grammar.rules:
            all_paths: set[KPath] = grammar.generate_all_k_paths(
                k=max_k, non_terminal=start_symbol
            )
        else:
            all_paths = set()

        # Group paths by their length
        self._k_paths_by_length: dict[int, set[KPath]] = {}
        for path in all_paths:
            length = len(path)
            if length not in self._k_paths_by_length:
                self._k_paths_by_length[length] = set()
            self._k_paths_by_length[length].add(path)

        # Build children map: (k-1)-prefix → set of k-paths that extend it
        self._children: dict[KPath, set[KPath]] = {}
        for path in all_paths:
            if len(path) > 1:
                prefix = path[:-1]
                if prefix not in self._children:
                    self._children[prefix] = set()
                self._children[prefix].add(path)

        self._all_goals: frozenset[KPath] = frozenset(all_paths)

    @property
    def root_goals(self) -> set[KPath]:
        """All 1-paths — active from the start, no prerequisites."""
        return set(self._k_paths_by_length.get(1, set()))

    def get_children(self, goal: KPath) -> set[KPath]:
        """Return all k-paths whose (k-1)-length prefix equals goal."""
        return set(self._children.get(goal, set()))

    @property
    def all_goals(self) -> frozenset[KPath]:
        """All k-paths across all lengths 1..max_k."""
        return self._all_goals


class _DynaMOSAGoalManager:
    """Tracks coverage and dynamically manages which goals are active.

    Active goals are the current objectives for the Pareto front ranking.
    A goal becomes active when its (k-1)-prefix has been covered.
    """

    def __init__(
        self,
        grammar: Grammar,
        goal_graph: _KPathGoalGraph,
        max_k: int,
        hard_constraints: List[Constraint] = [],
        soft_constraints: List[SoftValue] = [],
    ) -> None:
        self._grammar = grammar
        self._graph = goal_graph
        self._max_k = max_k
        self._hard_constraints: List[Constraint] = list(hard_constraints)
        self._soft_constraints: List[SoftValue] = list(soft_constraints)

        # Maps each covered optional goal (k-path or soft constraint) to the best individual
        self._optional_covered: dict[KPath | _SoftConstraintGoal, Individual] = {}

        # Mandatory goal tracking: index → best individual satisfying it
        self._mandatory_covered: dict[int, Individual] = {}

        # Mandatory goals (always active from the start)
        constraint_goals: set[_ConstraintGoal] = {
            _ConstraintGoal(i) for i in range(len(self._hard_constraints))
        }
        self._mandatory_goals: frozenset[_ConstraintGoal] = frozenset(constraint_goals)

        soft_goals: set[_SoftConstraintGoal] = {
            _SoftConstraintGoal(i) for i in range(len(self._soft_constraints))
        }

        # Currently active (uncovered) objectives: root k-path goals + all mandatory goals + all soft goals
        self._active: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = (
            set(goal_graph.root_goals) | constraint_goals | soft_goals
        )

    def _satisfies_mandatory(self, individual: Individual) -> bool:
        """Return True if the individual satisfies every hard constraint."""
        return all(
            c.fitness(individual.tree).fitness() >= 1.0 for c in self._hard_constraints
        )

    def _mandatory_covered_by(self, individual: Individual, index: int) -> bool:
        """Return True if the individual satisfies hard_constraint[index]."""
        return self._hard_constraints[index].fitness(individual.tree).fitness() >= 1.0

    def _soft_covered_by(self, individual: Individual, index: int) -> bool:
        """Return True if the individual covers soft_constraint[index] (score >= 0.5)."""
        soft = self._soft_constraints[index]
        raw = soft.fitness(individual.tree).fitness()
        soft.tdigest.update(raw)
        normalized = soft.tdigest.score(raw)
        score = normalized if soft.optimization_goal == "max" else 1 - normalized
        return score >= 0.5

    def _get_paths_for_individual(self, individual: Individual) -> set[KPath]:
        """Extract all k-paths (k=1..max_k) from an individual's derivation tree."""
        tree = individual.tree
        paths: set[KPath] = set()
        for k in range(1, self._max_k + 1):
            paths.update(self._grammar._extract_k_paths_from_tree(tree, k))
        return paths

    def update(self, population: List[Individual]) -> None:
        """Update coverage and active goals from a new population."""
        newly_covered_kpaths: set[KPath] = set()

        for individual in population:
            # --- Mandatory (constraint) goals ---
            for i, _ in enumerate(self._hard_constraints):
                if self._mandatory_covered_by(individual, i):
                    if i not in self._mandatory_covered:
                        self._mandatory_covered[i] = individual
                    elif individual.size() < self._mandatory_covered[i].size():
                        self._mandatory_covered[i] = individual

            # --- Optional (k-path) goals ---
            # Only count a k-path as covered if the individual also satisfies all constraints
            if self._hard_constraints and not self._satisfies_mandatory(individual):
                continue

            ind_paths = self._get_paths_for_individual(individual)
            for goal in self._graph.all_goals:
                if goal in ind_paths:
                    if goal not in self._optional_covered:
                        self._optional_covered[goal] = individual
                        newly_covered_kpaths.add(goal)
                    elif individual.size() < self._optional_covered[goal].size():
                        self._optional_covered[goal] = individual

        # Unlock children of newly covered k-path goals
        for goal in newly_covered_kpaths:
            for child in self._graph.get_children(goal):
                if child not in self._optional_covered:
                    self._active.add(child)

        # --- Soft (optional) constraint goals ---
        for individual in population:
            for i, _ in enumerate(self._soft_constraints):
                if self._soft_covered_by(individual, i):
                    soft_goal = _SoftConstraintGoal(i)
                    if soft_goal not in self._optional_covered:
                        self._optional_covered[soft_goal] = individual
                    elif individual.size() < self._optional_covered[soft_goal].size():
                        self._optional_covered[soft_goal] = individual

        # Remove all covered optional goals (k-paths + soft) from active set
        self._active -= set(self._optional_covered.keys())

        # Remove covered mandatory goals from active set
        for i in self._mandatory_covered:
            self._active.discard(_ConstraintGoal(i))

    @property
    def active_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        return set(self._active)

    @property
    def covered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        return set(self._optional_covered.keys()) | {
            _ConstraintGoal(i) for i in self._mandatory_covered
        }

    @property
    def uncovered_goals(self) -> set[KPath | _ConstraintGoal | _SoftConstraintGoal]:
        kpath_uncovered: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = {
            g for g in self._graph.all_goals if g not in self._optional_covered
        }
        constraint_uncovered: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = {
            _ConstraintGoal(i)
            for i in range(len(self._hard_constraints))
            if i not in self._mandatory_covered
        }
        soft_uncovered: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = {
            _SoftConstraintGoal(i)
            for i in range(len(self._soft_constraints))
            if _SoftConstraintGoal(i) not in self._optional_covered
        }
        return kpath_uncovered | constraint_uncovered | soft_uncovered

    @property
    def solutions(self) -> List[Individual]:
        """Deduplicated best individual per covered goal."""
        seen: set[int] = set()
        result: List[Individual] = []
        for ind in self._optional_covered.values():
            ind_id = id(ind)
            if ind_id not in seen:
                seen.add(ind_id)
                result.append(ind)
        return result


def _compute_pareto_fronts(
    population: List[Individual],
    active_goals: set[KPath | _ConstraintGoal | _SoftConstraintGoal],
    grammar: Grammar,
    max_k: int,
    hard_constraints: List[Constraint] = [],
    soft_constraints: List[SoftValue] = [],
) -> List[List[Individual]]:
    """NSGA-II style Pareto front computation over active k-path and constraint goals.

    Each individual's objective vector: 1 if it covers goal g, 0 otherwise.
    A dominates B if A covers a strict superset of B's covered active goals.
    Within a front, crowding = number of unique active goals covered.
    """
    if not population:
        return []

    if not active_goals:
        return [list(population)]

    n = len(population)

    # Separate active goals by type
    active_kpath_goals = {g for g in active_goals if isinstance(g, tuple)}
    active_constraint_goals = {
        g for g in active_goals if isinstance(g, _ConstraintGoal)
    }
    active_soft_goals = {g for g in active_goals if isinstance(g, _SoftConstraintGoal)}

    # Build coverage sets per individual
    coverage: list[set[KPath | _ConstraintGoal | _SoftConstraintGoal]] = []
    for ind in population:
        # K-path coverage
        ind_paths: set[KPath] = set()
        for k in range(1, max_k + 1):
            ind_paths.update(grammar._extract_k_paths_from_tree(ind.tree, k))
        kpath_cov: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = {
            p for p in ind_paths if p in active_kpath_goals
        }

        # Hard constraint coverage
        constraint_cov: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = {
            g
            for g in active_constraint_goals
            if hard_constraints[g.index].fitness(ind.tree).fitness() >= 1.0
        }

        # Soft constraint coverage (TDigest already updated via goal_manager.update)
        soft_cov: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = set()
        for g in active_soft_goals:
            soft = soft_constraints[g.index]
            raw = soft.fitness(ind.tree).fitness()
            normalized = soft.tdigest.score(raw)
            score = normalized if soft.optimization_goal == "max" else 1 - normalized
            if score >= 0.5:
                soft_cov.add(g)

        coverage.append(kpath_cov | constraint_cov | soft_cov)

    # A dominates B iff A covers a strict superset of B's active goals
    dominated_count: list[int] = [0] * n
    domination_set: list[list[int]] = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if coverage[i] > coverage[j]:  # i dominates j
                domination_set[i].append(j)
                dominated_count[j] += 1
            elif coverage[j] > coverage[i]:  # j dominates i
                domination_set[j].append(i)
                dominated_count[i] += 1

    fronts: list[list[int]] = []
    current_front = [i for i in range(n) if dominated_count[i] == 0]

    while current_front:
        fronts.append(current_front)
        next_front: list[int] = []
        for i in current_front:
            for j in domination_set[i]:
                dominated_count[j] -= 1
                if dominated_count[j] == 0:
                    next_front.append(j)
        current_front = next_front

    return [[population[i] for i in front] for front in fronts]


def _count_active_goals_covered(
    ind: Individual,
    active_goals: set[KPath | _ConstraintGoal | _SoftConstraintGoal],
    grammar: Grammar,
    max_k: int,
    hard_constraints: List[Constraint],
    soft_constraints: List[SoftValue] = [],
) -> int:
    """Count how many active goals an individual covers (for crowding distance)."""
    active_kpath_goals = {g for g in active_goals if isinstance(g, tuple)}
    active_constraint_goals = {
        g for g in active_goals if isinstance(g, _ConstraintGoal)
    }
    active_soft_goals = {g for g in active_goals if isinstance(g, _SoftConstraintGoal)}

    ind_paths: set[KPath] = set()
    for k in range(1, max_k + 1):
        ind_paths.update(grammar._extract_k_paths_from_tree(ind.tree, k))
    kpath_count = len(ind_paths.intersection(active_kpath_goals))

    constraint_count = sum(
        1
        for g in active_constraint_goals
        if hard_constraints[g.index].fitness(ind.tree).fitness() >= 1.0
    )

    soft_count = 0
    for g in active_soft_goals:
        soft = soft_constraints[g.index]
        raw = soft.fitness(ind.tree).fitness()
        normalized = soft.tdigest.score(raw)
        score = normalized if soft.optimization_goal == "max" else 1 - normalized
        if score >= 0.5:
            soft_count += 1

    return kpath_count + constraint_count + soft_count


class DynaMOSAAlgorithm(GenerationAlgorithm[Individual]):
    """
    Dynamic Many-Objective Sorting Algorithm (DynaMOSA).

    DynaMOSA dynamically formulates test generation as a many-objective problem,
    adding objectives as targets are covered and focusing on uncovered targets.

    Goals are k-paths in the grammar, organized in a prefix-dependency hierarchy:
    a k-path becomes active only after its (k-1)-prefix has been covered. This
    focuses search pressure on reachable, uncovered targets.

    Hard constraints are treated as always-active Pareto objectives. A k-path goal
    is only considered covered when a constraint-satisfying individual covers it.

    https://ieeexplore.ieee.org/document/7840029
    """

    def __init__(
        self,
        grammar: Grammar,
        constraints: List[Constraint | SoftValue],
        population_size: int = 10,
        max_k: int = 2,
        crossover_rate: float = 0.8,
        **kwargs: Any,
    ) -> None:
        super().__init__(grammar, constraints, population_size, **kwargs)
        self._max_k = max_k
        self._crossover_rate = crossover_rate
        self._crossover_fn = SimpleSubtreeCrossover()
        self._population: List[Individual] = []

    def _get_random_population(self) -> List[Individual]:
        return [_generate_individual(self.grammar) for _ in range(self.population_size)]

    def _breed_next_generation(
        self,
        active_goals: set[KPath | _ConstraintGoal | _SoftConstraintGoal],
    ) -> List[Individual]:
        """Produce offspring via tournament selection (rank + crowding) + crossover."""
        hard_constraints = self.evaluator._hard_constraints
        soft_constraints = self.evaluator._soft_constraints
        fronts = _compute_pareto_fronts(
            self._population,
            active_goals,
            self.grammar,
            self._max_k,
            hard_constraints,
            soft_constraints,
        )

        # Assign rank and crowding distance to each individual
        rank: dict[int, int] = {}
        crowding: dict[int, int] = {}
        for front_rank, front in enumerate(fronts):
            for ind in front:
                key = id(ind)
                rank[key] = front_rank
                crowding[key] = _count_active_goals_covered(
                    ind,
                    active_goals,
                    self.grammar,
                    self._max_k,
                    hard_constraints,
                    soft_constraints,
                )

        selection_fn: TournamentSelection[Individual] = TournamentSelection(
            tournament_size=2,
            key=lambda ind: (-rank.get(id(ind), 0), crowding.get(id(ind), 0)),
        )

        offspring: List[Individual] = []
        while len(offspring) < self.population_size:
            p1 = selection_fn.select(self._population)[0]
            p2 = selection_fn.select(self._population)[0]
            if random.random() <= self._crossover_rate:
                result = self._crossover_fn.crossover(
                    self.grammar, p1.clone(), p2.clone()
                )
                if result is not None:
                    c1, c2 = result
                    offspring.append(c1)
                    if len(offspring) < self.population_size:
                        offspring.append(c2)
                    continue
            offspring.append(_generate_individual(self.grammar))

        return offspring[: self.population_size]

    def _evolve(self, goal_manager: _DynaMOSAGoalManager) -> None:
        """Run one generation of DynaMOSA evolution."""
        hard_constraints = self.evaluator._hard_constraints
        soft_constraints = self.evaluator._soft_constraints
        active_goals = goal_manager.active_goals
        offspring = self._breed_next_generation(active_goals)
        combined = self._population + offspring

        # NSGA-II truncation: fill new population greedily from Pareto fronts
        fronts = _compute_pareto_fronts(
            combined,
            active_goals,
            self.grammar,
            self._max_k,
            hard_constraints,
            soft_constraints,
        )
        new_population: List[Individual] = []
        for front in fronts:
            if len(new_population) + len(front) <= self.population_size:
                new_population.extend(front)
            else:
                # Sort by crowding distance (descending) to pick the best within front
                front_sorted = sorted(
                    front,
                    key=lambda x: _count_active_goals_covered(
                        x,
                        active_goals,
                        self.grammar,
                        self._max_k,
                        hard_constraints,
                        soft_constraints,
                    ),
                    reverse=True,
                )
                remaining = self.population_size - len(new_population)
                new_population.extend(front_sorted[:remaining])
                break

        # Safety: ensure population is never empty
        while len(new_population) < self.population_size:
            new_population.append(_generate_individual(self.grammar))

        self._population = new_population
        goal_manager.update(self._population)

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        """Generates solutions using DynaMOSA for k-path coverage."""
        start_symbol = NonTerminal("<start>")
        graph = _KPathGoalGraph(self.grammar, self._max_k, start_symbol)
        goal_manager = _DynaMOSAGoalManager(
            self.grammar,
            graph,
            self._max_k,
            hard_constraints=self.evaluator._hard_constraints,
            soft_constraints=self.evaluator._soft_constraints,
        )

        self._population = self._get_random_population()
        goal_manager.update(self._population)

        generation = 0
        while (
            max_generations is None or generation < max_generations
        ) and goal_manager.uncovered_goals:
            self._evolve(goal_manager)
            generation += 1

        solutions = goal_manager.solutions
        if not solutions:
            solutions = (
                self._population[:1]
                if self._population
                else [_generate_individual(self.grammar)]
            )
        return Suite(solutions)
