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
    target_packets: tuple[PlannedPacket, ...] = ()

    def __repr__(self) -> str:
        return f"GuidePatch({self.route!r}, target_packets={self.target_packets!r})"
