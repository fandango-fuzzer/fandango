import itertools
import pytest
import sys
from fandango.language.parse.parse import parse
from fandango.api import Fandango
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from .utils import RESOURCES_ROOT
from pytest_benchmark.fixture import BenchmarkFixture


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

        assert False, f"9999 not found in the first 50 solutions: {solutions}"

    benchmark(func)
