from fandango.language.symbols.symbol import Symbol, SymbolType


class NonTerminal(Symbol):
    def __init__(self, symbol: str) -> None:
        assert isinstance(symbol, str)
        super().__init__(symbol, SymbolType.NON_TERMINAL)
        self._hash = hash((self._value, self._type))

    def name(self) -> str:
        """
        Return the name of the non-terminal symbol.
        """
        return str(self._value)

    def __hash__(self) -> int:
        return self._hash

    def format_as_spec(self) -> str:
        return self.name()
