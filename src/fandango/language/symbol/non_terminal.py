from fandango.language.symbol import Symbol, SymbolType


class NonTerminal(Symbol):
    def __init__(self, symbol: str) -> None:
        super().__init__(symbol, SymbolType.NON_TERMINAL)

    def name(self) -> str:
        """
        Return the name of the non-terminal symbol.
        """
        assert self.is_type(str)
        return str(self._value)

    def __hash__(self) -> int:
        return hash((self._value, self._type))

    def format_as_spec(self) -> str:
        return self.name()
