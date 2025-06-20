#!/usr/bin/env pytest

import ast
import os

import pytest
from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy
from antlr4.error.Errors import ParseCancellationException

from fandango.constraints import predicates
from fandango.constraints.base import ComparisonConstraint
from fandango.constraints.fitness import Comparison
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    SearchProcessor,
    PythonProcessor,
)
from fandango.language.grammar import (
    Alternative,
    Grammar,
)
from fandango.language.parse import parse
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import RuleSearch
from fandango.language.symbol import NonTerminal
from .utils import RESOURCES_ROOT

FUZZINGBOOK_GRAMMAR = {
    "<start>": ["<number>"],
    "<number>": ["<non_zero><digits>", "0"],
    "<digits>": ["", "<digit><digits>"],
    "<non_zero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


def get_tree(example, start="fandango"):
    lexer = FandangoLexer(InputStream(example))
    token = CommonTokenStream(lexer)
    parser = FandangoParser(token)
    parser._errHandler = BailErrorStrategy()
    return getattr(parser, start)()


def test_indents():
    tree = get_tree(
        r"""
<a> ::= \
    "a" \
    | "a" <a>
"""
    )
    splitter = FandangoSplitter()
    splitter.visit(tree)
    processor = GrammarProcessor()
    grammar = processor.get_grammar(splitter.productions)
    assert len(grammar.rules) == 1
    rule = list(grammar.rules.values())[0]
    assert isinstance(rule, Alternative)
    assert len(rule.alternatives) == 2


def test_alt_indents():
    tree = get_tree(
        r"""
<a> ::= (
    "a"
    | "a" <a>
    )
"""
    )
    splitter = FandangoSplitter()
    splitter.visit(tree)
    processor = GrammarProcessor()
    grammar = processor.get_grammar(splitter.productions)
    assert len(grammar.rules) == 1
    rule = list(grammar.rules.values())[0]
    assert isinstance(rule, Alternative)
    assert len(rule.alternatives) == 2


@pytest.mark.parametrize(
    "expression",
    [
        "x",
        "1",
        "x and y",
        "x or y",
        "x + y",
        "x - y",
        "x * y",
        "x / y",
        "x // y",
        "x ** y",
        "x @ y",
        "x << y",
        "x >> y",
        "x | y",
        "x ^ y",
        "~ x",
        "not x",
        "+ x",
        "- x",
        "x if y else z",
        "{x: y, v: w}",
        "{x, y, z}",
        "[x, y, z]",
        "(x, y, z)",
        "{x: y for x in z if x}",
        "{x for x in z if x}",
        "[x for x in z if x]",
        "(x for x in z if x)",
        "await x",
        "yield x",
        "yield from x",
        "x < y",
        "x <= y",
        "x > y",
        "x >= y",
        "x == y",
        # "x <> y",
        "x != y",
        "x is y",
        "x is not y",
        "x in y",
        "x not in y",
        "x()",
        "x(y, z, *a, v=w, **k)",
        "x.y.z",
        "x[y,a:b:c,::]",
        "*x",
    ],
)
def test_conversion_without_replace(expression):
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        with pytest.raises(ParseCancellationException):
            get_tree(
                expression,
                start="expression",
            )
    else:
        fandango_tree: FandangoParser.ExpressionContext = get_tree(
            expression, start="expression"
        )
        processor = SearchProcessor(Grammar({}))
        fandango_tree, searches, search_map = processor.visit(fandango_tree)
        assert 0 == len(searches)
        assert 0 == len(search_map)
        assert not isinstance(fandango_tree, list)
        assert ast.unparse(tree) == ast.unparse(fandango_tree)


@pytest.mark.parametrize(
    "expression,value,expected",
    [
        ("<x>", True, True),
        ("<x> and True", True, True),
        ("<x> or False", True, True),
        ("<x> + 3", 2, 5),
        ("<x> - 3", 2, -1),
        ("<x> * 3", 2, 6),
        ("<x> / 2", 2, 1),
        ("<x> // 2", 3, 1),
        ("<x> ** 3", 2, 8),
        ("<x> << 2", 2, 8),
        ("<x> >> 2", 8, 2),
        ("<x> | 2", 1, 3),
        ("<x> ^ 5", 4, 1),
        ("~ <x>", 1, -2),
        ("not <x>", True, False),
        ("+ <x>", 2, 2),
        ("- <x>", 2, -2),
        ("2 if <x> else 1", True, 2),
        ("{1: <x>, 3: 4}", 2, {1: 2, 3: 4}),
        ("{1, <x>, 3}", 2, {1, 2, 3}),
        ("[1, <x>, 3]", 2, [1, 2, 3]),
        ("(1, <x>, 3)", 2, (1, 2, 3)),
        ("{x: x for x in <x> if x % 2 == 1}", [1, 2, 3], {1: 1, 3: 3}),
        ("{x for x in <x> if x % 2 == 1}", [1, 2, 3], {1, 3}),
        ("[x for x in <x> if x % 2 == 1]", [1, 2, 3], [1, 3]),
        ("tuple(x for x in <x> if x % 2 == 1)", [1, 2, 3], (1, 3)),
        ("<x> < 3", 2, True),
        ("<x> <= 3", 2, True),
        ("<x> > 3", 2, False),
        ("<x> >= 3", 2, False),
        ("<x> == 3", 2, False),
        ("<x> != 3", 2, True),
        ("<x> is None", 2, False),
        ("<x> is not None", 2, True),
        ("<x> in [1, 2, 3]", 2, True),
        ("<x> not in [1, 2, 3]", 2, False),
        ("int(<x>)", "2", 2),
        ("<x>.lower()", "AbC", "abc"),
        # ("<x>[0, 2::2]", [1, 2, 3, 4], [1, 2, 4]),
    ],
)
def test_conversion_with_replacement(expression, value, expected):
    fandango_tree: FandangoParser.ExpressionContext = get_tree(
        expression, start="expression"
    )
    processor = SearchProcessor(Grammar({}))
    fandango_tree, searches, search_map = processor.visit(fandango_tree)
    assert 1 == len(search_map)
    assert 1 == len(searches)
    placeholder = list(search_map.keys())[0]
    assert expected == eval(ast.unparse(fandango_tree), {}, {placeholder: value})


@pytest.mark.parametrize(
    "stmt,value,is_global",
    [
        ("x = y = 1", 1, False),
        ("x: int = 1", 1, False),
        ("x = 0\nx += 1", 1, False),
        ("x = [0]\nx[0] += 1\nx = x[0]", 1, False),
        ("import os\nx = os.path.join('a', 'b')", os.path.join("a", "b"), False),
        (
            "try:\n    raise ValueError()\nexcept:\n    x = 1\nelse:\n    x = 1",
            1,
            False,
        ),
        ("a = [0, 1]\ndel a[0]\nx = a[0]", 1, False),
        ("pass\nx = 1", 1, False),
        ("def f(): yield 1\nfor x in f(): pass", 1, False),
        ("assert True\nx = 1", 1, False),
        ("for x in range(4):\n    if x != 1: continue\n    else: break", 1, False),
        ("global x\nx = 1", 1, True),
        (
            "def f():\n"
            "    y = 0\n"
            "    def g():\n"
            "        nonlocal y\n"
            "        y = 1\n"
            "        return y\n"
            "    return y + g()\n"
            "x = f()",
            1,
            False,
        ),
        ("if False: x = 0\nelif False: x = 2\nelse: x = 1", 1, False),
        ("class A: x = 1\nx = A.x", 1, False),
        (
            "class A:\n"
            "    def __enter__(self): return 1\n"
            "    def __exit__(self, exc_type, exc_val, exc_tb): pass\n"
            "with A() as x: pass",
            1,
            False,
        ),
        ("x = -2\nwhile x != 1: x += 1", 1, False),
        (
            "def f(y, *a, z: int, b: int=2, **c): return y + z - b\nx = f(4, z=-1)",
            1,
            False,
        ),
    ],
)
def test_conversion_statement(stmt, value, is_global):
    is_global = True  # As of now, all Python defs are parsed as global defs

    fandango_tree: FandangoParser.ExpressionContext = get_tree(stmt)
    splitter = FandangoSplitter()
    splitter.visit(fandango_tree)
    code = splitter.python_code
    processor = PythonProcessor()
    fandango_tree = processor.get_code(code)
    tree = ast.parse(stmt)
    assert ast.unparse(fandango_tree) == ast.unparse(tree)
    global_vars = predicates.__dict__.copy()
    local_vars = None  # Must be None to ensure top-level imports
    exec(ast.unparse(fandango_tree), global_vars, local_vars)
    if is_global:
        assert "x" in global_vars
        assert local_vars is None or "x" not in local_vars
        assert value == global_vars["x"]
    else:
        assert "x" not in global_vars
        assert local_vars is None or "x" in local_vars
        assert value == local_vars["x"]


def test_parsing():
    with open(RESOURCES_ROOT / "fandango.fan", "r") as file:
        grammar, constraints = parse(file, use_stdlib=False, use_cache=False)
    assert isinstance(grammar, Grammar)
    assert len(grammar.rules) == 4
    assert "<start>" in grammar
    assert "<number>" in grammar
    assert "<non_zero>" in grammar
    assert "<digit>" in grammar
    assert len(constraints) == 1
    constraint = constraints[0]
    assert isinstance(constraint, ComparisonConstraint)
    assert constraint.right == "0"
    assert constraint.operator == Comparison.EQUAL
    assert len(constraint.searches) == 1
    placeholder = list(constraint.searches.keys())[0]
    assert constraint.left == f"f({placeholder}) % 2"
    assert "f" in constraint.global_variables
    assert eval("f('1')", constraint.global_variables, constraint.local_variables) == 1
    assert isinstance(constraint.searches[placeholder], RuleSearch)
    search: RuleSearch = constraint.searches[placeholder]
    assert NonTerminal("<number>") == search.symbol
