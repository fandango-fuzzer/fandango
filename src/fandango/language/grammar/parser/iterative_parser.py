from collections.abc import Generator
from copy import deepcopy
from typing import Any, Optional

from fandango.errors import FandangoValueError
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.parser.column import Column
from fandango.language.grammar.parser.forest import ForestBuilder
from fandango.language.grammar.parser.grammar_compiler import GrammarCompiler
from fandango.language.grammar.parser.parse_state import (
    LeoEntry,
    LeoNest,
    ParserStateSymbolContent,
    ParseState,
)
from fandango.language.grammar.parser.parser_tree import ParserDerivationTree
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.symbols.symbol import Symbol
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import TreeValue, TreeValueType

IterativeParserVisitorReturnType = list[list[ParserStateSymbolContent]]


class IterativeParser:
    def __init__(
        self,
        grammar_rules: dict[NonTerminal, Node],
    ):
        self.implicit_start = NonTerminal("<*start*>")
        self._compiler = GrammarCompiler(grammar_rules)
        self.grammar_rules = self._compiler.grammar_rules
        self._rules = self._compiler._rules
        self._implicit_rules = self._compiler._implicit_rules
        self._context_rules = self._compiler._context_rules
        self._tmp_rules = self._compiler._tmp_rules
        self._incomplete: set[DerivationTree] = set()
        self._max_position = -1
        self._table_idx = 0
        self._table: list[Column] = []
        self._parsing_mode = ParsingMode.COMPLETE
        self._start: Optional[NonTerminal] = None
        self._first_consume = True
        self._hookin_parent: Optional[DerivationTree] = None
        self._columns_per_byte = 8
        self._forest = ForestBuilder(self._rules, self._compiler._nodes)

    def can_continue(self) -> bool:
        if len(self._table) <= 1:
            # Assume that an unstarted parse can continue
            return True
        table: list[Column] = list(self._table)
        table[self._table_idx] = deepcopy(table[self._table_idx])

        for state in table[-1]:
            if state.finished():
                self.complete(state, table, self._table_idx)

        return any(
            map(
                lambda state: state.is_incomplete or not state.finished(),
                table[self._table_idx],
            )
        )

    def predict(
        self,
        state: ParseState,
        table: list[Column],
        k: int,
        hookin_parent: Optional[DerivationTree] = None,
    ) -> None:
        symbol = state.dot
        assert symbol is not None
        assert isinstance(symbol, NonTerminal)
        predicted = table[k].predicted
        if symbol in predicted:
            # We dont add update the table, if we've already predicted the same symbol in the same column.
            # We make an exception for context rules, as they depend on semantics.
            if symbol not in self._context_rules:
                return
        else:
            predicted.add(symbol)
        if state.dot in self._rules:
            table[k].update(
                {ParseState(symbol, k, rule, 0) for rule in self._rules[symbol]}  # type: ignore[arg-type] # TODO:  this is a bug!
            )
        elif state.dot in self._implicit_rules:
            table[k].update(
                {
                    ParseState(symbol, k, rule, 0)  # type: ignore[arg-type] # TODO:  this is a bug!
                    for rule in self._implicit_rules[symbol]
                }
            )
        elif state.dot in self._tmp_rules:
            table[k].update(
                {ParseState(symbol, k, rule, 0) for rule in self._tmp_rules[symbol]}  # type: ignore[arg-type] # TODO:  this is a bug!
            )
        elif state.dot in self._context_rules:
            node, nt = self._context_rules[symbol]
            self.predict_ctx_rule(state, table, k, node, nt, hookin_parent)

    def current_tree(self) -> Optional[DerivationTree]:
        if len(self._table[self._table_idx]) == 0:
            return None
        for col in self._table[::-1]:
            if len(col) == 0:
                continue
            return self.construct_incomplete_tree(col[-1], self._table)
        return None

    def construct_incomplete_tree(
        self, state: ParseState, table: list[Column]
    ) -> DerivationTree:
        current_tree = ParserDerivationTree(
            state.nonterminal, self._forest.children_of(state)
        )
        current_state = state
        found_next_state = True
        while found_next_state:
            found_next_state = False
            for table_state in table[current_state.position].states:
                if table_state.dot == current_state.nonterminal:
                    current_state = table_state
                    found_next_state = True
                    break
            assert isinstance(current_tree.symbol, NonTerminal)
            if current_tree.symbol.name().startswith("<*"):
                current_tree = ParserDerivationTree(
                    current_state.nonterminal,
                    [
                        *self._forest.children_of(current_state),
                        *current_tree.children,
                    ],
                    **dict(current_state.dot_params or {}),
                )
            else:
                current_tree = ParserDerivationTree(
                    current_state.nonterminal,
                    [*self._forest.children_of(current_state), current_tree],
                    **dict(current_state.dot_params or {}),
                )

        return current_tree.children[0]

    def predict_ctx_rule(
        self,
        state: ParseState,
        table: list[Column],
        k: int,
        node: Node,
        nt_rule: ParserStateSymbolContent,
        hookin_parent: Optional[DerivationTree] = None,
    ) -> None:
        if not isinstance(node, Repetition):
            raise FandangoValueError(f"Node {node} needs to be a Repetition")

        tree = self.construct_incomplete_tree(state, table)
        collapsed_tree = self.collapse(tree)
        assert collapsed_tree is not None
        tree = collapsed_tree
        if hookin_parent is not None:
            hookin_parent.set_children(hookin_parent.children + [tree])
        try:
            context_nt = self._compiler.compile_bounded_repetition(
                node, nt_rule, tree if hookin_parent is None else hookin_parent
            )
        except (ValueError, FandangoValueError):
            return
        finally:
            if hookin_parent is not None:
                hookin_parent.set_children(hookin_parent.children[:-1])
        new_symbols: list[tuple[Symbol, frozenset[tuple[str, Any]]]] = []
        placed = False
        for symbol, dot_params in state.symbols:
            if symbol == state.dot and not placed:
                new_symbols.append(context_nt)
                placed = True
            else:
                new_symbols.append((symbol, dot_params))
        new_state = ParseState(
            state.nonterminal,
            state.position,
            tuple(new_symbols),
            state._dot,
            self._forest.children_of(state),
            state.incomplete_idx,
        )
        if state in table[k]:
            table[k].replace(state, new_state)
        self.predict(new_state, table, k)

    def scan_bit(
        self,
        state: ParseState,
        word: str | bytes,
        table: list[Column],
        k: int,
        w: int,
        bit_count: int,
    ) -> bool:
        """
        Scan a bit from the input `word`.
        `table` is the parse table (may be modified by this function).
        `table[k]` is the current column.
        `word[w]` is the current byte.
        `bit_count` is the current bit position (7-0).
        Return True if a bit was matched, False otherwise.
        """
        assert state.dot is not None
        assert state.dot.is_type(TreeValueType.TRAILING_BITS_ONLY)
        assert 0 <= bit_count <= 7

        if w >= len(word):
            return False

        # Get the highest bit. If `word` is bytes, word[w] is an integer.
        byte = ord(word[w]) if isinstance(word, str) else word[w]
        bit = (byte >> bit_count) & 1

        # LOGGER.debug(f"Checking {state.dot} against {bit}")
        match, match_length = state.dot.check(bit)
        if not match or match_length == 0:
            # LOGGER.debug(f"No match")
            return False

        # Found a match
        # LOGGER.debug(f"Found bit {bit}")
        next_state = state.next()
        tree = ParserDerivationTree(Terminal(bit))
        next_state.set_edge(state, tree)
        # LOGGER.debug(f"Added tree {tree.to_string()!r} to state {next_state!r}")
        # Insert a new table entry with next state
        # This is necessary, as our initial table holds one entry
        # per input byte, yet needs to be expanded to hold the bits, too.

        # Add a new table row if the bit isn't already represented
        # by a row in the parsing table
        # if len(table) <= k + 1:
        #    table.insert(k + 1, Column())
        table[k + 1].add(next_state)

        # Save the maximum position reached, so we can report errors
        self._max_position = max(self._max_position, w)

        return True

    def scan_bytes(
        self,
        state: ParseState,
        word: str | bytes,
        table: list[Column],
        k: int,
        w: int,
    ) -> bool:
        """
        Scan a byte from the input `word`.
        `state` is the current parse state.
        `table` is the parse table.
        `table[k]` is the current column.
        `word[w]` is the current byte.
        Return True if a byte was matched, False otherwise.
        """

        assert state.dot is not None
        assert not (
            state.dot.is_type(TreeValueType.TRAILING_BITS_ONLY)
            or state.dot.is_type(TreeValueType.EMPTY)
        )
        assert not state.dot.is_regex

        # LOGGER.debug(f"Checking byte(s) {state.dot!r} at position {w:#06x} ({w}) {word[w:]!r}")

        check_word = word[w:]
        if state.is_incomplete:
            prev_terminal = state.last_filler()
            assert isinstance(prev_terminal, DerivationTree)
            prev_val = prev_terminal.symbol.value()
            prev_val_raw: str | bytes
            if prev_val.is_type(TreeValueType.BYTES):
                prev_val_raw = bytes(prev_val)
                check_word = bytes(
                    TreeValue(prev_val_raw).append(TreeValue(check_word))
                )
            else:
                prev_val_raw = str(prev_val)
                check_word = str(TreeValue(prev_val_raw).append(TreeValue(check_word)))
        if state.dot.is_type(TreeValueType.BYTES):
            dot_len = len(bytes(state.dot.value()))
        else:
            dot_len = len(str(state.dot.value()))

        match, match_length = state.dot.check(check_word)
        table_idx_multiplier = self._columns_per_byte

        if not match:
            if (w + dot_len - state.incomplete_idx) < len(word):
                return False
            match, match_length = state.dot.check(check_word, incomplete=True)
            if not match or match_length == 0:
                return False

            next_state = state.copy()
            next_state.incomplete_idx = match_length
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            next_state.set_edge(
                state.predecessor() if state.is_incomplete else state, tree
            )
        else:
            next_state = state.next()
            next_state.incomplete_idx = 0
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            next_state.set_edge(
                state.predecessor() if state.is_incomplete else state, tree
            )
        table[k + ((match_length - state.incomplete_idx) * table_idx_multiplier)].add(
            next_state
        )
        # LOGGER.debug(f"Next state: {next_state} at column {k + match_length}")
        self._max_position = max(self._max_position, w + match_length)

        return True

    def scan_regex(
        self,
        state: ParseState,
        word: str | bytes,
        table: list[Column],
        k: int,
        w: int,
    ) -> bool:
        """
        Scan a byte from the input `word`.
        `state` is the current parse state.
        `table` is the parse table.
        `table[k]` is the current column.
        `word[w]` is the current byte.
        Return (True, #bytes) if bytes were matched, (False, 0) otherwise.
        """

        assert state.dot is not None
        assert not (
            state.dot.is_type(TreeValueType.TRAILING_BITS_ONLY)
            or state.dot.is_type(TreeValueType.EMPTY)
        )
        assert state.dot.is_regex

        check_word = word[w:]
        prev_match_length = 0
        if state.is_incomplete:
            prev_terminal = state.last_filler()
            assert isinstance(prev_terminal, DerivationTree)
            prev_val = prev_terminal.symbol.value()
            prev_val_raw: str | bytes
            if prev_val.is_type(TreeValueType.BYTES):
                prev_val_raw = bytes(prev_val)
                check_word = bytes(
                    TreeValue(prev_val_raw).append(TreeValue(check_word))
                )
            else:
                prev_val_raw = str(prev_val)
                check_word = str(TreeValue(prev_val_raw).append(TreeValue(check_word)))
            prev_match_length = len(prev_val_raw)

        table_idx_multiplier = self._columns_per_byte
        match, match_length = state.dot.check(check_word)
        table_offset = match_length
        if match and match_length <= prev_match_length:
            match = False
            match_length = 0
        incomplete_match, incomplete_match_length = state.dot.check(
            check_word, incomplete=True
        )
        incomplete_table_offset = incomplete_match_length
        if not match:
            if not incomplete_match or (incomplete_match_length + w) < len(word):
                return False

        if match:
            next_state = state.next()
            next_state.incomplete_idx = 0
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            # Growing a partial match replaces the previous partial
            # terminal rather than adding a child, so step back over it.
            next_state.set_edge(
                state.predecessor() if state.is_incomplete else state, tree
            )
            table[
                k + ((table_offset - state.incomplete_idx) * table_idx_multiplier)
            ].add(next_state)
        if incomplete_match:
            next_state = state.copy()
            next_state.incomplete_idx = incomplete_match_length
            tree = ParserDerivationTree(Terminal(check_word[:incomplete_match_length]))
            next_state.set_edge(
                state.predecessor() if state.is_incomplete else state, tree
            )
            table[
                k
                + (
                    (incomplete_table_offset - state.incomplete_idx)
                    * table_idx_multiplier
                )
            ].add(next_state)

        self._max_position = max(self._max_position, w + match_length)
        return True

    def _leo_entry(
        self, table: list[Column], index: int, symbol: Symbol
    ) -> Optional[LeoEntry]:
        """
        When only one way to reduce upwards from `symbol` exists, returns the
        top of that chain, else None.
        """
        pending: list[tuple[int, Symbol, ParseState]] = []
        entry: Optional[LeoEntry] = None
        current_index, current_symbol = index, symbol
        while True:
            column = table[current_index]
            if current_symbol in column.leo:
                entry = column.leo[current_symbol]
                break
            waiters = column.dot_map.get(current_symbol)
            # Ensure that we don't get a collision, from multiple states pointing to the same symbol.
            if waiters is None or len(waiters) != 1:
                column.leo[current_symbol] = None
                break
            waiter = waiters[0]
            # Only expand leo path if we are at the last symbol of the rule.
            if waiter._dot != len(waiter.symbols) - 1 or waiter.is_incomplete:
                column.leo[current_symbol] = None
                break
            pending.append((current_index, current_symbol, waiter))
            current_index, current_symbol = waiter.position, waiter.nonterminal
            if current_index > index:
                break

        for cached_index, cached_symbol, waiter in reversed(pending):
            entry = LeoEntry(waiter) if entry is None else entry.push(waiter)
            table[cached_index].leo[cached_symbol] = entry
        return entry

    def complete(
        self,
        state: ParseState,
        table: list[Column],
        k: int,
    ) -> None:
        column = table[k]
        if state.position < k:
            entry = self._leo_entry(table, state.position, state.nonterminal)
            if entry is not None:
                top = entry.top
                advanced = top.next()
                advanced.add_edge(
                    top, LeoNest(entry.chain, state, top.dot_params), top.dot_params
                )
                column.add(advanced)
                return
        for s in table[state.position].find_dot(state.nonterminal):
            advanced = s.next()
            advanced.add_edge(s, state, s.dot_params)
            column.add(advanced)

    def new_parse(
        self,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        starter_bit: int = -1,
    ) -> None:
        if isinstance(start, str):
            start = NonTerminal(start)
        self._start = start
        self._columns_per_byte = self._compiler.columns_per_byte_for(start)
        self._table_idx = (7 - starter_bit) % 8 if self._columns_per_byte == 8 else 0
        self._table = []
        self._table.append(Column())
        self._first_consume = True
        self._incomplete.clear()
        self._forest.reset()
        self._max_position = -1
        self._parsing_mode = mode
        self._hookin_parent = deepcopy(hookin_parent)
        self._compiler._clear_tmp()

    def consume(
        self, char: str | bytes | int
    ) -> Generator[tuple[DerivationTree, bool], None, None]:
        for tree, is_complete in self._consume(char):
            yield self.to_derivation_tree(tree), is_complete

    def _consume(
        self, char: str | bytes | int
    ) -> Generator[tuple[DerivationTree, bool], None, None]:
        assert self._start is not None, "Call new_parse() before consume()"
        if isinstance(char, int):
            char = bytes([char])
        word = char

        # If >= 0, indicates the next bit to be scanned (7-0)
        table = list(self._table)
        per_byte = self._columns_per_byte
        table.extend([Column() for _ in range(len(char) * per_byte)])
        # Add the start state at the first consume
        if self._first_consume:
            table[self._table_idx].add(
                ParseState(self.implicit_start, 0, ((self._start, frozenset()),))
            )
            self._first_consume = False
        curr_table_idx = self._table_idx
        curr_word_idx = 0

        while curr_table_idx < len(table):
            curr_bit_position = 7 - (curr_table_idx % 8)
            if curr_table_idx == len(table) - 1:
                self._table = list(table)
                if len(table) > 0:
                    self._table[-1] = deepcopy(table[-1])
                self._table_idx = curr_table_idx
            # True iff we have processed all characters
            # (or some bits of the last character)
            at_end = curr_word_idx >= len(word)
            ambiguous_starts: list[ParseState] = []
            for state in table[curr_table_idx]:
                if state.finished():
                    if state.nonterminal == self.implicit_start:
                        if at_end:
                            for child in self._forest.children_of(state):
                                yield child, True
                            ambiguous_starts.append(state)

                    self.complete(state, table, curr_table_idx)
                else:
                    if not state.is_incomplete and state.next_symbol_is_nonterminal():
                        self.predict(state, table, curr_table_idx, self._hookin_parent)
                    else:
                        if state.dot is not None and state.dot.is_type(
                            TreeValueType.TRAILING_BITS_ONLY
                        ):
                            # Scan a bit
                            _ = self.scan_bit(
                                state,
                                word,
                                table,
                                curr_table_idx,
                                curr_word_idx,
                                curr_bit_position,
                            )
                        else:
                            if state.dot is not None and state.dot.is_regex:
                                _ = self.scan_regex(
                                    state,
                                    word,
                                    table,
                                    curr_table_idx,
                                    curr_word_idx,
                                )
                            else:
                                _ = self.scan_bytes(
                                    state,
                                    word,
                                    table,
                                    curr_table_idx,
                                    curr_word_idx,
                                )

            if self._parsing_mode == ParsingMode.INCOMPLETE and at_end:
                for state in table[curr_table_idx]:
                    if not state.has_children():
                        continue
                    if state.nonterminal == self.implicit_start:
                        for child in self._forest.children_of(state):
                            if child not in self._incomplete:
                                self._incomplete.add(child)
                                yield child, False
                        if state not in ambiguous_starts:
                            ambiguous_starts.append(state)
                    self.complete(state, table, curr_table_idx)

            for state in ambiguous_starts:
                for child in self._forest.extra_alternatives(state):
                    if self._parsing_mode == ParsingMode.INCOMPLETE:
                        if child in self._incomplete:
                            continue
                        self._incomplete.add(child)
                        yield child, False
                    else:
                        yield child, True

            curr_table_idx += 1
            if curr_table_idx % per_byte == 0:
                curr_word_idx += 1

    def to_derivation_tree(self, tree: DerivationTree) -> DerivationTree:
        return self._forest.to_derivation_tree(tree)

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        return self._forest.collapse(tree)

    def max_position(self) -> int:
        """Return the maximum position reached during parsing."""
        return self._max_position
