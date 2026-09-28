from fandango.api import Fandango
from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.selection.coverage_tracker import CoverageTracker
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree

from .utils import RESOURCES_ROOT

IO_GRAMMAR = "ambiguous_io.fan"
GOAL = CoverageGoal.STATE_INPUTS


def packet_selector_and_tree(grammar_file):
    with open(RESOURCES_ROOT / grammar_file) as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    tree = fandango.fuzz(mode=FuzzingMode.IO, population_size=1)[0]
    assert isinstance(fandango.fandango, ProtocolAlgorithm)
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
    k = selector._coverage_tracker._diversity_k
    all_paths = selector.grammar.generate_all_k_paths(
        k=k,
        non_terminal=selector.start_symbol,
        coverage_goal=GOAL,
        input_parties=selector._input_parties(),
    )
    covered_paths = set()
    for tree in trees:
        covered_paths |= selector.grammar._extract_k_paths_from_tree(
            tree, k, coverage_goal=GOAL, input_parties=selector._input_parties()
        )
    return all_paths - covered_paths


def bruteforce_scores(selector, trees):
    messages_by_nt: dict[Symbol, list[DerivationTree]] = {}
    for tree in trees:
        for record in tree.protocol_msgs():
            messages_by_nt.setdefault(record.msg.symbol, []).append(record.msg)
    scores = {}
    for symbol in {message.symbol for message in selector._model.protocol_msg_symbols}:
        if symbol not in messages_by_nt:
            scores[symbol] = 0.0
        else:
            k = selector._coverage_tracker._diversity_k
            all_paths = selector.grammar.generate_all_k_paths(k=k, non_terminal=symbol)
            covered_paths = set()
            for message in messages_by_nt[symbol]:
                covered_paths |= selector.grammar._extract_k_paths_from_tree(message, k)
            scores[symbol] = len(covered_paths) / len(all_paths) if all_paths else 1.0
    return list(sorted(scores.items(), key=lambda x: (x[1], x[0].name())))


def test_folded_uncovered_matches_bruteforce():
    selector, tree = packet_selector_and_tree(IO_GRAMMAR)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    assert set(tracker.uncovered_paths()) == bruteforce_uncovered(
        selector, [tree, history]
    )


def test_folded_scores_match_bruteforce():
    selector, tree = packet_selector_and_tree(IO_GRAMMAR)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    assert tracker.coverage_scores() == bruteforce_scores(selector, [tree, history])


def test_folded_percent_matches_bruteforce():
    selector, tree = packet_selector_and_tree(IO_GRAMMAR)
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


def test_repeated_fold_is_idempotent():
    selector, tree = packet_selector_and_tree(IO_GRAMMAR)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    tracker.add_completed_tree(tree)
    assert set(tracker.uncovered_paths()) == bruteforce_uncovered(
        selector, [tree, history]
    )


def test_reset_clears_basis():
    selector, tree = packet_selector_and_tree(IO_GRAMMAR)
    history = DerivationTree(NonTerminal("<start>"))
    tracker = make_tracker(selector, history)
    tracker.add_completed_tree(tree)
    tracker.reset()
    assert set(tracker.uncovered_paths()) == bruteforce_uncovered(selector, [history])
    assert tracker.coverage_scores() == bruteforce_scores(selector, [history])


def test_compute_refreshes_coverage():
    selector, running = packet_selector_and_tree("minimal_io.fan")
    selector.reset_coverage()
    selector.set_coverage_goal(GOAL)
    tracker = selector.coverage_tracker
    empty_history = DerivationTree(NonTerminal("<start>"))

    selector.compute(empty_history)
    scores_before = tracker.coverage_scores()
    uncovered_before = set(tracker.uncovered_paths())
    assert scores_before == bruteforce_scores(selector, [empty_history])
    assert uncovered_before == bruteforce_uncovered(selector, [empty_history])

    selector.compute(running)
    assert tracker.coverage_scores() == bruteforce_scores(selector, [running])
    assert set(tracker.uncovered_paths()) == bruteforce_uncovered(selector, [running])
    assert tracker.coverage_scores() != scores_before
    assert set(tracker.uncovered_paths()) != uncovered_before
