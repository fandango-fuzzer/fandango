import time
from io import StringIO
from typing import Tuple

from docutils.core import publish_doctree

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse_file


def is_syntactically_valid_rest(rst_string):
    # StringIO to capture output messages (warnings, errors, etc.)
    error_stream = StringIO()

    try:
        # Parse the reST string into a document tree, capturing system messages
        doctree = publish_doctree(
            rst_string, settings_overrides={"warning_stream": error_stream}
        )

        # Check if any errors or warnings were captured in the error stream
        errors_warnings = error_stream.getvalue().strip()

        if errors_warnings:
            return False

        return True

    except:
        return False


def evaluate_rest(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    grammar, constraints = parse_file("rest_evaluation/rest.fan")
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
        if is_syntactically_valid_rest(str(solution)):
            valid.append(solution)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "REST",
        len(solutions),
        len(valid),
        valid_percentage,
        coverage,
        set_mean_length,
        set_medium_length,
    )
