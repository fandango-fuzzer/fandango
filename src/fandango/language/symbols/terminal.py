import functools
import re
from io import UnsupportedOperation
from typing import Any, cast

import regex

from fandango.errors import FandangoValueError
from fandango.language.symbols.symbol import Symbol, SymbolType
from fandango.language.tree_value import (
    BYTES_TO_STRING_ENCODING,
    TreeValue,
    TreeValueType,
)


@functools.cache
def _compile(symbol: str | bytes) -> Any:
    return regex.compile(symbol)  # type: ignore[no-untyped-call] # regex doesn't provide types


class Terminal(Symbol):
    def __init__(self, symbol: str | bytes | int | TreeValue) -> None:
        super().__init__(symbol, SymbolType.TERMINAL)

    def count_bytes(self) -> int:
        return self._value.count_bytes()

    @staticmethod
    def string_prefix(symbol: str) -> str:
        """Return the first letters ('f', 'b', 'r', ...) of a string literal"""
        match = re.match(r"([a-zA-Z]+)", symbol)
        return match.group(0) if match else ""

    @staticmethod
    def clean(symbol: str) -> str | bytes | int:
        # LOGGER.debug(f"Cleaning {symbol!r}")
        if symbol.startswith("f'") or symbol.startswith('f"'):
            # Cannot evaluate f-strings
            raise UnsupportedOperation("f-strings are currently not supported")

        return cast(
            str | bytes | int, eval(symbol)
        )  # also handles bits "0" and "1", just cast because of performance

    @staticmethod
    def from_symbol(symbol: str) -> "Terminal":
        t = Terminal(Terminal.clean(symbol))
        t._is_regex = "r" in Terminal.string_prefix(symbol)
        return t

    @staticmethod
    def from_number(number: str) -> "Terminal":
        return Terminal(Terminal.clean(number))

    def _align_type(self, word: str | bytes) -> tuple[str | bytes, str | bytes]:
        """
        Converts word and tree value such that they have the same type (string or bytes).
        """
        if isinstance(word, bytes):
            if self._value.is_type(TreeValueType.BYTES):
                return self._value.to_bytes(), word
            word = word.decode(BYTES_TO_STRING_ENCODING)
        return self._value.to_string(), word

    def regex_check_multiple_lengths(
        self, word: str | bytes, min_length: int = 1
    ) -> tuple[list[int], bool]:
        """
        Every length from `min_length` on at which this regex matches
        `word[:length]`, and whether the word could be further extended
         and still match the regex.
        """
        assert self.is_regex
        symbol, word = self._align_type(word)
        pattern = _compile(symbol)
        lengths: list[int] = []
        can_continue = False
        for length in range(min_length, len(word) + 1):
            match = pattern.fullmatch(word, 0, length, partial=True)
            can_continue = match is not None
            if not can_continue:
                break
            if not match.partial:
                lengths.append(length)
        return lengths, can_continue

    def check(
        self, word: str | bytes | int, incomplete: bool = False
    ) -> tuple[bool, int]:
        """Return (True, # characters matched by `word`), or (False, 0)"""

        if self._value.is_type(TreeValueType.TRAILING_BITS_ONLY) or isinstance(
            word, int
        ):
            return self.check_all(word), 1
        symbol, check_word = self._align_type(word)
        if self.is_regex:
            pattern = _compile(symbol)
            if incomplete:
                match = pattern.fullmatch(check_word, partial=True)
            else:
                match = pattern.match(check_word)
            if match is not None:
                return True, match.end()
            return False, 0

        if incomplete:
            prefix = check_word
            full_word = symbol
        else:
            prefix = symbol
            full_word = check_word
        if isinstance(full_word, str):
            assert isinstance(prefix, str)
            if full_word.startswith(prefix):
                return True, len(prefix)
        else:
            assert isinstance(full_word, bytes)
            assert isinstance(prefix, bytes)
            if full_word.startswith(prefix):
                return True, len(prefix)

        return False, 0

    def check_all(self, word: str | bytes | int) -> bool:
        if isinstance(word, str):
            return self._value.to_string() == word
        elif isinstance(word, bytes):
            return self._value.to_bytes() == word
        elif isinstance(word, int):
            return int(self._value) == word
        else:
            raise FandangoValueError(f"Invalid word type: {type(word)}")

    def format_as_spec(self) -> str:
        if self.is_regex:
            if self.is_type(TreeValueType.BYTES):
                symbol = repr(self._value)
                symbol = symbol.replace(r"\\", "\\")
                return "r" + symbol
            elif self.is_type(TreeValueType.TRAILING_BITS_ONLY):
                return "r'" + str(self._value) + "'"

            if "'" not in str(self._value):
                return "r'" + str(self._value) + "'"
            if '"' not in str(self._value):
                return 'r"' + str(self._value) + '"'

            # Mixed quotes: encode single quotes
            symbol = str(self._value).replace("'", r"\x27")
            return "r'" + str(symbol) + "'"

        # Not a regex
        return repr(self._value)

    def __hash__(self) -> int:
        return hash((self._value, self._type))

    def __len__(self) -> int:
        return self.count_bytes()
