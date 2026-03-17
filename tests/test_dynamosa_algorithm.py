"""Unit tests for DynaMOSAAlgorithm."""

import pytest

from fandango.evolution.algorithms.dynamosa import (
    _ConstraintGoal,
    _SoftConstraintGoal,
    DynaMOSAAlgorithm,
    _KPathGoalGraph,
    _DynaMOSAGoalManager,
    _compute_pareto_fronts,
)
from fandango.evolution.algorithms.random import _generate_individual
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.fitness.suite import KPathCoverageFitnessFunction
from fandango.language.grammar.grammar import KPath
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from tests.test_random_algorithm import _make_constraint
from tests.utils import RESOURCES_ROOT


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


class TestKPathGoalGraph:
    """Tests for _KPathGoalGraph."""

    def test_root_goals_are_1_paths(self, simple_grammar, start_symbol):
        """Root goals should be exactly the 1-paths (length 1 tuples)."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        for goal in graph.root_goals:
            assert len(goal) == 1, f"Root goal {goal} has length != 1"

    def test_root_goals_non_empty(self, simple_grammar, start_symbol):
        """The grammar should produce at least one 1-path root goal."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        assert len(graph.root_goals) > 0

    def test_all_goals_contains_root_goals(self, simple_grammar, start_symbol):
        """All goals includes all root goals."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        assert graph.root_goals.issubset(graph.all_goals)

    def test_children_are_prefix_extensions(self, simple_grammar, start_symbol):
        """Each child of a goal should have that goal as its prefix."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        for goal in graph.root_goals:
            for child in graph.get_children(goal):
                assert (
                    len(child) == len(goal) + 1
                ), f"Child {child} should be one element longer than {goal}"
                assert child[:-1] == goal, f"Child {child}'s prefix should equal {goal}"

    def test_children_of_max_k_paths_are_empty(self, simple_grammar, start_symbol):
        """Paths at maximum depth have no children."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        # All goals of length max_k should have no children
        max_k_paths = {g for g in graph.all_goals if len(g) == 2}
        for path in max_k_paths:
            assert (
                graph.get_children(path) == set()
            ), f"Max-k path {path} should have no children"

    def test_all_goals_with_max_k_1(self, simple_grammar, start_symbol):
        """With max_k=1 all goals are 1-paths and there are no children."""
        graph = _KPathGoalGraph(simple_grammar, max_k=1, start_symbol=start_symbol)
        assert graph.all_goals == frozenset(graph.root_goals)
        for goal in graph.root_goals:
            assert graph.get_children(goal) == set()

    def test_unknown_start_symbol_gives_empty(self, simple_grammar):
        """An unknown start symbol should yield an empty goal graph."""
        graph = _KPathGoalGraph(
            simple_grammar, max_k=2, start_symbol=NonTerminal("<unknown>")
        )
        assert len(graph.all_goals) == 0
        assert len(graph.root_goals) == 0


class TestDynaMOSAGoalManager:
    """Tests for _DynaMOSAGoalManager."""

    def test_initial_active_goals_equal_root_goals(self, simple_grammar, start_symbol):
        """Active goals before any update should be exactly the root goals."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)
        assert manager.active_goals == graph.root_goals

    def test_initially_no_covered_goals(self, simple_grammar, start_symbol):
        """No goals should be covered before update is called."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)
        assert len(manager.covered_goals) == 0

    def test_initially_all_goals_are_uncovered(self, simple_grammar, start_symbol):
        """All goals should be uncovered before update is called."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)
        assert manager.uncovered_goals == set(graph.all_goals)

    def test_update_increases_covered_goals(self, simple_grammar, start_symbol):
        """After updating with a population, covered goals should increase."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)

        population = [_generate_individual(simple_grammar) for _ in range(10)]
        manager.update(population)

        assert len(manager.covered_goals) > 0

    def test_covered_goals_not_in_active(self, simple_grammar, start_symbol):
        """Covered goals should not remain in the active set."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)

        population = [_generate_individual(simple_grammar) for _ in range(20)]
        manager.update(population)

        assert manager.covered_goals.isdisjoint(manager.active_goals)

    def test_children_unlocked_after_parent_covered(self, simple_grammar, start_symbol):
        """Children of a covered goal should be activated."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)

        population = [_generate_individual(simple_grammar) for _ in range(30)]
        manager.update(population)

        # For any 1-path that has been covered, its children should now be active
        # (or already covered, but not still locked)
        for goal in manager.covered_goals:
            if isinstance(goal, tuple) and len(goal) == 1:
                for child in graph.get_children(goal):
                    if child not in manager.covered_goals:
                        assert (
                            child in manager.active_goals
                        ), f"Child {child} of covered {goal} should be active"

    def test_solutions_are_deduplicated(self, simple_grammar, start_symbol):
        """Solutions property should not return duplicate individuals."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)

        population = [_generate_individual(simple_grammar) for _ in range(10)]
        manager.update(population)

        solutions = manager.solutions
        # Check no duplicate by identity
        seen_ids = [id(s) for s in solutions]
        assert len(seen_ids) == len(set(seen_ids))

    def test_uncovered_plus_covered_equals_all_goals(
        self, simple_grammar, start_symbol
    ):
        """uncovered_goals + covered_goals == all_goals."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(simple_grammar, graph, max_k=2)

        population = [_generate_individual(simple_grammar) for _ in range(10)]
        manager.update(population)

        assert manager.covered_goals | manager.uncovered_goals == set(graph.all_goals)


class TestComputeParetoFronts:
    """Tests for _compute_pareto_fronts."""

    def test_empty_population_returns_empty(self, simple_grammar):
        """Empty population yields empty fronts."""
        result = _compute_pareto_fronts([], set(), simple_grammar, max_k=2)
        assert result == []

    def test_no_active_goals_puts_all_in_one_front(self, simple_grammar):
        """With no active goals, no one dominates anyone — all in one front."""
        pop = [_generate_individual(simple_grammar) for _ in range(5)]
        result = _compute_pareto_fronts(pop, set(), simple_grammar, max_k=2)
        assert len(result) == 1
        assert len(result[0]) == 5

    def test_all_individuals_assigned(self, simple_grammar, start_symbol):
        """All individuals should appear in exactly one front."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        active: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = set(
            graph.root_goals
        )
        pop = [_generate_individual(simple_grammar) for _ in range(6)]
        fronts = _compute_pareto_fronts(pop, active, simple_grammar, max_k=2)

        assigned = [ind for front in fronts for ind in front]
        assert len(assigned) == len(pop)

    def test_first_front_non_empty(self, simple_grammar, start_symbol):
        """The first front should always be non-empty for a non-empty population."""
        graph = _KPathGoalGraph(simple_grammar, max_k=2, start_symbol=start_symbol)
        active: set[KPath | _ConstraintGoal | _SoftConstraintGoal] = set(
            graph.root_goals
        )
        pop = [_generate_individual(simple_grammar) for _ in range(4)]
        fronts = _compute_pareto_fronts(pop, active, simple_grammar, max_k=2)
        assert len(fronts) >= 1
        assert len(fronts[0]) >= 1


class TestDynaMOSAAlgorithm:
    """Integration tests for DynaMOSAAlgorithm."""

    def test_generate_returns_suite(self, simple_grammar, empty_constraints):
        """generate() should return a non-empty Suite."""
        algo = DynaMOSAAlgorithm(simple_grammar, empty_constraints, max_k=2)
        result = algo.generate(max_generations=2)
        assert isinstance(result, Suite)
        assert len(result) > 0

    def test_generate_individuals_are_valid(self, simple_grammar, empty_constraints):
        """All individuals in the returned suite should be Individual instances."""
        algo = DynaMOSAAlgorithm(simple_grammar, empty_constraints, max_k=2)
        result = algo.generate(max_generations=2)
        for ind in result:
            assert isinstance(ind, Individual)

    def test_population_size_respected(self, simple_grammar, empty_constraints):
        """Internal population should match configured population_size."""
        algo = DynaMOSAAlgorithm(
            simple_grammar, empty_constraints, population_size=5, max_k=2
        )
        algo.generate(max_generations=3)
        assert len(algo._population) == 5

    def test_coverage_improves_with_more_generations(
        self, simple_grammar, empty_constraints
    ):
        """More generations should produce at least as much k-path coverage."""
        fitness_fn = KPathCoverageFitnessFunction(simple_grammar, k=2)

        few = DynaMOSAAlgorithm(
            simple_grammar, empty_constraints, max_k=2, population_size=8
        )
        result_few = few.generate(max_generations=1)
        cov_few = fitness_fn.fitness(result_few)

        many = DynaMOSAAlgorithm(
            simple_grammar, empty_constraints, max_k=2, population_size=8
        )
        result_many = many.generate(max_generations=20)
        cov_many = fitness_fn.fitness(result_many)

        assert cov_many >= cov_few

    def test_max_k_1_terminates(self, simple_grammar, empty_constraints):
        """DynaMOSA with max_k=1 should terminate when all 1-paths are covered."""
        algo = DynaMOSAAlgorithm(
            simple_grammar, empty_constraints, max_k=1, population_size=5
        )
        result = algo.generate(max_generations=50)
        assert isinstance(result, Suite)
        assert len(result) > 0

    def test_single_generation_returns_suite(self, simple_grammar, empty_constraints):
        """Even with max_generations=1 a valid Suite must be returned."""
        algo = DynaMOSAAlgorithm(simple_grammar, empty_constraints, max_k=2)
        result = algo.generate(max_generations=1)
        assert isinstance(result, Suite)
        assert len(result) > 0

    def test_zero_max_generations_returns_suite(
        self, simple_grammar, empty_constraints
    ):
        """With max_generations=0 the initial population still yields a Suite."""
        algo = DynaMOSAAlgorithm(simple_grammar, empty_constraints, max_k=2)
        result = algo.generate(max_generations=0)
        assert isinstance(result, Suite)


class TestDynaMOSAWithConstraints:
    """Tests for _DynaMOSAGoalManager and DynaMOSAAlgorithm with hard constraints."""

    def test_constraint_goal_appears_in_uncovered_before_satisfied(
        self, simple_grammar, start_symbol
    ):
        """With an always-failing constraint, ConstraintGoal(0) should be in uncovered_goals."""
        failing = _make_constraint(always_pass=False)
        graph = _KPathGoalGraph(simple_grammar, max_k=1, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(
            simple_grammar, graph, max_k=1, hard_constraints=[failing]
        )
        assert _ConstraintGoal(0) in manager.uncovered_goals

    def test_constraint_satisfied_individual_removes_from_uncovered(
        self, simple_grammar, start_symbol
    ):
        """When an individual satisfies the constraint, ConstraintGoal leaves uncovered_goals."""
        passing = _make_constraint(always_pass=True)
        graph = _KPathGoalGraph(simple_grammar, max_k=1, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(
            simple_grammar, graph, max_k=1, hard_constraints=[passing]
        )
        population = [_generate_individual(simple_grammar) for _ in range(5)]
        manager.update(population)
        assert _ConstraintGoal(0) not in manager.uncovered_goals

    def test_kpath_not_covered_without_constraint_satisfaction(
        self, simple_grammar, start_symbol
    ):
        """With a failing constraint, k-path goals should NOT be marked as covered."""
        failing = _make_constraint(always_pass=False)
        graph = _KPathGoalGraph(simple_grammar, max_k=1, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(
            simple_grammar, graph, max_k=1, hard_constraints=[failing]
        )
        population = [_generate_individual(simple_grammar) for _ in range(20)]
        manager.update(population)
        kpath_covered = {g for g in manager.covered_goals if isinstance(g, tuple)}
        assert len(kpath_covered) == 0

    def test_no_constraints_unchanged_behavior(self, simple_grammar, start_symbol):
        """With no constraints, behavior is identical to original (no ConstraintGoals)."""
        graph = _KPathGoalGraph(simple_grammar, max_k=1, start_symbol=start_symbol)
        manager = _DynaMOSAGoalManager(
            simple_grammar, graph, max_k=1, hard_constraints=[]
        )
        assert manager._mandatory_goals == frozenset()
        population = [_generate_individual(simple_grammar) for _ in range(20)]
        manager.update(population)
        for g in manager.uncovered_goals:
            assert isinstance(g, tuple)
        for g in manager.covered_goals:
            assert isinstance(g, tuple)

    def test_pareto_fronts_with_constraint_goals(self, simple_grammar, start_symbol):
        """All individuals are assigned to fronts when constraint goals are active."""
        passing = _make_constraint(always_pass=True)
        failing = _make_constraint(always_pass=False)
        graph = _KPathGoalGraph(simple_grammar, max_k=1, start_symbol=start_symbol)
        active: set = set(graph.root_goals) | {_ConstraintGoal(0)}

        pop = [_generate_individual(simple_grammar) for _ in range(4)]
        fronts_pass = _compute_pareto_fronts(
            pop, active, simple_grammar, max_k=1, hard_constraints=[passing]
        )
        fronts_fail = _compute_pareto_fronts(
            pop, active, simple_grammar, max_k=1, hard_constraints=[failing]
        )
        assert sum(len(f) for f in fronts_pass) == len(pop)
        assert sum(len(f) for f in fronts_fail) == len(pop)

    def test_algorithm_with_passing_constraint_returns_suite(self, simple_grammar):
        """DynaMOSA with an always-passing constraint should complete and return a Suite."""
        passing = _make_constraint(always_pass=True)
        algo = DynaMOSAAlgorithm(simple_grammar, [passing], max_k=1, population_size=5)
        result = algo.generate(max_generations=5)
        assert isinstance(result, Suite)
        assert len(result) > 0
