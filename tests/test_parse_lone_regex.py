import time

import pytest

from fandango import Fandango
from fandango.language.grammar import ParsingMode

SPEC = """
<start> ::= <head> <blob> <text>
<head> ::= b'P'
<blob> ::= rb'[^m]*(?:m(?<!endstream)[^m]*)*'
<text> ::= r'[a-z]*'
<word> ::= r'[a-z]+'
<two> ::= rb'[0-9]+' b'x'
"""


@pytest.fixture(scope="module")
def grammar():  # type: ignore[no-untyped-def]
    return Fandango(SPEC).grammar


@pytest.mark.parametrize(
    "symbol, word",
    [
        ("<blob>", b""),
        ("<blob>", b"abc\x00\xffm"),
        ("<blob>", b"xendstream"),  # the regex rejects it
        ("<word>", "abc"),
        ("<word>", ""),  # needs one letter
        ("<word>", "aBc"),
        ("<text>", ""),
    ],
)
def test_a_rule_of_one_regex_parses_as_before(grammar, symbol, word) -> None:  # type: ignore[no-untyped-def]
    """The direct match gives the tree (or the failure) the Earley parser gives."""
    direct = grammar.parse(word, symbol)
    earley = grammar._parser.parse(word, symbol, mode=ParsingMode.COMPLETE)
    if earley is None:
        assert direct is None
    else:
        assert direct is not None
        assert direct.to_tree() == earley.to_tree()
        assert direct.symbol == earley.symbol
        assert [c.symbol for c in direct.children] == [
            c.symbol for c in earley.children
        ]
        assert (
            type(direct.children[0].symbol.value())
            is type(earley.children[0].symbol.value())
            if earley.children
            else True
        )


def test_other_rules_still_go_through_the_parser(grammar) -> None:  # type: ignore[no-untyped-def]
    assert str(grammar.parse(b"12x", "<two>")) == "12x"
    assert grammar.parse(b"12", "<two>") is None


def test_a_long_value_for_a_rule_of_one_regex_is_parsed_quickly(grammar) -> None:  # type: ignore[no-untyped-def]
    """The parser keeps a state and a copy of the prefix for every length the
    regex accepts: quadratic in the length (800,000 bytes took 8 GB)."""
    word = bytes(range(256)).replace(b"m", b"-") * 200  # 51,200 bytes
    start = time.time()
    tree = grammar.parse(word, "<blob>")
    assert tree is not None
    assert tree.to_bytes() == word
    assert time.time() - start < 2.0
