import logging

import pytest

from fandango import Fandango
from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.errors import FandangoGeneratorError
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.population import PopulationManager
from fandango.language.tree import DerivationTree

SPEC = """
<start> ::= <digit>
where int(<start>) > 100
"""


class _AnySuggestion(Suggestion):
    """Suggests one replacement, whatever the tree."""

    def get_replacements(self, individual, grammar):  # type: ignore[no-untyped-def]
        return [(individual, individual)]

    def rec_set_allow_repetition_full_delete(self, allow: bool) -> None:
        pass


def test_fix_individual_survives_a_generator_that_fails_during_a_repair(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A repair re-runs the generators above the replaced nodes. If the output of
    one cannot be parsed, the repair is dropped; the run must go on."""
    fan = Fandango(SPEC)
    manager = PopulationManager(fan.grammar, "<start>")
    individual = fan.grammar.parse("5")
    assert individual is not None
    evaluated: list[DerivationTree] = []

    def eval_individual(tree):  # type: ignore[no-untyped-def]
        evaluated.append(tree)
        return 0.0, [], None
        yield  # pragma: no cover

    def failing_replace(self, grammar, replacements):  # type: ignore[no-untyped-def]
        raise FandangoGeneratorError("Could not parse b'..' into <x>", "<x>")

    monkeypatch.setattr(DerivationTree, "replace_multiple", failing_replace)
    failing = [FailingTree(individual, fan.constraints[0])]

    with caplog.at_level(logging.WARNING, logger="fandango"):
        solutions, (fixed, fixes_made) = GeneratorWithReturn(
            manager.fix_individual(
                individual, failing, _AnySuggestion(), eval_individual
            )
        ).collect()

    assert fixed is individual
    assert fixes_made == 0
    assert solutions == []
    assert evaluated == []
    assert "Discarding a repair" in caplog.text
