import csv
import time
from io import StringIO
from typing import Tuple

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse_file
from fandango.logger import LOGGER


def is_syntactically_valid_csv(csv_string):
    try:
        # Create a file-like object from the string
        csv_file = StringIO(csv_string)

        # Create a CSV reader to parse the string
        reader = csv.reader(csv_file)

        # Iterate through the reader to trigger any parsing errors
        for row in reader:
            pass

        # If no errors, it's a valid CSV syntactically
        return True
    except csv.Error as e:
        # If there's a CSV parsing error, it's not valid
        return False


def evaluate_csv(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    grammar, constraints = parse_file("csv_evaluation/csv.fan")
    solutions = []

    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = Fandango(
            grammar, constraints, desired_solutions=100, logger_level=LoggerLevel.ERROR
        )
        fandango.evolve()
        solutions.extend(fandango.solution)

    coverage = grammar.compute_grammar_coverage(solutions, 4)

    valid = []
    for solution in solutions:
        if is_syntactically_valid_csv(str(solution)):
            valid.append(solution)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "CSV",
        len(solutions),
        len(valid),
        valid_percentage,
        coverage,
        set_mean_length,
        set_medium_length,
    )
