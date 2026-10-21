import random
import unittest
from collections.abc import Iterator
from unittest import mock

from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.graph.grammar_navigator import GrammarNavigator
from fandango.io.navigation.graph.grammar_navigator.path_search import PathSearch
from fandango.io.navigation.graph.packetnavigator import PacketNavigator
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.route import PlannedPacket
from fandango.io.navigation.selection.step_refusals import StepRefusalCounter
from fandango.io.navigation.selection.violation_profiler.value_features import (
    literals_of,
    value_features,
)
from fandango.io.navigation.selection.violation_profiler.violation_profile import (
    Symptom,
    ViolationProfile,
    _Feature,
)
from fandango.io.violation import FandangoRemoteViolation, RemoteViolationType
from fandango.language.grammar import FuzzingMode, ParsingMode
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree
from tests.utils import RESOURCES_ROOT

HELP = PacketNonTerminal("Fuzzer", "Extern", NonTerminal("<help>"))
GET = PacketNonTerminal("Fuzzer", "Extern", NonTerminal("<get>"))
CMD = PacketNonTerminal("Fuzzer", "Extern", NonTerminal("<cmd>"))
GARBAGE_INSTEAD_OF_HELPTEXT = Symptom(RemoteViolationType.SYNTAX, ("<helptext>",), ())
SESSIONS = 60
# <help> violates after <ehlo>, <cmd> with '!', and <get> after a <set> with <bad>
GRAMMAR = "violation_profile.fan"
EHLO = "hello\nehlo\nok\n"
HELO = "hello\nhelo\nok\nok\n"


def load(name: str) -> Grammar:
    with open(RESOURCES_ROOT / name) as spec:
        grammar, _ = parse(spec, use_stdlib=True, use_cache=False)
    assert grammar is not None
    return grammar


def session(grammar: Grammar, messages: str) -> DerivationTree:
    tree = grammar.parse(
        messages, mode=ParsingMode.INCOMPLETE, include_controlflow=True
    )
    assert tree is not None
    return tree


def last_message(tree: DerivationTree) -> DerivationTree:
    return next(tree.protocol_msgs(reverse=True)).msg


def nonterminals_in(message: DerivationTree) -> set[KPath]:
    """A stand-in for k-paths: every nonterminal in the message, as a path of length one."""

    def walk(node: DerivationTree) -> Iterator[DerivationTree]:
        yield node
        for child in node.children:
            yield from walk(child)

    return {
        (node.symbol,)
        for node in walk(message)
        if isinstance(node.symbol, NonTerminal)
        and not node.symbol.name().startswith("<__")
    }


def garbage_instead_of(tree: DerivationTree, expected: str) -> FandangoRemoteViolation:
    return FandangoRemoteViolation(
        "garbage",
        error_type=RemoteViolationType.SYNTAX,
        session_tree=tree,
        sender="Extern",
        recipient="Fuzzer",
        payload_raw="garbage\n",
        expected_nonterminals=[NonTerminal(expected)],
    )


class TestViolationProfile(unittest.TestCase):
    """
    <help> violates after <ehlo> and is answered after <helo>; <cmd> violates if its argument, one regular
    expression, is '!'; <get> violates after a <set> with the argument <bad>.
    """

    AFTER_EHLO = EHLO + "help\n"
    ANSWERED = HELO + "help\nhelptext\n"
    AFTER_BAD_SET = EHLO + "set !\nok\nget\n"

    def setUp(self):
        self.grammar = load(GRAMMAR)
        self.profile = ViolationProfile(
            k_paths_of=nonterminals_in,
            is_fuzzer_party=lambda name: name == "Fuzzer",
            literals=literals_of(self.grammar.rules),
        )

    def trigger(
        self, messages: str, times: int = 1, expected: str = "<helptext>"
    ) -> None:
        for _ in range(times):
            tree = session(self.grammar, messages)
            self.profile.observe_violation(tree, garbage_instead_of(tree, expected))
            self.profile.signal_session_end()

    def answer(self, messages: str, times: int = 1) -> None:
        for _ in range(times):
            self.profile.observe_answer(session(self.grammar, messages))
            self.profile.signal_session_end()

    def suspected(self, messages: str):
        return self.profile.suspicion_of(last_message(session(self.grammar, messages)))

    def _learn(self, answers: int = 3) -> None:
        self.trigger(self.AFTER_EHLO)
        self.answer(self.ANSWERED, answers)
        self.trigger(self.AFTER_EHLO, ViolationProfile.MIN_TRIGGERS - 1)

    def test_the_history_that_triggers_the_violation_is_suspected(self):
        self._learn()
        self.assertEqual(
            self.suspected(self.AFTER_EHLO),
            (HELP, GARBAGE_INSTEAD_OF_HELPTEXT),
        )
        self.assertIsNone(self.suspected(HELO + "help\n"))
        # Features every <help> has are never suspect
        (suspects,) = self.profile._suspect_features(HELP).values()
        self.assertNotIn(_Feature("path", None, (NonTerminal("<help>"),)), suspects)
        self.assertNotIn(_Feature("packet", ("Fuzzer", "<hello>"), None), suspects)

    def test_too_few_counterexamples_suspect_nothing(self):
        self._learn(answers=ViolationProfile.MIN_COUNTEREXAMPLES - 1)
        self.assertIsNone(self.suspected(self.AFTER_EHLO))

    def test_a_feature_explaining_no_further_trigger_is_not_suspected(self):
        # <cmd a> rides along on the route of every trigger; <ehlo> explains them all
        self.trigger(EHLO + "cmd a\nok\nhelp\n", ViolationProfile.MIN_TRIGGERS)
        self.answer(HELO + "cmd b\nok\nhelp\nhelptext\n", 3)
        (suspects,) = self.profile._suspect_features(HELP).values()
        self.assertEqual(suspects, {_Feature("packet", ("Fuzzer", "<ehlo>"), None)})

    def test_a_feature_common_in_answers_is_not_suspected(self):
        self.trigger(self.AFTER_EHLO)
        self.answer(self.ANSWERED, 3)
        self.answer(EHLO + "help\nhelptext\n", 3)
        self.trigger(self.AFTER_EHLO, ViolationProfile.MIN_TRIGGERS - 1)
        self.assertIsNone(self.suspected(self.AFTER_EHLO))

    def test_a_suspect_is_retried_after_waits_that_double(self):
        key = GARBAGE_INSTEAD_OF_HELPTEXT
        first_wait = ViolationProfile.FIRST_RETRY_WAIT
        self.assertFalse(self.profile.is_retry_due(HELP, key))
        self._learn()
        # The wait starts once the suspicion arises
        self.assertIsNotNone(self.suspected(self.AFTER_EHLO))
        for _ in range(first_wait - 1):
            self.profile.signal_session_end()
            self.assertFalse(self.profile.is_retry_due(HELP, key))
        self.profile.signal_session_end()
        self.assertTrue(self.profile.is_retry_due(HELP, key))
        self.profile.consume_retry(HELP, key)
        for _ in range(2 * first_wait - 1):
            self.profile.signal_session_end()
            self.assertFalse(self.profile.is_retry_due(HELP, key))
        self.profile.signal_session_end()
        self.assertTrue(self.profile.is_retry_due(HELP, key))

    def test_a_suspect_earlier_packet_rules_the_packet_out(self):
        self._learn()
        # The earlier <ehlo> is suspect by itself, so its content is not
        (suspects,) = self.profile._suspect_features(HELP).values()
        self.assertEqual(
            {feature.kind for feature in suspects if feature.predecessor}, {"packet"}
        )
        self.assertIsNone(self.suspected("hello\nehlo\n"))
        self.assertEqual(
            self.profile.ruled_out_predecessors(),
            {HELP: frozenset({("Fuzzer", "<ehlo>")})},
        )
        # Not while its retry is due, until it is used up
        for _ in range(ViolationProfile.FIRST_RETRY_WAIT):
            self.profile.signal_session_end()
        self.assertEqual(self.profile.ruled_out_predecessors(), {})
        self.profile.consume_retry(HELP, GARBAGE_INSTEAD_OF_HELPTEXT)
        self.assertIn(HELP, self.profile.ruled_out_predecessors())

    def test_a_value_inside_a_regular_expression_is_suspected(self):
        self.trigger(EHLO + "cmd !\n", ViolationProfile.MIN_TRIGGERS, "<ok>")
        for argument in "abc":
            self.answer(EHLO + f"cmd {argument}\nok\n")
        self.assertIsNotNone(self.suspected(EHLO + "cmd !\n"))
        self.assertIsNone(self.suspected(EHLO + "cmd b\n"))
        (suspects,) = self.profile._suspect_features(CMD).values()
        self.assertIn(
            _Feature("value", None, (("<cmd>", "<word>"), ("char", "!"))), suspects
        )

        def levels(messages: str, anchor: tuple[str, ...]) -> set:
            message = last_message(session(self.grammar, messages))
            return {
                level
                for value_anchor, level in value_features(
                    message, literals_of(self.grammar.rules)
                )
                if value_anchor == anchor
            }

        # A value in one regular expression, <word>, gets the same features as one in rules, <argument>;
        # the exact text counts for both, as '!' is a literal of the grammar
        self.assertEqual(
            levels(EHLO + "cmd !\n", ("<cmd>", "<word>")),
            levels(EHLO + "set !\n", ("<set>", "<argument>")),
        )
        literals = literals_of(self.grammar.rules)
        self.assertIn("!", literals)
        self.assertNotIn("[abc!]", literals)

    def test_the_content_of_an_earlier_message_is_suspected(self):
        self.trigger(self.AFTER_BAD_SET, expected="<value>")
        self.answer(EHLO + "set a\nok\nget\nvalue\n", 3)
        self.trigger(
            self.AFTER_BAD_SET, ViolationProfile.MIN_TRIGGERS - 1, expected="<value>"
        )
        (suspects,) = self.profile._suspect_features(GET).values()
        self.assertIn(
            _Feature("path", ("Fuzzer", "<set>"), (NonTerminal("<bad>"),)), suspects
        )
        self.assertIsNotNone(self.suspected(self.AFTER_BAD_SET))
        self.assertIsNone(self.suspected(EHLO + "set b\nok\nget\n"))
        # The <set> with <bad> is suspected as predecessor, so the filter avoids it
        (violation,) = self.profile._suspect_features(GET)
        self.assertEqual(self.suspected(EHLO + "set !\n"), (GET, violation))
        self.assertIsNone(self.suspected(EHLO + "set b\n"))
        self.assertEqual(
            _Feature("path", ("Fuzzer", "<set>"), (NonTerminal("<bad>"),)).describe(),
            "after <set> from Fuzzer with <bad>",
        )
        # A route cannot tell the content of the earlier <set>, so no packet is ruled out
        self.assertEqual(self.profile.ruled_out_predecessors(), {})


def new_algorithm(grammar_name: str = GRAMMAR) -> ProtocolAlgorithm:
    random.seed(0)
    with open(RESOURCES_ROOT / grammar_name) as spec:
        grammar, constraints = parse(spec, use_stdlib=True, use_cache=False)
    assert grammar is not None
    return ProtocolAlgorithm(
        packet_algorithm=SimpleGeneticAlgorithm(
            grammar=grammar, constraints=constraints
        ),
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
        remote_response_timeout=1.0,
    )


def run_sessions(with_profile: bool) -> ProtocolAlgorithm:
    """
    Runs up to SESSIONS sessions, completed or ended by a violation, against a server that sends no more than <cmd>,
    which violates if its argument is <bad>: often enough for the profile to learn and to hold back.
    """
    algorithm = new_algorithm("violation_by_argument.fan")
    if not with_profile:
        algorithm._violation_profile.MIN_SUSPICION_SCORE = float("inf")
    completed = 0
    for _ in algorithm.generate(mode=FuzzingMode.IO):
        completed += 1
        if completed + len(algorithm.violations) >= SESSIONS:
            break
    return algorithm


def learn_help_after_ehlo(algorithm: ProtocolAlgorithm) -> None:
    """Has the profile learn that <help> violates after <ehlo>, and is answered after <helo>."""
    after_ehlo = EHLO + "help\n"
    for messages in [after_ehlo] + [HELO + "help\nhelptext\n"] * 3 + [after_ehlo] * 2:
        tree = session(algorithm.grammar, messages)
        if messages == after_ehlo:
            algorithm._violation_profile.observe_violation(
                tree, garbage_instead_of(tree, "<helptext>")
            )
        else:
            algorithm._violation_profile.observe_answer(tree)
        algorithm._violation_profile.signal_session_end()


class TestViolationAvoidance(unittest.TestCase):
    def test_content_that_triggers_a_violation_is_held_back(self):
        without = run_sessions(with_profile=False)
        learned = run_sessions(with_profile=True)
        self.assertLess(len(learned.violations), len(without.violations))
        self.assertLessEqual(len(learned.violations), ViolationProfile.MIN_TRIGGERS)

    def test_the_filter_lets_a_suspect_through_once_its_retry_is_due(self):
        algorithm = new_algorithm()
        learn_help_after_ehlo(algorithm)
        profile = algorithm._violation_profile
        candidate = last_message(session(algorithm.grammar, EHLO + "help\n"))
        self.assertIsNone(algorithm._packet_coverage_filter.filter(candidate))
        for _ in range(ViolationProfile.FIRST_RETRY_WAIT):
            profile.signal_session_end()
        self.assertIsNotNone(algorithm._packet_coverage_filter.filter(candidate))
        # Only sending the suspect uses the retry up
        self.assertTrue(profile.is_retry_due(HELP, GARBAGE_INSTEAD_OF_HELPTEXT))

    def test_a_step_waiting_to_be_blocked_ends_the_run_with_the_history_derivable(
        self,
    ):
        algorithm = new_algorithm()
        guider = algorithm._packet_selector._guider
        (help_step,) = (
            step
            for step in guider._navigator_instance._rule_steps().values()
            if step.parent == NonTerminal("<exchange_help>")
            and step.packet == NonTerminal("<_packet_help>")
        )
        for _ in range(StepRefusalCounter.REFUSAL_LIMIT):
            guider._step_refusals.count_refusal(help_step, "Extern")
        history = session(algorithm.grammar, EHLO + "help\nhelptext\n")
        algorithm._packet_selector.history_tree = history
        target = (NonTerminal("<exchange_cmd>"),)
        guider.select_next_packet(history, lambda: {target}, lambda: [])
        self.assertTrue(guider.is_guide_to_end)
        self.assertTrue(
            any(True for _ in guider._navigator.get_controlflow_tree(history))
        )
        guider.observe_session_end()
        self.assertIn(help_step, guider._step_refusals.blocked_steps)


class TestRoutingAroundRuledOutPackets(unittest.TestCase):
    """The navigation with <help> ruled out after <ehlo>."""

    HELP_AFTER_EHLO = {HELP: frozenset({("Fuzzer", "<ehlo>")})}

    def setUp(self):
        self.searches: list[tuple[int, bool]] = []
        self.expanded: list[tuple[Symbol, ...]] = []
        search = GrammarNavigator._search
        is_reached = PathSearch._is_reached

        def logged_search(navigator, start, target):
            path = search(navigator, start, target)
            self.searches.append((navigator.comparisons, path is not None))
            return path

        def logged_is_reached(path_search, node):
            self.expanded.append(node.chain())
            return is_reached(path_search, node)

        for owner, name, wrapper in (
            (GrammarNavigator, "_search", logged_search),
            (PathSearch, "_is_reached", logged_is_reached),
        ):
            patcher = mock.patch.object(owner, name, wrapper)
            patcher.start()
            self.addCleanup(patcher.stop)

    def route(self, history: str, k_path: KPath) -> list:
        grammar = new_algorithm().grammar
        navigator = PacketNavigator(
            grammar, ruled_out_predecessors=lambda: self.HELP_AFTER_EHLO
        )
        navigator.set_message_cost(1)
        guide = navigator.astar_tree_including_k_paths(
            tree=session(grammar, history), destination_k_path=k_path
        )
        assert guide is not None
        return guide.route

    def test_the_search_never_goes_beyond_a_predecessor_that_rules_the_target_out(
        self,
    ):
        # <ehlo> is the cheaper way into <greeted>, but rules out <help> after it
        route = self.route(
            "hello\n",
            (NonTerminal("<greeted>"), NonTerminal("<exchange_help>")),
        )
        sent = [step.packet.symbol for step in route if isinstance(step, PlannedPacket)]
        self.assertEqual(
            sent, [NonTerminal("<helo>"), NonTerminal("<ok>"), NonTerminal("<ok>")]
        )
        self.assertFalse(
            any(NonTerminal("<_packet_ehlo>") in chain for chain in self.expanded)
        )

    def test_a_route_to_the_end_only_through_a_ruled_out_packet_is_given_up_at_once(
        self,
    ):
        grammar = new_algorithm().grammar
        quit_packet = PacketNonTerminal("Fuzzer", "Extern", NonTerminal("<quit>"))
        navigator = PacketNavigator(
            grammar,
            ruled_out_predecessors=lambda: {
                quit_packet: frozenset({("Fuzzer", "<ehlo>")})
            },
        )
        navigator.set_message_cost(1)
        route = navigator.astar_search_end_including_k_paths(session(grammar, EHLO))
        assert route is not None
        avoiding, *_ = self.searches
        self.assertEqual(avoiding, (1, False))
        # Ending the run outweighs avoiding <quit>
        self.assertIn(
            quit_packet,
            [step.packet for step in route if isinstance(step, PlannedPacket)],
        )

    def test_a_target_out_of_reach_in_this_run_is_given_up_at_once(self):
        # <helptext> itself can be derived, but only answers <help>
        for target in (NonTerminal("<exchange_help>"), NonTerminal("<helptext>")):
            with self.subTest(target=target):
                self.searches.clear()
                route = self.route(EHLO, (target,))
                self.assertIn(None, route)
                in_this_run, *_ = self.searches
                self.assertEqual(in_this_run, (1, False))


if __name__ == "__main__":
    unittest.main()
