from collections import Counter
from typing import Sequence

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal


class PowerSchedule:

    def __init__(self):
        self.energy = dict()
        self.exponent = 1.0

    def assign_energy(self, packet_types: Sequence[PacketNonTerminal]):
        frequencies = Counter(packet_types)
        self.energy = dict()
        for p_type, freq in frequencies.items():
            self.energy[p_type] = 1 / (freq ** self.exponent)

    def normalized_energy(self) -> dict[PacketNonTerminal, float]:
        sum_energy = sum(self.energy.values())
        assert sum_energy != 0
        norm_energy = dict(map(lambda item: (item[0], item[1] / sum_energy), self.energy.items()))
        return norm_energy

    def choose(self):
        pass