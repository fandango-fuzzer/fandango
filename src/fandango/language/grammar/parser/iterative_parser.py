from copy import deepcopy
from types import NoneType
from typing import Optional

from fandango.errors import FandangoValueError
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.parser.column import Column
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.repetition import Option
from fandango.language.grammar.nodes.repetition import Plus
from fandango.language.grammar.nodes.repetition import Star
from fandango.language.grammar.parser.parse_state import ParseState
from fandango.language.grammar.parser.parser_tree import ParserDerivationTree
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import TreeValue, TreeValueType


class IterativeParser(NodeVisitor):
    def __init__(
        self,
        grammar_rules: dict[NonTerminal, Node],
    ):
        self.implicit_start = NonTerminal("<*start*>")
        self.grammar_rules: dict[NonTerminal, Node] = grammar_rules
        self._rules: dict[NonTerminal, set[tuple[NonTerminal, frozenset]]] = {}
        self._implicit_rules: dict[NonTerminal, set[tuple[NonTerminal, frozenset]]] = {}
        self._context_rules: dict[
            NonTerminal, tuple[Node, tuple[NonTerminal, frozenset]]
        ] = dict()
        self._tmp_rules: dict[NonTerminal, set[tuple[NonTerminal, frozenset]]] = {}
        self._incomplete: set[DerivationTree] = set()
        self._nodes: dict[str, Node] = {}
        self._max_position = -1
        self.elapsed_time: float = 0.0
        self._process()
        self._table_idx = 0
        self._table: list[Column] = []
        self._parsing_mode = ParsingMode.COMPLETE
        self._bit_position = -1
        self._start: Optional[NonTerminal] = None
        self._first_consume = True
        self._hookin_parent: Optional[DerivationTree] = None
        self._prefix_word = None

    def _process(self):
        self._rules.clear()
        self._implicit_rules.clear()
        self._context_rules.clear()
        for nonterminal in self.grammar_rules:
            self.set_rule(nonterminal, self.visit(self.grammar_rules[nonterminal]))

        for nonterminal in self._implicit_rules:
            self._implicit_rules[nonterminal] = {
                tuple(a)  # type: ignore[misc]
                for a in self._implicit_rules[nonterminal]
            }

    def set_implicit_rule(
        self, rule: list[list[tuple[NonTerminal, frozenset]]]
    ) -> tuple[NonTerminal, frozenset]:
        nonterminal = NonTerminal(f"<*{len(self._implicit_rules)}*>")
        self._implicit_rules[nonterminal] = rule  # type: ignore[assignment]
        return (nonterminal, frozenset())

    def set_rule(
        self,
        nonterminal: NonTerminal,
        rule: list[list[tuple[NonTerminal, frozenset]]],
    ):
        self._rules[nonterminal] = {tuple(a) for a in rule}  # type: ignore[misc]

    def set_context_rule(
        self, node: Node, non_terminal: tuple[NonTerminal, frozenset]
    ) -> NonTerminal:
        nonterminal = NonTerminal(f"<*ctx_{len(self._context_rules)}*>")
        self._context_rules[nonterminal] = (node, non_terminal)
        return nonterminal

    def set_tmp_rule(
        self,
        rule: list[list[tuple[NonTerminal, frozenset]]],
        nonterminal: Optional[NonTerminal] = None,
    ):
        if nonterminal is None:
            nonterminal = NonTerminal(f"<*tmp_{len(self._tmp_rules)}*>")
        rule_id = str(nonterminal.value())[2:-2]
        self._tmp_rules[nonterminal] = {tuple(a) for a in rule}  # type: ignore[misc]
        return (nonterminal, frozenset()), rule_id

    def _clear_tmp(self):
        self._tmp_rules.clear()

    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative):
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result = self.visitChildren(node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitConcatenation(self, node: Concatenation):
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: list[list[tuple[NonTerminal, frozenset]]] = [[]]
        for child in node.children():
            to_add = self.visit(child)
            new_result = []
            for r in result:
                for a in to_add:
                    new_result.append(r + a)
            result = new_result
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitRepetition(
        self,
        node: Repetition,
        nt: Optional[tuple[NonTerminal, frozenset]] = None,
        tree: Optional[DerivationTree] = None,
    ):
        repetition_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[repetition_nt.name()] = node
        is_context = node.bounds_constraint is not None

        if nt is None:
            alternatives = self.visit(node.node)
            nt = self.set_implicit_rule(alternatives)

            if is_context:
                i_nt = self.set_context_rule(node, nt)
                self.set_rule(repetition_nt, [[(i_nt, frozenset())]])
                return [[(repetition_nt, frozenset())]]

        prev = None
        if node.bounds_constraint is not None:
            assert tree is not None
            right_most_node = tree
            while len(right_most_node.children) != 0:
                right_most_node = right_most_node.children[-1]
            node_min, _ = node.bounds_constraint.min(right_most_node)
            node_max, _ = node.bounds_constraint.max(right_most_node)
        else:
            node_min = node.min
            node_max = node.max
        for rep in range(node_min, node_max):
            alts = [[nt]]
            if prev is not None:
                alts.append([nt, prev])
            if is_context:
                prev, rule_id = self.set_tmp_rule(alts)
            else:
                prev = self.set_implicit_rule(alts)
        alts = [node_min * [nt]]
        if prev is not None:
            alts.append(node_min * [nt] + [prev])
        if is_context:
            tmp_nt, rule_id = self.set_tmp_rule(alts)
            return [[tmp_nt]]
        min_nt = self.set_implicit_rule(alts)
        self.set_rule(repetition_nt, [[min_nt]])
        return [[(repetition_nt, frozenset())]]

    def visitStar(self, node: Star):
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: list[list[tuple[NonTerminal, frozenset]]] = [[]]
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitPlus(self, node: Plus):
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: list[list[tuple[NonTerminal, frozenset]]] = []
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r)
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitOption(self, node: Option):
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: list[list[tuple[NonTerminal, frozenset]]] = [[]] + self.visit(node.node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitNonTerminalNode(self, node: NonTerminalNode):
        params = dict()
        if node.sender is not None:
            params["sender"] = node.sender
        if node.recipient is not None:
            params["recipient"] = node.recipient
        parameters = frozenset(params.items())
        return [[(node.symbol, parameters)]]

    def visitTerminalNode(self, node: TerminalNode):
        return [[(node.symbol, frozenset())]]

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        if tree is None:
            return None
        if isinstance(tree.symbol, NonTerminal):
            if str(tree.symbol.value()).startswith("<__"):
                raise FandangoValueError(
                    "Can't collapse a tree with an implicit root node"
                )
        return self._collapse(tree)[0]

    def _collapse(self, tree: DerivationTree) -> list[DerivationTree]:
        reduced = []
        for child in tree.children:
            rec_reduced = self._collapse(child)
            reduced.extend(rec_reduced)

        if isinstance(tree.symbol, NonTerminal):
            if str(tree.symbol.value()).startswith("<__"):
                return reduced

        return [
            DerivationTree(
                tree.symbol,
                children=reduced,
                sources=tree.sources,
                read_only=tree.read_only,
                recipient=tree.recipient,
                sender=tree.sender,
                origin_repetitions=tree.origin_repetitions,
            )
        ]

    def can_continue(self):
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
    ):
        symbol = state.dot
        assert symbol is not None
        assert isinstance(symbol, NonTerminal)
        if state.dot in self._rules:
            table[k].update(
                {
                    ParseState(state.dot, k, rule, 0)  # type: ignore[arg-type]
                    for rule in self._rules[symbol]
                }
            )
        elif state.dot in self._implicit_rules:
            table[k].update(
                {
                    ParseState(state.dot, k, rule, 0)  # type: ignore[arg-type]
                    for rule in self._implicit_rules[symbol]
                }
            )
        elif state.dot in self._tmp_rules:
            table[k].update(
                {
                    ParseState(state.dot, k, rule, 0)  # type: ignore[arg-type]
                    for rule in self._tmp_rules[symbol]
                }
            )
        elif state.dot in self._context_rules:
            node, nt = self._context_rules[symbol]
            self.predict_ctx_rule(state, table, k, node, nt, hookin_parent)

    def construct_incomplete_tree(
        self, state: ParseState, table: list[Column]
    ) -> DerivationTree:
        current_tree = ParserDerivationTree(state.nonterminal, state.children)
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
                    [*current_state.children, *current_tree.children],
                    **dict(current_state.dot_params or {}),
                )
            else:
                current_tree = ParserDerivationTree(
                    current_state.nonterminal,
                    [*current_state.children, current_tree],
                    **dict(current_state.dot_params or {}),
                )

        return current_tree.children[0]

    def predict_ctx_rule(
        self,
        state: ParseState,
        table: list[Column],
        k: int,
        node: Node,
        nt_rule,
        hookin_parent: Optional[DerivationTree] = None,
    ):
        if not isinstance(node, Repetition):
            raise FandangoValueError(f"Node {node} needs to be a Repetition")

        tree = self.construct_incomplete_tree(state, table)
        collapsed_tree = self.collapse(tree)
        assert collapsed_tree is not None
        tree = collapsed_tree
        if hookin_parent is not None:
            hookin_parent.set_children(hookin_parent.children + [tree])
        try:
            [[context_nt]] = self.visitRepetition(
                node, nt_rule, tree if hookin_parent is None else hookin_parent
            )
        except (ValueError, FandangoValueError):
            return
        finally:
            if hookin_parent is not None:
                hookin_parent.set_children(hookin_parent.children[:-1])
        new_symbols = []
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
            state.children,
            state.is_incomplete,
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
        next_state.append_child(tree)
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
        Scan a byte from th noe input `word`.
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
            prev_terminal = state.children[-1]
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
        table_idx_multiplier = 8

        if not match:
            if (w + dot_len - state.incomplete_idx) < len(word):
                return False
            match, match_length = state.dot.check(check_word, incomplete=True)
            if not match or match_length == 0:
                return False

            next_state = state.copy()
            next_state.incomplete_idx = match_length
            next_state.is_incomplete = True
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            if state.is_incomplete:
                next_state.children[-1] = tree
            else:
                next_state.append_child(tree)
        else:
            next_state = state.next()
            next_state.is_incomplete = False
            next_state.incomplete_idx = 0
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            if state.is_incomplete:
                next_state.children[-1] = tree
            else:
                next_state.append_child(tree)
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
        mode: ParsingMode,
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
            prev_terminal = state.children[-1]
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

        table_idx_multiplier = 8
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
            next_state.is_incomplete = False
            next_state.incomplete_idx = 0
            tree = ParserDerivationTree(Terminal(check_word[:match_length]))
            if state.is_incomplete:
                next_state.children[-1] = tree
            else:
                next_state.append_child(tree)
            table[
                k + ((table_offset - state.incomplete_idx) * table_idx_multiplier)
            ].add(next_state)
        if incomplete_match:
            next_state = state.copy()
            next_state.is_incomplete = True
            next_state.incomplete_idx = incomplete_match_length
            tree = ParserDerivationTree(Terminal(check_word[:incomplete_match_length]))
            if state.is_incomplete:
                next_state.children[-1] = tree
            else:
                next_state.append_child(tree)
            table[
                k
                + (
                    (incomplete_table_offset - state.incomplete_idx)
                    * table_idx_multiplier
                )
            ].add(next_state)

        self._max_position = max(self._max_position, w + match_length)
        return True

    def _rec_to_derivation_tree(
        self,
        tree: DerivationTree,
        origin_repetitions: Optional[list[tuple[str, int, int]]] = None,
    ):
        if origin_repetitions is None:
            origin_repetitions = []

        rep_option = None
        is_controlflow_node = (
            isinstance(tree.symbol, NonTerminal) and tree.symbol.name() in self._nodes
        )
        if is_controlflow_node:
            nt = tree.symbol
            assert isinstance(nt, NonTerminal)
            node = self._nodes[nt.name()]
            if isinstance(node, Repetition):
                node.iteration += 1
                rep_option = (node.id, node.iteration, 0)

        children: list[DerivationTree] = []
        for child in tree.children:
            if is_controlflow_node:
                if rep_option is not None:
                    current_origin_repetitions = list(origin_repetitions) + [rep_option]
                    rep_option = (rep_option[0], rep_option[1], rep_option[2] + 1)
                else:
                    current_origin_repetitions = list(origin_repetitions)
            else:
                current_origin_repetitions = []

            children.append(
                self._rec_to_derivation_tree(child, current_origin_repetitions)
            )  # type: ignore[arg-type]

        return DerivationTree(
            tree.symbol,
            children,
            parent=tree.parent,
            sources=tree.sources,
            sender=tree.sender,
            recipient=tree.recipient,
            read_only=tree.read_only,
            origin_repetitions=origin_repetitions,
        )

    def to_derivation_tree(self, tree: "ParserDerivationTree"):
        if tree is None:
            return None
        return self._rec_to_derivation_tree(tree)  # type: ignore[arg-type]

    def complete(
        self,
        state: ParseState,
        table: list[Column],
        k: int,
        use_implicit: bool = False,
    ):
        for s in table[state.position].find_dot(state.nonterminal):
            dot_params = dict(s.dot_params)
            s = s.next()
            if state.nonterminal in self._rules:
                s.append_child(
                    ParserDerivationTree(
                        state.nonterminal, state.children, **dot_params
                    )
                )
            else:
                if use_implicit and state.nonterminal in self._implicit_rules:
                    s.append_child(
                        ParserDerivationTree(
                            NonTerminal(state.nonterminal.symbol),
                            state.children,
                            **s.dot_params,
                        )
                    )
                else:
                    s.extend_children(state.children)
            table[k].add(s)

    def place_repetition_shortcut(self, table: list[Column], k: int):
        col = table[k]
        states = col.states
        beginner_nts = [f"<__{NodeType.PLUS}:", f"<__{NodeType.STAR}:"]

        found_beginners = set()
        for state in states:
            if any(
                map(
                    lambda b: str(state.nonterminal.value()).startswith(b),
                    beginner_nts,
                )
            ):
                found_beginners.add(state.symbols[0][0])

        for beginner in found_beginners:
            current_col_state = None
            for state in states:
                if state.nonterminal == beginner:
                    if state.finished():
                        continue
                    if len(state.symbols) == 2 and state.dot == beginner:
                        current_col_state = state
                        break
            if current_col_state is None:
                continue
            new_state = current_col_state
            origin_states = table[current_col_state.position].find_dot(
                current_col_state.dot
            )
            if len(origin_states) != 1:
                continue
            origin_state = origin_states[0]
            while not any(
                map(
                    lambda b: str(origin_state.nonterminal.value()).startswith(b),
                    beginner_nts,
                )
            ):
                new_state = ParseState(
                    new_state.nonterminal,
                    origin_state.position,
                    new_state.symbols,
                    new_state._dot,
                    [*origin_state.children, *new_state.children],
                    new_state.is_incomplete,
                )
                origin_states = table[new_state.position].find_dot(new_state.dot)
                if len(origin_states) != 1:
                    new_state = None  # type: ignore[assignment]
                    break
                origin_state = origin_states[0]

            if new_state is not None:
                col.replace(current_col_state, new_state)

    def new_parse(
        self,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        starter_bit=-1,
    ):
        if isinstance(start, str):
            start = NonTerminal(start)
        self._start = start
        self._table_idx = (7 - starter_bit) % 8
        self._table = []
        self._table.append(Column())
        self._first_consume = True
        self._incomplete.clear()
        self._max_position = -1
        self._parsing_mode = mode
        self._hookin_parent = deepcopy(hookin_parent)
        self._clear_tmp()

    def consume(self, char: str | bytes | int):
        for tree in self._consume(char):
            yield self.to_derivation_tree(tree)

    def _consume(self, char: str | bytes | int):
        assert self._start is not None, "Call new_parse() before consume()"
        if isinstance(char, int):
            char = bytes([char])
        word = char

        # If >= 0, indicates the next bit to be scanned (7-0)
        table = list(self._table)
        table.extend([Column() for _ in range(len(char) * 8)])
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
            for state in table[curr_table_idx]:
                if state.finished():
                    if state.nonterminal == self.implicit_start:
                        if at_end:
                            for child in state.children:
                                yield child

                    self.complete(state, table, curr_table_idx)
                else:
                    if not state.is_incomplete and state.next_symbol_is_nonterminal():
                        self.predict(state, table, curr_table_idx, self._hookin_parent)
                    else:
                        if state.dot.is_type(TreeValueType.TRAILING_BITS_ONLY):
                            # Scan a bit
                            match = self.scan_bit(
                                state,
                                word,
                                table,
                                curr_table_idx,
                                curr_word_idx,
                                curr_bit_position,
                            )
                        else:
                            if state.dot.is_regex:
                                match = self.scan_regex(
                                    state,
                                    word,
                                    table,
                                    curr_table_idx,
                                    curr_word_idx,
                                    self._parsing_mode,
                                )
                            else:
                                match = self.scan_bytes(
                                    state,
                                    word,
                                    table,
                                    curr_table_idx,
                                    curr_word_idx,
                                )

            if self._parsing_mode == ParsingMode.INCOMPLETE and at_end:
                for state in table[curr_table_idx]:
                    if len(state.children) == 0:
                        continue
                    if state.nonterminal == self.implicit_start:
                        for child in state.children:
                            if child not in self._incomplete:
                                self._incomplete.add(child)
                                yield child
                    self.complete(state, table, curr_table_idx)

            self.place_repetition_shortcut(table, curr_table_idx)
            curr_table_idx += 1
            if curr_table_idx % 8 == 0:
                curr_word_idx += 1

    def max_position(self):
        """Return the maximum position reached during parsing."""
        return self._max_position
