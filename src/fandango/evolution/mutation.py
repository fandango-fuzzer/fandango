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
        max_nodes: int = 50,
    ) -> DerivationTree:
        """
        Default mutation operator: evaluates the individual, selects a failing subtree
        (if any), and replaces it with a newly fuzzed subtree generated from the grammar.
        """
        # Get fitness and failing trees from the evaluation function
        _, failing_trees = evaluate_func(individual)

        # Collect the failing subtrees
        failing_subtrees = [ft.tree for ft in failing_trees]
        failing_subtrees = list(
            filter(
                lambda x: (not x.read_only) and (x.symbol.is_non_terminal),
                failing_subtrees,
            )
        )

        # If there is nothing to mutate, return the individual as is.
        if not failing_subtrees:
            return individual

        # Randomly choose one failing subtree for mutation.
        node_to_mutate = random.choice(failing_subtrees)
        subtrees = [node_to_mutate] + list(
            filter(
                lambda x: (not x.read_only) and (x.symbol.is_non_terminal),
                node_to_mutate.descendants(),
            )
        )
        node_to_mutate = random.choice(subtrees)

        # Get a truncated tree that contains all nodes left from the selected node.
        ctx_tree = node_to_mutate.split_end()
        if ctx_tree.parent is not None:
            ctx_tree = ctx_tree.parent
            ctx_tree.set_children(ctx_tree.children[:-1])
        else:
            ctx_tree = None
        new_subtree = grammar.fuzz(
            node_to_mutate.symbol, prefix_node=ctx_tree, max_nodes=max_nodes
        )
        mutated = individual.replace(grammar, node_to_mutate, new_subtree)
        return mutated
