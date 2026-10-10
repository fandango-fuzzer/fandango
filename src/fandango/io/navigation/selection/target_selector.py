from collections import Counter, defaultdict
from collections.abc import Callable

from fandango.io.navigation.coverage.powerschedule import (
    PowerScheduleCoverage,
    PowerScheduleKPath,
)
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols import NonTerminal, Symbol


class TargetSelector:
    """Picks the next k-path to guide toward."""

    # How often a target may be picked before the targets one longer are picked as well.
    MAX_PICKS = 3

    def __init__(self, model: ProtocolModel):
        self._model = model
        self._msg_power_schedule = PowerScheduleCoverage()
        self._state_path_power_schedule = PowerScheduleKPath()
        self._protocol_msg_symbols = set(
            map(lambda x: x.symbol, self._model.protocol_msg_symbols)
        )
        self._state_target_by_path: dict[KPath, KPath] = {}
        self._uncovered: set[KPath] = set()
        self._open_below: Counter[KPath] = Counter()
        self._picks: Counter[KPath] = Counter()

    def reset(self) -> None:
        """Forget the targets chosen so far, as after construction."""
        self._msg_power_schedule = PowerScheduleCoverage()
        self._state_path_power_schedule = PowerScheduleKPath()
        self._uncovered = set()
        self._open_below = Counter()
        self._picks = Counter()

    def select(
        self,
        uncovered_paths: list[KPath],
        coverage_scores: list[tuple[NonTerminal, float]],
        is_derivable: Callable[[KPath], bool],
    ) -> KPath:
        unreached_paths = set(uncovered_paths)
        self._update_open_below(unreached_paths)
        candidates = self._targets_up_to_current_length(
            unreached_paths, is_derivable
        ) or list(filter(is_derivable, self._open_below))
        if len(candidates) == 0:
            derivable_scores = [
                (message, score)
                for message, score in coverage_scores
                if is_derivable((message,))
            ]
            return (self._least_covered_message(derivable_scores or coverage_scores),)
        s_ps = self._state_path_power_schedule
        s_ps.assign_energy_k_path(candidates)
        selected_path = s_ps.choose()
        s_ps.add_past_target(selected_path)
        self._picks[selected_path] += 1
        return selected_path

    def _targets_up_to_current_length(
        self, unreached: set[KPath], is_derivable: Callable[[KPath], bool]
    ) -> list[KPath]:
        """
        The derivable unreached targets up to the current length.
        The current length is the shortest one with a target picked fewer than MAX_PICKS times.
        """
        unreached_by_length: dict[int, list[KPath]] = defaultdict(list)
        for target in self._open_below:
            if target in unreached:
                unreached_by_length[len(target)].append(target)
        candidates: list[KPath] = []
        for length in sorted(unreached_by_length):
            derivable = list(filter(is_derivable, unreached_by_length[length]))
            candidates.extend(derivable)
            if any(self._picks[target] < self.MAX_PICKS for target in derivable):
                return candidates
        return []

    def _update_open_below(self, uncovered: set[KPath]) -> None:
        """Updated the cached counts of k-paths that are currently uncovered."""
        newly_uncovered = uncovered - self._uncovered
        newly_covered = self._uncovered - uncovered
        for path in newly_uncovered:
            target = self._state_target_of(path)
            if len(target) != 0:
                self._open_below[target] += 1
        for path in newly_covered:
            target = self._state_target_of(path)
            if len(target) != 0:
                self._open_below[target] -= 1
                if self._open_below[target] == 0:
                    del self._open_below[target]
        self._uncovered = uncovered

    def is_every_path_underivable(
        self,
        uncovered_paths: list[KPath],
        is_derivable: Callable[[KPath], bool],
    ) -> bool:
        return not any(
            self._is_derivable_path(path, is_derivable) for path in uncovered_paths
        )

    def _is_derivable_path(
        self, path: KPath, is_derivable: Callable[[KPath], bool]
    ) -> bool:
        """True if the path trimmed to the state grammar, or else a message producing it, is derivable."""
        targets = self._trim_to_state_symbols([path]) or [
            (message,) for message in self._model.messages_producing(path[0])
        ]
        return any(map(is_derivable, targets))

    def _trim_to_state_symbols(self, uncovered_paths: list[KPath]) -> list[KPath]:
        """Trim each path back to its last state-grammar symbol; drop empties."""
        return [
            target
            for target in map(self._state_target_of, uncovered_paths)
            if len(target) > 0
        ]

    def _state_target_of(self, path: KPath) -> KPath:
        target = self._state_target_by_path.get(path)
        if target is None:
            path_last_state_cutoff = len(path) + 1
            in_state_area = True
            # Make sure that parts of the k-path are in the state area of the grammar. Ignore otherwise
            if len(path) > 0:
                first_symbol = path[0]
                if first_symbol not in self._model.state_grammar_symbols:
                    in_state_area = False
                    path_last_state_cutoff = 0
            if in_state_area:
                for path_idx, symbol in enumerate(path):
                    # Truncate k-path at first occurrence of a message symbol
                    if symbol in self._protocol_msg_symbols:
                        path_last_state_cutoff = path_idx + 1
                        break
            target = path[:path_last_state_cutoff]
            self._state_target_by_path[path] = target
        return target

    def _least_covered_message(
        self, coverage_scores: list[tuple[NonTerminal, float]]
    ) -> Symbol:
        message_coverage: dict[Symbol, float] = dict(coverage_scores)
        m_ps = self._msg_power_schedule
        m_ps.assign_energy_coverage(message_coverage)
        target = m_ps.choose()
        m_ps.add_past_target(target)
        return target
