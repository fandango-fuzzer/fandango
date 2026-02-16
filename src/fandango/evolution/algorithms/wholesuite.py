"""Whole Test Suite Generation algorithm."""

from beartype.typing import Generator, Optional, Any, Sequence
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.chromosomes.suite import Suite
from fandango.language.tree import DerivationTree


class WholeSuiteAlgorithm(GenerationAlgorithm[Suite]):
    """
    Whole Test Suite Generation algorithm.

    Evolves populations of test suites (not individual test cases),
    optimizing for suite-level coverage of grammar elements.

    https://ieeexplore.ieee.org/abstract/document/6152257

    TODO(lk): Implement WholeSuiteAlgorithm.
    """

    def generate_initial_population(self) -> Generator[DerivationTree, None, None]:
        raise NotImplementedError("WholeSuiteAlgorithm is not yet implemented")
        yield  # Make this a generator function

    def generate(
        self, max_generations: Optional[int] = None
    ) -> Generator[DerivationTree, None, None]:
        raise NotImplementedError("WholeSuiteAlgorithm is not yet implemented")
        yield  # Make this a generator function

    @property
    def population(self) -> Sequence[Suite]:
        raise NotImplementedError("WholeSuiteAlgorithm is not yet implemented")

    @property
    def evaluation(self) -> Sequence[Any]:
        raise NotImplementedError("WholeSuiteAlgorithm is not yet implemented")
