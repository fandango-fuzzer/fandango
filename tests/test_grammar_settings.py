import random
from typing import Any, Callable
from fandango.language.grammar import Grammar, Node, NonTerminalNode, TerminalNode
from fandango.language.parse import parse


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
    havoc_on_set: float,
    max_stack_on_set: int | None,
    match_lambda: Callable[[Node], bool],
):
    if match_lambda(node):
        assert node._settings._havoc_probability == havoc_on_set
        assert node._settings._max_stack_pow == max_stack_on_set
    else:
        assert node._settings._havoc_probability == None
        assert node._settings._max_stack_pow == None
    for n in node.children():
        check_node(n, havoc_on_set, max_stack_on_set, match_lambda)


def test_can_parse_grammar_settings():
    grammar = get_grammar([("<start>", {"havoc_probability": 0.5})])
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert gs._selector == "<start>"
    ns = gs._node_settings
    assert ns._havoc_probability == 0.5
    assert ns.havoc_probability == 0.5
    assert ns._max_stack_pow == None
    assert ns.max_stack_pow == 7

    def match_start(node: Node) -> bool:
        return isinstance(node, NonTerminalNode) and node.symbol.name() == "<start>"

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_start)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_start)


def test_assign_to_all_nonterminals():
    grammar = get_grammar(
        [("all_with_type(NonTerminalNode)", {"havoc_probability": 0.5})]
    )
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert gs._selector == "all_with_type(NonTerminalNode)"
    ns = gs._node_settings
    assert ns._havoc_probability == 0.5
    assert ns._max_stack_pow == None

    def match_nts(node: Node) -> bool:
        return isinstance(node, NonTerminalNode)

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_nts)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_nts)


def test_assign_to_all_terminals():
    grammar = get_grammar([("all_with_type(TerminalNode)", {"havoc_probability": 0.5})])
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert gs._selector == "all_with_type(TerminalNode)"
    ns = gs._node_settings
    assert ns._havoc_probability == 0.5
    assert ns._max_stack_pow == None

    def match_ts(node: Node) -> bool:
        return isinstance(node, TerminalNode)

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_ts)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_ts)


def test_assign_to_all():
    grammar = get_grammar([("*", {"havoc_probability": 0.5})])
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert gs._selector == "*"
    assert gs._node_settings._havoc_probability == 0.5

    def match_all(node: Node) -> bool:
        return True

    for node in grammar.rules.values():
        check_node(node, 0.5, None, match_all)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, None, match_all)


def test_multiple_settings_lines():
    grammar = get_grammar(
        [
            ("all_with_type(NonTerminalNode)", {"havoc_probability": 0.5}),
            ("all_with_type(TerminalNode)", {"havoc_probability": 0.5}),
        ]
    )
    gss = grammar._grammar_settings
    assert len(gss) == 2
    for gs in gss:
        assert (
            gs._selector == "all_with_type(NonTerminalNode)"
            or gs._selector == "all_with_type(TerminalNode)"
        )
        assert gs._node_settings._havoc_probability == 0.5
        assert gs._node_settings._max_stack_pow == None

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
                {"havoc_probability": 0.5, "max_stack_pow": 3},
            )
        ]
    )
    gss = grammar._grammar_settings
    assert len(gss) == 1
    gs = gss[0]
    assert gs._selector == "all_with_type(NonTerminalNode)"
    ns = gs._node_settings
    assert ns._havoc_probability == 0.5
    assert ns._max_stack_pow == 3

    def match_nts(node: Node) -> bool:
        return isinstance(node, NonTerminalNode)

    for node in grammar.rules.values():
        check_node(node, 0.5, 3, match_nts)

    for nt in grammar.rules.keys():
        check_node(NonTerminalNode(nt, gss), 0.5, 3, match_nts)
