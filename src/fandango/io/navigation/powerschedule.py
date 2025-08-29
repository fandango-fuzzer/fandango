import random
from collections import Counter
from typing import Any

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language import Symbol
from fandango.language.symbols.non_terminal import NonTerminal


class PowerSchedule:
    def __init__(self):
        self.energy = dict()
        self._past_targets = []
        self.exponent = 0.7

    def _normalize_energy(self) -> dict[NonTerminal, float]:
        sum_energy = sum(self.energy.values())
        if sum_energy == 0:
            n = len(self.energy)
            return dict(map(lambda item: (item[0], 1 / n), self.energy.items()))
        norm_energy = dict(
            map(lambda item: (item[0], item[1] / sum_energy), self.energy.items())
        )
        return norm_energy

    def choose(self):
        energy_list = list(self.energy.items())
        key_list = list(map(lambda item: item[0], energy_list))
        value_list = list(map(lambda item: item[1], energy_list))
        return random.choices(key_list, weights=value_list, k=1)[0]

    def add_past_target(self, new_target):
        self._past_targets.append(new_target)

class PowerScheduleKPath(PowerSchedule):
    def __init__(self):
        super().__init__()

    def assign_energy_k_path(self, k_paths: list[tuple[Symbol, ...]]):
        frequencies = Counter(self._past_targets)
        self.energy = dict()
        for path, freq in frequencies.items():
            self.energy[path] = (1 / (freq ** self.exponent))
        for path in k_paths:
            if path not in self.energy:
                self.energy[path] = 1
        self.energy = self._normalize_energy()

class PowerScheduleCoverage(PowerSchedule):
    def __init__(self):
        super().__init__()

    def assign_energy_coverage(self, coverage: dict[NonTerminal, float]):
        frequencies = Counter(self._past_targets)
        self.energy = dict()
        for p_type, freq in frequencies.items():
            if p_type in coverage:
                coverage_val = coverage[p_type]
            else:
                coverage_val = 0.0
            self.energy[p_type] = (1 / (freq ** self.exponent)) * (1.0 - coverage_val)
        for p_type in coverage.keys():
            if p_type not in self.energy:
                self.energy[p_type] = 1 - coverage[p_type]
        self.energy = self._normalize_energy()