from collections.abc import Iterator
from contextlib import contextmanager

from fandango.errors import FandangoValueError
from fandango.io.navigation.forecasting.forecasting_result import (
    ForecastingPacket,
    MountingPath,
)
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree, index_by_reference


class MessageHolder:
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

    @contextmanager
    def hold_messages_context(self) -> Iterator["MessageHolder"]:
        """Yields these holders; afterwards they are the parents of their messages again."""
        try:
            yield self
        finally:
            self.hold_messages()

    def hang_messages_into(self, tree: DerivationTree) -> None:
        """Swaps the messages in the tree for the messages under root."""
        message_copies = [message.msg for message in tree.protocol_msgs()]
        message_by_copy_id = {
            id(message_copy): message.msg
            for message_copy, message in zip(
                message_copies, self.root.protocol_msgs(), strict=False
            )
        }
        parents_of_copies = {
            id(message_copy.parent): message_copy.parent
            for message_copy in message_copies
        }
        for parent in parents_of_copies.values():
            assert parent is not None
            parent.set_children(
                [message_by_copy_id.get(id(child), child) for child in parent.children]
            )


class PacketMounter:
    """Mounts candidate packets into skeletons, one per mounting path, built around the history's messages.
    An attached packet has its mount point as parent but is not among its children;
    a mounted packet is among them."""

    def __init__(self, grammar: Grammar, start_symbol: str | NonTerminal):
        if isinstance(start_symbol, str):
            start_symbol_nt = NonTerminal(start_symbol)
        else:
            start_symbol_nt = start_symbol
        self._grammar = grammar
        self._history_message_holders = MessageHolder(
            DerivationTree(start_symbol_nt)
        )
        self._active_message_holders = self._history_message_holders
        self._message_holders_by_root_id: dict[int, MessageHolder] = {}
        self._mount_points_by_mounting_path: dict[MountingPath, DerivationTree] = {}
        self._first_mounted_packets_by_root_hash: dict[int, DerivationTree] = {}
        self._packets_by_mounted_packet_id: dict[int, DerivationTree] = {}

    @contextmanager
    def history_context(self, history: DerivationTree) -> Iterator[None]:
        """Builds skeletons around the history's messages during the block; afterwards the messages hang in the history."""
        self._set_history(history)
        try:
            yield
        finally:
            self._hold_messages_in(self._history_message_holders.root)

    def fuzz(
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
        The first equal packet is mounted because the fitness cache holds failing trees of its nodes.
        Packets mount into skeletons, never the history; with several mounted, the messages hang in the last one's skeleton."""
        if not self._is_attached(packet):
            yield packet
            return
        first_equal_packet = self._mount_first_equal(packet)
        self._packets_by_mounted_packet_id[id(first_equal_packet)] = packet
        try:
            yield first_equal_packet
        finally:
            del self._packets_by_mounted_packet_id[id(first_equal_packet)]
            self._unmount(first_equal_packet)

    def original(self, tree: DerivationTree) -> DerivationTree:
        """Returns the attached packet the tree is mounted in place of, or the tree itself.
        Valid only inside the tree's mounted context."""
        return self._packets_by_mounted_packet_id.get(id(tree), tree)

    def commit(self, packet: DerivationTree) -> DerivationTree:
        """Mounts the packet for good and returns its tree, the next history.
        Call it after the history context."""
        if self._is_attached(packet):
            self._mount(packet)
        history = packet.get_root()
        self._set_history(history)
        return history

    def _set_history(self, history: DerivationTree) -> None:
        """Drops all skeletons and first equal packets and hangs the messages into the history."""
        self._mount_points_by_mounting_path.clear()
        self._first_mounted_packets_by_root_hash.clear()
        self._message_holders_by_root_id.clear()
        self._history_message_holders = self._message_holders(history)
        self._active_message_holders = self._history_message_holders
        self._history_message_holders.hold_messages()

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
        """Hangs the history's messages into the packet's skeleton and adds the packet to its mount point's children."""
        mount_point = packet.parent
        assert mount_point is not None
        self._hold_messages_in(mount_point.get_root())
        mount_point.add_child(packet)

    @staticmethod
    def _unmount(packet: DerivationTree) -> None:
        """Removes the packet from its mount point's children; its parent pointer stays."""
        mount_point = packet.parent
        assert mount_point is not None
        packet_index = index_by_reference(mount_point.children, packet)
        assert packet_index is not None
        mount_point.remove_child(index=packet_index)
        packet.parent = mount_point

    @staticmethod
    def _is_attached(tree: DerivationTree) -> bool:
        """True if the tree has a parent that does not list it among its children."""
        mount_point = tree.parent
        return mount_point is not None and not any(
            child is tree for child in mount_point.children
        )

    def _hold_messages_in(self, root: DerivationTree) -> None:
        """Hangs the history's messages into the tree under root."""
        if root is self._active_message_holders.root:
            return
        self._active_message_holders = self._message_holders(root)
        self._active_message_holders.hold_messages()

    def _message_holders(self, root: DerivationTree) -> MessageHolder:
        """Returns the message holders of the tree under root, found once per history."""
        if id(root) not in self._message_holders_by_root_id:
            self._message_holders_by_root_id[id(root)] = MessageHolder(root)
        return self._message_holders_by_root_id[id(root)]

    def _mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """Returns the mounting path's mount point, built once per history."""
        if mounting_path not in self._mount_points_by_mounting_path:
            self._mount_points_by_mounting_path[mounting_path] = (
                self._build_mount_point(mounting_path)
            )
        return self._mount_points_by_mounting_path[mounting_path]

    def _build_mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """Builds a read-only skeleton of the mounting path's tree around the history's messages
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
        """Swaps the message copies in the skeleton for the history's messages.
        Raises if the mounting path's tree holds other messages than the history."""
        history_messages = [
            message.msg
            for message in self._history_message_holders.root.protocol_msgs()
        ]
        forecast_messages = [
            message.msg for message in mounting_path.tree.protocol_msgs()
        ]
        if forecast_messages != history_messages:
            raise FandangoValueError(
                f"Mounting path {mounting_path.path} holds other messages than the history"
            )
        self._history_message_holders.hang_messages_into(skeleton)

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
