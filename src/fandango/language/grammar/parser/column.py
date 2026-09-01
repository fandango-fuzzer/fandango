from collections.abc import Iterator
from typing import Optional

from fandango.language.grammar.parser.parse_state import LeoEntry, ParseState
from fandango.language.symbols.symbol import Symbol


class Column:
    def __init__(self) -> None:
        self.states: list[ParseState] = []
        self.dot_map = dict[Symbol, list[ParseState]]()
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

        old_symbol = old.dot
        if old_symbol is not None:
            self.dot_map[old_symbol].remove(old)

        new_symbol = new.dot
        if new_symbol is not None:
            dot_list = self.dot_map.get(new_symbol, [])
            dot_list.append(new)
            self.dot_map[new_symbol] = dot_list

    def __contains__(self, item: ParseState) -> bool:
        return item in self.unique

    def find_dot(self, nt: Optional[Symbol]) -> list[ParseState]:
        if nt is None:
            return []
        return self.dot_map.get(nt, [])

    def add(self, state: ParseState) -> bool:
        existing = self.unique.get(state)
        if existing is None:
            self.states.append(state)
            self.unique[state] = state
            symbol = state.dot
            if symbol is not None:
                state_list = self.dot_map.get(symbol, [])
                state_list.append(state)
                self.dot_map[symbol] = state_list
            return True
        if existing is not state and state.edges:
            # Same item, different derivation: keep it as an alternative.
            # Predicted states carry no edges, so this is a no-op for them.
            existing.edges.extend(state.edges)
        return False

    def update(self, states: set[ParseState]) -> None:
        for state in states:
            self.add(state)

    def __repr__(self) -> str:
        return f"Column({self.states})"
