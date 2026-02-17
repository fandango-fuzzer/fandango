"""Base classes for evolutionary algorithms."""

from abc import ABC, abstractmethod

from beartype.typing import Generator, Optional, Generic, TypeVar, Any, Sequence
from fandango.evolution.chromosomes.base import Chromosome
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
        constraints: Sequence[Constraint | SoftValue],
        population_size: int = 100,
        initial_population: Optional[Sequence[DerivationTree | str]] = None,
        **kwargs: Any,  # Algorithm-specific parameters
    ) -> None:
        self.grammar = grammar
        self.constraints = constraints
        self.population_size = population_size

    @abstractmethod
    def generate_initial_population(self) -> Generator[DerivationTree, None, None]:
        """
        Generate the initial population up to population_size.

        Yields:
            DerivationTree objects as solutions are discovered during initialization
        """
        pass

    @abstractmethod
    def generate(
        self,
        max_generations: Optional[int] = None,
    ) -> Generator[DerivationTree, None, None]:
        """
        Main evolution loop.

        Args:
            max_generations: Maximum number of generations (None = unlimited)

        Yields:
            DerivationTree objects as solutions are discovered
        """
        pass

    @property
    @abstractmethod
    def population(self) -> Sequence[T]:
        """Return current population of chromosomes."""
        pass

    @property
    @abstractmethod
    def evaluation(self) -> Sequence[Any]:
        """
        Return current fitness evaluations.

        Typically a sequence of tuples: (chromosome, fitness, ...).
        """
        pass
