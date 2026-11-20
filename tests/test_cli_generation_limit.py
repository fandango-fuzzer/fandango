import argparse
from collections.abc import Generator
from typing import Any

import pytest

import fandango.api
from fandango import Fandango
from fandango.cli import commands
from fandango.cli.parser import get_parser
from fandango.language.grammar import FuzzingMode
from fandango.language.tree import DerivationTree


def fuzz_kwargs(monkeypatch: pytest.MonkeyPatch, *cli: str) -> dict[str, Any]:
    """The arguments `fandango fuzz ...` passes on to Fandango.fuzz_iter()."""
    seen: dict[str, Any] = {}

    def fake_fuzz_iter(
        self: Fandango, **kwargs: Any
    ) -> Generator[DerivationTree, None, None]:
        seen.update(kwargs)
        yield from ()

    monkeypatch.setattr(fandango.api.Fandango, "fuzz_iter", fake_fuzz_iter)
    args: argparse.Namespace = get_parser(True).parse_args(
        ["fuzz", "-f", "docs/digits.fan", "--no-cache", *cli]
    )
    commands.fuzz_command(args)
    return seen


def test_cli_number_of_outputs_alone_means_no_generation_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_kwargs(monkeypatch, "-n", "10000")
    assert seen["desired_solutions"] == 10000
    assert seen["max_generations"] is None
    assert "max_stale_generations" not in seen


def test_cli_explicit_generations_are_a_hard_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_kwargs(monkeypatch, "-n", "10000", "-N", "7")
    assert seen["max_generations"] == 7


def test_without_any_limit_the_run_still_stops_after_500_generations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The CLI passes no limit on; Fandango.fuzz() then applies its default."""
    seen = fuzz_kwargs(monkeypatch)
    assert seen["desired_solutions"] is None
    assert seen["max_generations"] is None
    fan = Fandango("<start> ::= 'a'")
    max_generations, desired_solutions, infinite = fan._sanitize_runtime_end_settings(
        FuzzingMode.COMPLETE, None, None, False, False
    )
    assert max_generations == fandango.api.DEFAULT_MAX_GENERATIONS
    assert desired_solutions is None and not infinite


def test_number_of_outputs_alone_leaves_the_generations_unlimited() -> None:
    """Fandango.fuzz() adds no limit of its own when a number of outputs is given."""
    fan = Fandango("<start> ::= <digit>{2}")
    max_generations, desired_solutions, infinite = fan._sanitize_runtime_end_settings(
        FuzzingMode.COMPLETE, 10000, None, False, False
    )
    assert max_generations is None
    assert desired_solutions == 10000 and not infinite
