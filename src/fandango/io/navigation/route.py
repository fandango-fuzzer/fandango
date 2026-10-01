from typing import NamedTuple

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.step import Step
from fandango.language.symbols.non_terminal import NonTerminal


class PlannedPacket(NamedTuple):
    packet: PacketNonTerminal
    step: Step

    def __repr__(self) -> str:
        return f"PlannedPacket({self.packet!r})"


RouteSymbol = NonTerminal | PlannedPacket | None

Route = list[RouteSymbol]
