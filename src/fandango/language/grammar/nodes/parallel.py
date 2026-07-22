from collections.abc import Iterable, Iterator, Sequence
from typing import TYPE_CHECKING, Any

from fandango.errors import FandangoError
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.symbols.symbol import Symbol
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    import fandango.language.grammar.node_visitors


class Parallel(Node):
    def __init__(
        self,
        nodes: Iterable[Node],
        grammar_settings: Sequence[HasSettings],
        id: str = "",
    ):
        self.id = id
        self.nodes = list(nodes)
        super().__init__(NodeType.PARALLEL, grammar_settings)

    def to_symbol(self) -> Symbol:
        return NonTerminal(f"<__{self.id}>")

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ) -> None:
        raise FandangoError("Parallel node doesn't support fuzzing")

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor[fandango.language.grammar.node_visitors.node_visitor.AggregateType, fandango.language.grammar.node_visitors.node_visitor.ResultType]",
    ) -> Any:  # should be ResultType, beartype falls on its face
        return visitor.visitParallel(self)

    def children(self) -> list[Node]:
        return self.nodes

    def __getitem__(self, item: int) -> Node:
        return self.nodes.__getitem__(item)

    def __len__(self) -> int:
        return len(self.nodes)

    def format_as_spec(self) -> str:
        return " || ".join(map(lambda x: x.format_as_spec(), self.nodes))

    def descendents(
        self,
        grammar: "fandango.language.grammar.grammar.Grammar",
        filter_controlflow: bool = False,
    ) -> Iterator["Node"]:
        if filter_controlflow:
            for child in self.nodes:
                if child.is_controlflow:
                    yield from child.descendents(grammar, filter_controlflow)
                else:
                    yield child
        else:
            yield from self.nodes
