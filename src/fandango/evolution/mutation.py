# mutation.py
import random
from abc import ABC, abstractmethod
from typing import Callable, List, Tuple

from fandango.constraints.fitness import FailingTree
from fandango.language.grammar import DerivationTree, Grammar


class MutationOperator(ABC):
    @abstractmethod
    def mutate(
        self,
        individual: DerivationTree,
        grammar: Grammar,
        evaluate_func: Callable[[DerivationTree], Tuple[float, List[FailingTree]]],
    ) -> DerivationTree:
        """
        Abstract method to perform mutation on an individual.

        :param individual: The individual (DerivationTree) to mutate.
        :param grammar: The Grammar used to generate new subtrees.
        :param evaluate_func: A function that, given an individual, returns a tuple (fitness, failing_trees).
        :return: A new (mutated) DerivationTree.
        """
        pass


class SimpleMutation(MutationOperator):
    def mutate(
        self,
        individual: DerivationTree,
        grammar: Grammar,
        evaluate_func: Callable[[DerivationTree], Tuple[float, List[FailingTree]]],
    ) -> DerivationTree:
        """
        Default mutation operator: evaluates the individual, selects a failing subtree
        (if any), and replaces it with a newly fuzzed subtree generated from the grammar.
        """
        # Get fitness and failing trees from the evaluation function
        _, failing_trees = evaluate_func(individual)

        # Collect the failing subtrees
        failing_subtrees = [ft.tree for ft in failing_trees]

        # If there is nothing to mutate, return the individual as is.
        if not failing_subtrees:
            return individual

        # Randomly choose one failing subtree for mutation.
        node_to_mutate = random.choice(failing_subtrees)

        # If the symbol of the node is non-terminal, fuzz a new subtree and perform the replacement.
        if node_to_mutate.symbol.is_non_terminal:
            new_subtree = grammar.fuzz(node_to_mutate.symbol)
            mutated = individual.replace(node_to_mutate, new_subtree)
            return mutated

        return individual
