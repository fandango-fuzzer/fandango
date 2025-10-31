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


@pytest.mark.parametrize(
    "constraint",
    [
        "where <first_name> == 'John'",
        "where str(<first_name>) == 'John'",
        "where 'John' == <first_name>",
        "where 'John' == str(<first_name>)",
    ],
)
def test_provides_suggestion_with_fixed_value(constraint):
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
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 1
    target, source = suggested_replacements[0]
    assert target.symbol == NonTerminal("<first_name>")
    assert isinstance(source, DerivationTree)
    assert source.to_string() == "John"


@pytest.mark.parametrize(
    "constraint",
    [
        "where <first_name> == <last_name>",
        "where str(<first_name>) == str(<last_name>)",
        "where <first_name> == str(<last_name>)",
        "where str(<first_name>) == <last_name>",
        "where <last_name> == <first_name>",
        "where <last_name> == str(<first_name>)",
        "where str(<last_name>) == <first_name>",
        "where str(<last_name>) == str(<first_name>)",
    ],
)
def test_provides_suggestion_with_nt(constraint):
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
    assert len(failing_trees) == 2
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 1
    target, source = suggested_replacements[0]
    is_flipped = target.symbol == NonTerminal("<last_name>")
    assert isinstance(source, DerivationTree)
    if is_flipped:
        assert target.symbol == NonTerminal("<last_name>")
        assert source.to_string() == "First"
    else:
        assert target.symbol == NonTerminal("<first_name>")
        assert source.to_string() == "Last"


@pytest.mark.parametrize(
    "constraint",
    [
        "where <first_name> + 'hello' == 'Johnhello'",
        "where str(<first_name>) + 'hello' == 'Johnhello'",
        "where 'Johnhello' == <first_name> + 'hello'",
        "where 'Johnhello' == str(<first_name>) + 'hello'",
    ],
)
def test_does_not_provide_suggestion_with_altered_nt_and_fixed_value(constraint):
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
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 0


@pytest.mark.parametrize(
    "constraint",
    [
        "where <first_name> + 'hello' == <last_name>",
        "where str(<first_name>) + 'hello' == str(<last_name>)",
        "where <first_name> + 'hello' == str(<last_name>)",
        "where str(<first_name>) + 'hello' == <last_name>",
        "where <last_name> + 'hello' == <first_name>",
        "where <last_name> + 'hello' == str(<first_name>)",
        "where str(<last_name>) + 'hello' == <first_name>",
        "where str(<last_name>) + 'hello' == str(<first_name>)",
        "where <first_name> == <last_name> + 'hello'",
        "where str(<first_name>) == str(<last_name>) + 'hello'",
        "where <first_name> == str(<last_name>) + 'hello'",
        "where str(<first_name>)  == <last_name> + 'hello'",
        "where <last_name> == <first_name> + 'hello'",
        "where <last_name> == str(<first_name> + 'hello')",
        "where str(<last_name>) == <first_name> + 'hello'",
        "where str(<last_name>) == str(<first_name> + 'hello')",
    ],
)
def test_does_not_provide_suggestion_with_altered_nt_and_nt(constraint):
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
    assert len(failing_trees) == 2
    suggested_replacements = suggestion.get_replacements(individual, grammar)
    assert len(suggested_replacements) == 1
    target, source = suggested_replacements[0]
    is_flipped = target.symbol == NonTerminal("<last_name>")
    assert isinstance(source, DerivationTree)
    if is_flipped:
        assert target.symbol == NonTerminal("<last_name>")
        assert source.to_string() == "Firsthello"
    else:
        assert target.symbol == NonTerminal("<first_name>")
        assert source.to_string() == "Lasthello"
