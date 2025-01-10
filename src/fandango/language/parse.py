import ast
import hashlib
import importlib.metadata
import os
import re
from typing import Any, List, Tuple

import cachedir_tag
import dill as pickle
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import ParseCancellationException
from xdg_base_dirs import xdg_cache_home

from fandango.constraints import predicates
from fandango.constraints.base import Constraint
from fandango.language.convert import (
    ConstraintProcessor,
    FandangoSplitter,
    GrammarProcessor,
    PythonProcessor,
)
from fandango.language.grammar import Grammar, NodeType
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.symbol import NonTerminal
from fandango.logger import LOGGER, print_exception


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
                indirect = f"<{parent}>..<{symbol}>" in str(value)
                if not check_constraints_existence_children(
                    grammar, parent, symbol, indirect, indirect_child
                ):
                    msg = f"Constraint {constraint}: <{parent}> has no child <{symbol}>"
                    raise ValueError(msg)


def check_constraints_existence_children(
    grammar, parent, symbol, recurse, indirect_child
):
    # LOGGER.debug(f"Checking {parent}, {symbol}")

    if indirect_child[f"<{parent}>"][f"<{symbol}>"] is not None:
        return indirect_child[f"<{parent}>"][f"<{symbol}>"]

    grammar_symbols = grammar.rules[NonTerminal(f"<{parent}>")]
    grammar_matches = re.findall(r'(?<!")<([^>]*)>(?!.*")', str(grammar_symbols))

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

    def __init__(
        self,
        tree: Any,
        fan_contents: str,
        lazy: bool = False,
    ):
        self.version = importlib.metadata.version("fandango-fuzzer")
        self.fan_contents = fan_contents
        self.global_vars = self.GLOBALS.copy()
        self.local_vars = self.LOCALS
        self.lazy = lazy

        LOGGER.debug("Extracting code")
        splitter = FandangoSplitter()
        splitter.visit(tree)
        python_processor = PythonProcessor()
        code_tree = python_processor.get_code(splitter.python_code)
        ast.fix_missing_locations(code_tree)
        self.code_text = ast.unparse(code_tree)

        LOGGER.debug("Running code")
        self.run_code()

        LOGGER.debug("Extracting grammar")
        grammar_processor = GrammarProcessor(
            local_variables=self.local_vars,
            global_variables=self.global_vars,
        )
        self.grammar: Grammar = grammar_processor.get_grammar(splitter.productions)

        LOGGER.debug("Extracting constraints")
        constraint_processor = ConstraintProcessor(
            self.grammar,
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            lazy=self.lazy,
        )
        self.constraints: List[Constraint] = constraint_processor.get_constraints(
            splitter.constraints
        )

    def run_code(self):
        exec(self.code_text, self.global_vars, self.local_vars)


def parse(
    fan_contents: str,
    /,
    lazy: bool = False,
    check_constraints: bool = True,
    given_grammar=None,
    use_cache: bool = True,
) -> Tuple[Grammar, List[Constraint]]:
    """
    Extract grammar and constraints from the given content
    :param fan_contents: Fandango specification
    :param lazy: If True, the constraints are evaluated lazily
    :param check_constraints: If True, check if the constraints contain non-terminal symbols that are not in the grammar
    :param given_grammar: If provided, check if the constraints contain non-terminal symbols that are not in the given grammar
    :param use_cache: If True, use cache to store the parsed grammar and constraints
    :return: Tuple of grammar and constraints
    """
    from_cache = False

    CACHE_DIR = xdg_cache_home() / "fandango"

    if use_cache:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
            cachedir_tag.tag(CACHE_DIR, application="Fandango")

        hash_ = hashlib.sha256(fan_contents.encode()).hexdigest()
        pickle_file = CACHE_DIR / (hash_ + ".pickle")

        if os.path.exists(pickle_file):
            try:
                with open(pickle_file, "rb") as fp:
                    LOGGER.info(f"Loading cached spec from {pickle_file}")
                    spec: FandangoSpec = pickle.load(fp)
                    LOGGER.debug(f"Cached spec version: {spec.version}")
                    if spec.fan_contents != fan_contents:
                        e = ValueError("Hash collision")
                        e.add_note("If you get this, you'll be real famous")
                        raise e
                    from_cache = True
            except Exception as e:
                LOGGER.debug(type(e).__name__ + ":" + str(e))

        if from_cache:
            LOGGER.debug("Running code")
            try:
                spec.run_code()
            except Exception as e:
                print_exception(e)

                # In case the error has anything to do with caching, play it safe
                del spec
                os.remove(pickle_file)

    if not from_cache:
        LOGGER.debug("Setting up .fan parser")
        input_stream = InputStream(fan_contents)
        error_listener = MyErrorListener()
        lexer = FandangoLexer(input_stream)
        lexer.addErrorListener(error_listener)
        token_stream = CommonTokenStream(lexer)
        parser = FandangoParser(token_stream)
        parser.addErrorListener(error_listener)

        LOGGER.debug("Parsing .fan content")
        tree = parser.fandango()

        LOGGER.debug("Splitting content")
        spec = FandangoSpec(tree, fan_contents, lazy)

    if len(spec.grammar.rules) > 0:
        check_grammar(spec.grammar)

    if check_constraints:
        if not spec.grammar or len(spec.grammar.rules) == 0:
            g = given_grammar
        else:
            g = spec.grammar
        if g and len(g.rules) > 0:
            check_constraints_existence(g, spec.constraints)

    if use_cache and not from_cache:
        try:
            with open(pickle_file, "wb") as fp:
                LOGGER.info(f"Saving spec to cache {pickle_file}")
                pickle.dump(spec, fp)
        except Exception as e:
            print_exception(e)
            try:
                os.remove(pickle_file)  # might be inconsistent
            except Exception:
                pass

    LOGGER.debug("Parsing complete")
    return spec.grammar, spec.constraints


def parse_file(*filenames, lazy: bool = False) -> Tuple[Grammar, List[Constraint]]:
    contents = ""
    errors = False

    for file in filenames:
        try:
            with open(file, "r") as fp:
                contents += fp.read()
        except Exception as e:
            print_exception(e)
            errors = True

    if errors:
        raise FileNotFoundError("No input files")

    return parse(contents, lazy=lazy)
