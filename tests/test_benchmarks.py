import itertools
import sys
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


class ParseCase(NamedTuple):
    label: str
    spec: str
    word: str | bytes
    use_stdlib: bool = False
    incomplete: bool = False
    limit: int | None = None
    expect_trees: bool = True
    incremental: bool = False


PARSE_CASES = [
    ParseCase("csv", (RESOURCES_ROOT / "csv.fan").read_text(), "aa;bb;cc\n" * 16),
    ParseCase("node-types", GRAMMAR_WITH_ALL_NODE_TYPES, NODE_TYPE_RECORD * 24),
    ParseCase(
        "node-types-prefix",
        GRAMMAR_WITH_ALL_NODE_TYPES,
        NODE_TYPE_RECORD * 23 + "ab=1",
        incomplete=True,
    ),
    ParseCase(
        "no-match",
        GRAMMAR_WITH_ALL_NODE_TYPES,
        NODE_TYPE_RECORD * 23 + "ab=1?;",
        expect_trees=False,
    ),
    ParseCase("ambiguous", AMBIGUOUS_SPEC, "+".join("1" * 9), limit=25),
    ParseCase("right-recursion", RIGHT_RECURSIVE_SPEC, "a" * 300),
    ParseCase("left-recursion", LEFT_RECURSIVE_SPEC, "a" * 300),
    ParseCase("bits", (RESOURCES_ROOT / "bitstream.fan").read_text(), "a" * 64),
    ParseCase(
        "binary",
        (RESOURCES_ROOT / "rgb.fan").read_text(),
        b"rAbrBbrCbrDb" * 2 + b"\x01;",
    ),
    ParseCase("incremental", GRAMMAR_WITH_ALL_NODE_TYPES, NODE_TYPE_RECORD * 8, incremental=True),
]


def _run_case(case: ParseCase, fandango: FandangoBase, grammar: Any) -> None:
    if case.incremental:
        iter_parser = grammar._parser._iter_parser
        iter_parser.new_parse(start="<start>", mode=ParsingMode.INCOMPLETE if case.incomplete else ParsingMode.COMPLETE)
        for index in range(len(case.word)):
            for _ in iter_parser.consume(case.word[index : index + 1]):
                pass
        return

    trees = fandango.parse(case.word, prefix=case.incomplete)
    assert bool(list(itertools.islice(trees, case.limit))) is case.expect_trees


def test_parse(benchmark: BenchmarkFixture) -> None:
    prepared_grammars = []
    for case in PARSE_CASES:
        grammar, constraints = parse(case.spec, use_stdlib=case.use_stdlib, use_cache=False)
        assert grammar is not None
        fandango = Fandango._with_parsed(grammar, constraints)
        prepared_grammars.append((case, fandango, grammar))

    def clear_caches():
        for _, _, grammar in prepared_grammars:
            grammar._parser._cache.clear()

    def func():
        for case, fandango, grammar in prepared_grammars:
            _run_case(case, fandango, grammar)

    benchmark.pedantic(func, setup=clear_caches, rounds=25, iterations=1)


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
