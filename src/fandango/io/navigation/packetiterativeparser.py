from copy import deepcopy
from typing import Optional

from fandango.language.tree import DerivationTree
from fandango.errors import FandangoValueError
from fandango.language import NonTerminal
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.parser.column import Column
from fandango.language.grammar.parser.iterative_parser import IterativeParser
from fandango.language.grammar.parser.parse_state import ParseState


class PacketIterativeParser(IterativeParser):
    def __init__(self, grammar_rules: dict[NonTerminal, Node]):
        super().__init__(grammar_rules)
        self.reference_tree: Optional[DerivationTree] = None
        self.detailed_tree: Optional[DerivationTree] = None

    def construct_incomplete_tree(
        self, state: ParseState, table: list[Column]
    ) -> DerivationTree:
        i_tree = super().construct_incomplete_tree(state, table)
        i_cpy = deepcopy(i_tree)
        if self.reference_tree is None:
            raise FandangoValueError(
                "Reference tree must be set before constructing the incomplete tree!"
            )
        for i_msg, r_msg in zip(
            i_cpy.protocol_msgs(), self.reference_tree.protocol_msgs()
        ):
            i_msg.msg.set_children(r_msg.msg.children)
            i_msg.msg.sources = r_msg.msg.sources
            symbol = r_msg.msg.symbol
            if isinstance(symbol, NonTerminal):
                # TODO: Is this just to create a new string?
                i_msg.msg.symbol = NonTerminal("<" + symbol.name()[1:])
            else:
                raise FandangoValueError("NonTerminal symbol must be a string!")
        return i_cpy
