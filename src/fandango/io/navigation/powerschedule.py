import random
from collections import Counter
from typing import TypeVar, Generic
import abc

from fandango.language.symbols import Symbol
from fandango.language.grammar.grammar import KPath

ScheduleType = TypeVar("ScheduleType")


class PowerSchedule(abc.ABC, Generic[ScheduleType]):
    def __init__(self) -> None:
        self.energy: dict[ScheduleType, float] = dict()
        self._past_targets: list[ScheduleType] = []
        self.exponent = 0.7

    def _normalize_energy(self) -> dict[ScheduleType, float]:
        sum_energy = sum(self.energy.values())
        if sum_energy == 0:
            n = len(self.energy)
            return dict(map(lambda item: (item[0], 1 / n), self.energy.items()))
        norm_energy = dict(
            map(lambda item: (item[0], item[1] / sum_energy), self.energy.items())
        )
        return norm_energy

    def choose(self) -> ScheduleType:
        energy_list = list(self.energy.items())
        key_list = list(map(lambda item: item[0], energy_list))
        value_list = list(map(lambda item: item[1], energy_list))
        return random.choices(key_list, weights=value_list, k=1)[0]

    def add_past_target(self, new_target: ScheduleType) -> None:
        self._past_targets.append(new_target)


class PowerScheduleKPath(PowerSchedule[KPath]):
    def __init__(self) -> None:
        super().__init__()

    def assign_energy_k_path(self, k_paths: list[tuple[Symbol, ...]]) -> None:
        frequencies = Counter(self._past_targets)
        self.energy = dict()
        for path in k_paths:
            if path not in frequencies:
                self.energy[path] = len(path)
            else:
                self.energy[path] = 1 / (frequencies[path] ** self.exponent) * len(path)
        self.energy = self._normalize_energy()


class PowerScheduleCoverage(PowerSchedule[Symbol]):
    def __init__(self) -> None:
        super().__init__()

    def assign_energy_coverage(self, coverage: dict[Symbol, float]) -> None:
        frequencies = Counter(self._past_targets)
        self.energy = dict()
        for p_type, freq in frequencies.items():
            if p_type in coverage:
                coverage_val = coverage[p_type]
            else:
                coverage_val = 0.0
            self.energy[p_type] = (1 / (freq**self.exponent)) * (1.0 - coverage_val)
        for p_type in coverage.keys():
            if p_type not in self.energy:
                self.energy[p_type] = 1 - coverage[p_type]
        self.energy = self._normalize_energy()
