from typing import TYPE_CHECKING, Iterator, Sequence
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols.terminal import Terminal
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
    from fandango.language.grammar.grammar import Grammar


class CharSet(Node):
    def __init__(
        self,
        chars: str,
        grammar_settings: Sequence[HasSettings],
    ):
        self._grammar_settings = grammar_settings
        self.chars = chars
        super().__init__(NodeType.CHAR_SET, grammar_settings)

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ) -> list[DerivationTree]:
        raise NotImplementedError("CharSet fuzzing not implemented")

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitCharSet(self)

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        for char in self.chars:
            yield TerminalNode(Terminal(char), self._grammar_settings)

    def format_as_spec(self) -> str:
        return self.chars
