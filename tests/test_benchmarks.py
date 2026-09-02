import itertools
import sys
from collections.abc import Callable
from typing import Any, NamedTuple

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from fandango.api import Fandango, FandangoBase
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.language.grammar import ParsingMode
from fandango.language.parse.parse import parse

from .utils import RESOURCES_ROOT

GRAMMAR_WITH_ALL_NODE_TYPES = """
<start> ::= <record>+
<record> ::= <key> '=' <value> <flags> ';'
<key> ::= r'[a-z]+'
<value> ::= <number> | <quoted> | <empty>
<number> ::= <digit>{1,4}
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<quoted> ::= '"' <char>* '"'
<char> ::= 'x' | 'y'
<empty> ::= ''
<flags> ::= <flag>?
<flag> ::= '!'
"""
NODE_TYPE_RECORD = 'ab=12;cd="xy"!;ef=;'


AMBIGUOUS_SPEC = "<start> ::= <e>\n<e> ::= <e> '+' <e> | '1'\n"
RIGHT_RECURSIVE_SPEC = '<start> ::= <A>\n<A> ::= "a" <A> | "a"\n'
LEFT_RECURSIVE_SPEC = '<start> ::= <A>\n<A> ::= <A> "a" | "a"\n'


def repeat_to(unit: str, length: int) -> str:
    """`unit` repeated to about `length`, cut on a unit boundary."""
    return unit * max(1, round(length / len(unit)))


class ParseCase(NamedTuple):
    label: str
    spec: str
    make_word: Callable[[int], str | bytes]
    use_stdlib: bool = False
    incomplete: bool = False
    limit: int | None = None
    expect_trees: bool = True
    incremental: bool = False


PARSE_CASES = [
    ParseCase(
        label="csv",
        spec=(RESOURCES_ROOT / "csv.fan").read_text(),
        make_word=lambda n: repeat_to("aa;bb;cc\n", n),
    ),
    ParseCase(
        label="node-types",
        spec=GRAMMAR_WITH_ALL_NODE_TYPES,
        make_word=lambda n: repeat_to(NODE_TYPE_RECORD, n),
    ),
    ParseCase(
        label="node-types-prefix",
        spec=GRAMMAR_WITH_ALL_NODE_TYPES,
        make_word=lambda n: repeat_to(NODE_TYPE_RECORD, n) + "ab=1",
        incomplete=True,
    ),
    ParseCase(
        label="no-match",
        spec=GRAMMAR_WITH_ALL_NODE_TYPES,
        make_word=lambda n: repeat_to(NODE_TYPE_RECORD, n) + "ab=1?;",
        expect_trees=False,
    ),
    ParseCase(
        label="ambiguous",
        spec=AMBIGUOUS_SPEC,
        make_word=lambda n: "+".join("1" * (n // 2 + 1)),
        limit=25,
    ),
    ParseCase(
        label="right-recursion",
        spec=RIGHT_RECURSIVE_SPEC,
        make_word=lambda n: "a" * n,
    ),
    ParseCase(
        label="left-recursion",
        spec=LEFT_RECURSIVE_SPEC,
        make_word=lambda n: "a" * n,
    ),
    ParseCase(
        label="bits",
        spec=(RESOURCES_ROOT / "bitstream.fan").read_text(),
        make_word=lambda n: "a" * n,
    ),
    ParseCase(
        label="binary",
        spec=(RESOURCES_ROOT / "rgb.fan").read_text(),
        make_word=lambda n: b"rAb" * max(1, n // 3) + b"\x01;",
    ),
    ParseCase(
        label="incremental",
        spec=GRAMMAR_WITH_ALL_NODE_TYPES,
        make_word=lambda n: repeat_to(NODE_TYPE_RECORD, n),
        incremental=True,
    ),
]

PARSE_LENGTHS = (10, 30, 100)
PARSE_GRID = [(case, length) for case in PARSE_CASES for length in PARSE_LENGTHS]


def _run_case(
    case: ParseCase, word: str | bytes, fandango: FandangoBase, grammar: Any
) -> None:
    if case.incremental:
        iter_parser = grammar._parser._iter_parser
        iter_parser.new_parse(
            start="<start>",
            mode=ParsingMode.INCOMPLETE if case.incomplete else ParsingMode.COMPLETE,
        )
        for index in range(len(word)):
            for _ in iter_parser.consume(word[index : index + 1]):
                pass
        return

    trees = fandango.parse(word, prefix=case.incomplete)
    assert bool(list(itertools.islice(trees, case.limit))) is case.expect_trees


@pytest.mark.parametrize(
    ("case", "length"),
    PARSE_GRID,
    ids=[f"{case.label}-{length}" for case, length in PARSE_GRID],
)
def test_parse(benchmark: BenchmarkFixture, case: ParseCase, length: int) -> None:
    grammar, constraints = parse(case.spec, use_stdlib=case.use_stdlib, use_cache=False)
    assert grammar is not None
    fandango = Fandango._with_parsed(grammar, constraints)
    word = case.make_word(length)

    def func():
        _run_case(case, word, fandango, grammar)

    benchmark.pedantic(
        func, setup=grammar._parser._cache.clear, rounds=25, iterations=1
    )


def test_parse_spec(benchmark: BenchmarkFixture):
    with open(RESOURCES_ROOT / "csv.fan", "r") as file:
        contents = file.read()

    def func():
        grammar, constraints = parse(contents, use_stdlib=False, use_cache=False)
        assert grammar is not None
        assert len(constraints) == 1

    benchmark(func)


def test_init_fandango(benchmark: BenchmarkFixture):
    with open(RESOURCES_ROOT / "csv.fan", "r") as file:
        contents = file.read()

    def func():
        fan = Fandango(contents, use_stdlib=False, use_cache=False)
        assert fan is not None

    benchmark(func)


def test_generate_with_single_hard_constraint(benchmark: BenchmarkFixture):
    with open(RESOURCES_ROOT / "even_numbers.fan", "r") as file:
        contents = file.read()
        grammar, constraints = parse(contents)
        assert grammar is not None
        assert len(constraints) == 1

    def func():
        fan = Fandango._with_parsed(grammar, constraints)
        gen = fan.generate_solutions()
        truncated_gen = itertools.islice(gen, 150)
        solutions = list(truncated_gen)
        assert len(solutions) == 150
        assert all(int(str(solution)) % 2 == 0 for solution in solutions)

    benchmark(func)


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="Broken? This is a quick and dirty fix because we need to get a critical bugfix release out of the door.",
)
def test_generate_with_single_soft_constraint(benchmark: BenchmarkFixture):
    with open(RESOURCES_ROOT / "simple_softvalue.fan", "r") as file:
        contents = file.read()
        grammar, constraints = parse(contents)
        assert grammar is not None
        assert len(constraints) == 2
        assert len(list(filter(lambda c: isinstance(c, SoftValue), constraints))) == 1
        assert len(list(filter(lambda c: isinstance(c, Constraint), constraints))) == 1

    def func():
        fan = Fandango._with_parsed(grammar, constraints)
        # make this a non-limiting factor
        max_generations = 10000
        gen = fan.generate_solutions(max_generations=max_generations)
        truncated_gen = itertools.islice(gen, 50)
        solutions = []
        for solution in truncated_gen:
            s = str(solution)
            solutions.append(s)
            if s == "9999":
                return

        raise AssertionError(f"9999 not found in the first 50 solutions: {solutions}")

    benchmark(func)
