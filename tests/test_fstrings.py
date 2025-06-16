import pytest

from fandango import parse, FandangoParseError
from fandango.constraints.base import ExpressionConstraint


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
