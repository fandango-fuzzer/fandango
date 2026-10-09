from collections.abc import Callable, Generator

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.mutation import MutationOperator
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree


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
        evaluate_func: Callable[
            [DerivationTree],
            Generator[
                DerivationTree, None, tuple[float, list[FailingTree], Suggestion]
            ],
        ],
    ) -> Generator[DerivationTree, None, DerivationTree]:
        with self._packet_mounter.mounted_context(individual) as mounted_packet:
            solutions, mutated = GeneratorWithReturn(
                self._mutation_operator.mutate(mounted_packet, grammar, evaluate_func)
            ).collect()
            mutated = self._packet_mounter.original(mutated)
        yield from solutions
        return mutated
