import time

from fandango.errors import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.io import FandangoIO
from fandango.io.navigation.graph.packetforecaster import (
    ForecastingNonTerminals,
    ForecastingPacket,
    ForecastingResult,
)
from fandango.language import DerivationTree, Grammar, NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.parser.iterative_parser import IterativeParser

WAIT_FOR_EXPECTED_PARTY_TIME = 10
POLL_INTERVAL = 0.025

ReceivedMessages = list[tuple[str, str, str | bytes]]


def parse_next_remote_packet(
    grammar: Grammar,
    forecast: ForecastingResult,
    io_instance: FandangoIO,
    *,
    wait_for_completion_time: float = 1.0,
) -> list[tuple[ForecastingPacket, DerivationTree]]:
    """
    Parse the next packet a remote party sent, as one of the forecast
    non-terminals.

    `wait_for_completion_time` bounds the wait once a packet has parsed: a
    candidate that can still grow may yet become a longer packet, so a
    complete parse is only handed back after no more data has arrived for
    that long. It is paid per packet, so a caller that knows its packets
    cannot grow can turn it down.
    """
    if not io_instance.received_msg():
        return []

    sender = _wait_for_expected_sender(forecast, io_instance)
    candidates = _PacketCandidates(grammar, forecast[sender])
    fed_blocks_nr = 0
    while candidates.open:
        fresh_blocks = _wait_for_new_blocks(
            io_instance, sender, fed_blocks_nr, wait_for_completion_time
        )
        if not fresh_blocks:
            if not candidates.found:
                raise FandangoFailedError(
                    f"Timeout while waiting for next message fragment from {sender}. \n"
                    + candidates.describe(io_instance.get_full_fragments())
                )
            break
        fed_blocks_nr += len(fresh_blocks)
        candidates.consume(fresh_blocks)

    if not candidates.found:
        raise candidates.failure(io_instance.get_full_fragments())

    packet_end, packets = candidates.longest()
    io_instance.drop_received(sender, packet_end)
    return packets


def _wait_for_expected_sender(
    forecast: ForecastingResult, io_instance: FandangoIO
) -> str:
    """The first party in the forecast that sent something, waiting a while for one."""
    started = time.time()
    while True:
        senders = [sender for sender, _, _ in io_instance.get_received_msgs()]
        for sender in senders:
            if sender in forecast:
                return sender
        if time.time() - started > WAIT_FOR_EXPECTED_PARTY_TIME:
            if not senders:
                raise FandangoFailedError(
                    "Timeout while waiting for message. No message has been received."
                )
            raise FandangoValueError(
                "Unexpected party sent message. Expected: "
                + " | ".join(forecast.get_msg_parties())
                + f". Received: {set(senders)}."
                + f" Messages: {io_instance.get_full_fragments()}"
            )
        time.sleep(POLL_INTERVAL)


def _wait_for_new_blocks(
    io_instance: FandangoIO, sender: str, nr_fed_blocks: int, timeout: float
) -> list[str | bytes]:
    """The blocks from `sender` after the first `fed_blocks`, empty once `timeout` passes without any."""
    started = time.time()
    while True:
        blocks = io_instance.pending_blocks(sender)
        if len(blocks) > nr_fed_blocks:
            return blocks[nr_fed_blocks:]
        if time.time() - started > timeout:
            return []
        time.sleep(POLL_INTERVAL)


class _PacketCandidates:
    """One parser per forecast non-terminal, and the longest packet each has found so far."""

    def __init__(self, grammar: Grammar, expected: ForecastingNonTerminals):
        self._grammar = grammar
        self._expected = expected
        self.parsers: dict[NonTerminal, IterativeParser] = {}
        for non_terminal in expected.get_non_terminals():
            mounting_path = next(iter(expected[non_terminal].paths))
            hookin_path = [nt for nt, is_new in mounting_path.path if not is_new]
            hookin_parent = mounting_path.tree.get_last_by_path(hookin_path)
            parser = IterativeParser(grammar.rules)
            parser.new_parse(
                start=non_terminal,
                mode=ParsingMode.COMPLETE,
                hookin_parent=hookin_parent,
            )
            self.parsers[non_terminal] = parser
        self.open: set[NonTerminal] = set(self.parsers)
        self.found: dict[NonTerminal, tuple[int, DerivationTree]] = {}
        self.last_parameter_error: (
            tuple[NonTerminal, FandangoParseError, DerivationTree] | None
        ) = None

    def consume(self, blocks: list[str | bytes]) -> None:
        for non_terminal in list(self.open):
            parser = self.parsers[non_terminal]
            for block in blocks:
                parser.consume(block)
            self._take_longest_packet(non_terminal)
            if not parser.can_continue():
                self.open.remove(non_terminal)

    def _take_longest_packet(self, non_terminal: NonTerminal) -> None:
        parser = self.parsers[non_terminal]
        packet = self._expected[non_terminal]
        packet_ends = [end for end in parser.parsed_positions() if end > 0]
        # Longest first
        for packet_end in reversed(packet_ends):
            parsed, _ = next(parser.tree_at(packet_end), (None, None))
            if parsed is None:
                continue
            tree = parser.collapse(parsed)
            assert tree is not None
            tree.sender = packet.node.sender
            tree.recipient = packet.node.recipient
            try:
                self._grammar.populate_sources(tree)
            except FandangoParseError as e:
                self.last_parameter_error = (non_terminal, e, tree)
                continue
            self.found[non_terminal] = (packet_end, tree)
            return

    def longest(self) -> tuple[int, list[tuple[ForecastingPacket, DerivationTree]]]:
        packet_end = max(end for end, _ in self.found.values())
        packets = [
            (self._expected[non_terminal], tree)
            for non_terminal, (end, tree) in self.found.items()
            if end == packet_end
        ]
        return packet_end, packets

    def failure(self, received: ReceivedMessages) -> FandangoFailedError:
        if self.last_parameter_error is not None:
            non_terminal, error, tree = self.last_parameter_error
            return FandangoFailedError(
                f"Couldn't derive parameters for received packet or timed out while waiting for remaining packet. Applicable NonTerminal: {non_terminal} Received part: {tree!r}. Exception: {error}"
            )
        return FandangoFailedError(
            "Could not parse received message fragments into predicted NonTerminals.\n"
            + self.describe(received)
        )

    def describe(self, received: ReceivedMessages) -> str:
        unfinished = "Incompletely parsed NonTerminals:"
        for non_terminal in self.open:
            parser = self.parsers[non_terminal]
            unfinished += f"\n{non_terminal}: {parser.collapse(parser.current_tree())}"
        applicable = "Applicable NonTerminals: " + " | ".join(map(str, self.parsers))
        return f"{unfinished}\n{applicable}\nReceived messages: {received}"
