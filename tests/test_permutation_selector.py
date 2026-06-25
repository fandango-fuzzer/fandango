"""
Tests for permutation-aware handling in PacketSelector:
  - _build_permutation_groups correctly identifies permutation peer sets
  - When a permutation peer arrives out of order, it is removed from the
    guide path in-place rather than triggering a full re-plan
"""

import unittest

from fandango.api import Fandango
from fandango.io import ConnectionMode, FandangoIO, FandangoParty
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.packetselector import PacketSelector
from fandango.io.navigation.protocol_model import ProtocolModel
from fandango.language import DerivationTree, NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from tests.utils import RESOURCES_ROOT


def _load_grammar() -> Grammar:
    with open(RESOURCES_ROOT / "permutation_io.fan") as f:
        spec = f.read()
    return Fandango(spec, use_stdlib=True, use_cache=False).grammar


class _TestParty(FandangoParty):
    """Minimal concrete FandangoParty that skips the singleton registration
    so it can be used in isolated unit tests."""

    def send(self, message, recipient):
        pass

    def start(self):
        pass

    def stop(self):
        pass


def _make_test_io() -> FandangoIO:
    """Return a FandangoIO with a single fuzzer-controlled StdOut party."""
    # Bypass FandangoParty.__init__ to avoid the FandangoIO singleton dependency.
    party = object.__new__(_TestParty)
    party.party_name = "StdOut"
    party._connection_mode = ConnectionMode.CONNECT
    io = FandangoIO()
    io.parties["StdOut"] = party
    return io


class _StubSelector(PacketSelector):
    """PacketSelector with forecasting/party stubs so guide-path tests
    don't depend on a live IO instance or full coverage computation."""

    def next_fuzzer_parties(
        self, show_fuzzer_controlled=True, show_external_controlled=False
    ):
        return ["StdOut"] if show_fuzzer_controlled else []

    def get_fuzzer_packets(self):
        return []


class TestPermutationGroupBuilding(unittest.TestCase):
    """Unit tests for _build_permutation_groups and its helpers."""

    grammar: Grammar

    @classmethod
    def setUpClass(cls):
        cls.grammar = _load_grammar()

    def _bare_model(self):
        """Return a ProtocolModel instance with only ._grammar set (no full __init__)."""
        model = object.__new__(ProtocolModel)
        model._grammar = self.grammar
        return model

    def test_permutation_peers_share_group(self):
        groups = self._bare_model()._build_permutation_groups()
        msg_a = NonTerminal("<msg_a>")
        msg_b = NonTerminal("<msg_b>")
        self.assertIn(msg_a, groups)
        self.assertIn(msg_b, groups)
        self.assertEqual(groups[msg_a], frozenset({msg_a, msg_b}))
        self.assertEqual(groups[msg_b], frozenset({msg_a, msg_b}))

    def test_non_permutation_symbol_has_no_group(self):
        groups = self._bare_model()._build_permutation_groups()
        self.assertNotIn(NonTerminal("<msg_c>"), groups)

    def test_collect_packet_symbols_from_permutation_node(self):
        settings = self.grammar.grammar_settings
        nt_a = NonTerminalNode(
            NonTerminal("<msg_a>"), settings, sender="StdOut", recipient=None
        )
        nt_b = NonTerminalNode(
            NonTerminal("<msg_b>"), settings, sender="StdOut", recipient=None
        )
        alt = Alternative(
            [
                Concatenation([nt_a, nt_b], settings),
                Concatenation([nt_b, nt_a], settings),
            ],
            settings,
            is_permutation=True,
        )
        result: set[NonTerminal] = set()
        ProtocolModel._collect_packet_symbols_from_node(alt, result)
        self.assertEqual(result, {NonTerminal("<msg_a>"), NonTerminal("<msg_b>")})

    def test_non_permutation_alternative_yields_no_group(self):
        settings = self.grammar.grammar_settings
        nt_a = NonTerminalNode(
            NonTerminal("<msg_a>"), settings, sender="StdOut", recipient=None
        )
        nt_b = NonTerminalNode(
            NonTerminal("<msg_b>"), settings, sender="StdOut", recipient=None
        )
        alt = Alternative([nt_a, nt_b], settings, is_permutation=False)
        groups: dict[NonTerminal, frozenset[NonTerminal]] = {}
        model = self._bare_model()
        model._collect_permutation_groups(alt, groups)
        self.assertEqual(groups, {})


class TestPermutationGuidePathAdjustment(unittest.TestCase):
    """Integration tests verifying guide-path behaviour when permutation
    peers arrive out of order."""

    grammar: Grammar

    @classmethod
    def setUpClass(cls):
        cls.grammar = _load_grammar()

    def _make_selector(self):
        return _StubSelector(
            self.grammar,
            _make_test_io(),
            DerivationTree(NonTerminal("<start>")),
            diversity_k=1,
        )

    def test_out_of_order_permutation_peer_removed_from_guide_path(self):
        """msg_b arrives when the guide expects msg_a first.  Because they are
        permutation peers, msg_b should be silently consumed from the guide path
        rather than triggering a re-plan."""
        sel = self._make_selector()

        msg_a = NonTerminal("<msg_a>")
        msg_b = NonTerminal("<msg_b>")
        msg_c = NonTerminal("<msg_c>")
        pnt_a = PacketNonTerminal("StdOut", None, msg_a)
        pnt_b = PacketNonTerminal("StdOut", None, msg_b)
        pnt_c = PacketNonTerminal("StdOut", None, msg_c)

        sel._guide_path = [pnt_a, pnt_b, pnt_c]
        sel._guide_target = (msg_c,)
        sel._prev_session_msgs = []

        sel.history_tree = self.grammar.parse(
            "b", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        sel._forecasting_result = None

        sel._select_next_packet()

        self.assertIn(pnt_a, sel._guide_path, "pnt_a should still be pending")
        self.assertNotIn(
            pnt_b, sel._guide_path, "pnt_b arrived – should be gone from path"
        )
        self.assertIn(pnt_c, sel._guide_path, "pnt_c should still be pending")

    def test_guide_path_unchanged_when_no_new_messages(self):
        """With an empty history and no previously seen messages, the guide
        path should remain intact after _select_next_packet."""
        sel = self._make_selector()

        msg_a = NonTerminal("<msg_a>")
        msg_b = NonTerminal("<msg_b>")
        pnt_a = PacketNonTerminal("StdOut", None, msg_a)
        pnt_b = PacketNonTerminal("StdOut", None, msg_b)

        sel._guide_path = [pnt_a, pnt_b]
        sel._guide_target = (msg_b,)
        sel._prev_session_msgs = []

        sel._select_next_packet()

        self.assertEqual(sel._guide_path, [pnt_a, pnt_b])

    def test_expected_message_advances_guide_path(self):
        """When the in-order message (msg_a) arrives as expected, pnt_a is
        consumed and the guide path advances to pnt_b."""
        sel = self._make_selector()

        msg_a = NonTerminal("<msg_a>")
        msg_b = NonTerminal("<msg_b>")
        pnt_a = PacketNonTerminal("StdOut", None, msg_a)
        pnt_b = PacketNonTerminal("StdOut", None, msg_b)

        sel._guide_path = [pnt_a, pnt_b]
        sel._guide_target = (msg_b,)
        sel._prev_session_msgs = []

        sel.history_tree = self.grammar.parse(
            "a", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        sel._forecasting_result = None

        sel._select_next_packet()

        self.assertNotIn(pnt_a, sel._guide_path, "pnt_a arrived – should be consumed")
        self.assertIn(pnt_b, sel._guide_path, "pnt_b should still be pending")

    def test_both_permutation_peers_out_of_order_both_consumed(self):
        """Two sequential calls simulate b arriving first, then a.
        After both calls the only remaining guide-path entry should be pnt_c."""
        sel = self._make_selector()

        msg_a = NonTerminal("<msg_a>")
        msg_b = NonTerminal("<msg_b>")
        msg_c = NonTerminal("<msg_c>")
        pnt_a = PacketNonTerminal("StdOut", None, msg_a)
        pnt_b = PacketNonTerminal("StdOut", None, msg_b)
        pnt_c = PacketNonTerminal("StdOut", None, msg_c)

        # --- call 1: msg_b arrives out of order ---
        sel._guide_path = [pnt_a, pnt_b, pnt_c]
        sel._guide_target = (msg_c,)
        sel._prev_session_msgs = []
        sel.history_tree = self.grammar.parse(
            "b", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        sel._forecasting_result = None
        sel._select_next_packet()

        # pnt_b consumed out-of-order; pnt_a still pending
        self.assertIn(pnt_a, sel._guide_path)
        self.assertNotIn(pnt_b, sel._guide_path)

        # _remember_messages() was called inside _select_next_packet; do not
        # reset _prev_session_msgs — let the selector see only the incremental delta.

        # --- call 2: msg_a arrives next ---
        sel.history_tree = self.grammar.parse(
            "ba", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        sel._forecasting_result = None
        sel._select_next_packet()

        self.assertNotIn(pnt_a, sel._guide_path, "pnt_a arrived – should be consumed")
        self.assertNotIn(pnt_b, sel._guide_path, "pnt_b was consumed in call 1")
        self.assertIn(pnt_c, sel._guide_path, "pnt_c should still be pending")


if __name__ == "__main__":
    unittest.main()
