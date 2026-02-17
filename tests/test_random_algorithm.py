"""Unit tests for Random Algorithm implementations."""

from fandango.evolution.algorithms.random import (
    RandomIndividualAlgorithm,
)
from fandango.evolution.chromosomes.individual import Individual
from fandango.language.tree import DerivationTree


class TestRandomIndividualAlgorithm:
    """Test RandomIndividualAlgorithm implementation."""

    def test_generate_initial_population(self, simple_grammar, empty_constraints):
        """generate_initial_population yields exactly population_size DerivationTree objects."""
        algo = RandomIndividualAlgorithm(
            simple_grammar, empty_constraints, population_size=5
        )
        trees = list(algo.generate_initial_population())
        assert len(trees) == 5
        assert all(isinstance(t, DerivationTree) for t in trees)
        assert len(algo.population) == 5

    def test_generate(self, simple_grammar, empty_constraints):
        """generate(max_generations=N) yields exactly N DerivationTree objects."""
        algo = RandomIndividualAlgorithm(
            simple_grammar, empty_constraints, population_size=5
        )
        trees = list(algo.generate(max_generations=7))
        assert len(trees) == 7
        assert all(isinstance(t, DerivationTree) for t in trees)

    def test_population(self, simple_grammar, empty_constraints):
        """After generating, population returns a Sequence of Individual objects."""
        algo = RandomIndividualAlgorithm(
            simple_grammar, empty_constraints, population_size=3
        )
        list(algo.generate_initial_population())
        pop = algo.population
        assert len(pop) == 3
        assert all(isinstance(ind, Individual) for ind in pop)
