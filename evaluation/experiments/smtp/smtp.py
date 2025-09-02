import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import FuzzingMode
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("smtp.fan") as f:
        grammar, constraints = parse(
            f,
            use_stdlib=False,
        )

    time_start = time.time()
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=100,
        diversity_k=5,
        logger_level=LoggerLevel.INFO,
    )

    overall_start = time.time()

    try:
        solutions = fandango.evolve()
        for solution in solutions:
            if solution.contains_bytes():
                print(bytes(solution))
            else:
                print(str(solution))
    finally:
        with open("grammar_coverage.csv", "w") as f:
            print("Coverage log:")
            for timestamp, coverage in fandango.coverage_log:
                time_elapsed = timestamp - time_start
                f.write(f"{time_elapsed},{coverage}\n")
        print(f"Nr trees generated: {len(fandango.packet_selector._all_derivation_trees())}")
        print(
            f"Nr messages exchanged: {sum(len(sol.protocol_msgs()) for sol in fandango.packet_selector._all_derivation_trees())}")
        print(f"Overall time elapsed: {time.time() - time_start:.2f}s")


if __name__ == "__main__":
    main()
