import ast
import hashlib
import os
import platform
import re
import sys
import time
import shutil

from copy import deepcopy
from io import StringIO
from pathlib import Path
from typing import IO, Any, Optional

import cachedir_tag
import dill as pickle
from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from xdg_base_dirs import xdg_cache_home, xdg_data_dirs, xdg_data_home

import fandango
from fandango.errors import FandangoSyntaxError, FandangoValueError
from fandango.constraints import predicates
from fandango.constraints.base import Constraint, SoftValue
from fandango.io import FandangoIO, FandangoParty
from fandango.language.convert import (
    ConstraintProcessor,
    FandangoSplitter,
    GrammarProcessor,
    PythonProcessor,
)
from fandango.language.grammar import (
    FuzzingMode,
    Grammar,
    MessageNestingDetector,
    Node,
    NodeReplacer,
    NodeType,
    NonTerminalNode,
    PacketTruncator,
    SymbolFinder,
    closest_match,
)
from fandango.language.parser import sa_fandango
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import DescendantAttributeSearch, ItemSearch
from fandango.language.stdlib import stdlib
from fandango.language.symbol import NonTerminal, Symbol
from fandango.logger import LOGGER, print_exception


class PythonAntlrErrorListener(ErrorListener):
    """This is invoked from ANTLR when a syntax error is encountered"""

    def __init__(self, filename=None):
        self.filename = filename
        super().__init__()

    def syntaxError(
        self, recognizer, offendingSymbol, line: int, column: int, msg: str, e
    ):
        raise FandangoSyntaxError(
            f"{self.filename!r}, line {line}, column {column}: {msg}"
        )


class SpeedyAntlrErrorListener(sa_fandango.SA_ErrorListener):
    """This is invoked from the speedy ANTLR parser when a syntax error is encountered"""

    def __init__(self, filename=None):
        self.filename = filename
        super().__init__()

    def syntaxError(
        self,
        input_stream,
        offending_symbol,
        char_index: int,
        line: int,
        column: int,
        msg,
    ):
        raise FandangoSyntaxError(
            f"{self.filename!r}, line {line}, column {column}: {msg}"
        )


### Including Files

# Some global variables for `include()`, bwlow

# The current file name, for error messages
CURRENT_FILENAME: str = "<undefined>"

# The list of directories to search for include files
INCLUDES: list[str] = []

# The list of files to parse, with their include depth.
# An include depth of 0 means the file was given as input_.
# A higher include depth means the file was included from another file;
# hence its grammar and constraints should be processed _before_ the current file.
FILES_TO_PARSE: list[tuple[IO | str, int]] = []

# The current include depth
INCLUDE_DEPTH: int = 0


def include(file_to_be_included: str):
    """
    Include FILE_TO_BE_INCLUDED in the current context.
    This function is invoked from .fan files.
    """
    global FILES_TO_PARSE
    global CURRENT_FILENAME
    global INCLUDE_DEPTH

    path = os.path.dirname(CURRENT_FILENAME)
    if not path:
        # If the current file has no path, use the current directory
        path = "."
    if INCLUDES:
        path += ":" + ":".join(INCLUDES)
    if os.environ.get("FANDANGO_PATH"):
        path += ":" + os.environ["FANDANGO_PATH"]
    dirs = [Path(dir) for dir in path.split(":")]

    if platform.system() == "Darwin":
        dirs += [Path.home() / "Library" / "Fandango"]  # ~/Library/Fandango
        dirs += [Path("/Library/Fandango")]  # /Library/Fandango

    dirs += [xdg_data_home() / "fandango"]  # sth like ~/.local/share/fandango
    dirs += [
        dir / "fandango" for dir in xdg_data_dirs()
    ]  # sth like /usr/local/share/fandango

    for dir in dirs:
        try:
            full_file_name = dir / file_to_be_included
            full_file = open(full_file_name, "r")
        except FileNotFoundError:
            continue
        LOGGER.debug(f"{CURRENT_FILENAME}: including {full_file_name}")

        INCLUDE_DEPTH += 1  # Will be lowered when the included file is done processing
        FILES_TO_PARSE.append((full_file, INCLUDE_DEPTH))
        return

    raise FileNotFoundError(
        f"{CURRENT_FILENAME}: {file_to_be_included!r} not found in {':'.join(str(dir) for dir in dirs)}"
    )


### Parsing


class FandangoSpec:
    """
    Helper class to pickle and unpickle parsed Fandango specifications.
    This is necessary because the ANTLR4 parse trees cannot be pickled,
    so we pickle the code text, grammar, and constraints instead.
    """

    GLOBALS = predicates.__dict__
    GLOBALS.update({"include": include})
    LOCALS = None  # Must be None to ensure top-level imports

    def __init__(
        self,
        tree: Any,
        fan_contents: str,
        lazy: bool = False,
        filename: str = "<input_>",
        max_repetitions: int = 5,
    ):
        self.version = fandango.version()
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

        LOGGER.debug(f"{filename}: code text:\n{self.code_text}")

        LOGGER.debug(f"{filename}: running code")
        self.run_code(filename=filename)

        LOGGER.debug(f"{filename}: extracting grammar")
        grammar_processor = GrammarProcessor(
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            id_prefix="{0:x}".format(abs(hash(filename))),
            max_repetitions=max_repetitions,
        )
        self.grammar: Grammar = grammar_processor.get_grammar(
            splitter.productions, prime=False
        )

        LOGGER.debug(f"{filename}: extracting constraints")
        constraint_processor = ConstraintProcessor(
            self.grammar,
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            lazy=self.lazy,
        )
        self.constraints: list[Constraint | SoftValue] = (
            constraint_processor.get_constraints(splitter.constraints)
        )

    def run_code(self, filename: str = "<input_>"):
        global CURRENT_FILENAME
        CURRENT_FILENAME = filename

        # Ensure the directory of the file is in the path
        dirname = os.path.dirname(filename)
        if dirname not in sys.path:
            sys.path.append(dirname)

        # Set up environment as if this were a top-level script
        self.global_vars.update(
            {
                "__name__": "__main__",
                "__file__": filename,
                "__package__": None,
                "__spec__": None,
            }
        )
        exec(self.code_text, self.global_vars, self.local_vars)

    def __repr__(self):
        s = self.code_text
        if s:
            s += "\n\n"
        s += str(self.grammar) + "\n"
        if self.constraints:
            s += "\n"
        s += "\n".join("where " + str(constraint) for constraint in self.constraints)
        return s


def cache_dir() -> Path:
    """Return the parser cache directory"""
    CACHE_DIR = xdg_cache_home() / "fandango"
    if platform.system() == "Darwin":
        cache_path = Path.home() / "Library" / "Caches"
        if os.path.exists(cache_path):
            CACHE_DIR = cache_path / "Fandango"
    return CACHE_DIR


def clear_cache() -> None:
    """Clear the Fandango parser cache"""
    CACHE_DIR = cache_dir()
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR, ignore_errors=True)


def parse_spec(
    fan_contents: str,
    *,
    filename: str = "<input_>",
    use_cache: bool = True,
    lazy: bool = False,
    parties: list[str] | None = None,
    max_repetitions: int = 5,
) -> FandangoSpec:
    """
    Parse given content into a grammar and constraints.
    This is a helper function; use `parse()` as the main entry point.
    :param fan_contents: Fandango specification text
    :param filename: The file name of the content (for error messages)
    :param use_cache: If True (default), cache parsing results
    :param parties: If given, list of parties to consider in the grammar
    :param lazy: If True, the constraints are evaluated lazily
    :return: A FandangoSpec object containing the parsed grammar, constraints, and code text.
    """
    spec: Optional[FandangoSpec] = None
    from_cache = False

    CACHE_DIR = cache_dir()
    if use_cache:
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR, mode=0o700)
            cachedir_tag.tag(CACHE_DIR, application="Fandango")

        # Keep separate hashes for different Fandango and Python versions
        hash_contents = fan_contents + fandango.version() + "-" + sys.version
        hash = hashlib.sha256(hash_contents.encode()).hexdigest()
        pickle_file = CACHE_DIR / (hash + ".pickle")

        if os.path.exists(pickle_file):
            try:
                with open(pickle_file, "rb") as fp:
                    LOGGER.info(f"{filename}: loading cached spec from {pickle_file}")
                    start_time = time.time()
                    spec = pickle.load(fp)
                    assert spec is not None
                    LOGGER.debug(f"Cached spec version: {spec.version}")
                    if spec.fan_contents != fan_contents:
                        error = FandangoValueError(
                            "Hash collision (If you get this, you'll be real famous)"
                        )
                        raise error

                    LOGGER.debug(
                        f"{filename}: loaded from cache in {time.time() - start_time:.2f} seconds"
                    )
                    from_cache = True
            except Exception as exc:
                LOGGER.debug(type(exc).__name__ + ":" + str(exc))

    if spec:
        LOGGER.debug(f"{filename}: running code")
        try:
            spec.run_code(filename=filename)
        except Exception as exc:
            # In case the error has anything to do with caching, play it safe
            LOGGER.debug(f"Cached spec failed; removing {pickle_file}")
            os.remove(pickle_file)
            raise exc

    error_listener: SpeedyAntlrErrorListener | PythonAntlrErrorListener
    if not spec:
        if fandango.Fandango.parser != "legacy":
            if fandango.Fandango.parser == "cpp":
                sa_fandango.USE_CPP_IMPLEMENTATION = True
                try:
                    from .parser import sa_fandango_cpp_parser  # type: ignore[attr-defined]
                except ImportError:
                    raise ImportError(
                        "Requested C++ parser not available. "
                        "Check your installation "
                        "or use '--parser=python'"
                    )
            elif fandango.Fandango.parser == "python":
                sa_fandango.USE_CPP_IMPLEMENTATION = False
            elif fandango.Fandango.parser == "auto":
                pass  # let sa_fandango decide

            if sa_fandango.USE_CPP_IMPLEMENTATION:
                LOGGER.debug(f"{filename}: setting up C++ .fan parser")
            else:
                LOGGER.debug(f"{filename}: setting up Python .fan parser")

            input_stream = InputStream(fan_contents)
            error_listener = SpeedyAntlrErrorListener(filename)

            # Invoke the Speedy ANTLR parser
            LOGGER.debug(f"{filename}: parsing .fan content")
            start_time = time.time()
            tree = sa_fandango.parse(input_stream, "fandango", error_listener)
            LOGGER.debug(
                f"{filename}: parsed in {time.time() - start_time:.2f} seconds"
            )

        else:  # legacy parser
            LOGGER.debug(f"{filename}: setting up legacy .fan parser")
            input_stream = InputStream(fan_contents)
            error_listener = PythonAntlrErrorListener(filename)

            lexer = FandangoLexer(input_stream)
            lexer.removeErrorListeners()
            lexer.addErrorListener(error_listener)

            token_stream = CommonTokenStream(lexer)
            parser = FandangoParser(token_stream)
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)

            # Invoke the ANTLR parser
            LOGGER.debug(f"{filename}: parsing .fan content")
            start_time = time.time()
            tree = parser.fandango()

            LOGGER.debug(
                f"{filename}: parsed in {time.time() - start_time:.2f} seconds"
            )

        LOGGER.debug(f"{filename}: splitting content")
        spec = FandangoSpec(
            tree, fan_contents, lazy, filename=filename, max_repetitions=max_repetitions
        )

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

    if parties:
        slice_parties(spec.grammar, parties)

    LOGGER.debug(f"{filename}: parsing complete")
    return spec


# Legacy interface
def parse_content(*args, **kwargs) -> tuple[Grammar, list[Constraint | SoftValue]]:
    spec = parse_spec(*args, **kwargs)
    return spec.grammar, spec.constraints


# Save the set of symbols used in the standard library and imported grammars
USED_SYMBOLS: set[str] = set()

# Save the standard library grammar and constraints
STDLIB_GRAMMAR: Optional[Grammar] = None
STDLIB_CONSTRAINTS: Optional[list[Constraint | SoftValue]] = None


def parse(
    fan_files: str | IO | list[str | IO],
    constraints: Optional[list[str]] = None,
    *,
    use_cache: bool = True,
    use_stdlib: bool = True,
    check: bool = True,
    lazy: bool = False,
    given_grammars: list[Grammar] = [],
    start_symbol: Optional[str] = None,
    includes: Optional[list[str]] = [],
    parties: Optional[list[str]] = None,
    max_repetitions: int = 5,
) -> tuple[Optional[Grammar], list[Constraint | SoftValue]]:
    """
    Parse .fan content, handling multiple files, standard library, and includes.
    :param fan_files: One (open) .fan file, one string, or a list of these
    :param constraints: List of constraints (as strings); default: []
    :param use_cache: If True (default), cache parsing results
    :param use_stdlib: If True (default), use the standard library
    :param check: If True (default), the constraints are checked for consistency
    :param lazy: If True, the constraints are evaluated lazily
    :param given_grammars: Grammars to use in addition to the standard library
    :param start_symbol: The grammar start symbol (default: "<start>")
    :param includes: A list of directories to search for include files; default: []
    :param parties: If given, list of parties to consider in the grammar
    :param max_repetitions: The maximal number of repetitions
    :return: A tuple of the grammar and constraints
    """

    if not isinstance(fan_files, list):
        fan_files = [fan_files]

    if not fan_files and not constraints:
        return None, []

    if constraints is None:
        constraints = []

    if includes is None:
        includes = []

    if start_symbol is None:
        start_symbol = "<start>"

    global STDLIB_SYMBOLS, STDLIB_GRAMMAR, STDLIB_CONSTRAINTS
    if use_stdlib and STDLIB_GRAMMAR is None:
        LOGGER.debug("Reading standard library")
        STDLIB_GRAMMAR, STDLIB_CONSTRAINTS = parse_content(
            stdlib,
            filename="<stdlib>",
            use_cache=use_cache,
            max_repetitions=max_repetitions,
        )

    global USED_SYMBOLS
    USED_SYMBOLS = set()
    if use_stdlib:
        assert STDLIB_GRAMMAR is not None
        for symbol in STDLIB_GRAMMAR.rules.keys():
            # Do not complain about unused symbols in the standard library
            USED_SYMBOLS.add(str(symbol))

    global INCLUDES
    INCLUDES = includes

    grammars = []
    parsed_constraints: list[Constraint | SoftValue] = []
    if use_stdlib:
        assert STDLIB_GRAMMAR is not None
        assert STDLIB_CONSTRAINTS is not None
        try:
            grammars = [deepcopy(STDLIB_GRAMMAR)]
        except TypeError:
            # This can happen if we invoke parse() from a notebook
            grammars = [STDLIB_GRAMMAR]
        parsed_constraints = STDLIB_CONSTRAINTS.copy()

    grammars += given_grammars

    LOGGER.debug("Reading files")
    more_grammars = []
    global FILES_TO_PARSE
    FILES_TO_PARSE = [(file, 0) for file in fan_files]

    global INCLUDE_DEPTH
    INCLUDE_DEPTH = 0

    mode = FuzzingMode.COMPLETE

    while FILES_TO_PARSE:
        (file, depth) = FILES_TO_PARSE.pop(0)
        if isinstance(file, str):
            file = StringIO(file)
            file.name = "<string>"

        LOGGER.debug(f"Reading {file.name} (depth = {depth})")
        fan_contents = file.read()
        new_grammar, new_constraints = parse_content(
            fan_contents,
            filename=file.name,
            use_cache=use_cache,
            lazy=lazy,
            max_repetitions=max_repetitions,
        )
        parsed_constraints += new_constraints
        assert new_grammar is not None
        if new_grammar.fuzzing_mode == FuzzingMode.IO:
            mode = FuzzingMode.IO

        if depth == 0:
            # Given file: process in order
            more_grammars.append(new_grammar)
            for generator in new_grammar.generators.values():
                for nonterminal in generator.nonterminals.values():
                    USED_SYMBOLS.add(nonterminal.symbol.symbol)
        else:
            # Included file: process _before_ current grammar
            more_grammars = [new_grammar] + more_grammars
            # Do not complain about unused symbols in included files
            for symbol in new_grammar.rules.keys():
                USED_SYMBOLS.add(str(symbol))
            for generator in new_grammar.generators.values():
                for nonterminal in generator.nonterminals.values():
                    USED_SYMBOLS.add(nonterminal.symbol.symbol)

        if INCLUDE_DEPTH > 0:
            INCLUDE_DEPTH -= 1

    grammars += more_grammars

    LOGGER.debug(f"Processing {len(grammars)} grammars")
    grammar = grammars[0]
    LOGGER.debug(f"Grammar #1: {[str(key) for key in grammar.rules.keys()]}")
    n = 2
    for g in grammars[1:]:
        LOGGER.debug(f"Grammar #{n}: {[str(key) for key in g.rules.keys()]}")

        for symbol in g.rules.keys():
            if symbol in grammar.rules:
                LOGGER.info(f"Redefining {symbol}")

        grammar.update(g, prime=False)
        n += 1

    LOGGER.debug(f"Final grammar: {[str(key) for key in grammar.rules.keys()]}")

    grammar.fuzzing_mode = mode
    LOGGER.debug(f"Grammar fuzzing mode: {grammar.fuzzing_mode}")

    LOGGER.debug("Processing constraints")
    for constraint in constraints or []:
        LOGGER.debug(f"Constraint {constraint}")
        first_token = constraint.split()[0]
        if any(
            first_token.startswith(kw) for kw in ["where", "minimizing", "maximizing"]
        ):
            _, new_constraints = parse_content(
                constraint, filename=constraint, use_cache=use_cache, lazy=lazy
            )
        else:
            _, new_constraints = parse_content(
                "where " + constraint,
                filename=constraint,
                use_cache=use_cache,
                lazy=lazy,
            )
        parsed_constraints += new_constraints

    if check:
        LOGGER.debug("Checking and finalizing content")
        if grammar and len(grammar.rules) > 0:
            check_grammar_consistency(
                grammar, given_used_symbols=USED_SYMBOLS, start_symbol=start_symbol
            )

        if grammar and parsed_constraints:
            check_constraints_existence(grammar, parsed_constraints)

    global_env, local_env = grammar.get_spec_env()
    if not parties and grammar.fuzzing_mode == FuzzingMode.IO:
        # Prepare for interaction
        if "FandangoIO" not in global_env.keys():
            exec("FandangoIO.instance()", global_env, local_env)
        io_instance: FandangoIO = global_env["FandangoIO"].instance()

        assign_implicit_party(grammar, "StdOut")
        init_msg_parties(grammar, io_instance)
        remap_to_std_party(grammar, io_instance)
        init_msg_parties(grammar, io_instance)

        # Detect illegally nested data packets.
        rir_detector = MessageNestingDetector(grammar)
        rir_detector.fail_on_nested_packet(NonTerminal(start_symbol))
        fail_on_party_in_generator(grammar)

        truncate_invisible_packets(grammar, io_instance)

    # We invoke this at the very end, now that all data is there
    grammar.update(grammar, prime=check)
    if check:
        grammar.prime()

    if parties:
        slice_parties(grammar, parties)

    LOGGER.debug("All contents parsed")
    return grammar, parsed_constraints


### Consistency Checks


def fail_on_party_in_generator(grammar):
    for nt, node in grammar.rules.items():
        if nt not in grammar.generators:
            continue
        found_node = is_party_reachable(grammar, node)
        if found_node is not None:
            raise ValueError(
                f"{found_node} contains a party or recipient and is generated using the generator on {nt}. This is not allowed!"
            )

    for nt in grammar.generators.keys():
        dependencies: set[NonTerminal] = grammar.generator_dependencies(nt)
        for dep_nt in dependencies:
            found_node = is_party_reachable(grammar, grammar[dep_nt])
            if found_node is not None:
                raise ValueError(
                    f"{found_node} contains a party or recipient and is a parameter for the generator of {nt}. This is not allowed!"
                )


def is_party_reachable(grammar, node):
    seen_nt_nodes = set()
    symbol_finder = SymbolFinder()
    symbol_finder.visit(node)
    nt_node_queue: set[NonTerminalNode] = set(symbol_finder.nonTerminalNodes)
    while len(nt_node_queue) != 0:
        current_node = nt_node_queue.pop()
        if current_node.sender is not None or current_node.recipient is not None:
            return current_node

        seen_nt_nodes.add(current_node)
        symbol_finder = SymbolFinder()
        symbol_finder.visit(grammar[current_node.symbol])
        for next_nt in symbol_finder.nonTerminalNodes:
            if next_nt not in seen_nt_nodes:
                nt_node_queue.add(next_nt)
    return None


def init_msg_parties(
    grammar: "Grammar", io_instance: FandangoIO, ignore_existing: bool = True
):
    party_names = set()
    grammar_msg_parties = grammar.msg_parties(include_recipients=True)
    global_env, local_env = grammar.get_spec_env()

    # Initialize FandangoParty instances
    for key in global_env.keys():
        if key in grammar_msg_parties:
            the_type = global_env[key]
            if not isinstance(the_type, type):
                continue
            if FandangoParty in the_type.__mro__:
                party_names.add(key)
    # Call constructor
    for party in party_names:
        if party in io_instance.parties.keys() and ignore_existing:
            continue
        exec(f"{party}()", global_env, local_env)
        grammar_msg_parties.remove(party)


# Assign STD party to all parties which have no party-class defined.
def remap_to_std_party(grammar: "Grammar", io_instance: FandangoIO):
    remapped_parties = set()
    unknown_recipients = set()
    for symbol in grammar.rules.keys():
        symbol_finder = SymbolFinder()
        symbol_finder.visit(grammar.rules[symbol])
        non_terminals: list[NonTerminalNode] = symbol_finder.nonTerminalNodes

        for nt in non_terminals:
            if nt.sender is not None:
                if nt.sender not in io_instance.parties.keys():
                    remapped_parties.add(nt.sender)
                    nt.sender = "StdOut"
            if nt.recipient is not None:
                if nt.recipient not in io_instance.parties.keys():
                    unknown_recipients.add(nt.recipient)

    for name in remapped_parties:
        LOGGER.warning(f"Party {name!r} unspecified; will use 'StdOut' instead")
    if unknown_recipients:
        raise FandangoValueError(f"Recipients {unknown_recipients!r} unspecified")


def truncate_invisible_packets(grammar: "Grammar", io_instance: FandangoIO) -> None:
    keep_parties = grammar.msg_parties(include_recipients=True)
    io_instance.parties.keys()
    for existing_party in list(keep_parties):
        if not io_instance.parties[existing_party].is_fuzzer_controlled():
            keep_parties.remove(existing_party)

    for nt in grammar.rules.keys():
        PacketTruncator(grammar, keep_parties).visit(grammar.rules[nt])


def check_grammar_consistency(
    grammar, *, given_used_symbols=set(), start_symbol="<start>"
):
    check_grammar_definitions(
        grammar, given_used_symbols=given_used_symbols, start_symbol=start_symbol
    )
    check_grammar_types(grammar, start_symbol=start_symbol)


def check_grammar_definitions(
    grammar, *, given_used_symbols=set(), start_symbol="<start>"
):
    if not grammar:
        return

    LOGGER.debug("Checking grammar")

    used_symbols = set()
    undefined_symbols = set()
    defined_symbols = set()

    for symbol in grammar.rules.keys():
        defined_symbols.add(str(symbol))

    if start_symbol not in defined_symbols:
        if start_symbol == "<start>":
            raise FandangoValueError(
                f"Start symbol {start_symbol!s} not defined in grammar"
            )
        closest = closest_match(start_symbol, defined_symbols)
        raise FandangoValueError(
            f"Start symbol {start_symbol!r} not defined in grammar. Did you mean {closest!r}?"
        )

    def collect_used_symbols(node: Node):
        if node.node_type == NodeType.NON_TERMINAL:
            used_symbols.add(str(node.symbol))  # type: ignore[attr-defined] # We're checking types manually
        elif (
            node.node_type == NodeType.REPETITION
            or node.node_type == NodeType.STAR
            or node.node_type == NodeType.PLUS
            or node.node_type == NodeType.OPTION
        ):
            collect_used_symbols(node.node)  # type: ignore[attr-defined] # We're checking types manually

        for child in node.children():
            collect_used_symbols(child)

    for tree in grammar.rules.values():
        collect_used_symbols(tree)

    for symbol in used_symbols:
        if symbol not in defined_symbols:
            undefined_symbols.add(symbol)

    for symbol in defined_symbols:
        if (
            symbol not in used_symbols
            and symbol not in given_used_symbols
            and symbol != start_symbol
            and symbol != "<start>"  # Allow <start> to be defined but not used
        ):
            LOGGER.warning(f"Symbol {symbol!s} defined, but not used")

    if undefined_symbols:
        first_undefined_symbol = undefined_symbols.pop()
        error = FandangoValueError(
            f"Undefined symbol {first_undefined_symbol!s} in grammar"
        )
        if undefined_symbols:
            if getattr(Exception, "add_note", None):
                # Python 3.11+ has add_note() method
                error.add_note(
                    f"Other undefined symbols: {', '.join(str(symbol) for symbol in undefined_symbols)}"
                )
        raise error


def check_grammar_types(grammar, *, start_symbol="<start>"):
    if not grammar:
        return

    LOGGER.debug("Checking types")

    symbol_types: dict[Symbol, tuple[Optional[str], int, int, int]] = {}

    def compatible(tp1, tp2):
        if tp1 in ["int", "bytes"] and tp2 in ["int", "bytes"]:
            return True
        return tp1 == tp2

    def get_type(tree, rule_symbol) -> tuple[Optional[str], int, int, int]:
        # LOGGER.debug(f"Checking type of {tree!s} in {rule_symbol!s} ({tree.node_type!s})")
        nonlocal symbol_types, grammar

        tp: Optional[str]
        if tree.node_type == NodeType.TERMINAL:
            tp = type(tree.symbol.symbol).__name__
            # LOGGER.debug(f"Type of {tree.symbol.symbol!r} is {tp!r}")
            bits = 1 if isinstance(tree.symbol.symbol, int) else 0
            return tp, bits, bits, 0

        elif (
            tree.node_type == NodeType.REPETITION
            or tree.node_type == NodeType.STAR
            or tree.node_type == NodeType.PLUS
            or tree.node_type == NodeType.OPTION
        ):
            tp, min_bits, max_bits, step = get_type(tree.node, rule_symbol)
            # if min_bits % 8 != 0 and tree.min == 0:
            #     raise FandangoValueError(f"{rule_symbol!s}: Bits cannot be optional")

            try:
                rep_min = tree.min(grammar, None)
            except ValueError:
                rep_min = 0
            try:
                rep_max = tree.max(grammar, None)
            except ValueError:
                # Add 7 to min, such that there are 8 steps.
                # If result is not dividable by 8 this will catch at least one case.
                rep_max = rep_min + 7

            step = min(min_bits, max_bits)
            return tp, rep_min * min_bits, rep_max * max_bits, step

        elif tree.node_type == NodeType.NON_TERMINAL:
            if tree.symbol in symbol_types:
                return symbol_types[tree.symbol]

            symbol_types[tree.symbol] = (None, 0, 0, 0)
            symbol_tree = grammar.rules[tree.symbol]
            tp, min_bits, max_bits, step = get_type(symbol_tree, str(tree.symbol))
            symbol_types[tree.symbol] = tp, min_bits, max_bits, step
            # LOGGER.debug(f"Type of {tree.symbol!s} is {tp!r} with {min_bits}..{max_bits} bits")
            return tp, min_bits, max_bits, step

        elif (
            tree.node_type == NodeType.CONCATENATION
            or tree.node_type == NodeType.ALTERNATIVE
        ):
            common_tp = None
            tp_child = None
            first = True
            min_bits = 0
            max_bits = 0
            step = 0
            for child in tree.children():
                tp, min_child_bits, max_child_bits, child_step = get_type(
                    child, rule_symbol
                )
                if first:
                    min_bits = min_child_bits
                    max_bits = max_child_bits
                    step = child_step
                    first = False
                elif tree.node_type == NodeType.CONCATENATION:
                    min_bits += min_child_bits
                    max_bits += max_child_bits
                    step += child_step
                else:  # NodeType.ALTERNATIVE
                    min_bits = min(min_bits, min_child_bits)
                    max_bits = max(max_bits, max_child_bits)
                    step += min(step, child_step)
                if tp is None:
                    continue
                if common_tp is None:
                    common_tp = tp
                    tp_child = child
                    continue
                if not compatible(tp, common_tp):
                    if tree.node_type == NodeType.CONCATENATION:
                        LOGGER.warning(
                            f"{rule_symbol!s}: Concatenating {common_tp!r} ({tp_child!s}) and {tp!r} ({child!s})"
                        )
                    else:
                        LOGGER.warning(
                            f"{rule_symbol!s}: Type can be {common_tp!r} ({tp_child!s}) or {tp!r} ({child!s})"
                        )
                    common_tp = tp

            # LOGGER.debug(f"Type of {rule_symbol!s} is {common_tp!r} with {min_bits}..{max_bits} bits")
            return common_tp, min_bits, max_bits, step

        raise FandangoValueError("Unknown node type")

    start_tree = grammar.rules[NonTerminal(start_symbol)]
    _, min_start_bits, max_start_bits, start_step = get_type(
        start_tree, str(start_symbol)
    )
    if start_step > 0 and any(
        bits % 8 != 0 for bits in range(min_start_bits, max_start_bits + 1, start_step)
    ):
        if min_start_bits != max_start_bits:
            LOGGER.warning(
                f"{start_symbol!s}: Number of bits ({min_start_bits}..{max_start_bits}) may not be a multiple of eight"
            )
        else:
            LOGGER.warning(
                f"{start_symbol!s}: Number of bits ({min_start_bits}) is not a multiple of eight"
            )


def check_constraints_existence(grammar, constraints):
    LOGGER.debug("Checking constraints")

    indirect_child = {
        str(k): {str(l): None for l in grammar.rules.keys()}
        for k in grammar.rules.keys()
    }

    defined_symbols = []
    for symbol in grammar.rules.keys():
        defined_symbols.append(str(symbol))

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
                missing_symbols = ", ".join(
                    ["<" + str(symbol) + ">" for symbol in missing]
                )
                error = FandangoValueError(
                    f"{constraint}: undefined symbols {missing_symbols}. Did you mean {closest!r}?"
                )
                raise error

            if len(missing) == 1:
                missing_symbol = missing[0]
                error = FandangoValueError(
                    f"{constraint}: undefined symbol <{missing_symbol!r}>. Did you mean {closest!r}?"
                )
                raise error

            for i in range(len(constraint_matches) - 1):
                parent = constraint_matches[i]
                symbol = constraint_matches[i + 1]
                # This handles <parent>[...].<symbol> as <parent>..<symbol>.
                # We could also interpret the actual [...] contents here,
                # but slices and chains could make this hard -- AZ
                recurse = isinstance(value, DescendantAttributeSearch) or isinstance(
                    value, ItemSearch
                )
                if not check_constraints_existence_children(
                    grammar, parent, symbol, recurse, indirect_child
                ):
                    msg = f"{constraint!s}: <{parent!s}> has no child <{symbol!s}>"
                    raise FandangoValueError(msg)


def check_constraints_existence_children(
    grammar, parent, symbol, recurse, indirect_child
):
    # LOGGER.debug(f"Checking if <{symbol}> is a child of <{parent}>")

    if indirect_child[f"<{parent}>"][f"<{symbol}>"] is not None:
        return indirect_child[f"<{parent}>"][f"<{symbol}>"]

    grammar_symbols = grammar.rules[NonTerminal(f"<{parent}>")]

    # Original code; fails on <a> "b" <c> -- AZ
    # grammar_matches = re.findall(r'(?<!")<([^>]*)>(?!".*)',
    #                              str(grammar_symbols))
    #
    # Simpler version; may overfit (e.g. matches <...> in strings),
    # but that should not hurt us -- AZ
    finder = SymbolFinder()
    finder.visit(grammar_symbols)
    non_terminals = [str(nt.symbol)[1:-1] for nt in finder.nonTerminalNodes]

    if symbol in non_terminals:
        indirect_child[f"<{parent}>"][f"<{symbol}>"] = True
        return True

    is_child = False
    for match in non_terminals:
        if recurse or match.startswith("_"):
            is_child = is_child or check_constraints_existence_children(
                grammar, match, symbol, recurse, indirect_child
            )
    indirect_child[f"<{parent}>"][f"<{symbol}>"] = is_child
    return is_child


def slice_parties(grammar: "Grammar", parties: list[str]) -> None:
    """
    Slice the given parties from the grammar.
    :param grammar: The grammar to check
    :param parties: List of party names to check
    :raises FandangoValueError: If a party is not defined in the grammar
    """
    if not parties:
        return

    defined_parties = set(grammar.msg_parties(include_recipients=True))
    for party in parties:
        if party not in defined_parties:
            closest = closest_match(party, defined_parties)
            raise FandangoValueError(
                f"Party {party!r} not defined in the grammar. Did you mean {closest!r}?"
            )

    grammar.slice_parties(parties)


def assign_implicit_party(grammar, implicit_party: str):
    seen_nts: set[NonTerminal] = set()
    seen_nts.add(NonTerminal("<start>"))
    processed_nts: set[NonTerminal] = set()
    unprocessed_nts: set[NonTerminal] = seen_nts.difference(processed_nts)

    while len(unprocessed_nts) > 0:
        current_symbol = unprocessed_nts.pop()
        current_node = grammar.rules[current_symbol]

        symbol_finder = SymbolFinder()
        symbol_finder.visit(current_node)
        rule_nts = list(
            filter(lambda x: x not in processed_nts, symbol_finder.nonTerminalNodes)
        )

        if current_node in rule_nts and not isinstance(current_node, NonTerminalNode):
            rule_nts.remove(current_node)
        child_party: set[str] = set()

        for c_node in rule_nts:
            child_party |= c_node.msg_parties(include_recipients=False)

        if len(child_party) == 0:
            processed_nts.add(current_symbol)
            unprocessed_nts = seen_nts.difference(processed_nts)
            continue
        for c_node in rule_nts:
            seen_nts.add(c_node.symbol)
            if len(c_node.msg_parties(include_recipients=False)) != 0:
                continue
            c_node.sender = implicit_party
        for t_node in symbol_finder.terminalNodes:
            terminal_id = 0
            rule_nt = NonTerminal(f"<_terminal:{terminal_id}>")
            while rule_nt in grammar.rules:
                terminal_id += 1
                rule_nt = NonTerminal(f"<_terminal:{terminal_id}>")
            n_node = NonTerminalNode(rule_nt, implicit_party)
            NodeReplacer(t_node, n_node).visit(current_node)
            grammar.rules[rule_nt] = t_node

        processed_nts.add(current_symbol)
        unprocessed_nts = seen_nts.difference(processed_nts)
