"""Random Algorithms."""

from beartype.typing import Optional, Any, Sequence, List
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.chromosomes import Individual, Chromosome
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.fitness.base import SuiteFitnessFunction
from fandango.evolution.fitness.suite import (
    GraphCoverageFitnessFunction,
    ConstraintsFitnessFunction,
    SoftConstraintsFitnessFunction,
)
from fandango.language import Grammar
from fandango.language.tree import DerivationTree


def _to_individuals(
    grammar: Grammar, population: Sequence[str | DerivationTree] | None
) -> List[Individual]:
    if population is None:
        return []
    individuals = []
    for item in population:
        if isinstance(item, DerivationTree):
            tree = item
        else:
            tree_candidate = grammar.parse(item)
            if not tree_candidate:
                continue
            tree = tree_candidate
        individual = Individual(tree)
        individuals.append(individual)
    return individuals


def _to_suite(
    grammar: Grammar, population: Sequence[str | DerivationTree] | None
) -> Suite:
    individuals: List[Individual] = _to_individuals(grammar, population)
    return Suite(individuals)


def _generate_individual(grammar: Grammar) -> Individual:
    tree = grammar.fuzz("<start>")
    return Individual(tree)


def _generate_suite(grammar: Grammar, size: int = 10) -> Suite:
    individuals: List[Individual] = [_generate_individual(grammar) for _ in range(size)]
    return Suite(individuals)


class RandomIndividualAlgorithm(GenerationAlgorithm[Individual]):
    """
    Purely Random Individual Algorithm.

    Generates individuals randomly with no mutation or crossover.
    Serves as a baseline against which more sophisticated algorithms are compared.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._initial_population: List[Individual] = _to_individuals(
            self.grammar, kwargs.pop("initial_population", None)
        )
        self.archive.update(self._initial_population)

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        candidate = _generate_individual(self.grammar)
        self.archive.update([candidate])
        generation = 1
        while max_generations is None or generation < max_generations:
            candidate = _generate_individual(self.grammar)
            self.archive.update([candidate])
            generation += 1
        solutions: List[Individual] = [
            s for s in self.archive.solutions if isinstance(s, Individual)
        ]
        # TODO(lk): Individuals would need to be sorted by fitness and cut-off at
        #  population size for a fair comparison
        return Suite(solutions)


class RandomSuiteAlgorithm(GenerationAlgorithm[Suite]):
    """
    Purely Random Suite Algorithm.

    Generates suites randomly with no mutation or crossover.
    Serves as a baseline against which more sophisticated algorithms are compared.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._initial_population: List[Suite] = [
            _to_suite(self.grammar, kwargs.pop("initial_population", None))
        ]
        self._optional_ffs: List[SuiteFitnessFunction] = [
            GraphCoverageFitnessFunction(self.grammar),
            SoftConstraintsFitnessFunction(self.evaluator._soft_constraints),
        ]
        self._mandatory_ffs: List[SuiteFitnessFunction] = [
            ConstraintsFitnessFunction(self.evaluator._hard_constraints),
        ]

    def _mandatory_fitness(self, suite: Suite) -> float:
        return sum(ff.fitness(suite) for ff in self._mandatory_ffs) / len(
            self._mandatory_ffs
        )

    def _optional_fitness(self, suite: Suite) -> float:
        return sum(ff.fitness(suite) for ff in self._optional_ffs) / len(
            self._optional_ffs
        )

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        solution = _generate_suite(self.grammar)
        generation = 1
        while max_generations is None or generation < max_generations:
            candidate = _generate_suite(self.grammar)
            if (
                self._mandatory_fitness(candidate),
                self._optional_fitness(candidate),
            ) > (self._mandatory_fitness(solution), self._optional_fitness(solution)):
                solution = candidate
            generation += 1
        return solution
