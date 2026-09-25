import random
from typing import Optional

from fandango.constraints.failing_tree import Suggestion
from fandango.evolution.population import PopulationManager
from fandango.io.navigation.graph.packetforecaster import ForecastingPacket
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class IoPopulationManager(PopulationManager):
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str,
    ):
        super().__init__(grammar, start_symbol)
        self._prev_packet_idx = 0
        self.fuzzable_packets: list[ForecastingPacket] = []
        self.fallback_packets: list[ForecastingPacket] = []
        self.allow_fallback_packets = False
        self.packet_mounter = PacketMounter(grammar)

    def _generate_population_entry(self, max_nodes: int) -> DerivationTree:
        if self.fuzzable_packets is None or len(self.fuzzable_packets) == 0:
            return DerivationTree(NonTerminal(self._start_symbol))
        packet_selection = list(self.fuzzable_packets)
        if self.allow_fallback_packets:
            packet_selection.extend(self.fallback_packets)

        current_idx = (self._prev_packet_idx + 1) % len(packet_selection)
        current_pck = random.choice(packet_selection)
        mounting_option = random.choice(list(current_pck.paths))
        fuzzed_packet = self.packet_mounter.fuzz_attached(
            current_pck, mounting_option, max_nodes
        )

        self._prev_packet_idx = current_idx
        return fuzzed_packet

    def _apply_suggestion(
        self, individual: DerivationTree, suggestion: Optional[Suggestion]
    ) -> tuple[DerivationTree, int]:
        first_seen_packet = self.packet_mounter.first_seen_equal(individual)
        with self.packet_mounter.mount_context(first_seen_packet):
            fixed, fixes_made = super()._apply_suggestion(first_seen_packet, suggestion)
        return individual if fixed is first_seen_packet else fixed, fixes_made
