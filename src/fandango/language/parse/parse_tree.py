import time

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.tree.Tree import ParseTree

import fandango
from fandango.language.parse.parser_error_listeners import (
    PythonAntlrErrorListener,
    SpeedyAntlrErrorListener,
)
from fandango.language.parser import sa_fandango
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.logger import LOGGER

# The C++ extension installs as top-level `sa_fandango_cpp_parser` (see
# CMakeLists.txt), where the relative import generated in sa_fandango can't find it
try:
    import sa_fandango_cpp_parser  # type: ignore[import-not-found]

    sa_fandango.sa_fandango_cpp_parser = sa_fandango_cpp_parser  # type: ignore[attr-defined]
    CPP_PARSER_AVAILABLE = True
except ImportError:
    CPP_PARSER_AVAILABLE = False


def parse_tree(filename: str, fan_contents: str) -> ParseTree:
    error_listener: SpeedyAntlrErrorListener | PythonAntlrErrorListener
    if fandango.Fandango.parser != "legacy":
        if fandango.Fandango.parser == "cpp":
            if not CPP_PARSER_AVAILABLE:
                raise ImportError(
                    "Requested C++ parser not available. "
                    "Check your installation "
                    "or use '--parser=python'"
                )
            sa_fandango.USE_CPP_IMPLEMENTATION = True
        elif fandango.Fandango.parser == "python":
            sa_fandango.USE_CPP_IMPLEMENTATION = False
        elif fandango.Fandango.parser == "auto":
            sa_fandango.USE_CPP_IMPLEMENTATION = CPP_PARSER_AVAILABLE

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
        LOGGER.debug(f"{filename}: parsed in {time.time() - start_time:.2f} seconds")

    else:  # legacy parser
        LOGGER.debug(f"{filename}: setting up legacy .fan parser")
        input_stream = InputStream(fan_contents)
        error_listener = PythonAntlrErrorListener(filename)

        lexer = FandangoLexer(input_stream)
        lexer.removeErrorListeners()  # type: ignore[no-untyped-call] # antlr4 doesn't provide types
        lexer.addErrorListener(error_listener)  # type: ignore[no-untyped-call] # antlr4 doesn't provide types

        parser = FandangoParser(CommonTokenStream(lexer))
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        # Invoke the ANTLR parser
        LOGGER.debug(f"{filename}: parsing .fan content")
        start_time = time.time()
        tree = parser.fandango()  # type: ignore[no-untyped-call] # antlr4 doesn't provide types

        LOGGER.debug(f"{filename}: parsed in {time.time() - start_time:.2f} seconds")

    return tree
