import random
from collections import Counter
from collections.abc import Callable
from typing import Optional

from fandango.io.navigation.coverage.powerschedule import (
    PowerScheduleCoverage,
    PowerScheduleKPath,
)
from fandango.io.navigation.graph.packetnavigator import PacketNavigator
from fandango.io.navigation.selection.open_targets import OpenTargets
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar.k_paths import KPath
from fandango.language.symbols import NonTerminal, Symbol


class TargetSelector:
    """Picks the next k-path to guide toward."""

    # How often a target may be picked before the targets one longer are picked as well.
    MAX_PICKS = 3
    MESSAGE_TARGET_SHARE = 0.25

    def __init__(
        self,
        model: ProtocolModel,
        open_sent_messages: Callable[[], list[NonTerminal]] = list,
    ):
        self._model = model
        self._open_sent_messages = open_sent_messages
        self._msg_power_schedule = PowerScheduleCoverage()
        self._state_path_power_schedule = PowerScheduleKPath()
        self._open_targets = OpenTargets(model)
        self._picks: Counter[KPath] = Counter()

    def reset(self) -> None:
        """Forget the targets chosen so far, as after construction."""
        self._msg_power_schedule = PowerScheduleCoverage()
        self._state_path_power_schedule = PowerScheduleKPath()
        self._open_targets.reset()
        self._picks = Counter()

    def mark_unreachable(self, target: KPath) -> None:
        self._open_targets.mark_unreachable(target)

    def clear_unreachable(self) -> None:
        self._open_targets.clear_unreachable()

    def select(
        self,
        uncovered_paths: set[KPath],
        coverage_scores: list[tuple[NonTerminal, float]],
        navigator: PacketNavigator,
    ) -> Optional[KPath]:
        """Picks a reachable uncovered k-path, or else a reachable message. None if there is neither."""
        self._open_targets.set_uncovered(uncovered_paths)
        reachable_sent_messages = [
            message
            for message in self._open_sent_messages()
            if self._open_targets.is_reachable_message(message, navigator)
        ]
        if reachable_sent_messages and random.random() < self.MESSAGE_TARGET_SHARE:
            return (random.choice(reachable_sent_messages),)
        candidates = self._targets_up_to_current_length(navigator) or list(
            self._open_targets.reachable(navigator)
        )
        if len(candidates) == 0:
            reachable_scores = [
                (message, score)
                for message, score in coverage_scores
                if self._open_targets.is_reachable_message(message, navigator)
            ]
            if len(reachable_scores) == 0:
                return None
            return (self._least_covered_message(reachable_scores),)
        s_ps = self._state_path_power_schedule
        s_ps.assign_energy_k_path(candidates)
        selected_path = s_ps.choose()
        s_ps.add_past_target(selected_path)
        self._picks[selected_path] += 1
        return selected_path

    def _targets_up_to_current_length(self, navigator: PacketNavigator) -> list[KPath]:
        """
        The reachable uncovered targets up to the current length.
        The current length is the shortest one with a target picked fewer than MAX_PICKS times.
        """
        reachable_uncovered_by_length = (
            self._open_targets.reachable_uncovered_by_length(navigator)
        )
        candidates: list[KPath] = []
        for length in sorted(reachable_uncovered_by_length):
            targets = reachable_uncovered_by_length[length]
            candidates.extend(targets)
            if any(self._picks[target] < self.MAX_PICKS for target in targets):
                return candidates
        return []

    def is_derivable_coverage_complete(
        self, uncovered_paths: set[KPath], navigator: PacketNavigator
    ) -> bool:
        return self._open_targets.is_derivable_coverage_complete(
            uncovered_paths, navigator
        )

    def _least_covered_message(
        self, coverage_scores: list[tuple[NonTerminal, float]]
    ) -> Symbol:
        message_coverage: dict[Symbol, float] = dict(coverage_scores)
        m_ps = self._msg_power_schedule
        m_ps.assign_energy_coverage(message_coverage)
        target = m_ps.choose()
        m_ps.add_past_target(target)
        return target
