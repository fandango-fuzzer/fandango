import random
from abc import ABC, abstractmethod
from beartype.typing import Generic, List, Optional, Tuple, TypeVar

from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.chromosomes.individual import Individual
from fandango.evolution.chromosomes.suite import Suite
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree

T = TypeVar("T", bound=Chromosome)


class CrossoverOperator(ABC, Generic[T]):
    @abstractmethod
    def crossover(
        self, grammar: Grammar, parent1: T, parent2: T
    ) -> Optional[Tuple[T, T]]:
        """
        Abstract method to perform crossover on two parent individuals.

        Generic over Chromosome type T for supporting both Individual and Suite chromosomes.

        :param grammar: The Grammar used for crossover operations.
        :param parent1: The first parent (chromosome of type T).
        :param parent2: The second parent (chromosome of type T).
        :return: A tuple of two offspring (chromosomes of type T) or None if crossover is not possible.
        """
        pass


class SimpleSubtreeCrossover(CrossoverOperator[Individual]):
    def crossover(
        self, grammar: Grammar, parent1: Individual, parent2: Individual
    ) -> Optional[Tuple[Individual, Individual]]:
        # Unwrap DerivationTree from Individual
        tree1 = parent1.tree
        tree2 = parent2.tree

        symbols1 = tree1.get_non_terminal_symbols()
        symbols2 = tree2.get_non_terminal_symbols()
        common_symbols = symbols1.intersection(symbols2)
        if not common_symbols:
            return None
        symbol = random.choice(list(common_symbols))
        nodes1 = tree1.find_all_nodes(symbol)
        nodes2 = tree2.find_all_nodes(symbol)
        node1 = random.choice(nodes1)
        node2 = random.choice(nodes2)
        child1_tree = tree1.replace(grammar, node1, node2)
        child2_tree = tree2.replace(grammar, node2, node1)

        # Wrap results back in Individual
        return Individual(child1_tree), Individual(child2_tree)


class SuiteCrossover(CrossoverOperator[Suite]):
    def crossover(
        self, grammar: Grammar, parent1: Suite, parent2: Suite
    ) -> Optional[Tuple[Suite, Suite]]:
        if len(parent1) == 0 or len(parent2) == 0:
            return None
        point1 = random.randint(0, len(parent1))
        point2 = random.randint(0, len(parent2))
        inds1: List[Individual] = list(parent1)
        inds2: List[Individual] = list(parent2)
        child1 = Suite([ind.clone() for ind in inds1[:point1] + inds2[point2:]])
        child2 = Suite([ind.clone() for ind in inds2[:point2] + inds1[point1:]])
        if len(child1) == 0 or len(child2) == 0:
            return None
        return child1, child2
