from collections.abc import Iterator
from contextlib import contextmanager

from fandango.errors import FandangoValueError
from fandango.io.navigation.forecasting.forecasting_result import MountingPath
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
        for message_copy, message in zip(
            message_copies, self.root.protocol_msgs(), strict=False
        ):
            parent = message_copy.parent
            assert parent is not None
            children = list(parent.children)
            index = index_by_reference(children, message_copy)
            assert index is not None
            children[index] = message.msg
            parent.set_children(children)


class PacketMounter:
    """
    Puts candidate packets into copies of the session tree, so each can be evaluated and changed in the context of the whole session.

    The history is the session tree so far. A mounting path, found by the forecaster, is a forecast tree,
    which holds copies of the history's messages, and the path in it where a new packet can go.
    For each mounting path, the mounter builds a skeleton once per history: a read-only copy of the forecast tree
    with the history's message nodes in it and a mount point, the node new packets go under.

    A packet is in one of these states:

    Free: the packet is not connected to any tree. Its parent is None.
        Example: a received packet before attach. mounted_context yields a free packet unchanged.
    Attached: the packet knows its place in a skeleton but is not part of the skeleton's tree.
        The packet's parent is set to the mount point, but the mount point's children do not point to the packet.
        So get_root reaches the skeleton's root, but that tree does not contain the packet.
        Many packets can be attached to one mount point at once; population packets stay in this state.
        attach puts a packet into this state, also one fuzzed under mount_point, and mounted_context brings a packet back to it.
    Mounted: the packet is part of the skeleton's tree.
        The packet's parent is set to the mount point, and the mount point's children point to the packet as the last child.
        The skeleton's root is then the whole tree: the history's messages plus this packet.
    History: the packet is part of the new history.
        commit mounts the packet and makes the skeleton's root the new history. The packet stays among the mount point's
        children and is now a message of the history. All skeletons of the old history are dropped.
    """

    def __init__(self, grammar: Grammar, start_symbol: str | NonTerminal):
        if isinstance(start_symbol, str):
            start_symbol_nt = NonTerminal(start_symbol)
        else:
            start_symbol_nt = start_symbol
        self._grammar = grammar
        self._history_message_holders = MessageHolder(DerivationTree(start_symbol_nt))
        self._active_message_holders = self._history_message_holders
        self._message_holders_of_trees: list[MessageHolder] = []
        self._mount_points_by_mounting_path: dict[MountingPath, DerivationTree] = {}
        self._first_mounted_packets_by_root_hash: dict[int, DerivationTree] = {}
        self._mounted_and_original_packets: list[
            tuple[DerivationTree, DerivationTree]
        ] = []

    @contextmanager
    def history_context(self, history: DerivationTree) -> Iterator[None]:
        """
        Makes the history the base of new skeletons and drops all skeletons built before.
        After the block, even on error, points the messages' parents back into the history.
        """
        self._set_history(history)
        try:
            yield
        finally:
            self._hold_messages_in(self._history_message_holders.root)

    def mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """
        Appends the requested path to the DerivationTree, adds parsed messages to it,
        and returns the position in that tree, that would hold the packet at the position of `mounting_path`.
        """
        mount_point = self._mount_point(mounting_path)
        self._hold_messages_in(mount_point.get_root())
        return mount_point

    def attach(self, tree: DerivationTree, mounting_path: MountingPath) -> None:
        """
        Attaches an existing packet, at the mounting path's mount point; a packet already under the mount point is taken out of its children.
        It stops being a stand-in for equal packets, since at another mount point its whole tree differs.
        """
        self._first_mounted_packets_by_root_hash = {
            root_hash: first_equal_packet
            for root_hash, first_equal_packet in self._first_mounted_packets_by_root_hash.items()
            if first_equal_packet is not tree
        }
        mount_point = self._mount_point(mounting_path)
        if index_by_reference(mount_point.children, tree) is None:
            mount_point.add_child(tree)
        self._unmount(tree)

    @contextmanager
    def mounted_context(self, packet: DerivationTree) -> Iterator[DerivationTree]:
        """
        Yields the mounted packet. A stand-in is used only if it is not mounted right now.
        It is needed because for an equal whole tree the fitness cache returns failing trees in the stand-in,
        and operators can only change nodes of the mounted tree.
        A packet that is already mounted, such as by an outer mounted_context, is yielded unchanged.
        With several packets mounted, only the last one's skeleton holds the messages.
        """
        if not self._is_attached(packet):
            yield packet
            return
        first_equal_packet = self._mount_first_equal(packet)
        self._mounted_and_original_packets.append((first_equal_packet, packet))
        try:
            yield first_equal_packet
        finally:
            mounted_packet, _original = self._mounted_and_original_packets.pop()
            assert mounted_packet is first_equal_packet
            self._unmount(first_equal_packet)

    def original(self, packet: DerivationTree) -> DerivationTree:
        """
        Returns any packet that is not a stand-in unchanged.
        Call it on an operator's result inside mounted_context, so a stand-in never ends up in the population.
        """
        for mounted_packet, original_packet in self._mounted_and_original_packets:
            if mounted_packet is packet:
                return original_packet
        return packet

    def commit(self, packet: DerivationTree) -> DerivationTree:
        """
        Takes a packet and makes the entire DerivationTree (packet.get_root()) the new history
        from there on.
        """
        if self._is_attached(packet):
            self._mount(packet)
        history = packet.get_root()
        self._set_history(history)
        return history

    def _set_history(self, history: DerivationTree) -> None:
        """Makes the tree the new history: forgets everything built for the old one and points the messages' parents into the new history."""
        self._mount_points_by_mounting_path.clear()
        self._first_mounted_packets_by_root_hash.clear()
        self._message_holders_of_trees.clear()
        self._history_message_holders = self._message_holders(history)
        self._active_message_holders = self._history_message_holders
        self._history_message_holders.hold_messages()

    def _mount_first_equal(self, packet: DerivationTree) -> DerivationTree:
        """
        Mounts and returns the packet's stand-in.
        Mounts and returns the packet itself if it is the first with its whole tree or its stand-in is mounted right now.
        """
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
        """Mounts an attached packet and points the messages' parents into its skeleton."""
        mount_point = packet.parent
        assert mount_point is not None
        self._hold_messages_in(mount_point.get_root())
        mount_point.add_child(packet)

    @staticmethod
    def _unmount(packet: DerivationTree) -> None:
        """Turns a mounted packet back into an attached one."""
        mount_point = packet.parent
        assert mount_point is not None
        packet_index = index_by_reference(mount_point.children, packet)
        assert packet_index is not None
        mount_point.remove_child(index=packet_index)
        packet.parent = mount_point

    @staticmethod
    def _is_attached(tree: DerivationTree) -> bool:
        """True if the tree is attached."""
        mount_point = tree.parent
        return mount_point is not None and not any(
            child is tree for child in mount_point.children
        )

    def _hold_messages_in(self, root: DerivationTree) -> None:
        """Points the messages' parents into the tree under root; does nothing if they already point there."""
        if root is self._active_message_holders.root:
            return
        self._active_message_holders = self._message_holders(root)
        self._active_message_holders.hold_messages()

    def _message_holders(self, root: DerivationTree) -> MessageHolder:
        """Returns where the tree under root holds the messages; searches each tree once per history."""
        for message_holders in self._message_holders_of_trees:
            if message_holders.root is root:
                return message_holders
        message_holders = MessageHolder(root)
        self._message_holders_of_trees.append(message_holders)
        return message_holders

    def _mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """Returns the mounting path's mount point, building its skeleton on first use."""
        if mounting_path not in self._mount_points_by_mounting_path:
            self._mount_points_by_mounting_path[mounting_path] = (
                self._build_mount_point(mounting_path)
            )
        return self._mount_points_by_mounting_path[mounting_path]

    def _build_mount_point(self, mounting_path: MountingPath) -> DerivationTree:
        """
        Builds the mounting path's skeleton and returns its mount point.
        The nodes along the path down to the mount point are new and read-only too.
        Afterwards the messages' parents point into this skeleton.
        """
        skeleton = self._grammar.collapse(mounting_path.tree)
        if skeleton is None:
            raise FandangoValueError(
                f"Could not collapse tree for {mounting_path.path}"
            )
        self._replace_message_copies(skeleton, mounting_path)
        self._set_skeleton_read_only(skeleton)
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
        """
        Puts the history's message nodes into the skeleton in place of their copies.
        Raises if the forecast tree holds other messages than the history, since messages are swapped by position.
        """
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
    def _set_skeleton_read_only(skeleton: DerivationTree) -> None:
        """Marks every skeleton node outside the messages read-only, the message nodes included; nodes inside the messages stay as they are."""
        pending = [skeleton]
        while pending:
            node = pending.pop()
            node.read_only = True
            if node.sender is None:
                pending.extend(node.children)
                pending.extend(node.sources)
