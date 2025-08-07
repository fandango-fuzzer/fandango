import logging
import re
from typing import Counter

import pytest
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.grammar_settings import GrammarSetting
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.parse import parse
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.symbols.terminal import Terminal
from fandango.language.tree import DerivationTree

REPETITIONS = 1000


# Gmutator mutation (1a)
def test_repeat_terminal():
    raw_grammar = """
<start> ::= "a"
setting all_with_type(TerminalNode) terminal_should_repeat = 1.0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None
    found_empty = False
    found_multiple = False
    for _ in range(REPETITIONS):
        tree = grammar.fuzz()
        assert tree is not None
        tree_str = str(tree)
        num_as = tree_str.count("a")
        assert len(tree_str) == num_as
        if num_as > 1:
            found_multiple = True
        elif num_as == 0:
            found_empty = True
        else:
            assert False, f"Unexpected tree: {tree_str}"
    assert found_empty
    assert found_multiple


# Gmutator mutation (1b)
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


# Gmutator mutation (1c)
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


# Gmutator mutation (2)
def test_concatenated_alternatives():
    raw_grammar = """
<start> ::= <a> | <b>
<a> ::= "a"
<b> ::= "b"
setting all_with_type(Alternative) alternatives_should_concatenate = 1.0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None

    for _ in range(REPETITIONS):
        tree = grammar.fuzz()
        assert tree is not None
        if tree.to_string() == "ab":
            found_ab = True
        elif tree.to_string() == "ba":
            found_ba = True
        else:
            raise ValueError(f"Unexpected tree: {tree.to_string()}")
    assert found_ab
    assert found_ba


# Gmutator mutation (2)
def test_concatenated_alternatives_with_multiple_alternatives():
    raw_grammar = """
<start> ::= <a> | <b> | <c> | <d>
<a> ::= "a"
<b> ::= "b"
<c> ::= "c"
<d> ::= "d"
setting all_with_type(Alternative) alternatives_should_concatenate = 1.0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None

    for _ in range(REPETITIONS):
        tree = grammar.fuzz()
        s = tree.to_string()
        assert len(s) >= 2
        assert all(c in "abcd" for c in s)
        if Counter(s) == {"a": 1, "b": 1, "c": 1, "d": 1}:
            found_abcd = True
    assert found_abcd


# Gmutator mutation (2)
def test_concatenated_alternatives_with_one_node():
    outer = DerivationTree(NonTerminal("<start>"))
    settings = GrammarSetting(
        "all_with_type(Alternative)", {"alternatives_should_concatenate": "1.0"}
    )
    alt = Alternative([TerminalNode(Terminal("a"), [])], [settings])
    alt.distance_to_completion = 2
    alt.fuzz(outer, Grammar.dummy(), 100)
    assert outer.to_string() == "a"


# Gmutator mutation (3)
def test_invert_regex():
    pattern = r"a|b|c"
    raw_grammar = f"""
<start> ::= r"{pattern}"
setting all_with_type(TerminalNode) invert_regex = 1.0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None

    for _ in range(REPETITIONS):
        tree = grammar.fuzz()
        assert tree is not None
        s = tree.to_string()
        assert re.match(pattern, s) is None  # should *not* match


# Gmutator mutation (3)
def test_max_out_of_regex_tries(caplog: pytest.LogCaptureFixture):
    pattern = r"a|b|c"
    raw_grammar = f"""
<start> ::= r"{pattern}"
setting all_with_type(TerminalNode) invert_regex = 1.0
setting all_with_type(TerminalNode) max_out_of_regex_tries = 0
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None

    for _ in range(REPETITIONS):
        caplog.set_level(logging.WARNING)
        caplog.clear()
        tree = grammar.fuzz()
        assert tree is not None
        out_list = caplog.get_records("call")

        assert len(out_list) == 1
        message = out_list[0].message
        assert (
            f"Failed to generate a non-matching regex: {pattern}, falling back to matching regex"
            in message
        ), message

        s = tree.to_string()
        assert (
            re.match(pattern, s) is not None
        )  # should match because we're out of tries, so we're falling back to matching regex


def test_impossible_out_of_regex_pattern(caplog: pytest.LogCaptureFixture):
    pattern = r".*"
    raw_grammar = f"""
<start> ::= r"{pattern}"
setting all_with_type(TerminalNode) invert_regex = 1.0
setting all_with_type(TerminalNode) max_out_of_regex_tries = 100
"""
    grammar, _ = parse(raw_grammar)
    assert grammar is not None

    for _ in range(REPETITIONS):
        caplog.set_level(logging.WARNING)
        caplog.clear()
        tree = grammar.fuzz()
        assert tree is not None
        out_list = caplog.get_records("call")

        assert len(out_list) == 1
        message = out_list[0].message
        assert (
            f"Failed to generate a non-matching regex: {pattern}, falling back to matching regex"
            in message
        ), message

        s = tree.to_string()
        assert (
            re.match(pattern, s) is not None
        )  # should match because we're out of tries, so we're falling back to matching regex


# Gmutator mutation (4)
def test_non_terminal_use_other_rule():
    raw_grammar = """
<start> ::= "prefix" <a>
<a> ::= "a"
setting <start> non_terminal_use_other_rule = 1.0
"""
    grammar, _ = parse(raw_grammar, use_stdlib=False)
    assert grammar is not None

    for _ in range(1):
        tree = grammar.fuzz()
        assert tree is not None
        s = tree.to_string()
        assert s == "a"
