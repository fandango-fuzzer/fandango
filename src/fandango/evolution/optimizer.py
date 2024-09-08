import random
from typing import List

from fandango.constraints.base import Constraint, Fitness
from fandango.language.grammar import Grammar, DerivationTree


class GeneticAlgorithmOptimizer:
    def __init__(self, grammar: Grammar, constraints: List[Constraint], population_size: int = 100,
                 mutation_rate: float = 0.01, crossover_rate: float = 0.7):
        self.grammar = grammar
        self.constraints = constraints
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        # Initialize population
        self.population = [self.grammar.fuzz() for _ in range(population_size)]

    def evaluate_fitness(self, tree: DerivationTree) -> float:
        """
        Retrieves the fitness score for a derivation tree based on the constraint system.
        :param tree: The derivation tree to evaluate
        :return: A fitness score, normalized between 0 and 1
        """
        total_fitness = Fitness(0, 0, False)  # Initialize an empty fitness object

        # Evaluate the fitness across all constraints
        for constraint in self.constraints:
            constraint_fitness = constraint.fitness(tree)
            total_fitness.solved += constraint_fitness.solved
            total_fitness.total += constraint_fitness.total

        # Return normalized fitness as solved/total
        return total_fitness.fitness() if total_fitness.total > 0 else 0

    # RUNNING SOME TESTS HERE, THE SELECTION CAN CHOOSE THE SAME FATHER TWICE IF THERE IS NO OTHER GOOD FIT! (DISCUSS WITH TEAM)
    def select_parents(self) -> List[DerivationTree]:
        """
        Selects two parents from the population using fitness-proportional selection (roulette wheel).
        :return: Two parent derivation trees
        """
        fitness_scores = [self.evaluate_fitness(tree) for tree in self.population]
        total_fitness = sum(fitness_scores)

        if total_fitness == 0:
            # In case all trees have zero fitness, select random parents
            return random.sample(self.population, 2)

        # Use fitness scores as weights for selection
        parent1 = random.choices(self.population, weights=fitness_scores, k=1)[0]
        parent2 = random.choices(self.population, weights=fitness_scores, k=1)[0]

        return [parent1, parent2]
