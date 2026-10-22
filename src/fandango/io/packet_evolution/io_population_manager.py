import random
from typing import Optional

from fandango.constraints.failing_tree import Suggestion
from fandango.evolution.population import PopulationManager
from fandango.io.navigation.forecasting.forecasting_result import ForecastingPacket
from fandango.io.packet_evolution.packet_mounter import PacketMounter
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class IoPopulationManager(PopulationManager):
    def __init__(
        self,
        packet_mounter: PacketMounter,
        grammar: Grammar,
        start_symbol: str,
    ):
        super().__init__(grammar, start_symbol)
        self._prev_packet_idx = 0
        self.fuzzable_packets: list[ForecastingPacket] = []
        self.fallback_packets: list[ForecastingPacket] = []
        self.allow_fallback_packets = False
        self.packet_mounter = packet_mounter

    def individual_hash(self, individual: DerivationTree) -> int:
        mount_point = individual.parent
        return hash((mount_point and mount_point.get_root(), individual))

    def _generate_population_entry(self, max_nodes: int) -> DerivationTree:
        packet_selection = list(self.fuzzable_packets)
        if self.allow_fallback_packets:
            packet_selection.extend(self.fallback_packets)
        if len(packet_selection) == 0:
            return DerivationTree(NonTerminal(self._start_symbol))

        current_idx = (self._prev_packet_idx + 1) % len(packet_selection)
        current_pck = random.choice(packet_selection)
        mounting_option = random.choice(list(current_pck.paths))
        mount_point = self.packet_mounter.mount_point(mounting_option)
        current_pck.node.fuzz(mount_point, self._grammar, max_nodes)
        fuzzed_packet = mount_point.children[-1]
        self.packet_mounter.attach(fuzzed_packet, mounting_option)

        self._prev_packet_idx = current_idx
        return fuzzed_packet

    def _apply_suggestion(
        self, individual: DerivationTree, suggestion: Optional[Suggestion]
    ) -> tuple[DerivationTree, int]:
        with self.packet_mounter.mounted_context(individual) as mounted_packet:
            fixed, fixes_made = super()._apply_suggestion(mounted_packet, suggestion)
            return self.packet_mounter.original(fixed), fixes_made
