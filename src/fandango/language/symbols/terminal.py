from io import UnsupportedOperation
import re
from types import NoneType

import regex

from fandango.errors import FandangoValueError
from fandango.language.symbols import Symbol, SymbolType
from fandango.language.tree_value import TreeValue, TreeValueType


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

        return eval(symbol)  # also handles bits "0" and "1"

    @staticmethod
    def from_symbol(symbol: str) -> "Terminal":
        t = Terminal(Terminal.clean(symbol))
        t._is_regex = "r" in Terminal.string_prefix(symbol)
        return t

    @staticmethod
    def from_number(number: str) -> "Terminal":
        return Terminal(Terminal.clean(number))

    def check(self, word: str | bytes | int, incomplete=False) -> tuple[bool, int]:
        """Return (True, # characters matched by `word`), or (False, 0)"""

        if self._value.is_type(TreeValueType.TRAILING_BITS_ONLY) or isinstance(
            word, int
        ):
            return self.check_all(word), 1
        check_word: str | bytes = word

        symbol: str | bytes
        if self._value.is_type(TreeValueType.BYTES) and isinstance(check_word, bytes):
            symbol = self._value.to_bytes()
        else:
            symbol = self._value.to_string()
            check_word = (
                check_word
                if isinstance(check_word, str)
                else check_word.decode("latin-1")
            )

        if self.is_regex:
            if not incomplete:
                match = re.match(symbol, check_word)  # type: ignore [arg-type] # re actually does accept bytes
                if match:
                    # LOGGER.debug(f"It's a match: {match.group(0)!r}")
                    return True, len(match.group(0))
            else:
                compiled = regex.compile(symbol)
                match = compiled.match(check_word, partial=True)
                if match is not None and (
                    match.partial or match.end() == len(check_word)
                ):
                    return True, len(match.group(0))
                match = compiled.fullmatch(check_word, partial=True)
                if match is not None and (
                    match.partial or match.end() == len(check_word)
                ):
                    return True, len(match.group(0))
                return False, 0

        else:
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

        # LOGGER.debug(f"No match")
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

    def __repr__(self) -> str:
        return "Terminal(" + self.format_as_spec() + ")"

    def __len__(self) -> int:
        return self.count_bytes()
