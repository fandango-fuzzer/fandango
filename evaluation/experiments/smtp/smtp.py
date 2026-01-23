import time

from fandango.language.grammar import FuzzingMode
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    with open("smtp.fan") as f:
        grammar, constraints = parse(
            f,
            use_stdlib=False,
        )
    assert grammar is not None
    time_start = time.time()
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
    )

    solutions = []
    for solution in fandango.generate(mode=FuzzingMode.IO):
        print(str(solution))
        solutions.append(solution)
    time_end = time.time()
    print(f"Time taken: {time_end - time_start}")
    print(f"Nr. msg: {sum(len(x.protocol_msgs()) for x in solutions)}")
    print(f"Trees: {len(solutions)}")


if __name__ == "__main__":
    main()
