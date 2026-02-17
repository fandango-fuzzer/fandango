"""Unit tests for Random Algorithm implementations."""

import pytest

from fandango.evolution.algorithms.random import (
    RandomIndividualAlgorithm,
)
from fandango.evolution.chromosomes.individual import Individual
from fandango.language.parse.parse import parse
from fandango.language.tree import DerivationTree
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


class TestRandomIndividualAlgorithm:
    """Test RandomIndividualAlgorithm implementation."""

    def test_generate(self, simple_grammar, empty_constraints):
        """generate(max_generations=N) yields exactly N DerivationTree objects."""
        algo = RandomIndividualAlgorithm(
            simple_grammar, empty_constraints, population_size=5
        )
        trees = list(algo.generate(max_generations=7))
        assert len(trees) == 7
