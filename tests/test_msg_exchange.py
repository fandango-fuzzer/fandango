#!/usr/bin/env pytest
from fandango import parse
from fandango.evolution.algorithm import Fandango
from fandango.language.tree import DerivationTree


def test_parsing():
    file = open("tests/resources/minimal_io.fan", "r")

    grammar, constraints = parse(file, use_stdlib=False, use_cache=False)
    fandango = Fandango(grammar=grammar, constraints=constraints)
    result = fandango.evolve()
    assert len(result) == 1
    result = result[0]
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