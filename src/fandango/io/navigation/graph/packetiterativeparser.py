from copy import deepcopy
from typing import Optional

from fandango.errors import FandangoValueError
from fandango.io.packet_evolution.packet_mounter import MessageHolder
from fandango.language import NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.parser.column import Column
from fandango.language.grammar.parser.iterative_parser import IterativeParser
from fandango.language.grammar.parser.parse_state import ParseState
from fandango.language.tree import DerivationTree


class PacketIterativeParser(IterativeParser):
    def __init__(self, grammar_rules: dict[NonTerminal, Node]):
        super().__init__(grammar_rules)
        self.reference_tree: Optional[DerivationTree] = None
        self._consumed_history: Optional[str] = None

    def parse_history(self, history: str) -> None:
        if (
            self._consumed_history is None
            or not history.startswith(self._consumed_history)
            or len(self._context_rules) != 0
        ):
            self.new_parse(NonTerminal("<start>"), ParsingMode.INCOMPLETE)
            self._consumed_history = ""
        continuation = history[len(self._consumed_history) :]
        if continuation != "":
            self.consume(continuation)
        self._consumed_history = history

    def construct_incomplete_tree(
        self, state: ParseState, table: list[Column]
    ) -> DerivationTree:
        i_tree = super().construct_incomplete_tree(state, table)
        i_cpy = deepcopy(i_tree)
        if self.reference_tree is None:
            raise FandangoValueError(
                "Reference tree must be set before constructing the incomplete tree!"
            )
        with MessageHolder(
            self.reference_tree
        ).hold_messages_context() as session_messages:
            session_messages.hang_messages_into(i_cpy)
        return i_cpy


class NavigatorPacketIterativeParser(PacketIterativeParser):
    """
    Variant of PacketIterativeParser for use in PacketNavigator.
    Keeps reduced-grammar symbols (e.g. <_packet_X>) intact so that
    the grammar-graph walk stays consistent with the reduced grammar.
    """

    def construct_incomplete_tree(
        self, state: ParseState, table: list[Column]
    ) -> DerivationTree:
        return IterativeParser.construct_incomplete_tree(self, state, table)
