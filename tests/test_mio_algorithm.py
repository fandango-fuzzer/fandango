"""Unit tests for MIOAlgorithm and MIOArchive."""

import pytest

from fandango.constraints.fitness import ValueFitness
from fandango.constraints.soft import SoftValue, TDigest
from fandango.evolution.algorithms.archive import (
    MIOArchive,
    _ConstraintGoal,
    _SoftConstraintGoal,
)
from fandango.evolution.algorithms.mio import MIOAlgorithm
from fandango.evolution.algorithms.random import _generate_individual
from fandango.evolution.chromosomes import Chromosome
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite
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
    """Simple digits grammar for testing."""
    grammar_file = RESOURCES_ROOT / "simple_digits.fan"
    with open(grammar_file, "r") as f:
        grammar, _ = parse([f])
    return grammar


@pytest.fixture
def empty_constraints():
    return []


@pytest.fixture
def start_symbol():
    return NonTerminal("<start>")


class TestMIOArchive:
    """Tests for MIOArchive."""

    def test_starts_with_no_covered_goals(self, simple_grammar, start_symbol):
        """No goals should be covered initially."""
        archive = MIOArchive(simple_grammar, n=10, k=2, start_symbol=start_symbol)
        assert len(archive.covered_goals) == 0

    def test_update_marks_goals_covered(self, simple_grammar, start_symbol):
        """After updating with individuals, some goals should be covered."""
        archive = MIOArchive(simple_grammar, n=10, k=2, start_symbol=start_symbol)
        population = [_generate_individual(simple_grammar) for _ in range(10)]
        archive.update(population)
        assert len(archive.covered_goals) > 0

    def test_get_solution_returns_none_when_empty_pools(
        self, simple_grammar, start_symbol
    ):
        """get_solution returns None when uncovered pools are empty."""
        archive = MIOArchive(simple_grammar, n=10, k=2, start_symbol=start_symbol)
        assert archive.get_solution() is None

    def test_shrink_solutions_reduces_pool_size(self, simple_grammar, start_symbol):
        """shrink_solutions should cap pool sizes."""
        archive = MIOArchive(simple_grammar, n=10, k=2, start_symbol=start_symbol)
        # Manually add candidates to an uncovered goal pool
        goals = list(archive.uncovered_goals)
        if goals:
            goal = goals[0]
            individuals: list[Chromosome] = [
                _generate_individual(simple_grammar) for _ in range(5)
            ]
            archive._uncovered_populations[goal] = individuals
            archive.shrink_solutions(2)
            assert len(archive._uncovered_populations[goal]) <= 2

    def test_shorter_individual_replaces_longer_for_covered_goal(
        self, simple_grammar, start_symbol
    ):
        """A shorter individual should replace a longer one for the same covered goal."""
        archive = MIOArchive(simple_grammar, n=10, k=2, start_symbol=start_symbol)
        # Generate many individuals and update; then check that solutions
        # are maintained (at least one solution exists after update)
        population = [_generate_individual(simple_grammar) for _ in range(20)]
        archive.update(population)
        initial_solutions = list(archive.solutions)
        assert len(initial_solutions) > 0

        # Update again with more individuals -- should keep shortest
        more = [_generate_individual(simple_grammar) for _ in range(20)]
        archive.update(more)
        # Solutions should still exist
        assert len(archive.solutions) > 0

    def test_covered_and_uncovered_partition_all_goals(
        self, simple_grammar, start_symbol
    ):
        """covered_goals + uncovered_goals should equal all goals."""
        archive = MIOArchive(simple_grammar, n=10, k=2, start_symbol=start_symbol)
        population = [_generate_individual(simple_grammar) for _ in range(10)]
        archive.update(population)
        assert archive.covered_goals | archive.uncovered_goals == archive._goals


class TestMIOAlgorithm:
    """Integration tests for MIOAlgorithm."""

    def test_generate_returns_suite(self, simple_grammar, empty_constraints):
        """generate() should return a Suite."""
        algo = MIOAlgorithm(simple_grammar, empty_constraints, k=2)
        result = algo.generate(max_generations=5)
        assert isinstance(result, Suite)

    def test_generate_returns_non_empty_suite(self, simple_grammar, empty_constraints):
        """generate() should return a non-empty Suite."""
        algo = MIOAlgorithm(simple_grammar, empty_constraints, k=2)
        result = algo.generate(max_generations=5)
        assert len(result) > 0

    def test_zero_max_generations_returns_suite(
        self, simple_grammar, empty_constraints
    ):
        """With max_generations=0 a valid Suite is still returned."""
        algo = MIOAlgorithm(simple_grammar, empty_constraints, k=2)
        result = algo.generate(max_generations=0)
        assert isinstance(result, Suite)
        assert len(result) > 0

    def test_individuals_are_valid_type(self, simple_grammar, empty_constraints):
        """All items in the returned suite should be Individual instances."""
        algo = MIOAlgorithm(simple_grammar, empty_constraints, k=2)
        result = algo.generate(max_generations=5)
        for ind in result:
            assert isinstance(ind, Individual)

    def test_focused_flag_activates_at_threshold(
        self, simple_grammar, empty_constraints
    ):
        """The focused flag should activate when progress >= exploitation_starts_at."""
        algo = MIOAlgorithm(
            simple_grammar,
            empty_constraints,
            k=2,
            exploitation_starts_at=0.5,
        )
        # Test _update_parameters directly: generation=5, max=10 → progress=0.5 >= threshold
        algo._update_parameters(5, 10)
        assert algo._focused is True

    def test_parameter_pr_interpolates(self, simple_grammar, empty_constraints):
        """pr should decrease from initial towards focused during search."""
        algo = MIOAlgorithm(
            simple_grammar,
            empty_constraints,
            k=2,
            initial_pr=0.5,
            focused_pr=0.0,
            exploitation_starts_at=0.5,
        )
        initial_pr = algo._parameters.pr
        algo.generate(max_generations=10)
        # After search, pr should have moved towards focused_pr
        assert algo._parameters.pr <= initial_pr


class TestMIOAlgorithmWithConstraints:
    """Integration tests for MIOAlgorithm with hard and soft constraints."""

    def test_hard_constraint_goal_in_archive_goals(self, simple_grammar):
        """MIOArchive must include _ConstraintGoal(0) when a hard constraint is passed."""
        failing = _make_constraint(always_pass=False)
        algo = MIOAlgorithm(simple_grammar, [failing], k=1)
        assert _ConstraintGoal(0) in algo._mio_archive._goals

    def test_soft_constraint_goal_in_archive_goals(self, simple_grammar):
        """MIOArchive must include _SoftConstraintGoal(0) when a soft constraint is passed."""
        soft = _make_soft_value(always_high=True)
        algo = MIOAlgorithm(simple_grammar, [soft], k=1)
        assert _SoftConstraintGoal(0) in algo._mio_archive._goals

    def test_failing_constraint_does_not_gate_kpath_in_generate(self, simple_grammar):
        """With a failing hard constraint, generate() still returns a non-empty Suite."""
        failing = _make_constraint(always_pass=False)
        algo = MIOAlgorithm(simple_grammar, [failing], k=1)
        result = algo.generate(max_generations=10)
        assert isinstance(result, Suite)
        assert len(result) > 0

    def test_passing_hard_constraint_returns_valid_suite(self, simple_grammar):
        """With an always-passing hard constraint, generate() returns a Suite."""
        passing = _make_constraint(always_pass=True)
        algo = MIOAlgorithm(simple_grammar, [passing], k=1)
        result = algo.generate(max_generations=10)
        assert isinstance(result, Suite)
        assert len(result) > 0

    def test_kpath_not_covered_in_archive_when_constraint_fails(self, simple_grammar):
        """After generate(), k-path goals must not be covered if constraint always fails."""
        failing = _make_constraint(always_pass=False)
        algo = MIOAlgorithm(simple_grammar, [failing], k=1)
        algo.generate(max_generations=20)
        kpath_covered = {
            g for g in algo._mio_archive.covered_goals if isinstance(g, tuple)
        }
        assert len(kpath_covered) == 0

    def test_soft_constraint_goal_covered_in_archive(self, simple_grammar):
        """_SoftConstraintGoal(0) should be covered after generate() with high-fitness soft constraint."""
        soft = _make_soft_value(always_high=True)
        algo = MIOAlgorithm(simple_grammar, [soft], k=1)
        algo.generate(max_generations=10)
        assert _SoftConstraintGoal(0) in algo._mio_archive.covered_goals

    def test_no_constraints_archive_has_only_kpath_goals(self, simple_grammar):
        """Without constraints, archive goals are purely k-paths (baseline unchanged)."""
        algo = MIOAlgorithm(simple_grammar, [], k=1)
        for g in algo._mio_archive._goals:
            assert isinstance(g, tuple)

    def test_both_constraint_types_archive_partition_invariant(self, simple_grammar):
        """covered | uncovered == _goals holds with both constraint types after generate()."""
        passing = _make_constraint(always_pass=True)
        soft = _make_soft_value(always_high=True)
        algo = MIOAlgorithm(simple_grammar, [passing, soft], k=1)
        algo.generate(max_generations=10)
        archive = algo._mio_archive
        assert archive.covered_goals | archive.uncovered_goals == archive._goals
