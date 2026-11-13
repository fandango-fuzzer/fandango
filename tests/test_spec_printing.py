#!/usr/bin/env pytest

"""
`fandango convert` on a .fan file must print a spec that means the same.

Every .fan file of the repository is parsed and printed, and the printed text
is parsed again. Both parsed specs must then have the same structure: the
objects that make up their code, rules, generators and constraints are
compared attribute by attribute. Comparing the objects, not the texts, is what
finds a printed spec that parses but means something else, such as
`("a" <b>)*` printed as `'a' <b>*`.

A file whose Python code cannot run here (a missing module, say) is skipped.
"""

import re
from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import Any

import pytest

import fandango
from fandango.language.parse.parse_spec import parse_content
from fandango.language.parse.spec import FandangoSpec

from .utils import PROJECT_ROOT

# Attributes that do not say what a spec means: the Python environment,
# settings (which are not printed), generated names, and caches and state
# that fuzzing fills in.
IGNORED_ATTRIBUTES = {
    "id",
    "repetition_id",
    "_hash_cache",
    "local_variables",
    "global_variables",
    "_grammar_settings",
    "_settings",
    "cache",
    "iteration",
    "tdigest",
}

# Parsing names each search in an expression `___fandango_<address>_<count>___`
PLACEHOLDER = re.compile(r"___fandango_\d+_(\d+)___")


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


def attributes(
    value: Any, path: str = "spec", seen: tuple[int, ...] = ()
) -> Iterator[tuple[str, Any]]:
    """
    Everything `value` is made of, as (path, plain value) pairs, such as
    `("spec.rules[<start>].nodes[0].min", 1)`.
    """
    if isinstance(value, str):
        yield path, PLACEHOLDER.sub(r"___\1___", value)
    elif isinstance(value, (list, tuple)):
        yield f"{path}.length", len(value)
        for index, item in enumerate(value):
            yield from attributes(item, f"{path}[{index}]", seen)
    elif isinstance(value, dict):
        yield f"{path}.length", len(value)
        for index, (key, item) in enumerate(value.items()):
            name = key if isinstance(key, str) else key.format_as_spec()
            name = PLACEHOLDER.sub(r"___\1___", name)
            yield from attributes(item, f"{path}[{index}: {name}]", seen)
    elif (
        isinstance(value, Enum)
        or not type(value).__module__.startswith("fandango.")
        or not hasattr(value, "__dict__")
    ):
        yield path, value  # numbers, None, slices, ...
    elif id(value) in seen:
        yield path, f"the {type(value).__name__} above"
    else:
        yield f"{path}.type", type(value).__name__
        for name, attribute in vars(value).items():
            if name not in IGNORED_ATTRIBUTES:
                yield from attributes(attribute, f"{path}.{name}", (*seen, id(value)))


def spec_attributes(spec: FandangoSpec) -> dict[str, Any]:
    return dict(
        attributes(
            {
                "code": spec.code_text,
                "rules": spec.grammar.rules,
                "generators": spec.grammar.generators,
                "constraints": spec.constraints,
            }
        )
    )


@pytest.mark.parametrize(
    "path", spec_files(), ids=lambda path: str(path.relative_to(PROJECT_ROOT))
)
def test_printed_spec_means_the_same(
    path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(fandango.Fandango, "parser", "cpp")
    try:
        original = parse_content(path.read_text(), filename=str(path))
    except Exception as error:
        pytest.skip(f"does not parse on its own: {error!r}")

    printed = str(original)  # the text `fandango convert` prints
    try:
        reparsed = parse_content(printed, filename=str(path))
    except Exception as error:
        pytest.fail(f"the printed spec does not parse: {error}\n\n{printed}")

    assert spec_attributes(original) == spec_attributes(reparsed), printed
    # Printing the printed spec gives the same text again.
    assert str(reparsed) == printed
