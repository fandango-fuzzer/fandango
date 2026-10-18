import random
import unittest
from unittest.mock import patch

from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse
from tests.utils import RESOURCES_ROOT

SESSIONS = 4
FALLBACK_MAX_GENERATIONS = 3


class _SessionsEnded(Exception):
    pass


class TestUnsatisfiablePacket(unittest.TestCase):
    def test_session_ends_within_bounded_generations(self):
        random.seed(0)
        with open(RESOURCES_ROOT / "unsatisfiable_packet.fan") as spec:
            grammar, constraints = parse(spec, use_stdlib=True, use_cache=False)
        assert grammar is not None
        packet_algorithm = SimpleGeneticAlgorithm(
            grammar=grammar, constraints=constraints
        )
        algorithm = ProtocolAlgorithm(
            packet_algorithm=packet_algorithm,
            coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
            remote_response_timeout=1.0,
        )
        algorithm.FALLBACK_MAX_GENERATIONS = FALLBACK_MAX_GENERATIONS

        ended_sessions = []
        selector = algorithm._packet_selector
        signal_session_end = selector.signal_session_end

        def counting_signal_session_end(generation_failed=False):
            ended_sessions.append(str(selector.history_tree))
            signal_session_end(generation_failed)
            if len(ended_sessions) >= SESSIONS:
                raise _SessionsEnded()

        with (
            patch.object(
                packet_algorithm, "generate", wraps=packet_algorithm.generate
            ) as generate,
            patch.object(
                selector, "signal_session_end", side_effect=counting_signal_session_end
            ),
            self.assertRaises(_SessionsEnded),
        ):
            for _ in algorithm.generate(mode=FuzzingMode.IO):
                pass

        self.assertTrue(all(session == "hello\n" for session in ended_sessions))
        self.assertTrue(generate.call_args_list)
        self.assertNotIn(
            None,
            [call.kwargs.get("max_generations") for call in generate.call_args_list],
        )
        refusals = algorithm._packet_selector._guider._step_refusals
        self.assertTrue(refusals.blocked_steps)
