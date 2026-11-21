import argparse
from collections.abc import Generator
from typing import Any, Optional

import pytest

import fandango.api
from fandango import Fandango
from fandango.cli import commands
from fandango.cli.parser import get_parser
from fandango.language.grammar import FuzzingMode
from fandango.language.tree import DerivationTree


def fuzz_limits(monkeypatch: pytest.MonkeyPatch, *cli: str) -> dict[str, Any]:
    """The generation limit `fandango fuzz ...` passes to generate_solutions(),
    and the number of outputs it asks for."""
    seen: dict[str, Any] = {}

    def fake_generate_solutions(
        self: Fandango,
        max_generations: Optional[int] = None,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
    ) -> Generator[DerivationTree, None, None]:
        seen["max_generations"] = max_generations
        yield from ()

    def fake_warnings(
        self: Fandango, desired_solutions: Optional[int], found: int, settings: Any
    ) -> None:
        seen["desired_solutions"] = desired_solutions

    monkeypatch.setattr(
        fandango.api.Fandango, "generate_solutions", fake_generate_solutions
    )
    monkeypatch.setattr(
        fandango.api.Fandango, "_print_warnings_if_necessary_post_fuzz", fake_warnings
    )
    args: argparse.Namespace = get_parser(True).parse_args(
        ["fuzz", "-f", "docs/digits.fan", "--no-cache", *cli]
    )
    commands.fuzz_command(args)
    return seen


def test_cli_number_of_outputs_alone_means_no_generation_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_limits(monkeypatch, "-n", "10000")
    assert seen["desired_solutions"] == 10000
    assert seen["max_generations"] is None


def test_cli_explicit_generations_are_a_hard_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_limits(monkeypatch, "-n", "10000", "-N", "7")
    assert seen["max_generations"] == 7


def test_cli_without_any_limit_stops_after_500_generations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = fuzz_limits(monkeypatch)
    assert seen["desired_solutions"] is None
    assert seen["max_generations"] == fandango.api.DEFAULT_MAX_GENERATIONS


def test_number_of_outputs_alone_leaves_the_generations_unlimited() -> None:
    """Fandango.fuzz() adds no limit of its own when a number of outputs is given."""
    fan = Fandango("<start> ::= <digit>{2}")
    max_generations, desired_solutions, infinite = fan._sanitize_runtime_end_settings(
        FuzzingMode.COMPLETE, 10000, None, False, False
    )
    assert max_generations is None
    assert desired_solutions == 10000 and not infinite
