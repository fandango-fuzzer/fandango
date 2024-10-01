import ast
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
    grammar_processor = GrammarProcessor()
    grammar = grammar_processor.get_grammar(splitter.productions)
    global_vars = {}
    local_vars = predicates.__dict__
    python_processor = PythonProcessor()
    exec(
        ast.unparse(python_processor.get_code(splitter.python_code)),
        global_vars,
        local_vars,
    )
    constraint_processor = ConstraintProcessor(
        grammar, local_vars, global_vars, lazy=lazy
    )
    constraint = constraint_processor.get_constraints(splitter.constraints)
    return grammar, constraint


def parse_file(*args, lazy: bool = False) -> Tuple[Grammar, List[Constraint]]:
    contents = ""
    for file in args:
        with open(file, "r") as fp:
            contents += fp.read()
    return parse(contents, lazy=lazy)
