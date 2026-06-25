from typing import Optional

from fandango.io import FandangoIO
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.io.navigation.forecast_view import ForecastView
from fandango.io.navigation.kpath_coverage import KPathCoverage
from fandango.io.navigation.packet_guide import PacketGuide
from fandango.io.navigation.packetforecaster import (
    ForecastingPacket,
    ForecastingResult,
)
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.io.navigation.protocol_model import ProtocolModel
from fandango.io.navigation.target_selector import TargetSelector
from fandango.language.grammar.grammar import Grammar, KPath
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
        self.coverage_goal = CoverageGoal.STATE_INPUTS
        self.grammar = grammar
        self._model = ProtocolModel(grammar, self.start_symbol)
        self.io_instance = io_instance
        self._forecast = ForecastView(grammar, io_instance, lambda: self.history_tree)
        self.diversity_k = diversity_k
        self._coverage = KPathCoverage(grammar, diversity_k)
        self._target_selector = TargetSelector(grammar, self.start_symbol, self._model)
        self._guide = PacketGuide(
            self._model,
            self._forecast,
            PacketNavigator(grammar, self.start_symbol),
            self._target_selector,
            max_messages_per_tree=200,
        )
        self.parst_derivations: list[DerivationTree] = []
        self.history_tree: DerivationTree = DerivationTree(NonTerminal("<start>"))
        self._next_packets: Optional[list[ForecastingPacket]] = None
        self._coverage_scores: Optional[list[tuple[NonTerminal, float]]] = None
        self.compute(history_tree, self.parst_derivations)

    def _input_parties(self) -> set[str]:
        parties: set[str] = set()
        for party in self.io_instance.parties.values():
            if party.is_fuzzer_controlled():
                parties.add(party.party_name)
        return parties

    def _compute_coverage_score(
        self, k: int, overlap_to_root: bool = False
    ) -> list[tuple[NonTerminal, float]]:
        """
        Computes the coverage score for each NonTerminal in the given DerivationTrees.
        The score is the ratio of the number of trees containing the NonTerminal to the total number of trees.

        :param trees: List of DerivationTrees to analyze.
        :param k: The k-path length for coverage computation.
        :return: Dictionary mapping NonTerminals to their coverage scores.
        """
        messages_by_nt = self._model.group_messages_by_nt(self._all_derivation_trees())
        nt_coverage = {}
        for symbol in self._model.state_grammar_symbols:
            if symbol not in messages_by_nt:
                nt_coverage[symbol] = 0.0
                continue
            nt_coverage[symbol] = self._coverage.ratio(
                messages_by_nt[symbol], symbol, overlap_to_root=overlap_to_root
            )
        nt_coverage_list = list(
            sorted(nt_coverage.items(), key=lambda x: (x[1], x[0].name()))
        )
        return nt_coverage_list

    def compute(
        self, history_tree: DerivationTree, parst_derivations: list[DerivationTree]
    ) -> None:
        self.history_tree = history_tree
        self.parst_derivations = parst_derivations
        self._coverage_scores = None
        self._next_packets = None

    @property
    def forecasting_result(self) -> ForecastingResult:
        return self._forecast.result

    @property
    def coverage_scores(
        self,
    ) -> list[tuple[NonTerminal, float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_coverage_score(self.diversity_k)
        return self._coverage_scores

    def _ensure_next_packets(self) -> list[ForecastingPacket]:
        if self._next_packets is None:
            self._next_packets = self._guide.select_next_packet(
                self.history_tree,
                self.parst_derivations,
                self._uncovered_paths,
                lambda: self.coverage_scores,
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

    def _all_derivation_trees(self) -> list[DerivationTree]:
        all_derivation_trees = list(self.parst_derivations)
        all_derivation_trees.append(self.history_tree)
        return all_derivation_trees

    def _uncovered_paths(self) -> list[KPath]:
        return self._coverage.uncovered(
            self._all_derivation_trees(),
            self.start_symbol,
            coverage_goal=self.coverage_goal,
            input_parties=self._input_parties(),
        )

    def coverage_percent(self) -> float:
        u_paths = self._uncovered_paths()
        if len(u_paths) == 0:
            return 1.0
        all_paths = self._coverage.all_k_paths(
            coverage_goal=self.coverage_goal,
            input_parties=self._input_parties(),
        )
        if len(all_paths) == 0:
            return 1.0
        return 1.0 - (len(u_paths) / len(all_paths))

    def set_coverage_goal(self, goal: CoverageGoal) -> None:
        self.coverage_goal = goal
