from collections.abc import Callable, Sequence
from itertools import pairwise
from typing import NamedTuple, Optional

from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree


class Step(NamedTuple):
    """
    A packet and where it is produced.
    A Step contains the path from a producing symbol down to a produced symbol.
    It includes controlflow nodes.
    """

    path: tuple[NonTerminal, ...]

    @property
    def packet(self) -> NonTerminal:
        return self.path[-1]

    @property
    def parent(self) -> NonTerminal:
        """The rule that produces the packet."""
        return next(
            symbol
            for symbol in reversed(self.path[:-1])
            if not Step.is_control_flow(symbol)
        )

    @staticmethod
    def is_control_flow(symbol: Symbol) -> bool:
        return isinstance(symbol, NonTerminal) and symbol.name().startswith("<__")

    @staticmethod
    def of_path(
        path: Sequence[NonTerminal],
        is_recursive_call: Callable[[NonTerminal, NonTerminal], bool],
    ) -> "Step":
        """The step of a path from the start symbol down to a packet."""
        rules = [
            index
            for index, symbol in enumerate(path[:-1])
            if not Step.is_control_flow(symbol)
        ]
        for called_symbol, calling_symbol in pairwise(reversed(rules)):
            if is_recursive_call(path[calling_symbol], path[called_symbol]):
                return Step(tuple(path[calling_symbol:]))
        return Step(tuple(path))

    @staticmethod
    def of_message(
        message: DerivationTree,
        is_recursive_call: Callable[[NonTerminal, NonTerminal], bool],
    ) -> "Step":
        """The step of a message in a control-flow tree."""
        path: list[NonTerminal] = []
        node: Optional[DerivationTree] = message
        while node is not None:
            assert isinstance(node.symbol, NonTerminal)
            path.append(node.symbol)
            node = node.parent
        return Step.of_path(path[::-1], is_recursive_call)
