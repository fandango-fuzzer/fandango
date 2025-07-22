import enum
import re
from collections.abc import Generator
from collections import defaultdict
from copy import deepcopy
from thefuzz import process as thefuzz_process
from types import NoneType
from typing import Any, Sequence, cast, Optional, Union


from fandango.errors import FandangoValueError, FandangoParseError
from fandango.language.grammar.column import Column
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.literal_generator import LiteralGenerator
from fandango.language.grammar.node_visitors.disambiguator import Disambiguator
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
import fandango.language.grammar.nodes.repetition as repetition_mod
from fandango.language.grammar.nodes.repetition import (
    Option,
    Plus,
    Repetition,
    Star,
)
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.parse_state import ParseState
from fandango.language.tree import DerivationTree
from fandango.language.symbols import Symbol, NonTerminal, Terminal
from fandango.logger import LOGGER
from fandango.language.tree_value import TreeValue


class FuzzingMode(enum.Enum):
    COMPLETE = 0
    IO = 1


def closest_match(word, candidates):
    """
    `word` raises a syntax error;
    return alternate suggestion for `word` from `candidates`
    """
    return thefuzz_process.extractOne(word, candidates)[0]


class ParsingMode(enum.Enum):
    COMPLETE = 0
    INCOMPLETE = 1


class Grammar(NodeVisitor):
    """Represent a grammar."""

    class ParserDerivationTree(DerivationTree):
        def __init__(
            self,
            symbol: Symbol,
            children: Optional[list[DerivationTree]] = None,
            *,
            parent: Optional[DerivationTree] = None,
            sender: Optional[str] = None,
            recipient=None,
            read_only: bool = False,
            origin_repetitions: list[tuple[str, int, int]] | None = None,
        ):
            super().__init__(
                symbol,
                children,
                parent=parent,
                sources=[],
                sender=sender,
                recipient=recipient,
                read_only=read_only,
                origin_repetitions=origin_repetitions,
            )

        def set_children(self, children: list[DerivationTree]):
            self._children = children
            self.invalidate_hash()

    class IterativeParser(NodeVisitor):

        def __init__(
            self,
            grammar: "Grammar",
        ):
            self.implicit_start = NonTerminal("<*start*>")
            self.grammar_rules: dict[NonTerminal, Node] = grammar.rules
            self.grammar = grammar
            self._rules: dict[NonTerminal, set[tuple[NonTerminal, frozenset]]] = {}
            self._implicit_rules: dict[
                NonTerminal, set[tuple[NonTerminal, frozenset]]
            ] = {}
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
            result: list[list[tuple[NonTerminal, frozenset]]] = [[]] + self.visit(
                node.node
            )
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
            current_tree = Grammar.ParserDerivationTree(
                state.nonterminal, state.children
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
                    current_tree = Grammar.ParserDerivationTree(
                        current_state.nonterminal,
                        [*current_state.children, *current_tree.children],
                        **dict(current_state.dot_params or {}),
                    )
                else:
                    current_tree = Grammar.ParserDerivationTree(
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
            assert state.dot.is_type(NoneType)
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
            tree = Grammar.ParserDerivationTree(Terminal(bit))
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
            Scan a byte from the input `word`.
            `state` is the current parse state.
            `table` is the parse table.
            `table[k]` is the current column.
            `word[w]` is the current byte.
            Return True if a byte was matched, False otherwise.
            """

            assert state.dot is not None
            assert not state.dot.is_type(NoneType)
            assert not state.dot.is_regex

            # LOGGER.debug(f"Checking byte(s) {state.dot!r} at position {w:#06x} ({w}) {word[w:]!r}")

            check_word = word[w:]
            if state.is_incomplete:
                prev_terminal = state.children[-1]
                prev_val = prev_terminal.symbol.value()
                prev_val_raw: str | bytes
                if prev_val.is_type(bytes):
                    prev_val_raw = bytes(prev_val)
                    check_word = bytes(
                        TreeValue(prev_val_raw).append(TreeValue(check_word))
                    )
                else:
                    prev_val_raw = str(prev_val)
                    check_word = str(
                        TreeValue(prev_val_raw).append(TreeValue(check_word))
                    )
            if state.dot.is_type(bytes):
                dot_len = len(bytes(state.dot.value()))
            else:
                dot_len = len(str(state.dot.value()))

            match, match_length = state.dot.check(check_word)
            table_idx_multiplier = 1
            if isinstance(check_word, bytes):
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
                tree = Grammar.ParserDerivationTree(Terminal(check_word[:match_length]))
                if state.is_incomplete:
                    next_state.children[-1] = tree
                else:
                    next_state.append_child(tree)
            else:
                next_state = state.next()
                next_state.is_incomplete = False
                next_state.incomplete_idx = 0
                tree = Grammar.ParserDerivationTree(Terminal(check_word[:match_length]))
                if state.is_incomplete:
                    next_state.children[-1] = tree
                else:
                    next_state.append_child(tree)
            table[
                k + ((match_length - state.incomplete_idx) * table_idx_multiplier)
            ].add(next_state)
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
            assert not state.dot.is_type(NoneType)
            assert state.dot.is_regex

            check_word = word[w:]
            prev_match_length = 0
            if state.is_incomplete:
                prev_terminal = state.children[-1]
                prev_val = prev_terminal.symbol.value()
                prev_val_raw: str | bytes
                if prev_val.is_type(bytes):
                    prev_val_raw = bytes(prev_val)
                    check_word = bytes(
                        TreeValue(prev_val_raw).append(TreeValue(check_word))
                    )
                else:
                    prev_val_raw = str(prev_val)
                    check_word = str(
                        TreeValue(prev_val_raw).append(TreeValue(check_word))
                    )
                prev_match_length = len(prev_val_raw)

            table_idx_multiplier = 1
            if isinstance(check_word, bytes):
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
                tree = Grammar.ParserDerivationTree(Terminal(check_word[:match_length]))
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
                tree = Grammar.ParserDerivationTree(
                    Terminal(check_word[:incomplete_match_length])
                )
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
                isinstance(tree.symbol, NonTerminal)
                and tree.symbol.name() in self._nodes
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
                        current_origin_repetitions = list(origin_repetitions) + [
                            rep_option
                        ]
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

        def to_derivation_tree(self, tree: "Grammar.ParserDerivationTree"):
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
                        Grammar.ParserDerivationTree(
                            state.nonterminal, state.children, **dot_params
                        )
                    )
                else:
                    if use_implicit and state.nonterminal in self._implicit_rules:
                        s.append_child(
                            Grammar.ParserDerivationTree(
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
            self._bit_position = starter_bit
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
            if isinstance(char, bytes):
                table.extend([Column() for _ in range(len(char) * 8)])
            else:
                table.extend([Column() for _ in range(len(char))])
            # Add the start state at the first consume
            if self._first_consume:
                table[self._table_idx].add(
                    ParseState(self.implicit_start, 0, ((self._start, frozenset()),))
                )
                self._first_consume = False
            curr_table_idx = self._table_idx
            curr_word_idx = 0
            curr_bit_position = self._bit_position

            while curr_table_idx < len(table):
                if curr_table_idx == len(table) - 1:
                    self._table = list(table)
                    if len(table) > 0:
                        self._table[-1] = deepcopy(table[-1])
                    self._table_idx = curr_table_idx
                    self._bit_position = curr_bit_position
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
                        if (
                            not state.is_incomplete
                            and state.next_symbol_is_nonterminal()
                        ):
                            self.predict(
                                state, table, curr_table_idx, self._hookin_parent
                            )
                        else:
                            if state.dot.is_type(NoneType):
                                # Scan a bit
                                if curr_bit_position < 0:
                                    curr_bit_position = 7
                                match = self.scan_bit(
                                    state,
                                    word,
                                    table,
                                    curr_table_idx,
                                    curr_word_idx,
                                    curr_bit_position,
                                )
                                if match:
                                    pass
                            else:
                                # Scan a regex or a byte
                                if 0 <= curr_bit_position <= 7:
                                    # We are still expecting bits here:
                                    #
                                    # * we may have _peeked_ at a bit,
                                    # without actually parsing it; or
                                    # * we may have a grammar with bits
                                    # that do not come in multiples of 8.
                                    #
                                    # In either case, we need to get back
                                    # to scanning bytes here.
                                    self._bit_position = -1

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

                if curr_bit_position >= 0:
                    # Advance by one bit
                    curr_bit_position -= 1
                if curr_bit_position < 0:
                    # Advance to next byte
                    curr_word_idx += 1

                self.place_repetition_shortcut(table, curr_table_idx)

                if isinstance(char, bytes) and curr_bit_position < 0:
                    if curr_table_idx % 8 == 0:
                        curr_table_idx += 8
                    else:
                        curr_table_idx += -curr_table_idx % 8
                else:
                    curr_table_idx += 1

        def max_position(self):
            """Return the maximum position reached during parsing."""
            return self._max_position

    class Parser:

        def __init__(self, grammar: "Grammar"):
            self._iter_parser = Grammar.IterativeParser(grammar)
            self._cache: dict[
                tuple[
                    str | bytes,
                    NonTerminal,
                    ParsingMode,
                    Optional[DerivationTree],
                ],
                list[DerivationTree],
            ] = {}

        def _parse_forest(
            self,
            word: str | bytes,
            start: str | NonTerminal = "<start>",
            *,
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            starter_bit=-1,
        ):
            """
            Parse a forest of input trees from `word`.
            `start` is the start symbol (default: `<start>`).
            if `allow_incomplete` is True, the function will return trees even if the input ends prematurely.
            """
            self._iter_parser.new_parse(start, mode, hookin_parent, starter_bit)
            yield from self._iter_parser.consume(word)

        def parse_forest(
            self,
            word: str | bytes | int | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            include_controlflow: bool = False,
        ) -> Generator[Optional[DerivationTree], None, None]:
            """
            Yield multiple parse alternatives, using a cache.
            """
            starter_bit = -1
            if isinstance(word, DerivationTree):
                if word.contains_bits():
                    starter_bit = (word.count_terminals() - 1) % 8
                if word.should_be_serialized_to_bytes():
                    bit_string = word.to_bits()
                    word = int(bit_string, 2).to_bytes(
                        (len(bit_string) + 7) // 8, byteorder="big"
                    )
                else:
                    word = word.to_string()
            if isinstance(word, int):
                word = str(word)
            assert isinstance(word, str) or isinstance(word, bytes), type(word)

            if isinstance(start, str):
                start = NonTerminal(start)

            cache_key = (word, start, mode, hookin_parent)
            forest: list[DerivationTree]
            if cache_key in self._cache:
                forest = self._cache[cache_key]
                for tree in forest:
                    tree = deepcopy(tree)
                    if not include_controlflow:
                        yield self.collapse(tree)
                return

            for tree in self._parse_forest(
                word,
                start,
                mode=mode,
                hookin_parent=hookin_parent,
                starter_bit=starter_bit,
            ):
                tree = self._iter_parser.to_derivation_tree(tree)
                if cache_key in self._cache:
                    self._cache[cache_key].append(tree)
                else:
                    self._cache[cache_key] = [tree]
                yield self.collapse(tree) if not include_controlflow else tree

        def parse_multiple(
            self,
            word: str | bytes | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            include_controlflow: bool = False,
        ):
            """
            Yield multiple parse alternatives,
            even for incomplete inputs
            """
            return self.parse_forest(
                word,
                start,
                mode=mode,
                hookin_parent=hookin_parent,
                include_controlflow=include_controlflow,
            )

        def parse(
            self,
            word: str | bytes | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            include_controlflow: bool = False,
        ):
            """
            Return the first parse alternative,
            or `None` if no parse is possible
            """
            tree_gen = self.parse_multiple(
                word,
                start=start,
                mode=mode,
                hookin_parent=hookin_parent,
                include_controlflow=include_controlflow,
            )
            return next(tree_gen, None)

        def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
            return self._iter_parser.collapse(tree)

    def __init__(
        self,
        grammar_settings: Sequence[HasSettings],
        rules: Optional[dict[NonTerminal, Node]] = None,
        fuzzing_mode: Optional[FuzzingMode] = FuzzingMode.COMPLETE,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ):
        self._grammar_settings = grammar_settings
        self.rules: dict[NonTerminal, Node] = rules or {}
        self.generators: dict[NonTerminal, LiteralGenerator] = {}
        self.fuzzing_mode = fuzzing_mode
        self._local_variables = local_variables or {}
        self._global_variables = global_variables or {}
        self._parser = Grammar.Parser(self)

    @property
    def grammar_settings(self) -> Sequence[HasSettings]:
        return self._grammar_settings

    @staticmethod
    def _topological_sort(graph: dict[NonTerminal, set[NonTerminal]]):
        indegree: dict[Any, int] = defaultdict(int)
        queue = []

        for node in graph:
            for neighbour in graph[node]:
                indegree[neighbour] += 1
        for node in graph:
            if indegree[node] == 0:
                queue.append(node)

        topological_order = []
        while queue:
            node = queue.pop(0)
            topological_order.append(node)

            for neighbour in graph[node]:
                indegree[neighbour] -= 1

                if indegree[neighbour] == 0:
                    queue.append(neighbour)

        if len(topological_order) != len(graph):
            print("Cycle exists")
        return topological_order[::-1]

    def is_use_generator(self, tree: DerivationTree):
        symbol = tree.symbol
        if not symbol.is_non_terminal:
            return False
        nt = cast(NonTerminal, symbol)
        if nt not in self.generators:
            return False
        if tree is None:
            path = set()
        else:
            path = set(map(lambda x: x.symbol, tree.get_path()))
        generator_dependencies = self.generator_dependencies(nt)
        intersection = path.intersection(set(generator_dependencies))
        return len(intersection) == 0

    def derive_sources(self, tree: DerivationTree) -> list[DerivationTree]:
        gen_symbol = tree.symbol
        if not gen_symbol.is_non_terminal:
            raise FandangoValueError(f"Tree {tree.symbol} is not a nonterminal")
        if tree.symbol not in self.generators:
            raise FandangoValueError(f"No generator found for tree {tree.symbol}")

        if not self.is_use_generator(tree):
            return []

        assert isinstance(gen_symbol, NonTerminal)
        dependent_generators: dict[NonTerminal, set[NonTerminal]] = {gen_symbol: set()}
        for key, val in self.generators[gen_symbol].nonterminals.items():
            if val.symbol not in self.rules:
                closest = closest_match(str(val), self.rules.keys())
                raise FandangoValueError(
                    f"Symbol {val.symbol!s} not defined in grammar. Did you mean {closest!s}?"
                )

            if val.symbol not in self.generators:
                raise FandangoValueError(
                    f"{val.symbol}: Missing converter from {gen_symbol} ({val.symbol} ::= ... := f({gen_symbol}))"
                )

            dependent_generators[val.symbol] = self.generator_dependencies(val.symbol)
        dependent_gens = self._topological_sort(dependent_generators)
        dependent_gens.remove(gen_symbol)

        args = [tree]
        for symbol in dependent_gens:
            generated_param = self.generate(symbol, args)
            generated_param.sources = []
            generated_param._parent = tree
            for child in generated_param.children:
                self.populate_sources(child)
            args.append(generated_param)
        args.pop(0)
        return args

    def derive_generator_output(self, tree: DerivationTree):
        generated = self.generate(tree.nonterminal, tree.sources)
        return generated.children

    def populate_sources(self, tree: DerivationTree):
        self._rec_remove_sources(tree)
        self._populate_sources(tree)

    def _populate_sources(self, tree: DerivationTree):
        if self.is_use_generator(tree):
            tree.sources = self.derive_sources(tree)
            for child in tree.children:
                child.set_all_read_only(True)
            return
        for child in tree.children:
            self._populate_sources(child)

    def _rec_remove_sources(self, tree: DerivationTree):
        tree.sources = []
        for child in tree.children:
            self._rec_remove_sources(child)

    def generate_string(
        self,
        symbol: str | NonTerminal = "<start>",
        sources: Optional[list[DerivationTree]] = None,
    ) -> tuple[list[DerivationTree], str]:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        if self.generators[symbol] is None:
            raise ValueError(f"{symbol.format_as_spec()}: no generator")

        sources_: dict[Symbol, DerivationTree]
        if sources is None:
            sources_ = dict()
        else:
            sources_ = {tree.symbol: tree for tree in sources}
        generator = self.generators[symbol]

        local_variables = self._local_variables.copy()
        for id, nonterminal in generator.nonterminals.items():
            if nonterminal.symbol not in sources_:
                raise FandangoValueError(
                    f"{nonterminal.symbol}: missing generator parameter"
                )
            local_variables[id] = sources_[nonterminal.symbol]

        return list(sources_.values()), eval(
            generator.call, self._global_variables, local_variables
        )

    def generator_dependencies(self, symbol: str | NonTerminal = "<start>"):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        if self.generators[symbol] is None:
            return set()
        return set(
            map(lambda x: x.symbol, self.generators[symbol].nonterminals.values())
        )

    def generate(
        self,
        symbol: str | NonTerminal = "<start>",
        sources: Optional[list[DerivationTree]] = None,
    ) -> DerivationTree:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        sources, string = self.generate_string(symbol, sources)
        if not (
            isinstance(string, str)
            or isinstance(string, bytes)
            or isinstance(string, int)
            or isinstance(string, tuple)
        ):
            raise TypeError(
                f"Generator {self.generators[symbol]} must return string, bytes, int, or tuple (returned {string!r})"
            )

        if isinstance(string, tuple):
            string = str(DerivationTree.from_tree(string))
        tree = self.parse(string, symbol)
        if tree is None:
            raise FandangoParseError(
                f"Could not parse {string!r} (generated by {self.generators[symbol]}) into {symbol.format_as_spec()}"
            )
        tree.sources = [p.deepcopy(copy_parent=False) for p in sources]
        return tree

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        return self._parser.collapse(tree)

    def fuzz(
        self,
        start: str | NonTerminal = "<start>",
        max_nodes: int = 50,
        prefix_node: Optional[DerivationTree] = None,
    ) -> DerivationTree:
        if isinstance(start, str):
            start = NonTerminal(start)
        if prefix_node is None:
            root = DerivationTree(start)
        else:
            root = prefix_node
        fuzzed_idx = len(root.children)
        NonTerminalNode(start, self._grammar_settings).fuzz(
            root, self, max_nodes=max_nodes
        )
        root = root.children[fuzzed_idx]
        root._parent = None
        return root

    def update(self, grammar: Union["Grammar", dict[NonTerminal, Node]], prime=True):
        generators: dict[NonTerminal, LiteralGenerator]
        local_variables: dict[str, Any]
        global_variables: dict[str, Any]
        if isinstance(grammar, Grammar):
            generators = grammar.generators
            local_variables = grammar._local_variables
            global_variables = grammar._global_variables
            rules = grammar.rules
            fuzzing_mode = grammar.fuzzing_mode
        else:
            rules = grammar
            generators = {}
            local_variables = {}
            global_variables = {}
            fuzzing_mode = FuzzingMode.COMPLETE

        self.rules.update(rules)
        self.fuzzing_mode = fuzzing_mode
        self.generators.update(generators)

        for symbol in rules.keys():
            # We're updating from a grammar with a rule, but no generator,
            # so we should remove the generator if it exists
            if symbol not in generators and symbol in self.generators:
                del self.generators[symbol]

        self._parser = Grammar.Parser(self)
        self._local_variables.update(local_variables)
        self._global_variables.update(global_variables)
        if prime:
            self.prime()

    def parse(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        include_controlflow: bool = False,
    ):
        return self._parser.parse(
            word,
            start,
            mode=mode,
            hookin_parent=hookin_parent,
            include_controlflow=include_controlflow,
        )

    def parse_forest(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        include_controlflow: bool = False,
    ) -> Generator[Optional[DerivationTree], None, None]:
        return self._parser.parse_forest(
            word, start, mode=mode, include_controlflow=include_controlflow
        )

    def parse_multiple(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: ParsingMode = ParsingMode.COMPLETE,
        include_controlflow: bool = False,
    ):
        return self._parser.parse_multiple(
            word, start, mode=mode, include_controlflow=include_controlflow
        )

    def max_position(self):
        """Return the maximum position reached during last parsing."""
        return self._parser._iter_parser.max_position()

    def __contains__(self, item: str | NonTerminal):
        if not isinstance(item, NonTerminal):
            item = NonTerminal(item)
        return item in self.rules

    def __getitem__(self, item: str | NonTerminal):
        if not isinstance(item, NonTerminal):
            item = NonTerminal(item)
        return self.rules[item]

    def __setitem__(self, key: str | NonTerminal, value: Node):
        if not isinstance(key, NonTerminal):
            key = NonTerminal(key)
        self.rules[key] = value

    def __delitem__(self, key: str | NonTerminal):
        if not isinstance(key, NonTerminal):
            key = NonTerminal(key)
        del self.rules[key]

    def __iter__(self):
        return iter(self.rules)

    def __len__(self):
        return len(self.rules)

    def __repr__(self):
        return "\n".join(
            [
                f"{key.name()} ::= {value.format_as_spec()}{' := ' + str(self.generators[key]) if key in self.generators else ''}"
                for key, value in self.rules.items()
            ]
        )

    def msg_parties(self, *, include_recipients: bool = True) -> set:
        parties: set[str] = set()
        for rule in self.rules.values():
            parties |= rule.msg_parties(include_recipients=include_recipients)
        return parties

    def get_repr_for_rule(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return (
            f"{symbol.format_as_spec()} ::= {self.rules[symbol].format_as_spec()}"
            f"{' := ' + str(self.generators[symbol]) if symbol in self.generators else ''}"
        )

    @staticmethod
    def dummy():
        return Grammar(grammar_settings=[], rules={})

    def set_generator(
        self, symbol: str | NonTerminal, param: str, searches_map: dict = {}
    ):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators[symbol] = LiteralGenerator(
            call=param, nonterminals=searches_map
        )

    def remove_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators.pop(symbol)

    def has_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return symbol in self.generators

    def get_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return self.generators.get(symbol, None)

    def update_parser(self):
        self._parser = Grammar.Parser(self)

    def compute_kpath_coverage(
        self, derivation_trees: list[DerivationTree], k: int
    ) -> float:
        """
        Computes the k-path coverage of the grammar given a set of derivation trees.
        Returns a score between 0 and 1 representing the fraction of k-paths covered.
        """
        # Generate all possible k-paths in the grammar
        all_k_paths = self._generate_all_k_paths(k)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            covered_k_paths.update(self._extract_k_paths_from_tree(tree, k))

        # Compute coverage score
        if not all_k_paths:
            return 1.0  # If there are no k-paths, coverage is 100%
        return len(covered_k_paths) / len(all_k_paths)

    def _generate_all_k_paths(self, k: int) -> set[tuple[Node, ...]]:
        """
        Computes the *k*-paths for this grammar, constructively. See: doi.org/10.1109/ASE.2019.00027

        :param k: The length of the paths.
        :return: All paths of length up to *k* within this grammar.
        """

        initial = set()
        initial_work: list[Node] = [
            NonTerminalNode(name, self._grammar_settings) for name in self.rules.keys()
        ]
        while initial_work:
            node = initial_work.pop(0)
            if node in initial:
                continue
            initial.add(node)
            initial_work.extend(node.descendents(self))

        work: list[set[tuple[Node, ...]]] = [set((x,) for x in initial)]

        for _ in range(1, k):
            next_work = set()
            for base in work[-1]:
                for descendent in base[-1].descendents(self):
                    next_work.add(base + (descendent,))
            work.append(next_work)

        # return set.union(*work)
        return work[-1]

    @staticmethod
    def _extract_k_paths_from_tree(
        tree: DerivationTree, k: int
    ) -> set[tuple[Symbol, ...]]:
        """
        Extracts all k-length paths (k-paths) from a derivation tree.
        """
        paths = set()

        def traverse(node: DerivationTree, current_path: tuple[Symbol, ...]):
            new_path = current_path + (node.symbol,)
            if len(new_path) == k:
                paths.add(new_path)
                # Do not traverse further to keep path length at k
                return
            for child in node.children:
                traverse(child, new_path)

        traverse(tree, ())
        return paths

    def prime(self):
        LOGGER.debug("Priming grammar")
        nodes: list[Node] = sum(
            [self.visit(self.rules[symbol]) for symbol in self.rules], []
        )
        while nodes:
            node = nodes.pop(0)
            if isinstance(node, TerminalNode):
                continue
            elif isinstance(node, NonTerminalNode):
                if node.symbol not in self.rules:
                    raise FandangoValueError(
                        f"Symbol {node.symbol.format_as_spec()} not found in grammar"
                    )
                if self.rules[node.symbol].distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        self.rules[node.symbol].distance_to_completion + 1
                    )
            elif isinstance(node, Alternative):
                node.distance_to_completion = (
                    min([n.distance_to_completion for n in node.alternatives]) + 1
                )
                if node.distance_to_completion == float("inf"):
                    nodes.append(node)
            elif isinstance(node, Concatenation):
                if any([n.distance_to_completion == float("inf") for n in node.nodes]):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        sum([n.distance_to_completion for n in node.nodes]) + 1
                    )
            elif isinstance(node, Repetition):
                if node.node.distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    try:
                        min_rep = node.min
                    except ValueError:
                        min_rep = 0
                    node.distance_to_completion = (
                        node.node.distance_to_completion * min_rep + 1
                    )
            else:
                raise FandangoValueError(f"Unknown node type {node.node_type}")

    def slice_parties(self, parties: list[str]) -> None:
        """
        Returns a new grammar that only contains the rules that are relevant to the given parties.
        """
        for expansion in self.rules.values():
            expansion.slice_parties(parties)
        self.fuzzing_mode = FuzzingMode.COMPLETE

    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative):
        return self.visitChildren(node) + [node]

    def visitConcatenation(self, node: Concatenation):
        return self.visitChildren(node) + [node]

    def visitRepetition(self, node: Repetition):
        return self.visit(node.node) + [node]

    def visitStar(self, node: Star):
        return self.visit(node.node) + [node]

    def visitPlus(self, node: Plus):
        return self.visit(node.node) + [node]

    def visitOption(self, node: Option):
        return self.visit(node.node) + [node]

    def visitNonTerminalNode(self, node: NonTerminalNode):
        return [node]

    def visitTerminalNode(self, node: TerminalNode):
        return []

    def visitCharSet(self, node: CharSet):
        return []

    def compute_k_paths(self, k: int) -> set[tuple[Node, ...]]:
        """
        Computes all possible k-paths in the grammar.

        :param k: The length of the paths.
        :return: A set of tuples, each tuple representing a k-path as a sequence of symbols.
        """
        return self._generate_all_k_paths(k)

    def traverse_derivation(
        self,
        tree: DerivationTree,
        disambiguator: Optional[Disambiguator] = None,
        paths: Optional[set[tuple[Node, ...]]] = None,
        cur_path: Optional[tuple[Node, ...]] = None,
    ) -> set[tuple[Node, ...]]:
        if disambiguator is None:
            disambiguator = Disambiguator(self, self._grammar_settings)
        if paths is None:
            paths = set()
        if tree.symbol.is_terminal:
            if cur_path is None:
                cur_path = (TerminalNode(tree.terminal, self._grammar_settings),)
            paths.add(cur_path)
        elif isinstance(tree.symbol, NonTerminal):
            if cur_path is None:
                cur_path = (NonTerminalNode(tree.nonterminal, self._grammar_settings),)
            assert tree.symbol == cast(NonTerminalNode, cur_path[-1]).symbol
            disambiguation = disambiguator.visit(self.rules[tree.nonterminal])
            for tree, path in zip(
                tree.children, disambiguation[tuple(c.symbol for c in tree.children)]
            ):
                self.traverse_derivation(tree, disambiguator, paths, cur_path + path)
        else:
            raise FandangoValueError(
                f"Unknown symbol type: {type(tree.symbol)}: {tree.symbol}"
            )
        return paths

    def compute_grammar_coverage(
        self, derivation_trees: list[DerivationTree], k: int
    ) -> tuple[float, int, int]:
        """
        Compute the coverage of k-paths in the grammar based on the given derivation trees.

        :param derivation_trees: A list of derivation trees (solutions produced by FANDANGO).
        :param k: The length of the paths (k).
        :return: A float between 0 and 1 representing the coverage.
        """

        # Compute all possible k-paths in the grammar
        all_k_paths = self.compute_k_paths(k)

        disambiguator = Disambiguator(self, self._grammar_settings)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            for path in self.traverse_derivation(tree, disambiguator):
                # for length in range(1, k + 1):
                for window in range(len(path) - k + 1):
                    covered_k_paths.add(path[window : window + k])

        # Compute coverage
        if not all_k_paths:
            raise FandangoValueError("No k-paths found in the grammar")

        return (
            len(covered_k_paths) / len(all_k_paths),
            len(covered_k_paths),
            len(all_k_paths),
        )

    def get_spec_env(self):
        return self._global_variables, self._local_variables

    def contains_type(self, tp: type, *, start="<start>") -> bool:
        """
        Return true if the grammar can produce an element of type `tp` (say, `int` or `bytes`).
        * `start`: a start symbol other than `<start>`.
        """
        if isinstance(start, str):
            start = NonTerminal(start)

        if start not in self.rules:
            raise FandangoValueError(f"Start symbol {start} not defined in grammar")

        # We start on the right hand side of the start symbol
        start_node = self.rules[start]
        seen = set()

        def node_matches(node):
            if node in seen:
                return False
            seen.add(node)

            if isinstance(node, TerminalNode) and node.symbol.is_type(tp):
                return True
            if any(node_matches(child) for child in node.children()):
                return True
            if isinstance(node, NonTerminalNode):
                return node_matches(self.rules[node.symbol])
            return False

        return node_matches(start_node)

    def contains_bits(self, *, start="<start>") -> bool:
        """
        Return true iff the grammar can produce a bit element (0 or 1).
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(NoneType, start=start)

    def contains_bytes(self, *, start="<start>") -> bool:
        """
        Return true iff the grammar can produce a bytes element.
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(bytes, start=start)

    def contains_strings(self, *, start="<start>") -> bool:
        """
        Return true iff the grammar can produce a (UTF-8) string element.
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(str, start=start)

    def set_max_repetition(self, max_rep: int):
        repetition_mod.MAX_REPETITIONS = max_rep

    def get_max_repetition(self):
        return repetition_mod.MAX_REPETITIONS
