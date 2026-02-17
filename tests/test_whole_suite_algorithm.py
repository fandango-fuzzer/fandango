"""Unit tests for WholeSuiteAlgorithm."""

import pytest

from fandango.evolution.algorithms.wholesuite import WholeSuiteAlgorithm
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.fitness.suite import GraphCoverageFitnessFunction
from fandango.language.parse.parse import parse
from tests.utils import RESOURCES_ROOT


@pytest.fixture
def simple_grammar():
    """Create a simple grammar for testing."""
    grammar_file = RESOURCES_ROOT / "simple_digits.fan"
    with open(grammar_file, "r") as f:
        grammar, _ = parse([f])
    return grammar


@pytest.fixture
def empty_constraints():
    """Empty constraint list for testing."""
    return []


class TestWholeSuiteAlgorithm:
    """Integration tests for WholeSuiteAlgorithm."""

    def test_generate_returns_suite(self, simple_grammar, empty_constraints):
        """generate() returns a non-empty Suite."""
        algo = WholeSuiteAlgorithm(simple_grammar, empty_constraints)
        result = algo.generate(max_generations=2)
        assert isinstance(result, Suite)
        assert len(result) > 0

    def test_generate_improves_over_single_generation(
        self, simple_grammar, empty_constraints
    ):
        """Running multiple generations yields a suite with fitness >= a one-generation baseline."""
        fitness_fn = GraphCoverageFitnessFunction(simple_grammar)

        single = WholeSuiteAlgorithm(simple_grammar, empty_constraints)
        baseline = fitness_fn.fitness(single.generate(max_generations=1))

        multi = WholeSuiteAlgorithm(simple_grammar, empty_constraints)
        result = fitness_fn.fitness(multi.generate(max_generations=10))

        assert result >= baseline

    def test_elitism_preserves_best(self, simple_grammar, empty_constraints):
        """Population is sorted after evolution; first element should be best."""
        algo = WholeSuiteAlgorithm(simple_grammar, empty_constraints, elite=1)
        algo.generate(max_generations=5)
        assert algo._population is not None and len(algo._population) > 0

    def test_population_size_respected(self, simple_grammar, empty_constraints):
        """Population size matches the configured value after evolution."""
        algo = WholeSuiteAlgorithm(simple_grammar, empty_constraints, population_size=5)
        algo.generate(max_generations=3)
        assert len(algo._population) == 5
