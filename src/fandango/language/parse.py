import ast
import re
import os
import importlib.metadata
import platform

from thefuzz import process as thefuzz_process

from typing import Tuple, List, Set, Any, IO, Optional
from fandango.logger import LOGGER, print_exception

from antlr4 import InputStream, CommonTokenStream

import hashlib
import dill as pickle
from xdg_base_dirs import xdg_cache_home, xdg_data_home, xdg_data_dirs
import cachedir_tag
from copy import deepcopy
from pathlib import Path

from fandango.constraints import predicates
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
from fandango.language.stdlib import stdlib

from antlr4.error.ErrorListener import ErrorListener


class MyErrorListener(ErrorListener):
    """This is invoked from ANTLR when a syntax error is encountered"""
    def __init__(self, filename=None):
        self.filename = filename
        super().__init__()
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f'{repr(self.filename)}, line {line}, column {column}: {msg}')


def closest_match(word, candidates):
    return thefuzz_process.extractOne(word, candidates)[0]

def check_grammar_consistency(grammar, given_used_symbols=set(),
                              start_symbol="<start>"):
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
        if (symbol not in used_symbols
            and symbol not in given_used_symbols
            and str(symbol) != start_symbol):
            LOGGER.info(f"Symbol {symbol} defined, but not used")

    if undefined_symbols:
        first_undefined_symbol = undefined_symbols.pop()
        closest = closest_match(first_undefined_symbol, used_symbols)
        error = ValueError(f"Undefined symbol {first_undefined_symbol} in grammar. Did you mean {closest}?")
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

            if missing:
                first_missing_symbol = missing[0]
                closest = closest_match(first_missing_symbol, defined_symbols)

            if len(missing) > 1:
                missing_symbols = ", ".join(["<" + symbol + ">" for symbol in missing])
                error = ValueError(
                    f"{constraint}: undefined symbols {missing_symbols}. Did you mean {closest}?"
                )
                raise error

            if len(missing) == 1:
                missing_symbol = missing[0]
                error = ValueError(
                    f"{constraint}: undefined symbol <{missing_symbol}>. Did you mean {closest}?"
                )
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
                    msg = f"{constraint}: <{parent}> has no child <{symbol}>"
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


CURRENT_FILENAME: str = "<undefined>"
FILES_TO_PARSE: List[Tuple[IO, int]] = []
INCLUDES: List[str] = []
INCLUDE_DEPTH: int = 0

def include(file_to_be_included: str):
    """Include a file in the current context"""
    global FILES_TO_PARSE
    global CURRENT_FILENAME
    global INCLUDE_DEPTH

    path = os.path.dirname(CURRENT_FILENAME)
    if not path:
        path = "."  # For strings and standard input
    if INCLUDES:
        path += ":" + ":".join(INCLUDES)
    if os.environ.get("FANDANGO_PATH"):
        path += ":" + os.environ["FANDANGO_PATH"]
    dirs = [Path(dir) for dir in path.split(":")]

    if platform.system() == 'Darwin':
        dirs += [Path.home() / "Library" / "Fandango"]  # sth like ~/Library/Fandango
        dirs += [Path("/Library/Fandango")] # sth like /Library/Fandango
    else:
        dirs += [xdg_data_home() / "fandango"]  # sth like ~/.local/share/fandango
    dirs += [dir / "fandango" for dir in xdg_data_dirs()]  # sth like /usr/local/share/fandango

    for dir in dirs:
        try:
            full_file_name = dir / file_to_be_included
            full_file = open(full_file_name, 'r')
        except FileNotFoundError:
            continue
        LOGGER.debug(f"{CURRENT_FILENAME}: including {full_file_name}")

        INCLUDE_DEPTH += 1
        FILES_TO_PARSE.append((full_file, INCLUDE_DEPTH))
        return

    raise FileNotFoundError(f"{CURRENT_FILENAME}: {repr(file_to_be_included)} not found in {':'.join(str(dir) for dir in dirs)}")

class FandangoSpec:
    """Helper class to pickle and unpickle parsed Fandango specifications"""
    GLOBALS = predicates.__dict__
    GLOBALS.update({'include': include})
    LOCALS = None  # Must be None to ensure top-level imports

    def __init__(self, tree: Any, fan_contents: str,
                 lazy: bool = False, filename: str = "<input>"):
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
        self.run_code(filename=filename)

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
        self.constraints: List[str] = \
            constraint_processor.get_constraints(splitter.constraints)

    def run_code(self, filename: str="<input>"):
        global CURRENT_FILENAME
        CURRENT_FILENAME = filename

        exec(self.code_text, self.global_vars, self.local_vars)


def parse_content(
    fan_contents: str,
    /,
    filename: str = "<input>",
    use_cache: bool = True,
    lazy: bool = False,
) -> Tuple[Grammar, List[str]]:
    """
    Parse given content into a grammar and constraints.
    This is a helper function; use `parse()` as the main entry point.
    :param fan_contents: Fandango specification text
    :param filename: The file name of the content (for error messages)
    :param use_cache: If True (default), cache parsing results.
    :param lazy: If True, the constraints are evaluated lazily
    :return: A tuple of the grammar and constraints
    """
    spec: Optional[FandangoSpec] = None
    from_cache = False

    if platform.system() == 'Darwin':
        CACHE_DIR = Path.home() / "Library" / "Caches" / "Fandango"
    else:
        CACHE_DIR = xdg_cache_home() / "fandango"

    if use_cache:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR, mode = 0o700)
            cachedir_tag.tag(CACHE_DIR, application="Fandango")

        hash = hashlib.sha256(fan_contents.encode()).hexdigest()
        pickle_file = CACHE_DIR / (hash + ".pickle")

        if os.path.exists(pickle_file):
            try:
                with open(pickle_file, "rb") as fp:
                    LOGGER.info(f"{filename}: loading cached spec from {pickle_file}")
                    spec = pickle.load(fp)
                    assert spec is not None
                    LOGGER.debug(f"Cached spec version: {spec.version}")
                    if spec.fan_contents != fan_contents:
                        e = ValueError("Hash collision (If you get this, you'll be real famous)")
                        raise e

                    from_cache = True
            except Exception as e:
                LOGGER.debug(type(e).__name__ + ":" + str(e))

    if spec:
        LOGGER.debug(f"{filename}: running code")
        try:
            spec.run_code(filename=filename)
        except Exception as e:
            # In case the error has anything to do with caching, play it safe
            LOGGER.debug(f"Cached spec failed; removing {pickle_file}")
            os.remove(pickle_file)
            raise e

    if not spec:
        LOGGER.debug(f"{filename}: setting up .fan parser and lexer")
        input_stream = InputStream(fan_contents)
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
        spec = FandangoSpec(tree, fan_contents, lazy, filename=filename)

    assert spec is not None

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


USED_SYMBOLS: Set[str] = set()
STDLIB_GRAMMAR: Optional[Grammar] = None
STDLIB_CONSTRAINTS: Optional[List[str]] = None

def parse(fan_files: List[IO],
          constraints: List[str],
          /,
          use_stdlib: bool = True,
          use_cache: bool = True,
          lazy: bool = False,
          given_grammars: List[Grammar] = [],
          includes: List[str] = []) -> Tuple[Optional[Grammar], List[str]]:
    """
    Parse .fan content, handling multiple files, standard library, and includes.
    :param fan_files: List of (open) .fan files
    :param constraints: List of constraints (as strings)
    :param use_stdlib: If True (default), use the standard library
    :param use_cache: If True (default), cache parsing results
    :param lazy: If True, the constraints are evaluated lazily
    :param given_grammars: Grammars to use in addition to the standard library
    :param includes: A list of directories to search for include files
    :return: A tuple of the grammar and constraints
    """
    if not fan_files and not constraints:
        return None, []

    global STDLIB_SYMBOLS, STDLIB_GRAMMAR, STDLIB_CONSTRAINTS
    if STDLIB_GRAMMAR is None:
        LOGGER.debug("Reading standard library")
        STDLIB_GRAMMAR, STDLIB_CONSTRAINTS = parse_content(stdlib, "<stdlib>")

    assert STDLIB_GRAMMAR is not None
    assert STDLIB_CONSTRAINTS is not None

    global USED_SYMBOLS
    USED_SYMBOLS = set()
    for symbol in STDLIB_GRAMMAR.rules.keys():
        # Do not complain about unused symbols in the standard library
        USED_SYMBOLS.add(symbol)

    global INCLUDES
    INCLUDES = includes

    # LOGGER.debug("Given grammars:", str(given_grammars))

    grammars = [deepcopy(STDLIB_GRAMMAR)]
    parsed_constraints = STDLIB_CONSTRAINTS.copy()
    grammars += given_grammars

    LOGGER.debug("Reading files")
    more_grammars = []
    global FILES_TO_PARSE
    FILES_TO_PARSE = [(file, 0) for file in fan_files]

    global INCLUDE_DEPTH
    INCLUDE_DEPTH = 0

    while FILES_TO_PARSE:
        (file, depth) = FILES_TO_PARSE.pop(0)
        LOGGER.debug(f"Reading {file.name} (depth = {depth})")
        fan_contents = file.read()
        new_grammar, new_constraints = \
            parse_content(fan_contents, filename=file.name)
        parsed_constraints += new_constraints

        if depth == 0:
            # Given file: process in order
            more_grammars.append(new_grammar)
        else:
            # Included file: process _before_ current grammar
            more_grammars = [new_grammar] + more_grammars
            # Do not complain about unused symbols in included files
            for symbol in new_grammar.rules.keys():
                USED_SYMBOLS.add(symbol)

        if INCLUDE_DEPTH > 0:
            INCLUDE_DEPTH -= 1

    grammars += more_grammars

    LOGGER.debug(f"Processing {len(grammars)} grammars")
    grammar = grammars[0]
    LOGGER.debug(f"Grammar #1: {grammar.rules.keys()}")
    n = 2
    for g in grammars[1:]:
        LOGGER.debug(f"Grammar #{n}: {g.rules.keys()}")
        # LOGGER.debug(f"Grammar: {g}")

        for symbol in g.rules.keys():
            if symbol in grammar.rules:
                LOGGER.info(f"Redefining {symbol}")
        grammar.update(g, prime=False)
        n += 1

    LOGGER.debug("Processing constraints")
    for constraint in constraints:
        LOGGER.debug(f"Constraint {constraint}")
        _, new_constraints = parse_content(constraint + ";", constraint)
        parsed_constraints += new_constraints

    finalize(grammar, parsed_constraints, given_used_symbols=USED_SYMBOLS)
    return grammar, parsed_constraints


def finalize(grammar, constraints, given_used_symbols=set()):
    """Run final checks after parsing of all grammars is done"""
    LOGGER.debug("Finalizing contents")

    if grammar and len(grammar.rules) > 0:
        check_grammar_consistency(grammar, given_used_symbols)

    if grammar and constraints:
        check_constraints_existence(grammar, constraints)

    grammar.prime()