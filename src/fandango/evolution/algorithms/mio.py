"""MIO (Many Independent Objective) algorithm."""

from beartype.typing import Generator, Optional, Any, Sequence
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.chromosomes.individual import Individual
from fandango.language.tree import DerivationTree


class MIOAlgorithm(GenerationAlgorithm[Individual]):
    """
    Many Independent Objective algorithm (MIO).

    MIO maintains an archive of solutions covering different goals
    and uses focused search to explore each goal independently.

    https://arxiv.org/abs/1901.01541

    TODO(lk): Implement MIO.
    """

    def generate_initial_population(self) -> Generator[DerivationTree, None, None]:
        raise NotImplementedError("MIOAlgorithm is not yet implemented")
        yield  # Make this a generator function

    def generate(
        self, max_generations: Optional[int] = None
    ) -> Generator[DerivationTree, None, None]:
        raise NotImplementedError("MIOAlgorithm is not yet implemented")
        yield  # Make this a generator function

    @property
    def population(self) -> Sequence[Individual]:
        raise NotImplementedError("MIOAlgorithm is not yet implemented")

    @property
    def evaluation(self) -> Sequence[Any]:
        raise NotImplementedError("MIOAlgorithm is not yet implemented")
