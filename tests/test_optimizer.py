# test_optimizer.py

import random
import unittest
from typing import List

from fandango.evolution.algorithm import FANDANGO
from fandango.language.grammar import DerivationTree
from fandango.language.parse import parse_file


class GeneticTest(unittest.TestCase):
    def setUp(self):
        # Define a simple grammar for testing
        grammar, constraints = parse_file("../src/evaluation/csv/csv.fan")

        # Initialize FANDANGO with a fixed random seed for reproducibility
        self.fandango = FANDANGO(
            grammar=grammar,
            constraints=constraints,
            population_size=50,
            mutation_rate=0.1,
            crossover_rate=0.9,
            max_generations=100,
            elitism_rate=0.2,
            k=10,
            max_depth=20,
            verbose=False
        )
        random.seed(25)  # Set random seed

    def test_generate_k_path_population(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        self.assertEqual(len(population), 100)
        for individual in population:
            self.assertIsInstance(individual, DerivationTree)

    def test_evaluate_fitness(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        for individual in population:
            fitness, failing_trees = self.fandango.evaluate_fitness(individual, self.fandango.constraints)
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertIsInstance(failing_trees, List)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, DerivationTree)

    def test_evaluate_population(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation = self.fandango.evaluate_population(population, self.fandango.constraints)
        for tree, fitness, failing_trees in evaluation:
            self.assertIsInstance(tree, DerivationTree)
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertIsInstance(failing_trees, List)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, DerivationTree)

    def test_select_elites(self):
        # Generate a population of derivation trees
        population = self.fandango.population
        # Evaluate the fitness of the population
        evaluation = self.fandango.evaluate_population(population, self.fandango.constraints)
        # Select the elites
        elites = self.fandango.select_elites(evaluation)

        # sort the population by fitness
        evaluation.sort(key=lambda x: x[1], reverse=True)
        # Select the top 20% of the population
        expected_elites = evaluation[:int(self.fandango.elitism_rate * len(population))]
        self.assertEqual(elites, expected_elites)

    def test_fitness_proportionate_selection(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation = self.fandango.evaluate_population(population, self.fandango.constraints)
        # Select the elites
        elites = self.fandango.select_elites(evaluation)

        # Select the parents
        parent1 = self.fandango.fitness_proportionate_selection(evaluation)
        parent2 = self.fandango.fitness_proportionate_selection(evaluation)

        # Check that the parents are not in the elites
        for parent in [parent1, parent2]:
            self.assertNotIn(parent, elites)

        # Check that the parents are in the population
        self.assertIn(parent1, population)
        self.assertIn(parent2, population)

        # Check that the parents are different
        self.assertNotEqual(parent1, parent2)

        # Check that the parents are of the correct type
        self.assertIsInstance(parent1, DerivationTree)
        self.assertIsInstance(parent2, DerivationTree)

    def test_crossover(self):
        # Generate a population of derivation trees
        population = population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation = self.fandango.evaluate_population(population, self.fandango.constraints)

        # Select the parents
        parent1 = self.fandango.fitness_proportionate_selection(evaluation)
        parent2 = self.fandango.fitness_proportionate_selection(evaluation)

        parent_evaluation = self.fandango.evaluate_population([parent1, parent2], self.fandango.constraints)

        # Perform crossover
        children = self.fandango.crossover(parent_evaluation)

        # Check that the children are of the correct type
        for child in children:
            self.assertIsInstance(child, DerivationTree)

        # Check that the children are not in the population
        for child in children:
            self.assertNotIn(child, population)

        # Check that the children are different
        self.assertNotEqual(children[0], children[1])

        # Check that the children are not the same as the parents
        self.assertNotEqual(children[0], parent1)
        self.assertNotEqual(children[0], parent2)
        self.assertNotEqual(children[1], parent1)
        self.assertNotEqual(children[1], parent2)

    def test_mutation(self):
        # Generate a population of derivation trees
        population = population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation = self.fandango.evaluate_population(population, self.fandango.constraints)

        # Select the parents
        parent1 = self.fandango.fitness_proportionate_selection(evaluation)
        parent2 = self.fandango.fitness_proportionate_selection(evaluation)

        parent_evaluation = self.fandango.evaluate_population([parent1, parent2], self.fandango.constraints)

        # Perform crossover
        children = self.fandango.crossover(parent_evaluation)

        # Evaluate the fitness of the children
        children_evaluation = self.fandango.evaluate_population(children, self.fandango.constraints)

        # Perform mutation
        mutated_children = self.fandango.mutation(children_evaluation)

        # Check that the mutated children are of the correct type
        for child in mutated_children:
            self.assertIsInstance(child, DerivationTree)

        # Check that the mutated children are not in the population
        for child in mutated_children:
            self.assertNotIn(child, population)

        # Check that the mutated children are different
        self.assertNotEqual(mutated_children[0], mutated_children[1])

        # Check that the mutated children are not the same as the parents
        self.assertNotEqual(mutated_children[0], parent1)
        self.assertNotEqual(mutated_children[0], parent2)
        self.assertNotEqual(mutated_children[1], parent1)
        self.assertNotEqual(mutated_children[1], parent2)

    def test_evolve(self):
        population = self.fandango.population

        # Run the evolution process
        self.fandango.evolve()

        # Check that the population has been updated
        self.assertIsNotNone(self.fandango.population)
        self.assertNotEqual(self.fandango.population, population)

        # Optionally, check that the best individual has a high fitness
        best_fitness = max(fitness for _, fitness, _ in
                           self.fandango.evaluate_population(self.fandango.population, self.fandango.constraints))
        self.assertGreaterEqual(best_fitness, 1.0)


if __name__ == '__main__':
    unittest.main()
