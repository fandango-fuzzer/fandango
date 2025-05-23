import time
import xml.etree.ElementTree as ET
from typing import Tuple

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def is_syntactically_valid_xml(xml_string):
    try:
        # Try to parse the XML string
        ET.fromstring(xml_string)
        return True
    except ET.ParseError:
        # If parsing fails, it's not a valid XML
        return False


def evaluate_xml(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    grammar, constraints = parse_file("evaluation/vs_isla/xml_evaluation/xml.fan")
    solutions = []
    run = 0
    profiling_results = {}
    constraint_results = []
    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = FANDANGO(
            grammar,
            constraints,
            verbose=False,
            desired_solutions=100,
            subject="xml",
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
            f"execution/xml/{run:10d}/profiling.txt",
            "w",
        ) as f:
            f.write(str(profiling_results))
        solutions.extend(fandango.solution)

    # coverage = grammar.compute_grammar_coverage(solutions, 4)

    # valid = []
    # for solution in solutions:
    #     if is_syntactically_valid_xml(str(solution)):
    #         valid.append(solution)

    # set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    # set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    # valid_percentage = len(valid) / len(solutions) * 100
    return (
        "XML",
        len(solutions),
        profiling_results,
        constraint_results,
        # len(valid),
        # valid_percentage,
        # 0,
        # set_mean_length,
        # set_medium_length,
    )
