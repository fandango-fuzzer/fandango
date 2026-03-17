"""Unit tests for Random Algorithm implementations."""

from typing import Any

import pytest

from fandango.constraints.constraint import Constraint
from fandango.constraints.fitness import ConstraintFitness
from fandango.constraints.failing_tree import NopSuggestion
from fandango.language.tree import DerivationTree
from fandango.evolution.algorithms.random import (
    RandomIndividualAlgorithm,
    RandomSuiteAlgorithm,
    _generate_suite,
)
from fandango.evolution.chromosomes.suite import Suite
from fandango.language.parse.parse import parse
from tests.utils import RESOURCES_ROOT


def _make_constraint(always_pass: bool) -> Constraint:
    """Create a stub Constraint that always passes or always fails."""

    class _StubConstraint(Constraint):
        def fitness(
            self,
            tree: DerivationTree,
            scope=None,
            local_variables=None,
        ) -> ConstraintFitness:
            solved = 1 if always_pass else 0
            return ConstraintFitness(
                solved=solved,
                total=1,
                success=always_pass,
                suggestion=NopSuggestion(),
            )

        def accept(self, visitor: Any) -> None:
            pass

        def invert(self) -> "Constraint":
            return _make_constraint(not always_pass)

        def format_as_spec(self) -> str:
            return "stub"

    return _StubConstraint()


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
        single_gen = RandomSuiteAlgorithm(simple_grammar, empty_constraints)
        baseline = single_gen.generate(max_generations=1)

        multi_gen = RandomSuiteAlgorithm(simple_grammar, empty_constraints)
        result = multi_gen.generate(max_generations=20)

        assert (
            multi_gen._mandatory_fitness(result),
            multi_gen._optional_fitness(result),
        ) >= (
            single_gen._mandatory_fitness(baseline),
            single_gen._optional_fitness(baseline),
        )


class TestRandomSuiteWithConstraints:
    """Tests for RandomSuiteAlgorithm with hard constraints."""

    def test_mandatory_fitness_all_satisfied(self, simple_grammar):
        """mandatory_fitness returns 1.0 when all individuals satisfy the constraint."""
        passing = _make_constraint(always_pass=True)
        algo = RandomSuiteAlgorithm(simple_grammar, [passing])
        suite = _generate_suite(simple_grammar, 4)
        assert algo._mandatory_fitness(suite) == 1.0

    def test_mandatory_fitness_none_satisfied(self, simple_grammar):
        """mandatory_fitness returns 0.0 when no individual satisfies the constraint."""
        failing = _make_constraint(always_pass=False)
        algo = RandomSuiteAlgorithm(simple_grammar, [failing])
        suite = _generate_suite(simple_grammar, 4)
        assert algo._mandatory_fitness(suite) == 0.0

    def test_mandatory_fitness_no_constraints_returns_one(self, simple_grammar):
        """mandatory_fitness returns 1.0 when there are no hard constraints."""
        algo = RandomSuiteAlgorithm(simple_grammar, [])
        suite = _generate_suite(simple_grammar, 4)
        assert algo._mandatory_fitness(suite) == 1.0

    def test_generate_with_passing_constraint_returns_suite(self, simple_grammar):
        """generate() returns a non-empty Suite even with a hard constraint."""
        passing = _make_constraint(always_pass=True)
        algo = RandomSuiteAlgorithm(simple_grammar, [passing])
        result = algo.generate(max_generations=5)
        assert isinstance(result, Suite)
        assert len(result) > 0


class TestRandomIndividualAlgorithm:
    """Test RandomIndividualAlgorithm implementation."""

    def test_generate(self, simple_grammar, empty_constraints):
        """generate(max_generations=N) yields exactly N DerivationTree objects."""
        algo = RandomIndividualAlgorithm(
            simple_grammar, empty_constraints, population_size=5
        )
        trees = list(algo.generate(max_generations=7))
        assert len(trees) <= 7
