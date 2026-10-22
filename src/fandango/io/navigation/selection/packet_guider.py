from collections.abc import Callable
from typing import NamedTuple, Optional

from fandango.io.navigation.forecasting.forecast_view import ForecastView
from fandango.io.navigation.forecasting.forecasting_result import ForecastingPacket
from fandango.io.navigation.graph.grammar_navigator.navigator import (
    UnreachableTargetError,
)
from fandango.io.navigation.graph.packetnavigator import (
    PacketNavigator,
    SuspectPredecessors,
)
from fandango.io.navigation.route import GuidePath
from fandango.io.navigation.selection.guide_path_tracker import (
    Deviation,
    GuidePathTracker,
)
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.io.navigation.selection.step_refusals import StepRefusalCounter
from fandango.io.navigation.selection.target_selector import TargetSelector
from fandango.io.navigation.step import Step
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree
from fandango.logger import log_guidance_hint


class RouteRestrictions(NamedTuple):
    blocked_steps: frozenset[Step]
    suspect_predecessors: SuspectPredecessors

    def lifts_any_of(self, last: "RouteRestrictions") -> bool:
        """Tells whether a blocked step or suspect predecessor of last is missing here."""
        return not last.blocked_steps <= self.blocked_steps or any(
            not predecessors <= self.suspect_predecessors.get(packet_type, frozenset())
            for packet_type, predecessors in last.suspect_predecessors.items()
        )


class PacketGuider:
    """
    Decides which packet(s) to send next.
    Follows a planned guide path toward the current coverage target,
    re-plans when the path is left, and guides to the end of the run
    once coverage is full or the run grew too long.
    """

    TARGET_ATTEMPTS = 4

    def __init__(
        self,
        model: ProtocolModel,
        forecast: ForecastView,
        max_messages_per_tree: int,
        suspect_predecessors: Callable[[], SuspectPredecessors] = dict,
    ):
        self._model = model
        self._forecast = forecast
        self._step_refusals = StepRefusalCounter()
        self._suspect_predecessors = suspect_predecessors
        self._navigator_instance = PacketNavigator(
            self._model.grammar, self._model.start_symbol
        )
        self._target_selector = TargetSelector(model)
        self._max_messages_per_tree = max_messages_per_tree

        self._history_tree: DerivationTree = DerivationTree(NonTerminal("<start>"))
        self._guide_to_end = False
        self._abandons_run = False
        self._guide_target: Optional[KPath] = None
        self._guide_path = GuidePathTracker(model.permutation_groups)
        self._deviated_from_guide = False
        self._session_covered_k_paths: set[KPath] = set()
        self._steps_keeping_covered_paths: dict[str, set[Step]] = {}
        self._end_route_refusals_in_session = 0
        # Targets out of reach of every run under the restrictions last seen
        self._unreachable_targets: set[KPath] = set()
        self._last_restrictions: Optional[RouteRestrictions] = None

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
        self._unreachable_targets.clear()
        self._last_restrictions = None
        self._clear_plan()
        self._start_session()

    def observe_session_end(self, generation_failed: bool = False) -> None:
        """
        Notifies that the session ended, completed or aborted.
        Counts the step an external party still had to take as refused, unless the guider gave the session up.
        If generation_failed, the fuzzer could not generate a packet for its next step, which then counts as refused.
        Keeps the current route only if the session was not given up and its route leads to a target in the next session.
        """
        if not self._abandons_run:
            self._count_pending_step_as_refused(generation_failed)
        self._step_refusals.signal_session_end()
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
        self._deviated_from_guide = False
        self._session_covered_k_paths.clear()
        self._steps_keeping_covered_paths = {}
        self._end_route_refusals_in_session = 0

    def observe_message(self, history_tree: DerivationTree) -> None:
        """Notifies that a message was sent or received. It is the last message of history_tree, the new history."""
        self._history_tree = history_tree
        message = next(history_tree.protocol_msgs(reverse=True))
        steps = self._forecast.result.last_message_steps
        for step in steps:
            self._step_refusals.observe_taken(step, message.sender)
        self._check_covered_paths_kept(message.sender, history_tree)
        self._follow_guide_path(message.msg, message.sender, steps)
        self._steps_keeping_covered_paths = self._external_steps_keeping_covered_paths()

    def _check_covered_paths_kept(
        self, sender: str, history_tree: DerivationTree
    ) -> None:
        """
        Checks whether a parse of the history still contains the confirmed k-paths.
        If not, counts the steps the sender could have taken to keep them as refused and drops the confirmed k-paths.
        """
        if not self._session_covered_k_paths or self._is_tree_contains_paths(
            self._session_covered_k_paths, history_tree
        ):
            return
        for step in self._steps_keeping_covered_paths.get(sender, set()):
            self._step_refusals.count_refusal(step, sender)
        self._session_covered_k_paths.clear()
        self._deviated_from_guide = True

    def _external_steps_keeping_covered_paths(self) -> dict[str, set[Step]]:
        """The steps by which each external party can send its next packet and keep the confirmed k-paths."""
        if not self._session_covered_k_paths:
            return {}
        steps_by_party: dict[str, set[Step]] = {}
        for party in self._forecast.next_external_parties():
            if party not in self._forecast.result:
                continue
            for packet in self._forecast.result[party].nt_to_packet.values():
                for mounting_path in packet.paths:
                    if mounting_path.step is not None and self._is_tree_contains_paths(
                        self._session_covered_k_paths, mounting_path.tree
                    ):
                        steps_by_party.setdefault(party, set()).add(mounting_path.step)
        return steps_by_party

    def _follow_guide_path(
        self, message: DerivationTree, sender: str, steps: set[Step]
    ) -> None:
        """Follows the guide path with the message; counts the step the sender refused if it left the path."""
        if self._deviated_from_guide:
            # Only the first message that leaves the plan counts; the next selection plans anew.
            return
        deviation = self._guide_path.follow(message, steps)
        if deviation is None:
            if self._guide_path.is_empty and self._guide_target is not None:
                # The message completed the route, Limit upcoming parses to versions that contain the path.
                self._confirm_covered_path(self._guide_target)
            return
        self._deviated_from_guide = True
        if deviation.refused is not None:
            self._step_refusals.count_refusal(deviation.refused, sender)
            if self._guide_to_end:
                self._end_route_refusals_in_session += 1
        if self._is_end_route_refused(deviation):
            log_guidance_hint(
                f"{sender} refused the route to the end of the run at {deviation.refused}. Ending the session."
            )
            self._abandons_run = True

    def is_derivable_coverage_complete(self, uncovered_paths: list[KPath]) -> bool:
        return self._target_selector.is_every_path_underivable(
            uncovered_paths, self._updated_navigator().is_derivable
        )

    def _updated_navigator(self) -> PacketNavigator:
        """Brings the navigator up to the blocked steps, step costs and suspect predecessors and returns it."""
        blocked_steps = self._step_refusals.blocked_steps
        if blocked_steps != self._navigator_instance.blocked_steps:
            self._navigator_instance = self._navigator_instance.with_blocked_steps(
                blocked_steps
            )
        self._navigator_instance.set_step_costs(self._step_refusals.repeat_costs())
        self._navigator_instance.set_suspect_predecessors(self._suspect_predecessors())
        return self._navigator_instance

    def _update_unreachable_targets(self) -> None:
        """Forgets the targets out of reach of every run once a blocked step or suspect predecessor was lifted."""
        restrictions = RouteRestrictions(
            self._step_refusals.blocked_steps, self._suspect_predecessors()
        )
        if self._last_restrictions is not None and restrictions.lifts_any_of(
            self._last_restrictions
        ):
            self._unreachable_targets.clear()
        self._last_restrictions = restrictions

    def _is_reachable_target(self, target: KPath) -> bool:
        """True if the target is derivable and not known to be out of reach of every run."""
        return (
            target not in self._unreachable_targets
            and self._updated_navigator().is_derivable(target)
        )

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

        plan_left = self._deviated_from_guide
        self._deviated_from_guide = False

        uncovered_paths = get_uncovered_paths()
        if (
            len(list(history_tree.protocol_msgs())) > self._max_messages_per_tree
            or len(uncovered_paths) == 0
            or self._step_refusals.has_deferred_blocks
        ):
            if len(uncovered_paths) == 0:
                log_guidance_hint("Full coverage reached. Guiding to end of tree.")
                if self._guide_target is not None:
                    self._confirm_covered_path(self._guide_target)
            elif self._step_refusals.has_deferred_blocks:
                if not self._guide_to_end:
                    log_guidance_hint(
                        "Steps wait for the session end to be blocked. Guiding to end of tree."
                    )
            else:
                log_guidance_hint(
                    f"Current tree contains more then {self._max_messages_per_tree} messages. Guiding to end of tree."
                )
            self._plan_path_to_end()
        elif self._guide_target is None or self._guide_path.is_empty or plan_left:
            self._plan_path_to_reachable_target(uncovered_paths, get_coverage_scores)
        self._guide_to_end = self._guide_path.ends_run

        next_packet = self._guide_path.next_packet()
        sender = None if next_packet is None else next_packet.packet.sender
        hookin_states = self._guide_path.next_new_parent_states()
        packet_symbol = None if next_packet is None else next_packet.packet.symbol
        selected_packets = self.find_packets(
            sender=sender, hookin_states=hookin_states, packet_symbol=packet_symbol
        )
        if len(selected_packets) == 0:
            selected_packets = self._forecast.get_fuzzer_packets()
        return selected_packets

    def _plan_path_to_reachable_target(
        self,
        uncovered_paths: list[KPath],
        get_coverage_scores: Callable[[], list[tuple[NonTerminal, float]]],
    ) -> None:
        """
        Selects targets until one has a path, in this run or a new one, and follows that path. Leaves out each target
        without a path until a restriction is lifted. Follows a path to the end of the run if no target has a path.
        """
        self._update_unreachable_targets()
        for _ in range(self.TARGET_ATTEMPTS):
            target = self._target_selector.select(
                uncovered_paths, get_coverage_scores(), self._is_reachable_target
            )
            if target is None:
                break
            try:
                guide = self._updated_navigator().astar_tree_including_k_paths(
                    tree=self._history_tree,
                    destination_k_path=target,
                    included_k_paths=self._session_covered_k_paths,
                )
            except UnreachableTargetError:
                guide = None
            if guide is not None:
                self._guide_target = target
                self._guide_path.set_guide_path(guide)
                return
            log_guidance_hint(
                f"No path to {target} in this run or a new one. Leaving it out until a restriction is lifted."
            )
            self._unreachable_targets.add(target)
        log_guidance_hint("No target with a path. Guiding to end of tree.")
        self._plan_path_to_end()

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
        path = self._updated_navigator().astar_search_end_including_k_paths(
            self._history_tree, included_k_paths=self._session_covered_k_paths
        )
        # None marks the end of the run, as in the paths to a target.
        if path is None:
            self._guide_path.set_guide_path(GuidePath([None]))
        else:
            self._guide_path.set_guide_path(GuidePath([*path, None]))

    def _is_tree_contains_paths(self, paths: set[KPath], tree: DerivationTree) -> bool:
        return self._updated_navigator().contains_k_paths(paths, tree)

    def _confirm_covered_path(self, path: KPath) -> None:
        self._session_covered_k_paths.add(path)

    def _is_external_party(self, party: Optional[str]) -> bool:
        return party is not None and not self._forecast.is_fuzzer_controlled(party)

    def _count_pending_step_as_refused(self, generation_failed: bool) -> None:
        """
        Checks whether an external party still had to take a step of the plan when the session ended,
        and counts that step as refused. If generation_failed, a step of the fuzzer counts as well.
        """
        if self._deviated_from_guide:
            # The plan was left, so nothing of it is pending.
            return
        planned = self._guide_path.next_packet()
        if planned is not None:
            if generation_failed or self._is_external_party(planned.packet.sender):
                assert planned.packet.sender is not None
                self._step_refusals.count_refusal(planned.step, planned.packet.sender)
            return
        target_step = self._guide_path.target_step
        if (
            target_step is None
            or self._guide_path.is_empty
            or self._guide_path.ends_run
        ):
            # The target is reached, or it lies in the next session.
            return
        parties = (
            self._forecast.next_fuzzer_parties()
            if generation_failed
            else self._forecast.next_external_parties()
        )
        if parties:
            self._step_refusals.count_refusal(target_step, parties[0])

    def _is_end_route_refused(self, deviation: Deviation) -> bool:
        """
        True if the party refused a step of the route to the end of the run and that step's block is deferred,
        or if steps of routes to the end were refused REFUSAL_LIMIT times in this session.
        """
        return (
            self._guide_to_end
            and deviation.refused is not None
            and (
                self._step_refusals.is_block_deferred(deviation.refused)
                or self._end_route_refusals_in_session
                >= StepRefusalCounter.REFUSAL_LIMIT
            )
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
