from collections.abc import Generator
from typing import Any, Optional, Callable

from fandango.constraints.constraint import Constraint
from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.constraints.soft import SoftValue
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.evaluation import Evaluator
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language import Grammar
from fandango.language.tree import DerivationTree


class MountingEvaluator(Evaluator):
    """Evaluates packets mounted into the session."""

    def __init__(
        self,
        packet_mounter: PacketMounter,
        grammar: Grammar,
        constraints: list[Constraint | SoftValue],
        expected_fitness: float,
        diversity_k: int,
        diversity_weight: float,
        stop_criterion: Optional[Callable[[DerivationTree], bool]] = None,
        use_fcc: bool = False,
        put: Optional[str] = None,
        put_args: Optional[list[str]] = None,
    ):
        super().__init__(
            grammar=grammar,
            constraints=constraints,
            expected_fitness=expected_fitness,
            diversity_k=diversity_k,
            diversity_weight=diversity_weight,
            stop_criterion=stop_criterion,
            use_fcc=use_fcc,
            put=put,
            put_args=put_args,
        )
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
