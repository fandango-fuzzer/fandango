import time

from antlr4 import InputStream, CommonTokenStream

from fandango.constraints.base import ExpressionConstraint, ComparisonConstraint, Comparison
from fandango.evolution.optimizer import GeneticAlgorithmOptimizer
from fandango.language.convert import FandangoSplitter, GrammarProcessor
from fandango.language.grammar import NonTerminal, DerivationTree
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import RuleSearch


FANDANGO_GRAMMAR = """
<start> ::= <csv-file> ;
<csv-file> ::= <csv-header> <csv-records> ;
<csv-header> ::= <csv-record> ;
<csv-records> ::= <csv-record> <csv-records> | "" ;
<csv-record> ::= <csv-string-list> "\n" ;
<csv-string-list> ::= <raw-field> | <raw-field> ";" <csv-string-list> ;
<raw-field> ::= <simple-field> | <quoted-field> ;
<simple-field> ::= <spaces> <simple-characters> <spaces> ;
<simple-characters> ::= <simple-character> <simple-characters> | <simple-character> ;
<simple-character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" ;
<quoted-field> ::= '"' <escaped-field> '"' ;
<escaped-field> ::= <escaped-characters> ;
<escaped-characters> ::= <escaped-character> <escaped-characters> | "" ;
<escaped-character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" | " " | "\t" | "\r" |"\n" ;
<spaces> ::= "" | " " <spaces> ;
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

print(grammar)

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

always_ends_with_1_constraint = ComparisonConstraint(
    operator=Comparison.EQUAL,
    left="int(number) % 10",
    right="1",
    searches={"number": RuleSearch(NonTerminal("<number>"), grammar)}
)

constraints = [
    odd_constraint,
    smaller_than_10000_constraint,
    always_ends_with_1_constraint
]


def main():
    # Initialize the optimizer
    optimizer = GeneticAlgorithmOptimizer(
        grammar=grammar,
        constraints=[],
        population_size=10,
        generations=1000,
        verbose=True,
    )

    # Run the optimizer
    start_time = time.time()
    solution = optimizer.evolve()

    print(f"Time taken: {time.time() - start_time}")
    print(f"Solution: {solution}")



if __name__ == "__main__":
    main()
