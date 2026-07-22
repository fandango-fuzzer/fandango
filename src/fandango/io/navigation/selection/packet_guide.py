from collections.abc import Callable
from typing import Optional

from fandango.io.navigation.graph.packetforecaster import ForecastingPacket
from fandango.io.navigation.graph.packetnavigator import PacketNavigator
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.selection.forecast_view import ForecastView
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.io.navigation.selection.target_selector import TargetSelector
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree
from fandango.logger import log_guidance_hint


class PacketGuide:
    """
    Decides which packet(s) to send next.
    Follows a planned guide path toward the current coverage target,
    re-plans when the path is left, and guides to the end of the run
    once coverage is full or the run grew too long.
    """

    def __init__(
        self,
        model: ProtocolModel,
        forecast: ForecastView,
        navigator: PacketNavigator,
        target_selector: TargetSelector,
        max_messages_per_tree: int,
    ):
        self._model = model
        self._forecast = forecast
        self._navigator = navigator
        self._target_selector = target_selector
        self._max_messages_per_tree = max_messages_per_tree

        self._history_tree: DerivationTree = DerivationTree(NonTerminal("<start>"))
        self._last_completed_tree: Optional[DerivationTree] = None
        self._prev_completed_count = 0
        self._guide_to_end = False
        self._guide_target: Optional[KPath] = None
        self._guide_path: list[PacketNonTerminal | NonTerminal | None] = []
        self._prev_session_msgs: list[DerivationTree] = []
        self._session_covered_k_paths: set[KPath] = set()

    @property
    def is_guide_to_end(self) -> bool:
        return self._guide_to_end

    def select_next_packet(
        self,
        history_tree: DerivationTree,
        last_completed_tree: Optional[DerivationTree],
        completed_count: int,
        get_uncovered_paths: Callable[[], list[KPath]],
        get_coverage_scores: Callable[[], list[tuple[NonTerminal, float]]],
    ) -> list[ForecastingPacket]:
        self._history_tree = history_tree
        self._last_completed_tree = last_completed_tree

        if len(self._forecast.next_fuzzer_parties()) == 0:
            current_external_parties = set(
                self._forecast.next_fuzzer_parties(False, True)
            )
            if "TimerEvent" not in current_external_parties:
                return []

        is_new_tree = completed_count > self._prev_completed_count
        if is_new_tree:
            self._session_covered_k_paths.clear()
        self._prev_completed_count = completed_count

        uncovered_paths = get_uncovered_paths()
        self._guide_to_end = False
        if (
            len(history_tree.protocol_msgs()) > self._max_messages_per_tree
            or len(uncovered_paths) == 0
        ):
            if len(uncovered_paths) == 0:
                log_guidance_hint("Full coverage reached. Guiding to end of tree.")
                if self._guide_target is not None:
                    self._confirm_covered_path(self._guide_target)
            else:
                log_guidance_hint(
                    f"Current tree contains more then {self._max_messages_per_tree} messages. Guiding to end of tree."
                )
            self._guide_to_end = True
            return self._get_guide_to_end_packet()

        left_path = True
        if len(self._guide_path) != 0:
            left_path = False
            for msg in self._new_msgs(is_new_tree):
                old_next_packet = self._get_next_packet()
                if old_next_packet is None or old_next_packet.symbol != msg.symbol:
                    # Check if msg is a permutation peer arriving out of order
                    assert isinstance(msg.symbol, NonTerminal)
                    if (
                        old_next_packet is not None
                        and old_next_packet.symbol in self._model.permutation_groups
                        and msg.symbol
                        in self._model.permutation_groups[old_next_packet.symbol]
                    ):
                        msg_pnt = PacketNonTerminal(
                            msg.sender, msg.recipient, msg.symbol
                        )
                        if msg_pnt in self._guide_path:
                            idx = self._guide_path.index(msg_pnt)
                            self._guide_path = (
                                self._guide_path[:idx] + self._guide_path[idx + 1 :]
                            )
                            continue
                    left_path = True
                    break
                self._guide_path = self._guide_path[
                    self._guide_path.index(old_next_packet) + 1 :
                ]

        if self._guide_target is None or len(self._guide_path) == 0 or left_path:
            if self._guide_target is not None:
                should_covered_paths = self._session_covered_k_paths.union(
                    [self._guide_target]
                )
                if self._is_tree_contains_paths(should_covered_paths, history_tree):
                    self._confirm_covered_path(self._guide_target)

            self._guide_target = self._target_selector.select(
                uncovered_paths, get_coverage_scores()
            )
            found_guide_path = self._navigator.astar_tree_including_k_paths(
                tree=history_tree,
                destination_k_path=self._guide_target,
                included_k_paths=self._session_covered_k_paths,
            )
            assert found_guide_path is not None
            self._guide_path = found_guide_path
        self._guide_to_end = (
            len(list(filter(lambda p: p is None, self._guide_path))) > 0
        )
        selected_packets = []
        next_packet = self._get_next_packet()
        hookin_states: Optional[list[Symbol]] = None
        if next_packet is not None:
            assert self._guide_path is not None
            packet_idx = self._guide_path.index(next_packet)
            hookin_states = []
            for symbol in self._guide_path[:packet_idx]:
                if symbol is None:
                    continue
                assert isinstance(symbol, Symbol)
                hookin_states.append(symbol)
            packet_sender = next_packet.sender
            packet_symbol = next_packet.symbol
        else:
            if self._guide_path is not None:
                hookin_states = []
                for symbol in self._guide_path:
                    if symbol is None:
                        continue
                    assert isinstance(symbol, Symbol)
                    hookin_states.append(symbol)
            packet_sender = None
            packet_symbol = None

        selected_packets.extend(
            self.find_packets(
                sender=packet_sender,
                hookin_states=hookin_states,
                packet_symbol=packet_symbol,
            )
        )

        if len(selected_packets) == 0:
            selected_packets.extend(self._forecast.get_fuzzer_packets())
        self._remember_messages()
        return selected_packets

    def find_packets(
        self,
        *,
        sender: Optional[str] = None,
        hookin_states: Optional[list[Symbol]] = None,
        packet_symbol: Optional[NonTerminal] = None,
    ) -> list[ForecastingPacket]:
        packets = []
        hookin_states_tp: tuple[Symbol, ...] = tuple()
        if hookin_states is not None:
            hookin_states_tp = tuple(hookin_states)

        available_senders = self._forecast.next_fuzzer_parties()
        if "TimerEvent" in self._forecast.next_external_parties():
            available_senders.append("TimerEvent")

        for current_sender in available_senders:
            if sender is not None and current_sender != sender:
                continue
            for packet in self._forecast.result[current_sender].nt_to_packet.values():
                if packet_symbol is not None and packet.node.symbol != packet_symbol:
                    continue
                append_packet = ForecastingPacket(packet.node)
                for hookin_path in packet.paths:
                    if not self._is_tree_contains_paths(
                        self._session_covered_k_paths, hookin_path.tree
                    ):
                        continue
                    packet_hookin_states = tuple(
                        map(lambda y: y[0], filter(lambda x: x[1], hookin_path.path))
                    )
                    if not PacketGuide._tuple_contains(
                        hookin_states_tp, packet_hookin_states
                    ):
                        continue
                    append_packet.paths.add(hookin_path)
                if len(append_packet.paths) != 0:
                    packets.append(append_packet)
        return packets

    def _get_guide_to_end_packet(self) -> list[ForecastingPacket]:
        path = self._navigator.astar_search_end_including_k_paths(
            self._history_tree, included_k_paths=self._session_covered_k_paths
        )
        if path is None:
            return []
        if len(path) > 0:
            next_packet = next(
                filter(lambda x: isinstance(x, PacketNonTerminal), path), None
            )
            if next_packet is None:
                return []
            assert isinstance(next_packet, PacketNonTerminal)
            return self.find_packets(
                sender=next_packet.sender, packet_symbol=next_packet.symbol
            )
        return []

    def _get_next_packet(self) -> Optional[PacketNonTerminal]:
        if self._guide_path is None:
            return None
        return next(
            (x for x in self._guide_path if isinstance(x, PacketNonTerminal)), None
        )

    def _is_tree_contains_paths(
        self, paths: set[tuple[Symbol, ...]], tree: DerivationTree
    ) -> bool:
        _found_trees, include_k_paths = self._navigator._find_trees_including_k_paths(
            paths, tree
        )
        return include_k_paths

    def _confirm_covered_path(self, path: KPath) -> None:
        self._session_covered_k_paths.add(path)

    def _remember_messages(self) -> None:
        if self._history_tree is None:
            self._prev_session_msgs = []
            return
        self._prev_session_msgs = list(
            map(lambda x: x.msg, self._history_tree.protocol_msgs())
        )

    def _new_msgs(self, is_new_tree: bool) -> list[DerivationTree]:
        prev_msgs = []
        if is_new_tree:
            assert self._last_completed_tree is not None
            prev_msgs = list(
                map(lambda x: x.msg, self._last_completed_tree.protocol_msgs())
            )
        current_session_msgs = list(
            map(lambda x: x.msg, self._history_tree.protocol_msgs())
        )
        all_current_msgs = prev_msgs + current_session_msgs

        if all(m.arrival_index is not None for m in all_current_msgs) and all(
            m.arrival_index is not None for m in self._prev_session_msgs
        ):
            seen = {m.arrival_index for m in self._prev_session_msgs}
            new_msgs = [m for m in all_current_msgs if m.arrival_index not in seen]
            new_msgs.sort(
                key=lambda m: m.arrival_index if m.arrival_index is not None else -1
            )
            return new_msgs

        # Fallback
        new_msgs = []
        for prev, new in zip(self._prev_session_msgs, all_current_msgs, strict=False):
            if prev != new:
                new_msgs.extend(current_session_msgs)
                return new_msgs
        if len(all_current_msgs) > len(self._prev_session_msgs):
            return all_current_msgs[len(self._prev_session_msgs) :]
        return new_msgs

    @staticmethod
    def _tuple_contains(sub: tuple[Symbol, ...], full: tuple[Symbol, ...]) -> bool:
        n, m = len(sub), len(full)
        if n == 0:
            return True
        for i in range(m - n + 1):
            if full[i : i + n] == sub:
                return True
        return False
