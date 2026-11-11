# Tests are spread all over the place, adding this while none other are available.

import os
import pickle
import subprocess
import sys
from collections.abc import Generator

import pytest

from fandango.constraints.repetition_bounds import RepetitionBoundsConstraint
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
                raise AssertionError("Should not happen")


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


def test_pickled_tree_is_usable_in_another_process():
    """
    A tree pickled in one process must work against the same spec parsed in
    another. String hashes differ between processes, so neither cached hashes
    nor ids derived from them may end up in the pickle.
    """
    spec = '<start> ::= <n> <x>{int(<n>)}\n<n> ::= "1" | "2" | "3"\n<x> ::= "x"\n'
    writer = f"""
import pickle, sys
from fandango.language.parse.parse import parse
from fandango.language.symbols.terminal import Terminal
from fandango.language.tree import DerivationTree

grammar, constraints = parse({spec!r}, use_cache=False, use_stdlib=False)
good = grammar.parse("2xx")
bad = grammar.parse("2xx")
bad.children[0].set_children([DerivationTree(Terminal("3"))])  # now "3xx"
# fill the hash caches before pickling
assert good.symbol in grammar.rules and hash(good) != hash(bad)
sys.stdout.buffer.write(pickle.dumps((good, bad)))
"""
    seed = "2" if os.environ.get("PYTHONHASHSEED") != "2" else "3"
    result = subprocess.run(
        [sys.executable, "-c", writer],
        env={**os.environ, "PYTHONHASHSEED": seed},
        capture_output=True,
        check=True,
    )
    good, bad = pickle.loads(result.stdout)

    grammar, constraints = parse(spec, use_cache=False, use_stdlib=False)
    assert grammar is not None
    (constraint,) = constraints

    assert str(good) == "2xx" and str(bad) == "3xx"
    # hash caches
    assert good.symbol == NonTerminal("<start>")
    assert hash(good.symbol) == hash(NonTerminal("<start>"))
    assert good.symbol in grammar.rules
    assert good == grammar.parse("2xx")
    # repetition ids
    assert isinstance(constraint, RepetitionBoundsConstraint)
    assert len(good.find_by_origin(constraint.repetition_id)) == 2
    assert constraint.fitness(good).success
    assert not constraint.fitness(bad).success
