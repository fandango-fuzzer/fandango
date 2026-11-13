#!/usr/bin/env pytest
from typing import Any

from fandango.language.parse.parse import parse

SPEC = """<start> ::= <n> <item>{int(<n>)}
<n> ::= "1" | "2" | "3"
<item> ::= ("a" <b> | <b> "a")* | "z"
<b> ::= "b"
"""


def load(spec: Any = SPEC) -> tuple[Any, Any]:
    grammar, constraints = parse(spec, use_stdlib=False, use_cache=False, check=False)
    assert grammar is not None
    return grammar, constraints


def ids(grammar: Any) -> list[str]:
    found = []

    def walk(node: Any) -> None:
        if getattr(node, "id", ""):
            found.append(node.id)
        for child in node.children():
            walk(child)

    for rule in grammar.rules.values():
        walk(rule)
    return found


def test_ids_only_depend_on_contents(tmp_path, monkeypatch):
    (tmp_path / "sub").mkdir()
    (tmp_path / "demo.fan").write_text(SPEC)
    (tmp_path / "sub" / "other.fan").write_text(SPEC)
    monkeypatch.chdir(tmp_path)
    loaded = []
    for name in ("demo.fan", "./demo.fan", str(tmp_path / "demo.fan"), "sub/other.fan"):
        with open(name) as fd:
            loaded.append(load(fd))
    (grammar, constraints), *others = loaded

    assert len(set(ids(grammar))) == len(ids(grammar)) > 0
    for other_grammar, other_constraints in others:
        assert ids(other_grammar) == ids(grammar)
        # The constraint for the computed bound finds its repetition in a tree
        # made with the other grammar
        tree = grammar.parse("2zab", "<start>")
        assert tree is not None
        (bounds,) = other_constraints
        assert len(bounds.group_by_repetition_id(tree.children)) == 1


def test_included_files_have_their_own_ids(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "d.fan").write_text('<digit> ::= "1" | "2"\n')
    (tmp_path / "a.fan").write_text("include('d.fan')\n<start> ::= <digit> | \"x\"\n")
    (tmp_path / "b.fan").write_text("include('d.fan')\n<b> ::= <digit>* | \"y\"\n")
    (tmp_path / "top.fan").write_text(
        "include('a.fan')\ninclude('b.fan')\n<top> ::= <start> <b>\n"
    )
    grammars = {}
    for name in ("a.fan", "b.fan", "top.fan"):
        with open(name) as fd:
            grammars[name], _ = load(fd)
    a, b, top = grammars["a.fan"], grammars["b.fan"], grammars["top.fan"]

    # the included file has the same ids wherever, and however often, it is included
    assert a["<digit>"].id == b["<digit>"].id == top["<digit>"].id
    assert a["<digit>"].id.startswith("alternative:1_")
    # numbering in a file does not depend on what it includes
    assert a["<start>"].id.startswith("alternative:1_")
    assert a["<start>"].id == top["<start>"].id
    assert a["<start>"].id != a["<digit>"].id
