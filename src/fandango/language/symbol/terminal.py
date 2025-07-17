from io import UnsupportedOperation
import re
from types import NoneType

import regex

from fandango.language.symbol import Symbol, SymbolType
from fandango.language.tree_value import TreeValue


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

    def check(self, word: str | int, incomplete=False) -> tuple[bool, int]:
        """Return (True, # characters matched by `word`), or (False, 0)"""

        if self._value.is_type(NoneType) or isinstance(word, int):
            return self.check_all(word), 1

        if self._value.is_type(bytes) and isinstance(word, bytes):
            symbol = self._value.to_bytes()
        else:
            symbol = self._value.to_string()
            word = word if isinstance(word, str) else word.decode("latin-1")

        if self.is_regex:
            if not incomplete:
                match = re.match(symbol, word)
                if match:
                    # LOGGER.debug(f"It's a match: {match.group(0)!r}")
                    return True, len(match.group(0))
            else:
                compiled = regex.compile(symbol)
                match = compiled.match(word, partial=True)
                if match is not None and (match.partial or match.end() == len(word)):
                    return True, len(match.group(0))
                else:
                    return False, 0

        else:
            if not incomplete:
                if word.startswith(symbol):
                    # LOGGER.debug(f"It's a match: {symbol!r}")
                    return True, len(symbol)
            else:
                if symbol.startswith(word):
                    return True, len(word)

        # LOGGER.debug(f"No match")
        return False, 0

    def check_all(self, word: str | int) -> bool:
        if isinstance(word, str):
            if self._value.is_type(NoneType):
                # cannot reasonably compare strings to partial bytes
                return False
            else:
                return str(self._value) == word
        else:
            return int(self._value) == word

    def format_as_spec(self) -> str:
        if self.is_regex:
            if self.is_type(bytes):
                symbol = repr(self._value)
                symbol = symbol.replace(r"\\", "\\")
                return "r" + symbol
            elif self.is_type(NoneType):
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
