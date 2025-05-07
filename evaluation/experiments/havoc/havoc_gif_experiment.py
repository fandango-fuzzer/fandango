import gif
import os

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def evaluate_gif():
    with open("evaluation/experiments/havoc/havoc_gif.fan", "r") as fd:
        grammar, constraints = parse(fd)
    i = 0
    while True:
        fandango = Fandango(
            grammar,
            constraints,
            logger_level=LoggerLevel.DEBUG,
            max_generations=100,
            desired_solutions=100,
            population_size=100,
            profiling=True,
        )
        print("Evolving...")
        fandango.evolve()
        fandango.evolve()
        print("Done evolving")
        for sol in fandango.solution:
            reader = gif.Reader()
            reader.feed(bytes(str(sol), "latin1"))
            if (
                not reader.has_screen_descriptor()
                or reader.has_unknown_block()
                or not reader.is_complete()
            ):
                os.makedirs("evaluation/experiments/havoc/files", exist_ok=True)
                with open(
                    f"evaluation/experiments/havoc/files/havoc_gif_error_{i}.gif", "wb"
                ) as fd:
                    fd.write(bytes(str(sol), "latin1"))
                i += 1


if __name__ == "__main__":
    evaluate_gif()
