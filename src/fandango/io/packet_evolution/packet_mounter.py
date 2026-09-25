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
    """Mounts candidate packets into one skeleton per mounting path, all built around the session's messages.
    An attached packet has its mount point as parent but is not among its children until mounted.
    A message has one parent pointer, so the messages move into a skeleton before a packet is mounted there."""

    def __init__(self, grammar: Grammar, start_symbol: str):
        self._grammar = grammar
        self._session_tree = DerivationTree(NonTerminal(start_symbol))
        self._session_messages_holder = self._session_tree
        self._mount_points_by_mounting_path: dict[MountingPath, DerivationTree] = {}
        self._first_seen_packets_by_root_hash: dict[int, DerivationTree] = {}

    def reset(self, session_tree: DerivationTree) -> None:
        """Drops all mount points and first seen packets and builds new skeletons around the messages
        of the session tree from now on; needed whenever the session tree changes."""
        self._mount_points_by_mounting_path.clear()
        self._first_seen_packets_by_root_hash.clear()
        self._session_tree = session_tree
        self._move_session_messages_to(session_tree)

    def fuzz_attached(
        self, packet: ForecastingPacket, mounting_path: MountingPath, max_nodes: int
    ) -> DerivationTree:
        """Fuzzes a new packet at the mount point of the mounting path and returns it attached."""
        mount_point = self._mount_point(mounting_path)
        self._move_session_messages_to(mount_point.get_root())
        packet.node.fuzz(mount_point, self._grammar, max_nodes)
        fuzzed_packet = mount_point.children[-1]
        self._unmount(fuzzed_packet)
        return fuzzed_packet

    def attach(self, tree: DerivationTree, mounting_path: MountingPath) -> None:
        """Attaches an existing tree to the mount point of the mounting path."""
        mount_point = self._mount_point(mounting_path)
        mount_point.add_child(tree)
        self._unmount(tree)

    @contextmanager
    def mount_context(self, *trees: DerivationTree) -> Iterator[None]:
        """Mounts the attached trees for the duration of the block, then unmounts them.
        The session's messages move into the skeleton of the last attached tree."""
        mounted_packets: list[DerivationTree] = []
        for tree in trees:
            if self.is_unmounted(tree):
                self.mount(tree)
                mounted_packets.append(tree)
        try:
            yield
        finally:
            for packet in mounted_packets:
                self._unmount(packet)

    def mount(self, tree: DerivationTree) -> DerivationTree:
        """Mounts an attached tree and returns the session tree now holding it."""
        if self.is_unmounted(tree):
            assert tree.parent is not None
            self._move_session_messages_to(tree.get_root())
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

    def _mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """Returns the mount point of the mounting path, built on first use after a reset."""
        if mounting_path not in self._mount_points_by_mounting_path:
            self._mount_points_by_mounting_path[mounting_path] = (
                self._build_mount_point(mounting_path)
            )
        return self._mount_points_by_mounting_path[mounting_path]

    def _build_mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """Builds a read-only skeleton of the mounting path's tree that holds the session's messages
        and returns the node in it that packets are appended to."""
        skeleton = self._grammar.collapse(mounting_path.tree)
        if skeleton is None:
            raise FandangoValueError(
                f"Could not collapse tree for {mounting_path.path}"
            )
        self._replace_message_copies(skeleton, mounting_path)
        self._set_read_only_above_messages(skeleton)
        hookin = DerivationTree(NonTerminal("<hookin>"))
        skeleton.append(mounting_path.path[1:-1], hookin, read_only_new_nodes=True)
        mount_point = hookin.parent
        assert mount_point is not None
        self._unmount(hookin)
        return mount_point

    def _replace_message_copies(
        self, skeleton: DerivationTree, mounting_path: MountingPath
    ) -> None:
        """Replaces the message copies in the skeleton by the session's messages, which move into it.
        Raises if the mounting path's tree holds other messages than the session."""
        session_messages = [
            message.msg for message in self._session_tree.protocol_msgs()
        ]
        forecast_messages = [
            message.msg for message in mounting_path.tree.protocol_msgs()
        ]
        if forecast_messages != session_messages:
            raise FandangoValueError(
                f"Mounting path {mounting_path.path} holds other messages than the session"
            )
        message_copies = [message.msg for message in skeleton.protocol_msgs()]
        session_message_by_copy_id = {
            id(message_copy): session_message
            for message_copy, session_message in zip(
                message_copies, session_messages, strict=True
            )
        }
        parents_of_copies = {
            id(message_copy.parent): message_copy.parent
            for message_copy in message_copies
        }
        for parent in parents_of_copies.values():
            assert parent is not None
            parent.set_children(
                [
                    session_message_by_copy_id.get(id(child), child)
                    for child in parent.children
                ]
            )
        self._session_messages_holder = skeleton

    def _move_session_messages_to(self, root: DerivationTree) -> None:
        """Points the parents of the session's messages into the tree under root, unless they are there already."""
        if root is self._session_messages_holder:
            return
        pending = [root]
        while pending:
            node = pending.pop()
            if node.sender is not None:
                continue
            if any(child.sender is not None for child in node.children):
                node.set_children(node.children)
            pending.extend(node.children)
        self._session_messages_holder = root

    @staticmethod
    def _set_read_only_above_messages(skeleton: DerivationTree) -> None:
        """Sets the skeleton's nodes above the messages read-only; the messages already are."""
        pending = [skeleton]
        while pending:
            node = pending.pop()
            node.read_only = True
            if node.sender is None:
                pending.extend(node.children)
                pending.extend(node.sources)

    @staticmethod
    def _unmount(packet: DerivationTree) -> None:
        """Removes the packet from its mount point's children but keeps its parent pointer."""
        mount_point = packet.parent
        assert mount_point is not None
        mount_point.set_children(
            [child for child in mount_point.children if child is not packet]
        )
