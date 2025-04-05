import copy
import random
from abc import ABC, abstractmethod
from typing import Tuple

from fandango.language.grammar import Grammar
from fandango.language.tree import DerivationTree


class CrossoverOperator(ABC):
    @abstractmethod
    def crossover(
        self, grammar: Grammar, parent1: DerivationTree, parent2: DerivationTree
    ) -> Tuple[DerivationTree, DerivationTree]:
        pass


class SimpleSubtreeCrossover(CrossoverOperator):
    def crossover(
        self, grammar: Grammar, parent1: DerivationTree, parent2: DerivationTree
    ) -> Tuple[DerivationTree, DerivationTree]:
        symbols1 = parent1.get_non_terminal_symbols()
        symbols2 = parent2.get_non_terminal_symbols()
        common_symbols = symbols1.intersection(symbols2)
        if not common_symbols:
            return parent1, parent2
        symbol = random.choice(sorted(list(common_symbols)))
        nodes1 = parent1.find_all_nodes(symbol)
        nodes2 = parent2.find_all_nodes(symbol)
        node1 = random.choice(nodes1)
        node2 = random.choice(nodes2)
        child1 = parent1.replace(grammar, node1, copy.deepcopy(node2))
        child2 = parent2.replace(grammar, node2, copy.deepcopy(node1))
        return child1, child2
