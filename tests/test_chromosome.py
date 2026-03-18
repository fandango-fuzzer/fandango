"""Unit tests for Chromosome abstractions (Individual and Suite)."""

import pytest
from fandango import DerivationTree
from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.crossover import SuiteCrossover
from fandango.language.parse.parse import parse
from tests.utils import RESOURCES_ROOT


@pytest.fixture
def simple_grammar():
    grammar_file = RESOURCES_ROOT / "simple_digits.fan"
    with open(grammar_file, "r") as f:
        grammar, _ = parse([f])
    return grammar


@pytest.fixture
def sample_tree(simple_grammar):
    return simple_grammar.fuzz("<start>", max_nodes=10)


@pytest.fixture
def another_tree(simple_grammar):
    return simple_grammar.fuzz("<start>", max_nodes=10)


class TestIndividual:
    def test_creation(self, sample_tree):
        ind = Individual(sample_tree)
        assert ind.tree is sample_tree
        assert isinstance(ind, Chromosome)
        assert isinstance(ind.tree, DerivationTree)

    def test_size(self, sample_tree):
        assert Individual(sample_tree).size() == sample_tree.size()

    def test_clone(self, sample_tree):
        ind = Individual(sample_tree)
        cloned = ind.clone()
        assert isinstance(cloned, Individual)
        assert cloned == ind
        assert cloned is not ind
        assert cloned.tree is not ind.tree
        assert cloned.size() == ind.size()

    def test_equality_same_content(self, sample_tree):
        assert Individual(sample_tree) == Individual(sample_tree)

    def test_equality_different_content(self, sample_tree, another_tree):
        if sample_tree != another_tree:
            assert Individual(sample_tree) != Individual(another_tree)

    @pytest.mark.parametrize("other", ["not an individual", 42, None])
    def test_equality_wrong_type(self, sample_tree, other):
        assert Individual(sample_tree) != other

    def test_hash_consistent(self, sample_tree):
        ind1 = Individual(sample_tree)
        ind2 = Individual(sample_tree)
        assert hash(ind1) == hash(ind1)  # deterministic
        assert hash(ind1) == hash(ind2)  # same content -> same hash
        assert len({ind1, ind2}) == 1  # deduplication in sets

    def test_to_derivation_trees(self, sample_tree):
        trees = Individual(sample_tree).to_derivation_trees()
        assert len(trees) == 1
        assert trees[0] is sample_tree

    def test_suite_add_remove_cycle(self, sample_tree, another_tree, simple_grammar):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        ind3 = Individual(simple_grammar.fuzz("<start>", max_nodes=5))
        suite = Suite([ind1, ind2])
        suite.add_individual(ind3)
        removed = suite.remove_individual(1)
        assert removed is ind2
        suite.add_individual(removed)
        assert suite[-1] is ind2

    def test_nested_clone_idempotence(self, sample_tree):
        ind = Individual(sample_tree)
        clone1 = ind.clone()
        clone2 = clone1.clone()
        assert clone1 == ind and clone2 == ind

    @pytest.mark.parametrize("max_nodes", [1, 100])
    def test_individual_tree_sizes(self, simple_grammar, max_nodes):
        tree = simple_grammar.fuzz("<start>", max_nodes=max_nodes)
        ind = Individual(tree)
        assert ind.size() >= 1
        cloned = ind.clone()
        assert cloned == ind and cloned is not ind


class TestSuite:
    def test_creation(self, sample_tree, another_tree):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        suite = Suite([ind1, ind2])
        assert isinstance(suite, Chromosome)
        assert len(suite) == 2
        assert suite[0] is ind1 and suite[1] is ind2

    def test_creation_empty(self):
        assert len(Suite([])) == 0

    def test_size(self, sample_tree, another_tree):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        assert Suite([]).size() == 0
        assert Suite([ind1]).size() == ind1.size()
        assert Suite([ind1, ind2]).size() == ind1.size() + ind2.size()

    def test_clone(self, sample_tree, another_tree):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        suite = Suite([ind1, ind2])
        cloned = suite.clone()
        assert isinstance(cloned, Suite)
        assert cloned == suite and cloned is not suite
        assert len(cloned) == len(suite)
        for i in range(len(suite)):
            assert cloned[i] == suite[i] and cloned[i] is not suite[i]

    def test_clone_empty(self):
        cloned = Suite([]).clone()
        assert isinstance(cloned, Suite) and len(cloned) == 0

    def test_equality(self, sample_tree, another_tree):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        assert Suite([]) == Suite([])
        assert Suite([ind1, ind2]) == Suite([ind1, ind2])
        assert Suite([ind1, ind2]) != Suite([ind2, ind1])  # order matters
        assert Suite([ind1, ind2]) != Suite([ind1])  # different length

    @pytest.mark.parametrize("other", ["not a suite", 42, None])
    def test_equality_wrong_type(self, sample_tree, other):
        assert Suite([Individual(sample_tree)]) != other

    def test_hash_consistent(self, sample_tree, another_tree):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        s1, s2 = Suite([ind1, ind2]), Suite([ind1, ind2])
        assert hash(s1) == hash(s2)
        assert len({s1, s2}) == 1

    def test_iteration_and_indexing(self, sample_tree, another_tree):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        suite = Suite([ind1, ind2])
        assert list(suite) == [ind1, ind2]
        assert suite[-1] is ind2 and suite[-2] is ind1
        with pytest.raises(IndexError):
            _ = suite[10]

    def test_add_individual(self, sample_tree, another_tree):
        ind1, ind2 = Individual(sample_tree), Individual(another_tree)
        suite = Suite([])
        suite.add_individual(ind1)
        assert len(suite) == 1
        suite.add_individual(ind2)
        assert len(suite) == 2 and suite[1] is ind2

    def test_remove_individual(self, simple_grammar):
        trees = [simple_grammar.fuzz("<start>", max_nodes=5) for _ in range(3)]
        ind1, ind2, ind3 = [Individual(t) for t in trees]
        suite = Suite([ind1, ind2, ind3])

        assert suite.remove_individual(1) is ind2
        assert len(suite) == 2 and suite[0] is ind1 and suite[1] is ind3

        assert suite.remove_individual(-1) is ind3
        assert len(suite) == 1

        with pytest.raises(IndexError):
            suite.remove_individual(10)

    def test_to_derivation_trees(self, simple_grammar):
        trees = [simple_grammar.fuzz("<start>", max_nodes=5) for _ in range(3)]
        suite = Suite([Individual(t) for t in trees])
        assert suite.to_derivation_trees() == trees
        assert Suite([]).to_derivation_trees() == []

    def test_suite_with_many_individuals(self, simple_grammar):
        suite = Suite(
            [
                Individual(simple_grammar.fuzz("<start>", max_nodes=5))
                for _ in range(100)
            ]
        )
        assert len(suite) == 100
        cloned = suite.clone()
        assert cloned == suite and len(cloned) == 100


class TestSuiteCrossover:
    def test_crossover_produces_two_non_empty_suites(self, simple_grammar):
        parent1 = Suite([Individual(simple_grammar.fuzz("<start>", max_nodes=5))])
        parent2 = Suite([Individual(simple_grammar.fuzz("<start>", max_nodes=5))])
        op = SuiteCrossover()
        for _ in range(200):
            result = op.crossover(simple_grammar, parent1, parent2)
            assert result is not None
            child1, child2 = result
            assert isinstance(child1, Suite) and isinstance(child2, Suite)
            assert len(child1) > 0 and len(child2) > 0
            assert len(child1) + len(child2) == len(parent1) + len(parent2)
