import time
from io import StringIO
from typing import Tuple

from docutils.core import publish_doctree

from fandango.evolution.algorithm import FANDANGO
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
    grammar, constraints = parse_file("evaluation/vs_isla/rest_evaluation/rest.fan")
    solutions = []
    profiling_results = {}
    constraint_results = []
    time_in_an_hour = time.time() + seconds
    run = 0
    while time.time() < time_in_an_hour:
        fandango = FANDANGO(
            grammar,
            constraints,
            verbose=False,
            desired_solutions=100,
            subject="rest",
            run=run,
        )
        run += 1
        fandango.evolve()
        for key, value in fandango.profiler.metrics.items():
            if key in profiling_results:
                profiling_results[key]["count"] += value["count"]
                profiling_results[key]["time"] += value["time"]
            else:
                profiling_results[key] = {
                    "count": value["count"],
                    "time": value["time"],
                }
        constraint_results.extend(fandango.constraint_profile)
        with open(
            f"execution/rest/{run:10d}/profiling.txt",
            "w",
        ) as f:
            f.write(str(profiling_results))
        solutions.extend(fandango.solution)

    # coverage = grammar.compute_grammar_coverage(solutions, 4)

    # valid = []
    # for solution in solutions:
    #     if is_syntactically_valid_rest(str(solution)):
    #         valid.append(solution)

    # set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    # set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    # valid_percentage = len(valid) / len(solutions) * 100
    return (
        "REST",
        len(solutions),
        profiling_results,
        constraint_results,
        # len(valid),
        # valid_percentage,
        # 0,
        # set_mean_length,
        # set_medium_length,
    )
