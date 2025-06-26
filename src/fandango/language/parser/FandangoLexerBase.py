import re
import sys
from typing import TextIO, Optional

# noinspection PyUnresolvedReferences
from fandango.language.parser.FandangoParser import FandangoParser
from antlr4 import Lexer, InputStream, Token
from antlr4.Token import CommonToken

# noinspection PyUnresolvedReferences
from fandango.language.parser.FandangoParser import FandangoParser

# Current lexer instance, set by the generated lexer code
lexer: Optional["FandangoLexerBase"] = None


class FandangoLexerBase(Lexer):
    NEW_LINE_PATTERN = re.compile("[^\r\n\f]+")
    SPACES_PATTERN = re.compile("[\r\n\f]+")

    def __init__(self, input_: InputStream, output: TextIO = sys.stdout):
        super().__init__(input_, output)
        self.tokens: list[Token] = []
        self.indents: list[int] = []
        self.opened = 0
        self.in_python = 0
        self.in_fstring = False

        # Set the global lexer instance to this one
        global lexer
        lexer = self

    def reset(self):
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.in_python = 0
        self.in_fstring = False
        super().reset()

    def emitToken(self, token: Token):
        self._token = token  # type: ignore[assignment] # library seems to be wrong here?
        self.tokens.append(token)

    def nextToken(self) -> Token:
        # Check if the end-of-file is ahead and there are still some DEDENTS expected.
        if self._input.LA(1) == FandangoParser.EOF and len(self.indents) != 0:
            # Remove any trailing EOF tokens from our buffer.
            self.tokens = [
                token for token in self.tokens if token.type != FandangoParser.EOF
            ]

            # First emit an extra line break that serves as the end of the statement.
            self.emitToken(self.commonToken(FandangoParser.NEWLINE, "\n"))

            # Now emit as much DEDENT tokens as needed.
            while len(self.indents) != 0:
                self.emitToken(self.createDedent())
                self.indents.pop()

            # Put the EOF back on the token stream.
            self.emitToken(self.commonToken(FandangoParser.EOF, "<EOF>"))

        next_ = super().nextToken()
        token = next_ if len(self.tokens) == 0 else self.tokens.pop(0)
        # print(
        #     f"nextToken(): {token.text!r} ({token.type}) at {token.start}..{token.stop}", file=sys.stderr
        # )
        return token

    def createDedent(self) -> Token:
        return self.commonToken(FandangoParser.DEDENT, "")

    def commonToken(self, type_: int, text: str) -> Token:
        stop = self.getCharIndex() - 1
        start = stop if text == "" else stop - len(text) + 1
        token = CommonToken(
            self._tokenFactorySourcePair,
            type_,
            Lexer.DEFAULT_TOKEN_CHANNEL,
            start,
            stop,
        )
        token.text = text
        return token

    @staticmethod
    def get_indentation_count(whitespace: str) -> int:
        count = 0
        for c in whitespace:
            if c == "\t":
                count += 8 - count % 8
            else:
                count += 1
        return count

    def at_start_of_input(self) -> bool:
        return self.getCharIndex() == 0

    def open_brace(self) -> None:
        self.opened += 1

    def close_brace(self) -> None:
        self.opened -= 1

    def python_start(self) -> None:
        self.in_python += 1

    def python_end(self) -> None:
        self.in_python = 0

    # while f-string do not consider the string token
    def fstring_start(self):
        self.in_fstring = True

    def fstring_end(self):
        self.in_fstring = False

    def is_not_fstring(self):
        return not self.in_fstring

    def on_newline(self) -> None:
        new_line = self.NEW_LINE_PATTERN.sub("", self.text)
        spaces = self.SPACES_PATTERN.sub("", self.text)

        next_ = self._input.LA(1)
        next_next = self._input.LA(2)

        if self.opened > 0 or (next_next != -1 and next_ in (10, 13, 35)):
            self.skip()
        else:
            self.emitToken(self.commonToken(FandangoParser.NEWLINE, new_line))
            indent = self.get_indentation_count(spaces)
            previous = 0 if len(self.indents) == 0 else self.indents[-1]

            if indent == previous:
                self.skip()
            elif indent > previous:
                self.indents.append(indent)
                self.emitToken(self.commonToken(FandangoParser.INDENT, spaces))
            else:
                while len(self.indents) > 0 and self.indents[-1] > indent:
                    self.in_python -= 1
                    self.emitToken(self.createDedent())
                    self.indents.pop()


# These are called from the generated lexer code


def at_start_of_input() -> None:
    global lexer
    assert lexer is not None
    lexer.at_start_of_input()


def open_brace() -> None:
    global lexer
    assert lexer is not None
    lexer.open_brace()


def close_brace() -> None:
    global lexer
    assert lexer is not None
    lexer.close_brace()


def python_start() -> None:
    global lexer
    assert lexer is not None
    lexer.python_start()


def python_end() -> None:
    global lexer
    assert lexer is not None
    lexer.python_end()


def on_newline() -> None:
    global lexer
    assert lexer is not None
    lexer.on_newline()


def fstring_start() -> None:
    global lexer
    assert lexer is not None
    return lexer.fstring_start()


def fstring_end() -> None:
    global lexer
    assert lexer is not None
    return lexer.fstring_end()


def is_not_fstring() -> None:
    global lexer
    assert lexer is not None
    return lexer.is_not_fstring()
