from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Metrics:
    time: float
    coverage: float


def _parse_last_row_metrics(csv_path: Path) -> Metrics | None:
    """Return time/coverage from the last non-empty row.

    Assumes the first two columns are time and overall coverage.
    """
    last_row: list[str] | None = None
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row or all(cell.strip() == "" for cell in row):
                continue
            last_row = row

    if not last_row or len(last_row) < 2:
        return None

    try:
        time_value = float(last_row[0])
        coverage_value = float(last_row[1])
    except ValueError:
        return None

    return Metrics(time=time_value, coverage=coverage_value)


def _pair_csvs(folder: Path) -> dict[str, dict[str, Path]]:
    pairs: dict[str, dict[str, Path]] = {}
    for csv_path in folder.glob("*.csv"):
        name = csv_path.name
        if name.endswith("_guided.csv"):
            base = name[: -len("_guided.csv")]
            pairs.setdefault(base, {})["guided"] = csv_path
        elif name.endswith("_unguided.csv"):
            base = name[: -len("_unguided.csv")]
            pairs.setdefault(base, {})["unguided"] = csv_path
    return pairs


def _percent_faster(unguided_time: float, guided_time: float) -> float:
    if unguided_time == 0:
        return 0.0
    return (unguided_time - guided_time) / unguided_time * 100.0


def _aggregate_speedup(folder: Path) -> tuple[float, list[str]]:
    pairs = _pair_csvs(folder)
    speedups: list[float] = []
    skipped: list[str] = []

    for base, files in sorted(pairs.items()):
        guided_path = files.get("guided")
        unguided_path = files.get("unguided")
        if not guided_path or not unguided_path:
            skipped.append(base)
            continue

        guided_metrics = _parse_last_row_metrics(guided_path)
        unguided_metrics = _parse_last_row_metrics(unguided_path)
        if not guided_metrics or not unguided_metrics:
            skipped.append(base)
            continue

        speedups.append(_percent_faster(unguided_metrics.time, guided_metrics.time))

    if not speedups:
        return 0.0, skipped

    avg_speedup = sum(speedups) / len(speedups)
    return avg_speedup, skipped


def main() -> None:
    workspace = Path(__file__).resolve().parent
    msgs_folder = workspace / "msgs"
    all_folder = workspace / "overall"

    msgs_speedup, msgs_skipped = _aggregate_speedup(msgs_folder)
    all_speedup, all_skipped = _aggregate_speedup(all_folder)

    print(f"msgs average guided speedup: {msgs_speedup:.2f}%")
    print(f"all average guided speedup: {all_speedup:.2f}%")

    if msgs_skipped:
        print("msgs skipped (missing or invalid pairs):", ", ".join(msgs_skipped))
    if all_skipped:
        print("all skipped (missing or invalid pairs):", ", ".join(all_skipped))


if __name__ == "__main__":
    main()
