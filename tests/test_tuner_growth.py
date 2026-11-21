from fandango import Fandango
from fandango.evolution.adaptation import AdaptiveTuner
from fandango.evolution.evaluation import Evaluator
from fandango.language import DerivationTree
from fandango.language.grammar import nodes
from fandango.language.grammar.k_paths import GrammarKPaths

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


def _tuner() -> AdaptiveTuner:
    return AdaptiveTuner(0.2, 0.8, 20, 200, None, 0.5, 1000, 0.5)


class _NoDiversityEvaluator(Evaluator):
    def __init__(self) -> None:
        grammar = Fandango(SPEC).grammar
        super().__init__(
            grammar=grammar,
            k_paths=GrammarKPaths(grammar),
            constraints=[],
            expected_fitness=1.0,
            diversity_k=0,
            diversity_weight=0.0,
        )

    def compute_diversity_bonus(  # type: ignore[override]
        self, individuals: list[DerivationTree], fill_up: object = None
    ) -> list[float]:
        return []


def _update_stuck(tuner: AdaptiveTuner, found_new_solutions: bool) -> None:
    """One generation in which the best fitness did not improve."""
    tuner.update_parameters(
        generation=1,
        prev_best_fitness=1.0,
        current_best_fitness=1.0,
        population=[],
        evaluator=_NoDiversityEvaluator(),
        current_max_repetition=20,
        found_new_solutions=found_new_solutions,
    )


def test_tuner_does_not_grow_when_the_generation_found_new_solutions() -> None:
    tuner = _tuner()
    _update_stuck(tuner, found_new_solutions=True)
    assert tuner.current_max_repetition == 20
    assert tuner.current_max_nodes == 200


def test_tuner_grows_when_the_generation_found_no_new_solutions() -> None:
    tuner = _tuner()
    _update_stuck(tuner, found_new_solutions=False)
    assert tuner.current_max_repetition > 20
    assert tuner.current_max_nodes > 200
