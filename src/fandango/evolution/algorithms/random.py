"""Random Algorithms."""

from beartype.typing import Optional, Any, Sequence, List
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.chromosomes import Individual
from fandango.evolution.chromosomes.suite import Suite
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


def _to_suites(
    grammar: Grammar, population: Sequence[str | DerivationTree] | None
) -> List[Suite]:
    individuals: List[Individual] = _to_individuals(grammar, population)
    return [Suite(individuals)]


class RandomIndividualAlgorithm(GenerationAlgorithm[Individual]):
    """
    Purely Random Individual Algorithm.

    Generates individuals randomly with no mutation or crossover.
    Serves as a baseline against which more sophisticated algorithms are compared.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._population: List[Individual] = []
        self._initial_population: List[Individual] = _to_individuals(
            self.grammar, kwargs.pop("initial_population", None)
        )

    def generate_initial_population(self) -> Suite:
        while len(self._population) < self.population_size:
            tree = self.grammar.fuzz("<start>")
            individual = Individual(tree)
            self._population.append(individual)
        return Suite(self._population)

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        generation = 0
        while max_generations is None or generation < max_generations:
            tree = self.grammar.fuzz("<start>")
            individual = Individual(tree)
            self._population.append(individual)
            generation += 1
        return Suite(self._population)

    @property
    def population(self) -> Sequence[Individual]:
        return self._population

    @property
    def evaluation(self) -> Sequence[Any]:
        return []


class RandomSuiteAlgorithm(GenerationAlgorithm[Suite]):
    """
    Purely Random Suite Algorithm.

    Generates suites randomly with no mutation or crossover.
    Serves as a baseline against which more sophisticated algorithms are compared.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._population: List[Suite] = []
        self._initial_population: List[Suite] = _to_suites(
            self.grammar, kwargs.pop("initial_population", None)
        )

    def generate_initial_population(self) -> Suite:
        while len(self._population) < self.population_size:
            tree = self.grammar.fuzz("<start>")
            individual = Individual(tree)
            suite = Suite([individual])
            self._population.append(suite)
        return self._population[0]

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        self.generate_initial_population()
        generation = 1
        while max_generations is None or generation < max_generations:
            tree = self.grammar.fuzz("<start>")
            individual = Individual(tree)
            suite = Suite([individual])
            self._population.append(suite)
            generation += 1
        return self._population[0]

    @property
    def population(self) -> Sequence[Suite]:
        return self._population

    @property
    def evaluation(self) -> Sequence[Any]:
        return []
