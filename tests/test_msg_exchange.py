#!/usr/bin/env pytest
from fandango import parse
from fandango.api import Fandango
from fandango.language.grammar import FuzzingMode
from fandango.language.tree import DerivationTree
from .utils import RESOURCES_ROOT


def test_msg_exchange():
    with open(RESOURCES_ROOT / "minimal_io.fan") as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    result_list = fandango.fuzz(mode=FuzzingMode.IO)
    assert len(result_list) == 1
    result = result_list[0]
    assert isinstance(result, DerivationTree)
    messages = result.protocol_msgs()
    assert len(messages) == 4
    assert messages[0].sender == "Fuzzer"
    assert messages[0].recipient == "Extern"
    assert messages[0].msg.to_string() == "ping\n"
    assert messages[1].sender == "Extern"
    assert messages[1].recipient == "Fuzzer"
    assert messages[1].msg.to_string() == "pong\n"
    assert messages[2].sender == "Fuzzer"
    assert messages[2].recipient == "Extern"
    assert messages[2].msg.to_string() == "puff\n"
    assert messages[3].sender == "Extern"
    assert messages[3].recipient == "Fuzzer"
    assert messages[3].msg.to_string() == "paff\n"
