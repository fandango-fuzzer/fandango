#!/usr/bin/env pytest

import random
import unittest
from fandango.constraints.fitness import FailingTree
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


class GeneticTest(unittest.TestCase):
    def setUp(self):
        # Define a simple grammar for testing
        file = open("tests/resources/example_number.fan", "r")
        try:
            grammar_int, constraints_int = parse(
                file, use_stdlib=False, use_cache=False
            )
        except FileNotFoundError:
            grammar_int, constraints_int = parse(
                file, use_stdlib=False, use_cache=False
            )

        random.seed(25)  # Set random seed

        # Initialize FANDANGO with a fixed random seed for reproducibility
        assert grammar_int is not None
        self.fandango = Fandango(
            grammar=grammar_int,
            constraints=constraints_int,
            population_size=50,
            mutation_rate=0.2,
            crossover_rate=0.8,
            elitism_rate=0.2,
            logger_level=LoggerLevel.DEBUG,
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
        population = self.fandango.population
        unique = set(population)
        for individual in population:
            generator = GeneratorWithReturn(
                self.fandango.evaluator.evaluate_individual(individual)
            )
            solutions = list(generator)  # extract all solutions
            self.assertEqual(
                len(solutions),
                individual.to_int() % 2 if individual not in unique else 0,
                f"Individual: {individual}",
            )
            fitness, failing_trees = generator.return_value
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertLessEqual(fitness, 1.0)
            self.assertIsInstance(failing_trees, list)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, FailingTree)
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_evaluate_population(self):
        # Evaluate the fitness of the population
        generator = GeneratorWithReturn(
            self.fandango.evaluator.evaluate_population(self.fandango.population)
        )
        solutions = list(generator)
        self.assertTrue(all(s.to_int() % 2 == 0) for s in solutions)
        self.assertTrue(
            all(ind.to_int() % 2 != 0)
            for ind in self.fandango.population
            if ind not in solutions
        )
        self.assertEqual(len(solutions), len(set(solutions)))
        evaluation = generator.return_value
        self.assertEqual(len(evaluation), len(self.fandango.population))
        for ind, fitness, failing_trees in evaluation:
            self.assertIsInstance(fitness, float)
            self.assertGreaterEqual(fitness, 0.0)
            self.assertLessEqual(fitness, 1.0)
            self.assertIsInstance(failing_trees, list)
            for failing_tree in failing_trees:
                self.assertIsInstance(failing_tree, FailingTree)

        # Check that the population is valid
        for individual in self.fandango.population:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_select_elites(self):
        # Select the elites
        elites = self.fandango.evaluator.select_elites(
            self.fandango.evaluation,
            elitism_rate=self.fandango.elitism_rate,
            population_size=self.fandango.population_size,
        )

        self.assertEqual(
            len(elites), self.fandango.elitism_rate * self.fandango.population_size
        )

        # Check that the population is valid
        for individual in elites:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_selection(self):
        # Select the parents
        parent1, parent2 = self.fandango.evaluator.tournament_selection(
            self.fandango.evaluation,
            tournament_size=max(
                2, int(self.fandango.population_size * self.fandango.tournament_size)
            ),
        )

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
        tournament_size = max(
            2, int(self.fandango.population_size * self.fandango.tournament_size)
        )
        parent1, parent2 = self.fandango.evaluator.tournament_selection(
            self.fandango.evaluation,
            tournament_size,
        )

        # Perform crossover
        children = self.fandango.crossover_operator.crossover(
            self.fandango.grammar, parent1, parent2
        )

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
        tournament_size = max(
            2, int(self.fandango.population_size * self.fandango.tournament_size)
        )
        parent1, parent2 = self.fandango.evaluator.tournament_selection(
            self.fandango.evaluation, tournament_size
        )

        children = self.fandango.crossover_operator.crossover(
            self.fandango.grammar, parent1, parent2
        )

        # Perform mutation
        gen1 = GeneratorWithReturn(
            self.fandango.mutation_method.mutate(
                children[0],
                self.fandango.grammar,
                self.fandango.evaluator.evaluate_individual,
            )
        )
        _solutions1 = list(gen1)
        mutant1 = gen1.return_value

        gen2 = GeneratorWithReturn(
            self.fandango.mutation_method.mutate(
                children[1],
                self.fandango.grammar,
                self.fandango.evaluator.evaluate_individual,
            )
        )
        _solutions2 = list(gen2)
        mutant2 = gen2.return_value

        # Check that the mutated children are of the correct type
        for child in [mutant1, mutant2]:
            self.assertIsInstance(child, DerivationTree)

        # Check that the mutated children are different
        self.assertNotEqual(mutant1, mutant2)

        # Check that the population is valid
        for individual in [mutant1, mutant2]:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))

    def test_evolve(self):
        # Run the evolution process
        self.fandango.evolve(max_generations=100)

        # Check that the population has been updated
        self.assertIsNotNone(self.fandango.population)
        self.assertNotEqual(self.fandango.population, [])

        # Check that the population is valid
        for individual in self.fandango.population:
            self.assertTrue(self.fandango.grammar.parse(str(individual)))


class DeterminismTests(unittest.TestCase):
    # fandango fuzz -f tests/resources/determinism.fan -n 100 --random-seed 1
    def get_solutions(
        self,
        specification_file,
        desired_solutions,
        random_seed,
    ):
        file = open(specification_file, "r")
        grammar_int, constraints_int = parse(file, use_stdlib=False, use_cache=False)
        assert grammar_int is not None
        fandango = Fandango(
            grammar=grammar_int,
            constraints=constraints_int,
            random_seed=random_seed,
        )
        solutions: list[DerivationTree] = fandango.evolve(
            desired_solutions=desired_solutions,
            max_generations=100,
        )
        return [s.to_string() for s in solutions]

    def test_deterministic_solutions(self):
        solutions_1 = self.get_solutions("tests/resources/determinism.fan", 100, 1)

        solutions_2 = self.get_solutions("tests/resources/determinism.fan", 100, 1)

        self.assertListEqual(solutions_1, solutions_2)


if __name__ == "__main__":
    unittest.main()
