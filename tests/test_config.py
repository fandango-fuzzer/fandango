import pytest

from fandango import Fandango

def test_config_from_fan_file():
    spec = """
    # @option max_repetitions = 20
    # @option mutation_rate = 0.3
    # @option desired_solutions = 5
    
    <start> ::= "hello"
    """
    fan = Fandango(spec)
    
    # Check that options are attached to grammar
    assert getattr(fan._grammar, "options", None) is not None
    assert fan._grammar.options["max_repetitions"] == 20
    assert fan._grammar.options["mutation_rate"] == 0.3
    assert fan._grammar.options["desired_solutions"] == 5

    # Check that fuzz respects these
    solutions = fan.fuzz()
    assert len(solutions) == 5  # because desired_solutions = 5 in config!

def test_config_overridden_by_kwargs():
    spec = """
    # @option desired_solutions = 5
    
    <start> ::= "hello"
    """
    fan = Fandango(spec)
    
    # Override via kwargs in fuzz
    solutions = fan.fuzz(desired_solutions=3)
    assert len(solutions) == 3
