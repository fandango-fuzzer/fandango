import time
from io import StringIO

from docutils.core import publish_doctree

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


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

    except Exception:
        return False


def evaluate_rest(
    seconds=60,
) -> tuple[str, int, int, float, tuple[float, int, int], float, float]:
    with open("evaluation/rest/rest.fan", "r") as file:
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


if __name__ == "__main__":
    result = evaluate_rest(seconds=10)
    print(
        f"Type: {result[0]}, "
        f"Solutions: {result[1]}, "
        f"Valid: {result[2]}, "
        f"Valid Percentage: {result[3]:.2f}%, "
        f"Coverage: {result[4]}, "
        f"Mean Length: {result[5]:.2f}, "
        f"Medium Length: {result[6]:.2f}"
    )
