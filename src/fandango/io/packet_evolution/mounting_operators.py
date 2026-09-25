from collections.abc import Callable, Generator
from typing import Optional

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.crossover import CrossoverOperator
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.mutation import MutationOperator
from fandango.io.packet_evolution.packet_mounting import PacketMounting
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree

Evaluation = Generator[
    DerivationTree, None, tuple[float, list[FailingTree], Suggestion]
]


class MountingEvaluator(Evaluator):
    def __init__(self, evaluator: Evaluator, packet_mounting: PacketMounting):
        self.__dict__ = evaluator.__dict__
        self._packet_mounting = packet_mounting

    def evaluate_individual(self, individual: DerivationTree) -> Evaluation:
        canonical_packet = self._packet_mounting.canonical(individual)
        with self._packet_mounting.mounted(canonical_packet):
            solutions, evaluation = GeneratorWithReturn(
                super().evaluate_individual(canonical_packet.get_root())
            ).collect()
        for _solution in solutions:
            yield individual
        return evaluation


class MountingCrossover(CrossoverOperator):
    def __init__(
        self, crossover_operator: CrossoverOperator, packet_mounting: PacketMounting
    ):
        self._crossover_operator = crossover_operator
        self._packet_mounting = packet_mounting

    def crossover(
        self, grammar: Grammar, parent1: DerivationTree, parent2: DerivationTree
    ) -> Optional[tuple[DerivationTree, DerivationTree]]:
        with self._packet_mounting.mounted(parent1, parent2):
            return self._crossover_operator.crossover(grammar, parent1, parent2)


class MountingMutation(MutationOperator):
    def __init__(
        self, mutation_operator: MutationOperator, packet_mounting: PacketMounting
    ):
        self._mutation_operator = mutation_operator
        self._packet_mounting = packet_mounting

    def mutate(
        self,
        individual: DerivationTree,
        grammar: Grammar,
        evaluate_func: Callable[[DerivationTree], Evaluation],
    ) -> Generator[DerivationTree, None, DerivationTree]:
        canonical_packet = self._packet_mounting.canonical(individual)
        with self._packet_mounting.mounted(canonical_packet):
            solutions, mutated = GeneratorWithReturn(
                self._mutation_operator.mutate(canonical_packet, grammar, evaluate_func)
            ).collect()
        yield from solutions
        return individual if mutated is canonical_packet else mutated
