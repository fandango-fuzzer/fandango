# framework.py

import argparse

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file


def main():
    parser = argparse.ArgumentParser(
        description="FANDANGO Grammar-Based Genetic Algorithm Framework"
    )
    parser.add_argument(
        "fan_file_path",
        type=str,
        help="Path to the .fan file containing the grammar and constraints",
    )
    parser.add_argument(
        "-p",
        "--population_size",
        type=int,
        default=100,
        help="Population size (default: 100)",
    )
    parser.add_argument(
        "-m",
        "--mutation_rate",
        type=float,
        default=0.1,
        help="Mutation rate (default: 0.1)",
    )
    parser.add_argument(
        "-c",
        "--crossover_rate",
        type=float,
        default=0.9,
        help="Crossover rate (default: 0.9)",
    )
    parser.add_argument(
        "-g",
        "--max_generations",
        type=int,
        default=100,
        help="Maximum number of generations (default: 100)",
    )
    parser.add_argument(
        "-e",
        "--elitism_rate",
        type=float,
        default=0.2,
        help="Elitism rate (default: 0.2)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    # Parse the grammar and constraints from the .fan file
    grammar, constraints = parse_file(args.fan_file_path)

    # Initialize FANDANGO
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=args.population_size,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        max_generations=args.max_generations,
        elitism_rate=args.elitism_rate,
        verbose=args.verbose,
    )

    # Run the evolution process
    fandango.evolve()

    # Output the best solution found
    if fandango.population:
        print("\nBest solution found:")
        print(fandango.population)


if __name__ == "__main__":
    main()
