# Tests are spread all over the place, adding this while none other are available.

import pytest
from collections.abc import Generator
from fandango.language.parse.parse import parse
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


@pytest.mark.parametrize("constructor", [lambda e: e, lambda e: NonTerminal(e)])
def tests_find_nt(constructor):
    SPEC = """
    <start> ::= <a> <b> <c> <c>
    <a> ::= "a" | "A"
    <b> ::= "b" | "B"
    <c> ::= "c" <d> | "C" <d>
    <d> ::= "d" | "D"
    """

    grammar, _ = parse(SPEC)
    assert grammar is not None
    tree = grammar.parse("abcdCD")
    assert isinstance(tree, DerivationTree)

    assert isinstance(tree.find_subtrees(constructor("<a>")), Generator)

    assert list(tree.find_subtrees(constructor("<a>"))) == [
        grammar.parse("a", start="<a>")
    ]
    assert list(tree.find_subtrees(constructor("<b>"))) == [
        grammar.parse("b", start="<b>")
    ]

    ds = list(tree.find_subtrees(constructor("<d>")))
    assert len(ds) == 2
    assert grammar.parse("d", start="<d>") in ds
    assert grammar.parse("D", start="<d>") in ds

    cs = list(tree.find_subtrees(constructor("<c>")))
    assert len(cs) == 2
    assert "cd" in cs
    assert "CD" in cs

    for c in cs:
        assert isinstance(c, DerivationTree)
        match str(c.children[0]):
            case "c":
                d = grammar.parse("d", start="<d>")
                assert c.children[1] == d
                assert list(c.find_subtrees(constructor("<d>"))) == [d]
            case "C":
                d = grammar.parse("D", start="<d>")
                assert c.children[1] == d
                assert list(c.find_subtrees(constructor("<d>"))) == [d]
            case _:
                assert False


def test_find_nt_is_breadth_first():
    spec = """
<start> ::= <left> <right>
<left> ::= <target>
<right> ::= "x" <target>
<target> ::= "a"
"""
    grammar, _ = parse(spec)
    assert grammar is not None
    tree = grammar.parse("axa")
    assert isinstance(tree, DerivationTree)

    targets = list(tree.find_subtrees("<target>"))

    assert len(targets) == 2
    assert str(targets[0]) == "a"
    assert str(targets[1]) == "a"
    assert targets[0].parent is not None
    assert targets[1].parent is not None
    assert str(targets[0].parent.symbol) == "<left>"
    assert str(targets[1].parent.symbol) == "<right>"
