from typing import Optional

from fandango.evolution.crossover import CrossoverOperator
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree


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
