import os
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    with open("dune.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    assert grammar is not None
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
    )

    is_enable_guidance = True
    output_folder_name = (
        "coverage_w_guidance" if is_enable_guidance else "coverage_wo_guidance"
    )

    time_start = time.time()
    try:
        for solution in fandango.generate(mode=FuzzingMode.IO):
            pass
    finally:
        current_id = 1
        while os.path.exists(
            f"{output_folder_name}/run_{current_id}_grammar_coverage.csv"
        ):
            current_id += 1


if __name__ == "__main__":
    main()
