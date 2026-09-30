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

    def __init__(self, model: ProtocolModel):
        self._model = model
        self._msg_power_schedule = PowerScheduleCoverage()
        self._state_path_power_schedule = PowerScheduleKPath()

    def reset(self) -> None:
        """Forget the targets chosen so far, as after construction."""
        self._msg_power_schedule = PowerScheduleCoverage()
        self._state_path_power_schedule = PowerScheduleKPath()

    def select(
        self,
        uncovered_paths: list[KPath],
        coverage_scores: list[tuple[NonTerminal, float]],
        is_derivable: Callable[[KPath], bool],
    ) -> KPath:
        uncovered_paths = list(
            filter(is_derivable, self._trim_to_state_symbols(uncovered_paths))
        )
        if len(uncovered_paths) == 0:
            derivable_scores = [
                (message, score)
                for message, score in coverage_scores
                if is_derivable((message,))
            ]
            return (self._least_covered_message(derivable_scores or coverage_scores),)
        s_ps = self._state_path_power_schedule
        s_ps.assign_energy_k_path(uncovered_paths)
        selected_path = s_ps.choose()
        s_ps.add_past_target(selected_path)
        return selected_path

    def is_every_path_underivable(
        self,
        uncovered_paths: list[KPath],
        is_derivable: Callable[[KPath], bool],
    ) -> bool:
        trimmed_paths = self._trim_to_state_symbols(uncovered_paths)
        return len(trimmed_paths) == len(uncovered_paths) and not any(
            map(is_derivable, trimmed_paths)
        )

    def _trim_to_state_symbols(self, uncovered_paths: list[KPath]) -> list[KPath]:
        """Trim each path back to its last state-grammar symbol; drop empties."""
        uncovered_paths = list(uncovered_paths)
        protocol_msg_symbols = set(
            map(lambda x: x.symbol, self._model.protocol_msg_symbols)
        )
        for list_idx, path in enumerate(list(uncovered_paths)):
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
                    if symbol in protocol_msg_symbols:
                        path_last_state_cutoff = path_idx + 1
                        break
            remaining_path = path[:path_last_state_cutoff]
            uncovered_paths[list_idx] = remaining_path
        return list(filter(lambda x: len(x) > 0, uncovered_paths))

    def _least_covered_message(
        self, coverage_scores: list[tuple[NonTerminal, float]]
    ) -> Symbol:
        message_coverage: dict[Symbol, float] = dict(coverage_scores)
        m_ps = self._msg_power_schedule
        m_ps.assign_energy_coverage(message_coverage)
        target = m_ps.choose()
        m_ps.add_past_target(target)
        return target
