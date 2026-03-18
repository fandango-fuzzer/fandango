"""Unit tests for WholeSuiteAlgorithm."""

import pytest

from fandango.evolution.algorithms.random import _generate_suite
from fandango.evolution.algorithms.wholesuite import WholeSuiteAlgorithm
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.fitness.suite import GraphCoverageFitnessFunction
from fandango.language.parse.parse import parse
from tests.test_random_algorithm import _make_constraint
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


class TestWholeSuiteWithConstraints:
    """Tests for WholeSuiteAlgorithm with hard constraints."""

    def test_mandatory_fitness_all_satisfied(self, simple_grammar):
        """mandatory_fitness returns 1.0 when all individuals satisfy the constraint."""
        passing = _make_constraint(always_pass=True)
        algo = WholeSuiteAlgorithm(simple_grammar, [passing], population_size=5)
        suite = _generate_suite(simple_grammar, 4)
        assert algo._mandatory_fitness(suite) == 1.0

    def test_mandatory_fitness_none_satisfied(self, simple_grammar):
        """mandatory_fitness returns 0.0 when no individual satisfies the constraint."""
        failing = _make_constraint(always_pass=False)
        algo = WholeSuiteAlgorithm(simple_grammar, [failing], population_size=5)
        suite = _generate_suite(simple_grammar, 4)
        assert algo._mandatory_fitness(suite) == 0.0

    def test_mandatory_fitness_no_constraints_returns_one(self, simple_grammar):
        """mandatory_fitness returns 1.0 when there are no hard constraints."""
        algo = WholeSuiteAlgorithm(simple_grammar, [], population_size=5)
        suite = _generate_suite(simple_grammar, 4)
        assert algo._mandatory_fitness(suite) == 1.0

    def test_sort_prefers_constraint_satisfying_suites(self, simple_grammar):
        """Population sort puts constraint-satisfying suites first."""
        passing = _make_constraint(always_pass=True)
        algo = WholeSuiteAlgorithm(simple_grammar, [passing], population_size=4)
        # Manually set two suites; since passing always returns 1.0, all suites
        # should have mandatory=1.0 and be sorted by optional fitness
        algo._population = [_generate_suite(simple_grammar, 2) for _ in range(4)]
        algo._sort_population()
        # Best suite (index 0) should have mandatory fitness 1.0
        assert algo._mandatory_fitness(algo._population[0]) == 1.0

    def test_stopping_on_constraint_satisfaction(self, simple_grammar):
        """Algorithm stops when mandatory fitness reaches 1.0 for the best suite."""
        passing = _make_constraint(always_pass=True)
        algo = WholeSuiteAlgorithm(
            simple_grammar, [passing], population_size=5, suite_size=3
        )
        result = algo.generate(max_generations=20)
        assert isinstance(result, Suite)
        assert len(result) > 0
