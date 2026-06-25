import pytest

from fandango.api import Fandango
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.selection.coverage_tracker import CoverageTracker
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

from .utils import RESOURCES_ROOT

IO_GRAMMARS = ["minimal_io.fan", "ambiguous_io.fan"]
GOAL = CoverageGoal.STATE_INPUTS


def packet_selector_and_tree(grammar_file):
    with open(RESOURCES_ROOT / grammar_file) as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    tree = fandango.fuzz(mode=FuzzingMode.IO, population_size=1)[0]
    return fandango.fandango._packet_selector, tree


def make_tracker(selector, history):
    return CoverageTracker(
        selector.grammar,
        selector._coverage_tracker._diversity_k,
        selector._model,
        selector.start_symbol,
        selector._input_parties,
        lambda: history,
        GOAL,
    )


def bruteforce_uncovered(selector, trees):
    return set(
        selector.grammar.get_uncovered_k_paths(
            trees,
            selector._coverage_tracker._diversity_k,
            selector.start_symbol,
            coverage_goal=GOAL,
            input_parties=selector._input_parties(),
        )
    )


def bruteforce_scores(selector, trees):
    messages_by_nt = selector._model.group_messages_by_nt(trees)
    scores = {}
    for symbol in selector._model.state_grammar_symbols:
        if symbol not in messages_by_nt:
            scores[symbol] = 0.0
        else:
            scores[symbol] = selector.grammar.compute_kpath_coverage(
                messages_by_nt[symbol],
                selector._coverage_tracker._diversity_k,
                symbol
            )
    return list(sorted(scores.items(), key=lambda x: (x[1], x[0].name())))


@pytest.mark.parametrize("grammar_file", IO_GRAMMARS)
def test_folded_uncovered_matches_bruteforce(grammar_file):
    selector, tree = packet_selector_and_tree(grammar_file)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    assert set(tracker.uncovered_paths()) == bruteforce_uncovered(
        selector, [tree, history]
    )


@pytest.mark.parametrize("grammar_file", IO_GRAMMARS)
def test_folded_scores_match_bruteforce(grammar_file):
    selector, tree = packet_selector_and_tree(grammar_file)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    assert tracker.coverage_scores() == bruteforce_scores(selector, [tree, history])


@pytest.mark.parametrize("grammar_file", IO_GRAMMARS)
def test_folded_percent_matches_bruteforce(grammar_file):
    selector, tree = packet_selector_and_tree(grammar_file)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    uncovered = bruteforce_uncovered(selector, [tree, history])
    if len(uncovered) == 0:
        expected = 1.0
    else:
        all_paths = selector.grammar.generate_all_k_paths(
            k=selector._coverage_tracker._diversity_k,
            non_terminal=selector.start_symbol,
            coverage_goal=GOAL,
            input_parties=selector._input_parties(),
        )
        expected = 1.0 - (len(uncovered) / len(all_paths))
    assert tracker.coverage_percent() == expected


@pytest.mark.parametrize("grammar_file", IO_GRAMMARS)
def test_repeated_fold_is_idempotent(grammar_file):
    selector, tree = packet_selector_and_tree(grammar_file)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    tracker.add_completed_tree(tree)
    assert set(tracker.uncovered_paths()) == bruteforce_uncovered(
        selector, [tree, history]
    )


@pytest.mark.parametrize("grammar_file", IO_GRAMMARS)
def test_reset_clears_basis(grammar_file):
    selector, tree = packet_selector_and_tree(grammar_file)
    tracker = make_tracker(selector, DerivationTree(NonTerminal("<start>")))
    tracker.add_completed_tree(tree)
    tracker.reset()
    assert tracker._whole_covered == set()
    assert tracker._message_covered == {False: {}, True: {}}
