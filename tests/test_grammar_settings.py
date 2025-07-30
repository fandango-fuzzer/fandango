import random
from typing import Any, Callable
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.grammar_settings import GrammarSetting
from fandango.language.grammar.nodes.node import Node, NODE_SETTINGS_DEFAULTS
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.parse import parse

FLOAT_KEY = next(
    k for k in NODE_SETTINGS_DEFAULTS if isinstance(NODE_SETTINGS_DEFAULTS[k], float)
)
INT_KEY = next(
    k for k in NODE_SETTINGS_DEFAULTS if isinstance(NODE_SETTINGS_DEFAULTS[k], int)
)


def get_grammar(
    selector_probability_pairs: list[tuple[str, dict[str, Any]]],
) -> Grammar:
    raw_spec = f"""
<start> ::= "a" | <b>*
<b> ::= "b"
"""

    for selector, settings in selector_probability_pairs:
        # try both '=' and ' ' as separators
        oddness = random.choice([0, 1])
        kv_pairs = " ".join(
            [
                f"{k}{'=' if i % 2 == oddness else ' '}{v}"
                for i, (k, v) in enumerate(settings.items())
            ]
        )
        raw_spec += f"""setting {selector} {kv_pairs}
"""
    grammar, constraints = parse(raw_spec, use_cache=False, use_stdlib=False)
    assert grammar is not None
    assert constraints is not None and len(constraints) == 0
    return grammar


def check_node(
    node: Node,
    float_key_on_set: float,
    int_key_on_set: int | None,
    match_lambda: Callable[[Node], bool],
):
    if match_lambda(node):
        assert node._settings._settings[FLOAT_KEY] == float_key_on_set
        if int_key_on_set is not None:
            assert node._settings._settings[INT_KEY] == int_key_on_set
        else:
            assert INT_KEY not in node._settings._settings
    else:
        assert FLOAT_KEY not in node._settings._settings
        assert INT_KEY not in node._settings._settings
    for n in node.children():
        check_node(n, float_key_on_set, int_key_on_set, match_lambda)


def test_can_parse_grammar_settings():
    grammar = get_grammar([("<start>", {FLOAT_KEY: 0.5})])
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert isinstance(gs, GrammarSetting)
    assert gs._selector == "<start>"
    ns = gs._node_settings
    assert ns._settings[FLOAT_KEY] == 0.5
    assert ns.get(FLOAT_KEY) == 0.5
    assert INT_KEY not in ns._settings
    assert ns.get(INT_KEY) == NODE_SETTINGS_DEFAULTS[INT_KEY]

    def match_start(node: Node) -> bool:
        return isinstance(node, NonTerminalNode) and node.symbol.name() == "<start>"

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_start)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_start)


def test_assign_to_all_nonterminals():
    grammar = get_grammar([("all_with_type(NonTerminalNode)", {FLOAT_KEY: 0.5})])
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert isinstance(gs, GrammarSetting)
    assert gs._selector == "all_with_type(NonTerminalNode)"
    ns = gs._node_settings
    assert ns._settings[FLOAT_KEY] == 0.5
    assert ns.get(FLOAT_KEY) == 0.5
    assert INT_KEY not in ns._settings
    assert ns.get(INT_KEY) == NODE_SETTINGS_DEFAULTS[INT_KEY]

    def match_nts(node: Node) -> bool:
        return isinstance(node, NonTerminalNode)

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_nts)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_nts)


def test_assign_to_all_terminals():
    grammar = get_grammar([("all_with_type(TerminalNode)", {FLOAT_KEY: 0.5})])
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert isinstance(gs, GrammarSetting)
    assert gs._selector == "all_with_type(TerminalNode)"
    ns = gs._node_settings
    assert ns._settings[FLOAT_KEY] == 0.5
    assert ns.get(FLOAT_KEY) == 0.5
    assert INT_KEY not in ns._settings
    assert ns.get(INT_KEY) == NODE_SETTINGS_DEFAULTS[INT_KEY]

    def match_ts(node: Node) -> bool:
        return isinstance(node, TerminalNode)

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_ts)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_ts)


def test_assign_to_all():
    grammar = get_grammar([("*", {FLOAT_KEY: 0.5})])
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert isinstance(gs, GrammarSetting)
    assert gs._selector == "*"
    assert gs._node_settings._settings[FLOAT_KEY] == 0.5
    assert gs._node_settings.get(FLOAT_KEY) == 0.5
    assert INT_KEY not in gs._node_settings._settings
    assert gs._node_settings.get(INT_KEY) == NODE_SETTINGS_DEFAULTS[INT_KEY]

    def match_all(node: Node) -> bool:
        return True

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_all)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_all)


def test_multiple_settings_lines():
    grammar = get_grammar(
        [
            ("all_with_type(NonTerminalNode)", {FLOAT_KEY: 0.5}),
            ("all_with_type(TerminalNode)", {FLOAT_KEY: 0.5}),
        ]
    )
    gss = grammar._grammar_settings
    assert len(gss) == 2
    for gs in gss:
        assert isinstance(gs, GrammarSetting)
        assert (
            gs._selector == "all_with_type(NonTerminalNode)"
            or gs._selector == "all_with_type(TerminalNode)"
        )
        assert gs._node_settings._settings[FLOAT_KEY] == 0.5
        assert INT_KEY not in gs._node_settings._settings

    def match_ts_and_nts(node: Node) -> bool:
        return isinstance(node, NonTerminalNode) or isinstance(node, TerminalNode)

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_ts_and_nts)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_ts_and_nts)


def test_multiple_key_value_pairs():
    grammar = get_grammar(
        [
            (
                "all_with_type(NonTerminalNode)",
                {FLOAT_KEY: 0.5, INT_KEY: 3},
            )
        ]
    )
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert isinstance(gs, GrammarSetting)
    assert gs._selector == "all_with_type(NonTerminalNode)"
    ns = gs._node_settings
    assert ns._settings[FLOAT_KEY] == 0.5
    assert ns._settings[INT_KEY] == 3
    assert ns.get(FLOAT_KEY) == 0.5
    assert ns.get(INT_KEY) == 3

    def match_nts(node: Node) -> bool:
        return isinstance(node, NonTerminalNode)

    for node in grammar.rules.values():
        check_node(node, 0.5, 3, match_nts)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, 3, match_nts)
