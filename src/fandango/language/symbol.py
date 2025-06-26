import abc
import enum
import re
from io import UnsupportedOperation

import regex


class SymbolType(enum.Enum):
    TERMINAL = "Terminal"
    NON_TERMINAL = "NonTerminal"
    SLICE = "Slice"


class Symbol(abc.ABC):
    def __init__(self, symbol: str | bytes | int, type_: SymbolType):
        self.symbol = symbol
        self.type = type_
        self._is_regex = False

    def check(self, word: str, incomplete=False) -> tuple[bool, int]:
        """Return (True, # of characters matched by `word`), or (False, 0)"""
        return False, 0

    def check_all(self, word: str) -> bool:
        """Return True if `word` matches"""
        return False

    @property
    def is_terminal(self):
        return self.type == SymbolType.TERMINAL

    @property
    def is_non_terminal(self):
        return self.type == SymbolType.NON_TERMINAL

    @property
    def is_slice(self):
        return self.type == SymbolType.SLICE

    @property
    def is_regex(self):
        try:
            return self._is_regex
        except AttributeError:
            return False  # for cached grammars

    @abc.abstractmethod
    def __hash__(self):
        return NotImplemented

    def _repr(self):
        return str(self.symbol)

    def __str__(self):
        return str(self.symbol)

    def __repr__(self):
        return "Symbol(" + repr(self.symbol) + ")"


class NonTerminal(Symbol):
    def __init__(self, symbol: str):
        super().__init__(symbol, SymbolType.NON_TERMINAL)

    def __eq__(self, other):
        return isinstance(other, NonTerminal) and self.symbol == other.symbol

    def __lt__(self, other):
        if (
            isinstance(other, NonTerminal)
            and isinstance(self.symbol, str)
            and isinstance(other.symbol, str)
        ):
            return self.symbol < other.symbol
        raise TypeError(
            f"Cannot compare NonTerminal with {type(other).__name__} or symbols are not bytes"
        )

    def __hash__(self):
        return hash((self.symbol, self.type))

    def __repr__(self):
        return "NonTerminal(" + repr(self.symbol) + ")"


class Terminal(Symbol):
    def __init__(self, symbol: str | bytes | int):
        super().__init__(symbol, SymbolType.TERMINAL)

    def __len__(self):
        if isinstance(self.symbol, int):
            return 1
        return len(self.symbol)

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
        if isinstance(self.symbol, int) or isinstance(word, int):
            return self.check_all(word), 1

        # LOGGER.debug(f"Checking {self.symbol!r} against {word!r}")
        symbol = self.symbol

        if isinstance(symbol, bytes) and isinstance(word, str):
            assert isinstance(symbol, bytes)
            symbol = symbol.decode("iso-8859-1")
        if isinstance(symbol, str) and isinstance(word, bytes):
            assert isinstance(word, bytes)
            word = word.decode("iso-8859-1")

        assert (isinstance(symbol, str) and isinstance(word, str)) or (
            isinstance(symbol, bytes) and isinstance(word, bytes)
        )

        if self.is_regex:
            if not incomplete:
                match = re.match(symbol, word)
                if match:
                    # LOGGER.debug(f"It's a match: {match.group(0)!r}")
                    return True, len(match.group(0))
            else:
                compiled = regex.compile("")
                match = compiled.match(word, partial=True)
                return match is not None and (
                    match.partial or match.end() == len(word)
                ), len(match.group(0))
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
        return word == self.symbol

    def _repr(self):
        if self.is_regex:
            if isinstance(self.symbol, bytes):
                symbol = repr(self.symbol)
                symbol = symbol.replace(r"\\", "\\")
                return "r" + symbol
            elif isinstance(self.symbol, int):
                return "r'" + str(self.symbol) + "'"

            if "'" not in self.symbol:
                return "r'" + str(self.symbol) + "'"
            if '"' not in self.symbol:
                return 'r"' + str(self.symbol) + '"'

            # Mixed quotes: encode single quotes
            symbol = self.symbol.replace("'", r"\x27")
            return "r'" + str(symbol) + "'"

        # Not a regex
        return repr(self.symbol)

    def __eq__(self, other):
        return isinstance(other, Terminal) and self.symbol == other.symbol

    def __hash__(self):
        return hash((self.symbol, self.type))

    def __repr__(self):
        return "Terminal(" + self._repr() + ")"

    def __str__(self):
        return self._repr()


class Slice(Symbol):
    def __init__(self):
        super().__init__("", SymbolType.SLICE)

    def __hash__(self):
        return hash(self.type)
