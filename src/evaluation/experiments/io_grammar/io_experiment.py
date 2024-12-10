from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file

def main():
    # Parse grammar and constraints
    grammar, constraints = parse_file('io_example.fan')

    # Initialize FANDANGO with desired parameters
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=100,
        max_generations=10,
        verbose=True
    )

    # Evolve solutions
    solutions = fandango.evolve()

    # Output solutions
    for solution in solutions:
        print(str(solution))

if __name__ == '__main__':
    #print(int("0xB", 16))
    main()
