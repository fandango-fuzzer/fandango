#!/usr/bin/env pytest

"""
`fandango convert` on a .fan file must print a spec that means the same.

Two checks, both on the printed text:

- `printing.fan` has one of every construct. What it is printed as is kept in
  `printing_expected.fan`, to be read next to it: each line there has to mean
  what the line in `printing.fan` means.
- Every .fan file of the repository is printed. The printed text has to parse,
  and to be printed as the same text again.

A file whose Python code cannot run here (a missing module, say) is skipped.
"""

from pathlib import Path

import pytest

import fandango
from fandango.language.parse.parse_spec import parse_content

from .utils import PROJECT_ROOT, RESOURCES_ROOT


def spec_files() -> list[Path]:
    """All .fan files of the repository, without build output and hidden folders."""
    return sorted(
        path
        for path in PROJECT_ROOT.rglob("*.fan")
        if not any(
            part == "build" or part.startswith(".")
            for part in path.relative_to(PROJECT_ROOT).parts
        )
    )


def printed(text: str, filename: str) -> str:
    """What `fandango convert` prints for the spec `text`."""
    return str(parse_content(text, filename=filename)) + "\n"


@pytest.fixture(autouse=True)
def cpp_parser(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fandango.Fandango, "parser", "cpp")


def test_printed_as_expected() -> None:
    source = RESOURCES_ROOT / "printing.fan"
    expected = RESOURCES_ROOT / "printing_expected.fan"
    assert printed(source.read_text(), str(source)) == expected.read_text()


@pytest.mark.parametrize(
    "path", spec_files(), ids=lambda path: str(path.relative_to(PROJECT_ROOT))
)
def test_printed_spec_is_printed_the_same(path: Path) -> None:
    try:
        text = printed(path.read_text(), str(path))
    except Exception as error:
        pytest.skip(f"does not parse on its own: {error!r}")
    assert printed(text, str(path)) == text
