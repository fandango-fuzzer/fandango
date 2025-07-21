from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("3_party_io.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
        assert grammar is not None

    fandango = Fandango(grammar=grammar, constraints=constraints, population_size=100)

    # Evolve solutions
    solutions = fandango.evolve()

    # Output solutions
    for solution in solutions:
        print(str(solution))


if __name__ == "__main__":
    main()
