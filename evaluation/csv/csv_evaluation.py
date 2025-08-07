import csv
import time
from io import StringIO

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


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
    except csv.Error:
        # If there's a CSV parsing error, it's not valid
        return False


def evaluate_csv(
    seconds=60,
) -> tuple[str, int, int, float, tuple[float, int, int], float, float]:
    with open("evaluation/csv/csv.fan", "r") as file:
        grammar, constraints = parse(file, use_stdlib=False)
        assert grammar is not None

    solutions = []

    time_in_an_hour = time.time() + seconds

    fandango = Fandango(grammar, constraints, logger_level=LoggerLevel.ERROR)
    fan_gen = fandango.generate()
    for solution in fan_gen:
        solutions.append(solution)
        if time.time() >= time_in_an_hour:
            break

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


if __name__ == "__main__":
    result = evaluate_csv(seconds=10)
    print(
        f"Type: {result[0]}, "
        f"Solutions: {result[1]}, "
        f"Valid: {result[2]}, "
        f"Valid Percentage: {result[3]:.2f}%, "
        f"Coverage: {result[4]}, "
        f"Mean Length: {result[5]:.2f}, "
        f"Medium Length: {result[6]:.2f}"
    )
