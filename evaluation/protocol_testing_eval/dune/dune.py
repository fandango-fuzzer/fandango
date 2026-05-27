from fandango.evolution.algorithm import LoggerLevel, SimpleGeneticAlgorithm
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    with open("dune.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    assert grammar is not None
    fandango = SimpleGeneticAlgorithm(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
    )

    list(fandango.generate(mode=FuzzingMode.IO))  # force evaluation of generator


if __name__ == "__main__":
    main()
