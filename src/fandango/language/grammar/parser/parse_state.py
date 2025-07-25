from typing import Any, Optional

from fandango.language.tree import DerivationTree
from fandango.language.symbols import NonTerminal, Symbol


class ParseState:
    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: tuple[tuple[Symbol, frozenset[tuple[str, Any]]], ...],
        dot: int = 0,
        children: Optional[list[DerivationTree]] = None,
        is_incomplete: bool = False,
        incomplete_idx=0,
    ):
        self._nonterminal = nonterminal
        self._position = position
        self._symbols = symbols
        self._dot = dot
        self.children = children or []
        self.is_incomplete = is_incomplete
        self.incomplete_idx = incomplete_idx
        self._hash: Optional[int] = None

    @property
    def nonterminal(self):
        return self._nonterminal

    def append_child(self, child: DerivationTree):
        self.children.append(child)
        self._hash = None

    def extend_children(self, children: list[DerivationTree]):
        self.children.extend(children)
        self._hash = None

    @property
    def position(self):
        return self._position

    @property
    def symbols(self):
        return self._symbols

    @property
    def dot(self) -> Optional[Symbol]:
        return self.symbols[self._dot][0] if self._dot < len(self.symbols) else None

    @property
    def dot_params(self) -> Optional[frozenset[tuple[str, Any]]]:
        return self.symbols[self._dot][1] if self._dot < len(self.symbols) else None

    def finished(self):
        return self._dot >= len(self.symbols) and not self.is_incomplete

    def next_symbol_is_nonterminal(self):
        return (
            self._dot < len(self.symbols) and self.symbols[self._dot][0].is_non_terminal
        )

    def next_symbol_is_terminal(self):
        return self._dot < len(self.symbols) and self.symbols[self._dot][0].is_terminal

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(
                (
                    self.nonterminal,
                    self.position,
                    self.symbols,
                    self._dot,
                    tuple(self.children),
                )
            )
        return self._hash

    def __eq__(self, other):
        return (
            isinstance(other, ParseState)
            and self.nonterminal == other.nonterminal
            and self.position == other.position
            and self.symbols == other.symbols
            and self._dot == other._dot
        )

    def __repr__(self):
        return (
            f"({self.nonterminal.format_as_spec()} -> "
            + "".join(
                [
                    f"{'•' if i == self._dot else ''}{s[0].format_as_spec()!s}"
                    for i, s in enumerate(self.symbols)
                ]
            )
            + ("•" if self.finished() else "")
            + f", column {self.position}"
            + ")"
        )

    def next(self):
        next_state = self.copy()
        next_state._dot += 1
        return next_state

    def copy(self):
        return ParseState(
            self.nonterminal,
            self.position,
            self.symbols,
            self._dot,
            self.children[:],
            self.is_incomplete,
            self.incomplete_idx,
        )
