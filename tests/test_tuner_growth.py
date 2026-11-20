from fandango import Fandango
from fandango.evolution.adaptation import AdaptiveTuner
from fandango.language.grammar import nodes

SPEC = "<start> ::= <digit>*"


def run_generations(spec: str, generations: int, **settings):  # type: ignore[no-untyped-def]
    fan = Fandango(spec)
    fan.init_population(random_seed=1, population_size=20, **settings)
    assert fan.fandango is not None
    solutions = list(fan.fandango.generate(max_generations=generations))
    return fan.fandango, solutions


def test_repetitions_and_nodes_do_not_grow_while_solutions_keep_coming() -> None:
    """The tuner raises the repetition cap and the node budget when the search
    is stuck. A generation that found new solutions is not stuck, even though
    the best fitness cannot improve any more."""
    old = nodes.MAX_REPETITIONS
    nodes.MAX_REPETITIONS = 20  # other tests may have left it grown
    try:
        algorithm, solutions = run_generations(SPEC, 12)
        assert len(solutions) > 12
        assert algorithm.adaptive_tuner.current_max_repetition == 20
        assert nodes.MAX_REPETITIONS == 20
    finally:
        nodes.MAX_REPETITIONS = old


def test_repetitions_grow_when_no_solution_is_found() -> None:
    old = nodes.MAX_REPETITIONS
    nodes.MAX_REPETITIONS = 20
    try:
        # needs more digits than the repetition cap allows at first
        algorithm, _solutions = run_generations(
            SPEC + "\nwhere len(str(<start>)) > 30", 6
        )
        assert algorithm.adaptive_tuner.current_max_repetition > 20
    finally:
        nodes.MAX_REPETITIONS = old


def test_tuner_records_the_solution_count_per_generation() -> None:
    tuner = AdaptiveTuner(0.2, 0.8, 20, 200, None, 0.5, 200, 0.5)
    assert tuner._record_solution_count(0) is False
    assert tuner._record_solution_count(3) is True
    assert tuner._record_solution_count(3) is False
    assert tuner._record_solution_count(4) is True


def test_reset_starts_the_count_of_solutions_again() -> None:
    """SimpleGeneticAlgorithm.reset() empties the evaluator's solution set and
    resets the tuner; the first solutions after it count as new."""
    old = nodes.MAX_REPETITIONS
    nodes.MAX_REPETITIONS = 20
    try:
        algorithm, solutions = run_generations(SPEC, 3)
        assert algorithm.adaptive_tuner._solutions_seen > 0
        algorithm.reset()
        assert algorithm.evaluator.get_solution_count() == 0
        assert algorithm.adaptive_tuner._solutions_seen == 0
        assert algorithm.adaptive_tuner._record_solution_count(1) is True
    finally:
        nodes.MAX_REPETITIONS = old
