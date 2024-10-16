# test_optimizer.py

import random
import string
import unittest
from typing import Set

from fuzzingbook.Grammars import Grammar, srange
from fuzzingbook.Parser import EarleyParser

from fandango.evolution.algorithm import FANDANGO
from fandango.language.tree import DerivationTree
from fandango.language.parse import parse_file

csvGRAMMAR = {
    "<start>": ["<csv-file>"],
    "<csv-file>": ["<csv-header><csv-records>"],
    "<csv-header>": ["<csv-record>"],
    "<csv-records>": ["<csv-record><csv-records>", ""],
    "<csv-record>": ["<csv-string-list>\n"],
    "<csv-string-list>": ["<raw-field>", "<raw-field>;<csv-string-list>"],
    "<raw-field>": ["<simple-field>", "<quoted-field>"],
    "<simple-field>": ["<spaces><simple-characters><spaces>"],
    "<simple-characters>": [
        "<simple-character><simple-characters>",
        "<simple-character>",
    ],
    "<simple-character>": [
        c
        for c in srange(string.printable)
        if c not in ["\n", ";", '"', " ", "\t", "\r", '"']
    ],
    "<quoted-field>": ['"<escaped-field>"'],
    "<escaped-field>": ["<escaped-characters>"],
    "<escaped-characters>": ["<escaped-character><escaped-characters>", ""],
    "<escaped-character>": [c for c in srange(string.printable) if c not in ['"']],
    "<spaces>": ["", " <spaces>"],
}

INT_GRAMMAR = {
    "<start>": ["<number>"],
    "<number>": ["<non_zero><digits>", "0"],
    "<non_zero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<digits>": ["<digit>", "<digit><digits>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


def check_validity(population: [DerivationTree], grammar: Grammar) -> bool:
    parser = EarleyParser(grammar)
    checks = 0
    for inp_ in population:
        try:
            for _ in parser.parse(str(inp_)):
                checks += 1
        except:
            pass
    return checks == len(population)


class GeneticTest(unittest.TestCase):
    def setUp(self):
        # Define a simple grammar for testing
        grammar_int, constraints_int = parse_file("resources/int.fan")
        # grammar_csv, constraints_csv = parse_file("resources/csv.fan")

        random.seed(25)  # Set random seed

        # Initialize FANDANGO with a fixed random seed for reproducibility
        self.fandango = FANDANGO(
            grammar=grammar_int,
            constraints=constraints_int,
            population_size=20,
            mutation_rate=0.2,
            crossover_rate=0.8,
            max_generations=100,
            elitism_rate=0.2,
            verbose=False,
        )

    def test_generate_initial_population(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        self.assertEqual(len(population), self.fandango.population_size)
        for individual in population:
            self.assertIsInstance(individual, DerivationTree)

    def test_evaluate_fitness(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        for individual in population:
            fitness, failing_trees = self.fandango.evaluate_fitness(
                individual, self.fandango.constraints
            )
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertIsInstance(failing_trees, Set)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, DerivationTree)

    def test_evaluate_population(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )
        for tree, fitness, failing_trees in evaluation:
            self.assertIsInstance(tree, DerivationTree)
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertIsInstance(failing_trees, Set)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, DerivationTree)

    def test_select_elites(self):
        # Generate a population of derivation trees
        population = self.fandango.population
        # Evaluate the fitness of the population
        evaluation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )
        # Select the elites
        elites = self.fandango.select_elites(evaluation)

        # sort the population by fitness
        evaluation.sort(key=lambda x: x[1], reverse=True)
        # Select the top 20% of the population
        expected_elites = evaluation[
            : int(self.fandango.elitism_rate * len(population))
        ]
        for elite, _, _ in expected_elites:
            self.assertIn(elite, elites)

    def test_fitness_proportionate_selection(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )
        evaluation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )
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
        population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )

        # Select the parents
        parent1 = self.fandango.fitness_proportionate_selection(evaluation)
        parent2 = self.fandango.fitness_proportionate_selection(evaluation)

        parent_evaluation, _ = self.fandango.evaluate_population(
            [parent1, parent2], self.fandango.constraints
        )

        # Perform crossover
        children = self.fandango.crossover(parent_evaluation)

        # Check that the children are of the correct type
        for child in children:
            self.assertIsInstance(child, DerivationTree)

        # Check that the children are different
        self.assertNotEqual(children[0], children[1])

    def test_mutation(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )

        # Select the parents
        parent1 = self.fandango.fitness_proportionate_selection(evaluation)
        parent2 = self.fandango.fitness_proportionate_selection(evaluation)

        parent_evaluation, _ = self.fandango.evaluate_population(
            [parent1, parent2], self.fandango.constraints
        )

        # Perform crossover
        children = self.fandango.crossover(parent_evaluation)

        # Evaluate the fitness of the children
        children_evaluation, _s = self.fandango.evaluate_population(
            children, self.fandango.constraints
        )

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

        first_computation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )
        initial_fitness = sum([f for _, f, _ in first_computation]) / len(
            [f for _, f, _ in first_computation]
        )

        # Run the evolution process
        self.fandango.evolve()

        final_computation, _ = self.fandango.evaluate_population(
            self.fandango.population, self.fandango.constraints
        )
        final_fitness = sum([f for _, f, _ in final_computation]) / len(
            [f for _, f, _ in final_computation]
        )

        # Check that the population has been updated
        self.assertIsNotNone(self.fandango.population)
        self.assertNotEqual(self.fandango.population, population)

        # Check that the final fitness is better than the initial fitness
        self.assertGreaterEqual(final_fitness, initial_fitness)

    def test_valid_initial_population(self):
        self.setUp()

        # Generate a population and check if they are still valid according to the grammar
        population = self.fandango.population
        self.assertTrue(check_validity(population, INT_GRAMMAR))

    def test_valid_mutations(self):
        # Mutate a population and check if they are still valid according to the grammar
        population = self.fandango.population
        fitness, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )
        mutated_population = self.fandango.mutation(fitness)

        self.assertTrue(check_validity(mutated_population, INT_GRAMMAR))

    def test_valid_crossover(self):
        # Generate a population of derivation trees
        population = self.fandango.population

        # Evaluate the fitness of the population
        evaluation, _ = self.fandango.evaluate_population(
            population, self.fandango.constraints
        )

        offspring = []

        while len(offspring) < len(population):
            # Select the parents
            parent1 = self.fandango.fitness_proportionate_selection(evaluation)
            parent2 = self.fandango.fitness_proportionate_selection(evaluation)

            parent_evaluation, _ = self.fandango.evaluate_population(
                [parent1, parent2], self.fandango.constraints
            )

            # Perform crossover
            children = self.fandango.crossover(parent_evaluation)

            # if the children are the same as the parents, skip
            if children[0] == parent1 and children[1] == parent2:
                continue
            else:
                offspring.extend(children)

        self.assertTrue(check_validity(offspring, INT_GRAMMAR))


if __name__ == "__main__":
    unittest.main()
