import random
from typing import Counter
from collections.abc import Generator, Sequence

from fandango.constraints.constraint import Constraint
from fandango.constraints.repetition_bounds import RepetitionBoundsConstraint
from fandango.constraints.soft import SoftValue
from fandango.constraints.failing_tree import (
    ApplyAllSuggestions,
    FailingTree,
    NopSuggestion,
    Suggestion,
)
from fandango.language.tree import DerivationTree
from fandango.language.grammar.grammar import Grammar
from fandango.logger import LOGGER, print_exception


class Evaluator:
    def __init__(
        self,
        grammar: Grammar,
        constraints: list[Constraint | SoftValue],
        expected_fitness: float,
        diversity_k: int,
        diversity_weight: float,
        warnings_are_errors: bool = False,
    ):
        self._grammar = grammar
        self._soft_constraints: list[SoftValue] = []
        self._hard_constraints: list[Constraint] = []
        self._repetition_bounds_constraints: list[RepetitionBoundsConstraint] = []
        self._expected_fitness = expected_fitness
        self._diversity_k = diversity_k
        self._diversity_weight = diversity_weight
        self._warnings_are_errors = warnings_are_errors
        self._fitness_cache: dict[int, tuple[float, list[FailingTree], Suggestion]] = {}
        self._solution_set: set[int] = set()
        self._checks_made = 0

        for constraint in constraints:
            if isinstance(constraint, SoftValue):
                self._soft_constraints.append(constraint)
            elif isinstance(constraint, RepetitionBoundsConstraint):
                self._repetition_bounds_constraints.append(constraint)
            elif isinstance(constraint, Constraint):
                self._hard_constraints.append(constraint)
            else:
                raise ValueError(f"Invalid constraint type: {type(constraint)}")

    @property
    def expected_fitness(self) -> float:
        return self._expected_fitness

    def get_fitness_check_count(self) -> int:
        """
        :return: The number of fitness checks made so far.
        """
        return self._checks_made

    def compute_mutation_pool(
        self, population: list[DerivationTree]
    ) -> list[DerivationTree]:
        """
        Computes the mutation pool for the given population.

        The mutation pool is computed by sampling the population with replacement, where the probability of sampling an individual is proportional to its fitness.

        :param population: The population to compute the mutation pool for.
        :return: The mutation pool.
        """
        weights = [self._fitness_cache[hash(ind)][0] for ind in population]
        if not all(w == 0 for w in weights):
            return random.choices(population, weights=weights, k=len(population))
        else:
            return population

    def flush_fitness_cache(self) -> None:
        """
        For soft constraints, the normalized fitness may change over time as we observe more inputs, this method flushes the fitness cache if the grammar contains any soft constraints.
        """
        if len(self._soft_constraints) > 0:
            self._fitness_cache = {}

    def compute_diversity_bonus(self, individuals: list[DerivationTree]) -> list[float]:
        ind_kpaths = [
            self._grammar._extract_k_paths_from_tree(ind, self._diversity_k)
            for ind in individuals
        ]
        frequencies = Counter(path for paths in ind_kpaths for path in paths)

        bonus = [
            (
                sum(1.0 / frequencies[path] for path in paths) / len(paths)
                if paths
                else 0.0
            )
            for paths in ind_kpaths
        ]
        return bonus

    def evaluate_hard_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree], Suggestion]:
        return self._evaluate_constraints(individual, self._hard_constraints)

    def evaluate_repetition_bounds_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree], Suggestion]:
        return self._evaluate_constraints(
            individual, self._repetition_bounds_constraints
        )

    def _evaluate_constraints(
        self, individual: DerivationTree, constraints: Sequence[Constraint]
    ) -> tuple[float, list[FailingTree], Suggestion]:
        if len(constraints) == 0:
            return 1.0, [], NopSuggestion()

        fitness = 0.0
        failing_trees: list[FailingTree] = []
        suggestions = []
        for constraint in constraints:
            try:
                result = constraint.fitness(individual)
                fitness += result.fitness()
                failing_trees.extend(result.failing_trees)
                if result.suggestion is not None:
                    suggestions.append(result.suggestion)
                self._checks_made += 1
            except Exception as e:
                LOGGER.error(
                    f"Error evaluating constraint {constraint.format_as_spec()}"
                )
                print_exception(e)

        # normalize to 0 <= fitness <= 1
        fitness /= len(constraints)
        return (
            fitness,
            failing_trees,
            ApplyAllSuggestions(suggestions),
        )

    def evaluate_soft_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        if not self._soft_constraints:
            return 1.0, []

        soft_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self._soft_constraints:
            try:
                result = constraint.fitness(individual)

                # failing_trees are required for mutations;
                # with soft constraints, we never know when they are fully optimized.
                failing_trees.extend(result.failing_trees)

                constraint.tdigest.update(result.fitness())
                normalized_fitness = constraint.tdigest.score(result.fitness())

                if constraint.optimization_goal == "max":
                    soft_fitness += normalized_fitness
                else:  # "min"
                    soft_fitness += 1 - normalized_fitness
            except Exception as e:
                LOGGER.error(
                    f"Error evaluating soft constraint {constraint.format_as_spec()}: {e}"
                )
                soft_fitness += 0.0

        soft_fitness /= len(self._soft_constraints)
        return soft_fitness, failing_trees

    def evaluate_individual(
        self,
        individual: DerivationTree,
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree], Suggestion]]:
        key = hash(individual)
        if key in self._fitness_cache:
            return self._fitness_cache[key]

        total_constraint_count = (
            len(self._hard_constraints)
            + len(self._repetition_bounds_constraints)
            + len(self._soft_constraints)
        )

        fitness, failing_trees, suggestion = self.evaluate_hard_constraints(individual)

        fully_solved_so_far = fitness == 1.0

        if total_constraint_count > 0:
            # normalize the fitness to the number of hard constraints
            fitness = fitness / (total_constraint_count) * len(self._hard_constraints)

        if len(self._repetition_bounds_constraints) > 0 and fully_solved_so_far:
            # all hard constraints are satisfied, so we can evaluate the repetition bounds constraints
            rep_fitness, rep_failing_trees, rep_suggestion = (
                self.evaluate_repetition_bounds_constraints(individual)
            )
            suggestion = rep_suggestion
            failing_trees.extend(rep_failing_trees)

            fully_solved_so_far = fully_solved_so_far and rep_fitness == 1.0

            # normalize the fitness to the number of constraints
            fitness += (
                rep_fitness
                / total_constraint_count
                * len(self._repetition_bounds_constraints)
            )

        if len(self._soft_constraints) > 0 and fully_solved_so_far:
            # all hard and repetition bounds constraints are satisfied, so we can evaluate the soft constraints
            soft_fitness, soft_failing_trees = self.evaluate_soft_constraints(
                individual
            )

            failing_trees.extend(soft_failing_trees)

            fitness += (
                soft_fitness / total_constraint_count * len(self._soft_constraints)
            )

        if fitness >= self._expected_fitness and key not in self._solution_set:
            self._solution_set.add(key)
            yield individual

        self._fitness_cache[key] = (fitness, failing_trees, suggestion)
        return fitness, failing_trees, suggestion

    def evaluate_population(
        self,
        population: list[DerivationTree],
    ) -> Generator[
        DerivationTree,
        None,
        list[tuple[DerivationTree, float, list[FailingTree], Suggestion]],
    ]:
        evaluation = []
        for ind in population:
            ind_eval = yield from self.evaluate_individual(ind)
            evaluation.append((ind, *ind_eval))

        if self._diversity_k > 0 and self._diversity_weight > 0:
            bonuses = self.compute_diversity_bonus(population)
            evaluation = [
                (ind, fitness + bonus, failing_trees, suggestion)
                for (ind, fitness, failing_trees, suggestion), bonus in zip(
                    evaluation, bonuses
                )
            ]

        return evaluation

    def select_elites(
        self,
        evaluation: list[tuple[DerivationTree, float, list[FailingTree], Suggestion]],
        elitism_rate: float,
        population_size: int,
    ) -> list[DerivationTree]:
        return [
            x[0]
            for x in sorted(evaluation, key=lambda x: x[1], reverse=True)[
                : int(elitism_rate * population_size)
            ]
        ]

    def tournament_selection(
        self,
        evaluation: list[tuple[DerivationTree, float, list[FailingTree], Suggestion]],
        tournament_size: int,
    ) -> tuple[DerivationTree, DerivationTree]:
        tournament = random.sample(evaluation, k=min(tournament_size, len(evaluation)))
        tournament.sort(key=lambda x: x[1], reverse=True)
        parent1 = tournament[0][0]
        if len(tournament) == 2:
            parent2 = tournament[1][0] if tournament[1][0] != parent1 else parent1
        else:
            parent2 = (
                tournament[1][0] if tournament[1][0] != parent1 else tournament[2][0]
            )
        return parent1, parent2
