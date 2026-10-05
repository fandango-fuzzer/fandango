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
from fandango.language.tree import DerivationTree
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
            self._model.grammar,
            self._model.start_symbol,
            step_costs=self._step_refusals.repeat_costs,
        )
        self._target_selector = TargetSelector(model)
        self._max_messages_per_tree = max_messages_per_tree

        self._history_tree: DerivationTree = DerivationTree(NonTerminal("<start>"))
        self._guide_to_end = False
        self._abandons_run = False
        self._guide_target: Optional[KPath] = None
        self._guide_path = GuidePathTracker(model.permutation_groups)
        self._deviation: Optional[Deviation] = None
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
        self._clear_plan()
        self._start_session()
        self._build_navigator_around_blocked_steps()

    def observe_session_end(self, history_tree: DerivationTree) -> None:
        """
        Notifies that the session of history_tree ended via completion or abandance.
        Counts the step an external party still had to take as refused, unless the guider gave the session up.
        Keeps the current route only if the session was not given up and its route leads to a target in the next session.
        """
        if not self._abandons_run:
            self._count_unanswered_step(history_tree)
        self._step_refusals.signal_session_end()
        self._build_navigator_around_blocked_steps()
        if (
            self._abandons_run
            or self._guide_target is None
            or not self._guide_path.ends_run
        ):
            self._clear_plan()
        else:
            self._guide_path.move_to_next_session_start()
        self._start_session()

    def _clear_plan(self) -> None:
        self._guide_target = None
        self._guide_path.clear()

    def _start_session(self) -> None:
        """Forgets what belongs to the ended session."""
        self._history_tree = DerivationTree(NonTerminal("<start>"))
        self._guide_to_end = False
        self._abandons_run = False
        self._deviation = None
        self._session_covered_k_paths.clear()

    def observe_message(self, history_tree: DerivationTree) -> None:
        """Notifies that a message was sent or received. It is the last message of history_tree, the new history."""
        self._history_tree = history_tree
        message = next(history_tree.protocol_msgs(reverse=True))
        steps = self._forecast.result.message_steps[-1]
        for step in steps:
            self._step_refusals.observe_taken(step, message.sender)
        if self._deviation is not None:
            # Only the first message that leaves the plan counts; the next selection plans anew.
            return
        self._deviation = self._guide_path.follow(message.msg, steps)
        if self._deviation is None:
            return
        if self._deviation.refused is not None:
            self._step_refusals.count_refusal(self._deviation.refused, message.sender)
        if self._is_end_route_refused(self._deviation):
            LOGGER.warning(
                "NAVIGATORPANIC: Observed derivation of planned protocol path twice for the same transition. "
                f"Hard-terminating protocol session. Observed derivation {self._deviation}"
            )
            self._abandons_run = True

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
        get_uncovered_paths: Callable[[], list[KPath]],
        get_coverage_scores: Callable[[], list[tuple[NonTerminal, float]]],
    ) -> list[ForecastingPacket]:
        self._history_tree = history_tree

        if len(self._forecast.next_fuzzer_parties()) == 0:
            current_external_parties = set(
                self._forecast.next_fuzzer_parties(False, True)
            )
            if "TimerEvent" not in current_external_parties:
                return []

        route_completed = self._guide_path.next_packet() is None
        completed_target = self._guide_target if route_completed else None
        deviation = self._deviation
        self._deviation = None
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
            completed_target is not None
            and completed_target != self._guide_target
            and completed_target not in self._session_covered_k_paths
        ):
            # Keep the followed target if a packet can.
            selected_packets = self.find_packets(
                sender=sender,
                hookin_states=hookin_states,
                packet_symbol=packet_symbol,
                required_k_paths=self._session_covered_k_paths.union(
                    [completed_target]
                ),
            )
        if len(selected_packets) == 0:
            selected_packets = self.find_packets(
                sender=sender, hookin_states=hookin_states, packet_symbol=packet_symbol
            )
        if len(selected_packets) == 0:
            selected_packets = self._forecast.get_fuzzer_packets()
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

    def _count_unanswered_step(self, history_tree: DerivationTree) -> None:
        """Counts a refusal of the step an external party had to take next when the run ended without it."""
        self._history_tree = history_tree
        if self._deviation is not None:
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
            refused = self._guide_path.target_step
            if refused is not None:
                self._step_refusals.count_refusal(refused, party)
                return

    def _is_end_route_refused(self, deviation: Deviation) -> bool:
        """
        True if the party refused a step of the route to the end of the run and that step's block is deferred.
        """
        return (
            self._guide_to_end
            and deviation.refused is not None
            and self._step_refusals.is_block_deferred(deviation.refused)
        )

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
