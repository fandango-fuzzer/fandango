from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any

from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node, NodeType

if TYPE_CHECKING:
    import fandango.language.grammar.node_visitors


class Parallel(Concatenation):
    def __init__(
        self,
        nodes: Iterable[Node],
        grammar_settings: Sequence[HasSettings],
        id: str = "",
    ):
        super().__init__(nodes, grammar_settings, id)
        self._node_type = NodeType.PARALLEL


    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor[fandango.language.grammar.node_visitors.node_visitor.AggregateType, fandango.language.grammar.node_visitors.node_visitor.ResultType]",
    ) -> Any:  # should be ResultType, beartype falls on its face
        return visitor.visitParallel(self)

    def format_as_spec(self) -> str:
        return " || ".join(map(lambda x: x.format_as_spec(), self.nodes))
