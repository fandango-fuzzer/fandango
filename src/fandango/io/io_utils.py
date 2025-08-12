from typing import Optional

from fandango.io.navigation.packetforecaster import ForecastingResult, ForcastingPacket
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.tree import DerivationTree
from fandango.language.symbols.symbol import Symbol
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols.non_terminal import NonTerminal


def compute_message_coverage_score(
    grammar: Grammar, trees: list[DerivationTree], k: int
) -> dict[NonTerminal, float]:
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
        nt_coverage[non_terminal] = grammar.compute_kpath_coverage(
            messages_by_nt[non_terminal], k, non_terminal
        )
    return nt_coverage


def get_guide_to_end_packet(
    navigator: PacketNavigator, history_tree: DerivationTree, forecast: ForecastingResult, msg_parties: list[str]
) -> Optional[ForcastingPacket]:
    path = navigator.astar_search_end(history_tree)
    if len(path) > 0:
        sender, receiver, next_nt = path[0]
        if sender in msg_parties and next_nt in forecast[sender].nt_to_packet:
            return forecast[sender].nt_to_packet[next_nt]
    return None


def select_next_packet(
    forecast: ForecastingResult,
    msg_parties: list[str],
    grammar: Grammar,
    parst_io_derivations: list[DerivationTree],
    history_tree: DerivationTree,
):
    fuzzable_packets = []
    max_messages_per_tree = 50
    navigator = PacketNavigator(grammar, NonTerminal("<start>"))
    if len(history_tree.protocol_msgs()) > max_messages_per_tree:
        print(
            f"Current tree contains more then {max_messages_per_tree} messages. Guiding to end of tree."
        )
        fuzzable_packets.append(get_guide_to_end_packet(navigator, history_tree, forecast, msg_parties))
        return fuzzable_packets
    # Select next packet to send by computing guiding generator to underexplored areas of the grammar
    all_derivations = list(parst_io_derivations)
    all_derivations.append(history_tree)
    coverage_scores: dict[NonTerminal, float] = compute_message_coverage_score(
        grammar, all_derivations, 2
    )
    scores_sorted = list(
        sorted(coverage_scores.items(), key=lambda x: (x[1], x[0].name()))
    )
    if len(scores_sorted) > 0 and scores_sorted[0][1] == 1.0:
        print("Full coverage reached. Guiding to end of tree.")
        fuzzable_packets.append(get_guide_to_end_packet(navigator, history_tree, forecast, msg_parties))
        return fuzzable_packets

    for target_nt, coverage_score in scores_sorted:
        path = navigator.astar_tree(history_tree, target_nt)
        if path is None:
            # We can't find a path to this non-terminal. That means we can't reach it without starting a new tree.
            # So we try to finish this tree ASAP by selecting the non-terminal with the lowest distance to completion.
            print(
                f"No path found for target {target_nt} with score {coverage_score}. Guiding to end of tree."
            )
            fuzzable_packets.append(
                get_guide_to_end_packet(navigator, history_tree, forecast, msg_parties)
            )
            break
        else:
            print(f"Guiding to target {target_nt} with score {coverage_score}")
            sender, receiver, next_nt = path[0]
            if sender in msg_parties and next_nt in forecast[sender].nt_to_packet:
                fuzzable_packets.append(forecast[sender].nt_to_packet[next_nt])
                break
    if len(fuzzable_packets) == 0:
        fuzzable_packets.append(get_guide_to_end_packet(navigator, history_tree, forecast, msg_parties))
    return fuzzable_packets
