import os
import time

from evaluation.experiments.utils import write_coverage_log
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    protocols = ["ftp"]
    for protocol in protocols:
        for _ in range(10):
            with open(f"{protocol}/{protocol}.fan") as f:
                grammar, constraints = parse(
                    f,
                    use_stdlib=False,
                )
            assert grammar is not None

            time_start = time.time()
            fandango = Fandango(
                grammar=grammar,
                constraints=constraints,
                logger_level=LoggerLevel.INFO,
                coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS
            )
            fandango.enable_guidance(True)
            output_folder_name = f"{protocol}/" + ("coverage_w_guidance" if fandango._is_enable_guidance else "coverage_wo_guidance")

            try:
                for solution in fandango.generate(mode=FuzzingMode.IO):
                    if solution.contains_bytes():
                        print(bytes(solution))
                    else:
                        print(str(solution))
            finally:
                current_id = 1
                while os.path.exists(f"{output_folder_name}/run_{current_id}_grammar_coverage.csv"):
                    current_id += 1
                write_coverage_log(fandango, output_folder_name, current_id, time_start)

if __name__ == "__main__":
    main()
