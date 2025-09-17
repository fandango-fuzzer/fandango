import random
from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Optional

import fandango.language.grammar.nodes as nodes
from fandango.errors import FandangoValueError
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols.terminal import Terminal
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    import fandango


class Repetition(Node):
    def __init__(
        self,
        node: Node,
        grammar_settings: Sequence[HasSettings],
        id: str = "",
        min_: int = 0,
        max_: Optional[int] = None,
    ):
        self.id = id
        self.min = min_
        self._max = max_
        self.node = node
        self.bounds_constraint: Optional[
            "fandango.constraints.repetition_bounds.RepetitionBoundsConstraint"
        ] = None
        self.iteration = 0
        if min_ < 0:
            raise FandangoValueError(
                f"Minimum repetitions {min_} must be greater than or equal to 0"
            )
        if self.max <= 0 or self.max < min_:
            raise FandangoValueError(
                f"Maximum repetitions {self.max} must be greater than 0 or greater than min {min_}"
            )
        super().__init__(NodeType.REPETITION, grammar_settings)

    @property
    def internal_max(self):
        return self._max

    @property
    def max(self):
        if self._max is None:
            return nodes.MAX_REPETITIONS
        return self._max

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor",
    ):
        return visitor.visitRepetition(self)

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
        override_current_iteration: Optional[int] = None,
        override_starting_repetition: int = 0,
        override_iterations_to_perform: Optional[int] = None,
    ):
        prev_parent_size = parent.size()
        prev_children_len = len(parent.children)
        if override_current_iteration is None:
            self.iteration += 1
            current_iteration = self.iteration
        else:
            current_iteration = override_current_iteration

        rep_goal = random.randint(self.min, self.max)
        if override_iterations_to_perform is not None:
            rep_goal = override_iterations_to_perform - override_starting_repetition

        reserved_max_nodes = self.distance_to_completion

        for rep in range(rep_goal):
            current_rep = rep + override_starting_repetition
            if self.node.distance_to_completion >= max_nodes:
                if rep >= self.min and override_iterations_to_perform is None:
                    break
                self.node.fuzz(parent, grammar, 0, in_message)
            else:
                reserved_max_nodes -= self.node.distance_to_completion
                self.node.fuzz(
                    parent, grammar, int(max_nodes - reserved_max_nodes), in_message
                )
            for child in parent.children[prev_children_len:]:
                child.origin_repetitions.insert(
                    0, (self.id, current_iteration, current_rep)
                )
            max_nodes -= parent.size() - prev_parent_size
            prev_parent_size = parent.size()
            prev_children_len = len(parent.children)

    def format_as_spec(self) -> str:
        if self.min == self.max:
            return f"{self.node.format_as_spec()}{{{self.min}}}"
        return f"{self.node.format_as_spec()}{{{self.min},{self.max}}}"

    def descendents(
        self, grammar: "fandango.language.grammar.grammar.Grammar"
    ) -> Iterator["Node"]:
        base: list = []
        if self.min == 0:
            base.append(TerminalNode(Terminal(""), self._grammar_settings))
        if self.min <= 1 <= self.max:
            base.append(self.node)
        yield Alternative(
            base
            + [
                Concatenation([self.node] * r, self._grammar_settings)
                for r in range(max(2, self.min), self.max + 1)
            ],
            self._grammar_settings,
        )

    def children(self):
        return [self.node]

    def in_parties(self, parties: list[str]) -> bool:
        return self.node.in_parties(parties)


class Star(Repetition):
    def __init__(
        self,
        node: Node,
        grammar_settings: Sequence[HasSettings],
        id: str = "",
    ):
        super().__init__(node, grammar_settings, id, min_=0)

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor",
    ):
        return visitor.visitStar(self)

    def format_as_spec(self) -> str:
        return self.node.format_as_spec() + "*"


class Plus(Repetition):
    def __init__(
        self,
        node: Node,
        grammar_settings: Sequence[HasSettings],
        id: str = "",
    ):
        super().__init__(node, grammar_settings, id, min_=1)

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
        override_current_iteration: Optional[int] = None,
        override_starting_repetition: int = 0,
        override_iterations_to_perform: Optional[int] = None,
    ):
        # Gmutator mutation (1b)
        if random.random() < self.settings.get("plus_should_return_nothing"):
            return  # nop, don't add a node
        else:
            return super().fuzz(
                parent,
                grammar,
                max_nodes,
                in_message,
                override_current_iteration,
                override_starting_repetition,
                override_iterations_to_perform,
            )

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor",
    ):
        return visitor.visitPlus(self)

    def format_as_spec(self) -> str:
        return self.node.format_as_spec() + "+"


class Option(Repetition):
    def __init__(
        self,
        node: Node,
        grammar_settings: Sequence[HasSettings],
        id: str = "",
    ):
        super().__init__(node, grammar_settings, id, min_=0, max_=1)

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
        override_current_iteration: Optional[int] = None,
        override_starting_repetition: int = 0,
        override_iterations_to_perform: Optional[int] = None,
    ):
        # Gmutator mutation (1c)
        should_return_multiple = random.random() < self.settings.get(
            "option_should_return_multiple"
        )
        if should_return_multiple:
            repetition = Repetition(
                self.node, self._grammar_settings, id=self.id, min_=2
            )
            repetition.distance_to_completion = self.node.distance_to_completion * 2 + 1
            return repetition.fuzz(
                parent,
                grammar,
                max_nodes,
                in_message,
                override_current_iteration,
                override_starting_repetition,
                override_iterations_to_perform,
            )
        else:
            return super().fuzz(
                parent,
                grammar,
                max_nodes,
                in_message,
                override_current_iteration,
                override_starting_repetition,
                override_iterations_to_perform,
            )

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor",
    ):
        return visitor.visitOption(self)

    def format_as_spec(self) -> str:
        return self.node.format_as_spec() + "?"

    def descendents(
        self, grammar: "fandango.language.grammar.grammar.Grammar"
    ) -> Iterator["Node"]:
        yield from (self.node, TerminalNode(Terminal(""), self._grammar_settings))
