from fandango.api import Fandango
from fandango.io.coverage_filter import PacketCoverageFilter
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols import NonTerminal

from .utils import RESOURCES_ROOT


def filter_and_tree():
    with open(RESOURCES_ROOT / "minimal_io.fan") as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    tree = fandango.fuzz(mode=FuzzingMode.IO, population_size=1)[0]
    diversity_k = fandango.fandango._packet_algorithm.diversity_k
    return PacketCoverageFilter(diversity_k, fandango.grammar), tree


def bruteforce_msgs(trees, packet_type=None):
    msgs = set()
    for tree in trees:
        for record in tree.protocol_msgs():
            msgs.add(record.msg)
    if packet_type is None:
        return msgs
    return {
        m
        for m in msgs
        if isinstance(m.symbol, NonTerminal)
        and PacketNonTerminal(m.sender, m.recipient, m.symbol) == packet_type
    }


def test_get_past_msgs_matches_bruteforce():
    flt, tree = filter_and_tree()
    flt.add_completed_tree(tree)
    flt.set_current_tree(tree)
    assert flt.get_past_msgs() == bruteforce_msgs([tree])


def test_get_past_msgs_filters_by_type():
    flt, tree = filter_and_tree()
    flt.add_completed_tree(tree)
    record = tree.protocol_msgs()[0]
    packet_type = PacketNonTerminal(record.sender, record.recipient, record.msg.symbol)
    assert flt.get_past_msgs(packet_type) == bruteforce_msgs([tree], packet_type)


def test_reset_clears():
    flt, tree = filter_and_tree()
    flt.add_completed_tree(tree)
    flt.set_current_tree(tree)
    flt.reset()
    assert flt.get_past_msgs() == set()
