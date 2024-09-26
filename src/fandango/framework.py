import time

from fandango.evolution.OLD_IMPL import GeneticAlgorithmOptimizer
from fandango.language.parse import parse_file


def main():
    grammar, constraints, _ = parse_file("../evaluation/csv/csv.fan")

    # Initialize the optimizer
    times = []
    while len(times) < 1:
        optimizer = GeneticAlgorithmOptimizer(
            grammar=grammar,
            constraints=constraints,
            population_size=500,
            generations=100,
            verbose=True,
            crossover_rate=0.5,
            crossover_method="constraint_driven",
            mutation_rate=0.5,
            mutation_method="constraint_driven",
        )

        # Run the optimizer
        start_time = time.time()
        solution = optimizer.evolve()
        end_time = time.time()
        times.append(end_time - start_time)

        print(f"Solution: {solution}")

    print(f"Average time: {sum(times) / len(times)}")


if __name__ == "__main__":
    main()
