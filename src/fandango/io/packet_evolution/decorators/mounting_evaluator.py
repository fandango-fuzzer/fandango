from collections.abc import Generator
from typing import Optional

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.evaluation import AbstractEvaluator
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.tree import DerivationTree


class MountingEvaluator(AbstractEvaluator):
    """Evaluates packets mounted into the session, with the evaluator it decorates."""

    def __init__(self, evaluator: AbstractEvaluator, packet_mounter: PacketMounter):
        self._evaluator = evaluator
        self._packet_mounter = packet_mounter

    @property
    def expected_fitness(self) -> float:
        return self._evaluator.expected_fitness

    @property
    def stop_criterion_met(self) -> bool:
        return self._evaluator.stop_criterion_met

    @property
    def uses_diversity_bonus(self) -> bool:
        return self._evaluator.uses_diversity_bonus

    def evaluate_individual(
        self, individual: DerivationTree
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree], Suggestion]]:
        with self._packet_mounter.mounted_context(individual) as mounted_packet:
            solutions, evaluation = GeneratorWithReturn(
                self._evaluator.evaluate_individual(mounted_packet.get_root())
            ).collect()
        if solutions:
            yield individual
        return evaluation

    def compute_diversity_bonus(
        self,
        individuals: list[DerivationTree],
        fill_up: Optional[list[DerivationTree]] = None,
    ) -> list[float]:
        return self._evaluator.compute_diversity_bonus(individuals, fill_up)

    def get_fitness_check_count(self) -> int:
        return self._evaluator.get_fitness_check_count()

    def flush_fitness_cache(self) -> None:
        self._evaluator.flush_fitness_cache()

    def clear_constraint_caches(self) -> None:
        self._evaluator.clear_constraint_caches()

    def reset(self) -> None:
        self._evaluator.reset()
