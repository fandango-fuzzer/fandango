from typing import NamedTuple, Optional

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.route import GuidePath, PlannedPacket, Route
from fandango.io.navigation.step import Step
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree


class Deviation(NamedTuple):
    """A message that did not follow the guide path."""

    planned: Optional[PlannedPacket]
    message: DerivationTree

    def __repr__(self) -> str:
        return f"Deviation(planned={self.planned!r}, message={self.message.symbol!r})"


class GuidePathTracker:
    """
    Tracks the planned route, give the next packet to produce, and detects derivations from
    the given path.
    """

    def __init__(self, permutation_groups: dict[NonTerminal, frozenset[NonTerminal]]):
        self._permutation_groups = permutation_groups
        self._route: Route = []
        self._target_step: Optional[Step] = None
        self._target_packets: tuple[PlannedPacket, ...] = ()

    def set_guide_path(
        self,
        guide_path: GuidePath,
    ) -> None:
        """Sets the route to follow, with the step into its target and the packets inside the target, if any."""
        self._route = list(guide_path.route)
        self._target_step = guide_path.target_step
        self._target_packets = guide_path.target_packets

    def refused_step(self, sender: str) -> Optional[Step]:
        """The step the sender refused by answering otherwise after the route: to its first packet inside the target, else into the target."""
        return next(
            (p.step for p in self._target_packets if p.packet.sender == sender),
            self._target_step,
        )

    def clear(self) -> None:
        self._route = []
        self._target_step = None
        self._target_packets = ()

    @property
    def route(self) -> Route:
        return list(self._route)

    @property
    def is_empty(self) -> bool:
        return len(self._route) == 0

    @property
    def ends_run(self) -> bool:
        """True if the route leads to the end of the run."""
        return None in self._route

    def next_packet(self) -> Optional[PlannedPacket]:
        next_planned = self._next_planned()
        return None if next_planned is None else next_planned[1]

    def next_new_parent_states(self) -> list[Symbol]:
        """
        Parent states of the next packet that are not yet in the session tree.
        All states along the route if no packet is left.
        """
        next_planned = self._next_planned()
        route = self._route if next_planned is None else self._route[: next_planned[0]]
        return [symbol for symbol in route if isinstance(symbol, NonTerminal)]

    def follow(self, new_messages: list[DerivationTree]) -> Optional[Deviation]:
        """Consumes the messages that arrive as planned; returns the first one that deviates, if any."""
        for message in new_messages:
            assert isinstance(message.symbol, NonTerminal)
            arrived = PacketNonTerminal(
                message.sender, message.recipient, message.symbol
            )
            next_planned = self._next_planned()
            if next_planned is not None and next_planned[1].packet == arrived:
                self._route = self._route[next_planned[0] + 1 :]
                continue
            planned_packet = None if next_planned is None else next_planned[1]
            if self._consume_permutation_peer(planned_packet, arrived):
                continue
            return Deviation(planned_packet, message)
        return None

    def _next_planned(self) -> Optional[tuple[int, PlannedPacket]]:
        """The next planned packet and its index in the route."""
        for index, planned_packet in enumerate(self._route):
            if isinstance(planned_packet, PlannedPacket):
                return index, planned_packet
        return None

    def _consume_permutation_peer(
        self, planned: Optional[PlannedPacket], arrived: PacketNonTerminal
    ) -> bool:
        """Removes the arrived packet from the route if it is a permutation peer of the planned packet arriving out of order."""
        if (
            planned is None
            or planned.packet.symbol not in self._permutation_groups
            or arrived.symbol not in self._permutation_groups[planned.packet.symbol]
        ):
            return False
        for index, symbol in enumerate(self._route):
            if isinstance(symbol, PlannedPacket) and symbol.packet == arrived:
                del self._route[index]
                return True
        return False

    def __repr__(self) -> str:
        return f"GuidePathTracker(route={self._route!r}, target_step={self._target_step!r})"
