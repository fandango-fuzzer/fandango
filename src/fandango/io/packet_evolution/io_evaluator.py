from collections.abc import Generator, Sequence
from typing import Callable, Optional

from fandango.constraints.constraint import Constraint
from fandango.constraints.failing_tree import (
    ApplyAllSuggestions,
    FailingTree,
    Suggestion,
)
from fandango.constraints.soft import SoftValue
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.evaluation import Evaluator
from fandango.io.constraints.constraint_scope import (
    ConstraintScope,
    ConstraintScopeAnalyzer,
)
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class IoEvaluator(Evaluator):
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
        self._constraint_scopes = ConstraintScopeAnalyzer(self._grammar)
        self._mounted_packet: Optional[DerivationTree] = None

    def evaluate_individual(
        self, individual: DerivationTree
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree], Suggestion]]:
        with self._packet_mounter.mounted_context(individual) as mounted_packet:
            self._mounted_packet = mounted_packet
            try:
                solutions, evaluation = GeneratorWithReturn(
                    super().evaluate_individual(mounted_packet.get_root())
                ).collect()
            finally:
                self._mounted_packet = None
        if solutions:
            yield individual
        return evaluation

    def _evaluate_constraints(
        self, individual: DerivationTree, constraints: Sequence[Constraint]
    ) -> tuple[float, list[FailingTree], Suggestion]:
        if (
            self._mounted_packet is None
            or not constraints
            or not isinstance(self._mounted_packet.symbol, NonTerminal)
        ):
            return super()._evaluate_constraints(individual, constraints)
        scoped: dict[ConstraintScope, list[Constraint]] = {
            scope: [] for scope in ConstraintScope
        }
        packet_symbol = self._mounted_packet.symbol
        assert isinstance(packet_symbol, NonTerminal)
        for constraint in constraints:
            scoped[self._constraint_scopes.scope(packet_symbol, constraint)].append(
                constraint
            )
        message_constraints = scoped[ConstraintScope.INSIDE]
        session_constraints = scoped[ConstraintScope.CROSSING]
        unrelated_constraints = scoped[ConstraintScope.UNRELATED]
        message_fitness, message_failing, message_suggestion = (
            super()._evaluate_constraints(self._mounted_packet, message_constraints)
        )
        session_fitness, session_failing, session_suggestion = (
            super()._evaluate_constraints(individual, session_constraints)
        )
        fitness = (
            message_fitness * len(message_constraints)
            + session_fitness * len(session_constraints)
            + len(unrelated_constraints)
        ) / len(constraints)
        return (
            fitness,
            [*message_failing, *session_failing],
            ApplyAllSuggestions([message_suggestion, session_suggestion]),
        )
