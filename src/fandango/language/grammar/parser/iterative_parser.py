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
    ParseState,
    RuleSymbol,
)
from fandango.language.grammar.parser.parser_tree import ParserDerivationTree
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.symbols.symbol import Symbol
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import TreeValue, TreeValueType


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
        self._max_position = -1
        self._column_index = 0
        self._table: list[Column] = []
        self._parsing_mode = ParsingMode.COMPLETE
        self._start: Optional[NonTerminal] = None
        self._first_consume = True
        self._hookin_parent: Optional[DerivationTree] = None
        self._columns_per_byte = 8
        self._forest = ForestBuilder(self._rules, self._compiler._nodes)
        self._consumed_length = 0
        # saves starting states per index of the given input for complete and incomplete parses.
        self._completed: dict[int, list[ParseState]] = {}
        # for incomplete parsed we only store positions of other states that are also in _completed or that
        # are at the end of one given input from consume
        self._incomplete: dict[int, list[ParseState]] = {}

    @staticmethod
    def has_unfinished_states(column: Column) -> bool:
        """Whether any state in `column` still has input to match."""
        return any(
            state.is_terminal_partial_match
            # A force-completed state was cut short to report a partial parse,
            # so it waits for nothing; counting it would make every column that
            # holds one look as if the parse could grow.
            or (not state.is_finished and not state.force_completed)
            for state in column
        )

    def can_continue(self) -> bool:
        if len(self._table) <= 1:
            # Assume that an unstarted parse can continue
            return True
        table: list[Column] = list(self._table)
        table[self._column_index] = deepcopy(table[self._column_index])

        for state in table[self._column_index]:
            if state.is_finished:
                self.complete(state, table, self._column_index)

        return any(
            state.is_terminal_partial_match or not state.is_finished
            for state in table[self._column_index]
        )

    def predict(
        self,
        state: ParseState,
        table: list[Column],
        column_index: int,
        hookin_parent: Optional[DerivationTree] = None,
    ) -> None:
        symbol = state.next_symbol
        assert symbol is not None
        assert isinstance(symbol, NonTerminal)
        predicted = table[column_index].predicted
        if symbol in predicted:
            # Predicting the same symbol in the same column again adds nothing
            # new. Context rules are the exception: their expansion depends on
            # the tree parsed so far.
            if symbol not in self._context_rules:
                return
        else:
            predicted.add(symbol)

        for rules in (self._rules, self._implicit_rules, self._tmp_rules):
            alternatives = rules.get(symbol)
            if alternatives is not None:
                table[column_index].update(
                    {
                        ParseState(symbol, column_index, alternative)
                        for alternative in alternatives
                    }
                )
                return
        if symbol in self._context_rules:
            node, rule_symbol = self._context_rules[symbol]
            self.predict_ctx_rule(
                state, table, column_index, node, rule_symbol, hookin_parent
            )

    def current_tree(self) -> Optional[DerivationTree]:
        if len(self._table[self._column_index]) == 0:
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
                if table_state.next_symbol == current_state.nonterminal:
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
                    **dict(current_state.next_params or {}),
                )
            else:
                current_tree = ParserDerivationTree(
                    current_state.nonterminal,
                    [*self._forest.children_of(current_state), current_tree],
                    **dict(current_state.next_params or {}),
                )

        return current_tree.children[0]

    def predict_ctx_rule(
        self,
        state: ParseState,
        table: list[Column],
        column_index: int,
        node: Node,
        rule_symbol: RuleSymbol,
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
                node, rule_symbol, tree if hookin_parent is None else hookin_parent
            )
        except (ValueError, FandangoValueError):
            return
        finally:
            if hookin_parent is not None:
                hookin_parent.set_children(hookin_parent.children[:-1])
        new_symbols: list[tuple[Symbol, frozenset[tuple[str, Any]]]] = []
        placed = False
        for symbol, params in state.symbols:
            if symbol == state.next_symbol and not placed:
                new_symbols.append(context_nt)
                placed = True
            else:
                new_symbols.append((symbol, params))
        new_state = ParseState(
            state.nonterminal,
            state.position,
            tuple(new_symbols),
            state.dot,
            self._forest.children_of(state),
            state.matched_length,
            state.force_completed,
        )
        if state in table[column_index]:
            table[column_index].replace(state, new_state)
        self.predict(new_state, table, column_index)

    def scan_bit(
        self,
        state: ParseState,
        word: str | bytes,
        table: list[Column],
        column_index: int,
        word_index: int,
        bit_position: int,
    ) -> bool:
        """
        Scan a bit from the input `word`.
        `table` is the parse table (may be modified by this function).
        `table[column_index]` is the current column.
        `word[word_index]` is the current byte.
        `bit_position` is the current bit position (7-0).
        Return True if a bit was matched, False otherwise.
        """
        assert state.next_symbol is not None
        assert state.next_symbol.is_type(TreeValueType.TRAILING_BITS_ONLY)
        assert 0 <= bit_position <= 7

        if word_index >= len(word):
            return False

        # Get the highest bit. If `word` is bytes, word[word_index] is an integer.
        byte = ord(word[word_index]) if isinstance(word, str) else word[word_index]
        bit = (byte >> bit_position) & 1

        match, match_length = state.next_symbol.check(bit)
        if not match or match_length == 0:
            return False

        next_state = state.next()
        tree = ParserDerivationTree(Terminal(bit))
        next_state.set_edge(state, tree)
        # A bit advances the parse by exactly one column; the table holds
        # `columns_per_byte` (8) columns per input byte for this.
        table[column_index + 1].add(next_state)

        # Save the maximum position reached, so we can report errors
        self._max_position = max(self._max_position, word_index)

        return True

    def scan_bytes(
        self,
        state: ParseState,
        word: str | bytes,
        table: list[Column],
        column_index: int,
        word_index: int,
    ) -> bool:
        """
        Scan a byte from the input `word`.
        `state` is the current parse state.
        `table` is the parse table.
        `table[column_index]` is the current column.
        `word[word_index]` is the current byte.
        Return True if a byte was matched, False otherwise.
        """

        assert state.next_symbol is not None
        assert not (
            state.next_symbol.is_type(TreeValueType.TRAILING_BITS_ONLY)
            or state.next_symbol.is_type(TreeValueType.EMPTY)
        )
        assert not state.next_symbol.is_regex

        check_word = word[word_index:]
        if state.is_terminal_partial_match:
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
        if state.next_symbol.is_type(TreeValueType.BYTES):
            dot_len = len(bytes(state.next_symbol.value()))
        else:
            dot_len = len(str(state.next_symbol.value()))

        match, match_length = state.next_symbol.check(check_word)
        columns_per_byte = self._columns_per_byte

        if not match:
            if (word_index + dot_len - state.matched_length) < len(word):
                return False
            match, match_length = state.next_symbol.check(check_word, incomplete=True)
            if not match or match_length == 0:
                return False

            next_state = state.copy()
            next_state.matched_length = match_length
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            next_state.set_edge(
                state.predecessor() if state.is_terminal_partial_match else state, tree
            )
        else:
            next_state = state.next()
            next_state.matched_length = 0
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            next_state.set_edge(
                state.predecessor() if state.is_terminal_partial_match else state, tree
            )
        table[
            column_index + ((match_length - state.matched_length) * columns_per_byte)
        ].add(next_state)
        self._max_position = max(self._max_position, word_index + match_length)

        return True

    def scan_regex(
        self,
        state: ParseState,
        word: str | bytes,
        table: list[Column],
        column_index: int,
        word_index: int,
    ) -> bool:
        """
        Scan a regex terminal from the input `word`.
        `state` is the current parse state.
        `table` is the parse table.
        `table[column_index]` is the current column.
        `word[word_index]` is the current byte.
        Return True if the regex matched, completely or as an
        extendable prefix, False otherwise.
        """

        assert state.next_symbol is not None
        assert not (
            state.next_symbol.is_type(TreeValueType.TRAILING_BITS_ONLY)
            or state.next_symbol.is_type(TreeValueType.EMPTY)
        )
        assert state.next_symbol.is_regex

        check_word = word[word_index:]
        prev_match_length = 0
        if state.is_terminal_partial_match:
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

        columns_per_byte = self._columns_per_byte
        # A growing a partial match replaces the previous partial terminal
        predecessor = state.predecessor() if state.is_terminal_partial_match else state
        # A regex accepts prefixes of the remaining input in several lengths,
        # and only the grammar around it decides which one carries the parse.
        # We walk the prefixes one by one and store a state at every length the regex
        # accepts.
        scanned = False
        taken = prev_match_length
        for prefix_length in range(prev_match_length + 1, len(check_word) + 1):
            prefix = check_word[:prefix_length]
            match, match_length = state.next_symbol.check(prefix)
            if match and match_length > taken:
                next_state = state.next()
                next_state.matched_length = 0
                tree = ParserDerivationTree(Terminal(check_word[:match_length]))
                next_state.set_edge(predecessor, tree)
                table[
                    column_index
                    + ((match_length - state.matched_length) * columns_per_byte)
                ].add(next_state)
                self._max_position = max(self._max_position, word_index + match_length)
                scanned = True

            incomplete_match, incomplete_match_length = state.next_symbol.check(
                prefix, incomplete=True
            )
            if incomplete_match_length <= taken:
                incomplete_match = False
            if not incomplete_match:
                break
            if prefix_length == len(check_word):
                next_state = state.copy()
                next_state.matched_length = incomplete_match_length
                tree = ParserDerivationTree(
                    Terminal(check_word[:incomplete_match_length])
                )
                next_state.set_edge(predecessor, tree)
                table[
                    column_index
                    + (
                        (incomplete_match_length - state.matched_length)
                        * columns_per_byte
                    )
                ].add(next_state)
                scanned = True
            taken = incomplete_match_length

        return scanned

    def _leo_entry(
        self, table: list[Column], column_index: int, symbol: Symbol
    ) -> Optional[LeoEntry]:
        """
        When only one way to reduce upwards from `symbol` exists, returns the
        top of that chain, else None.
        """
        pending: list[tuple[int, Symbol, ParseState]] = []
        entry: Optional[LeoEntry] = None
        current_index, current_symbol = column_index, symbol
        while True:
            column = table[current_index]
            if current_symbol in column.leo:
                entry = column.leo[current_symbol]
                break
            waiters = column.waiting.get(current_symbol)
            # Ensure that we don't get a collision, from multiple states pointing to the same symbol.
            if waiters is None or len(waiters) != 1:
                column.leo[current_symbol] = None
                break
            waiter = waiters[0]
            # Only expand leo path if we are at the last symbol of the rule.
            if (
                waiter.dot != len(waiter.symbols) - 1
                or waiter.is_terminal_partial_match
            ):
                column.leo[current_symbol] = None
                break
            pending.append((current_index, current_symbol, waiter))
            current_index, current_symbol = waiter.position, waiter.nonterminal
            if current_index > column_index:
                break

        for cached_index, cached_symbol, waiter in reversed(pending):
            entry = LeoEntry(waiter) if entry is None else entry.push(waiter)
            table[cached_index].leo[cached_symbol] = entry
        return entry

    def complete(
        self,
        state: ParseState,
        table: list[Column],
        column_index: int,
    ) -> None:
        column = table[column_index]
        force_completed = not state.is_finished
        if force_completed and state.position == column_index:
            # Spans no input, so it would hand a waiter of the same column
            # its own children as the filler's derivation.
            return
        if state.position < column_index:
            entry = self._leo_entry(table, state.position, state.nonterminal)
            if entry is not None:
                top = entry.top
                next_state = top.next(force_completed)
                next_state.add_edge(
                    top, LeoNest(entry.chain, state, top.next_params), top.next_params
                )
                column.add(next_state)
                return
        for waiter in table[state.position].waiting_for(state.nonterminal):
            next_state = waiter.next(force_completed)
            next_state.add_edge(waiter, state, waiter.next_params)
            column.add(next_state)

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
        self._column_index = (7 - starter_bit) % 8 if self._columns_per_byte == 8 else 0
        self._table = []
        self._table.append(Column())
        self._first_consume = True
        self._forest.reset()
        self._max_position = -1
        self._consumed_length = 0
        self._completed = {}
        self._incomplete = {}
        self._parsing_mode = mode
        self._hookin_parent = deepcopy(hookin_parent)
        self._compiler._clear_tmp()

    def consume(self, char: str | bytes | int) -> None:
        """
        Continues the current parse by adding `char` to the stream.
        Read the parses back with `parsed_positions` and `tree_at`.
        """
        assert self._start is not None, "Call new_parse() before consume()"
        if isinstance(char, int):
            char = bytes([char])
        word = char

        consumed = self._consumed_length
        self._consumed_length = consumed + len(word)
        table = list(self._table)
        columns_per_byte = self._columns_per_byte
        table.extend([Column() for _ in range(len(char) * columns_per_byte)])
        # Add the start state at the first consume
        if self._first_consume:
            table[self._column_index].add(
                ParseState(self.implicit_start, 0, ((self._start, frozenset()),))
            )
            self._first_consume = False
        column_index = self._column_index
        word_index = 0

        while column_index < len(table):
            bit_position = 7 - (column_index % 8)
            if column_index == len(table) - 1:
                self._table = list(table)
                self._table[-1] = deepcopy(table[-1])
                self._column_index = column_index
            # True iff we have processed all characters
            # (or some bits of the last character)
            at_end = word_index >= len(word)
            offset = consumed + word_index
            for state in table[column_index]:
                if state.is_finished:
                    # A parse counts at whole bytes, and at the end of the
                    # input even when that falls within a byte.
                    if state.nonterminal == self.implicit_start and (
                        column_index % columns_per_byte == 0 or at_end
                    ):
                        self._store_emittable_state(self._completed, offset, state)

                    self.complete(state, table, column_index)
                else:
                    if (
                        not state.is_terminal_partial_match
                        and state.next_symbol_is_nonterminal()
                    ):
                        self.predict(state, table, column_index, self._hookin_parent)
                    else:
                        if state.next_symbol is not None and state.next_symbol.is_type(
                            TreeValueType.TRAILING_BITS_ONLY
                        ):
                            # Scan a bit
                            _ = self.scan_bit(
                                state,
                                word,
                                table,
                                column_index,
                                word_index,
                                bit_position,
                            )
                        else:
                            if (
                                state.next_symbol is not None
                                and state.next_symbol.is_regex
                            ):
                                _ = self.scan_regex(
                                    state,
                                    word,
                                    table,
                                    column_index,
                                    word_index,
                                )
                            else:
                                _ = self.scan_bytes(
                                    state,
                                    word,
                                    table,
                                    column_index,
                                    word_index,
                                )

            if self._parsing_mode == ParsingMode.INCOMPLETE and at_end:
                for state in table[column_index]:
                    if state.is_finished or not state.has_children():
                        continue
                    if state.nonterminal == self.implicit_start:
                        self._store_emittable_state(self._incomplete, offset, state)
                    self.complete(state, table, column_index)
                # A complete parse the input could still extend is an
                # incomplete parse as well: an empty parse has no state to cut
                # short, yet more input may well extend it.
                if self.has_unfinished_states(table[column_index]):
                    for state in self._completed.get(offset, []):
                        self._store_emittable_state(self._incomplete, offset, state)

            column_index += 1
            if column_index % columns_per_byte == 0:
                word_index += 1

    @staticmethod
    def _store_emittable_state(
        states_by_offset: dict[int, list[ParseState]], offset: int, state: ParseState
    ) -> None:
        """Stores `state` under `offset`, replacing an equal one stored before."""
        states = states_by_offset.setdefault(offset, [])
        for index, known in enumerate(states):
            if known == state:
                states[index] = state
                return
        states.append(state)

    def consumed_length(self) -> int:
        """How many units of input `consume` has taken since `new_parse`."""
        return self._consumed_length

    def parsed_positions(self) -> list[int]:
        """
        Every offset since `new_parse` at which the start symbol has a complete parse.
        """
        return list(self._completed)

    def tree_at(
        self, offset: int, *, incomplete: bool = False
    ) -> Generator[tuple[DerivationTree, bool], None, None]:
        """
        Every parse parsable with `offset` given bytes, as `(tree, is_complete)`.

        Without `incomplete`, only the complete parses. With it also the
        incomplete ones: those cut short at the end of a `consume`, and the
        complete ones once more when the input could go on.
        """
        flagged = [(state, True) for state in self._completed.get(offset, [])]
        if incomplete:
            flagged.extend((state, False) for state in self._incomplete.get(offset, []))
        seen: set[tuple[DerivationTree, bool]] = set()
        for state, flag in flagged:
            for tree in self._forest.derivations_of(state):
                if (tree, flag) in seen:
                    continue
                seen.add((tree, flag))
                yield self.to_derivation_tree(tree), flag

    def to_derivation_tree(self, tree: DerivationTree) -> DerivationTree:
        return self._forest.to_derivation_tree(tree)

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        return self._forest.collapse(tree)

    def max_position(self) -> int:
        """Return the maximum position reached during parsing."""
        return self._max_position
