import random
import copy
import time
from typing import List, Tuple, Set

from fandango.constraints.base import Constraint
from fandango.evolution.selection import tournament_selection, select_elites
from fandango.language.grammar import Grammar, DerivationTree
from fandango.evolution.initialization import generate_initial_population
from fandango.evolution.mutate import (
    constraint_guided_mutation,
    random_subtree_replacement,
)
from fandango.evolution.crossover import type_safe_crossover
from fandango.evolution.fitness import evaluate_fitness, evaluate_population


class FANDANGO:
    def __init__(
        self,
        grammar: Grammar,
        constraints: List[Constraint],
        population_size: int,
        generations: int,
        mutation_rate: float,
        crossover_rate: float,
        elitism_rate: float,
        tournament_size: int,
    ):
        self.grammar = grammar
        self.constraints = constraints
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate  # Probability of mutation
        self.crossover_rate = crossover_rate  # Probability of crossover
        self.elitism_rate = elitism_rate  # Fraction of elites to carry over
        self.tournament_size = tournament_size  # Size of tournament for selection

        self.currentBestPopulation = generate_initial_population(
            self.grammar, self.population_size
        )
        self.currentFitness, self.currentFailingNodes = evaluate_population(
            self.currentBestPopulation, self.constraints
        )

    def evolve(self) -> List[DerivationTree]:
        """
        Runs the genetic algorithm to evolve a population of derivation trees that satisfy the constraints.
        :return: The final population of derivation trees.
        """
        if self.generations <= 0:  # No evolution
            return self.currentBestPopulation

        for generation in range(self.generations):
            # Evaluate current population if not already evaluated
            if not self.currentFitness:
                self.currentFitness, self.currentFailingNodes = evaluate_population(
                    self.currentBestPopulation, self.constraints
                )

            # Check for optimal solution
            if all(fitness == 1.0 for _, fitness, _ in self.currentFitness):
                print(f"Optimal solution found at generation {generation}.")
                break

            # a. Select Elites
            num_elites = max(1, int(self.elitism_rate * self.population_size))
            elites = select_elites(
                self.currentBestPopulation, self.currentFitness, num_elites
            )

            # b. Select Parents for Crossover (excluding elites if desired)
            non_elite_fitness = [
                (individual, fitness, tree)
                for (individual, fitness, tree) in self.currentFitness
                if individual not in elites
            ]

            num_parents = (
                self.population_size - num_elites or 2
            )  # Ensure at least 2 parents
            parents = tournament_selection(
                non_elite_fitness, self.tournament_size, num_parents
            )

            # c. Perform Crossover
            offspring = []
            for i in range(0, len(parents), 2):
                parent1 = parents[i]
                parent2 = parents[(i + 1) % len(parents)]
                if random.random() < self.crossover_rate:
                    child1, child2 = type_safe_crossover(parent1, parent2)
                else:
                    child1, child2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
                offspring.extend([child1, child2])

            # If we have an odd number of parents, we might have one extra child
            offspring = offspring[:num_parents]

            # d. Perform Mutation
            mutated_offspring = []
            for individual in offspring:
                if random.random() < self.mutation_rate:
                    mutant = random_subtree_replacement(individual, self.grammar)
                    mutated_offspring.append(mutant)
                else:
                    mutated_offspring.append(individual)

            # f. Form New Generation
            self.currentBestPopulation = elites + mutated_offspring
            self.currentFitness, self.currentFailingNodes = evaluate_population(
                self.currentBestPopulation, self.constraints
            )

        # Return the final population
        return self.currentBestPopulation


if __name__ == "__main__":
    from fandango.language.parse import parse_file

    # Parse grammar from src/evaluation/csv/csv.fan
    grammar, constraints, _ = parse_file("../../evaluation/csv/csv.fan")

    # Initialize FANDANGO with parameters
    fandango = FANDANGO(
        grammar,
        constraints,
        population_size=500,
        generations=1000,
        mutation_rate=0.2,
        crossover_rate=0.8,
        elitism_rate=0.2,
        tournament_size=10,
    )

    # Run the genetic algorithm
    start_time = time.time()
    fandango.evolve()
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")
    print(f"Evolution completed after {fandango.generations} generations.")
    print(
        f"Final fitness: {sum([fitness for _, fitness, _ in fandango.currentFitness]) / len([fitness for _, fitness, _ in fandango.currentFitness]):.2f}"
    )
    print(f"Final population: {fandango.currentBestPopulation}")
