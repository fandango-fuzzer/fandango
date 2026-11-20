import argparse
import inspect
from typing import Any

import pytest

import fandango.api
from fandango import Fandango
from fandango.cli import commands
from fandango.cli.parser import get_parser
from fandango.language.tree import DerivationTree

SPEC = """
<start> ::= <digit>{3}
where int(<start>) > 100
"""
TWO = "<start> ::= 'a' | 'b'"


def test_fuzz_iter_yields_the_solutions_one_at_a_time() -> None:
    solutions = Fandango(SPEC).fuzz_iter(desired_solutions=5, random_seed=1)
    assert inspect.isgenerator(solutions)
    trees = list(solutions)
    assert len(trees) == 5
    assert all(int(str(t)) > 100 for t in trees)


def test_fuzz_returns_what_fuzz_iter_yields() -> None:
    seen: list[DerivationTree] = []
    solutions = Fandango(SPEC).fuzz(
        desired_solutions=5,
        solution_callback=lambda tree, _i: seen.append(tree),
        random_seed=1,
    )
    iterated = list(Fandango(SPEC).fuzz_iter(desired_solutions=5, random_seed=1))
    assert solutions == seen
    assert [str(t) for t in solutions] == [str(t) for t in iterated]


def test_fuzz_iter_reports_missing_solutions_at_the_end(caplog) -> None:  # type: ignore[no-untyped-def]
    trees = list(
        Fandango(TWO).fuzz_iter(desired_solutions=5, max_generations=3, random_seed=1)
    )
    assert sorted(str(t) for t in trees) == ["a", "b"]
    assert "Only found 2 perfect solutions" in caplog.text


def test_fuzz_iter_raises_on_missing_solutions_if_asked() -> None:
    with pytest.raises(fandango.api.FandangoFailedError):
        list(
            Fandango(TWO).fuzz_iter(
                desired_solutions=5,
                max_generations=3,
                warnings_are_errors=True,
                random_seed=1,
            )
        )


def test_best_effort_pads_up_to_the_desired_number() -> None:
    """The solutions, then up to 3 individuals of the population, each once."""
    fan = Fandango(TWO)
    result = fan.fuzz(
        desired_solutions=5, max_generations=3, best_effort=True, random_seed=1
    )
    assert fan.fandango is not None
    padding = fan.fandango.population[:3]
    assert sorted(str(t) for t in result[:2]) == ["a", "b"]
    assert result[2:] == padding


def test_cli_writes_solutions_without_collecting_them(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """`fandango fuzz` goes through fuzz_iter, never through fuzz()."""

    def no_fuzz(self: Fandango, **_kwargs: Any) -> list[DerivationTree]:
        raise AssertionError("the CLI must not collect solutions")

    monkeypatch.setattr(fandango.api.Fandango, "fuzz", no_fuzz)
    out = tmp_path / "out"
    args: argparse.Namespace = get_parser(True).parse_args(
        ["fuzz", "-f", "docs/digits.fan", "--no-cache", "-n", "5", "--random-seed", "1"]
        + ["-d", str(out), "--validate"]
    )
    commands.fuzz_command(args)
    assert len(list(out.iterdir())) == 5


def test_cli_has_no_best_effort_option() -> None:
    """It never wrote the padding (the CLI writes solutions only), so it is gone;
    the `best_effort` setting of fuzz() remains."""
    with pytest.raises(SystemExit):
        get_parser(True).parse_args(["fuzz", "-f", "docs/digits.fan", "--best-effort"])
