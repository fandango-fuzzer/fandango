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
        with self._packet_mounter.mounted_context(individual) as mounted_packet:
            solutions, evaluation = GeneratorWithReturn(
                super().evaluate_individual(mounted_packet.get_root())
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
        with (
            self._packet_mounter.mounted_context(parent1) as mounted_parent1,
            self._packet_mounter.mounted_context(parent2) as mounted_parent2,
        ):
            children = self._crossover_operator.crossover(
                grammar, mounted_parent1, mounted_parent2
            )
        if children is None:
            return None
        child1, child2 = children
        return (
            parent1 if child1 is mounted_parent1 else child1,
            parent2 if child2 is mounted_parent2 else child2,
        )


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
        with self._packet_mounter.mounted_context(individual) as mounted_packet:
            solutions, mutated = GeneratorWithReturn(
                self._mutation_operator.mutate(mounted_packet, grammar, evaluate_func)
            ).collect()
        yield from solutions
        return individual if mutated is mounted_packet else mutated
