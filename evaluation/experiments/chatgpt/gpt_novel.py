import os
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import FuzzingMode
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("report.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=100,
        logger_level=LoggerLevel.INFO,
    )

    fandango.enable_guidance(False)
    time_start = time.time()
    try:
        for solution in fandango.generate(mode=FuzzingMode.IO):
            pass
    finally:
        for entry, value in fandango.packet_selector.coverage_scores:
            print(entry, value)

        current_id = 1
        while os.path.exists(f"coverage_raw/attempt_{current_id}_grammar_coverage.csv"):
            current_id += 1

        with open(f"coverage_raw/attempt_{current_id}_grammar_coverage.csv", "w") as f:
            for timestamp, coverage in fandango.coverage_log:
                time_elapsed = timestamp - time_start
                f.write(f"{time_elapsed},{coverage}\n")
        with open(f"coverage_raw/attempt_{current_id}_metrics.md", "w") as f:
            f.write("Coverage metrics:\n")
            f.write(f"Nr trees generated: {len(fandango.packet_selector._all_derivation_trees())}\n")
            f.write(
                f"Nr messages exchanged: {sum(len(sol.protocol_msgs()) for sol in fandango.packet_selector._all_derivation_trees())}\n")
            f.write(f"Overall time elapsed: {time.time() - time_start:.2f}s\n")


if __name__ == "__main__":
    main()
