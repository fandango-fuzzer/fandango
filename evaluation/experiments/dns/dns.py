import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import FuzzingMode
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("dns.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)

    time_start = time.time()
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=10,
        logger_level=LoggerLevel.INFO,
    )

    solution_count = 0
    for solution in fandango.generate(mode=FuzzingMode.IO):
        print(time.time() - time_start)
        if solution.contains_bytes():
            print(solution.to_bytes())
        else:
            print(solution.to_string())
        time_start = time.time()
        solution_count += 1
        if solution_count >= 10:
            break

if __name__ == "__main__":
    main()
