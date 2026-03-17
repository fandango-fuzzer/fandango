"""Whole Test Suite Generation algorithm."""

import random

from beartype.typing import List, Optional, Any, Sequence

from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.algorithms.random import _generate_suite, _generate_individual
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.crossover import SuiteCrossover
from fandango.evolution.fitness.base import SuiteFitnessFunction
from fandango.evolution.fitness.suite import (
    GraphCoverageFitnessFunction,
    ConstraintsFitnessFunction,
    SoftConstraintsFitnessFunction,
)
from fandango.language.grammar.grammar import Grammar
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue


class WholeSuiteAlgorithm(GenerationAlgorithm[Suite]):
    """
    Whole Test Suite Generation algorithm.

    Evolves populations of test suites (not individual test cases),
    optimizing for suite-level coverage of grammar elements.

    https://ieeexplore.ieee.org/abstract/document/6152257
    """

    def __init__(
        self,
        grammar: Grammar,
        constraints: List[Constraint | SoftValue],
        population_size: int = 10,
        crossover_rate: float = 0.8,
        elite: int = 1,
        suite_size: int = 10,
        mutation_probability: float = 0.1,
        **kwargs: Any,
    ) -> None:
        super().__init__(grammar, constraints, population_size, **kwargs)
        self._crossover_rate = crossover_rate
        self._elite = elite
        self._suite_size = suite_size
        self._mutation_probability = mutation_probability
        self._crossover_fn = SuiteCrossover()
        self._optional_ffs: List[SuiteFitnessFunction] = [
            GraphCoverageFitnessFunction(grammar),
            SoftConstraintsFitnessFunction(self.evaluator._soft_constraints),
        ]
        self._mandatory_ffs: List[SuiteFitnessFunction] = [
            ConstraintsFitnessFunction(self.evaluator._hard_constraints),
        ]
        self._population: List[Suite] = []

    def _get_random_population(self) -> List[Suite]:
        return [
            _generate_suite(self.grammar, self._suite_size)
            for _ in range(self.population_size)
        ]

    def _update_archive(self) -> None:
        for suite in self._population:
            self.archive.update(list(suite))

    def _mandatory_fitness(self, suite: Suite) -> float:
        """Average fitness across all mandatory fitness functions."""
        return sum(ff.fitness(suite) for ff in self._mandatory_ffs) / len(
            self._mandatory_ffs
        )

    def _optional_fitness(self, suite: Suite) -> float:
        """Average fitness across all optional fitness functions."""
        return sum(ff.fitness(suite) for ff in self._optional_ffs) / len(
            self._optional_ffs
        )

    def _is_done(self) -> bool:
        if not self._population:
            return False
        best = self._population[0]
        if self.evaluator._hard_constraints:
            return self._mandatory_fitness(best) >= 1.0
        return self._optional_fitness(best) >= 1.0

    def _sort_population(self) -> None:
        self._population.sort(
            key=lambda s: (self._mandatory_fitness(s), self._optional_fitness(s)),
            reverse=True,
        )

    def _get_best_individual(self) -> Suite:
        return (
            self._population[0]
            if self._population
            else _generate_suite(self.grammar, self._suite_size)
        )

    def _mutate_suite(self, suite: Suite) -> Suite:
        new_individuals: List[Individual] = []
        for ind in suite:
            if random.random() < self._mutation_probability:
                # TODO(lk): Mutate failing_trees once constraints are added
                new_individuals.append(_generate_individual(self.grammar))
            else:
                new_individuals.append(ind.clone())
        if not new_individuals:
            new_individuals.append(_generate_individual(self.grammar))
        return Suite(new_individuals)

    def _elitism(self) -> List[Suite]:
        return [s.clone() for s in self._population[: self._elite]]

    def _evolve(self) -> None:
        new_generation: List[Suite] = self._elitism()

        while len(new_generation) < self.population_size:
            parent1 = random.choice(self._population)
            parent2 = random.choice(self._population)
            offspring1 = parent1.clone()
            offspring2 = parent2.clone()

            if random.random() <= self._crossover_rate:
                result = self._crossover_fn.crossover(
                    self.grammar, offspring1, offspring2
                )
                if result is not None:
                    offspring1, offspring2 = result

            offspring1 = self._mutate_suite(offspring1)
            offspring2 = self._mutate_suite(offspring2)

            fitness_parents = max(
                self._optional_fitness(parent1), self._optional_fitness(parent2)
            )
            fitness_offspring = max(
                self._optional_fitness(offspring1),
                self._optional_fitness(offspring2),
            )
            size_parents = parent1.size() + parent2.size()
            size_offspring = offspring1.size() + offspring2.size()

            best_size = max(self._get_best_individual().size(), 1)

            if fitness_offspring > fitness_parents or (
                fitness_offspring == fitness_parents and size_offspring <= size_parents
            ):
                for offspring, parent in [(offspring1, parent1), (offspring2, parent2)]:
                    if len(new_generation) >= self.population_size:
                        break
                    if offspring.size() <= 2 * best_size:
                        new_generation.append(offspring)
                    else:
                        new_generation.append(parent.clone())
            else:
                for parent in [parent1, parent2]:
                    if len(new_generation) >= self.population_size:
                        break
                    new_generation.append(parent.clone())

        self._population = new_generation
        self._update_archive()
        self._sort_population()

    def _get_solution(self) -> Suite:
        archive_solutions = [
            s for s in self.archive.solutions if isinstance(s, Individual)
        ]
        if archive_solutions:
            return Suite(archive_solutions)
        return self._get_best_individual()

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        self._population = self._get_random_population()
        self._update_archive()
        self._sort_population()

        generation = 0
        while (
            max_generations is None or generation < max_generations
        ) and not self._is_done():
            self._evolve()
            generation += 1

        return self._get_solution()
