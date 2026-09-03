import random
import time
from collections.abc import Generator

from fandango.errors import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.io import FandangoIO
from fandango.io.navigation.graph.packetforecaster import (
    ForecastingPacket,
    ForecastingResult,
)
from fandango.language import DerivationTree, Grammar, NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.parser.iterative_parser import IterativeParser


def parse_next_remote_packet(
    grammar: Grammar,
    forecast: ForecastingResult,
    io_instance: FandangoIO,
    *,
    wait_for_completion_time: float = 1,
) -> Generator[tuple[ForecastingPacket, DerivationTree], None, None]:
    """
    Parse the next packet a remote party sent, as one of the forecast
    non-terminals.

    `wait_for_completion_time` bounds the wait once a packet has parsed: a
    candidate that can still grow may yet become a longer packet, so a
    complete parse is only handed back after no more data has arrived for
    that long. It is paid per packet, so a caller that knows its packets
    cannot grow can turn it down.
    """
    if len(io_instance.get_received_msgs()) == 0:
        return None

    wait_for_expected_party_time = 10
    received_parties = list(map(lambda x: x[0], io_instance.get_received_msgs()))
    start_time = time.time()
    while not forecast.contains_any_party(received_parties):
        if time.time() - start_time > wait_for_expected_party_time:
            if len(received_parties) == 0:
                raise FandangoFailedError(
                    "Timeout while waiting for message. No message has been received."
                )
            else:
                raise FandangoValueError(
                    "Unexpected party sent message. Expected: "
                    + " | ".join(forecast.get_msg_parties())
                    + f". Received: {set(received_parties)}."
                    + f" Messages: {io_instance.get_full_fragments()}"
                )
        time.sleep(0.025)
        received_parties = list(map(lambda x: x[0], io_instance.get_received_msgs()))

    msg_sender = None
    # We might have received messages from different parties. Select a party that sent a message and is
    # in the current forecast.
    for msg_sender, _msg_recipient, _ in io_instance.get_received_msgs():
        if msg_sender in forecast.get_msg_parties():
            break

    assert msg_sender is not None

    forecast_non_terminals = forecast[msg_sender]
    available_non_terminals = set(forecast_non_terminals.get_non_terminals())

    # Initialize parsers for each non-terminal in the forecast applicable for the sender
    nt_parsers: dict[NonTerminal, IterativeParser] = dict()
    for non_terminal in available_non_terminals:
        forecast_packet = forecast_non_terminals[non_terminal]
        hookin_data = random.choice(list(forecast_packet.paths))
        hookin_tree = hookin_data.tree
        assert hookin_tree is not None
        path = list(map(lambda x: x[0], filter(lambda x: not x[1], hookin_data.path)))
        hookin_point = hookin_tree.get_last_by_path(path)
        nt_parsers[non_terminal] = IterativeParser(grammar.rules)
        nt_parsers[non_terminal].new_parse(
            start=non_terminal, mode=ParsingMode.COMPLETE, hookin_parent=hookin_point
        )

    continue_parse = True
    complete_parses: dict[NonTerminal, tuple[int, DerivationTree]] = dict()
    # Units of `msg_sender`'s stream already handed to the parsers.
    consumed_nr: int = 0
    parameter_parsing_exception_tuple = None
    while continue_parse:
        # Find the next message fragment sent by the selected sender
        start_time = time.time()
        pending = io_instance.pending_from(msg_sender)
        while pending is None or len(pending) <= consumed_nr:
            pending = io_instance.pending_from(msg_sender)
            if time.time() - start_time > wait_for_completion_time:
                if len(complete_parses) == 0:
                    current_parse_str = "Incompletely parsed NonTerminals:"
                    for incomplete_nt in available_non_terminals:
                        nt_parser = nt_parsers[incomplete_nt]
                        current_parse = nt_parser.collapse(nt_parser.current_tree())
                        current_parse_str += (
                            f"\n{str(incomplete_nt)}: {str(current_parse)}"
                        )

                    raise FandangoFailedError(
                        f"Timeout while waiting for next message fragment from {msg_sender}. \n"
                        + generate_parsing_error_msg_information(
                            forecast_non_terminals.get_non_terminals(),
                            available_non_terminals,
                            nt_parsers,
                            io_instance.get_full_fragments(),
                        )
                    )
                else:
                    continue_parse = False
                    break
            time.sleep(0.025)
        if not continue_parse:
            break

        assert pending is not None
        next_fragment = pending[consumed_nr:]
        consumed_nr = len(pending)

        for non_terminal in set(available_non_terminals):
            parser = nt_parsers[non_terminal]
            # Longest first: the first packet end whose parameters can be
            # derived is this non-terminal's best answer for the stream so far.
            for packet_end in reversed(parser.consume_positions(next_fragment)):
                parse_tree = next(parser.tree_at(packet_end), None)
                if parse_tree is None:
                    continue
                parse_tree = parser.collapse(parse_tree)
                assert parse_tree is not None
                forecast_packet = forecast_non_terminals[non_terminal]
                parse_tree.sender = forecast_packet.node.sender
                parse_tree.recipient = forecast_packet.node.recipient
                try:
                    grammar.populate_sources(parse_tree)
                except FandangoParseError as e:
                    parameter_parsing_exception_tuple = (
                        non_terminal,
                        e,
                        parse_tree,
                    )
                    continue
                complete_parses[non_terminal] = (packet_end, parse_tree)
                break
            if not parser.can_continue():
                available_non_terminals.remove(non_terminal)
        continue_parse = len(available_non_terminals) > 0

    if len(complete_parses) == 0:
        if parameter_parsing_exception_tuple is not None:
            applicable_nt, parameter_parsing_exception, complete_msg = (
                parameter_parsing_exception_tuple
            )
            raise FandangoFailedError(
                f"Couldn't derive parameters for received packet or timed out while waiting for remaining packet. Applicable NonTerminal: {applicable_nt} Received part: {complete_msg!r}. Exception: {str(parameter_parsing_exception)}"
            )
        else:
            raise FandangoFailedError(
                "Could not parse received message fragments into predicted NonTerminals.\n"
                + generate_parsing_error_msg_information(
                    forecast_non_terminals.get_non_terminals(),
                    available_non_terminals,
                    nt_parsers,
                    io_instance.get_full_fragments(),
                )
            )

    max_parse_end = 0
    yield_items: set[tuple[NonTerminal, DerivationTree]] = set()
    for non_terminal, (parse_end, parse_tree) in complete_parses.items():
        if parse_end < max_parse_end:
            continue
        if parse_end > max_parse_end:
            yield_items.clear()
        max_parse_end = parse_end
        yield_items.add((non_terminal, parse_tree))

    assert len(yield_items) != 0

    io_instance.consume_received(msg_sender, max_parse_end)
    for non_terminal, parse_tree in yield_items:
        yield forecast_non_terminals[non_terminal], parse_tree
    return None


def generate_parsing_error_msg_information(
    allowed_nts: set[NonTerminal],
    remaining_nts: set[NonTerminal],
    parsers: dict[NonTerminal, IterativeParser],
    received_fragments: list[tuple[str, str, str | bytes]],
) -> str:
    nt_list = map(lambda x: str(x), allowed_nts)
    applicable_nt_str = "Applicable NonTerminals: " + str(" | ".join(nt_list))
    current_parse_str = "Incompletely parsed NonTerminals:"
    for incomplete_nt in remaining_nts:
        nt_parser = parsers[incomplete_nt]
        current_parse = nt_parser.collapse(nt_parser.current_tree())
        current_parse_str += f"\n{str(incomplete_nt)}: {str(current_parse)}"
    received_msgs = f"Received messages: {received_fragments}"
    return f"{current_parse_str}\n{applicable_nt_str}\n{received_msgs}"
