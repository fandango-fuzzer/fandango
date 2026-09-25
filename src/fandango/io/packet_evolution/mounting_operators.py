from collections.abc import Callable, Generator
from typing import Optional

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.crossover import CrossoverOperator
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.mutation import MutationOperator
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree

Evaluation = Generator[
    DerivationTree, None, tuple[float, list[FailingTree], Suggestion]
]


class MountingEvaluator(Evaluator):
    def __init__(self, evaluator: Evaluator, packet_mounter: PacketMounter):
        self.__dict__ = evaluator.__dict__
        self._packet_mounter = packet_mounter

    def evaluate_individual(self, individual: DerivationTree) -> Evaluation:
        first_seen_packet = self._packet_mounter.first_seen_equal(individual)
        with self._packet_mounter.mount_context(first_seen_packet):
            solutions, evaluation = GeneratorWithReturn(
                super().evaluate_individual(first_seen_packet.get_root())
            ).collect()
        for _solution in solutions:
            yield individual
        return evaluation


class MountingCrossover(CrossoverOperator):
    def __init__(
        self, crossover_operator: CrossoverOperator, packet_mounter: PacketMounter
    ):
        self._crossover_operator = crossover_operator
        self._packet_mounter = packet_mounter

    def crossover(
        self, grammar: Grammar, parent1: DerivationTree, parent2: DerivationTree
    ) -> Optional[tuple[DerivationTree, DerivationTree]]:
        with self._packet_mounter.mount_context(parent1, parent2):
            return self._crossover_operator.crossover(grammar, parent1, parent2)


class MountingMutation(MutationOperator):
    def __init__(
        self, mutation_operator: MutationOperator, packet_mounter: PacketMounter
    ):
        self._mutation_operator = mutation_operator
        self._packet_mounter = packet_mounter

    def mutate(
        self,
        individual: DerivationTree,
        grammar: Grammar,
        evaluate_func: Callable[[DerivationTree], Evaluation],
    ) -> Generator[DerivationTree, None, DerivationTree]:
        first_seen_packet = self._packet_mounter.first_seen_equal(individual)
        with self._packet_mounter.mount_context(first_seen_packet):
            solutions, mutated = GeneratorWithReturn(
                self._mutation_operator.mutate(
                    first_seen_packet, grammar, evaluate_func
                )
            ).collect()
        yield from solutions
        return individual if mutated is first_seen_packet else mutated
