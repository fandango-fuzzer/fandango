import os
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("ftp.fan") as f:
        grammar, constraints = parse(f, use_stdlib=True)

    time_start = time.time()
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=100,
        logger_level=LoggerLevel.INFO,
    )

    try:
        solutions = fandango.evolve()
        for solution in solutions:
            if solution.contains_bytes():
                print(bytes(solution))
            else:
                print(str(solution))
    finally:
        current_id = 1
        while os.path.exists(f"attempt_{current_id}_grammar_coverage.csv"):
            current_id += 1

        with open(f"attempt_{current_id}_grammar_coverage.csv", "w") as f:
            print("Coverage log:")
            for timestamp, coverage in fandango.coverage_log:
                time_elapsed = timestamp - time_start
                f.write(f"{time_elapsed},{coverage}\n")
        with open(f"attempt_{current_id}_metrics.md", "w") as f:
            f.write("Coverage metrics:")
            f.write(f"Nr trees generated: {len(fandango.packet_selector._all_derivation_trees())}")
            f.write(
                f"Nr messages exchanged: {sum(len(sol.protocol_msgs()) for sol in fandango.packet_selector._all_derivation_trees())}")
            f.write(f"Overall time elapsed: {time.time() - time_start:.2f}s")


if __name__ == "__main__":
    main()
