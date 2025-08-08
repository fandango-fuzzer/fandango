import random
import time
from typing import Optional

from fandango.errors import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.io import FandangoIO
from fandango.io.packetforecaster import PacketForecaster
from fandango.language import Grammar, NonTerminal, DerivationTree
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.parser.iterative_parser import IterativeParser


def _find_next_fragment(
    role_sender: str, messages: list[tuple[str, str, str | bytes]], start_idx: int = 0
) -> tuple[int, Optional[str | bytes]]:
    """
    Find the next message fragment sent by the specified sender in the list of messages.
    Returns the index of the message and the message fragment.
    """
    for idx in range(start_idx, len(messages)):
        sender, recipient, msg_fragment = messages[idx]
        if sender == role_sender:
            return idx, msg_fragment
    return -1, None


def parse_next_remote_packet(
    grammar: Grammar,
    forecast: PacketForecaster.ForecastingResult,
    io_instance: FandangoIO,
):
    if len(io_instance.get_received_msgs()) == 0:
        return None, None

    # Wait till we receive a message from one of the parties in the forecast
    received_parties = list(map(lambda x: x[0], io_instance.get_received_msgs()))
    wait_for_msg_time = 10
    start_time = time.time()
    while not forecast.contains_any_party(received_parties):
        if time.time() - start_time > wait_for_msg_time:
            if len(received_parties) == 0:
                raise FandangoFailedError(
                    "Timeout while waiting for message. No message has been received."
                )
            else:
                raise FandangoValueError(
                    "Unexpected party sent message. Expected: "
                    + " | ".join(forecast.get_msg_parties())
                    + f". Received: {received_parties}."
                    + f" Messages: {io_instance.get_received_msgs()}"
                )
        time.sleep(0.025)
        received_parties = list(map(lambda x: x[0], io_instance.get_received_msgs()))

    msg_sender = None
    # We might have received messages from different parties. Select a party that sent a message and is
    # in the current forecast.
    for idx, (msg_sender, msg_recipient, _) in enumerate(
        io_instance.get_received_msgs()
    ):
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
    current_fragment_idx: int = -1
    parameter_parsing_exception_tuple = None
    wait_for_completion_time = 1
    while continue_parse:

        # Find the next message fragment sent by the selected sender
        start_time = time.time()
        next_fragment_idx, next_fragment = _find_next_fragment(
            msg_sender, io_instance.get_received_msgs(), current_fragment_idx + 1
        )
        while next_fragment is None:
            next_fragment_idx, next_fragment = _find_next_fragment(
                msg_sender, io_instance.get_received_msgs(), current_fragment_idx + 1
            )
            if time.time() - start_time > wait_for_completion_time:
                if len(complete_parses) == 0:
                    raise FandangoFailedError(
                        "Timeout while waiting for next message fragment from "
                        + msg_sender
                        + ". Messages: "
                        + str(io_instance.get_received_msgs())
                    )
                else:
                    continue_parse = False
                    break
            time.sleep(0.025)
        if not continue_parse:
            break

        assert next_fragment is not None
        current_fragment_idx = next_fragment_idx

        for non_terminal in set(available_non_terminals):
            parser = nt_parsers[non_terminal]
            parse_tree = next(parser.consume(next_fragment), None)
            if parse_tree is not None:
                parse_tree = parser.collapse(parse_tree)
                assert parse_tree is not None
                forecast_packet = forecast_non_terminals[non_terminal]
                parse_tree.sender = forecast_packet.node.sender
                parse_tree.recipient = forecast_packet.node.recipient
                try:
                    grammar.populate_sources(parse_tree)
                    complete_parses[non_terminal] = (current_fragment_idx, parse_tree)
                except FandangoParseError as e:
                    parameter_parsing_exception_tuple = (non_terminal, e, parse_tree)
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
            nt_list = map(
                lambda x: x.format_as_spec(), forecast_non_terminals.get_non_terminals()
            )
            raise FandangoValueError(
                "Could not parse received message fragments into predicted NonTerminals. "
                + "Predicted NonTerminals: "
                + str(" | ".join(nt_list))
                + " Messages: "
                + str(io_instance.get_received_msgs())
            )

    max_parse_idx = -1
    best_parse_tree = None
    best_non_terminal = None
    for non_terminal, (parse_idx, parse_tree) in complete_parses.items():
        if max_parse_idx < parse_idx:
            max_parse_idx = parse_idx
            best_parse_tree = parse_tree
            best_non_terminal = non_terminal

    assert best_non_terminal is not None

    io_instance.clear_by_party(msg_sender, max_parse_idx)
    return forecast_non_terminals[best_non_terminal], best_parse_tree
