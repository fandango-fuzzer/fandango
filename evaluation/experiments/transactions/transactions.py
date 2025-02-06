from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def main():
    # Load the fandango file
    file = open("evaluation/experiments/transactions/transactions.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    fandango = Fandango(grammar, constraints)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    main()
