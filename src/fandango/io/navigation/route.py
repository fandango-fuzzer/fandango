from typing import NamedTuple, Optional

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.step import Step
from fandango.language.symbols.non_terminal import NonTerminal


class PlannedPacket(NamedTuple):
    packet: PacketNonTerminal
    step: Optional[Step]


RouteSymbol = NonTerminal | PlannedPacket | None

Route = list[RouteSymbol]
