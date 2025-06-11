import time

import coverage
import gif

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.legacy.parse import parse


def is_syntactically_valid_gif(file_path):
    with open(file_path, "rb") as file:
        reader = gif.Reader()
        file_data = file.read()
        reader.feed(file_data)
    errors = False
    if reader.has_screen_descriptor():
        print("Size: %dx%d" % (reader.width, reader.height))
        print("Colors: %s" % repr(reader.color_table))
        for block in reader.blocks:
            if isinstance(block, gif.Image):
                print("Pixels: %s" % repr(block.get_pixels()))
        if reader.has_unknown_block():
            print("Encountered unknown block")
            errors = True
        else:
            print("No unknown blocks")
        if not reader.is_complete():
            print("Missing trailer")
            errors = True
        else:
            print("Trailer found")
        if not errors:
            print("No errors found")
            return True
    else:
        print("Not a valid GIF file")
        return False


def evaluate_gif():
    # Parse the grammar and constraints for Fandango
    with open("evaluation/experiments/gif/gif.fan", "r") as fd:
        grammar, constraints = parse(fd)

    start_time = time.time()
    fandango = Fandango(
        grammar,
        constraints,
        logger_level=LoggerLevel.DEBUG,
        population_size=1000,
    )
    fandango.evolve(max_generations=100, desired_solutions=1000)
    end_time = time.time()

    valid_count = 0
    # List to hold every binary input produced (to later review what was sent to gif.Reader)
    inputs_list = []

    for i, sol in enumerate(fandango.solution):
        file_path = f"evaluation/experiments/gif/files/fuzzed_{i}.gif"
        with open(file_path, "wb") as fd:
            # Convert solution to bytes using latin1 to preserve byte values
            gif_bytes = bytes(str(sol), "latin1")
            print(f"Generated GIF file bytes: {gif_bytes}")
            # Process escape sequences: first decode as unicode_escape then re-encode with latin1
            binary_data = gif_bytes.decode("unicode_escape").encode("latin1")
            print(f"First 10 bytes of generated GIF: {binary_data[:10]}")
            fd.write(binary_data)
            inputs_list.append(binary_data)

        # Validate the generated GIF file using the gif library
        if is_syntactically_valid_gif(file_path):
            valid_count += 1

    print(
        f"Generated {valid_count} valid GIF files in {end_time - start_time:.2f} seconds"
    )
    return inputs_list


if __name__ == "__main__":
    # Start coverage measurement for the 'gif' module.
    # (Ensure that coverage.py is installed: pip install coverage)
    cov = coverage.Coverage(source=["gif"])
    cov.start()

    # Run the GIF evaluation (fuzzing and validation)
    all_inputs = evaluate_gif()

    # Stop coverage measurement and output the report.
    cov.stop()
    cov.save()
    print("\nCoverage report for the 'gif' module:")
    cov.report(show_missing=True)
