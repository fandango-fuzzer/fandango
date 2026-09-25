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


class PacketMounter:
    """Mounts candidate packets into a read-only copy of the session tree.
    An attached packet has its mount point as parent but is not among its children until mounted."""

    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self._mount_points_by_mounting_path: dict[MountingPath, DerivationTree] = {}
        self._first_seen_packets_by_root_hash: dict[int, DerivationTree] = {}

    def clear(self) -> None:
        """Drops all mount points and first seen packets; needed whenever the session tree changes."""
        self._mount_points_by_mounting_path.clear()
        self._first_seen_packets_by_root_hash.clear()

    def fuzz_attached(
        self, packet: ForecastingPacket, mounting_path: MountingPath, max_nodes: int
    ) -> DerivationTree:
        """Fuzzes a new packet at the mount point of the mounting path and returns it attached."""
        mount_point = self._mount_point(packet, mounting_path)
        packet.node.fuzz(mount_point, self._grammar, max_nodes)
        fuzzed_packet = mount_point.children[-1]
        self._unmount(fuzzed_packet)
        return fuzzed_packet

    def attach(
        self,
        tree: DerivationTree,
        packet: ForecastingPacket,
        mounting_path: MountingPath,
    ) -> None:
        """Attaches an existing tree to the mount point of the mounting path."""
        mount_point = self._mount_point(packet, mounting_path)
        mount_point.add_child(tree)
        self._unmount(tree)

    @contextmanager
    def mount_context(self, *trees: DerivationTree) -> Iterator[None]:
        """Mounts the attached trees for the duration of the block, then unmounts them."""
        attached_packets: list[DerivationTree] = []
        for tree in trees:
            if self.is_unmounted(tree) and not any(
                tree is packet for packet in attached_packets
            ):
                attached_packets.append(tree)
        for packet in attached_packets:
            assert packet.parent is not None
            packet.parent.add_child(packet)
        try:
            yield
        finally:
            for packet in attached_packets:
                self._unmount(packet)

    def mount(self, tree: DerivationTree) -> DerivationTree:
        """Mounts an attached tree for good and returns the session tree now holding it."""
        if self.is_unmounted(tree):
            assert tree.parent is not None
            tree.parent.add_child(tree)
        return tree.get_root()

    def first_seen_equal(self, tree: DerivationTree) -> DerivationTree:
        """Returns the first tree passed here that, mounted, gave an equal session tree.
        On the first call for a structure that is the tree itself; unmounted trees come back unchanged."""
        if not self.is_unmounted(tree):
            return tree
        with self.mount_context(tree):
            root_hash = hash(tree.get_root())
        return self._first_seen_packets_by_root_hash.setdefault(root_hash, tree)

    @staticmethod
    def is_unmounted(tree: DerivationTree) -> bool:
        """A tree is unmounted when it has a parent that does not list it as child."""
        mount_point = tree.parent
        return mount_point is not None and not any(
            child is tree for child in mount_point.children
        )

    def _mount_point(
        self, packet: ForecastingPacket, mounting_path: MountingPath
    ) -> DerivationTree:
        """Returns the node a packet is appended to in a read-only copy of the session tree,
        built once per mounting path until the next clear."""
        if mounting_path not in self._mount_points_by_mounting_path:
            session_tree = self._grammar.collapse(mounting_path.tree)
            if session_tree is None:
                raise FandangoValueError(
                    f"Could not collapse tree for {mounting_path.path} in packet {packet.node}"
                )
            session_tree.set_all_read_only(True)
            hookin = DerivationTree(NonTerminal("<hookin>"))
            session_tree.append(
                mounting_path.path[1:-1], hookin, read_only_new_nodes=True
            )
            mount_point = hookin.parent
            assert mount_point is not None
            self._unmount(hookin)
            self._mount_points_by_mounting_path[mounting_path] = mount_point
        return self._mount_points_by_mounting_path[mounting_path]

    @staticmethod
    def _unmount(packet: DerivationTree) -> None:
        """Removes the packet from its mount point's children but keeps its parent pointer."""
        mount_point = packet.parent
        assert mount_point is not None
        mount_point.set_children(
            [child for child in mount_point.children if child is not packet]
        )
