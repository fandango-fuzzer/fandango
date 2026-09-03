#!/usr/bin/env pytest

"""
Tests `FandangoIO`'s buffer of received data.
"""

from fandango.io import FandangoIO


def io_with(*messages: tuple[str, str, str | bytes]) -> FandangoIO:
    io = FandangoIO()
    for sender, receiver, message in messages:
        io.add_receive(sender, receiver, message)
    return io


def test_a_message_stays_whole() -> None:
    io = io_with(("Extern", "Fuzzer", "ping\n"))
    assert io.get_received_msgs() == [("Extern", "Fuzzer", "ping\n")]


def test_blocks_come_back_as_they_arrived() -> None:
    io = io_with(
        ("Extern", "Fuzzer", "pi"),
        ("Extern", "Fuzzer", "ng"),
        ("Extern", "Fuzzer", "\n"),
    )
    assert io.pending_blocks("Extern") == ["pi", "ng", "\n"]


def test_blocks_ignore_other_senders() -> None:
    io = io_with(
        ("Extern", "Fuzzer", "ab"),
        ("Other", "Fuzzer", "XX"),
        ("Extern", "Fuzzer", "cd"),
    )
    assert io.pending_blocks("Extern") == ["ab", "cd"]
    assert io.pending_blocks("Other") == ["XX"]


def test_unknown_sender_has_no_blocks() -> None:
    assert io_with(("Extern", "Fuzzer", "ab")).pending_blocks("Nobody") == []


def test_blocks_do_not_mix_text_and_bytes() -> None:
    io = io_with(("Extern", "Fuzzer", "ab"), ("Extern", "Fuzzer", b"\x01"))
    assert io.pending_blocks("Extern") == ["ab"]


def test_blocks_keep_bytes_as_bytes() -> None:
    io = io_with(("Extern", "Fuzzer", b"\x01"), ("Extern", "Fuzzer", b"\x02\x03"))
    assert io.pending_blocks("Extern") == [b"\x01", b"\x02\x03"]


def test_drop_removes_whole_messages() -> None:
    io = io_with(("Extern", "Fuzzer", "ping\n"), ("Extern", "Fuzzer", "pong\n"))
    io.drop_received("Extern", 5)
    assert io.pending_blocks("Extern") == ["pong\n"]


def test_drop_trims_a_partial_message() -> None:
    io = io_with(("Extern", "Fuzzer", "ping\npo"), ("Extern", "Fuzzer", "ng\n"))
    io.drop_received("Extern", 5)
    assert io.pending_blocks("Extern") == ["po", "ng\n"]


def test_drop_across_several_messages() -> None:
    io = io_with(
        ("Extern", "Fuzzer", "pi"),
        ("Extern", "Fuzzer", "ng"),
        ("Extern", "Fuzzer", "\npong\n"),
    )
    io.drop_received("Extern", 5)
    assert io.pending_blocks("Extern") == ["pong\n"]


def test_drop_leaves_other_senders_alone() -> None:
    io = io_with(("Extern", "Fuzzer", "ping\n"), ("Other", "Fuzzer", "keep"))
    io.drop_received("Extern", 5)
    assert io.pending_blocks("Extern") == []
    assert io.pending_blocks("Other") == ["keep"]


def test_drop_nothing_changes_nothing() -> None:
    io = io_with(("Extern", "Fuzzer", "ping\n"))
    io.drop_received("Extern", 0)
    assert io.pending_blocks("Extern") == ["ping\n"]


def test_drop_more_than_there_is_empties_the_sender() -> None:
    io = io_with(("Extern", "Fuzzer", "ping\n"))
    io.drop_received("Extern", 99)
    assert io.pending_blocks("Extern") == []
    assert io.received_msg() is False


def test_full_fragments_joins() -> None:
    io = io_with(
        ("Extern", "Fuzzer", "pi"),
        ("Extern", "Fuzzer", "ng"),
        ("Other", "Fuzzer", "x"),
    )
    assert io.pending_blocks("Extern") == ["pi", "ng"]
    assert io.get_full_fragments() == [
        ("Extern", "Fuzzer", "ping"),
        ("Other", "Fuzzer", "x"),
    ]
