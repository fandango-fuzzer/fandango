"""Whole Test Suite Generation algorithm."""

from beartype.typing import Generator, Optional, Any, Sequence
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.chromosomes.suite import Suite


class WholeSuiteAlgorithm(GenerationAlgorithm[Suite]):
    """
    Whole Test Suite Generation algorithm.

    Evolves populations of test suites (not individual test cases),
    optimizing for suite-level coverage of grammar elements.

    https://ieeexplore.ieee.org/abstract/document/6152257

    TODO(lk): Implement WholeSuiteAlgorithm.
    """

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        raise NotImplementedError("WholeSuiteAlgorithm is not yet implemented")

    @property
    def population(self) -> Sequence[Suite]:
        raise NotImplementedError("WholeSuiteAlgorithm is not yet implemented")

    @property
    def evaluation(self) -> Sequence[Any]:
        raise NotImplementedError("WholeSuiteAlgorithm is not yet implemented")
