from fandango.api import Fandango
from fandango.io.coverage_filter import PacketCoverageFilter
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.selection.coverage_tracker import CoverageTracker
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.tree import DerivationTree

from .utils import RESOURCES_ROOT

START = NonTerminal("<start>")
DIVERSITY_K = 5


def note(sender, recipient, text):
    return DerivationTree(
        NonTerminal("<note>"),
        [DerivationTree(Terminal(f"{text}\n"))],
        sender=sender,
        recipient=recipient,
    )


def session(*exchanges):
    return DerivationTree(
        START,
        [
            DerivationTree(
                NonTerminal("<exchange>"),
                [note("Fuzzer", "Extern", sent)]
                + ([note("Extern", "Fuzzer", reply)] if reply else []),
            )
            for sent, reply in exchanges
        ],
    )


def tracker_after(finished_session):
    grammar = Fandango(
        (RESOURCES_ROOT / "echo_io.fan").read_text(), use_stdlib=False, use_cache=False
    ).grammar
    empty_history = DerivationTree(START)
    tracker = CoverageTracker(
        grammar,
        DIVERSITY_K,
        ProtocolModel(grammar, START),
        START,
        lambda: {"Fuzzer"},
        lambda: empty_history,
        CoverageGoal.STATE_INPUTS,
    )
    tracker.add_completed_tree(finished_session)
    return tracker


def filter_after(finished_session):
    return PacketCoverageFilter(tracker_after(finished_session))


def test_new_k_path_passes():
    packet_filter = filter_after(session(("A", "C")))
    assert packet_filter.filter(session(("B", None))) is not None


def test_known_k_path_is_held_back():
    packet_filter = filter_after(session(("A", "C")))
    candidate = session(("A", None))
    assert packet_filter.filter(candidate) is None
    assert candidate in packet_filter.hold_back_solutions_by_msg_hash.values()


def test_other_party_does_not_count():
    packet_filter = filter_after(session(("A", "C")))
    assert packet_filter.filter(session(("C", None))) is not None


def test_unreachable_k_paths_end_holding_back():
    packet_filter = filter_after(session(("A", "C")))
    candidate = session(("A", None))
    assert packet_filter.filter(candidate) is None
    packet_filter.mark_uncovered_k_paths_unreachable()
    assert packet_filter.filter(candidate) is not None


def test_unreachable_k_path_still_counts_when_hit():
    packet_filter = filter_after(session(("A", "C")))
    packet_filter.filter(session(("A", None)))
    packet_filter.mark_uncovered_k_paths_unreachable()
    assert packet_filter.filter(session(("B", None))) is not None
