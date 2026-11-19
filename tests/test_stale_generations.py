import argparse
from typing import Any

import pytest

import fandango.api
from fandango import Fandango
from fandango.cli import commands
from fandango.cli.parser import get_parser
from fandango.language.tree import DerivationTree

TWO = "<start> ::= 'a' | 'b'"
MANY = "<start> ::= <digit>{6}"


def test_generation_stops_after_generations_without_a_new_solution() -> None:
    fan = Fandango(TWO)
    fan.init_population(random_seed=1)
    assert fan.fandango is not None
    solutions = list(fan.fandango.generate(max_stale_generations=3))
    assert sorted(str(s) for s in solutions) == ["a", "b"]


def test_a_run_that_keeps_finding_solutions_is_not_stopped() -> None:
    """Each generation of 10 individuals yields a few solutions; 300 of them
    take far more than the 2 generations a run may go without one."""
    solutions = Fandango(MANY).fuzz(
        desired_solutions=300,
        population_size=10,
        max_stale_generations=2,
        random_seed=1,
    )
    assert len(solutions) == 300


def fuzz_kwargs(monkeypatch: pytest.MonkeyPatch, *cli: str) -> dict[str, Any]:
    """The arguments `fandango fuzz ...` passes on to Fandango.fuzz()."""
    seen: dict[str, Any] = {}

    def fake_fuzz(self: Fandango, **kwargs: Any) -> list[DerivationTree]:
        seen.update(kwargs)
        return []

    monkeypatch.setattr(fandango.api.Fandango, "fuzz", fake_fuzz)
    args: argparse.Namespace = get_parser(True).parse_args(
        ["fuzz", "-f", "docs/digits.fan", "--no-cache", *cli]
    )
    commands.fuzz_command(args)
    return seen


def test_cli_number_of_outputs_alone_is_not_cut_off_after_500_generations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_kwargs(monkeypatch, "-n", "10000")
    assert seen["desired_solutions"] == 10000
    assert seen["max_generations"] is None
    assert seen["max_stale_generations"] == fandango.api.DEFAULT_MAX_GENERATIONS


def test_cli_explicit_generations_are_a_hard_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_kwargs(monkeypatch, "-n", "10000", "-N", "7")
    assert seen["max_generations"] == 7
    assert seen["max_stale_generations"] is None


def test_cli_without_any_limit_still_stops_after_500_generations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_kwargs(monkeypatch)
    assert seen["desired_solutions"] is None
    assert seen["max_generations"] == fandango.api.DEFAULT_MAX_GENERATIONS
    assert seen["max_stale_generations"] is None
