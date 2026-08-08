from typing import Optional

from fandango.io import FandangoIO
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.graph.packetforecaster import (
    ForecastingPacket,
    ForecastingResult,
)
from fandango.io.navigation.graph.packetnavigator import PacketNavigator
from fandango.io.navigation.selection.coverage_tracker import CoverageTracker
from fandango.io.navigation.selection.forecast_view import ForecastView
from fandango.io.navigation.selection.packet_guide import PacketGuide
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.io.navigation.selection.target_selector import TargetSelector
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class PacketSelector:
    def __init__(
        self,
        grammar: Grammar,
        io_instance: FandangoIO,
        history_tree: DerivationTree,
        diversity_k: int,
    ):
        self.start_symbol = NonTerminal("<start>")
        self.grammar = grammar
        self.io_instance = io_instance
        self._model = ProtocolModel(grammar, self.start_symbol)
        self._forecast = ForecastView(grammar, io_instance, lambda: self.history_tree)
        self._target_selector = TargetSelector(grammar, self.start_symbol, self._model)
        self._guide = PacketGuide(
            self._model,
            self._forecast,
            PacketNavigator(grammar, self.start_symbol),
            self._target_selector,
            max_messages_per_tree=200,
        )
        self.history_tree: DerivationTree = DerivationTree(NonTerminal("<start>"))
        self._last_completed_tree: Optional[DerivationTree] = None
        self._completed_count = 0
        self._coverage_tracker = CoverageTracker(
            grammar,
            diversity_k,
            self._model,
            self.start_symbol,
            self._input_parties,
            lambda: self.history_tree,
            CoverageGoal.STATE_INPUTS,
        )
        self._next_packets: Optional[list[ForecastingPacket]] = None
        self._is_enable_guidance = True
        self.compute(history_tree)

    def _input_parties(self) -> set[str]:
        parties: set[str] = set()
        for party in self.io_instance.parties.values():
            if party.is_fuzzer_controlled():
                parties.add(party.party_name)
        return parties

    def compute(self, history_tree: DerivationTree) -> None:
        self.history_tree = history_tree
        self._coverage_tracker.invalidate()
        self._next_packets = None

    def add_completed_tree(self, tree: DerivationTree) -> None:
        """Fold a finished protocol run into the coverage basis."""
        self.record_coverage(tree)
        self._last_completed_tree = tree
        self._completed_count += 1

    def record_coverage(self, tree: DerivationTree) -> None:
        self._coverage_tracker.add_completed_tree(tree)

    def reset_coverage(self) -> None:
        self._coverage_tracker.reset()
        self._last_completed_tree = None
        self._completed_count = 0

    @property
    def forecasting_result(self) -> ForecastingResult:
        return self._forecast.result

    def enable_guidance(self, enable: bool) -> None:
        self._is_enable_guidance = enable

    def _ensure_next_packets(self) -> list[ForecastingPacket]:
        if self._next_packets is None:
            if not self._is_enable_guidance:
                self._next_packets = self.get_fuzzer_packets()
            else:
                self._next_packets = self._guide.select_next_packet(
                    self.history_tree,
                    self._last_completed_tree,
                    self._completed_count,
                    self._coverage_tracker.uncovered_paths,
                    self._coverage_tracker.coverage_scores,
                )
        return self._next_packets

    @property
    def next_packets(self) -> list[ForecastingPacket]:
        return self._ensure_next_packets()

    def is_guide_to_end(self) -> bool:
        self._ensure_next_packets()
        return self._guide.is_guide_to_end

    def is_complete(self) -> bool:
        return self._forecast.is_complete()

    def next_fuzzer_parties(
        self,
        show_fuzzer_controlled: bool = True,
        show_external_controlled: bool = False,
    ) -> list[str]:
        return self._forecast.next_fuzzer_parties(
            show_fuzzer_controlled, show_external_controlled
        )

    def get_fuzzer_packets(self) -> list[ForecastingPacket]:
        return self._forecast.get_fuzzer_packets()

    def next_external_parties(self) -> list[str]:
        return self._forecast.next_external_parties()

    def get_next_parties(self) -> list[str]:
        return self._forecast.get_next_parties()

    def coverage_percent(self, *, alt_cache: bool = False) -> float:
        return self._coverage_tracker.coverage_percent(alt_cache=alt_cache)

    def _compute_coverage_trees(
        self, overlap_to_root: bool = False
    ) -> dict[NonTerminal, tuple[int, int]]:
        return self._coverage_tracker.coverage_trees(overlap_to_root)

    def set_coverage_goal(self, goal: CoverageGoal) -> None:
        self._coverage_tracker.set_coverage_goal(goal)
