from types import NoneType
from typing import TYPE_CHECKING, Sequence
import exrex
from fandango.errors import FandangoValueError
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.symbols import Terminal
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    from fandango.language.grammar import Grammar
    from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor


class TerminalNode(Node):
    def __init__(
        self,
        symbol: Terminal,
        grammar_settings: Sequence[HasSettings],
    ):
        self._grammar_settings = grammar_settings
        self.symbol = symbol
        super().__init__(
            NodeType.TERMINAL, grammar_settings, distance_to_completion=1.0
        )

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        if not self.symbol.is_regex:
            parent.add_child(DerivationTree(self.symbol))
        else:
            if self.symbol.is_type(bytes):
                # Exrex can't do bytes, so we decode to str and back
                instance = exrex.getone(
                    self.symbol.value().to_string(bytes_to_str_encoding="latin-1")
                ).encode("latin-1")
            elif self.symbol.is_type(str):
                instance = exrex.getone(str(self.symbol.value()))
            elif self.symbol.is_type(NoneType):
                instance = exrex.getone(int(self.symbol.value()))
            else:
                raise FandangoValueError(
                    f"Unsupported type: {self.symbol.value().type_}"
                )
            parent.add_child(DerivationTree(Terminal(instance)))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitTerminalNode(self)

    def format_as_spec(self) -> str:
        return self.symbol.format_as_spec()

    def __eq__(self, other):
        return isinstance(other, TerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)
