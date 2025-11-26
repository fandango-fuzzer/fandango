from typing import TYPE_CHECKING, Any
from collections.abc import Iterable, Iterator, Sequence
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.tree import DerivationTree
from fandango.language.symbols.symbol import Symbol
from fandango.language.symbols.non_terminal import NonTerminal

if TYPE_CHECKING:
    import fandango


class Concatenation(Node):
    def __init__(
        self,
        nodes: Iterable[Node],
        grammar_settings: Sequence[HasSettings],
        id: str = "",
    ):
        self.id = id
        self.nodes = list(nodes)
        super().__init__(NodeType.CONCATENATION, grammar_settings)

    def to_symbol(self) -> Symbol:
        return NonTerminal(f"<__{self.id}>")

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ) -> None:
        prev_parent_size = parent.size()
        for node in self.nodes:
            if node.distance_to_completion >= max_nodes:
                node.fuzz(parent, grammar, 0, in_message)
            else:
                reserved_distance = self.distance_to_completion
                for dist_node in self.nodes:
                    reserved_distance -= dist_node.distance_to_completion
                    if dist_node == node:
                        break
                node.fuzz(
                    parent, grammar, int(max_nodes - reserved_distance), in_message
                )
            max_nodes -= parent.size() - prev_parent_size
            prev_parent_size = parent.size()

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor[fandango.language.grammar.node_visitors.node_visitor.AggregateType, fandango.language.grammar.node_visitors.node_visitor.ResultType]",
    ) -> Any:  # should be ResultType, beartype falls on its face
        return visitor.visitConcatenation(self)

    def children(self) -> list[Node]:
        return self.nodes

    def slice_parties(self, parties: list[str]) -> None:
        self.nodes = [node for node in self.nodes if node.in_parties(parties)]
        super().slice_parties(parties)

    def __getitem__(self, item: int) -> Node:
        return self.nodes.__getitem__(item)

    def __len__(self) -> int:
        return len(self.nodes)

    def format_as_spec(self) -> str:
        return " ".join(map(lambda x: x.format_as_spec(), self.nodes))

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
