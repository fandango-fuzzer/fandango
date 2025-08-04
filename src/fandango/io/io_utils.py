from itertools import groupby

from fandango.language.tree import DerivationTree
from fandango.language import NonTerminal, Grammar


def compute_nt_coverage_score(grammar: Grammar, trees: list[DerivationTree], k: int) -> dict[NonTerminal, float]:
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
    for non_terminal, messages in messages_by_nt.items():
        nt_coverage[non_terminal] = grammar.compute_kpath_coverage(messages, k)
    return nt_coverage