"""
Tests for constraint-based disambiguation when an incoming packet is syntactically
ambiguous — i.e. it can be parsed by two different non-terminals that produce the
same string, but only one of them satisfies all constraints.

Grammar under test (ambiguous_io.fan):
    <start> ::= <Fuzzer:Extern:query> (<Extern:Fuzzer:nt_pass> | <Extern:Fuzzer:nt_fail>)
    <query>   ::= 'hello'
    <nt_pass> ::= 'response'      (no constraint → always passes)
    <nt_fail> ::= 'response'      (constraint: str(<nt_fail>) == "world" → always fails)

The Fuzzer.send() immediately injects the Extern reply so the algorithm
receives it before timing out.
"""

import unittest

from fandango.api import Fandango
from fandango.io import FandangoIO
from fandango.io.navigation.packetforecaster import PacketForecaster
from fandango.io.packetparser import parse_next_remote_packet
from fandango.language.grammar import FuzzingMode, ParsingMode
from fandango.language.symbols import NonTerminal
from tests.utils import RESOURCES_ROOT


def _load_fandango() -> Fandango:
    with open(RESOURCES_ROOT / "ambiguous_io.fan") as f:
        spec = f.read()
    return Fandango(spec, use_stdlib=False, use_cache=False)


class TestParseNextRemotePacketAmbiguity(unittest.TestCase):
    """Unit tests for parse_next_remote_packet with a syntactically ambiguous message."""

    def test_yields_one_result_per_matching_non_terminal(self):
        """
        When the received message can be parsed by two different non-terminals
        (<nt_pass> and <nt_fail>) that both produce 'response', the generator
        must yield exactly two (ForecastingPacket, DerivationTree) pairs — one
        for each candidate non-terminal.
        """
        f = _load_fandango()
        grammar = f.grammar

        # Build a history tree that represents the state after <query> was sent.
        history_tree = grammar.parse("hello", mode=ParsingMode.INCOMPLETE)
        self.assertIsNotNone(history_tree)

        forecast = PacketForecaster(grammar).predict(history_tree)
        self.assertIn("Extern", forecast.get_msg_parties())
        self.assertIn(
            NonTerminal("<nt_pass>"),
            forecast["Extern"].get_non_terminals(),
        )
        self.assertIn(
            NonTerminal("<nt_fail>"),
            forecast["Extern"].get_non_terminals(),
        )

        # Inject the ambiguous message using a fresh (non-singleton) IO instance.
        io = FandangoIO()
        io.add_receive("Extern", "Fuzzer", "response")

        results = list(parse_next_remote_packet(grammar, forecast, io))

        yielded_symbols = {pair[1].symbol for pair in results}
        self.assertEqual(
            yielded_symbols,
            {NonTerminal("<nt_pass>"), NonTerminal("<nt_fail>")},
            "Expected one result for each syntactically matching non-terminal",
        )
        self.assertEqual(
            len(results),
            2,
            "Exactly two parse candidates should be yielded",
        )

    def test_both_candidates_parse_to_same_string(self):
        """
        Both yielded parse trees should produce the same string ('response'),
        confirming the syntactic equivalence that makes the packet ambiguous.
        """
        f = _load_fandango()
        grammar = f.grammar

        history_tree = grammar.parse("hello", mode=ParsingMode.INCOMPLETE)
        forecast = PacketForecaster(grammar).predict(history_tree)

        io = FandangoIO.instance()
        io.add_receive("Extern", "Fuzzer", "response")

        results = list(parse_next_remote_packet(grammar, forecast, io))

        self.assertEqual(len(results), 2, "Expected two parse candidates")

        for _, parse_tree in results:
            self.assertEqual(
                str(parse_tree),
                "response",
                f"Parse tree for {parse_tree.symbol} should yield 'response'",
            )


class TestConstraintDisambiguation(unittest.TestCase):
    """
    Integration tests: the protocol algorithm must select the interpretation
    of the ambiguous response that satisfies the constraints.
    """

    def test_selects_non_terminal_that_passes_constraint(self):
        """
        fuzz() must return a protocol run where the Extern response is attached
        to <nt_pass> (no constraint), not <nt_fail> (str(<nt_fail>) == "world"
        always fails for the received value 'response').
        """
        f = _load_fandango()
        result_list = f.fuzz(mode=FuzzingMode.IO, population_size=1)

        self.assertEqual(len(result_list), 1)
        result = result_list[0]
        messages = result.protocol_msgs()
        self.assertEqual(len(messages), 3)

        # First message: Fuzzer sends the query
        self.assertEqual(messages[0].sender, "Fuzzer")
        self.assertEqual(str(messages[0].msg), "hello")

        # Second message: Extern's response must be interpreted as <nt_pass>
        self.assertEqual(messages[1].sender, "Extern")
        self.assertEqual(str(messages[1].msg), "response")
        self.assertEqual(messages[2].sender, "Extern")
        self.assertEqual(str(messages[2].msg), "response")
        self.assertEqual(
            messages[1].msg.symbol,
            NonTerminal("<nt_pass>"),
            f"Expected <nt_pass> (passes constraint), got {messages[1].msg.symbol}",
        )
        self.assertEqual(
            messages[2].msg.symbol,
            NonTerminal("<nt_pass>"),
            f"Expected <nt_pass> (passes constraint), got {messages[2].msg.symbol}",
        )

    def test_rejects_interpretation_that_fails_constraint(self):
        """
        The <nt_fail> non-terminal must never appear in the final protocol run
        because its constraint str(<nt_fail>) == "world" is never satisfied by
        the received value 'response'.
        """
        f = _load_fandango()
        result_list = f.fuzz(mode=FuzzingMode.IO, population_size=1)

        self.assertEqual(len(result_list), 1)
        result = result_list[0]
        messages = result.protocol_msgs()

        for msg in messages:
            self.assertNotEqual(
                msg.msg.symbol,
                NonTerminal("<nt_fail>"),
                "<nt_fail> should never be selected because its constraint fails",
            )


if __name__ == "__main__":
    unittest.main()
