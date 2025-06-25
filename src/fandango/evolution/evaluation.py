import random
from typing import Counter, Union
from collections.abc import Generator

from fandango.constraints.base import Constraint, SoftValue
from fandango.constraints.fitness import FailingTree
from fandango.language import DerivationTree, Grammar
from fandango.logger import LOGGER


class Evaluator:
    def __init__(
        self,
        grammar: Grammar,
        constraints: list[Union[Constraint, SoftValue]],
        expected_fitness: float,
        diversity_k: int,
        diversity_weight: float,
        warnings_are_errors: bool = False,
    ):
        self._grammar = grammar
        self._soft_constraints: list[SoftValue] = []
        self._hard_constraints: list[Constraint] = []
        self._expected_fitness = expected_fitness
        self._diversity_k = diversity_k
        self._diversity_weight = diversity_weight
        self._warnings_are_errors = warnings_are_errors
        self._fitness_cache: dict[int, tuple[float, list[FailingTree]]] = {}
        self._solution_set: set[int] = set()
        self._checks_made = 0

        for constraint in constraints:
            if isinstance(constraint, SoftValue):
                self._soft_constraints.append(constraint)
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
    ) -> tuple[float, list[FailingTree]]:
        if len(self._hard_constraints) == 0:
            return 1.0, []

        hard_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self._hard_constraints:
            try:
                result = constraint.fitness(individual)

                if result.success:
                    hard_fitness += result.fitness()
                else:
                    failing_trees.extend(result.failing_trees)
                    hard_fitness += result.fitness()
                self._checks_made += 1
            except Exception as e:
                LOGGER.error(f"Error evaluating hard constraint {constraint}: {e}")
                hard_fitness += 0.0
        hard_fitness /= len(self._hard_constraints)
        return hard_fitness, failing_trees

    def evaluate_soft_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
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
                LOGGER.error(f"Error evaluating soft constraint {constraint}: {e}")
                soft_fitness += 0.0

        soft_fitness /= len(self._soft_constraints)
        return soft_fitness, failing_trees

    def evaluate_individual(
        self,
        individual: DerivationTree,
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree]]]:
        key = hash(individual)
        if key in self._fitness_cache:
            return self._fitness_cache[key]

        fitness, failing_trees = self.evaluate_hard_constraints(individual)

        if self._soft_constraints:
            if fitness < 1.0:
                fitness = (
                    fitness
                    * len(self._hard_constraints)
                    / (len(self._hard_constraints) + len(self._soft_constraints))
                )
            else:  # fitness from hard constraints == 1.0
                soft_fitness, soft_failing_trees = self.evaluate_soft_constraints(
                    individual
                )

                failing_trees.extend(soft_failing_trees)

                fitness = (
                    fitness * len(self._hard_constraints)
                    + soft_fitness * len(self._soft_constraints)
                ) / (len(self._hard_constraints) + len(self._soft_constraints))

        if fitness >= self._expected_fitness and key not in self._solution_set:
            self._solution_set.add(key)
            yield individual

        self._fitness_cache[key] = (fitness, failing_trees)
        return fitness, failing_trees

    def evaluate_population(
        self,
        population: list[DerivationTree],
    ) -> Generator[
        DerivationTree, None, list[tuple[DerivationTree, float, list[FailingTree]]]
    ]:
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]] = []
        for ind in population:
            ind_eval = yield from self.evaluate_individual(ind)
            evaluation.append((ind, *ind_eval))

        if self._diversity_k > 0 and self._diversity_weight > 0:
            bonuses = self.compute_diversity_bonus(population)
            evaluation = [
                (ind, fitness + bonus, failing_trees)
                for (ind, fitness, failing_trees), bonus in zip(evaluation, bonuses)
            ]

        return evaluation

    def select_elites(
        self,
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]],
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
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]],
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
