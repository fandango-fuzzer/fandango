from collections.abc import Iterator
from contextlib import contextmanager

from fandango.errors import FandangoValueError
from fandango.io.navigation.graph.packetforecaster import (
    ForecastingPacket,
    MountingPath,
)
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class PacketMounting:
    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self._anchors_by_option: dict[MountingPath, DerivationTree] = {}
        self._canonical_packets_by_root_hash: dict[int, DerivationTree] = {}

    def forget(self) -> None:
        self._anchors_by_option.clear()
        self._canonical_packets_by_root_hash.clear()

    def fuzz_detached_packet(
        self, packet: ForecastingPacket, mounting_option: MountingPath, max_nodes: int
    ) -> DerivationTree:
        anchor = self._anchor(packet, mounting_option)
        packet.node.fuzz(anchor, self._grammar, max_nodes)
        fuzzed_packet = anchor.children[-1]
        self._detach(fuzzed_packet)
        return fuzzed_packet

    @contextmanager
    def mounted(self, *trees: DerivationTree) -> Iterator[None]:
        packets: list[DerivationTree] = []
        for tree in trees:
            if self.is_detached(tree) and not any(tree is packet for packet in packets):
                packets.append(tree)
        for packet in packets:
            assert packet.parent is not None
            packet.parent.add_child(packet)
        try:
            yield
        finally:
            for packet in packets:
                self._detach(packet)

    def attach(self, tree: DerivationTree) -> DerivationTree:
        if self.is_detached(tree):
            assert tree.parent is not None
            tree.parent.add_child(tree)
        return tree.get_root()

    def canonical(self, packet: DerivationTree) -> DerivationTree:
        if not self.is_detached(packet):
            return packet
        with self.mounted(packet):
            root_hash = hash(packet.get_root())
        return self._canonical_packets_by_root_hash.setdefault(root_hash, packet)

    @staticmethod
    def is_detached(tree: DerivationTree) -> bool:
        anchor = tree.parent
        return anchor is not None and not any(
            child is tree for child in anchor.children
        )

    def _anchor(
        self, packet: ForecastingPacket, mounting_option: MountingPath
    ) -> DerivationTree:
        if mounting_option not in self._anchors_by_option:
            session_tree = self._grammar.collapse(mounting_option.tree)
            if session_tree is None:
                raise FandangoValueError(
                    f"Could not collapse tree for {mounting_option.path} in packet {packet.node}"
                )
            session_tree.set_all_read_only(True)
            hookin = DerivationTree(NonTerminal("<hookin>"))
            session_tree.append(
                mounting_option.path[1:-1], hookin, read_only_new_nodes=True
            )
            anchor = hookin.parent
            assert anchor is not None
            self._detach(hookin)
            self._anchors_by_option[mounting_option] = anchor
        return self._anchors_by_option[mounting_option]

    @staticmethod
    def _detach(packet: DerivationTree) -> None:
        anchor = packet.parent
        assert anchor is not None
        anchor.set_children([child for child in anchor.children if child is not packet])
