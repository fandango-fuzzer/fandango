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
        logger_level=LoggerLevel.INFO,
    )

    # Output solutions
    solution_count = 0
    overall_start = time.time()
    for solution in fandango.generate(mode=FuzzingMode.IO):
        print(time.time() - time_start)
        if solution.contains_bytes():
            print(solution.to_bytes())
        else:
            print(solution.to_string())
        time_start = time.time()
        solution_count += 1
        if solution_count >= 10 and False:
            break

    print(f"Overall time: {time.time() - overall_start:.4f} seconds")


if __name__ == "__main__":
    main()
