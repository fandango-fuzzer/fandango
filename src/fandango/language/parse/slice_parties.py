from fandango.errors import FandangoValueError
from fandango.language import NonTerminal
from fandango.language.grammar import closest_match
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.node_visitors.packet_truncator import PacketTruncator


def slice_parties(
    grammar: Grammar, parties: set[str], ignore_receivers: bool = False
) -> None:
    is_first = True
    deleted_keys: set[NonTerminal] = set()
    while len(deleted_keys) != 0 or is_first:
        keys_to_delete = set(deleted_keys)
        deleted_keys = set()
        is_first = False
        for nt in set(grammar.rules.keys()):
            delete_rule = PacketTruncator(
                grammar,
                parties,
                ignore_receivers=ignore_receivers,
                delete_rules=keys_to_delete,
            ).visit(grammar.rules[nt])
            if delete_rule:
                deleted_keys.add(nt)
                del grammar.rules[nt]
