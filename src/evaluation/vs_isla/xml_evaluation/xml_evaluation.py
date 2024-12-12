import time
import xml.etree.ElementTree as ET
from typing import Tuple

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse_file


def is_syntactically_valid_xml(xml_string):
    try:
        # Try to parse the XML string
        ET.fromstring(xml_string)
        return True
    except ET.ParseError as e:
        # If parsing fails, it's not a valid XML
        return False


def evaluate_xml(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    grammar, constraints = parse_file("xml_evaluation/xml.fan")
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
        if is_syntactically_valid_xml(str(solution)):
            valid.append(solution)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "XML",
        len(solutions),
        len(valid),
        valid_percentage,
        coverage,
        set_mean_length,
        set_medium_length,
    )
