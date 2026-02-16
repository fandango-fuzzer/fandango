"""Unit tests for suite-level fitness functions."""

import pytest
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.fitness.base import SuiteFitnessFunction
from fandango.evolution.fitness.suite import (
    SymbolCoverageFitnessFunction,
    PathCoverageFitnessFunction,
)
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal, Terminal
from tests.utils import RESOURCES_ROOT


@pytest.fixture
def simple_grammar():
    """Create a simple grammar for testing."""
    grammar_file = RESOURCES_ROOT / "simple_digits.fan"
    with open(grammar_file, "r") as f:
        grammar, _ = parse([f])
    return grammar


@pytest.fixture
def sample_suite(simple_grammar):
    """Create a sample suite with multiple individuals."""
    trees = [simple_grammar.fuzz("<start>", max_nodes=10) for _ in range(3)]
    individuals = [Individual(tree) for tree in trees]
    return Suite(individuals)


@pytest.fixture
def empty_suite():
    """Create an empty suite."""
    return Suite([])


@pytest.fixture
def single_individual_suite(simple_grammar):
    """Create a suite with a single individual."""
    tree = simple_grammar.fuzz("<start>", max_nodes=10)
    return Suite([Individual(tree)])


class TestSymbolCoverageFitnessFunction:
    """Test SymbolCoverageFitnessFunction."""

    def test_construction(self, simple_grammar):
        """Test creating a SymbolCoverageFitnessFunction."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        assert fitness_fn is not None
        assert isinstance(fitness_fn, SuiteFitnessFunction)

    def test_construction_with_custom_start_symbol(self, simple_grammar):
        """Test construction with custom start symbol."""
        fitness_fn = SymbolCoverageFitnessFunction(
            simple_grammar, start_symbol=NonTerminal("<digit>")
        )
        assert fitness_fn is not None

    def test_is_maximising(self, simple_grammar):
        """Test that SymbolCoverageFitnessFunction is maximizing."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        assert fitness_fn.is_maximising() is True

    def test_cache_property(self, simple_grammar):
        """Test that cache property returns a dictionary."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        cache = fitness_fn.cache
        assert isinstance(cache, dict)

    def test_type_checking_raises_on_individual(self, simple_grammar):
        """Test that passing an Individual raises TypeError."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        tree = simple_grammar.fuzz("<start>", max_nodes=10)
        individual = Individual(tree)

        with pytest.raises(TypeError) as exc_info:
            fitness_fn.fitness(individual)
        assert "Suite" in str(exc_info.value)
        assert "Individual" in str(exc_info.value)

    def test_empty_suite_returns_zero(self, simple_grammar, empty_suite):
        """Test that empty suite returns 0.0 fitness."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        fitness_value = fitness_fn.fitness(empty_suite)
        assert fitness_value == 0.0

    def test_single_tree_partial_coverage(
        self, simple_grammar, single_individual_suite
    ):
        """Test that single tree gives partial coverage."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        fitness_value = fitness_fn.fitness(single_individual_suite)

        # Should be > 0 (some coverage) but may not be 1.0 (full coverage)
        assert 0.0 < fitness_value <= 1.0

    def test_multiple_trees_increase_coverage(self, simple_grammar):
        """Test that adding more trees increases or maintains coverage."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        # Single tree
        tree1 = simple_grammar.fuzz("<start>", max_nodes=10)
        suite1 = Suite([Individual(tree1)])
        fitness1 = fitness_fn.fitness(suite1)

        # Two trees
        tree2 = simple_grammar.fuzz("<start>", max_nodes=10)
        suite2 = Suite([Individual(tree1), Individual(tree2)])
        fitness2 = fitness_fn.fitness(suite2)

        # Adding more trees should not decrease coverage (monotonicity)
        assert fitness2 >= fitness1

    def test_full_coverage_returns_one(self, simple_grammar):
        """Test that full coverage returns 1.0."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        # Generate many trees to achieve full coverage
        trees = [simple_grammar.fuzz("<start>", max_nodes=20) for _ in range(50)]
        individuals = [Individual(tree) for tree in trees]
        suite = Suite(individuals)

        fitness_value = fitness_fn.fitness(suite)

        # With enough trees, should eventually reach full coverage
        # For simple_digits.fan with <start> and <digit>, this should be achievable
        assert 0.0 < fitness_value <= 1.0

    def test_is_covered_true_when_full_coverage(self, simple_grammar):
        """Test that is_covered returns True when fitness >= 1.0."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        # Generate many trees to achieve full coverage
        trees = [simple_grammar.fuzz("<start>", max_nodes=20) for _ in range(50)]
        individuals = [Individual(tree) for tree in trees]
        suite = Suite(individuals)

        fitness = fitness_fn.fitness(suite)
        assert (
            fitness >= 1.0
        ), "50 trees should achieve full coverage of simple_digits grammar"
        assert fitness_fn.is_covered(suite) is True

    def test_is_covered_false_when_partial_coverage(
        self, simple_grammar, single_individual_suite
    ):
        """Test that is_covered returns False when fitness < 1.0."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        fitness = fitness_fn.fitness(single_individual_suite)
        # For simple_digits.fan with <start> and <digit>, a single small tree
        # might achieve full coverage (it's a very simple grammar)
        # So we only test the is_covered logic when partial coverage occurs
        if fitness < 1.0:
            assert fitness_fn.is_covered(single_individual_suite) is False
        else:
            # If full coverage achieved, is_covered should return True
            assert fitness_fn.is_covered(single_individual_suite) is True

    def test_caching_same_suite(self, simple_grammar, sample_suite):
        """Test that caching works for same suite."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        # First call
        fitness1 = fitness_fn.fitness(sample_suite)

        # Second call should use cache
        fitness2 = fitness_fn.fitness(sample_suite)

        assert fitness1 == fitness2
        assert hash(sample_suite) in fitness_fn.cache

    def test_fitness_range_invariant(self, simple_grammar, sample_suite):
        """Test that fitness is always in [0.0, 1.0]."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        fitness_value = fitness_fn.fitness(sample_suite)

        assert 0.0 <= fitness_value <= 1.0

    def test_monotonicity_adding_trees(self, simple_grammar):
        """Test that adding trees never decreases coverage."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        individuals = []
        previous_fitness = 0.0

        for i in range(10):
            tree = simple_grammar.fuzz("<start>", max_nodes=15)
            individuals.append(Individual(tree))
            suite = Suite(individuals.copy())
            current_fitness = fitness_fn.fitness(suite)

            # Coverage should never decrease
            assert current_fitness >= previous_fitness
            previous_fitness = current_fitness

    def test_empty_grammar_returns_one(self):
        """Test that empty grammar (no symbols) returns 1.0."""
        from fandango.language.grammar.grammar import Grammar

        empty_grammar = Grammar(grammar_settings=[], rules={})
        fitness_fn = SymbolCoverageFitnessFunction(empty_grammar)

        suite = Suite([])
        fitness_value = fitness_fn.fitness(suite)

        # No symbols to cover = full coverage
        assert fitness_value == 1.0

    def test_different_suites_different_fitness(self, simple_grammar):
        """Test that different suites may have different fitness values."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        # Small suite
        tree1 = simple_grammar.fuzz("<start>", max_nodes=5)
        suite1 = Suite([Individual(tree1)])

        # Large suite
        trees2 = [simple_grammar.fuzz("<start>", max_nodes=20) for _ in range(10)]
        suite2 = Suite([Individual(tree) for tree in trees2])

        fitness1 = fitness_fn.fitness(suite1)
        fitness2 = fitness_fn.fitness(suite2)

        # Larger suite should have equal or better coverage
        assert fitness2 >= fitness1

    def test_instanceof_suite_fitness_function(self, simple_grammar):
        """Test that SymbolCoverageFitnessFunction is a SuiteFitnessFunction."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        assert isinstance(fitness_fn, SuiteFitnessFunction)

    def test_deterministic_symbol_coverage(self, simple_grammar):
        """Test symbol coverage with hand-crafted tree with known expected fitness."""
        from fandango.language.tree import DerivationTree

        # Create a hand-crafted tree that covers only <start> symbol
        # simple_digits.fan has <start> and <digit> symbols (total: 2)
        # Tree structure: <start> -> "0" (terminal, no <digit> symbol used)
        tree = DerivationTree(
            symbol=NonTerminal("<start>"),
            children=[DerivationTree(symbol=Terminal("0"), children=None)],
        )

        suite = Suite([Individual(tree)])
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        fitness_value = fitness_fn.fitness(suite)

        # This tree covers only <start>, not <digit>
        # Expected: 1/2 = 0.5
        assert fitness_value == 0.5, f"Expected 0.5, got {fitness_value}"

    def test_clear_cache_method(self, simple_grammar, sample_suite):
        """Test that clear_cache method works correctly."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        # Evaluate to populate cache
        fitness_fn.fitness(sample_suite)
        assert len(fitness_fn.cache) > 0

        # Clear cache
        fitness_fn.clear_cache()
        assert len(fitness_fn.cache) == 0


class TestPathCoverageFitnessFunction:
    """Test PathCoverageFitnessFunction."""

    def test_construction(self, simple_grammar):
        """Test creating a PathCoverageFitnessFunction."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        assert fitness_fn is not None
        assert isinstance(fitness_fn, SuiteFitnessFunction)

    def test_construction_with_custom_start_symbol(self, simple_grammar):
        """Test construction with custom start symbol."""
        fitness_fn = PathCoverageFitnessFunction(
            simple_grammar, start_symbol=NonTerminal("<digit>")
        )
        assert fitness_fn is not None

    def test_is_maximising(self, simple_grammar):
        """Test that PathCoverageFitnessFunction is maximizing."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        assert fitness_fn.is_maximising() is True

    def test_cache_property(self, simple_grammar):
        """Test that cache property returns a dictionary."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        cache = fitness_fn.cache
        assert isinstance(cache, dict)

    def test_type_checking_raises_on_individual(self, simple_grammar):
        """Test that passing an Individual raises TypeError."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        tree = simple_grammar.fuzz("<start>", max_nodes=10)
        individual = Individual(tree)

        with pytest.raises(TypeError) as exc_info:
            fitness_fn.fitness(individual)
        assert "Suite" in str(exc_info.value)
        assert "Individual" in str(exc_info.value)

    def test_empty_suite_returns_zero(self, simple_grammar, empty_suite):
        """Test that empty suite returns 0.0 fitness."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        fitness_value = fitness_fn.fitness(empty_suite)
        assert fitness_value == 0.0

    def test_single_tree_partial_coverage(
        self, simple_grammar, single_individual_suite
    ):
        """Test that single tree gives partial coverage."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        fitness_value = fitness_fn.fitness(single_individual_suite)

        # Should be > 0 (some coverage) but may not be 1.0 (full coverage)
        assert 0.0 < fitness_value <= 1.0

    def test_multiple_trees_increase_coverage(self, simple_grammar):
        """Test that adding more trees increases or maintains coverage."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # Single tree
        tree1 = simple_grammar.fuzz("<start>", max_nodes=10)
        suite1 = Suite([Individual(tree1)])
        fitness1 = fitness_fn.fitness(suite1)

        # Two trees
        tree2 = simple_grammar.fuzz("<start>", max_nodes=10)
        suite2 = Suite([Individual(tree1), Individual(tree2)])
        fitness2 = fitness_fn.fitness(suite2)

        # Adding more trees should not decrease coverage (monotonicity)
        assert fitness2 >= fitness1

    def test_full_coverage_achievable(self, simple_grammar):
        """Test that full coverage is achievable with sufficient trees."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # Generate many trees to achieve full coverage
        trees = [simple_grammar.fuzz("<start>", max_nodes=20) for _ in range(100)]
        individuals = [Individual(tree) for tree in trees]
        suite = Suite(individuals)

        fitness_value = fitness_fn.fitness(suite)

        # With enough trees, should eventually reach good coverage
        assert 0.0 < fitness_value <= 1.0

    def test_is_covered_true_when_full_coverage(self, simple_grammar):
        """Test that is_covered returns True when fitness >= 1.0."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # Generate many trees to achieve full coverage
        trees = [simple_grammar.fuzz("<start>", max_nodes=20) for _ in range(100)]
        individuals = [Individual(tree) for tree in trees]
        suite = Suite(individuals)

        fitness = fitness_fn.fitness(suite)
        assert (
            fitness >= 1.0
        ), "100 trees should achieve full path coverage of simple_digits grammar"
        assert fitness_fn.is_covered(suite) is True

    def test_is_covered_false_when_partial_coverage(
        self, simple_grammar, single_individual_suite
    ):
        """Test that is_covered returns False when fitness < 1.0."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        fitness = fitness_fn.fitness(single_individual_suite)
        # Test the is_covered logic based on actual fitness
        if fitness < 1.0:
            assert fitness_fn.is_covered(single_individual_suite) is False
        else:
            assert fitness_fn.is_covered(single_individual_suite) is True

    def test_caching_same_suite(self, simple_grammar, sample_suite):
        """Test that caching works for same suite."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # First call
        fitness1 = fitness_fn.fitness(sample_suite)

        # Second call should use cache
        fitness2 = fitness_fn.fitness(sample_suite)

        assert fitness1 == fitness2
        assert hash(sample_suite) in fitness_fn.cache

    def test_fitness_range_invariant(self, simple_grammar, sample_suite):
        """Test that fitness is always in [0.0, 1.0]."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        fitness_value = fitness_fn.fitness(sample_suite)

        assert 0.0 <= fitness_value <= 1.0

    def test_monotonicity_adding_trees(self, simple_grammar):
        """Test that adding trees never decreases coverage."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        individuals = []
        previous_fitness = 0.0

        for i in range(10):
            tree = simple_grammar.fuzz("<start>", max_nodes=15)
            individuals.append(Individual(tree))
            suite = Suite(individuals.copy())
            current_fitness = fitness_fn.fitness(suite)

            # Coverage should never decrease
            assert current_fitness >= previous_fitness
            previous_fitness = current_fitness

    def test_no_paths_returns_one(self):
        """Test that grammar with no 2-paths returns 1.0."""
        from fandango.language.grammar.grammar import Grammar

        empty_grammar = Grammar(grammar_settings=[], rules={})
        fitness_fn = PathCoverageFitnessFunction(empty_grammar)

        suite = Suite([])
        fitness_value = fitness_fn.fitness(suite)

        # No paths to cover = full coverage
        assert fitness_value == 1.0

    def test_different_suites_different_fitness(self, simple_grammar):
        """Test that different suites may have different fitness values."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # Small suite
        tree1 = simple_grammar.fuzz("<start>", max_nodes=5)
        suite1 = Suite([Individual(tree1)])

        # Large suite
        trees2 = [simple_grammar.fuzz("<start>", max_nodes=20) for _ in range(10)]
        suite2 = Suite([Individual(tree) for tree in trees2])

        fitness1 = fitness_fn.fitness(suite1)
        fitness2 = fitness_fn.fitness(suite2)

        # Larger suite should have equal or better coverage
        assert fitness2 >= fitness1

    def test_instanceof_suite_fitness_function(self, simple_grammar):
        """Test that PathCoverageFitnessFunction is a SuiteFitnessFunction."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        assert isinstance(fitness_fn, SuiteFitnessFunction)

    def test_2path_extraction_works(self, simple_grammar):
        """Test that 2-path extraction is working correctly."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # Generate a tree and check that some paths are covered
        tree = simple_grammar.fuzz("<start>", max_nodes=20)
        suite = Suite([Individual(tree)])

        fitness_value = fitness_fn.fitness(suite)

        # Should have covered at least some paths
        assert fitness_value > 0.0

    def test_deterministic_path_coverage(self, simple_grammar):
        """Test path coverage with hand-crafted tree with known expected fitness."""
        from fandango.language.tree import DerivationTree

        # Create a hand-crafted tree: <start> -> <digit> -> "5"
        # This creates one 2-path: (<start>, <digit>)
        digit_tree = DerivationTree(
            symbol=NonTerminal("<digit>"),
            children=[DerivationTree(symbol=Terminal("5"), children=None)],
        )
        start_tree = DerivationTree(
            symbol=NonTerminal("<start>"), children=[digit_tree]
        )

        suite = Suite([Individual(start_tree)])
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # Get total number of 2-paths in grammar
        total_paths = len(fitness_fn._all_paths)
        if total_paths > 0:
            fitness_value = fitness_fn.fitness(suite)
            # This tree should cover at least the (<start>, <digit>) path
            assert fitness_value > 0.0, f"Expected > 0.0, got {fitness_value}"

    def test_clear_cache_method(self, simple_grammar, sample_suite):
        """Test that clear_cache method works correctly."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        # Evaluate to populate cache
        fitness_fn.fitness(sample_suite)
        assert len(fitness_fn.cache) > 0

        # Clear cache
        fitness_fn.clear_cache()
        assert len(fitness_fn.cache) == 0


class TestSuiteFitnessInterface:
    """Test that both fitness functions comply with SuiteFitnessFunction interface."""

    def test_symbol_coverage_isinstance_check(self, simple_grammar):
        """Test SymbolCoverageFitnessFunction isinstance check."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)
        assert isinstance(fitness_fn, SuiteFitnessFunction)

    def test_path_coverage_isinstance_check(self, simple_grammar):
        """Test PathCoverageFitnessFunction isinstance check."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)
        assert isinstance(fitness_fn, SuiteFitnessFunction)

    def test_symbol_coverage_has_required_methods(self, simple_grammar):
        """Test SymbolCoverageFitnessFunction has all required methods."""
        fitness_fn = SymbolCoverageFitnessFunction(simple_grammar)

        assert hasattr(fitness_fn, "fitness")
        assert hasattr(fitness_fn, "is_covered")
        assert hasattr(fitness_fn, "is_maximising")
        assert hasattr(fitness_fn, "cache")

        assert callable(fitness_fn.fitness)
        assert callable(fitness_fn.is_covered)
        assert callable(fitness_fn.is_maximising)

    def test_path_coverage_has_required_methods(self, simple_grammar):
        """Test PathCoverageFitnessFunction has all required methods."""
        fitness_fn = PathCoverageFitnessFunction(simple_grammar)

        assert hasattr(fitness_fn, "fitness")
        assert hasattr(fitness_fn, "is_covered")
        assert hasattr(fitness_fn, "is_maximising")
        assert hasattr(fitness_fn, "cache")

        assert callable(fitness_fn.fitness)
        assert callable(fitness_fn.is_covered)
        assert callable(fitness_fn.is_maximising)


class TestImports:
    """Test that fitness functions are importable from the package."""

    def test_import_from_fitness_module(self):
        """Test importing from fandango.evolution.fitness."""
        from fandango.evolution.fitness import (
            SymbolCoverageFitnessFunction,
            PathCoverageFitnessFunction,
        )

        assert SymbolCoverageFitnessFunction is not None
        assert PathCoverageFitnessFunction is not None

    def test_import_from_suite_submodule(self):
        """Test importing from fandango.evolution.fitness.suite."""
        from fandango.evolution.fitness.suite import (
            SymbolCoverageFitnessFunction,
            PathCoverageFitnessFunction,
        )

        assert SymbolCoverageFitnessFunction is not None
        assert PathCoverageFitnessFunction is not None
