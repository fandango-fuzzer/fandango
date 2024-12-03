import ast
import re
import sys
from typing import Tuple, List

from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy

from fandango.constraints import predicates
from fandango.constraints.base import Constraint
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    ConstraintProcessor,
    PythonProcessor,
)
from fandango.language.grammar import Grammar
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser


def parse(fan: str, lazy: bool = False) -> Tuple[Grammar, List[Constraint]]:
    lexer = FandangoLexer(InputStream(fan))
    token = CommonTokenStream(lexer)
    parser = FandangoParser(token)
    parser._errHandler = BailErrorStrategy()
    tree = parser.fandango()
    splitter = FandangoSplitter()
    splitter.visit(tree)
    global_vars = {}
    local_vars = predicates.__dict__
    python_processor = PythonProcessor()
    exec(
        ast.unparse(python_processor.get_code(splitter.python_code)),
        global_vars,
        local_vars,
    )
    grammar_processor = GrammarProcessor(
        local_variables=local_vars, global_variables=global_vars
    )
    grammar = grammar_processor.get_grammar(splitter.productions)
    constraint_processor = ConstraintProcessor(
        grammar, local_variables=local_vars, global_variables=global_vars, lazy=lazy
    )
    constraint = constraint_processor.get_constraints(splitter.constraints)
    check_constraints_existence(grammar, constraint)
    return grammar, constraint

def check_constraints_existence(grammar, constraints):
    # TODO: Check for direct and indirect children. You can try this by running faker_experiment.py adding the following constraints: str(<name>..<start>[0]) == 'A'; for undirected children, and str(<name>.<start>[0]) == 'A'; for directed children.
    for constraint in constraints:
        # get all non-terminal symbols in the constraint
        constraint_symbols = constraint.get_symbols()
        for value in constraint_symbols:
            constraint_matches = re.findall(r"<(.*?)>", str(value))
            grammar_symbols = grammar.rules.keys()
            grammar_matches = re.findall(r"<(.*?)>", str(grammar_symbols))
            missing = [match for match in constraint_matches if match not in grammar_matches]
            if len(missing) > 0:
                raise ValueError(f"Constraint {constraint} contains non-terminal symbols {missing} that are not in the grammar")
            # Check for valid indirect children (<name>*<alpha>) means alpha is a child of name, or any of the children of name.
            print(value) # <name>*<start>
            # Check for valid direct children (<name>.<alpha>) means alpha is a direct child of name.



def parse_file(*args, lazy: bool = False) -> Tuple[Grammar, List[Constraint]]:
    contents = ""
    for file in args:
        with open(file, "r") as fp:
            contents += fp.read()
    return parse(contents, lazy=lazy)
