from typing import NamedTuple, Optional

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.step import Step, to_packet_step
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree

GuidePathSymbol = PacketNonTerminal | NonTerminal | None
"""A state, a packet, or None. (None marks the end of a session.)"""


class Deviation(NamedTuple):
    """A message that did not follow the guide path."""

    planned_packet: Optional[PacketNonTerminal]
    message: DerivationTree
    planned_step: Optional[Step]


class GuidePathTracker:
    """
    Tracks the planned route, give the next packet to produce, and detects derivations from
    the given path.
    """

    def __init__(self, permutation_groups: dict[NonTerminal, frozenset[NonTerminal]]):
        self._permutation_groups = permutation_groups
        self._symbols: list[GuidePathSymbol] = []
        self._parent_of_last_packet: Optional[NonTerminal] = None

    def set_route(
        self,
        symbols: list[GuidePathSymbol],
        parent_of_last_packet: Optional[NonTerminal] = None,
    ) -> None:
        """Sets the given route as the route to follow."""
        self._symbols = list(symbols)
        self._parent_of_last_packet = parent_of_last_packet

    def clear(self) -> None:
        self.set_route([])

    @property
    def symbols(self) -> list[GuidePathSymbol]:
        return list(self._symbols)

    @property
    def is_empty(self) -> bool:
        return len(self._symbols) == 0

    @property
    def ends_run(self) -> bool:
        """True if the route leads to the end of the run."""
        return None in self._symbols

    def next_packet(self) -> Optional[PacketNonTerminal]:
        return next(
            (x for x in self._symbols if isinstance(x, PacketNonTerminal)), None
        )

    def next_new_parent_states(self) -> list[Symbol]:
        """
        Parent states of the next packet that are not yet in the session tree.
        All states along the route if no packet is left.
        """
        next_packet = self.next_packet()
        if next_packet is None:
            route = self._symbols
        else:
            route = self._symbols[: self._symbols.index(next_packet)]
        return [symbol for symbol in route if isinstance(symbol, NonTerminal)]

    def follow(self, new_messages: list[DerivationTree]) -> Optional[Deviation]:
        """Consumes the messages that arrive as planned; returns the first one that deviates, if any."""
        for message in new_messages:
            planned_packet = self.next_packet()
            planned_step = self._producing_step(planned_packet)
            if planned_packet is None or planned_packet.symbol != message.symbol:
                if self._consume_permutation_peer(planned_packet, message):
                    continue
                return Deviation(planned_packet, message, planned_step)
            if planned_step is not None:
                self._parent_of_last_packet = planned_step[0]
            self._symbols = self._symbols[self._symbols.index(planned_packet) + 1 :]
        return None

    def _consume_permutation_peer(
        self, planned_packet: Optional[PacketNonTerminal], message: DerivationTree
    ) -> bool:
        """Removes the message from the route if it is a permutation peer of the planned packet arriving out of order."""
        assert isinstance(message.symbol, NonTerminal)
        if (
            planned_packet is None
            or planned_packet.symbol not in self._permutation_groups
            or message.symbol not in self._permutation_groups[planned_packet.symbol]
        ):
            return False
        peer = PacketNonTerminal(message.sender, message.recipient, message.symbol)
        if peer not in self._symbols:
            return False
        index = self._symbols.index(peer)
        self._symbols = self._symbols[:index] + self._symbols[index + 1 :]
        return True

    def _producing_step(
        self, packet_nonterminal: Optional[PacketNonTerminal]
    ) -> Optional[Step]:
        """The step that produces this given packet on the current route"""
        if packet_nonterminal is None:
            return None
        planned = self._symbols[: self._symbols.index(packet_nonterminal)]
        if None in planned:
            planned = planned[len(planned) - planned[::-1].index(None) :]
        parent = planned[-1] if len(planned) > 0 else self._parent_of_last_packet
        if parent is None:
            return None
        assert isinstance(parent, NonTerminal)
        return to_packet_step(parent, packet_nonterminal.symbol)
