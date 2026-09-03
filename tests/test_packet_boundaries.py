#!/usr/bin/env pytest

import time

from fandango.api import Fandango
from fandango.io import FandangoIO
from fandango.io.navigation.graph.packetforecaster import PacketForecaster
from fandango.io.packetparser import parse_next_remote_packet
from fandango.language.grammar import ParsingMode
from tests.utils import RESOURCES_ROOT

PARTIES = """
class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)
"""
HEAD = "<start> ::= <Fuzzer:Extern:query> <Extern:Fuzzer:reply>\n<query> ::= 'hello'\n"
FIXED = HEAD + "<reply> ::= 'abcd;'\n" + PARTIES
GROWABLE = HEAD + "<reply> ::= <line>+\n<line> ::= r'[a-z]+' ';'\n" + PARTIES
AMBIGUOUS = (RESOURCES_ROOT / "ambiguous_io.fan").read_text()


def forecast_of(spec: str):
    """The grammar, and what it expects next once the query has been sent."""
    grammar = Fandango(spec, use_stdlib=False, use_cache=False).grammar
    history = grammar.parse("hello", mode=ParsingMode.INCOMPLETE)
    assert history is not None
    return grammar, PacketForecaster(grammar).predict(history)


def test_packet_ending_within_block() -> None:
    grammar, forecast = forecast_of(AMBIGUOUS)
    io = FandangoIO()
    io.add_receive("Extern", "Fuzzer", "responseAND MORE")

    results = list(parse_next_remote_packet(grammar, forecast, io))

    assert {str(tree) for _, tree in results} == {"response"}
    assert io.pending_blocks("Extern") == ["AND MORE"]
    assert io.received_msg()


def test_packet_arriving_in_pieces() -> None:
    grammar, forecast = forecast_of(AMBIGUOUS)
    io = FandangoIO()
    for piece in ("res", "pon", "se"):
        io.add_receive("Extern", "Fuzzer", piece)

    results = list(parse_next_remote_packet(grammar, forecast, io))

    assert {str(tree) for _, tree in results} == {"response"}
    assert io.pending_blocks("Extern") == []
    assert not io.received_msg()


def test_a_growable_packet_waits_for_more_data() -> None:
    grammar, forecast = forecast_of(GROWABLE)
    io = FandangoIO()
    io.add_receive("Extern", "Fuzzer", "abcd;")

    start = time.perf_counter()
    results = list(
        parse_next_remote_packet(grammar, forecast, io, wait_for_completion_time=0.3)
    )
    waited = time.perf_counter() - start

    assert {str(tree) for _, tree in results} == {"abcd;"}
    assert waited >= 0.3, "Method didn't wait long enough"
    assert waited < 0.9, "Method did wait for too long"


def test_a_fixed_packet_does_not_wait() -> None:
    """Once no candidate can grow, the answer is due at once."""
    grammar, forecast = forecast_of(FIXED)
    io = FandangoIO()
    io.add_receive("Extern", "Fuzzer", "abcd;")

    start = time.perf_counter()
    results = list(parse_next_remote_packet(grammar, forecast, io))
    waited = time.perf_counter() - start

    assert {str(tree) for _, tree in results} == {"abcd;"}
    assert waited < 0.3, "Method did wait but shouldn't"
