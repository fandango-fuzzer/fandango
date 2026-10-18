import random
import unittest

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

        generations_per_call = []
        generate_packet = packet_algorithm.generate

        def counting_generate(max_generations=None, mode=FuzzingMode.COMPLETE):
            generations_per_call.append(max_generations)
            return generate_packet(max_generations=max_generations, mode=mode)

        packet_algorithm.generate = counting_generate

        ended_sessions = []
        selector = algorithm._packet_selector
        signal_session_end = selector.signal_session_end

        def counting_signal_session_end(generation_failed=False):
            ended_sessions.append(str(selector.history_tree))
            signal_session_end(generation_failed)
            if len(ended_sessions) >= SESSIONS:
                raise _SessionsEnded()

        selector.signal_session_end = counting_signal_session_end

        with self.assertRaises(_SessionsEnded):
            for _ in algorithm.generate(mode=FuzzingMode.IO):
                pass

        self.assertTrue(all(session == "hello\n" for session in ended_sessions))
        self.assertNotIn(None, generations_per_call)
        refusals = algorithm._packet_selector._guider._step_refusals
        self.assertTrue(refusals.blocked_steps)
