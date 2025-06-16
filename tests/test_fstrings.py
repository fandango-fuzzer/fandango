import pytest

from fandango import parse, FandangoParseError, DerivationTree
from fandango.constraints.base import ExpressionConstraint, ComparisonConstraint
from fandango.language import NonTerminal, Terminal


@pytest.mark.parametrize(
    "expression",
    [
        "f'test'",
        "f'{x}'",
        "f'{x} {y}'",
        "f'{x} {y} {z}'",
        "f'{x} {y} {z} {a}'",
        "f'{x} {y} {z} {a} {b}'",
        "f'{x} {y} {z} {a} {b} {c}'",
        "f'{x}{y}{z}{a}{b}{c}'",
        "f'{x!r}'",
        "f'{x!s}'",
        "f'{x!a}'",
        "f'{<x>!r}'",
        "f'{<x>:{y}}'",
        "f'{<x>!r:{y}}{z}'",
        'f""',
        'f"test {x}"',
        'f"test {x} {y}"',
        'f"""\ntest\n{x}\n"""',
        'f"""\ntest\n{x} {y}\n"""',
        "f'''\ntest\n{x}\n'''",
        "f'''\ntest\n{x} {y}\n'''",
        """f"{x}" 'test0' "test1" f'{y}' 'test2'""",
    ],
)
def test_fstrings(expression):
    try:
        grammar, constraints = parse(
            f'<start> ::= <x>\n<x> ::= "x"\nwhere {expression}'
        )
    except FandangoParseError:
        pytest.fail(f"Failed to parse expression: {expression}")
    else:
        assert (
            grammar is not None
        ), f"Grammar should not be None for expression: {expression}"
        assert (
            len(constraints) == 1
        ), f"Constraints should contain one item for expression: {expression}"
        assert isinstance(
            constraints[0], ExpressionConstraint
        ), f"Constraints should be an ExpressionConstraint for expression: {expression}"


VALID = DerivationTree(
    NonTerminal("<start>"),
    [
        DerivationTree(NonTerminal("<x>"), [DerivationTree(Terminal("1"))]),
    ],
)

INVALID = DerivationTree(
    NonTerminal("<start>"),
    [
        DerivationTree(NonTerminal("<x>"), [DerivationTree(Terminal("2"))]),
    ],
)


def test_concreate_constraint():
    grammar, constraints = parse(
        '<start> ::= <x>\n<x> ::= "1" | "2" | "3" \nwhere f"{<x>!s:03}" == "100"',
    )
    assert grammar is not None, "Grammar should not be None"
    assert len(constraints) == 1, "Constraints should contain one item"
    assert isinstance(
        constraints[0], ComparisonConstraint
    ), "Constraints should be a ComparisonConstraint"
    constraint: ComparisonConstraint = constraints[0]
    assert len(constraint.searches) == 1, "Constraint should have one search"
    tmp_var: str = ""
    for search in constraint.searches:
        tmp_var = search
    assert (
        eval(constraint.left, {tmp_var: "25"}) == "250"
    ), "Left side of comparison should evaluate to '250'"
    assert (
        eval(constraint.right) == "100"
    ), "Right side of comparison should evaluate to '100'"
    assert constraint.check(VALID), "Constraint should pass for VALID tree"
    assert not constraint.check(INVALID), "Constraint should fail for INVALID tree"
