import time

import gif

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def is_syntactically_valid_gif(file_path):
    file = open(file_path, "rb")
    reader = gif.Reader()
    reader.feed(file.read())
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
    with open("evaluation/experiments/gif/gif.fan", "r") as fd:
        grammar, constraints = parse(fd)
    start_time = time.time()
    fandango = Fandango(
        grammar,
        constraints,
        logger_level=LoggerLevel.DEBUG,
        max_generations=100,
        desired_solutions=100,
        population_size=100,
    )
    fandango.evolve()
    end_time = time.time()
    i = 0
    for sol in fandango.solution:
        with open(f"evaluation/experiments/gif/files/fuzzed_{i}.gif", "wb") as fd:
            # Ensure sol is valid byte data, convert to bytes if needed
            gif_bytes = bytes(
                str(sol), "latin1"
            )  # Use 'latin1' to preserve byte values
            print(f"Generated GIF file: {gif_bytes}")  # Debug output
            # First, convert the string into bytes, then decode the escape sequences,
            # then re-encode in a one-to-one manner (e.g. latin1) to preserve byte values.
            binary_data = gif_bytes.decode("unicode_escape").encode("latin1")

            print(f"First 10 bytes of generated GIF: {gif_bytes[:10]}")  # Debug output

            fd.write(binary_data)  # Write the raw byte sequence to the file

        # Check the validity of the written file
        if is_syntactically_valid_gif(
            f"evaluation/experiments/gif/files/fuzzed_{i}.gif"
        ):
            i += 1

    print(f"Generated {i} valid GIF files in {end_time - start_time} seconds")


if __name__ == "__main__":
    evaluate_gif()
