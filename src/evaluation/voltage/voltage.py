from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def evaluate_img():
    grammar, constraints = parse_file("voltage.fan")

    print(grammar)
    print(constraints)

    fandango = FANDANGO(grammar, constraints, population_size=1000, max_generations=3000)
    fandango.evolve()

    print(fandango.population)


if __name__ == "__main__":
    evaluate_img()