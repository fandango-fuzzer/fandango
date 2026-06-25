from fandango.io.navigation.coverage.powerschedule import (
    PowerScheduleCoverage,
    PowerScheduleKPath,
)
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal, Symbol


class TargetSelector:
    """Picks the next k-path to guide toward."""

    def __init__(
        self, grammar: Grammar, start_symbol: NonTerminal, model: ProtocolModel
    ):
        self._grammar = grammar
        self._start_symbol = start_symbol
        self._model = model
        self._msg_power_schedule = PowerScheduleCoverage()
        self._state_path_power_schedule = PowerScheduleKPath()

    def select(
        self,
        uncovered_paths: list[KPath],
        coverage_scores: list[tuple[NonTerminal, float]],
    ) -> KPath:
        uncovered_paths = self._trim_to_state_symbols(uncovered_paths)
        if len(uncovered_paths) == 0:
            return (self._least_covered_message(coverage_scores),)
        s_ps = self._state_path_power_schedule
        s_ps.assign_energy_k_path(uncovered_paths)
        selected_path = s_ps.choose()
        s_ps.add_past_target(selected_path)
        return selected_path

    def _trim_to_state_symbols(self, uncovered_paths: list[KPath]) -> list[KPath]:
        """Trim each path back to its last state-grammar symbol; drop empties."""
        uncovered_paths = list(uncovered_paths)
        for list_idx, path in enumerate(list(uncovered_paths)):
            remaining_path = path
            for path_idx, symbol in enumerate(path[::-1]):
                if symbol in self._model.state_grammar_symbols:
                    break
                last_idx = len(path) - path_idx - 1
                remaining_path = remaining_path[:last_idx]
            uncovered_paths[list_idx] = remaining_path
        return list(filter(lambda x: len(x) > 0, uncovered_paths))

    def _least_covered_message(
        self, coverage_scores: list[tuple[NonTerminal, float]]
    ) -> Symbol:
        protocol_msgs = self._grammar.get_protocol_messages(self._start_symbol)
        message_nts = set(map(lambda x: x.symbol, protocol_msgs))
        message_coverage: dict[Symbol, float] = dict(
            filter(lambda x: x[0] in message_nts, coverage_scores)
        )
        m_ps = self._msg_power_schedule
        m_ps.assign_energy_coverage(message_coverage)
        target = m_ps.choose()
        m_ps.add_past_target(target)
        return target
