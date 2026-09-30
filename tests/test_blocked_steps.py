import itertools
import random
import unittest

from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.step import Step
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal
from tests.utils import RESOURCES_ROOT

SESSIONS = 30


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
        selector = self.algorithm._packet_selector
        self.refusals = selector._step_refusals
        rule_body = selector._guider._navigator._state_rules[NonTerminal("<rule>")]
        a_ok, _a_err, c_ok = rule_body.alternatives
        ok = NonTerminal("<_packet_ok>")
        self.ok_after_a = Step(
            NonTerminal("<rule>"), (rule_body.to_symbol(), a_ok.to_symbol()), ok
        )
        self.ok_after_c = Step(
            NonTerminal("<rule>"), (rule_body.to_symbol(), c_ok.to_symbol()), ok
        )

    def _run_sessions(self) -> list[tuple[str, frozenset[Step]]]:
        """Each session's messages and the steps blocked after it."""
        sessions = itertools.islice(
            self.algorithm.generate(mode=FuzzingMode.IO), SESSIONS
        )
        return [(str(session), self.refusals.blocked_steps) for session in sessions]

    def test_refused_occurrence_is_blocked(self):
        blocked_per_session = [blocked for _, blocked in self._run_sessions()]
        self.assertIn(frozenset([self.ok_after_a]), blocked_per_session)

    def test_only_the_refused_occurrence_is_blocked(self):
        for _, blocked in self._run_sessions():
            self.assertLessEqual(blocked, {self.ok_after_a})
            self.assertNotIn(self.ok_after_c, blocked)

    def test_stops_once_only_blocked_targets_are_left(self):
        sessions = self._run_sessions()
        self.assertLess(len(sessions), SESSIONS)
        self.assertIn("hello\nc\nok\nquit\n", [text for text, _ in sessions])
        _, blocked_at_stop = sessions[-1]
        self.assertEqual(blocked_at_stop, {self.ok_after_a})


if __name__ == "__main__":
    unittest.main()
