from typing import Optional
from antlr4.error.ErrorListener import ErrorListener
from antlr4.InputStream import InputStream
from antlr4.Recognizer import Recognizer
from antlr4.Token import Token

from fandango.errors import FandangoSyntaxError
from fandango.language.parser import sa_fandango


class PythonAntlrErrorListener(ErrorListener):
    """This is invoked from ANTLR when a syntax error is encountered"""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__()

    def syntaxError(
        self,
        recognizer: Recognizer,
        offendingSymbol: Token,
        line: int,
        column: int,
        msg: str,
        e: Exception,
    ) -> None:
        raise FandangoSyntaxError(
            f"{self.filename!r}, line {line}, column {column}: {msg}"
        )


class SpeedyAntlrErrorListener(sa_fandango.SA_ErrorListener):
    """This is invoked from the speedy ANTLR parser when a syntax error is encountered"""

    def __init__(self, filename: Optional[str] = None) -> None:
        self.filename = filename
        super().__init__()

    def syntaxError(
        self,
        input_stream: InputStream,
        offending_symbol: Token,
        char_index: int,
        line: int,
        column: int,
        msg: str,
    ) -> None:
        raise FandangoSyntaxError(
            f"{self.filename!r}, line {line}, column {column}: {msg}"
        )
