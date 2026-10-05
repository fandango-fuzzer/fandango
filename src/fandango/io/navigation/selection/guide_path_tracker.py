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

    def set_guide_path(
        self,
        guide_path: GuidePath,
    ) -> None:
        """Sets the route to follow, with the step into its target, if any."""
        self._route = list(guide_path.route)
        self._target_step = guide_path.target_step

    @property
    def target_step(self) -> Optional[Step]:
        """The step into the target; a party refuses it by answering otherwise after the route."""
        return self._target_step

    def clear(self) -> None:
        self._route = []
        self._target_step = None

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

    def follow(self, message: DerivationTree, steps: set[Step]) -> Optional[Deviation]:
        """
        Consumes the message if it arrives as planned; returns the deviation otherwise.
        After the last planned packet, the message follows the plan if one of its steps, the steps that may have produced it, lies inside the target.
        """
        assert isinstance(message.symbol, NonTerminal)
        arrived = PacketNonTerminal(message.sender, message.recipient, message.symbol)
        next_planned = self._next_planned()
        if next_planned is not None and next_planned[1].packet == arrived:
            self._route = self._route[next_planned[0] + 1 :]
            return None
        planned_packet = None if next_planned is None else next_planned[1]
        if self._consume_permutation_peer(planned_packet, arrived):
            return None
        if next_planned is None:
            path_into_target = self._route_state_tail()
            if any(self._is_step_in_target(step, path_into_target) for step in steps):
                # The message reached the target, so the plan is done.
                self._route = []
                return None
        return Deviation(planned_packet, message)

    @staticmethod
    def _is_step_in_target(
        step: Step, path_into_target: tuple[NonTerminal, ...]
    ) -> bool:
        if not path_into_target:
            return False
        *above_target, target = path_into_target
        rules = [
            symbol for symbol in step.path[:-1] if not Step.is_control_flow(symbol)
        ]
        if target not in rules:
            return False
        at_target = len(rules) - 1 - rules[::-1].index(target)
        # The step only reaches up to the caller of its nearest recursive call.
        overlap = min(at_target, len(above_target))
        return (
            rules[at_target - overlap : at_target]
            == above_target[len(above_target) - overlap :]
        )

    def _route_state_tail(self) -> tuple[NonTerminal, ...]:
        """The NonTerminals tailing self._route after the last PlannedPacket."""
        entered: list[NonTerminal] = []
        for symbol in reversed(self._route):
            if not isinstance(symbol, NonTerminal):
                break
            entered.append(symbol)
        return tuple(reversed(entered))

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
