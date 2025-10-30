import pytest
from fandango import DerivationTree
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse
from fandango.language.symbols.non_terminal import NonTerminal
from tests.utils import RESOURCES_ROOT


def test_with_passed_eq_constraints():
    with open(RESOURCES_ROOT / "persons.fan", "r") as file:
        grammar, constraints = parse([file, 'where <first_name> == "First"'])

    assert grammar is not None
    fan = Fandango(grammar, constraints)
    individual = grammar.parse("First Last,30")
    assert individual is not None
    gen = GeneratorWithReturn(fan.evaluator.evaluate_individual(individual=individual))
    solutions, (fitness, failing_trees, suggestion) = gen.collect()
    assert len(solutions) == 1
    assert fitness == 1.0
    assert len(failing_trees) == 0
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 0


@pytest.mark.parametrize(
    "constraint",
    [
        ("where <first_name> == 'John'"),
        ("where 'John' == <first_name>"),
    ],
)
def test_with_failing_eq_constraints_right_into_left(constraint):
    with open(RESOURCES_ROOT / "persons.fan", "r") as file:
        grammar, constraints = parse([file, constraint])

    assert grammar is not None
    fan = Fandango(grammar, constraints)
    individual = grammar.parse("First Last,30")
    assert individual is not None
    gen = GeneratorWithReturn(fan.evaluator.evaluate_individual(individual=individual))
    solutions, (fitness, failing_trees, suggestion) = gen.collect()
    assert len(solutions) == 0
    assert fitness == 0.0
    assert len(failing_trees) == 1
    assert failing_trees[0].tree.symbol == NonTerminal("<first_name>")
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 1
    target, source = suggested_replacements[0]
    assert target.symbol == NonTerminal("<first_name>")
    assert isinstance(source, DerivationTree)
    assert source == "John"


def test_with_soft_constraint():
    with open(RESOURCES_ROOT / "persons.fan", "r") as file:
        grammar, constraints = parse([file, "maximizing int(<age>)"])

    assert grammar is not None
    fan = Fandango(grammar, constraints)
    individual = grammar.parse("First Last,30")
    assert individual is not None
    gen = GeneratorWithReturn(fan.evaluator.evaluate_individual(individual=individual))
    solutions, (fitness, failing_trees, suggestion) = gen.collect()
    assert len(solutions) == 1
    assert 0 <= fitness <= 1
    assert len(failing_trees) == 1
    assert failing_trees[0].tree.symbol == NonTerminal("<age>")
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 0


def test_with_successful_hard_and_soft_constraints():
    with open(RESOURCES_ROOT / "persons.fan", "r") as file:
        grammar, constraints = parse(
            [file, "where <first_name> == 'First'", "maximizing int(<age>)"]
        )

    assert grammar is not None
    fan = Fandango(grammar, constraints)
    individual = grammar.parse("First Last,30")
    assert individual is not None
    gen = GeneratorWithReturn(fan.evaluator.evaluate_individual(individual=individual))
    solutions, (fitness, failing_trees, suggestion) = gen.collect()
    assert len(solutions) == 1
    assert 0.5 <= fitness <= 1
    assert len(failing_trees) == 1
    assert failing_trees[0].tree.symbol == NonTerminal("<age>")
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 0


def test_with_failing_hard_and_soft_constraints():
    with open(RESOURCES_ROOT / "persons.fan", "r") as file:
        grammar, constraints = parse(
            [file, "where <first_name> == 'John'", "maximizing int(<age>)"]
        )

    assert grammar is not None
    fan = Fandango(grammar, constraints)
    individual = grammar.parse("First Last,30")
    assert individual is not None
    gen = GeneratorWithReturn(fan.evaluator.evaluate_individual(individual=individual))
    solutions, (fitness, failing_trees, suggestion) = gen.collect()
    assert len(solutions) == 0
    assert fitness == 0.0
    assert len(failing_trees) == 1
    assert failing_trees[0].tree.symbol == NonTerminal("<first_name>")
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 1
    target, source = suggested_replacements[0]
    assert target.symbol == NonTerminal("<first_name>")
    assert isinstance(source, DerivationTree)
    assert source == "John"
