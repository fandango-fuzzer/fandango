"""Unit tests for Archive and CoverageArchive."""

import pytest

from fandango.evolution.algorithms.archive import Archive, CoverageArchive
from fandango.evolution.chromosomes.individual import Individual
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from tests.utils import RESOURCES_ROOT


@pytest.fixture
def simple_grammar():
    """Load simple_digits grammar: <start> ::= <digit>+, <digit> ::= 0|1|2|3|4."""
    grammar_file = RESOURCES_ROOT / "simple_digits.fan"
    with open(grammar_file, "r") as f:
        grammar, _ = parse([f])
    return grammar


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
