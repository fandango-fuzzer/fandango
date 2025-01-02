import ast
import re
import os
import sys
import importlib.metadata

from typing import Tuple, List, Any
from fandango.logger import LOGGER, print_exception

from antlr4 import InputStream, CommonTokenStream

import hashlib
import dill as pickle
from xdg_base_dirs import xdg_cache_home
import cachedir_tag

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


class MyErrorListener(ErrorListener):
    def __init__(self, filename=None):
        self.filename = filename
        super().__init__()
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f'{repr(self.filename)}, line {line}, column {column}: {msg}')


def check_grammar_consistency(grammar, ignored_symbols=None, 
                              start_symbol="<start>"):
    if not grammar:
        return

    LOGGER.debug("Checking grammar")

    used_symbols = set()
    undefined_symbols = set()
    defined_symbols = set()
    ignored_symbols = ignored_symbols or set()

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
        if (symbol not in used_symbols and
            symbol not in ignored_symbols and 
            str(symbol) != start_symbol):
            LOGGER.info(f"Symbol {symbol} defined, but not used")

    if undefined_symbols:
        defined_symbols_str = ", ".join(symbol for symbol in defined_symbols
                                        and symbol not in ignored_symbols)

        error = ValueError(f"Undefined symbols {undefined_symbols} in grammar")
        error.add_note(f"Possible symbols: {defined_symbols_str}")
        raise error


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

    grammar_symbols = grammar.rules.keys()
    grammar_matches = re.findall(r"<([^>]*)>", str(grammar_symbols))
    # LOGGER.debug(f"All used symbols: {grammar_matches}")

    for constraint in constraints:
        constraint_symbols = constraint.get_symbols()

        for value in constraint_symbols:
            # LOGGER.debug(f"Constraint {constraint}: Checking {value}")

            constraint_matches = re.findall(r"<([^>]*)>", str(value))  # was <(.*?)>

            missing = [
                match for match in constraint_matches if match not in grammar_matches
            ]

            if len(missing) > 1:
                missing_symbols = ", ".join(["<" + symbol + ">" for symbol in missing])
                error = ValueError(
                    f"Constraint {constraint}: undefined symbols {missing_symbols}"
                )
                error.add_note(f"Possible symbols: {defined_symbols_str}")
                raise error

            if len(missing) == 1:
                missing_symbol = missing[0]
                error = ValueError(
                    f"Constraint {constraint}: undefined symbol <{missing_symbol}>"
                )
                error.add_note(f"Possible symbols: {defined_symbols_str}")
                raise error

            for i in range(len(constraint_matches) - 1):
                parent = constraint_matches[i]
                symbol = constraint_matches[i + 1]
                # This handles <parent>[...].<symbol> as <parent>..<symbol>.
                # We could also interpret the actual [...] contents here,
                # but slices and chains could make this hard -- AZ
                recurse = f"<{parent}>[" in str(value) or f"..<{symbol}>" in str(value)
                if not check_constraints_existence_children(
                    grammar, parent, symbol, recurse, indirect_child
                ):
                    msg = f"Constraint {constraint}: <{parent}> has no child <{symbol}>"
                    raise ValueError(msg)


def check_constraints_existence_children(
    grammar, parent, symbol, recurse, indirect_child
):
    # LOGGER.debug(f"Checking if <{symbol}> is a child of <{parent}>")

    if indirect_child[f"<{parent}>"][f"<{symbol}>"] is not None:
        return indirect_child[f"<{parent}>"][f"<{symbol}>"]

    grammar_symbols = grammar.rules[NonTerminal(f"<{parent}>")]

    # Original code; fails on <a> "b" <c> -- AZ
    # grammar_matches = re.findall(r'(?<!")<([^>]*)>(?!.*")',
    #                              str(grammar_symbols))
    #
    # Simpler version; may overfit (e.g. matches <...> in strings),
    # but that should not hurt us -- AZ
    grammar_matches = re.findall(r"<([^>]*)>", str(grammar_symbols))

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


class FandangoSpec:
    GLOBALS = predicates.__dict__
    LOCALS = None  # Must be None to ensure top-level imports

    def __init__(self, tree: Any, fan_contents: str,
                 lazy: bool = False, filename: str = "<input>",):
        self.version = importlib.metadata.version("fandango")
        self.fan_contents = fan_contents
        self.global_vars = self.GLOBALS.copy()
        self.local_vars = self.LOCALS
        self.lazy = lazy

        LOGGER.debug(f"{filename}: extracting code")
        splitter = FandangoSplitter()
        splitter.visit(tree)
        python_processor = PythonProcessor()
        code_tree = python_processor.get_code(splitter.python_code)
        ast.fix_missing_locations(code_tree)
        self.code_text = ast.unparse(code_tree)

        LOGGER.debug(f"{filename}: running code")
        self.run_code()

        LOGGER.debug(f"{filename}: extracting grammar")
        grammar_processor = GrammarProcessor(
            local_variables=self.local_vars, global_variables=self.global_vars
        )
        self.grammar: Grammar = \
            grammar_processor.get_grammar(splitter.productions, prime=False)

        LOGGER.debug(f"{filename}: extracting constraints")
        constraint_processor = ConstraintProcessor(
            self.grammar,
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            lazy=self.lazy,
        )
        self.constraints: List[Constraint] = \
            constraint_processor.get_constraints(splitter.constraints)

    def run_code(self):
        exec(self.code_text, self.global_vars, self.local_vars)


def parse(
    fan_content: str,
    /,
    filename: str = "<input>",
    lazy: bool = False,
    use_cache: bool = True,
) -> Tuple[Grammar, List[Constraint]]:
    """
    Extract grammar and constraints from the given content
    :param fan_content: Fandango specification text
    :param lazy: If True, the constraints are evaluated lazily
    :param check_constraints: If True, check if the constraints contain non-terminal symbols that are not in the grammar
    """
    from_cache = False

    CACHE_DIR = xdg_cache_home() / "fandango"

    if use_cache:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
            cachedir_tag.tag(CACHE_DIR, application="Fandango")

        hash = hashlib.sha256(fan_content.encode()).hexdigest()
        pickle_file = CACHE_DIR / (hash + ".pickle")

        if os.path.exists(pickle_file):
            try:
                with open(pickle_file, "rb") as fp:
                    LOGGER.info(f"{filename}: loading cached spec from {pickle_file}")
                    spec: FandangoSpec = pickle.load(fp)
                    LOGGER.debug(f"Cached spec version: {spec.version}")
                    if spec.fan_contents != fan_content:
                        e = ValueError("Hash collision")
                        e.add_note("If you get this, you'll be real famous")
                        raise e
                    from_cache = True
            except Exception as e:
                LOGGER.debug(type(e).__name__ + ":" + str(e))

    if from_cache:
        LOGGER.debug(f"{filename}: running code")
        try:
            spec.run_code()
        except Exception as e:
            print_exception(e)

            # In case the error has anything to do with caching, play it safe
            del spec
            os.remove(pickle_file)

    if not from_cache:
        LOGGER.debug(f"{filename}: setting up .fan parser and lexer")
        input_stream = InputStream(fan_content)
        error_listener = MyErrorListener(filename)
        lexer = FandangoLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        token_stream = CommonTokenStream(lexer)
        parser = FandangoParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        LOGGER.debug(f"{filename}: parsing .fan content")
        tree = parser.fandango()

        LOGGER.debug(f"{filename}: splitting content")
        spec = FandangoSpec(tree, fan_content, lazy)

    if use_cache and not from_cache:
        try:
            with open(pickle_file, "wb") as fp:
                LOGGER.info(f"{filename}: saving spec to cache {pickle_file}")
                pickle.dump(spec, fp)
        except Exception as e:
            print_exception(e)
            try:
                os.remove(pickle_file)  # might be inconsistent
            except Exception:
                pass

    LOGGER.debug(f"{filename}: parsing complete")
    return spec.grammar, spec.constraints


def finalize(grammar, constraints, ignored_symbols=None):
    """Run final checks after parsing of all grammars is done"""
    ignored_symbols = ignored_symbols or set()

    if grammar and len(grammar.rules) > 0:
        check_grammar_consistency(grammar, ignored_symbols)

    if grammar and constraints:
        check_constraints_existence(grammar, constraints)

    LOGGER.debug("Finalizing grammar")
    grammar.prime()


# def parse_file(*filenames, lazy: bool = False) -> Tuple[Grammar, List[Constraint]]:
#     contents = ""
#     errors = False

#     for file in filenames:
#         try:
#             with open(file, "r") as fp:
#                 contents += fp.read()
#         except Exception as e:
#             print_exception(e)
#             errors = True

#     if errors:
#         raise FileNotFoundError("No input files")

#     return parse(contents, lazy=lazy)
