import types
from collections.abc import Callable
from typing import Optional

from antlr4.Lexer import Lexer
from antlr4.Parser import Parser
from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.Recognizer import Recognizer
from antlr4.Token import Token
from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree import ParseTree

from .FandangoLexer import FandangoLexer
from .FandangoParser import FandangoParser

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
    ) -> None:
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
    stream: InputStream, entry_rule_name: str, sa_err_listener: Optional[SA_ErrorListener] = None
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

# need to specify the type to allow mypy to deal with the dynamic import
native_cpp_parse: Optional[
    Callable[
        [type[FandangoParser], InputStream, str, Optional[SA_ErrorListener]],
        ParseTree,
    ]
] = None

try:
    from fandango.native import cpp_parse as native_cpp_parse
except ImportError:
    USE_CPP_IMPLEMENTATION = False


def _cpp_parse(
    stream: InputStream, entry_rule_name: str, sa_err_listener: Optional[SA_ErrorListener] = None
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

    if native_cpp_parse is None:
        raise RuntimeError("C++ parser is not available")

    return native_cpp_parse(
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

    def syntaxError(
        self,
        recognizer: Recognizer,
        offendingSymbol: Token,
        line: int,
        column: int,
        msg: str,
        e: Optional[Exception] = None,
    ) -> None:
        if isinstance(recognizer, Lexer):
            input_stream = recognizer.inputStream
        elif isinstance(recognizer, Parser):
            input_stream = recognizer.getInputStream() # type: ignore[no-untyped-call]
        else:
            raise RuntimeError("Unknown recognizer type")

        char_index = input_stream.index

        self.sa_err_listener.syntaxError(
            self.input_stream, offendingSymbol, char_index, line, column, msg
        )


def _py_parse(
    stream: InputStream, entry_rule_name: str, sa_err_listener: Optional[SA_ErrorListener] = None
) -> ParseTree:
    if sa_err_listener is not None:
        err_listener = _FallbackErrorTranslator(sa_err_listener, stream)

    # Lex
    lexer = FandangoLexer(stream)
    if sa_err_listener is not None:
        lexer.removeErrorListeners() # type: ignore[no-untyped-call]
        lexer.addErrorListener(err_listener) # type: ignore[no-untyped-call]
    token_stream = CommonTokenStream(lexer)

    # Parse
    parser = FandangoParser(token_stream)
    if sa_err_listener is not None:
        parser.removeErrorListeners()
        parser.addErrorListener(err_listener)

    entry_rule_func = getattr(parser, entry_rule_name, None)
    if not isinstance(entry_rule_func, types.MethodType):
        raise ValueError("Invalid entry_rule_name '%s'" % entry_rule_name)
    entry_rule = entry_rule_func()
    assert isinstance(entry_rule, ParseTree)
    return entry_rule
