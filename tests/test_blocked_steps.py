import itertools
import random
import unittest

from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.forecasting.packetforecaster import PacketForecaster
from fandango.io.navigation.selection.step_refusals import StepRefusals
from fandango.io.navigation.step import Step
from fandango.language.grammar import FuzzingMode, ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from tests.utils import RESOURCES_ROOT

SESSIONS = 30


def step_of_last_message(grammar: Grammar, messages: str) -> Step:
    """The step that produced the last of the messages, as the forecaster observes it."""
    history = grammar.parse(
        messages, mode=ParsingMode.INCOMPLETE, include_controlflow=True
    )
    assert history is not None
    (step,) = PacketForecaster(grammar).predict(history).message_steps[-1]
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
        self.refusals = self.algorithm._packet_selector._step_refusals
        self.ok_after_a = step_of_last_message(grammar, "hello\na\nok\n")
        self.ok_after_c = step_of_last_message(grammar, "hello\nc\nok\n")
        self.note = step_of_last_message(grammar, "hello\nc\nok\nbye\nnote\n")

    def _run_sessions(self) -> list[tuple[str, frozenset[Step]]]:
        """Each session's messages and the steps blocked after it."""
        sessions = itertools.islice(
            self.algorithm.generate(mode=FuzzingMode.IO), SESSIONS
        )
        return [(str(session), self.refusals.blocked_steps) for session in sessions]

    def test_refused_occurrence_is_blocked(self):
        blocked_per_session = [blocked for _, blocked in self._run_sessions()]
        self.assertTrue(
            any(self.ok_after_a in blocked for blocked in blocked_per_session)
        )

    def test_only_the_refused_steps_are_blocked(self):
        for _, blocked in self._run_sessions():
            self.assertLessEqual(blocked, {self.ok_after_a, self.note})
            self.assertNotIn(self.ok_after_c, blocked)

    def test_stops_once_only_blocked_targets_are_left(self):
        sessions = self._run_sessions()
        self.assertLess(len(sessions), SESSIONS)
        self.assertTrue(any("c\nok\n" in text for text, _ in sessions))
        _, blocked_at_stop = sessions[-1]
        self.assertEqual(blocked_at_stop, {self.ok_after_a, self.note})


STEP = Step(NonTerminal("<rule>"), (), NonTerminal("<_packet_ok>"))


class TestStepRefusals(unittest.TestCase):
    def setUp(self):
        self.refusals = StepRefusals()

    def _refuse(self, times: int) -> None:
        for _ in range(times):
            self.refusals.count_refusal(STEP, "Extern")

    def _end_sessions(self, count: int) -> None:
        for _ in range(count):
            self.refusals.signal_session_end()

    def test_blocks_at_the_refusal_limit(self):
        self._refuse(StepRefusals.REFUSAL_LIMIT - 1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)
        self._refuse(1)
        self.assertIn(STEP, self.refusals.blocked_steps)

    def test_observation_resets_the_refusals(self):
        self._refuse(StepRefusals.REFUSAL_LIMIT - 1)
        self.refusals.observe_taken(STEP, "Extern")
        self._refuse(StepRefusals.REFUSAL_LIMIT - 1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)

    def test_observation_unblocks(self):
        self._refuse(StepRefusals.REFUSAL_LIMIT)
        self.refusals.observe_taken(STEP, "Extern")
        self.assertNotIn(STEP, self.refusals.blocked_steps)

    def test_block_expires_after_its_sessions(self):
        self._refuse(StepRefusals.REFUSAL_LIMIT)
        self._end_sessions(StepRefusals.FIRST_REFUSAL_SESSIONS - 1)
        self.assertIn(STEP, self.refusals.blocked_steps)
        self._end_sessions(1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)

    def test_one_refusal_after_expiry_blocks_twice_as_long(self):
        self._refuse(StepRefusals.REFUSAL_LIMIT)
        self._end_sessions(StepRefusals.FIRST_REFUSAL_SESSIONS)
        self._refuse(1)
        self._end_sessions(2 * StepRefusals.FIRST_REFUSAL_SESSIONS - 1)
        self.assertIn(STEP, self.refusals.blocked_steps)
        self._end_sessions(1)
        self.assertNotIn(STEP, self.refusals.blocked_steps)


if __name__ == "__main__":
    unittest.main()
