import unittest

from fandango.api import Fandango
from fandango.io import ConnectionMode, FandangoIO, FandangoParty
from fandango.io.navigation.forecast_view import ForecastView
from fandango.io.navigation.packet_guide import PacketGuide
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.protocol_model import ProtocolModel
from fandango.io.navigation.target_selector import TargetSelector
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


class _StubForecast(ForecastView):
    """ForecastView with fixed party/packet stubs, keeping the real prediction."""

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
    """Guide-path adjustment when permutation peers arrive out of order."""

    grammar: Grammar

    @classmethod
    def setUpClass(cls):
        cls.grammar = _load_grammar()

    def _make_guide(self) -> PacketGuide:
        start = NonTerminal("<start>")
        self.history = DerivationTree(start)
        model = ProtocolModel(self.grammar, start)
        forecast = _StubForecast(self.grammar, _make_test_io(), lambda: self.history)
        navigator = PacketNavigator(self.grammar, start)
        target_selector = TargetSelector(self.grammar, start, model)
        return PacketGuide(
            model, forecast, navigator, target_selector, max_messages_per_tree=200
        )

    def _select(self, guide: PacketGuide) -> None:
        # a non-empty uncovered list keeps the guide off the "guide to end" path
        guide.select_next_packet(
            self.history, [], lambda: [(NonTerminal("<msg_c>"),)], lambda: []
        )

    def _parse(self, text: str) -> DerivationTree:
        return self.grammar.parse(
            text, mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )

    def test_out_of_order_permutation_peer_removed_from_guide_path(self):
        guide = self._make_guide()
        pnt_a = PacketNonTerminal("StdOut", None, NonTerminal("<msg_a>"))
        pnt_b = PacketNonTerminal("StdOut", None, NonTerminal("<msg_b>"))
        pnt_c = PacketNonTerminal("StdOut", None, NonTerminal("<msg_c>"))

        guide._guide_path = [pnt_a, pnt_b, pnt_c]
        guide._guide_target = (NonTerminal("<msg_c>"),)
        guide._prev_session_msgs = []
        self.history = self._parse("b")
        self._select(guide)

        self.assertEqual(guide._guide_path, [pnt_a, pnt_c])

    def test_guide_path_unchanged_when_no_new_messages(self):
        guide = self._make_guide()
        pnt_a = PacketNonTerminal("StdOut", None, NonTerminal("<msg_a>"))
        pnt_b = PacketNonTerminal("StdOut", None, NonTerminal("<msg_b>"))

        guide._guide_path = [pnt_a, pnt_b]
        guide._guide_target = (NonTerminal("<msg_b>"),)
        guide._prev_session_msgs = []
        self._select(guide)

        self.assertEqual(guide._guide_path, [pnt_a, pnt_b])

    def test_expected_message_advances_guide_path(self):
        guide = self._make_guide()
        pnt_a = PacketNonTerminal("StdOut", None, NonTerminal("<msg_a>"))
        pnt_b = PacketNonTerminal("StdOut", None, NonTerminal("<msg_b>"))

        guide._guide_path = [pnt_a, pnt_b]
        guide._guide_target = (NonTerminal("<msg_b>"),)
        guide._prev_session_msgs = []
        self.history = self._parse("a")
        self._select(guide)

        self.assertEqual(guide._guide_path, [pnt_b])

    def test_both_permutation_peers_out_of_order_both_consumed(self):
        guide = self._make_guide()
        pnt_a = PacketNonTerminal("StdOut", None, NonTerminal("<msg_a>"))
        pnt_b = PacketNonTerminal("StdOut", None, NonTerminal("<msg_b>"))
        pnt_c = PacketNonTerminal("StdOut", None, NonTerminal("<msg_c>"))

        guide._guide_path = [pnt_a, pnt_b, pnt_c]
        guide._guide_target = (NonTerminal("<msg_c>"),)
        guide._prev_session_msgs = []
        self.history = self._parse("b")
        self._select(guide)
        self.assertEqual(guide._guide_path, [pnt_a, pnt_c])

        self.history = self._parse("ba")
        self._select(guide)
        self.assertEqual(guide._guide_path, [pnt_c])


if __name__ == "__main__":
    unittest.main()
