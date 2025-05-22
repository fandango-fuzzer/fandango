import subprocess
import tempfile
import time
from typing import Tuple

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def is_syntactically_valid_csv(tree) -> bool:
    with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
        tmp.write(str(tree).encode())
        tmp.flush()

        cmd = ["csvlint", "-delimiter", ";", tmp.name]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,  # <--- capture stdout to suppress terminal output
            stderr=subprocess.PIPE,
        )
        (stdout, stderr) = process.communicate()
        exit_code = process.wait()

        err_msg = stderr.decode("utf-8")
        has_error = exit_code != 0 or (bool(err_msg) and "valid" not in err_msg)

        return not has_error


def evaluate_csv(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    grammar, constraints = parse_file("evaluation/vs_isla/csv_evaluation/csv.fan")
    solutions = []
    profiling_results = {}
    constraint_results = []
    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = FANDANGO(grammar, constraints, verbose=False, desired_solutions=100)
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
        solutions.extend(fandango.solution)
    # coverage = grammar.compute_grammar_coverage(solutions, 4)

    # valid = []
    # for solution in solutions:
    #     if is_syntactically_valid_csv(str(solution)):
    #         valid.append(solution)

    # set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    # set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    # valid_percentage = len(valid) / len(solutions) * 100
    return (
        "CSV",
        len(solutions),
        profiling_results,
        constraint_results,
        # len(valid),
        # valid_percentage,
        # 0,
        # set_mean_length,
        # set_medium_length,
    )
