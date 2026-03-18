"""Base fitness classes."""

from abc import ABC, abstractmethod
from beartype.typing import Dict, Any
from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite


class FitnessFunction(ABC):
    """
    Abstract base for fitness evaluation.

    Evaluates chromosomes (Individual or Suite) and returns fitness scores.
    """

    @abstractmethod
    def fitness(self, chromosome: Chromosome) -> float:
        """
        Evaluate fitness of a chromosome.

        Returns:
            Fitness value in [0.0, 1.0]
        """
        pass

    @property
    @abstractmethod
    def cache(self) -> Dict[Any, Any]:
        """Fitness cache for memoization."""
        pass

    @abstractmethod
    def is_maximising(self) -> bool:
        """Whether this fitness function is maximizing (True) or minimizing (False)."""
        pass


class IndividualFitnessFunction(FitnessFunction, ABC):
    """
    Fitness function that evaluates an Individual in isolation.

    Used for constraint-based fitness.

    Implementations should check that the chromosome is an Individual
    in the fitness() method.
    """

    @abstractmethod
    def is_covered(self, individual: Individual) -> bool:
        """Check if an individual satisfies coverage/constraint goals."""
        pass


class SuiteFitnessFunction(FitnessFunction, ABC):
    """
    Fitness function that evaluates test suites based on suite-level properties.

    Used for suite coverage, diversity, suite-level optimization goals.

    Implementations should check that the chromosome is a Suite in the fitness() method.
    """

    @abstractmethod
    def is_covered(self, suite: Suite) -> bool:
        """Check if the suite satisfies coverage goals."""
        pass
