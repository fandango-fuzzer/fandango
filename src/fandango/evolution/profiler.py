import time
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Union
from collections.abc import Generator


class Timer(ABC):
    """Abstract base class for timing operations."""

    def __init__(self, profiler: "Profiler", key: str):
        self.profiler = profiler
        self.key = key
        self._start_time = time.time()

    @abstractmethod
    def increment(self, count: int = 1) -> None:
        """Increment the count for this metric."""
        pass

    @abstractmethod
    def _stop(self) -> None:
        """Stop the timer and record the elapsed time."""
        pass


class EnabledTimer(Timer):
    """Timer implementation for when profiling is enabled."""

    def _stop(self) -> None:
        elapsed = time.time() - self._start_time
        if "time" not in self.profiler.metrics[self.key]:
            self.profiler.metrics[self.key]["time"] = 0
        self.profiler.metrics[self.key]["time"] += elapsed

    def increment(self, count: int = 1) -> None:
        if not self.profiler.enabled:
            return

        if "count" not in self.profiler.metrics[self.key]:
            self.profiler.metrics[self.key]["count"] = 0
        self.profiler.metrics[self.key]["count"] += count


class DisabledTimer(Timer):
    """No-op timer implementation for when profiling is disabled."""

    def __init__(self, profiler: "Profiler", key: str):
        pass

    def increment(self, count: int = 1) -> None:
        pass

    def _stop(self) -> None:
        pass


class Profiler:
    """A profiling utility for tracking execution times and counts."""

    def __init__(self, enabled: bool):
        self.enabled = enabled
        self.metrics: dict[str, dict[str, Union[int, float]]] = {
            "initial_population": {"count": 0, "time": 0.0},
            "evaluate_population": {"count": 0, "time": 0.0},
            "select_elites": {"count": 0, "time": 0.0},
            "tournament_selection": {"count": 0, "time": 0.0},
            "filling": {"count": 0, "time": 0.0},
            "crossover": {"count": 0, "time": 0.0},
            "mutation": {"count": 0, "time": 0.0},
        }

    @contextmanager
    def timer(
        self, key: str, increment: Union[int, list[Any], None] = None
    ) -> Generator[Timer, None, None]:
        """Context manager for profiling operations.

        :param key: The metric key to track
        :param increment: Either an integer, a list the length which will be used as the increment value.
        :yields: A timer object that can be used to increment the metric if it has to be calculated manually.
        """
        timer = EnabledTimer(self, key) if self.enabled else DisabledTimer(self, key)
        try:
            yield timer
        finally:
            if self.enabled:
                timer._stop()
                # Calculate increment value after operation completes
                if isinstance(increment, list):
                    timer.increment(len(increment))
                elif isinstance(increment, int):
                    timer.increment(increment)
                elif increment is not None:
                    raise ValueError(f"Invalid increment value: {increment}")

    def log_results(self) -> None:
        """Log the profiling results."""
        if not self.enabled:
            return

        for key, value in self.metrics.items():
            if isinstance(value, dict) and "time" in value and "count" in value:
                avg_time = value["time"] / value["count"] if value["count"] > 0 else 0
                print(
                    f"{key}: {avg_time:.6f}s per execution ({value['count']} runs, total {value['time']:.6f}s)"
                )
            else:
                print(f"Warning: '{key}' does not have valid time/count data.")
