#!/usr/bin/env python3
#
# This script runs fandango fuzz multiple times and generates a CSV from some performance metrics.
#
# Usage: python parse_times.py <number_of_iterations> [fandango_args]
# Example: python parse_times.py 1000 -f docs/persons.fan -n 1000

import subprocess
import shlex
import multiprocessing as mp
import csv
import sys


def run_single_iteration(args_list):
    fuzz_args = ["fandango", "fuzz", "--format", "none", *args_list]
    fuzz_cmd = shlex.join(fuzz_args)
    sh_command = f"{fuzz_cmd} >/dev/null 2>&1"
    cmd = ["/usr/bin/time", "-l", "sh", "-c", sh_command]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stderr


def run_command(args_list, number_of_iterations):
    pool_size = min(number_of_iterations, mp.cpu_count())
    with mp.Pool(pool_size) as pool:
        results = pool.map(run_single_iteration, [args_list] * number_of_iterations)
    return results


def parse_times(results):
    parsed_results = []

    for i, result in enumerate(results, 1):
        lines = result.split("\n")
        if len(lines) < 17:
            continue

        data: dict[str, int | float] = {"Iter": i}

        # Parse first line (real, user, sys)
        first_line = lines[0].split()
        data["Real"] = float(first_line[0])
        data["User"] = float(first_line[2])
        data["Sys"] = float(first_line[4])

        # Parse all other metrics
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        value = int(parts[0])
                        metric = " ".join(parts[1:])
                        data[metric] = value
                    except ValueError as e:
                        print(
                            f"Error parsing line: {line} with error: {e}",
                            file=sys.stderr,
                        )
                        continue

        parsed_results.append(data)

    return parsed_results


def print_csv(results):
    if not results:
        print("No data found")
        return

    # Get all unique keys from all results
    all_keys = set()
    for result in results:
        all_keys.update(result.keys())

    # Sort keys for consistent ordering
    keys = sorted(all_keys)

    # Write CSV to stdout
    writer = csv.DictWriter(sys.stdout, fieldnames=keys)
    writer.writeheader()
    writer.writerows(results)

    # Calculate and write averages
    if results:
        avg_row = {}
        for key in keys:
            if key == "Iter":
                avg_row[key] = "AVG"
            else:
                try:
                    values = [
                        result[key]
                        for result in results
                        if key in result and isinstance(result[key], (int, float))
                    ]
                    if values:
                        avg_row[key] = sum(values) / len(values)
                    else:
                        avg_row[key] = "N/A"
                except (TypeError, ValueError):
                    avg_row[key] = "N/A"

        writer.writerow(avg_row)


if __name__ == "__main__":
    # Get additional arguments from command line (skip script name)
    if len(sys.argv) < 2:
        print("Usage: python parse_times.py <number_of_iterations> [fandango_args]")
        print("Example: python parse_times.py 1000 -f docs/persons.fan -n 1000")
        sys.exit(1)

    number_of_iterations = int(sys.argv[1])
    additional_args_list = sys.argv[2:]

    raw_results = run_command(additional_args_list, number_of_iterations)
    parsed_results = parse_times(raw_results)
    print_csv(parsed_results)
