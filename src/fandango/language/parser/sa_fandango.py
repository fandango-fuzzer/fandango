# This file was auto-generated by speedy-antlr-tool v1.4.3
#  https://github.com/amykyta3/speedy-antlr-tool

import sys
import types

import antlr4
from antlr4 import InputStream, CommonTokenStream, Token
from antlr4.tree.Tree import ParseTree
from antlr4.error.ErrorListener import ErrorListener

from .FandangoParser import FandangoParser
from .FandangoLexer import FandangoLexer

# -------------------------------------------------------------------------------
# User API
# -------------------------------------------------------------------------------
#: Defines whether C++ implementation is used when calling parse()
#: This is automatically set to False if the accelerator is not available.
#: You may override this to False to force use of Python fallback implementation.
USE_CPP_IMPLEMENTATION = True


class SA_ErrorListener:
    """
    Base callback class to handle Antlr syntax errors.

    Not able to do a 1-to-1 bridge of Antlr's error listener
    Instead, this class provides roughly equivalent functionality.
    """

    def syntaxError(
        self,
        input_stream: InputStream,
        offendingSymbol: Token,
        char_index: int,
        line: int,
        column: int,
        msg: str,
    ):
        """
        Called when lexer or parser encountered a syntax error.

        Parameters
        ----------
        input_stream:InputStream
            Reference to the original input stream that this error is from

        offendingSymbol:Token
            If available, denotes the erronous token

        char_index:int
            Character offset of the error within the input stream

        line:int
            Line number of the error

        column:int
            Character offset within the line

        msg:str
            Antlr error message
        """
        pass


def parse(
    stream: InputStream, entry_rule_name: str, sa_err_listener: SA_ErrorListener = None
) -> ParseTree:
    """
    Parse the input stream

    If C++ implementation of parser is not available, automatically falls back
    to Python implementation.

    Parameters
    ----------
    stream:InputStream
        Source stream to lex & parse

    entry_rule_name:str
        Name of grammar rule to use as the entry point

    sa_err_listener:SA_ErrorListener
        Optionally override the error listener.
        By default, Antlr's default ConsoleErrorListener is used

        Important! This is NOT a reference to an Antlr ErrorListener class!
        This is a slightly different implementation.
    """
    if USE_CPP_IMPLEMENTATION:
        return _cpp_parse(stream, entry_rule_name, sa_err_listener)
    else:
        return _py_parse(stream, entry_rule_name, sa_err_listener)


# -------------------------------------------------------------------------------
# C++ implementation of parser
# -------------------------------------------------------------------------------

try:
    from . import sa_fandango_cpp_parser
except ImportError:
    USE_CPP_IMPLEMENTATION = False


def _cpp_parse(
    stream: InputStream, entry_rule_name: str, sa_err_listener: SA_ErrorListener = None
) -> ParseTree:
    # Validate input types here before handing over to C++
    if not isinstance(stream, InputStream):
        raise TypeError("'stream' shall be an Antlr InputStream")
    if not isinstance(entry_rule_name, str):
        raise TypeError("'entry_rule_name' shall be a string")
    if sa_err_listener is not None and not isinstance(
        sa_err_listener, SA_ErrorListener
    ):
        raise TypeError(
            "'sa_err_listener' shall be an instance of SA_ErrorListener or None"
        )

    return sa_fandango_cpp_parser.do_parse(
        FandangoParser, stream, entry_rule_name, sa_err_listener
    )


# -------------------------------------------------------------------------------
# Fall-back Python implementation of parser
# -------------------------------------------------------------------------------


class _FallbackErrorTranslator(ErrorListener):
    """
    Translates syntax error to user-defined SA_ErrorListener callback
    """

    def __init__(self, sa_err_listener: SA_ErrorListener, input_stream: InputStream):
        self.sa_err_listener = sa_err_listener
        self.input_stream = input_stream

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if isinstance(recognizer, antlr4.Lexer):
            input_stream = recognizer.inputStream
        elif isinstance(recognizer, antlr4.Parser):
            input_stream = recognizer.getInputStream()
        else:
            raise RuntimeError("Unknown recognizer type")

        char_index = input_stream.index

        self.sa_err_listener.syntaxError(
            self.input_stream, offendingSymbol, char_index, line, column, msg
        )


def _py_parse(
    stream: InputStream, entry_rule_name: str, sa_err_listener: SA_ErrorListener = None
) -> ParseTree:
    if sa_err_listener is not None:
        err_listener = _FallbackErrorTranslator(sa_err_listener, stream)

    # Lex
    lexer = FandangoLexer(stream)
    if sa_err_listener is not None:
        lexer.removeErrorListeners()
        lexer.addErrorListener(err_listener)
    token_stream = CommonTokenStream(lexer)

    # Parse
    parser = FandangoParser(token_stream)
    if sa_err_listener is not None:
        parser.removeErrorListeners()
        parser.addErrorListener(err_listener)

    entry_rule_func = getattr(parser, entry_rule_name, None)
    if not isinstance(entry_rule_func, types.MethodType):
        raise ValueError("Invalid entry_rule_name '%s'" % entry_rule_name)
    return entry_rule_func()
