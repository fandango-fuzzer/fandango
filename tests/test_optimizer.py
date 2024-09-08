import unittest
import random

from antlr4 import InputStream, CommonTokenStream

from fandango.constraints.base import ExpressionConstraint
from fandango.language.grammar import Grammar, NonTerminal, DerivationTree, Terminal
from fandango.evolution.optimizer import GeneticAlgorithmOptimizer
from fandango.language.convert import FandangoSplitter, GrammarProcessor
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

    def test_optimizer(self):
        # Step 1: Parse the grammar
        lexer = FandangoLexer(InputStream(self.FANDANGO_GRAMMAR))
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

        # Step 4: Initialize the optimizer
        optimizer = GeneticAlgorithmOptimizer(grammar=grammar, constraints=[odd_constraint], population_size=10)

        # Step 5: Evaluate fitness for the first tree in the population
        for i, tree in enumerate(optimizer.population):
            fitness = optimizer.evaluate_fitness(tree)
            print(f"Tree {i}: {tree} - Fitness: {fitness}")

        # Step 6: Test the parent selection mechanism
        parents = optimizer.select_parents()
        self.assertEqual(len(parents), 2)  # Ensure that two parents are selected
        print(f"Selected parents: {parents[0]} and {parents[1]}")


if __name__ == "__main__":
    unittest.main()