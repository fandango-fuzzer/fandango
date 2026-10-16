from collections.abc import Generator, Sequence
from typing import Callable, Optional

from fandango.constraints.constraint import Constraint
from fandango.constraints.failing_tree import (
    ApplyAllSuggestions,
    FailingTree,
    Suggestion,
)
from fandango.constraints.forall import ForallConstraint
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
from fandango.logger import LOGGER, print_exception


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
            scoped[
                self._constraint_scopes.analyse_scope(packet_symbol, constraint)
            ].append(constraint)
        inside_constraints = scoped[ConstraintScope.INSIDE]
        crossing_constraints = scoped[ConstraintScope.CROSSING]
        unrelated_constraints = scoped[ConstraintScope.UNRELATED]
        message_fitness, message_failing, message_suggestion = (
            super()._evaluate_constraints(self._mounted_packet, inside_constraints)
        )
        session_fitness, session_failing, session_suggestion = (
            self._evaluate_crossing_constraints(individual, crossing_constraints)
        )
        fitness = (
            message_fitness * len(inside_constraints)
            + session_fitness * len(crossing_constraints)
            + len(unrelated_constraints)
        ) / len(constraints)
        return (
            fitness,
            [*message_failing, *session_failing],
            ApplyAllSuggestions([message_suggestion, session_suggestion]),
        )

    def _evaluate_crossing_constraints(
        self, individual: DerivationTree, constraints: Sequence[Constraint]
    ) -> tuple[float, list[FailingTree], Suggestion]:
        """Evaluates a forall over instances of a symbol only on the instances that contain or lie inside the
        mounted packet. Meaning all instances along the parents of the mounted packet."""
        assert self._mounted_packet is not None
        per_instance = [
            constraint
            for constraint in constraints
            if self._constraint_scopes.per_instance_search_scope(constraint) is not None
        ]
        if not per_instance:
            return super()._evaluate_constraints(individual, constraints)
        fitness, failing_trees, suggestion = super()._evaluate_constraints(
            individual, [c for c in constraints if c not in per_instance]
        )
        fitness *= len(constraints) - len(per_instance)
        suggestions = [suggestion]
        for constraint in per_instance:
            assert isinstance(constraint, ForallConstraint)
            search_scope = self._constraint_scopes.per_instance_search_scope(constraint)
            assert search_scope is not None
            try:
                result = constraint.fitness_over(
                    individual, self._instances_around_packet(search_scope)
                )
            except Exception as e:
                LOGGER.error(
                    f"Error evaluating constraint {constraint.format_as_spec()}"
                )
                print_exception(e)
                continue
            fitness += result.fitness()
            failing_trees.extend(result.failing_trees)
            if result.suggestion is not None:
                suggestions.append(result.suggestion)
            self._checks_made += 1
        return (
            fitness / len(constraints),
            failing_trees,
            ApplyAllSuggestions(suggestions),
        )

    def _instances_around_packet(self, symbol: NonTerminal) -> list[DerivationTree]:
        """The instances of symbol inside the mounted packet and the ancestors of it that are one."""
        assert self._mounted_packet is not None
        instances = list(self._mounted_packet.find_subtrees(symbol))
        ancestor = self._mounted_packet.parent
        while ancestor is not None:
            if ancestor.symbol == symbol:
                instances.append(ancestor)
            ancestor = ancestor.parent
        return instances
