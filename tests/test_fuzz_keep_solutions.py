import gc
import weakref

from fandango import Fandango
from fandango.language.tree import DerivationTree

SPEC = """
<start> ::= <digit>{3}
where int(<start>) > 100
"""


def test_fuzz_keeps_and_returns_solutions_by_default() -> None:
    seen: list[DerivationTree] = []
    solutions = Fandango(SPEC).fuzz(
        desired_solutions=5,
        solution_callback=lambda tree, _i: seen.append(tree),
        random_seed=1,
    )
    assert len(solutions) == 5
    assert solutions == seen


def test_fuzz_can_hand_solutions_to_the_callback_only() -> None:
    """With keep_solutions=False the callback is the only receiver, so a long
    run does not hold on to every tree it has produced."""
    refs: list[weakref.ref[DerivationTree]] = []
    solutions = Fandango(SPEC).fuzz(
        desired_solutions=5,
        solution_callback=lambda tree, _i: refs.append(weakref.ref(tree)),
        keep_solutions=False,
        random_seed=1,
    )
    assert solutions == []
    assert len(refs) == 5


def test_fuzz_without_keeping_still_reports_missing_solutions(caplog) -> None:  # type: ignore[no-untyped-def]
    count = 0

    def callback(_tree: DerivationTree, _i: int) -> None:
        nonlocal count
        count += 1

    solutions = Fandango("<start> ::= 'a' | 'b'").fuzz(
        desired_solutions=5,
        max_generations=3,
        solution_callback=callback,
        keep_solutions=False,
        random_seed=1,
    )
    gc.collect()
    assert solutions == []
    assert count == 2
    assert "Only found 2 perfect solutions" in caplog.text


def test_fuzz_without_keeping_returns_no_best_effort_padding() -> None:
    """best_effort pads the result with individuals of the population. A caller
    that asked for nothing back gets nothing back."""
    spec = "<start> ::= 'a' | 'b'"
    kept = Fandango(spec).fuzz(
        desired_solutions=5, max_generations=3, best_effort=True, random_seed=1
    )
    assert len(kept) > 2  # two solutions plus padding

    seen: list[DerivationTree] = []
    solutions = Fandango(spec).fuzz(
        desired_solutions=5,
        max_generations=3,
        best_effort=True,
        solution_callback=lambda tree, _i: seen.append(tree),
        keep_solutions=False,
        random_seed=1,
    )
    assert solutions == []
    assert len(seen) == 2
