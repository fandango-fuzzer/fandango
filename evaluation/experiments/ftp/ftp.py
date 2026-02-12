import os
import sys
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import FuzzingMode
from evaluation.experiments.utils import write_coverage_log
from fandango.language.parse.parse import parse


def main():
    sys.setrecursionlimit(10**6)
    for _ in range(10):
        # Parse grammar and constraints
        with open("ftp_client.fan") as f:
            grammar, constraints = parse(f, use_stdlib=True)
        assert grammar is not None
        fandango = Fandango(
            grammar=grammar,
            constraints=constraints,
            logger_level=LoggerLevel.INFO,
        )
        fandango.enable_guidance(True)
        is_enable_guidance = True
        output_folder_name = (
            "coverage_w_guidance" if fandango._is_enable_guidance else "coverage_wo_guidance"
        )

        time_start = time.time()
        try:
            for solution in fandango.generate(mode=FuzzingMode.IO):
                pass
        finally:
            current_id = 1
            while os.path.exists(f"{output_folder_name}/run_{current_id}_grammar_coverage.csv"):
                current_id += 1
            write_coverage_log(fandango, output_folder_name, current_id, time_start)


if __name__ == "__main__":
    main()
