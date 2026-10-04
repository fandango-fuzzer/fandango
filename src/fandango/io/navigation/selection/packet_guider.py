from collections.abc import Callable
from typing import Optional

from fandango.io.navigation.forecasting.forecast_view import ForecastView
from fandango.io.navigation.forecasting.forecasting_result import ForecastingPacket
from fandango.io.navigation.graph.packetnavigator import PacketNavigator
from fandango.io.navigation.route import GuidePath
from fandango.io.navigation.selection.guide_path_tracker import (
    Deviation,
    GuidePathTracker,
)
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.io.navigation.selection.step_refusals import StepRefusalCounter
from fandango.io.navigation.selection.target_selector import TargetSelector
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree, ProtocolMessage, index_by_reference
from fandango.logger import LOGGER, log_guidance_hint


class PacketGuider:
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
        max_messages_per_tree: int,
    ):
        self._model = model
        self._forecast = forecast
        self._step_refusals = StepRefusalCounter()
        self._navigator = PacketNavigator(
            self._model.grammar, self._model.start_symbol, step_costs=self._step_refusals.repeat_costs
        )
        self._target_selector = TargetSelector(model)
        self._max_messages_per_tree = max_messages_per_tree

        self._history_tree: DerivationTree = DerivationTree(NonTerminal("<start>"))
        self._last_completed_tree: Optional[DerivationTree] = None
        self._prev_completed_count = 0
        self._guide_to_end = False
        self._abandons_run = False
        self._guide_target: Optional[KPath] = None
        self._guide_path = GuidePathTracker(model.permutation_groups)
        self._prev_session_msgs: list[DerivationTree] = []
        self._session_covered_k_paths: set[KPath] = set()

    @property
    def is_guide_to_end(self) -> bool:
        return self._guide_to_end

    @property
    def abandons_run(self) -> bool:
        """True if the run cannot be guided to its end and should be aborted."""
        return self._abandons_run

    @property
    def max_messages_per_tree(self) -> int:
        return self._max_messages_per_tree

    @max_messages_per_tree.setter
    def max_messages_per_tree(self, count: int) -> None:
        self._max_messages_per_tree = count

    def reset(self) -> None:
        """Forget everything about previous runs, as after construction."""
        self._target_selector.reset()
        self._step_refusals.reset()
        self.abort_run()
        self._last_completed_tree = None
        self._prev_completed_count = 0
        self._build_navigator_around_blocked_steps()

    def abort_run(self) -> None:
        """Forget the current guide target and start with a new DerivationTree."""
        self._history_tree = DerivationTree(NonTerminal("<start>"))
        self._guide_to_end = False
        self._abandons_run = False
        self._guide_target = None
        self._guide_path.clear()
        self._prev_session_msgs = []
        self._session_covered_k_paths.clear()
        self._step_refusals.signal_session_end()

    def observe_message(self, message: ProtocolMessage) -> None:
        """Notifies that the message was sent or received. It is the last message of the history."""

    def observe_run_end(self, history_tree: DerivationTree) -> None:
        self._history_tree = history_tree
        self._observe_messages(self._new_msgs(False))
        self._build_navigator_around_blocked_steps()
        self._step_refusals.signal_session_end()

    def is_derivable_coverage_complete(self, uncovered_paths: list[KPath]) -> bool:
        return self._target_selector.is_every_path_underivable(
            uncovered_paths, self._navigator.is_derivable
        )

    def _build_navigator_around_blocked_steps(self) -> None:
        """Builds a new navigator if the blocked steps changed."""
        blocked_steps = self._step_refusals.blocked_steps
        if blocked_steps != self._navigator.blocked_steps:
            self._navigator = self._navigator.gen_with_blocked_steps(blocked_steps)

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

        route_followed = not is_new_tree and self._guide_path.next_packet() is None
        followed_target = self._guide_target if route_followed else None
        new_msgs = self._new_msgs(is_new_tree)
        self._observe_messages(new_msgs)
        deviation = self._guide_path.follow(new_msgs)
        if deviation is not None:
            self._count_refused_step(deviation)
            if (
                deviation.planned is None
                and followed_target is not None
                and followed_target not in self._session_covered_k_paths
                and not self._is_tree_contains_paths({followed_target}, history_tree)
            ):
                # The route was followed to its end and the last answer left the target.
                self._count_refused_target(new_msgs[-1])
            if self._is_end_route_refused(deviation):
                LOGGER.warning(
                    "NAVIGATORPANIC: Observed derivation of planned protocol path twice for the same transition. "
                    f"Hard-terminating protocol session. Observed derivation {deviation}"
                )
                self._abandons_run = True
        self._build_navigator_around_blocked_steps()

        uncovered_paths = get_uncovered_paths()
        if (
            len(list(history_tree.protocol_msgs())) > self._max_messages_per_tree
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
            self._plan_path_to_end()
        elif (
            self._guide_target is None
            or self._guide_path.is_empty
            or deviation is not None
        ):
            if self._guide_target is not None:
                should_covered_paths = self._session_covered_k_paths.union(
                    [self._guide_target]
                )
                if self._is_tree_contains_paths(should_covered_paths, history_tree):
                    self._confirm_covered_path(self._guide_target)

            self._guide_target = self._target_selector.select(
                uncovered_paths, get_coverage_scores(), self._navigator.is_derivable
            )
            guide = self._navigator.astar_tree_including_k_paths(
                tree=history_tree,
                destination_k_path=self._guide_target,
                included_k_paths=self._session_covered_k_paths,
            )
            if guide is None:
                # The target is not reachable from this tree; finish the run,
                # the next one starts from scratch.
                log_guidance_hint(
                    "No path from the current tree to the selected k-path. Guiding to end of tree."
                )
                self._plan_path_to_end()
            else:
                self._guide_path.set_guide_path(guide)
        self._guide_to_end = self._guide_path.ends_run

        next_packet = self._guide_path.next_packet()
        sender = None if next_packet is None else next_packet.packet.sender
        hookin_states = self._guide_path.next_new_parent_states()
        packet_symbol = None if next_packet is None else next_packet.packet.symbol
        selected_packets = []
        if (
            followed_target is not None
            and followed_target != self._guide_target
            and followed_target not in self._session_covered_k_paths
        ):
            # Keep the followed target if a packet can.
            selected_packets = self.find_packets(
                sender=sender,
                hookin_states=hookin_states,
                packet_symbol=packet_symbol,
                required_k_paths=self._session_covered_k_paths.union([followed_target]),
            )
        if len(selected_packets) == 0:
            selected_packets = self.find_packets(
                sender=sender, hookin_states=hookin_states, packet_symbol=packet_symbol
            )
        if len(selected_packets) == 0:
            selected_packets = self._forecast.get_fuzzer_packets()
        self._remember_messages()
        return selected_packets

    def find_packets(
        self,
        *,
        sender: Optional[str] = None,
        hookin_states: Optional[list[Symbol]] = None,
        packet_symbol: Optional[NonTerminal] = None,
        required_k_paths: Optional[set[KPath]] = None,
    ) -> list[ForecastingPacket]:
        if required_k_paths is None:
            required_k_paths = self._session_covered_k_paths
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
                        required_k_paths, hookin_path.tree
                    ):
                        continue
                    packet_hookin_states = tuple(
                        map(lambda y: y[0], filter(lambda x: x[1], hookin_path.path))
                    )
                    if not PacketGuider._tuple_contains(
                        hookin_states_tp, packet_hookin_states
                    ):
                        continue
                    append_packet.paths.add(hookin_path)
                if len(append_packet.paths) != 0:
                    packets.append(append_packet)
        return packets

    def _plan_path_to_end(self) -> None:
        """Drops the target and follows a path to the end of the run from now on."""
        self._guide_target = None
        path = self._navigator.astar_search_end_including_k_paths(
            self._history_tree, included_k_paths=self._session_covered_k_paths
        )
        # None marks the end of the run, as in the paths to a target.
        if path is None:
            self._guide_path.set_guide_path(GuidePath([None]))
        else:
            self._guide_path.set_guide_path(GuidePath([*path, None]))

    def _is_tree_contains_paths(self, paths: set[KPath], tree: DerivationTree) -> bool:
        return self._navigator.contains_k_paths(paths, tree)

    def _confirm_covered_path(self, path: KPath) -> None:
        self._session_covered_k_paths.add(path)

    def _is_external_party(self, party: Optional[str]) -> bool:
        return party is not None and not self._forecast.is_fuzzer_controlled(party)

    def _observe_messages(self, messages: list[DerivationTree]) -> None:
        """Counts the steps that may have produced the external messages of the history as taken."""
        history_messages = [record.msg for record in self._history_tree.protocol_msgs()]
        message_steps = self._forecast.result.message_steps
        for message in messages:
            index = index_by_reference(history_messages, message)
            if index is None or not self._is_external_party(message.sender):
                continue
            assert message.sender is not None
            for step in message_steps[index]:
                self._step_refusals.observe_taken(step, message.sender)

    def _count_refused_step(self, deviation: Deviation) -> None:
        planned, msg = deviation
        if planned is None:
            return
        # If someone else sent the message we dont penalize the expected party.
        if msg.sender != planned.packet.sender or not self._is_external_party(
            msg.sender
        ):
            return
        assert msg.sender is not None
        self._step_refusals.count_refusal(planned.step, msg.sender)

    def count_unanswered_step(self, history_tree: DerivationTree) -> None:
        """Counts a refusal of the step an external party had to take next when the run ended without it."""
        self._history_tree = history_tree
        if self._guide_path.follow(self._new_msgs(False)) is not None:
            return
        planned = self._guide_path.next_packet()
        if planned is not None:
            if self._is_external_party(planned.packet.sender):
                assert planned.packet.sender is not None
                self._step_refusals.count_refusal(planned.step, planned.packet.sender)
            return
        if self._guide_target is None or self._guide_to_end:
            return
        # The route was followed to its end, so the answer inside the target is missing.
        for party in self._forecast.next_external_parties():
            refused = self._guide_path.refused_step(party)
            if refused is not None:
                self._step_refusals.count_refusal(refused, party)
                return

    def _is_end_route_refused(self, deviation: Deviation) -> bool:
        """
        True if the party refused a step of the route to the end of the run and that step's block is deferred.
        """
        planned, _message = deviation
        return (
            self._guide_to_end
            and planned is not None
            and self._step_refusals.is_block_deferred(planned.step)
        )

    def _count_refused_target(self, message: DerivationTree) -> None:
        """Counts the refusal on the step to the first packet the sender had to send inside the target, or else on the step to the target."""
        if not self._is_external_party(message.sender):
            return
        assert message.sender is not None
        refused = self._guide_path.refused_step(message.sender)
        if refused is not None:
            self._step_refusals.count_refusal(refused, message.sender)

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

    def __repr__(self) -> str:
        return (
            f"PacketGuider(target={self._guide_target!r}, "
            f"guide_to_end={self._guide_to_end}, {self._guide_path!r}, "
            f"session_covered={len(self._session_covered_k_paths)}, {self._step_refusals!r})"
        )
