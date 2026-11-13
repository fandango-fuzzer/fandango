import pytest

from fandango.language.grammar.alternative_weights import AlternativeWeights
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.node import Node
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

from .utils import RESOURCES_ROOT

VALUE = NonTerminal("<value>")


def load_grammar() -> Grammar:
    """`<value> ::= <number> | <quoted> | <empty>` inside `<record>`s."""
    with open(RESOURCES_ROOT / "grammar_with_all_nodes.fan") as spec:
        grammar, _ = parse(spec, use_stdlib=False, use_cache=False)
    assert grammar is not None
    return grammar


def value_alternatives(grammar: Grammar) -> list[Node]:
    rule = grammar[VALUE]
    assert isinstance(rule, Alternative)
    return rule.alternatives


def value_in_a_record(grammar: Grammar) -> DerivationTree:
    tree = grammar.parse("k=;")
    assert tree is not None
    return next(tree.find_subtrees(VALUE))


def k_paths(grammar: Grammar, k: int, word: str) -> set[KPath]:
    tree = grammar.parse(word)
    assert tree is not None
    return grammar._extract_k_paths_from_tree(tree, k)


def test_covering_lowers_the_weights_of_the_covered_alternatives():
    grammar = load_grammar()
    weights = AlternativeWeights(grammar, 3, covered_weight=0.1)
    value = value_in_a_record(grammar)
    alternatives = value_alternatives(grammar)
    assert weights.weights(alternatives, value) == pytest.approx([1.1, 1.1, 1.1])

    weights.add_covered(k_paths(grammar, 3, "k=;"))
    weights.add_covered(k_paths(grammar, 3, "k=1;"))
    number, quoted, empty = weights.weights(alternatives, value)
    assert empty == pytest.approx(0.1)
    assert 0.1 < number < 1.1
    assert quoted == pytest.approx(1.1)


def test_full_coverage_leaves_the_covered_weight():
    grammar = load_grammar()
    weights = AlternativeWeights(grammar, 1, covered_weight=0.1)
    weights.add_covered(k_paths(grammar, 1, 'k=0123;k=4567;k=89;k="xy"!;k=;'))
    assert weights.weights(
        value_alternatives(grammar), value_in_a_record(grammar)
    ) == pytest.approx([0.1, 0.1, 0.1])


def test_failed_picks_decay_the_uncovered_share_until_progress():
    grammar = load_grammar()
    weights = AlternativeWeights(
        grammar, 3, covered_weight=0.1, failure_decay=0.5, decay_floor=0.2
    )
    undecayed = AlternativeWeights(grammar, 3, covered_weight=0.1, failure_decay=1.0)
    value = value_in_a_record(grammar)
    alternatives = [number, quoted, empty] = value_alternatives(grammar)

    weights.choose([quoted], value)
    assert weights.weights(alternatives, value) == pytest.approx([1.1, 0.1 + 0.5, 1.1])
    for _ in range(10):
        weights.choose([quoted], value)
    assert weights.weights(alternatives, value) == pytest.approx([1.1, 0.1 + 0.2, 1.1])

    covered = k_paths(grammar, 3, 'k="x";')
    weights.add_covered(covered)
    undecayed.add_covered(covered)
    assert weights.weights(alternatives, value) == pytest.approx(
        undecayed.weights(alternatives, value)
    )
