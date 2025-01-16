from fandango.evolution.algorithm import Fandango
from fandango.language.grammar import *
from fandango.language.symbol import *
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("simple_io_2.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    # Initialize FANDANGO with desired parameters
    seen_non_terminals = set()
    seen_non_terminals.add(NonTerminal('<start>'))

    processed_non_terminals = set()
    unprocessed_non_terminals = seen_non_terminals.difference(processed_non_terminals)

    while len(unprocessed_non_terminals) > 0:
        current_symbol = unprocessed_non_terminals.pop()

        assigner = RoleAssigner('TEST', grammar, processed_non_terminals)
        assigner.run(grammar.rules[current_symbol])

        processed_non_terminals.add(current_symbol)
        seen_non_terminals = seen_non_terminals.union(assigner.seen_non_terminals)
        unprocessed_non_terminals = seen_non_terminals.difference(processed_non_terminals)

    fandango = Fandango(grammar=grammar, constraints=constraints, population_size=100)

    # Evolve solutions
    solutions = fandango.evolve()

    # Output solutions
    for solution in solutions:
        print(str(solution))


if __name__ == "__main__":
    main()
