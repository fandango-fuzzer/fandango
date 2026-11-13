#!/usr/bin/env pytest

"""
`fandango convert` on a .fan file must print a spec that means the same.

Every .fan file of the repository is parsed and printed. The printed text is
parsed again and compared with the original, piece by piece: Python code,
rules (with repetition bounds and settings), generators and constraints.
Comparing the parsed specs, not the texts, is what finds a printed spec that
parses but means something else, such as `("a" <b>)*` printed as `'a' <b>*`.
Last, the printed spec is printed once more, and the text must stay the same.

A file whose Python code cannot run here (a missing module, say) is skipped.
"""

from collections import Counter
from collections.abc import Mapping
from pathlib import Path

import pytest

import fandango
from fandango.constraints.conjunction import ConjunctionConstraint
from fandango.constraints.constraint import Constraint
from fandango.constraints.disjunct import DisjunctionConstraint
from fandango.constraints.exists import ExistsConstraint
from fandango.constraints.forall import ForallConstraint
from fandango.constraints.implication import ImplicationConstraint
from fandango.constraints.repetition_bounds import RepetitionBoundsConstraint
from fandango.constraints.soft import SoftValue
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import NODE_SETTINGS_DEFAULTS, Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.parse.parse_spec import parse_content
from fandango.language.parse.spec import FandangoSpec
from fandango.language.search import NonTerminalSearch

from .utils import PROJECT_ROOT


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


def resolve(
    text: str, placeholders: Mapping[str, NonTerminalSearch | NonTerminalNode]
) -> str:
    """Replace the internal placeholders in `text` by what they stand for."""
    for placeholder, target in placeholders.items():
        text = text.replace(placeholder, target.format_as_spec())
    return text


def describe_node(node: Node) -> str:
    """
    The grammar element `node` in a spelling that cannot be read in two ways:
    every sequence and every alternative is in parentheses, computed
    repetition bounds are written out, and settings other than the defaults
    follow in brackets.
    """
    if isinstance(node, Alternative):
        text = "(" + " | ".join(describe_node(n) for n in node.alternatives) + ")"
    elif isinstance(node, Concatenation):
        text = "(" + " ".join(describe_node(n) for n in node.nodes) + ")"
    elif isinstance(node, Star):
        text = describe_node(node.node) + "*"
    elif isinstance(node, Plus):
        text = describe_node(node.node) + "+"
    elif isinstance(node, Option):
        text = describe_node(node.node) + "?"
    elif isinstance(node, Repetition):
        bounds = node.bounds_constraint
        if bounds is None:
            low, high = str(node.min), str(node.max)
        else:
            low = resolve(bounds.expr_data_min[0], bounds.expr_data_min[2])
            high = resolve(bounds.expr_data_max[0], bounds.expr_data_max[2])
        text = f"{describe_node(node.node)}{{{low}, {high}}}"
    else:
        # Terminals and nonterminals. A terminal is compared in its printed
        # form, because printing may respell a regex (`'` as `\x27`).
        text = node.format_as_spec()
    settings = {
        key: node.settings.get(key)
        for key, default in NODE_SETTINGS_DEFAULTS.items()
        if node.settings.get(key) != default
    }
    return f"{text} [{settings}]" if settings else text


def describe_constraint(constraint: Constraint | SoftValue) -> str:
    """The constraint with the kind of each of its parts spelled out."""
    if isinstance(constraint, (ConjunctionConstraint, DisjunctionConstraint)):
        text = ", ".join(describe_constraint(c) for c in constraint.constraints)
    elif isinstance(constraint, ImplicationConstraint):
        text = f"{describe_constraint(constraint.antecedent)} -> {describe_constraint(constraint.consequent)}"
    elif isinstance(constraint, (ForallConstraint, ExistsConstraint)):
        bound = constraint.bound
        name = bound if isinstance(bound, str) else bound.format_as_spec()
        text = f"{name} in {constraint.search.format_as_spec()}: {describe_constraint(constraint.statement)}"
    elif isinstance(constraint, RepetitionBoundsConstraint):
        low = resolve(constraint.expr_data_min[0], constraint.expr_data_min[2])
        high = resolve(constraint.expr_data_max[0], constraint.expr_data_max[2])
        text = f"{low} <= |{describe_node(constraint.repetition_node.node)}| <= {high}"
    else:
        text = constraint.format_as_spec()
    return f"{type(constraint).__name__}[{text}]"


def describe(spec: FandangoSpec) -> Counter[str]:
    """Everything a spec says, one entry per rule, generator and constraint."""
    grammar = spec.grammar
    return Counter(
        [
            f"code: {spec.code_text}",
            *(
                f"rule: {symbol.name()} ::= {describe_node(node)}"
                for symbol, node in grammar.rules.items()
            ),
            *(
                f"generator: {symbol.name()} := {resolve(generator.call, generator.nonterminals)}"
                for symbol, generator in grammar.generators.items()
            ),
            *(f"constraint: {describe_constraint(c)}" for c in spec.constraints),
        ]
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

    before, after = describe(original), describe(reparsed)
    lost = "\n".join(sorted((before - after).elements()))
    new = "\n".join(sorted((after - before).elements()))
    assert before == after, (
        f"the printed spec means something else.\n\n"
        f"Only in the original:\n{lost}\n\nOnly in the printed spec:\n{new}\n\n"
        f"Printed spec:\n{printed}"
    )
    # Printing the printed spec gives the same text again.
    assert str(reparsed) == printed
