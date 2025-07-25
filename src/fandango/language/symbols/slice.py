from fandango.language.symbols import Symbol, SymbolType
from fandango.logger import LOGGER


class Slice(Symbol):
    def __init__(self) -> None:
        super().__init__("", SymbolType.SLICE)

    def __hash__(self) -> int:
        return hash(self._type)

    def format_as_spec(self) -> str:
        LOGGER.warning(
            "Slice.format_as_spec() called. If this does not behave as expected, please report this as a bug."
        )
        return str(self._value)
