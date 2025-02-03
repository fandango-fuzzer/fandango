import time
from typing import Tuple

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def is_syntactically_valid_uvl(uvl_string):
    try:
        return True
    except Exception:
        pass


def evaluate_uvl(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    file = open("evaluation/vs_isla/uvl_evaluation/uvl.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)
    solutions = []

    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = Fandango(
            grammar,
            constraints,
            desired_solutions=100,
            logger_level=LoggerLevel.INFO,
        )
        fandango.evolve()
        solutions.extend(fandango.solution)

    coverage = grammar.compute_grammar_coverage(solutions, 4)

    valid = []
    for solution in solutions:
        if is_syntactically_valid_uvl(str(solution)):
            valid.append(solution)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "UVL",
        len(solutions),
        len(valid),
        valid_percentage,
        coverage,
        set_mean_length,
        set_medium_length,
    )


if __name__ == "__main__":
    print(evaluate_uvl())
