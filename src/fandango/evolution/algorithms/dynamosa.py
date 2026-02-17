"""Dynamic Many-Objective Sorting Algorithm (DynaMOSA)."""

from beartype.typing import Generator, Optional, Any, Sequence
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.chromosomes import Suite
from fandango.evolution.chromosomes.individual import Individual


class DynaMOSAAlgorithm(GenerationAlgorithm[Individual]):
    """
    Dynamic Many-Objective Sorting Algorithm (DynaMOSA).

    DynaMOSA dynamically formulates test generation as a many-objective problem,
    adding objectives as targets are covered and focusing on uncovered targets.

    https://ieeexplore.ieee.org/document/7840029

    TODO(lk): Implement DynaMOSA.
    """

    def generate_initial_population(self) -> Suite:
        """Generates the initial population."""
        raise NotImplementedError("DynaMOSAAlgorithm is not yet implemented")

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        """Generates solutions for the grammar."""
        raise NotImplementedError("DynaMOSAAlgorithm is not yet implemented")

    @property
    def population(self) -> Sequence[Individual]:
        """Returns the current population."""
        raise NotImplementedError("DynaMOSAAlgorithm is not yet implemented")

    @property
    def evaluation(self) -> Sequence[Any]:
        """Returns the current fitness evaluations."""
        raise NotImplementedError("DynaMOSAAlgorithm is not yet implemented")
