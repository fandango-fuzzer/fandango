import argparse
from collections.abc import Generator
from typing import Any

import pytest

import fandango.api
from fandango import Fandango
from fandango.cli import commands
from fandango.cli.parser import get_parser
from fandango.evolution.algorithm import SimpleGeneticAlgorithm
from fandango.language.tree import DerivationTree

SPEC = """
<start> ::= <digit>{3}
where int(<start>) > 100
"""
TWO = "<start> ::= 'a' | 'b'"


def test_fuzz_returns_what_it_hands_to_the_callback() -> None:
    seen: list[DerivationTree] = []
    solutions = Fandango(SPEC).fuzz(
        desired_solutions=5,
        solution_callback=lambda tree, _i: seen.append(tree),
        random_seed=1,
    )
    assert len(solutions) == 5
    assert solutions == seen
    assert all(int(str(t)) > 100 for t in solutions)


def test_fuzz_reports_missing_solutions(caplog) -> None:  # type: ignore[no-untyped-def]
    trees = Fandango(TWO).fuzz(desired_solutions=5, max_generations=3, random_seed=1)
    assert sorted(str(t) for t in trees) == ["a", "b"]
    assert "Only found 2 perfect solutions" in caplog.text


def test_fuzz_raises_on_missing_solutions_if_asked() -> None:
    with pytest.raises(fandango.api.FandangoFailedError):
        Fandango(TWO).fuzz(
            desired_solutions=5,
            max_generations=3,
            warnings_are_errors=True,
            random_seed=1,
        )


def test_best_effort_pads_up_to_the_desired_number() -> None:
    """The solutions, then up to 3 individuals of the population, each once."""
    fan = Fandango(TWO)
    result = fan.fuzz(
        desired_solutions=5, max_generations=3, best_effort=True, random_seed=1
    )
    assert isinstance(fan.fandango, SimpleGeneticAlgorithm)
    padding = fan.fandango.population[:3]
    assert sorted(str(t) for t in result[:2]) == ["a", "b"]
    assert result[2:] == padding


def test_cli_writes_solutions_without_collecting_them(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """`fandango fuzz` takes the solutions from generate_solutions() and never
    goes through fuzz(), which collects them."""

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


def test_cli_best_effort_writes_the_padding(tmp_path: Any) -> None:
    """The CLI writes what fuzz(best_effort=True) returns: the solutions plus padding."""
    spec = tmp_path / "two.fan"
    spec.write_text(TWO + "\n")
    out = tmp_path / "out"
    args: argparse.Namespace = get_parser(True).parse_args(
        ["fuzz", "-f", str(spec), "--no-cache", "-n", "5", "-N", "3"]
        + ["--random-seed", "1", "--best-effort", "-d", str(out)]
    )
    commands.fuzz_command(args)
    expected = Fandango(TWO).fuzz(
        desired_solutions=5, max_generations=3, best_effort=True, random_seed=1
    )
    assert len(expected) > 2  # padded
    written = sorted(out.iterdir())
    assert [p.read_text() for p in written] == [str(t) for t in expected]


def test_fuzz_with_infinite_is_deprecated() -> None:
    """It still runs (here until the callback stops it), but warns."""

    class Enough(Exception):
        pass

    def stop_after_three(_tree: DerivationTree, i: int) -> None:
        if i == 2:
            raise Enough()

    with pytest.warns(DeprecationWarning, match="generate_solutions"):
        with pytest.raises(Enough):
            Fandango(SPEC).fuzz(
                infinite=True, solution_callback=stop_after_three, random_seed=1
            )


def test_cli_validation_stops_at_the_first_output_that_does_not_parse_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """--validate parses each output back right after writing it; the first
    one that does not parse back ends the run, so it is the last output."""
    from fandango.errors import FandangoError

    def parses_nothing(
        self: Fandango, word: Any, **_kwargs: Any
    ) -> Generator[DerivationTree, None, None]:
        yield from ()

    monkeypatch.setattr(fandango.api.Fandango, "parse", parses_nothing)
    out = tmp_path / "out"
    args: argparse.Namespace = get_parser(True).parse_args(
        ["fuzz", "-f", "docs/digits.fan", "--no-cache", "-n", "5", "--random-seed", "1"]
        + ["-d", str(out), "--validate"]
    )
    with pytest.raises(FandangoError, match="Output 0 does not parse back"):
        commands.fuzz_command(args)
    assert sorted(p.name for p in out.iterdir()) == ["fandango-0000.txt"]
