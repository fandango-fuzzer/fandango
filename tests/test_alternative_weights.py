import pytest

from fandango.language.grammar.alternative_weights import AlternativeWeights
from fandango.language.grammar.grammar import Grammar, KPath
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
    weights = AlternativeWeights(grammar, 3)
    value = value_in_a_record(grammar)
    alternatives = grammar[VALUE].alternatives
    assert weights.weights(alternatives, value, 0.1) == pytest.approx([1.1, 1.1, 1.1])

    weights.add_covered(k_paths(grammar, 3, "k=;"))
    weights.add_covered(k_paths(grammar, 3, "k=1;"))
    number, quoted, empty = weights.weights(alternatives, value, 0.1)
    assert empty == pytest.approx(0.1)
    assert 0.1 < number < 1.1
    assert quoted == pytest.approx(1.1)


def test_full_coverage_leaves_the_covered_weight():
    grammar = load_grammar()
    weights = AlternativeWeights(grammar, 1)
    weights.add_covered(k_paths(grammar, 1, 'k=0123;k=4567;k=89;k="xy"!;k=;'))
    assert weights.weights(
        grammar[VALUE].alternatives, value_in_a_record(grammar), 0.1
    ) == pytest.approx([0.1, 0.1, 0.1])


def test_failed_picks_decay_the_uncovered_share_until_progress():
    grammar = load_grammar()
    weights = AlternativeWeights(grammar, 3)
    value = value_in_a_record(grammar)
    number, quoted, empty = grammar[VALUE].alternatives

    def decayed() -> list[float]:
        return weights.weights([number, quoted, empty], value, 0.1, 0.5, 0.2)

    weights.choose([quoted], value, 0.1, 0.5, 0.2)
    assert decayed() == pytest.approx([1.1, 0.1 + 0.5, 1.1])
    for _ in range(10):
        weights.choose([quoted], value, 0.1, 0.5, 0.2)
    assert decayed() == pytest.approx([1.1, 0.1 + 0.2, 1.1])

    weights.add_covered(k_paths(grammar, 3, 'k="x";'))
    assert decayed() == pytest.approx(
        weights.weights([number, quoted, empty], value, 0.1)
    )
