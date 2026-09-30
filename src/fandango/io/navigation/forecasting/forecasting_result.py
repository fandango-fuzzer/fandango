from __future__ import annotations

from typing import Any, Optional

from fandango.errors import FandangoValueError
from fandango.io.navigation.step import Step
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class MountingPath:
    def __init__(
        self,
        tree: DerivationTree,
        controlflow_path: tuple[tuple[NonTerminal, bool], ...],
    ):
        """
        Represents a path in the given DerivationTree where a protocol message can be mounted.
        """
        self.tree = tree
        self.controlflow_path = controlflow_path
        self.path: tuple[tuple[NonTerminal, bool], ...] = MountingPath._collapsed_path(
            controlflow_path
        )

    @staticmethod
    def _collapsed_path(
        path: tuple[tuple[NonTerminal, bool], ...],
    ) -> tuple[tuple[NonTerminal, bool], ...]:
        return tuple(
            (nt, new_node) for nt, new_node in path if not nt.name().startswith("<__")
        )

    def __hash__(self) -> int:
        return hash((hash(self.tree), hash(self.path)))

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return f"({', '.join([f'({nt.format_as_spec()}, {new_node})' for nt, new_node in self.path])})"


class ForecastingPacket:
    def __init__(self, node: NonTerminalNode):
        self.node = node
        self.paths: set[MountingPath] = set()

    def add_path(self, path: MountingPath) -> None:
        self.paths.add(path)


class ForecastingNonTerminals:
    def __init__(self) -> None:
        self.nt_to_packet = dict[NonTerminal, ForecastingPacket]()

    def get_non_terminals(self) -> set[NonTerminal]:
        return set(self.nt_to_packet.keys())

    def __getitem__(self, item: NonTerminal) -> ForecastingPacket:
        return self.nt_to_packet[item]

    def add_packet(self, packet: ForecastingPacket) -> None:
        """
        Adds a packet to the ForcastingNonTerminals.
        """
        if packet.node.symbol in self.nt_to_packet.keys():
            for path in packet.paths:
                self.nt_to_packet[packet.node.symbol].add_path(path)
        else:
            self.nt_to_packet[packet.node.symbol] = packet


class ForecastingResult:
    def __init__(self) -> None:
        self.parties_to_packets = dict[str, ForecastingNonTerminals]()
        self.complete_trees = set[DerivationTree]()
        self.message_steps = list[set[Step]]()

    def get_msg_parties(self) -> set[str]:
        return set(self.parties_to_packets.keys())

    def __getitem__(self, item: str) -> ForecastingNonTerminals:
        return self.parties_to_packets[item]

    def __contains__(self, item: str) -> bool:
        return item in self.parties_to_packets

    def add_packet(self, party: Optional[str], packet: ForecastingPacket) -> None:
        """
        Adds a packet to the ForecastingResult under the specified party.
        """
        if party is None:
            raise FandangoValueError("Party cannot be None")
        if party not in self.parties_to_packets.keys():
            self.parties_to_packets[party] = ForecastingNonTerminals()
        self.parties_to_packets[party].add_packet(packet)

    def union(self, other: ForecastingResult) -> ForecastingResult:
        """
        Merge ``other`` into this result in place and return ``self``.
        :param other: The other ForecastingResult to combine with.
        """
        for party, fnt in other.parties_to_packets.items():
            for fp in fnt.nt_to_packet.values():
                self.add_packet(party, fp)
        self.complete_trees.update(other.complete_trees)
        return self
