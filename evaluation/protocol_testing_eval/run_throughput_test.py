import os
import sys
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    sys.setrecursionlimit(10**6)
    protocols = [("dune", "dune.fan"), ("smtp", "smtp_client.fan"), ("dns", "dns.fan"), ("ftp", "ftp_client.fan"), ("chatgpt", "chatgpt.fan")]
    experiment_time_in_s = 3600
    for folder, spec in protocols:
        start_time = time.time()
        with open(f"{folder}/{spec}") as f:
            grammar, constraints = parse(
                f,
                use_stdlib=False,
            )
        assert grammar is not None
        fandango = Fandango(
            grammar=grammar,
            constraints=constraints,
            logger_level=LoggerLevel.INFO,
            coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS
        )
        fandango.stop_on_full_coverage = False
        fandango.enable_guidance(True)
        output_folder_name = f"{folder}/throughput_test"

        try:
            for _ in fandango.generate(mode=FuzzingMode.IO):
                if start_time + experiment_time_in_s < time.time():
                    break
        finally:
            current_id = 1
            os.path.exists(output_folder_name) or os.makedirs(output_folder_name)
            file_path = f"{output_folder_name}/throughput_metrics_{current_id}.md"
            while os.path.exists(file_path):
                current_id += 1
                file_path = f"{output_folder_name}/throughput_metrics_{current_id}.md"
            with open(file_path, "w") as f:
                f.write(
                    f"Nr trees generated: {len(fandango.packet_selector._all_derivation_trees())}\n"
                )
                f.write(
                    f"Nr messages exchanged: {sum(len(sol.protocol_msgs()) for sol in fandango.packet_selector._all_derivation_trees())}\n"
                )
                msgs_by_sender: dict[str, int] = dict()
                ignore_parties = {'SocketControlServer', 'SocketControlClient'}
                for session in fandango.packet_selector._all_derivation_trees():
                    for msg in session.protocol_msgs():
                        if msg.sender in ignore_parties:
                            continue
                        msgs_by_sender[msg.sender] = msgs_by_sender.get(msg.sender, 0) + 1

                for sender, count in msgs_by_sender.items():
                    f.write(f"Nr messages sent by {sender}: {count}\n")
                f.write(f"Overall time elapsed: {time.time() - start_time:.2f}s\n")
                f.write(f"Netto time elapsed: {time.time() - (start_time + fandango._time_in_measurements):.2f}s\n")
                f.write(f"Grammar coverage: {(fandango.packet_selector.coverage_percent(alt_cache=True)*100):.2f}\n")


if __name__ == "__main__":
    main()
