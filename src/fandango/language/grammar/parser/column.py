from typing import Optional

from fandango.language.grammar.parser.parse_state import ParseState
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.symbols.symbol import Symbol


class Column:
    def __init__(self, states: Optional[list[ParseState]] = None):
        self.states: list[ParseState] = states or []
        self.dot_map = dict[Symbol, list[ParseState]]()
        self.unique = set(self.states)
        for state in self.states:
            self.dot_map[state.nonterminal].append(state)

    def __iter__(self):
        yield from self.states

    def __len__(self):
        return len(self.states)

    def __getitem__(self, item):
        return self.states[item]

    def remove(self, state: ParseState):
        if state not in self.unique:
            return False
        self.unique.remove(state)
        self.states.remove(state)
        symbol = state.dot
        assert symbol is not None
        default_list: list[ParseState] = []
        self.dot_map.get(symbol, default_list).remove(state)
        return None

    def replace(self, old: ParseState, new: ParseState):
        self.unique.remove(old)
        self.unique.add(new)
        i_old = self.states.index(old)
        del self.states[i_old]
        self.states.insert(i_old, new)

        old_symbol = old.dot
        if old_symbol is not None:
            self.dot_map[old_symbol].remove(old)

        new_symbol = new.dot
        if new_symbol is not None:
            dot_list = self.dot_map.get(new_symbol, [])
            dot_list.append(new)
            self.dot_map[new_symbol] = dot_list

    def __contains__(self, item):
        return item in self.unique

    def find_dot(self, nt: NonTerminal):
        return self.dot_map.get(nt, [])

    def add(self, state: ParseState):
        if state not in self.unique:
            self.states.append(state)
            self.unique.add(state)
            symbol = state.dot
            if symbol is not None:
                state_list = self.dot_map.get(symbol, [])
                state_list.append(state)
                self.dot_map[symbol] = state_list
            return True
        return False

    def update(self, states: set[ParseState]):
        for state in states:
            self.add(state)

    def __repr__(self):
        return f"Column({self.states})"
