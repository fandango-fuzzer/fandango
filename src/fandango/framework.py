import time

from antlr4 import InputStream, CommonTokenStream

from fandango.constraints.base import ExpressionConstraint
from fandango.evolution.optimizer import GeneticAlgorithmOptimizer
from fandango.language.convert import FandangoSplitter, GrammarProcessor
from fandango.language.grammar import NonTerminal, DerivationTree
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import RuleSearch


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

# smaller_than_50000_constraint = ExpressionConstraint(
#     expression="int(number) < 50000",
#     searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
# )
#
# always_ends_with_1_constraint = ExpressionConstraint(
#     expression="int(number) % 10 == 1",
#     searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
# )
#
# bigger_than_10000_constraint = ExpressionConstraint(
#     expression="int(number) > 10000",
#     searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
# )

constraints = [odd_constraint]

def main():
    # Initialize the optimizer
    optimizer = GeneticAlgorithmOptimizer(grammar=grammar, constraints=constraints,
                                          population_size=100, verbose=True)

    # Run the optimizer
    start_time = time.time()
    solution = optimizer.evolve()

    print(f"Time taken: {time.time() - start_time}")
    print(f"Solution: {solution}")


if __name__ == '__main__':
    main()