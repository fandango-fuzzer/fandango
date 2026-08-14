from typing import Any, Optional

from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree

ParserStateSymbolContent = tuple[Symbol, frozenset[tuple[str, Any]]]


class ParseState:
    _prev: "Optional[ParseState]"
    _added: list[DerivationTree]

    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: tuple[ParserStateSymbolContent, ...],
        dot: int = 0,
        children: Optional[list[DerivationTree]] = None,
        is_incomplete: bool = False,
        incomplete_idx: int = 0,
    ):
        self._nonterminal = nonterminal
        self._position = position
        self._symbols = symbols
        self._dot = dot
        self._prev = None
        self._added: list[DerivationTree] = children if children is not None else []
        self._children_cache: Optional[list[DerivationTree]] = None
        self.is_incomplete = is_incomplete
        self.incomplete_idx = incomplete_idx
        self._hash: Optional[int] = None

    @property
    def nonterminal(self) -> NonTerminal:
        return self._nonterminal

    @property
    def children(self) -> list[DerivationTree]:
        """The full child list, flattened from the shared chain on demand."""
        cached = self._children_cache
        if cached is not None:
            return cached
        chunks = []
        node = self
        while node is not None:
            if node._added:
                chunks.append(node._added)
            node = node._prev
        children: list[DerivationTree] = []
        for chunk in reversed(chunks):
            children.extend(chunk)
        self._children_cache = children
        return children

    def append_child(self, child: DerivationTree) -> None:
        self._added.append(child)
        self._children_cache = None

    def extend_children(self, children: list[DerivationTree]) -> None:
        self._added.extend(children)
        self._children_cache = None

    def replace_last_child(self, child: DerivationTree) -> None:
        if self._added:
            self._added[-1] = child
        else:
            prev = self._prev
            assert prev is not None and len(prev._added) == 1, (
                "replace_last_child expects the previous state to have "
                "contributed exactly one (partial terminal) child"
            )
            self._prev = prev._prev
            self._added = [child]
        self._children_cache = None

    @property
    def position(self) -> int:
        return self._position

    @property
    def symbols(self) -> tuple[ParserStateSymbolContent, ...]:
        return self._symbols

    @property
    def dot(self) -> Optional[Symbol]:
        return self.symbols[self._dot][0] if self._dot < len(self.symbols) else None

    @property
    def dot_params(self) -> Optional[frozenset[tuple[str, Any]]]:
        return self.symbols[self._dot][1] if self._dot < len(self.symbols) else None

    def finished(self) -> bool:
        return self._dot >= len(self.symbols) and not self.is_incomplete

    def next_symbol_is_nonterminal(self) -> bool:
        return (
            self._dot < len(self.symbols) and self.symbols[self._dot][0].is_non_terminal
        )

    def next_symbol_is_terminal(self) -> bool:
        return self._dot < len(self.symbols) and self.symbols[self._dot][0].is_terminal

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(
                (
                    self.nonterminal,
                    self.position,
                    self._dot,
                    len(self.symbols),
                    self.symbols[0][0] if self.symbols else None,
                )
            )
        return self._hash

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ParseState)
            and self.nonterminal == other.nonterminal
            and self.position == other.position
            and self.symbols == other.symbols
            and self._dot == other._dot
        )

    def __repr__(self) -> str:
        return (
            f"({self.nonterminal.format_as_spec()} -> "
            + "".join(
                [
                    f"{'•' if i == self._dot else ''}{s[0]!s}"
                    for i, s in enumerate(self.symbols)
                ]
            )
            + ("•" if self.finished() else "")
            + f", column {self.position}"
            + ")"
        )

    def next(self) -> "ParseState":
        next_state = self.copy()
        next_state._dot += 1
        return next_state

    def copy(self) -> "ParseState":
        # Share this state's children rather than copying them: the copy
        # contributes nothing of its own and chains back to us.
        copied = ParseState(
            self.nonterminal,
            self.position,
            self.symbols,
            self._dot,
            None,
            self.is_incomplete,
            self.incomplete_idx,
        )
        copied._prev = self
        return copied
