"""Base classes for evolutionary algorithms."""

from abc import ABC, abstractmethod

from beartype.typing import Optional, Generic, TypeVar, Any, Sequence, List

from fandango.evolution.algorithms.archive import CoverageArchive, Archive
from fandango.evolution.chromosomes import Suite
from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.evaluation import Evaluator
from fandango.language.tree import DerivationTree
from fandango.language.grammar.grammar import Grammar
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue

T = TypeVar("T", bound=Chromosome)


class GenerationAlgorithm(ABC, Generic[T]):
    """
    Abstract base class for evolutionary test generation algorithms.

    Generic over Chromosome type (Individual or Suite).
    """

    def __init__(
        self,
        grammar: Grammar,
        constraints: List[Constraint | SoftValue],
        population_size: int = 10,
        initial_population: Optional[Sequence[DerivationTree | str]] = None,
        **kwargs: Any,  # Algorithm-specific parameters
    ) -> None:
        self.grammar = grammar
        self.constraints = constraints
        self.population_size = population_size
        self.archive: Archive = CoverageArchive(grammar)

        # Only to be compatible with Fandango (class)
        # TODO(lk): In the long term we probably want to make Fandango a subclass of this
        self.average_population_fitness: float = -1.0
        self.evaluator = Evaluator(
            grammar,
            constraints,
            expected_fitness=1.0,
            diversity_k=1,
            diversity_weight=0.0,
        )
        self.population: List[DerivationTree] = []

    @abstractmethod
    def generate(
        self,
        max_generations: Optional[int] = None,
    ) -> Suite:
        """
        Main evolution loop.

        Args:
            max_generations: Maximum number of generations (None = unlimited)

        Yields:
            DerivationTree objects as solutions are discovered
        """
        pass
