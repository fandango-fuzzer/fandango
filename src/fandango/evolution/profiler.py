import time


class Profiler:
    def __init__(self):
        self.metrics = {
            "initial_population": {"count": 0, "time": 0.0},
            "evaluate_population": {"count": 0, "time": 0.0},
            "select_elites": {"count": 0, "time": 0.0},
            "tournament_selection": {"count": 0, "time": 0.0},
            "filling": {"count": 0, "time": 0.0},
            "crossover": {"count": 0, "time": 0.0},
            "mutation": {"count": 0, "time": 0.0},
        }

    def start_timer(self, key: str):
        if key not in self.metrics or not isinstance(self.metrics[key], dict):
            self.metrics[key] = {}  # Ensure it's a dictionary before adding keys
        self.metrics[key]["_start_time"] = time.time()

    def stop_timer(self, key: str):
        if key not in self.metrics or not isinstance(self.metrics[key], dict):
            raise KeyError(f"Timer '{key}' was never started.")

        if "_start_time" not in self.metrics[key]:
            raise KeyError(f"Timer '{key}' does not have a start time.")

        elapsed = time.time() - self.metrics[key].pop("_start_time", 0)

        if "time" not in self.metrics[key]:
            self.metrics[key]["time"] = 0  # Initialize "time" if missing

        self.metrics[key]["time"] += elapsed

    def increment(self, key: str, count: int = 1):
        self.metrics[key]["count"] += count

    def log_results(self):
        for key, value in self.metrics.items():
            if isinstance(value, dict) and "time" in value and "count" in value:
                avg_time = value["time"] / value["count"] if value["count"] > 0 else 0
                print(
                    f"{key}: {avg_time:.6f}s per execution ({value['count']} runs, total {value['time']:.6f}s)"
                )
            else:
                print(f"Warning: '{key}' does not have valid time/count data.")
