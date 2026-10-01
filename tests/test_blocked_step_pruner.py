import unittest

from fandango.io.navigation.forecasting.packetforecaster import PacketForecaster
from fandango.io.navigation.graph.blocked_step_pruner import BlockedStepPruner
from fandango.io.navigation.graph.packetnavigator import PacketNavigator
from fandango.io.navigation.graph.stategrammarconverter import StateGrammarConverter
from fandango.io.navigation.route import PlannedPacket
from fandango.io.navigation.step import Step
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.repetition import Option
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from tests.utils import RESOURCES_ROOT

START = NonTerminal("<start>")
RULE = NonTerminal("<rule>")
AFTER_OK = NonTerminal("<after_ok>")
CLOSING = NonTerminal("<closing>")
NOTES = NonTerminal("<notes>")


def load_blocked_steps_grammar() -> Grammar:
    """The grammar of resources/blocked_steps.fan."""
    with open(RESOURCES_ROOT / "blocked_steps.fan") as spec:
        grammar, _ = parse(spec, use_stdlib=True, use_cache=False)
    assert grammar is not None
    return grammar


def step_of_last_message(grammar: Grammar, messages: str) -> Step:
    """The step that produced the last of the messages, as the forecaster observes it."""
    history = grammar.parse(
        messages, mode=ParsingMode.INCOMPLETE, include_controlflow=True
    )
    assert history is not None
    (step,) = PacketForecaster(grammar).predict(history).message_steps[-1]
    return step


class TestBlockedStepPruner(unittest.TestCase):
    def setUp(self):
        self.grammar = load_blocked_steps_grammar()
        self.state_rules = StateGrammarConverter(self.grammar.grammar_settings).process(
            self.grammar.rules, START
        )
        self.pruner = BlockedStepPruner(self.grammar.grammar_settings)

    def _step(self, messages: str) -> Step:
        return step_of_last_message(self.grammar, messages)

    def _prune(self, step: Step) -> dict[NonTerminal, Node]:
        return self.pruner.prune(self.state_rules, START, frozenset([step]))

    def test_blocked_step_removes_its_concatenation(self):
        rules = self._prune(self._step("hello\na\nok\n"))
        self.assertEqual(len(rules[RULE].children()), 2)
        self.assertNotIn(AFTER_OK, rules)

    def test_repetition_that_must_repeat_takes_its_rule_and_referrers_along(self):
        rules = self._prune(self._step("hello\na\nok\nx\n"))
        self.assertNotIn(AFTER_OK, rules)
        self.assertEqual(len(rules[RULE].children()), 2)

    def test_rule_deriving_nothing_leaves_a_made_up_option(self):
        rules = self._prune(self._step("hello\nc\nok\nbye\nnote\n"))
        self.assertNotIn(NOTES, rules)
        _bye, option = rules[CLOSING].children()
        self.assertIsInstance(option, Option)
        self.assertTrue(self.pruner.is_made_up(option))
        self.assertFalse(self.pruner.is_made_up(option.children()[0]))

    def test_planned_step_skips_the_made_up_option(self):
        navigator = PacketNavigator(self.grammar).gen_with_blocked_steps(
            frozenset([self._step("hello\nc\nok\nbye\nnote\n")])
        )
        history = self.grammar.parse(
            "hello\nc\nok\nbye\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        assert history is not None
        route = navigator.astar_tree_including_k_paths(
            tree=history, destination_k_path=(CLOSING, NonTerminal("<done>"))
        )
        assert route is not None
        planned_steps = [
            symbol.step for symbol in route if isinstance(symbol, PlannedPacket)
        ]
        self.assertIn(self._step("hello\nc\nok\nbye\ndone\n"), planned_steps)

    def test_route_to_a_target_without_packet_gives_the_step_to_it(self):
        navigator = PacketNavigator(self.grammar)
        history = self.grammar.parse(
            "hello\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        assert history is not None
        route = navigator.astar_tree_including_k_paths(
            tree=history, destination_k_path=(AFTER_OK,)
        )
        assert route is not None and navigator.last_target_step is not None
        self.assertEqual(navigator.last_target_step.packet, AFTER_OK)
        blocked = navigator.gen_with_blocked_steps(
            frozenset([navigator.last_target_step])
        )
        self.assertFalse(blocked.is_derivable((AFTER_OK,)))


if __name__ == "__main__":
    unittest.main()
