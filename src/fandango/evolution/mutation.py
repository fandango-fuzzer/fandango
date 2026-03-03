# mutation.py
import random
from abc import ABC, abstractmethod
from collections.abc import Callable, Generator
from beartype.typing import Generic, TypeVar

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.chromosomes.individual import Individual
from fandango.language import DerivationTree, Grammar
from fandango.language.symbols import NonTerminal

T = TypeVar("T", bound=Chromosome)


class MutationOperator(ABC, Generic[T]):
    @abstractmethod
    def mutate(
        self,
        individual: T,
        grammar: Grammar,
        evaluate_func: Callable[
            [T],
            Generator[
                DerivationTree, None, tuple[float, list[FailingTree], Suggestion]
            ],
        ],
    ) -> Generator[DerivationTree, None, T]:
        """
        Abstract method to perform mutation on an individual.

        Generic over Chromosome type T for supporting both Individual and Suite chromosomes.

        :param individual: The individual (chromosome of type T) to mutate.
        :param grammar: The Grammar used to generate new subtrees.
        :param evaluate_func: A function that, given an individual, returns a tuple (fitness, failing_trees).
        :return: A new (mutated) chromosome of type T.
        """
        pass


class SimpleMutation(MutationOperator[Individual]):
    def mutate(
        self,
        individual: Individual,
        grammar: Grammar,
        evaluate_func: Callable[
            [Individual],
            Generator[
                DerivationTree, None, tuple[float, list[FailingTree], Suggestion]
            ],
        ],
        max_nodes: int = 50,
    ) -> Generator[DerivationTree, None, Individual]:
        """
        Default mutation operator: evaluates the individual, selects a failing subtree
        (if any), and replaces it with a newly fuzzed subtree generated from the grammar.
        """
        # Get fitness and failing trees from the evaluation function
        _, failing_trees, _suggestion = yield from evaluate_func(individual)

        # Unwrap the DerivationTree from Individual
        tree = individual.tree

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
        assert isinstance(node_to_mutate.symbol, NonTerminal)

        # Get a truncated tree that contains all nodes left from the selected node.
        ctx_tree = node_to_mutate.split_end()
        if ctx_tree.parent is not None:
            prefix_node = ctx_tree.parent
            prefix_node.set_children(ctx_tree.children[:-1])
        else:
            prefix_node = None
        new_subtree = grammar.fuzz(
            node_to_mutate.symbol,
            prefix_node=prefix_node,
            max_nodes=node_to_mutate.size() + (max_nodes - tree.size()),
        )
        mutated_tree = tree.replace(grammar, node_to_mutate, new_subtree)

        # Wrap the result back in Individual
        return Individual(mutated_tree)
