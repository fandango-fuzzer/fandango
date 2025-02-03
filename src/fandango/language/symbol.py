import abc
import enum
import re
from fandango.logger import LOGGER


class SymbolType(enum.Enum):
    TERMINAL = "Terminal"
    NON_TERMINAL = "NonTerminal"
    IMPLICIT = "Implicit"


class Symbol(abc.ABC):
    def __init__(self, symbol: str | bytes, type_: SymbolType):
        self.symbol = symbol
        self.type = type_
        self._is_regex = False

    def check(self, word: str) -> tuple[bool, int]:
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
    def is_implicit(self):
        return self.type == SymbolType.IMPLICIT

    @property
    def is_regex(self):
        try:
            return self._is_regex
        except AttributeError:
            return False  # for cached grammars

    @abc.abstractmethod
    def __hash__(self):
        return NotImplemented


class NonTerminal(Symbol):
    def __init__(self, symbol: str):
        super().__init__(symbol, SymbolType.NON_TERMINAL)

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return isinstance(other, NonTerminal) and self.symbol == other.symbol

    def __hash__(self):
        return hash((self.symbol, self.type))


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
        # Not sure whether any of these are necessary, as we eval() anyway
        if len(symbol) >= 2:
            if symbol[0] == symbol[-1] == "'" or symbol[0] == symbol[-1] == '"':
                return eval(symbol)
            elif len(symbol) >= 3:
                if symbol[0] == "b" and (
                    symbol[1] == symbol[-1] == "'" or symbol[1] == symbol[-1] == '"'
                ):
                    return eval(symbol)
        return eval(symbol)  # also handles bits "0" and "1"

    @staticmethod
    def from_symbol(symbol: str) -> "Terminal":
        t = Terminal(Terminal.clean(symbol))
        t._is_regex = "r" in Terminal.string_prefix(symbol)
        return t

    @staticmethod
    def from_number(number: str) -> "Terminal":
        return Terminal(Terminal.clean(number))

    def check(self, word: str | int) -> tuple[bool, int]:
        """Return (True, # characters matched by `word`), or (False, 0)"""
        if isinstance(self.symbol, int) or isinstance(word, int):
            return self.check_all(word), 1

        # LOGGER.debug(f"Checking {self.symbol!r} against {word!r}")
        symbol = self.symbol

        if isinstance(self.symbol, bytes) and isinstance(word, str):
            assert isinstance(symbol, bytes)
            symbol = symbol.decode("iso-8859-1")
        if isinstance(self.symbol, str) and isinstance(word, bytes):
            assert isinstance(word, bytes)
            word = word.decode("iso-8859-1")

        assert isinstance(symbol, str)
        assert isinstance(word, str)

        if self.is_regex:
            match = re.match(symbol, word)
            if match:
                # LOGGER.debug(f"It's a match: {match.group(0)!r}")
                return True, len(match.group(0))
        else:
            if word.startswith(symbol):
                # LOGGER.debug(f"It's a match: {symbol!r}")
                return True, len(symbol)

        # LOGGER.debug(f"No match")
        return False, 0


    def check_all(self, word: str | int) -> bool:
        return word == self.symbol

    def __repr__(self):
        if self.is_regex:
            if isinstance(self.symbol, bytes):
                symbol = repr(self.symbol)
                symbol = symbol.replace(r'\\', '\\')
                return "r" + symbol

            if "'" not in self.symbol:
                return "r'" + str(self.symbol) + "'"
            if '"' not in self.symbol:
                return 'r"' + str(self.symbol) + '"'

            # Mixed quotes: escape single quotes
            symbol = self.symbol.replace("'", r"\'")
            return "r'" + str(symbol) + "'"

        # Not a regex
        return repr(self.symbol)

    def __eq__(self, other):
        return isinstance(other, Terminal) and self.symbol == other.symbol

    def __str__(self):
        return self.symbol

    def __hash__(self):
        return hash((self.symbol, self.type))


class Implicit(Symbol):
    def __init__(self, symbol: str):
        super().__init__(symbol, SymbolType.IMPLICIT)

    def __hash__(self):
        return hash((self.symbol, self.type))

    def __eq__(self, other):
        return isinstance(other, Implicit) and self.symbol == other.symbol
