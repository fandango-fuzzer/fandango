import itertools
import random
import unittest

from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.forecasting.packetforecaster import PacketForecaster
from fandango.io.navigation.selection.step_refusals import StepRefusalCounter
from fandango.io.navigation.step import Step
from fandango.language.grammar import FuzzingMode, ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from tests.utils import RESOURCES_ROOT

SESSIONS = 30


def step_of_last_message(grammar: Grammar, messages: str) -> Step:
    """The step that produced the last of the messages, as the forecaster observes it."""
    history = grammar.parse(
        messages, mode=ParsingMode.INCOMPLETE, include_controlflow=True
    )
    assert history is not None
    (step,) = PacketForecaster(grammar).predict(history).last_message_steps
    return step


class TestBlockedSteps(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        with open(RESOURCES_ROOT / "blocked_steps.fan") as spec:
            grammar, constraints = parse(spec, use_stdlib=True, use_cache=False)
        assert grammar is not None
        self.algorithm = ProtocolAlgorithm(
            packet_algorithm=SimpleGeneticAlgorithm(
                grammar=grammar, constraints=constraints
            ),
            coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
            remote_response_timeout=1.0,
        )
        self.refusals = self.algorithm._packet_selector._guider._step_refusals
        self.ok_after_a = step_of_last_message(grammar, "hello\na\nok\n")
        self.ok_after_c = step_of_last_message(grammar, "hello\nc\nok\n")
        self.note = step_of_last_message(grammar, "hello\nc\nok\nbye\nnote\n")
        # The server answering <bye> with <done> refuses <note>, or <notes> if the route ended there.
        self.notes = Step(self.note.path[:-2])
        # Steps the server never takes are blocked wherever their calling rule is used.
        self.refusable = {
            step.as_in_calling_last_rule()
            for step in (self.ok_after_a, self.note, self.notes)
        }

    def _run_sessions(self) -> list[tuple[str, frozenset[Step]]]:
        """Each session's messages and the steps blocked after it."""
        sessions = itertools.islice(
            self.algorithm.generate(mode=FuzzingMode.IO), SESSIONS
        )
        return [(str(session), self.refusals.blocked_steps) for session in sessions]

    def test_only_the_refused_steps_are_blocked(self):
        for _, blocked in self._run_sessions():
            self.assertLessEqual(blocked, self.refusable)
            self.assertNotIn(self.ok_after_c, blocked)

    def test_stops_once_only_blocked_targets_are_left(self):
        sessions = self._run_sessions()
        self.assertLess(len(sessions), SESSIONS)
        self.assertTrue(any("c\nok\n" in text for text, _ in sessions))
        _, blocked_at_stop = sessions[-1]
        self.assertLessEqual(blocked_at_stop, self.refusable)
        ok_after_a, note, notes = (
            step.as_in_calling_last_rule()
            for step in (self.ok_after_a, self.note, self.notes)
        )
        self.assertTrue(
            {ok_after_a, note} <= blocked_at_stop
            or {ok_after_a, notes} <= blocked_at_stop
        )


class TestUnansweredStep(unittest.TestCase):
    def test_step_is_blocked_when_the_run_keeps_ending_without_its_answer(self):
        random.seed(0)
        with open(RESOURCES_ROOT / "refused_reply.fan") as spec:
            grammar, constraints = parse(spec, use_stdlib=True, use_cache=False)
        assert grammar is not None
        algorithm = ProtocolAlgorithm(
            packet_algorithm=SimpleGeneticAlgorithm(
                grammar=grammar, constraints=constraints
            ),
            coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
            remote_response_timeout=1.0,
        )
        refusals = algorithm._packet_selector._guider._step_refusals
        ok_after_a = step_of_last_message(
            grammar, "hello\na\nok_a\n"
        ).as_in_calling_last_rule()
        blocked_per_session = [
            refusals.blocked_steps
            for _ in itertools.islice(algorithm.generate(mode=FuzzingMode.IO), SESSIONS)
        ]
        # Generation stops once only blocked targets are left, so the last block shows only after it.
        blocked_per_session.append(refusals.blocked_steps)
        self.assertTrue(any(ok_after_a in blocked for blocked in blocked_per_session))


class TestStep(unittest.TestCase):
    PATH = (
        NonTerminal("<start>"),
        NonTerminal("<__concatenation:1>"),
        NonTerminal("<rule>"),
        NonTerminal("<__alternative:1>"),
        NonTerminal("<__concatenation:2>"),
        NonTerminal("<inner>"),
        NonTerminal("<__concatenation:3>"),
        NonTerminal("<_packet_a>"),
    )

    def test_of_path_starts_at_the_caller_of_the_nearest_recursive_call(self):
        def inner_derives_rule(caller: NonTerminal, callee: NonTerminal) -> bool:
            return (caller, callee) == (NonTerminal("<rule>"), NonTerminal("<inner>"))

        self.assertEqual(
            Step.of_path(self.PATH, inner_derives_rule), Step(self.PATH[2:])
        )

    def test_of_path_starts_at_the_start_symbol_without_a_recursive_call(self):
        self.assertEqual(
            Step.of_path(self.PATH, lambda caller, callee: False), Step(self.PATH)
        )

    def test_of_message_tells_occurrences_of_the_same_packet_apart(self):
        """
        <rule> -> <__alternative:1> -> <__concatenation:2> -> <_packet_a>
               -> <__star:1> -> <_packet_a>
        """
        in_concatenation = DerivationTree(NonTerminal("<_packet_a>"))
        in_star = DerivationTree(NonTerminal("<_packet_a>"))
        DerivationTree(
            NonTerminal("<rule>"),
            [
                DerivationTree(
                    NonTerminal("<__alternative:1>"),
                    [
                        DerivationTree(
                            NonTerminal("<__concatenation:2>"), [in_concatenation]
                        )
                    ],
                ),
                DerivationTree(NonTerminal("<__star:1>"), [in_star]),
            ],
        )
        never = lambda caller, callee: False  # noqa: E731
        self.assertEqual(
            Step.of_message(in_concatenation, never),
            Step(
                (
                    NonTerminal("<rule>"),
                    NonTerminal("<__alternative:1>"),
                    NonTerminal("<__concatenation:2>"),
                    NonTerminal("<_packet_a>"),
                )
            ),
        )
        self.assertEqual(
            Step.of_message(in_star, never),
            Step(
                (
                    NonTerminal("<rule>"),
                    NonTerminal("<__star:1>"),
                    NonTerminal("<_packet_a>"),
                )
            ),
        )


STEP = Step((NonTerminal("<rule>"), NonTerminal("<_packet_ok>")))


class TestStepRefusals(unittest.TestCase):
    def setUp(self):
        self.refusals = StepRefusalCounter()

    def _refuse(self, times: int) -> None:
        for _ in range(times):
            self.refusals.count_refusal(STEP, "Extern")

    def _end_sessions(self, count: int) -> None:
        for _ in range(count):
            self.refusals.signal_session_end()

    def test_blocks_at_the_refusal_limit(self):
        self._refuse(StepRefusalCounter.REFUSAL_LIMIT - 1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)
        self._refuse(1)
        self.assertIn(STEP, self.refusals.blocked_steps)

    def test_observation_resets_the_refusals(self):
        self._refuse(StepRefusalCounter.REFUSAL_LIMIT - 1)
        self.refusals.observe_taken(STEP, "Extern")
        self._refuse(StepRefusalCounter.REFUSAL_LIMIT - 1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)

    def test_observation_unblocks(self):
        self._refuse(StepRefusalCounter.REFUSAL_LIMIT)
        self.refusals.observe_taken(STEP, "Extern")
        self.assertNotIn(STEP, self.refusals.blocked_steps)

    def test_step_taken_in_the_session_is_blocked_at_its_end(self):
        self.refusals.observe_taken(STEP, "Extern")
        self._refuse(StepRefusalCounter.REFUSAL_LIMIT)
        self.assertNotIn(STEP, self.refusals.blocked_steps)
        self.assertTrue(self.refusals.is_block_deferred(STEP))
        self._end_sessions(1)
        self.assertIn(STEP, self.refusals.blocked_steps)
        self.assertFalse(self.refusals.is_block_deferred(STEP))

    def test_step_never_taken_is_blocked_in_every_context(self):
        here = Step(
            (NonTerminal("<a>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        there = Step(
            (NonTerminal("<b>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        self.refusals.count_refusal(here, "Extern")
        self.refusals.count_refusal(there, "Extern")
        self.assertEqual(self.refusals.blocked_steps, frozenset())
        self.refusals.count_refusal(here, "Extern")
        self.assertEqual(self.refusals.blocked_steps, frozenset([STEP]))
        self.refusals.observe_taken(there, "Extern")
        self.assertEqual(self.refusals.blocked_steps, frozenset())

    def test_repeat_cost_rises_with_takes_up_to_its_cap(self):
        step = Step(
            (NonTerminal("<a>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        for takes in range(1, 4 * StepRefusalCounter.REPEAT_STEP + 1):
            self.refusals.observe_taken(step, "Extern")
            cost = min(
                StepRefusalCounter.REPEAT_COST, takes // StepRefusalCounter.REPEAT_STEP
            )
            self.assertEqual(
                self.refusals.repeat_costs(),
                {step.as_in_calling_last_rule(): cost} if cost else {},
            )

    def test_step_taken_somewhere_is_blocked_only_where_refused(self):
        here = Step(
            (NonTerminal("<a>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        there = Step(
            (NonTerminal("<b>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        self.refusals.observe_taken(there, "Extern")
        for _ in range(StepRefusalCounter.REFUSAL_LIMIT):
            self.refusals.count_refusal(here, "Extern")
        self.assertEqual(self.refusals.blocked_steps, frozenset([here]))

    def test_step_refused_where_it_was_taken_is_blocked_wherever_its_rule_is_used(
        self,
    ):
        here = Step(
            (NonTerminal("<a>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        there = Step(
            (NonTerminal("<b>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        self.refusals.observe_taken(there, "Extern")
        self._end_sessions(1)
        self.refusals.count_refusal(there, "Extern")
        for _ in range(StepRefusalCounter.REFUSAL_LIMIT - 1):
            self.assertEqual(self.refusals.blocked_steps, frozenset())
            self.refusals.count_refusal(here, "Extern")
        self.assertEqual(
            self.refusals.blocked_steps, frozenset([here.as_in_calling_last_rule()])
        )

    def test_block_expires_after_its_sessions(self):
        self._refuse(StepRefusalCounter.REFUSAL_LIMIT)
        self._end_sessions(StepRefusalCounter.FIRST_REFUSAL_SESSIONS - 1)
        self.assertIn(STEP, self.refusals.blocked_steps)
        self._end_sessions(1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)

    def test_one_refusal_after_expiry_blocks_twice_as_long(self):
        self._refuse(StepRefusalCounter.REFUSAL_LIMIT)
        self._end_sessions(StepRefusalCounter.FIRST_REFUSAL_SESSIONS)
        self._refuse(1)
        self._end_sessions(2 * StepRefusalCounter.FIRST_REFUSAL_SESSIONS - 1)
        self.assertIn(STEP, self.refusals.blocked_steps)
        self._end_sessions(1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)

    def test_take_restarts_the_block_duration_of_the_rule_step(self):
        here = Step(
            (NonTerminal("<a>"), NonTerminal("<rule>"), NonTerminal("<_packet_ok>"))
        )
        for _ in range(StepRefusalCounter.REFUSAL_LIMIT):
            self.refusals.count_refusal(here, "Extern")
        self._end_sessions(StepRefusalCounter.FIRST_REFUSAL_SESSIONS)
        self.refusals.observe_taken(here, "Extern")
        self._end_sessions(1)
        for _ in range(StepRefusalCounter.REFUSAL_LIMIT):
            self.refusals.count_refusal(here, "Extern")
        self.assertIn(STEP, self.refusals.blocked_steps)
        self._end_sessions(StepRefusalCounter.FIRST_REFUSAL_SESSIONS)
        self.assertNotIn(STEP, self.refusals.blocked_steps)


if __name__ == "__main__":
    unittest.main()
