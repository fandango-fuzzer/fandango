from collections.abc import Sequence
from typing import NamedTuple, Optional

from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


class Step(NamedTuple):
    parent: NonTerminal
    control_flow: tuple[NonTerminal, ...]
    packet: NonTerminal

    @staticmethod
    def of_path(path: Sequence[NonTerminal]) -> Optional["Step"]:
        """Produce the step of a path ending with packet."""
        *above, packet = path
        for index in reversed(range(len(above))):
            if not above[index].name().startswith("<__"):
                return Step(above[index], tuple(above[index + 1 :]), packet)
        return None

    @staticmethod
    def of_message(message: DerivationTree) -> Optional["Step"]:
        """The step of a message in a control-flow tree."""
        path: list[NonTerminal] = []
        node: Optional[DerivationTree] = message
        while node is not None:
            assert isinstance(node.symbol, NonTerminal)
            path.append(node.symbol)
            node = node.parent
        return Step.of_path(path[::-1])
