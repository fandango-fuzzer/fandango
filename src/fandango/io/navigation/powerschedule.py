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

    def assign_energy_new(self, paths_covered_by_next_nt: dict[Symbol, int], direct_cover_symbols: dict[tuple[Symbol, ...], dict[str, Any]]):
        if len(direct_cover_symbols) != 0:
            pass

        points_by_next_nt = dict(paths_covered_by_next_nt)
        for path, packet in direct_cover_symbols.items():
            symbol = path[0]
            if symbol not in points_by_next_nt:
                points_by_next_nt[symbol] = 0
            points_by_next_nt[symbol] += packet['score'] * 10

        self.energy = dict()
        frequencies = Counter(self._past_targets)
        for symbol, points in points_by_next_nt.items():
            freq = frequencies[symbol] if symbol in frequencies else 1
            self.energy[symbol] = 1 / (freq ** self.exponent) * points
        self.energy = self._normalize_energy()


    def assign_energy(self, coverage: dict[NonTerminal, float]):
        frequencies = Counter(self._past_targets)
        self.energy = dict()

        for p_type, freq in frequencies.items():
            if p_type in coverage:
                coverage_val = coverage[p_type]
            else:
                coverage_val = 0.0
            self.energy[p_type] = (1.0 - coverage_val)
            #self.energy[p_type] = (1.0 - coverage_val)
        for p_type in coverage.keys():
            if p_type not in self.energy:
                self.energy[p_type] = 1 - coverage[p_type]
        self.energy = self._normalize_energy()

    def _normalize_energy(self) -> dict[NonTerminal, float]:
        sum_energy = sum(self.energy.values())
        if sum_energy == 0:
            # all energies are zero, assign uniform distribution
            n = len(self.energy)
            return dict(map(lambda item: (item[0], 1 / n), self.energy.items()))
        norm_energy = dict(
            map(lambda item: (item[0], item[1] / sum_energy), self.energy.items())
        )
        return norm_energy

    def choose(self) -> NonTerminal:
        energy_list = list(self.energy.items())
        key_list = list(map(lambda item: item[0], energy_list))
        value_list = list(map(lambda item: item[1], energy_list))
        return random.choices(key_list, weights=value_list, k=1)[0]

    def add_past_target(self, new_target):
        self._past_targets.append(new_target)
