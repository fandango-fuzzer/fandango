import random
from collections import Counter
from typing import Sequence

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language.symbols.non_terminal import NonTerminal


class PowerSchedule:

    def __init__(self):
        self.energy = dict()
        self.exponent = 2.0

    def assign_energy(self, packet_types: Sequence[NonTerminal], coverage: dict[NonTerminal, float]):
        frequencies = Counter(packet_types)
        self.energy = dict()

        for p_type, freq in frequencies.items():
            if p_type in coverage:
                coverage_val = coverage[p_type]
            else:
                coverage_val = 0.0
            self.energy[p_type] = 1 / (freq**self.exponent) * (1 - coverage_val)
        for p_type in coverage.keys():
            if p_type not in self.energy:
                self.energy[p_type] = 1 - coverage[p_type]
        self.energy = self._normalize_energy()

    def _normalize_energy(self) -> dict[PacketNonTerminal, float]:
        sum_energy = sum(self.energy.values())
        assert sum_energy != 0
        norm_energy = dict(
            map(lambda item: (item[0], item[1] / sum_energy), self.energy.items())
        )
        return norm_energy

    def choose(self) -> NonTerminal:
        energy_list = list(self.energy.items())
        key_list = list(map(lambda item: item[0], energy_list))
        value_list = list(map(lambda item: item[1], energy_list))
        return random.choices(key_list, weights=value_list, k=1)[0]
