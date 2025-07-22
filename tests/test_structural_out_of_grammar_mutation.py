from typing import Counter
from fandango.language.parse import parse

REPETITIONS = 1000


def test_repeat_nonterminal():
    raw_grammar = """
<start> ::= <nonterminal>
<nonterminal> ::= "a"
setting <nonterminal> nonterminal_should_repeat = 1.0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None
    found_empty = False
    found_multiple = False
    for _ in range(REPETITIONS):
        tree = grammar.fuzz()
        assert tree is not None
        counter = Counter(tree.to_string())
        assert len(counter) < 2
        if len(counter) == 1:
            assert "a" in counter
            assert counter["a"] != 1
            found_multiple = True
        else:
            assert tree.to_string() == ""
            found_empty = True
    assert found_empty
    assert found_multiple


def test_plus_should_return_nothing():
    raw_grammar = """
<start> ::= <nonterminal>+
<nonterminal> ::= "a"
setting all_with_type(Plus) plus_should_return_nothing = 1.0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None

    for _ in range(REPETITIONS):
        tree = grammar.fuzz()
        assert tree is not None
        assert tree.to_string() == ""


def test_option_should_return_multiple():
    raw_grammar = """
<start> ::= <nonterminal>?
<nonterminal> ::= "a"
setting all_with_type(Option) option_should_return_multiple = 1.0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None
    for _ in range(REPETITIONS):
        tree = grammar.fuzz()
        assert tree is not None
        t = tree.to_string()
        assert len(t) >= 2
        assert t.count("a") == len(t)
