import unittest

from antlr4 import InputStream, CommonTokenStream

from fandango.constraints.base import ExpressionConstraint, ComparisonConstraint, Comparison
from fandango.evolution.optimizer import GeneticAlgorithmOptimizer
from fandango.language.convert import FandangoSplitter, GrammarProcessor
from fandango.language.grammar import NonTerminal, DerivationTree
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import RuleSearch


class TestOptimizer(unittest.TestCase):
    FANDANGO_GRAMMAR = """
<start> ::= <number> ;
<number> ::= <non_zero> <digit>* | "0" ;
<non_zero> ::= "1" | "2" | "3"| "4" | "5" | "6" | "7" | "8" | "9" ;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
"""

    lexer = FandangoLexer(InputStream(FANDANGO_GRAMMAR))
    token_stream = CommonTokenStream(lexer)
    parser = FandangoParser(token_stream)
    tree = parser.fandango()

    # Step 2: Split and process the grammar
    splitter = FandangoSplitter()
    splitter.visit(tree)

    processor = GrammarProcessor()
    grammar = processor.get_grammar(splitter.productions)

    # Step 3: Define an odd-number constraint
    odd_constraint = ComparisonConstraint(
        operator=Comparison.NOT_EQUAL,
        left="int(number) % 2",
        right="0",
        searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
    )

    smaller_than_10000_constraint = ComparisonConstraint(
        operator=Comparison.LESS,
        left="int(number)",
        right="10000",
        searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
    )

    constraints = [odd_constraint, smaller_than_10000_constraint]

    def test_population(self):
            optimizer = GeneticAlgorithmOptimizer(
                grammar=self.grammar,
                constraints=self.constraints,
                population_size=10,
                generations=1000,
                verbose=True,
            )

            # Check if the population is initialized correctly
            self.assertEqual(len(optimizer.population), 10)

            #check if population is different
            self.assertEqual(len(set(optimizer.population)), len(optimizer.population))

            for tree in optimizer.population:
                self.assertIsInstance(tree, DerivationTree)
                self.assertEqual(tree.symbol, NonTerminal("<start>"))

    def test_fitness_evaluation(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(
            grammar=self.grammar,
            constraints=self.constraints,
            population_size=10,
            generations=1000,
            verbose=True,
        )

        # Evaluate fitness for each tree in the population
        for i, tree in enumerate(optimizer.population):
            print(f"Tree {tree} fitness: {optimizer.evaluate_fitness(tree)}")

            self.assertIsInstance(optimizer.evaluate_fitness(tree)[0], float)
            self.assertGreaterEqual(optimizer.evaluate_fitness(tree)[0], 0.0)
            self.assertLessEqual(optimizer.evaluate_fitness(tree)[0], 1.0)


    def test_next_generation_selection(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=self.constraints,
                                              population_size=10)

        first_generation = optimizer.population

        # Select the next generation
        optimizer.select_next_generation()

        second_generation = optimizer.population

        # Check if the population size remains the same
        self.assertEqual(len(second_generation), 10)
        self.assertEqual(len(first_generation), len(second_generation))
        self.assertNotEqual(first_generation, second_generation)

        print("First generation: ", first_generation)
        print("Second generation: ", second_generation)

        # assert second gen fitness is better or equal than first gen fitness
        first_gen_fitness = [optimizer.evaluate_fitness(tree)[0] for tree in first_generation]
        second_gen_fitness = [optimizer.evaluate_fitness(tree)[0] for tree in second_generation]

        self.assertGreaterEqual(sum(second_gen_fitness), sum(first_gen_fitness))

    def test_parent_selection(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=self.constraints,
                                              population_size=10)

        # Test the parent selection mechanism
        parents = optimizer.select_parents()

        # print p1 with fitness
        print(f"Parent 1: {parents[0]} with fitness {optimizer.evaluate_fitness(parents[0])[0]}")
        print(f"Parent 2: {parents[1]} with fitness {optimizer.evaluate_fitness(parents[1])[0]}")

        self.assertEqual(len(parents), 2)
        self.assertIsInstance(parents[0], DerivationTree)
        self.assertIsInstance(parents[1], DerivationTree)
        self.assertNotEqual(parents[0], parents[1])

    def test_random_crossover(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=self.constraints,
                                              population_size=10, crossover_rate=1.0, crossover_method="random")

        # Select two parents
        parent1, parent2 = optimizer.select_parents()

        # Perform random crossover
        children = optimizer.crossover(parent1, parent2)
        self.assertEqual(len(children), 2)

        for child in children:
            self.assertIsInstance(child, DerivationTree)
            self.assertEqual(child.symbol, NonTerminal("<start>"))
            self.assertNotEqual(child, parent1)
            self.assertNotEqual(child, parent2)

    def test_constraint_driven_crossover(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=self.constraints,
                                              population_size=10, crossover_rate=1.0, crossover_method="constraint_driven")

        # Select two parents
        parent1, parent2 = optimizer.select_parents()

        # Perform constraint-driven crossover
        children = optimizer.crossover(parent1, parent2)
        self.assertEqual(len(children), 2)

        for child in children:
            self.assertIsInstance(child, DerivationTree)
            self.assertEqual(child.symbol, NonTerminal("<start>"))
            self.assertNotEqual(child, parent1)
            self.assertNotEqual(child, parent2)


    def test_random_mutation(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=self.constraints,
                                              population_size=100, mutation_rate=1.0, mutation_method="random")

        # Select a parent
        parent = optimizer.select_parents()[0]

        # Perform random mutation
        child = optimizer.mutate(parent)

        self.assertIsInstance(child, DerivationTree)
        self.assertEqual(child.symbol, NonTerminal("<start>"))
        self.assertNotEqual(child, parent)

    def test_constraint_driven_mutation(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=self.constraints,
                                              population_size=100, mutation_rate=1.0, mutation_method="constraint_driven")

        # Select a parent
        parent = optimizer.select_parents()[0]

        # Perform constraint-driven mutation
        child = optimizer.mutate(parent)

        self.assertIsInstance(child, DerivationTree)
        self.assertEqual(child.symbol, NonTerminal("<start>"))
        self.assertNotEqual(child, parent)

if __name__ == "__main__":
    unittest.main()
