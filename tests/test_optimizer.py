# test_optimizer.py
import random
import unittest
from typing import List

from fandango.constraints.fitness import FailingTree
from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file
from fandango.language.tree import DerivationTree


class GeneticTest(unittest.TestCase):
    def setUp(self):
        # Define a simple grammar for testing
        try:
            grammar_int, constraints_int = parse_file("tests/resources/example_number.fan")
        except FileNotFoundError:
            grammar_int, constraints_int = parse_file("resources/example_number.fan")

        random.seed(25)  # Set random seed

        # Initialize FANDANGO with a fixed random seed for reproducibility
        self.fandango = Fandango(
            grammar=grammar_int,
            constraints=constraints_int,
            population_size=50,
            mutation_rate=0.2,
            crossover_rate=0.8,
            max_generations=100,
            elitism_rate=0.2,
        )

    def test_generate_initial_population(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        self.assertEqual(len(population), self.fandango.population_size)
        for individual in population:
            self.assertIsInstance(individual, DerivationTree)
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_evaluate_fitness(self):
        # Evaluate the fitness of the population
        for individual in self.fandango.population:
            fitness, failing_trees = self.fandango.evaluate_individual(individual)
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertLessEqual(fitness, 1.0)
            self.assertIsInstance(failing_trees, List)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, FailingTree)
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_evaluate_population(self):
        # Evaluate the fitness of the population
        evaluation = self.fandango.evaluate_population()
        assert len(evaluation) == len(self.fandango.population)
        for derivation_tree, fitness, failing_trees in evaluation:
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertLessEqual(fitness, 1.0)
            self.assertIsInstance(failing_trees, List)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, FailingTree)

        # Check that the population is valid
        for individual in self.fandango.population:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_select_elites(self):
        # Select the elites
        elites = self.fandango.select_elites()

        self.assertEqual(
            len(elites), self.fandango.elitism_rate * self.fandango.population_size
        )

        # Check that the population is valid
        for individual in elites:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_selection(self):
        # Select the parents
        parent1, parent2 = self.fandango.tournament_selection()

        # Check that the parents are in the population
        self.assertIn(parent1, self.fandango.population)
        self.assertIn(parent2, self.fandango.population)

        # Check that the parents are different
        self.assertNotEqual(parent1, parent2)

        # Check that the parents are of the correct type
        self.assertIsInstance(parent1, DerivationTree)
        self.assertIsInstance(parent2, DerivationTree)

        # Check that the population is valid
        for individual in [parent1, parent2]:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_crossover(self):
        # Select the parents
        parent1, parent2 = self.fandango.tournament_selection()

        # Perform crossover
        children = self.fandango.crossover(parent1, parent2)

        # Check that the children are of the correct type
        for child in children:
            self.assertIsInstance(child, DerivationTree)

        # Check that the children are different
        self.assertNotEqual(children[0], children[1])

        # Check that the population is valid
        for individual in children:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_mutation(self):
        # Select the parents
        parent1, parent2 = self.fandango.tournament_selection()

        children = self.fandango.crossover(parent1, parent2)

        # Perform mutation
        mutant1 = self.fandango.mutate(children[0])
        mutant2 = self.fandango.mutate(children[1])

        # Check that the mutated children are of the correct type
        for child in [mutant1, mutant2]:
            self.assertIsInstance(child, DerivationTree)

        # Check that the mutated children are different
        self.assertNotEqual(mutant1, mutant2)

        # Check that the population is valid
        for individual in [mutant1, mutant2]:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_evolve(self):
        initial_population = self.fandango.population
        initial_fitness = self.fandango.fitness

        # Run the evolution process
        self.fandango.evolve()

        # Check that the population has been updated
        self.assertIsNotNone(self.fandango.population)
        self.assertNotEqual(self.fandango.population, initial_population)

        # Check that the final fitness is better than the initial fitness
        self.assertGreaterEqual(self.fandango.fitness, initial_fitness)

        # Check that the population is valid
        for individual in self.fandango.population:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))


if __name__ == "__main__":
    unittest.main()
