import argparse
import shutil
from pathlib import Path
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
    assert fan.fandango is not None
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


def test_cli_has_no_best_effort_option() -> None:
    """It never wrote the padding (the CLI writes solutions only), so it is gone;
    the `best_effort` setting of fuzz() remains."""
    with pytest.raises(SystemExit):
        get_parser(True).parse_args(["fuzz", "-f", "docs/digits.fan", "--best-effort"])


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


def test_cli_validation_is_in_memory_and_writes_failures_to_disk(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """--validate parses each solution back without a file; a solution that
    fails is written to a directory that the error names."""
    from fandango.errors import FandangoError

    def always_fails(original: Any, parsed: Any, *, filename: str = "") -> None:
        raise FandangoError(f"{filename}: does not match")

    monkeypatch.setattr(commands, "validate", always_fails)
    # report each failure and go on, as outside the tests
    monkeypatch.setattr("fandango.logger._RAISE_ON_LOGGED_EXCEPTIONS", False)
    out = tmp_path / "out"
    args: argparse.Namespace = get_parser(True).parse_args(
        ["fuzz", "-f", "docs/digits.fan", "--no-cache", "-n", "2", "--random-seed", "1"]
        + ["-d", str(out), "--validate"]
    )
    with pytest.raises(FandangoError, match="2 error") as error:
        commands.fuzz_command(args)
    failure_dir = str(error.value).rsplit(" ", 1)[-1]
    written = sorted(p.name for p in Path(failure_dir).iterdir())
    assert written == ["fandango-0000.txt", "fandango-0001.txt"]
    assert sorted(p.name for p in out.iterdir()) == written  # same contents
    for name in written:
        assert (Path(failure_dir) / name).read_text() == (out / name).read_text()
    shutil.rmtree(failure_dir)
