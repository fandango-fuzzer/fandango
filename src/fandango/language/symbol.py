import abc
import enum
import re


class SymbolType(enum.Enum):
    TERMINAL = "Terminal"
    NON_TERMINAL = "NonTerminal"
    IMPLICIT = "Implicit"


class Symbol(abc.ABC):
    def __init__(self, symbol: str | bytes, type_: SymbolType):
        self.symbol = symbol
        self.type = type_
        self._is_regex = False

    def check(self, word: str) -> bool:
        return False

    def check_all(self, word: str) -> bool:
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

    def check(self, word: str | int) -> bool:
        if isinstance(self.symbol, int) or isinstance(word, int):
            return self.check_all(word)

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
            return re.match(symbol, word) is not None
        else:
            return word.startswith(symbol)

    def check_all(self, word: str | int) -> bool:
        return word == self.symbol

    def __repr__(self):
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
