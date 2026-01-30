from typing import Any, Optional
from fandango.errors import FandangoError, FandangoValueError
from fandango.io import FandangoIO, FandangoParty
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.node_visitors.message_nesting_detector import (
    MessageNestingDetector,
)
from fandango.language.grammar.node_visitors.node_replacer import NodeReplacer
from fandango.language.grammar.node_visitors.packet_truncator import PacketTruncator
from fandango.language.grammar.node_visitors.symbol_finder import SymbolFinder
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.logger import LOGGER


def init_io(
    global_env: dict[str, Any],
    local_env: dict[str, Any],
    grammar: Grammar,
    start_symbol: str,
) -> None:
    # Prepare for interaction
    if "FandangoIO" not in global_env.keys():
        exec("FandangoIO.instance()", global_env, local_env)
    io_instance: FandangoIO = global_env["FandangoIO"].instance()

    assign_implicit_party(grammar, "StdOut")
    init_msg_parties(grammar, io_instance)
    remap_to_std_party(grammar, io_instance)
    init_msg_parties(grammar, io_instance)

    # Detect illegally nested data packets.
    rir_detector = MessageNestingDetector(grammar)
    rir_detector.fail_on_nested_packet(NonTerminal(start_symbol))
    fail_on_party_in_generator(grammar)

    truncate_invisible_packets(grammar, io_instance)


def fail_on_party_in_generator(grammar: Grammar) -> None:
    for nt, node in grammar.rules.items():
        if nt not in grammar.generators:
            continue
        found_node = is_party_reachable(grammar, node)
        if found_node is not None:
            raise ValueError(
                f"{found_node} contains a party or recipient and is generated using the generator on {nt}. This is not allowed!"
            )

    for nt in grammar.generators.keys():
        dependencies: set[NonTerminal] = grammar.generator_dependencies(nt)
        for dep_nt in dependencies:
            found_node = is_party_reachable(grammar, grammar[dep_nt])
            if found_node is not None:
                raise ValueError(
                    f"{found_node} contains a party or recipient and is a parameter for the generator of {nt}. This is not allowed!"
                )


def is_party_reachable(grammar: Grammar, node: Node) -> Optional[Node]:
    seen_nt_nodes = set()
    symbol_finder = SymbolFinder()
    symbol_finder.visit(node)
    nt_node_queue: set[NonTerminalNode] = set(symbol_finder.nonTerminalNodes)
    while len(nt_node_queue) != 0:
        current_node = nt_node_queue.pop()
        if current_node.sender is not None or current_node.recipient is not None:
            return current_node

        seen_nt_nodes.add(current_node)
        symbol_finder = SymbolFinder()
        symbol_finder.visit(grammar[current_node.symbol])
        for next_nt in symbol_finder.nonTerminalNodes:
            if next_nt not in seen_nt_nodes:
                nt_node_queue.add(next_nt)
    return None


def init_msg_parties(
    grammar: Grammar, io_instance: FandangoIO, ignore_existing: bool = True
) -> None:
    party_names = set()
    grammar_msg_parties = grammar.msg_parties(include_recipients=True)
    global_env, local_env = grammar.get_spec_env()

    # Initialize FandangoParty instances
    for key in global_env.keys():
        if key in grammar_msg_parties:
            the_type = global_env[key]
            if not isinstance(the_type, type):
                continue
            if FandangoParty in the_type.__mro__:
                party_names.add(key)
    # Call constructor
    for party in party_names:
        if party in io_instance.parties.keys() and ignore_existing:
            continue
        exec(f"{party}()", global_env, local_env)
        grammar_msg_parties.remove(party)


# Assign STD party to all parties which have no party-class defined.
def remap_to_std_party(grammar: Grammar, io_instance: FandangoIO) -> None:
    remapped_parties = set()
    unknown_recipients = set()
    for symbol in grammar.rules.keys():
        symbol_finder = SymbolFinder()
        symbol_finder.visit(grammar.rules[symbol])
        non_terminals: list[NonTerminalNode] = symbol_finder.nonTerminalNodes

        for nt in non_terminals:
            if nt.sender is not None:
                if nt.sender not in io_instance.parties.keys():
                    remapped_parties.add(nt.sender)
                    nt.sender = "StdOut"
            if nt.recipient is not None:
                if nt.recipient not in io_instance.parties.keys():
                    unknown_recipients.add(nt.recipient)

    for name in remapped_parties:
        LOGGER.warning(f"Party {name!r} unspecified; will use 'StdOut' instead")
    if unknown_recipients:
        raise FandangoValueError(f"Recipients {unknown_recipients!r} unspecified")


def truncate_invisible_packets(grammar: Grammar, io_instance: FandangoIO) -> None:
    keep_parties = grammar.msg_parties(include_recipients=True)
    io_instance.parties.keys()
    for existing_party in list(keep_parties):
        if not io_instance.parties[existing_party].is_fuzzer_controlled():
            keep_parties.remove(existing_party)

    for nt in grammar.rules.keys():
        PacketTruncator(grammar, keep_parties).visit(grammar.rules[nt])


def assign_implicit_party(grammar: Grammar, implicit_party: str) -> None:
    seen_nts: set[NonTerminal] = set()
    seen_nts.add(NonTerminal("<start>"))
    processed_nts: set[NonTerminal] = set()
    unprocessed_nts: set[NonTerminal] = seen_nts.difference(processed_nts)

    while len(unprocessed_nts) > 0:
        current_symbol = unprocessed_nts.pop()
        current_node = grammar.rules[current_symbol]

        symbol_finder = SymbolFinder()
        symbol_finder.visit(current_node)
        rule_nts = [x for x in symbol_finder.nonTerminalNodes if x not in processed_nts]

        if current_node in rule_nts and not isinstance(current_node, NonTerminalNode):
            raise FandangoError("This should never happen")
        child_party: set[str] = set()

        for c_node in rule_nts:
            child_party |= c_node.msg_parties(include_recipients=False)

        if len(child_party) == 0:
            processed_nts.add(current_symbol)
            unprocessed_nts = seen_nts.difference(processed_nts)
            continue
        for c_node in rule_nts:
            seen_nts.add(c_node.symbol)
            if len(c_node.msg_parties(include_recipients=False)) != 0:
                continue
            c_node.sender = implicit_party
        for t_node in symbol_finder.terminalNodes:
            terminal_id = 0
            rule_nt = NonTerminal(f"<_terminal:{terminal_id}>")
            while rule_nt in grammar.rules:
                terminal_id += 1
                rule_nt = NonTerminal(f"<_terminal:{terminal_id}>")
            n_node = NonTerminalNode(
                rule_nt,
                grammar.grammar_settings,
                implicit_party,
            )
            NodeReplacer(t_node, n_node).visit(current_node)
            grammar.rules[rule_nt] = t_node

        processed_nts.add(current_symbol)
        unprocessed_nts = seen_nts.difference(processed_nts)
