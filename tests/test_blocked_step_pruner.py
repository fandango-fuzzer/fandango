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
EXCHANGE_LOGIN = NonTerminal("<exchange_login>")
LOGGED_IN = NonTerminal("<logged_in>")
SUCCESS = NonTerminal("<_packet_success>")
FAILED = NonTerminal("<_packet_failed>")


def load_blocked_steps_grammar(name: str = "blocked_steps.fan") -> Grammar:
    """The grammar of resources/blocked_steps.fan."""
    with open(RESOURCES_ROOT / name) as spec:
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

    def _rule(self, rules: dict[NonTerminal, Node], symbol: NonTerminal) -> Node:
        """The rule that stands for symbol, a copy if the blocked step is below it."""
        (body,) = [
            body
            for pruned_symbol, body in rules.items()
            if BlockedStepPruner.original(pruned_symbol) == symbol
        ]
        return body

    def test_blocked_step_removes_its_concatenation(self):
        rules = self._prune(self._step("hello\na\nok\n"))
        self.assertEqual(len(self._rule(rules, RULE).children()), 2)
        self.assertNotIn(AFTER_OK, rules)

    def test_repetition_that_must_repeat_takes_its_rule_and_referrers_along(self):
        rules = self._prune(self._step("hello\na\nok\nx\n"))
        self.assertNotIn(AFTER_OK, rules)
        self.assertEqual(len(self._rule(rules, RULE).children()), 2)

    def test_rule_deriving_nothing_leaves_a_made_up_option(self):
        rules = self._prune(self._step("hello\nc\nok\nbye\nnote\n"))
        self.assertNotIn(NOTES, rules)
        _bye, option = self._rule(rules, CLOSING).children()
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


class TestBlockedStepInContext(unittest.TestCase):
    def setUp(self):
        self.grammar = load_blocked_steps_grammar("blocked_login.fan")
        self.state_rules = StateGrammarConverter(self.grammar.grammar_settings).process(
            self.grammar.rules, START
        )
        self.pruner = BlockedStepPruner(self.grammar.grammar_settings)
        self.second_success = step_of_last_message(
            self.grammar, "login\nsuccess\nlogin\nsuccess\n"
        )

    def test_step_is_blocked_below_the_caller_of_its_recursive_call(self):
        rules = self.pruner.prune(
            self.state_rules, START, frozenset([self.second_success])
        )
        self.assertEqual(
            rules[EXCHANGE_LOGIN].format_as_spec(),
            self.state_rules[EXCHANGE_LOGIN].format_as_spec(),
        )
        (copy,) = [
            symbol
            for symbol in rules
            if symbol != EXCHANGE_LOGIN
            and BlockedStepPruner.original(symbol) == EXCHANGE_LOGIN
        ]
        self.assertIn(copy.name(), rules[LOGGED_IN].format_as_spec())
        self.assertIn("failed", rules[copy].format_as_spec())
        self.assertNotIn("success", rules[copy].format_as_spec())

    def test_history_taking_the_step_in_another_context_still_parses(self):
        navigator = PacketNavigator(self.grammar).gen_with_blocked_steps(
            frozenset([self.second_success])
        )
        history = self.grammar.parse(
            "login\nsuccess\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        assert history is not None
        self.assertTrue(any(True for _ in navigator.get_controlflow_tree(history)))
        self.assertTrue(navigator.is_derivable((EXCHANGE_LOGIN, SUCCESS)))
        self.assertTrue(navigator.is_derivable((LOGGED_IN, EXCHANGE_LOGIN, FAILED)))
        self.assertFalse(navigator.is_derivable((LOGGED_IN, EXCHANGE_LOGIN, SUCCESS)))

    def test_route_through_a_copy_names_the_state_grammar(self):
        navigator = PacketNavigator(self.grammar).gen_with_blocked_steps(
            frozenset([self.second_success])
        )
        history = self.grammar.parse(
            "login\nsuccess\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        assert history is not None
        route = navigator.astar_tree_including_k_paths(
            tree=history, destination_k_path=(LOGGED_IN, EXCHANGE_LOGIN, FAILED)
        )
        assert route is not None
        self.assertIn(EXCHANGE_LOGIN, route)
        planned_steps = [
            symbol.step for symbol in route if isinstance(symbol, PlannedPacket)
        ]
        self.assertIn(
            step_of_last_message(self.grammar, "login\nsuccess\nlogin\nfailed\n"),
            planned_steps,
        )

    def test_step_without_recursive_call_above_is_blocked_on_its_path_from_start(self):
        grammar = load_blocked_steps_grammar("blocked_first_login.fan")
        navigator = PacketNavigator(grammar)
        first_login = grammar.parse(
            "login\nsuccess\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        assert first_login is not None
        route = navigator.astar_tree_including_k_paths(
            tree=first_login, destination_k_path=(LOGGED_IN, EXCHANGE_LOGIN, SUCCESS)
        )
        assert route is not None
        (second_success,) = [
            symbol.step
            for symbol in route
            if isinstance(symbol, PlannedPacket)
            and symbol.step is not None
            and symbol.step.packet == SUCCESS
        ]
        self.assertEqual(
            second_success,
            step_of_last_message(grammar, "login\nsuccess\nlogin\nsuccess\n"),
        )
        blocked = navigator.gen_with_blocked_steps(frozenset([second_success]))
        self.assertTrue(any(True for _ in blocked.get_controlflow_tree(first_login)))
        self.assertFalse(blocked.is_derivable((START, LOGGED_IN, EXCHANGE_LOGIN)))
        self.assertTrue(blocked.is_derivable((LOGGED_IN, LOGGED_IN, EXCHANGE_LOGIN)))


if __name__ == "__main__":
    unittest.main()
