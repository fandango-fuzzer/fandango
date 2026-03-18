"""Unit tests for Archive and CoverageArchive."""

import pytest

from fandango.constraints.fitness import ValueFitness
from fandango.constraints.soft import SoftValue, TDigest
from fandango.evolution.algorithms.archive import (
    Archive,
    CoverageArchive,
    MIOArchive,
    _ConstraintGoal,
    _SoftConstraintGoal,
)
from fandango.evolution.algorithms.random import _generate_individual
from fandango.evolution.chromosomes.individual import Individual
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from tests.test_random_algorithm import _make_constraint
from tests.utils import RESOURCES_ROOT


def _make_soft_value(always_high: bool) -> SoftValue:
    """Create a stub SoftValue that always returns a fixed fitness (1.0 or 0.0)."""

    class _StubSoftValue(SoftValue):
        def __init__(self) -> None:
            self.optimization_goal = "max"
            self.tdigest = TDigest("max")
            self._always_high = always_high

        def fitness(self, tree, scope=None, local_variables=None) -> ValueFitness:
            return ValueFitness(values=[1.0 if self._always_high else 0.0])

    return _StubSoftValue()


@pytest.fixture
def simple_grammar():
    """Load simple_digits grammar: <start> ::= <digit>+, <digit> ::= 0|1|2|3|4."""
    grammar_file = RESOURCES_ROOT / "simple_digits.fan"
    with open(grammar_file, "r") as f:
        grammar, _ = parse([f])
    return grammar


@pytest.fixture
def start_symbol():
    return NonTerminal("<start>")


@pytest.fixture
def all_goals_k2(simple_grammar):
    """All k=2 paths for the simple grammar."""
    return frozenset(
        simple_grammar.generate_all_k_paths(k=2, non_terminal=NonTerminal("<start>"))
    )


def make_individual(grammar, text: str) -> Individual:
    """Parse a string and wrap it in an Individual."""
    tree = grammar.parse(text)
    assert tree is not None, f"Could not parse '{text}'"
    return Individual(tree)


class TestCoverageArchiveInit:
    def test_all_goals_match_grammar(self, simple_grammar, all_goals_k2):
        archive = CoverageArchive(simple_grammar, k=2)
        assert archive._goals == all_goals_k2

    def test_starts_empty(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        assert archive.covered_goals == frozenset()
        assert archive.solutions == []
        assert archive.uncovered_goals == archive._goals

    def test_unknown_start_symbol(self, simple_grammar):
        """If start_symbol not in grammar, all_goals is empty."""
        archive = CoverageArchive(
            simple_grammar, k=2, start_symbol=NonTerminal("<nonexistent>")
        )
        assert archive._goals == frozenset()

    def test_isinstance_archive(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        assert isinstance(archive, Archive)


class TestCoverageArchiveUpdate:
    def test_empty_update_returns_false(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        changed = archive.update([])
        assert changed is False
        assert archive.solutions == []

    def test_single_individual_covers_goals(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        ind = make_individual(simple_grammar, "0")
        changed = archive.update([ind])
        assert changed is True
        assert len(archive.covered_goals) > 0

    def test_covered_goals_subset_of_all_goals(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        ind = make_individual(simple_grammar, "1")
        archive.update([ind])
        assert archive.covered_goals <= archive._goals

    def test_uncovered_goals_complement(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        ind = make_individual(simple_grammar, "2")
        archive.update([ind])
        assert archive.covered_goals | archive.uncovered_goals == archive._goals
        assert archive.covered_goals & archive.uncovered_goals == frozenset()

    def test_shorter_replaces_longer(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        # Parse a longer string first so it covers some goals
        long_ind = make_individual(simple_grammar, "0000")
        archive.update([long_ind])
        covered_before = set(archive.covered_goals)

        # Now try a shorter one that covers a subset
        short_ind = make_individual(simple_grammar, "0")
        changed = archive.update([short_ind])
        # At least one goal should be replaced (short_ind.size() < long_ind.size())
        # changed should be True if any replacement happened
        assert isinstance(changed, bool)
        # For every goal covered by short_ind, the archive should now hold the shorter one
        short_paths = simple_grammar._extract_k_paths_from_tree(short_ind.tree, k=2)
        for path in short_paths & archive._goals:
            assert archive._covered[path].size() <= short_ind.size()

    def test_same_size_does_not_change(self, simple_grammar):
        """Updating with equal-size individual covering only already-covered goals → False."""
        archive = CoverageArchive(simple_grammar, k=2)
        ind1 = make_individual(simple_grammar, "0")
        archive.update([ind1])

        # ind2 covers identical paths; same size since same string
        ind2 = make_individual(simple_grammar, "0")
        # size is equal — not smaller, so no replacement for existing goals
        # and no new goals → should return False
        changed = archive.update([ind2])
        assert changed is False

    def test_new_goal_always_true(self, simple_grammar):
        """Updating with an individual that covers a previously uncovered goal → True."""
        archive = CoverageArchive(simple_grammar, k=2)
        # First update with "0"
        ind1 = make_individual(simple_grammar, "0")
        archive.update([ind1])
        prev_covered = archive.covered_goals

        # If there are still uncovered goals, try to cover them
        if archive.uncovered_goals:
            ind2 = make_individual(simple_grammar, "01234")
            changed = archive.update([ind2])
            if archive.covered_goals > prev_covered:
                assert changed is True


class TestCoverageArchiveSolutions:
    def test_solutions_deduplication(self, simple_grammar):
        """One Individual covering multiple goals appears once in solutions."""
        archive = CoverageArchive(simple_grammar, k=2)
        ind = make_individual(simple_grammar, "01234")
        archive.update([ind])
        # Even if ind covers many goals, it should appear only once in solutions
        solutions = archive.solutions
        assert solutions.count(ind) <= 1

    def test_solutions_empty_when_no_update(self, simple_grammar):
        archive = CoverageArchive(simple_grammar, k=2)
        assert archive.solutions == []


class TestCoverageArchiveInvariants:
    def test_union_invariant(self, simple_grammar):
        """covered_goals | uncovered_goals == all_goals always holds."""
        archive = CoverageArchive(simple_grammar, k=2)
        assert archive.covered_goals | archive.uncovered_goals == archive._goals

        ind = make_individual(simple_grammar, "01234")
        archive.update([ind])
        assert archive.covered_goals | archive.uncovered_goals == archive._goals

    def test_full_coverage(self, simple_grammar, all_goals_k2):
        """After enough individuals, uncovered_goals can reach empty."""
        archive = CoverageArchive(simple_grammar, k=2)
        # Generate many individuals to try to cover everything
        for _ in range(50):
            tree = simple_grammar.fuzz("<start>")
            archive.update([Individual(tree)])
        # If we've hit full coverage, uncovered should be empty
        if archive.covered_goals == all_goals_k2:
            assert archive.uncovered_goals == frozenset()


class TestMIOArchiveWithConstraints:
    """Tests for MIOArchive constraint goal handling."""

    def test_hard_constraint_goal_added_to_goals(self, simple_grammar, start_symbol):
        """_ConstraintGoal(0) should appear in _goals when a hard constraint is given."""
        failing = _make_constraint(always_pass=False)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            hard_constraints=[failing],
        )
        assert _ConstraintGoal(0) in archive._goals

    def test_soft_constraint_goal_added_to_goals(self, simple_grammar, start_symbol):
        """_SoftConstraintGoal(0) should appear in _goals when a soft constraint is given."""
        soft = _make_soft_value(always_high=True)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            soft_constraints=[soft],
        )
        assert _SoftConstraintGoal(0) in archive._goals

    def test_hard_constraint_goal_initially_uncovered(
        self, simple_grammar, start_symbol
    ):
        """Hard constraint goal must start in uncovered_goals."""
        failing = _make_constraint(always_pass=False)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            hard_constraints=[failing],
        )
        assert _ConstraintGoal(0) in archive.uncovered_goals

    def test_passing_hard_constraint_becomes_covered(
        self, simple_grammar, start_symbol
    ):
        """_ConstraintGoal(0) moves to covered_goals when satisfied by an individual."""
        passing = _make_constraint(always_pass=True)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            hard_constraints=[passing],
        )
        population = [_generate_individual(simple_grammar) for _ in range(5)]
        archive.update(population)
        assert _ConstraintGoal(0) in archive.covered_goals

    def test_failing_hard_constraint_does_not_gate_kpath_coverage(
        self, simple_grammar, start_symbol
    ):
        """K-path goals ARE covered even when the hard constraint always fails.

        K-path coverage is now independent of hard-constraint satisfaction.
        Filtering happens at output time via valid_solutions, not during archiving.
        """
        failing = _make_constraint(always_pass=False)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            hard_constraints=[failing],
        )
        population = [_generate_individual(simple_grammar) for _ in range(20)]
        archive.update(population)
        kpath_covered = {g for g in archive.covered_goals if isinstance(g, tuple)}
        assert len(kpath_covered) > 0

    def test_passing_hard_constraint_allows_kpath_coverage(
        self, simple_grammar, start_symbol
    ):
        """K-path goals ARE covered when the hard constraint always passes."""
        passing = _make_constraint(always_pass=True)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            hard_constraints=[passing],
        )
        population = [_generate_individual(simple_grammar) for _ in range(10)]
        archive.update(population)
        kpath_covered = {g for g in archive.covered_goals if isinstance(g, tuple)}
        assert len(kpath_covered) > 0

    def test_soft_constraint_goal_covered_with_high_fitness(
        self, simple_grammar, start_symbol
    ):
        """_SoftConstraintGoal(0) is covered when fitness is always high."""
        soft = _make_soft_value(always_high=True)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            soft_constraints=[soft],
        )
        population = [_generate_individual(simple_grammar) for _ in range(5)]
        archive.update(population)
        assert _SoftConstraintGoal(0) in archive.covered_goals

    def test_no_constraints_only_kpath_goals_covered(
        self, simple_grammar, start_symbol
    ):
        """Without constraints, all covered goals must be k-paths (baseline unchanged)."""
        archive = MIOArchive(simple_grammar, n=10, k=2, start_symbol=start_symbol)
        population = [_generate_individual(simple_grammar) for _ in range(10)]
        archive.update(population)
        for g in archive.covered_goals:
            assert isinstance(g, tuple)

    def test_covered_and_uncovered_partition_goals_with_both_constraints(
        self, simple_grammar, start_symbol
    ):
        """covered | uncovered == _goals holds when both constraint types are present."""
        passing = _make_constraint(always_pass=True)
        soft = _make_soft_value(always_high=True)
        archive = MIOArchive(
            simple_grammar,
            n=10,
            k=2,
            start_symbol=start_symbol,
            hard_constraints=[passing],
            soft_constraints=[soft],
        )
        population = [_generate_individual(simple_grammar) for _ in range(10)]
        archive.update(population)
        assert archive.covered_goals | archive.uncovered_goals == archive._goals
