import ast
import re
import sys
from typing import Tuple, List
from fandango.logger import LOGGER

from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy

from fandango.constraints import predicates
from fandango.constraints.base import Constraint
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    ConstraintProcessor,
    PythonProcessor,
)
from fandango.language.grammar import Grammar, NodeType
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.symbol import NonTerminal

from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException

class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise ParseCancellationException(f"Line %{line}, Column {column}: error: {msg}")

def check_grammar(grammar, start_symbol="<start>"):
    if not grammar:
        return

    LOGGER.debug("Checking grammar")

    used_symbols = set()
    undefined_symbols = set()
    defined_symbols = set()

    for symbol in grammar.rules.keys():
        defined_symbols.add(symbol)

    def collect_used_symbols(tree):
        if tree.node_type == NodeType.NON_TERMINAL:
            used_symbols.add(tree.symbol)
        if tree.node_type == NodeType.REPETITION:
            collect_used_symbols(tree.node)
        for child in tree.children():
            collect_used_symbols(child)

    for tree in grammar.rules.values():
        collect_used_symbols(tree)

    for symbol in used_symbols:
        if symbol not in defined_symbols:
            undefined_symbols.add(symbol)

    for symbol in defined_symbols:
        if symbol not in used_symbols and str(symbol) != start_symbol:
            LOGGER.info(f"Symbol {symbol} defined, but not used")

    if undefined_symbols:
        for symbol in grammar.rules.keys():
            defined_symbols_str = ", ".join(symbol)

        error = ValueError(f"Undefined symbols {undefined_symbols} in grammar")
        error.add_note(f"Possible symbols: {defined_symbols_str}")
        raise error


def check_constraints(constraints, grammar):
    try:
        LOGGER.debug("Checking constraints")

        used_symbols = set()
        undefined_symbols = set()
        defined_symbols = set()

        if grammar:
            for symbol in grammar.rules.keys():
                defined_symbols.add(str(symbol))

        def collect_used_symbols(constraint):
            nonlocal used_symbols
            # FIXME: This should actually traverse the constraint
            matches = re.findall("<[a-zA-Z0-9_]*>", str(constraint))
            for match in matches:
                used_symbols.add(match)

        for constraint in constraints:
            collect_used_symbols(constraint)

        for symbol in used_symbols:
            if not symbol in defined_symbols:
                undefined_symbols.add(symbol)

        if undefined_symbols:
            error = ValueError(f"Undefined symbols {undefined_symbols} in constraints")
            error.add_note(f"Possible symbols: {defined_symbols}")
            raise error
    except ValueError as e:
        # do nothing
        pass


def check_constraints_existence(grammar, constraints):
    LOGGER.debug("Checking constraints")

    indirect_child = {
        str(k): {str(l): None for l in grammar.rules.keys()}
        for k in grammar.rules.keys()
    }

    defined_symbols = []
    for symbol in grammar.rules.keys():
        defined_symbols.append(str(symbol))
    defined_symbols_str = ", ".join(defined_symbols)

    for constraint in constraints:
        constraint_symbols = constraint.get_symbols()

        for value in constraint_symbols:
            constraint_matches = re.findall(r"<(.*?)>", str(value))
            grammar_symbols = grammar.rules.keys()
            grammar_matches = re.findall(r"<(.*?)>", str(grammar_symbols))
            missing = [
                match for match in constraint_matches if match not in grammar_matches
            ]

            if len(missing) > 1:
                missing_symbols = ", ".join([ '<' + symbol + '>' for symbol in missing ])
                error = ValueError(f"Constraint {constraint}: undefined symbols {missing_symbols}")
                error.add_note(f"Possible symbols: {defined_symbols_str}")
                raise error

            if len(missing) == 1:
                missing_symbol = missing[0]
                error = ValueError(f"Constraint {constraint}: undefined symbol <{missing_symbol}>")
                error.add_note(f"Possible symbols: {defined_symbols_str}")
                raise error

            for i in range(len(constraint_matches) - 1):
                parent = constraint_matches[i]
                symbol = constraint_matches[i + 1]
                indirect = f"<{parent}>*<{symbol}>" in str(value)
                if not check_constraints_existence_children(
                    grammar, parent, symbol, indirect, indirect_child
                ):
                    msg = f"Constraint {constraint}: <{parent}> has no child <{symbol}>"
                    raise ValueError(msg)


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


def parse(fan_contents: str, /, lazy: bool = False,
          check_existence: bool = True, given_grammar=None) -> Tuple[Grammar, List[Constraint]]:
    """
    Extract grammar and constraints from the given content
    :param fan: Fandango specification
    :param lazy: If True, the constraints are evaluated lazily
    :param check_existence: If True, check if the constraints contain non-terminal symbols that are not in the grammar
    """

    LOGGER.debug("Parsing .fan content")
    error_listener = MyErrorListener()
    input_stream = InputStream(fan_contents)
    lexer = FandangoLexer(input_stream)
    lexer.addErrorListener(error_listener)
    token_stream = CommonTokenStream(lexer)
    parser = FandangoParser(token_stream)
    parser.addErrorListener(error_listener)
    # parser._errHandler = BailErrorStrategy()
    tree = parser.fandango()

    LOGGER.debug("Extracting code")
    splitter = FandangoSplitter()
    splitter.visit(tree)
    global_vars = predicates.__dict__.copy()
    local_vars = None  # Must be None to ensure top-level imports
    python_processor = PythonProcessor()
    code_tree = python_processor.get_code(splitter.python_code)
    code_text = ast.unparse(code_tree)

    LOGGER.debug("Running code")
    exec(code_text, global_vars, local_vars)

    LOGGER.debug("Extracting grammar")
    grammar_processor = GrammarProcessor(
        local_variables=local_vars, global_variables=global_vars
    )
    grammar: Grammar = grammar_processor.get_grammar(splitter.productions)

    if len(grammar.rules) > 0:
        check_grammar(grammar)

    LOGGER.debug("Extracting constraints")
    constraint_processor = ConstraintProcessor(
        grammar,
        local_variables=local_vars,
        global_variables=global_vars,
        lazy=lazy,
    )
    constraints: List[Constraint] = \
        constraint_processor.get_constraints(splitter.constraints)

    # if len(grammar.rules) == 0:
    #     # No grammar found; check constraints against given (existing) grammar
    #     check_constraints(constraints, given_grammar)
    # else:
    #     try:
    #         check_constraints(constraints, grammar)
    #     except ValueError as e:
    #         LOGGER.print_exception(e)

    if check_existence:
        if len(grammar.rules) == 0:
            g = given_grammar
        else:
            g = grammar
        if g:
            check_constraints_existence(g, constraints)

    LOGGER.debug("Parsing complete")
    return grammar, constraints


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
