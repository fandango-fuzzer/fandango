from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_transactions():
    # Load the fandango file
    file = open("evaluation/experiments/transactions/transactions.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    fandango = Fandango(grammar, constraints)
    fandango.evolve(max_generations=100, desired_solutions=10)

    print("TRANSACTIONS")
    for solution in fandango.solution:
        print(solution)


if __name__ == "__main__":
    evaluate_transactions()
