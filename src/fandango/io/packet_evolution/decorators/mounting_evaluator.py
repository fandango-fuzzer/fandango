from collections.abc import Generator
from typing import Any

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.evaluation import Evaluator
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.tree import DerivationTree


class MountingEvaluator(Evaluator):
    """Evaluates packets mounted into the session."""

    def __init__(self, packet_mounter: PacketMounter, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._packet_mounter = packet_mounter

    def evaluate_individual(
        self, individual: DerivationTree
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree], Suggestion]]:
        with self._packet_mounter.mounted_context(individual) as mounted_packet:
            solutions, evaluation = GeneratorWithReturn(
                super().evaluate_individual(mounted_packet.get_root())
            ).collect()
        if solutions:
            yield individual
        return evaluation
