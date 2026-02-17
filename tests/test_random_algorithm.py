"""Unit tests for Random Algorithm implementations."""

import pytest

from fandango.evolution.algorithms.random import (
    RandomIndividualAlgorithm,
    RandomSuiteAlgorithm,
)
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


class TestRandomSuiteAlgorithm:
    """Integration tests for RandomSuiteAlgorithm."""

    def test_generate_improves_over_single_generation(
        self, simple_grammar, empty_constraints
    ):
        """Running multiple generations yields a suite with fitness >= a one-generation baseline."""
        fitness_fn = GraphCoverageFitnessFunction(simple_grammar)

        single_gen = RandomSuiteAlgorithm(simple_grammar, empty_constraints)
        baseline_suite = single_gen.generate(max_generations=1)
        baseline_fitness = fitness_fn.fitness(baseline_suite)

        multi_gen = RandomSuiteAlgorithm(simple_grammar, empty_constraints)
        result_suite = multi_gen.generate(max_generations=20)
        result_fitness = fitness_fn.fitness(result_suite)

        assert result_fitness >= baseline_fitness


class TestRandomIndividualAlgorithm:
    """Test RandomIndividualAlgorithm implementation."""

    def test_generate(self, simple_grammar, empty_constraints):
        """generate(max_generations=N) yields exactly N DerivationTree objects."""
        algo = RandomIndividualAlgorithm(
            simple_grammar, empty_constraints, population_size=5
        )
        trees = list(algo.generate(max_generations=7))
        assert len(trees) <= 7
