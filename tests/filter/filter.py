import time

from antlr4 import InputStream, CommonTokenStream
from fuzzingbook.Grammars import Grammar

from fandango.constraints.base import ExpressionConstraint
from fandango.evolution.optimizer import GeneticAlgorithmOptimizer
from fandango.language.convert import FandangoSplitter, GrammarProcessor
from fandango.language.grammar import NonTerminal, DerivationTree
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import RuleSearch

from isla.solver import ISLaSolver

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

ISLA_GRAMMAR = {
    "<start>": ["<number>"],
    "<number>": ["<non_zero><digits>", "0"],
    "<digits>": ["", "<digit><digits>"],
    "<non_zero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

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

smaller_than_50000_constraint = ExpressionConstraint(
    expression="int(number) < 50000",
    searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
)

always_ends_with_1_constraint = ExpressionConstraint(
    expression="int(number) % 10 == 1",
    searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
)

bigger_than_10000_constraint = ExpressionConstraint(
    expression="int(number) > 10000",
    searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
)

# hash of number has to be even
hash_of_number_has_to_be_even = ExpressionConstraint(
    expression="hash(number) % 2 == 0",
    searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
)

FANDANGO_CONSTRAINTS = [odd_constraint, smaller_than_50000_constraint, always_ends_with_1_constraint, bigger_than_10000_constraint, hash_of_number_has_to_be_even]

def fandango_filter(size=10, dev=False):
    solution = []
    total = []

    start_time = time.time()
    while len(solution) < size:
        inp_ = grammar.fuzz()
        # if inp satisfies all constraints
        if all(c.check(inp_) for c in FANDANGO_CONSTRAINTS):
            solution.append(inp_)
        if dev:
            total.append(inp_)
    end_time = time.time()

    print(f"FANDANGO: Time taken to generate {size} valid solutions: {end_time - start_time} seconds")
    if dev:
        print(f"FANDANGO: Amount of inputs produced: {len(total)}")
        #compute inputs per second
        print(f"FANDANGO: Total inputs per second: {len(total)/(end_time - start_time)}")
    print(f"FANDANGO: Solutions: {solution}")

def isla_filter(size=10):
    solver = ISLaSolver(ISLA_GRAMMAR, 'str.to.int(<number>) > 10000 and str.to.int(<number>) < 50000 and str.to.int(<number>) mod 10 = 1 and str.to.int(<number>) mod 2 = 1')
    solutions = []

    start_time = time.time()
    while len(solutions) < size:
        solution = None
        for s in solver.solve():
            solution = s
            break
        solutions.append(solution)

    end_time = time.time()

    print(f"\n\nISLA: Time taken to generate {size} solutions: {end_time - start_time} seconds")
    print(f"Solutions: {solutions}")



if __name__ == "__main__":
    size = 1000
    fandango_filter(size, dev=True)
    # isla_filter(size)
