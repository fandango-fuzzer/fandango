import abc
import enum
from typing import Any

from fandango.language.tree_value import TreeValue, TreeValueType


class SymbolType(enum.Enum):
    TERMINAL = "Terminal"
    NON_TERMINAL = "NonTerminal"
    SLICE = "Slice"
    TREE_NODE = "TreeNode"


class Symbol(abc.ABC):
    def __init__(self, value: str | bytes | int | TreeValue, type_: SymbolType):
        self._value = value if isinstance(value, TreeValue) else TreeValue(value)
        self._type = type_
        self._is_regex = False

    def check(self, word: str | int | bytes, incomplete=False) -> tuple[bool, int]:
        """Return (True, # of characters matched by `word`), or (False, 0)"""
        return False, 0

    def check_all(self, word: str | int | bytes) -> bool:
        """Return True if `word` matches"""
        return False

    @property
    def is_terminal(self) -> bool:
        return self._type == SymbolType.TERMINAL

    @property
    def is_non_terminal(self) -> bool:
        return self._type == SymbolType.NON_TERMINAL

    @property
    def is_slice(self) -> bool:
        return self._type == SymbolType.SLICE

    @property
    def is_regex(self) -> bool:
        return getattr(self, "_is_regex", False)

    def is_type(self, type_: TreeValueType) -> bool:
        return self._value.is_type(type_)

    def value(self) -> TreeValue:
        return self._value

    def __eq__(self, other: Any) -> bool:
        return type(self) is type(other) and self._value == other._value

    @abc.abstractmethod
    def __hash__(self) -> int:
        return NotImplemented

    def _repr(self) -> str:
        return str(self.value())

    def __str__(self) -> str:
        raise KeyError(f"str() not implemented for {type(self)}, use specific function")

    def __repr__(self) -> str:
        raise KeyError(
            f"repr() not implemented for {type(self)}, use specific function"
        )
