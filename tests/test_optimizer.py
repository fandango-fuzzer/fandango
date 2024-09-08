import unittest

from antlr4 import InputStream, CommonTokenStream

from fandango.constraints.base import ExpressionConstraint
from fandango.evolution.optimizer import GeneticAlgorithmOptimizer
from fandango.language.convert import FandangoSplitter, GrammarProcessor
from fandango.language.grammar import NonTerminal, DerivationTree
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import RuleSearch


class TestOptimizer(unittest.TestCase):
    FANDANGO_GRAMMAR = """
        <start> ::= <number>;
        <number> ::= <non_zero><digit>* | "0";
        <non_zero> ::= 
                      "1" 
                    | "2" 
                    | "3"
                    | "4" 
                    | "5" 
                    | "6" 
                    | "7" 
                    | "8" 
                    | "9"
                    ;
        <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
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
    odd_constraint = ExpressionConstraint(
        expression="int(number) % 2 != 0",
        searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
    )

    def test_population(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=[self.odd_constraint], population_size=10)

        # Check if the population is initialized correctly
        self.assertEqual(len(optimizer.population), 10)

        for tree in optimizer.population:
            self.assertIsInstance(tree, DerivationTree)
            self.assertEqual(tree.symbol, NonTerminal("<start>"))

    def test_fitness_evaluation(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=[self.odd_constraint], population_size=10)

        # Evaluate fitness for each tree in the population
        for i, tree in enumerate(optimizer.population):
            fitness = optimizer.evaluate_fitness(tree)
            self.assertIsInstance(fitness, float)

    def test_selection(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=[self.odd_constraint], population_size=10)

        # Test the parent selection mechanism
        parents = optimizer.select_parents()
        self.assertEqual(len(parents), 2)

    def test_random_crossover(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=[self.odd_constraint], population_size=10)

        # Select two parents
        parent1, parent2 = optimizer.select_parents()

        # Perform random crossover
        children = optimizer.crossover(parent1, parent2, method="random")
        self.assertEqual(len(children), 2)

        for child in children:
            self.assertIsInstance(child, DerivationTree)
            self.assertEqual(child.symbol, NonTerminal("<start>"))

    def test_intelligent_crossover(self):
        pass

    def test_random_mutation(self):
        # Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=self.grammar, constraints=[self.odd_constraint], population_size=10, mutation_rate=1.0)

        # Select a parent
        parent = optimizer.select_parents()[0]

        # Perform random mutation
        child = optimizer.mutate(parent, method="random")

        self.assertIsInstance(child, DerivationTree)
        self.assertEqual(child.symbol, NonTerminal("<start>"))


    def test_intelligent_mutation(self):
        pass

if __name__ == "__main__":
    unittest.main()
