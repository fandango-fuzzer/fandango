import random
from typing import TYPE_CHECKING, Iterator, Sequence
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    from fandango.language.grammar.grammar import Grammar
    from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor


class Alternative(Node):
    def __init__(
        self,
        alternatives: list[Node],
        grammar_settings: Sequence[HasSettings],
        id: str = "",
    ):
        self.id = id
        self.alternatives = alternatives
        super().__init__(NodeType.ALTERNATIVE, grammar_settings)

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        in_range_nodes = list(
            filter(lambda x: x.distance_to_completion < max_nodes, self.alternatives)
        )
        if len(in_range_nodes) == 0:
            min_ = min(self.alternatives, key=lambda x: x.distance_to_completion)
            random.choice(
                [
                    a
                    for a in self.alternatives
                    if a.distance_to_completion <= min_.distance_to_completion
                ]
            ).fuzz(parent, grammar, 0, in_message)
            return
        random.choice(in_range_nodes).fuzz(parent, grammar, max_nodes, in_message)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitAlternative(self)

    def children(self):
        return self.alternatives

    def slice_parties(self, parties: list[str]) -> None:
        self.alternatives = [
            node for node in self.alternatives if node.in_parties(parties)
        ]
        super().slice_parties(parties)

    def __getitem__(self, item):
        return self.alternatives.__getitem__(item)

    def __len__(self):
        return len(self.alternatives)

    def format_as_spec(self) -> str:
        return (
            "(" + " | ".join(map(lambda x: x.format_as_spec(), self.alternatives)) + ")"
        )

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield from self.alternatives
