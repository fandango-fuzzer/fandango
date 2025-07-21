from fandango.language.symbol import Symbol, SymbolType


class Slice(Symbol):
    def __init__(self) -> None:
        super().__init__("", SymbolType.SLICE)

    def __hash__(self) -> int:
        return hash(self._type)
