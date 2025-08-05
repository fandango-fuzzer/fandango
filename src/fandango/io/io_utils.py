from itertools import groupby
from typing import Optional

from fandango.io.navigation.packetforecaster import ForecastingResult, ForcastingPacket
from fandango.language.tree import DerivationTree
from fandango.language import NonTerminal, Grammar


def compute_message_coverage_score(grammar: Grammar, trees: list[DerivationTree], k: int) -> dict[NonTerminal, float]:
    """
    Computes the coverage score for each NonTerminal in the given DerivationTrees.
    The score is the ratio of the number of trees containing the NonTerminal to the total number of trees.

    :param grammar: The Grammar to use for computing coverage.
    :param trees: List of DerivationTrees to analyze.
    :param k: The k-path length for coverage computation.
    :return: Dictionary mapping NonTerminals to their coverage scores.
    """
    messages: list[DerivationTree] = []
    for tree in trees:
        messages.extend(map(lambda x: x.msg, tree.protocol_msgs()))
    messages_by_nt = {}
    for msg in messages:
        messages_by_nt.setdefault(msg.symbol, []).append(msg)
    nt_coverage = {}
    for non_terminal in grammar.get_protocol_messages():
        if non_terminal not in messages_by_nt:
            nt_coverage[non_terminal] = 0.0
            continue
        nt_coverage[non_terminal] = grammar.compute_kpath_coverage(messages, k, non_terminal)
    return nt_coverage

def get_guide_to_end_packet(forecast: ForecastingResult, fuzzer_parties: list[str]) -> Optional[ForcastingPacket]:
    current_selection = None
    for sender in fuzzer_parties:
        for nt, packet in forecast[sender].nt_to_packet.items():
            if current_selection is None:
                current_selection = packet
                continue
            if packet.node.distance_to_completion < current_selection.node.distance_to_completion:
                current_selection = packet
    return current_selection