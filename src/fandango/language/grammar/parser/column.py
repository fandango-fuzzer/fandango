from collections.abc import Iterator
from typing import Optional

from fandango.language.grammar.parser.parse_state import LeoEntry, ParseState
from fandango.language.symbols.symbol import Symbol


class Column:
    def __init__(self) -> None:
        self.states: list[ParseState] = []
        self.waiting = dict[Symbol, list[ParseState]]()
        self.unique = dict[ParseState, ParseState]()
        # Used for early deduplication in predict
        self.predicted = set[Symbol]()
        self.leo: dict[Symbol, Optional[LeoEntry]] = {}

    def __iter__(self) -> Iterator[ParseState]:
        yield from self.states

    def __len__(self) -> int:
        return len(self.states)

    def __getitem__(self, item: int) -> ParseState:
        return self.states[item]

    def replace(self, old: ParseState, new: ParseState) -> None:
        del self.unique[old]
        self.unique[new] = new
        self.states[self.states.index(old)] = new

        old_symbol = old.next_symbol
        if old_symbol is not None:
            self.waiting[old_symbol].remove(old)

        new_symbol = new.next_symbol
        if new_symbol is not None:
            waiters = self.waiting.get(new_symbol, [])
            waiters.append(new)
            self.waiting[new_symbol] = waiters

    def __contains__(self, item: ParseState) -> bool:
        return item in self.unique

    def waiting_for(self, symbol: Optional[Symbol]) -> list[ParseState]:
        if symbol is None:
            return []
        return self.waiting.get(symbol, [])

    def add(self, state: ParseState) -> bool:
        existing = self.unique.get(state)
        if existing is None:
            self.states.append(state)
            self.unique[state] = state
            symbol = state.next_symbol
            if symbol is not None:
                waiters = self.waiting.get(symbol, [])
                waiters.append(state)
                self.waiting[symbol] = waiters
            return True
        if existing is not state and state.edges:
            # Same item, different derivation: keep it as an alternative.
            existing.edges.extend(state.edges)
        return False

    def update(self, states: set[ParseState]) -> None:
        for state in states:
            self.add(state)

    def __repr__(self) -> str:
        return f"Column({self.states})"
