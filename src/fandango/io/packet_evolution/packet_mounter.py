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


class MessageHolders:
    """The nodes of a tree that have session messages as children."""

    def __init__(self, root: DerivationTree):
        self.root = root
        self._holder_message_pairs: list[tuple[DerivationTree, DerivationTree]] = []
        pending = [root]
        while pending:
            node = pending.pop()
            for child in node.children:
                if child.sender is None:
                    pending.append(child)
                else:
                    self._holder_message_pairs.append((node, child))

    def hold_messages(self) -> None:
        """Makes these nodes the parents of their messages again."""
        for holder, message in self._holder_message_pairs:
            message.parent = holder


class PacketMounter:
    """Mounts candidate packets into skeletons, one per mounting path, built around the session's messages.
    An attached packet has its mount point as parent but is not among its children."""

    def __init__(self, grammar: Grammar, start_symbol: str):
        self._grammar = grammar
        self._session_message_holders = MessageHolders(
            DerivationTree(NonTerminal(start_symbol))
        )
        self._active_message_holders = self._session_message_holders
        self._message_holders_by_root_id: dict[int, MessageHolders] = {}
        self._mount_points_by_mounting_path: dict[MountingPath, DerivationTree] = {}
        self._first_mounted_packets_by_root_hash: dict[int, DerivationTree] = {}

    @contextmanager
    def session_context(self, session_tree: DerivationTree) -> Iterator[None]:
        """Builds skeletons around the session tree's messages during the block.
        Afterwards the messages hang in the session tree, or in the tree of the committed packet."""
        self._start_session(session_tree)
        try:
            yield
        finally:
            self._hold_messages_in(self._session_message_holders.root)

    def fuzz_attached(
        self, packet: ForecastingPacket, mounting_path: MountingPath, max_nodes: int
    ) -> DerivationTree:
        """Fuzzes a new packet at the mounting path's mount point and returns it attached."""
        mount_point = self._mount_point(mounting_path)
        self._hold_messages_in(mount_point.get_root())
        packet.node.fuzz(mount_point, self._grammar, max_nodes)
        fuzzed_packet = mount_point.children[-1]
        self._unmount(fuzzed_packet)
        return fuzzed_packet

    def attach(self, tree: DerivationTree, mounting_path: MountingPath) -> None:
        """Attaches the tree at the mounting path's mount point; it no longer serves as first equal packet."""
        self._first_mounted_packets_by_root_hash = {
            root_hash: first_equal_packet
            for root_hash, first_equal_packet in self._first_mounted_packets_by_root_hash.items()
            if first_equal_packet is not tree
        }
        mount_point = self._mount_point(mounting_path)
        mount_point.add_child(tree)
        self._unmount(tree)

    @contextmanager
    def mounted_context(self, packet: DerivationTree) -> Iterator[DerivationTree]:
        """Mounts the first equal packet in place of the attached packet during the block and yields it; others come back unchanged.
        Packets mount into skeletons, never the session tree; with several mounted, the messages hang in the last one's skeleton."""
        if not self._is_attached(packet):
            yield packet
            return
        first_equal_packet = self._mount_first_equal(packet)
        try:
            yield first_equal_packet
        finally:
            self._unmount(first_equal_packet)

    def commit(self, packet: DerivationTree) -> DerivationTree:
        """Mounts the packet for good and returns its tree, which becomes the session tree."""
        if self._is_attached(packet):
            self._mount(packet)
        session_tree = packet.get_root()
        self._start_session(session_tree)
        return session_tree

    def _start_session(self, session_tree: DerivationTree) -> None:
        """Drops all skeletons and first equal packets and hangs the messages into the session tree."""
        self._mount_points_by_mounting_path.clear()
        self._first_mounted_packets_by_root_hash.clear()
        self._message_holders_by_root_id.clear()
        self._session_message_holders = self._message_holders(session_tree)
        self._active_message_holders = self._session_message_holders
        self._session_message_holders.hold_messages()

    def _mount_first_equal(self, packet: DerivationTree) -> DerivationTree:
        """Mounts the first packet seen with an equal mounted tree and returns it,
        or mounts and returns the packet itself while that first packet is mounted."""
        self._mount(packet)
        root_hash = hash(packet.get_root())
        first_equal_packet = self._first_mounted_packets_by_root_hash.setdefault(
            root_hash, packet
        )
        if first_equal_packet is packet or not self._is_attached(first_equal_packet):
            return packet
        self._unmount(packet)
        self._mount(first_equal_packet)
        return first_equal_packet

    def _mount(self, packet: DerivationTree) -> None:
        """Hangs the session's messages into the packet's skeleton and adds the packet to its mount point's children."""
        mount_point = packet.parent
        assert mount_point is not None
        self._hold_messages_in(mount_point.get_root())
        mount_point.add_child(packet)

    @staticmethod
    def _unmount(packet: DerivationTree) -> None:
        """Removes the packet from its mount point's children; its parent pointer stays."""
        mount_point = packet.parent
        assert mount_point is not None
        mount_point.set_children(
            [child for child in mount_point.children if child is not packet]
        )

    @staticmethod
    def _is_attached(tree: DerivationTree) -> bool:
        """True if the tree has a parent that does not list it among its children."""
        mount_point = tree.parent
        return mount_point is not None and not any(
            child is tree for child in mount_point.children
        )

    def _hold_messages_in(self, root: DerivationTree) -> None:
        """Hangs the session's messages into the tree under root."""
        if root is self._active_message_holders.root:
            return
        self._active_message_holders = self._message_holders(root)
        self._active_message_holders.hold_messages()

    def _message_holders(self, root: DerivationTree) -> MessageHolders:
        """Returns the message holders of the tree under root, found once per session."""
        if id(root) not in self._message_holders_by_root_id:
            self._message_holders_by_root_id[id(root)] = MessageHolders(root)
        return self._message_holders_by_root_id[id(root)]

    def _mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """Returns the mounting path's mount point, built once per session."""
        if mounting_path not in self._mount_points_by_mounting_path:
            self._mount_points_by_mounting_path[mounting_path] = (
                self._build_mount_point(mounting_path)
            )
        return self._mount_points_by_mounting_path[mounting_path]

    def _build_mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """Builds a read-only skeleton of the mounting path's tree around the session's messages
        and returns the node packets are appended to."""
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
        self._active_message_holders = self._message_holders(skeleton)
        return mount_point

    def _replace_message_copies(
        self, skeleton: DerivationTree, mounting_path: MountingPath
    ) -> None:
        """Swaps the message copies in the skeleton for the session's messages.
        Raises if the mounting path's tree holds other messages than the session."""
        session_messages = [
            message.msg
            for message in self._session_message_holders.root.protocol_msgs()
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

    @staticmethod
    def _set_read_only_above_messages(skeleton: DerivationTree) -> None:
        """Sets the skeleton's nodes above the messages read-only."""
        pending = [skeleton]
        while pending:
            node = pending.pop()
            node.read_only = True
            if node.sender is None:
                pending.extend(node.children)
                pending.extend(node.sources)
