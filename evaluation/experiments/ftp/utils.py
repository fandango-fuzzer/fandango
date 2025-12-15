import time

from fandango.language.symbols.non_terminal import NonTerminal


def _write_coverage_log(
    file,
    time_start,
    coverage_log: list[tuple[float, dict[NonTerminal, tuple[int, int]]]],
):
    with open(file, "w") as f:
        symbol_sorted = None
        for timestamp, coverage_dict in coverage_log:
            if symbol_sorted is None:
                symbol_sorted = list(coverage_dict.keys())
                symbol_sorted.sort(key=lambda x: str(x))
                f.write("time_elapsed")
                for symbol in symbol_sorted:
                    f.write(
                        f",covered_{str(symbol)},total_{str(symbol)},percent_{str(symbol)}"
                    )
                f.write("\n")

            time_elapsed = timestamp - time_start
            f.write(f"{time_elapsed}")
            for symbol in symbol_sorted:
                (covered, total) = coverage_dict[symbol]
                coverage_percent = covered / total if total > 0 else 0
                f.write(f",{covered},{total},{coverage_percent}")
            f.write("\n")


def write_coverage_log(fandango, output_folder_name, id_nr, time_start):
    _write_coverage_log(
        f"{output_folder_name}/run_{id_nr}_grammar_coverage.csv",
        time_start,
        fandango.coverage_log,
    )
    _write_coverage_log(
        f"{output_folder_name}/run_{id_nr}_grammar_coverage_overlap.csv",
        time_start,
        fandango.coverage_log_overlap,
    )

    with open(f"{output_folder_name}/run_{id_nr}_metrics.md", "w") as f:
        f.write("Coverage metrics:\n")
        f.write(
            f"Nr trees generated: {len(fandango.packet_selector._all_derivation_trees())}\n"
        )
        f.write(
            f"Nr messages exchanged: {sum(len(sol.protocol_msgs()) for sol in fandango.packet_selector._all_derivation_trees())}\n"
        )
        f.write(f"Overall time elapsed: {time.time() - time_start:.2f}s\n")
