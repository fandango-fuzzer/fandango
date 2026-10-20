#!/usr/bin/env pytest

"""
Tests timers of protocol specs: when they expire, and that they leave other parties' messages alone.
"""

import time
from collections.abc import Iterator

import pytest

from fandango.io import (
    ConnectionMode,
    FandangoIO,
    FandangoParty,
    TimerControl,
    TimerEvent,
)
from fandango.language.parse.parse import parse


class Server(FandangoParty):
    def __init__(self) -> None:
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass


class Client(FandangoParty):
    def __init__(self) -> None:
        super().__init__(connection_mode=ConnectionMode.CONNECT)

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass


@pytest.fixture
def io() -> Iterator[FandangoIO]:
    io = FandangoIO.instance()
    parties_before = dict(io.parties)
    io.clear_received_msgs()
    yield io
    for party in set(io.parties.values()) - set(parties_before.values()):
        party.stop()
    io.parties = parties_before
    io.clear_received_msgs()


def expired_count(io: FandangoIO) -> int:
    return sum(sender == "TimerEvent" for sender, _, _ in io.get_received_msgs())


def test_a_message_without_sender_comes_from_the_external_party_not_a_timer(
    io: FandangoIO,
) -> None:
    Server()
    TimerEvent()
    client = Client()

    client.receive("PONG\n", None)

    assert io.get_received_msgs() == [("Server", "Client", "PONG\n")]


def test_a_timer_expires_once(io: FandangoIO) -> None:
    timers = TimerControl()

    timers.start_timer("1", 1)
    time.sleep(1.5)

    assert io.get_received_msgs() == [("TimerEvent", "TimerControl", "expired: 1\n")]


def test_a_cancelled_timer_does_not_expire(io: FandangoIO) -> None:
    timers = TimerControl()

    timers.start_timer("1", 1)
    time.sleep(0.2)
    timers.stop_timers("1")
    time.sleep(1.3)

    assert expired_count(io) == 0


def test_a_cancelled_timer_started_again_at_once_expires_once(io: FandangoIO) -> None:
    timers = TimerControl()

    timers.start_timer("1", 1)
    timers.stop_timers("1")
    timers.start_timer("1", 1)
    time.sleep(1.6)

    assert expired_count(io) == 1


def test_a_timer_cancelled_after_it_expired_drops_its_expiry_not_handled_yet(
    io: FandangoIO,
) -> None:
    timers = TimerControl()

    timers.start_timer("1", 1)
    time.sleep(1.5)
    timers.stop_timers("1")

    assert expired_count(io) == 0


def test_a_timer_of_a_fraction_of_a_second_expires_on_time(io: FandangoIO) -> None:
    timers = TimerControl()

    timers.start_timer("1", 0.3)
    time.sleep(0.2)
    assert expired_count(io) == 0
    time.sleep(0.2)

    assert expired_count(io) == 1


def test_a_start_message_with_a_decimal_timeout_starts_a_timer_of_that_duration() -> (
    None
):
    grammar, _ = parse("<start> ::= <timer_start>", use_cache=False)
    assert grammar is not None
    start_message = grammar.parse("start: 7 (0.25)\n")
    assert start_message is not None
    # parse() enters an environment of its own, with its own FandangoIO
    io = FandangoIO.instance()
    timers = TimerControl()

    timers.send(start_message, None)
    time.sleep(0.4)

    assert io.get_received_msgs() == [("TimerEvent", "TimerControl", "expired: 7\n")]
    timers.stop()
