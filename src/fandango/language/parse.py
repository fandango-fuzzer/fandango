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
from fandango.language.symbol import NonTerminal


def parse(fan: str, lazy: bool = False, check_existence=True) -> Tuple[Grammar, List[Constraint]]:
    """
    Parse a Fandango specification and return a Grammar and a list of Constraints.

    :param fan: Fandango specification
    :param lazy: If True, the constraints are evaluated lazily
    :param check_existence: If True, check if the constraints contain non-terminal symbols that are not in the grammar
    """
    lexer = FandangoLexer(InputStream(fan))
    token = CommonTokenStream(lexer)
    parser = FandangoParser(token)
    parser._errHandler = BailErrorStrategy()
    tree = parser.fandango()
    splitter = FandangoSplitter()
    splitter.visit(tree)
    global_vars = {}
    local_vars = predicates.__dict__.copy()
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
    if check_existence:
        check_constraints_existence(grammar, constraint)
    return grammar, constraint


def check_constraints_existence(grammar, constraints):
    indirect_child = {
        str(k): {str(l): None for l in grammar.rules.keys()}
        for k in grammar.rules.keys()
    }

    for constraint in constraints:
        constraint_symbols = constraint.get_symbols()

        for value in constraint_symbols:
            constraint_matches = re.findall(r"<(.*?)>", str(value))
            grammar_symbols = grammar.rules.keys()
            grammar_matches = re.findall(r"<(.*?)>", str(grammar_symbols))
            missing = [
                match for match in constraint_matches if match not in grammar_matches
            ]

            if len(missing) > 0:
                raise ValueError(
                    f"Constraint {constraint} contains non-terminal symbols {missing} that are not in the grammar"
                )

            for i in range(len(constraint_matches) - 1):
                parent = constraint_matches[i]
                symbol = constraint_matches[i + 1]
                indirect = f"<{parent}>*<{symbol}>" in str(value)
                if not check_constraints_existence_children(
                    grammar, parent, symbol, indirect, indirect_child
                ):
                    raise ValueError(
                        f"In constraint {constraint}: <{parent}> has no child <{symbol}>"
                    )


def check_constraints_existence_children(
    grammar, parent, symbol, recurse, indirect_child
):
    if indirect_child[f"<{parent}>"][f"<{symbol}>"] is not None:
        return indirect_child[f"<{parent}>"][f"<{symbol}>"]

    grammar_symbols = grammar.rules[NonTerminal(f"<{parent}>")]
    grammar_matches = re.findall(r'(?<!")<(.*?)>(?!.*")', str(grammar_symbols))

    if symbol not in grammar_matches:
        if recurse:
            is_child = False
            for match in grammar_matches:
                is_child = is_child or check_constraints_existence_children(
                    grammar, match, symbol, recurse, indirect_child
                )
            indirect_child[f"<{parent}>"][f"<{symbol}>"] = is_child
            return is_child
        else:
            return False

    indirect_child[f"<{parent}>"][f"<{symbol}>"] = True
    return True


def parse_file(*args, lazy: bool = False) -> Tuple[Grammar, List[Constraint]]:
    contents = ""
    try:
        for file in args:
            with open(file, "r") as fp:
                contents += fp.read()
    except FileNotFoundError:
        print(
            f"File not found, trying with default .fan specification", file=sys.stderr
        )
        try:
            with open("default.fan", "r") as fp:
                contents = fp.read()
        except FileNotFoundError:
            print(f"Default .fan specification not found, exiting", file=sys.stderr)
            sys.exit(1)

    return parse(contents, lazy=lazy)
