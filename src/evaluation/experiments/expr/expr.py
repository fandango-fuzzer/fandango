from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file

def main():
    # Load the fandango file
    grammar, constraints = parse_file("expr.fan")

    fandango = FANDANGO(grammar, constraints)
    fandango.evolve()

    for i in range(1):
        print(fandango.population[i])


if __name__ == "__main__":
    main()
