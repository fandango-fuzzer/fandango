import os
import sys
import time

from evaluation.experiments.utils import write_coverage_log
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    sys.setrecursionlimit(10**6)
    # Parse grammar and constraints
    protocols = [("dune", "dune.fan"), ("smtp", "smtp_client.fan"), ("dns", "dns.fan"), ("ftp", "ftp_client.fan"), ("chatgpt", "chatgpt.fan")]
    for folder, spec in protocols:
        overall_max_coverage_guided = 0.0
        nr_failed_new_coverage = 0
        for enable_guidance in [True, False]:
            for _ in range(10):
                max_coverage_guided = 0.0
                with open(f"{folder}/{spec}") as f:
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
                fandango.coverage_log_interval = 20
                fandango.enable_guidance(enable_guidance)
                output_folder_name = f"{folder}/" + ("coverage_w_guidance" if enable_guidance else "coverage_wo_guidance")

                try:
                    for solution in fandango.generate(mode=FuzzingMode.IO):
                        if solution.contains_bytes():
                            print(bytes(solution))
                        else:
                            print(str(solution))
                        current_cov = fandango.packet_selector.coverage_percent(alt_cache=True)
                        if enable_guidance:
                            if current_cov > max_coverage_guided:
                                max_coverage_guided = current_cov
                                overall_max_coverage_guided = max(overall_max_coverage_guided, max_coverage_guided)
                                nr_failed_new_coverage = 0
                            else:
                                nr_failed_new_coverage += 1
                                if nr_failed_new_coverage >= 10:
                                    break
                        else:
                            if current_cov - overall_max_coverage_guided >= -0.0001:
                                break
                finally:
                    current_id = 1
                    os.path.exists(output_folder_name) or os.makedirs(output_folder_name)
                    while os.path.exists(f"{output_folder_name}/run_{current_id}_grammar_coverage.csv"):
                        current_id += 1
                    print("Writing coverage log to", f"{output_folder_name}/run_{current_id}_grammar_coverage.csv")
                    write_coverage_log(fandango, output_folder_name, current_id, time_start)

if __name__ == "__main__":
    main()
