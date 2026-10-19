from typing import NamedTuple, Optional

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


class GuidePath(NamedTuple):
    route: Route
    target_step: Optional[Step] = None

    def __repr__(self) -> str:
        return f"GuidePath({self.route!r}, target_step={self.target_step!r})"
