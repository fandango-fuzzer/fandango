from typing import Callable, List, Set

from fandango.constraints.fitness import Comparison, ComparisonSide, FailingTree
from fandango.language.grammar import DerivationTree, Grammar
from fandango.logger import LOGGER


class PopulationManager:
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str,
        population_size: int,
        warnings_are_errors: bool = False,
    ):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.population_size = population_size
        self.warnings_are_errors = warnings_are_errors

    def add_unique_individual(
        self,
        population: List[DerivationTree],
        candidate: DerivationTree,
        unique_set: Set[int],
    ) -> bool:
        h = hash(candidate)
        if h not in unique_set:
            unique_set.add(h)
            population.append(candidate)
            return True
        return False

    def generate_random_initial_population(
        self, fix_func: Callable[[DerivationTree], DerivationTree]
    ) -> List[DerivationTree]:
        unique_population = []
        unique_hashes = set()
        attempts = 0
        max_attempts = self.population_size * 10  # safeguard against infinite loops

        while len(unique_population) < self.population_size and attempts < max_attempts:
            candidate = fix_func(self.grammar.fuzz(self.start_symbol))
            self.add_unique_individual(unique_population, candidate, unique_hashes)
            attempts += 1

        if len(unique_population) < self.population_size:
            LOGGER.warning(
                f"Could not generate a full population of unique individuals. Population size reduced to {len(unique_population)}."
            )
        return unique_population

    def refill_population(
        self,
        current_population: List[DerivationTree],
        fix_func: Callable[[DerivationTree], DerivationTree],
    ) -> List[DerivationTree]:
        unique_hashes = {hash(ind) for ind in current_population}
        attempts = 0
        max_attempts = (self.population_size - len(current_population)) * 10

        while (
            len(current_population) < self.population_size and attempts < max_attempts
        ):
            candidate = fix_func(self.grammar.fuzz(self.start_symbol))
            if hash(candidate) not in unique_hashes:
                unique_hashes.add(hash(candidate))
                current_population.append(candidate)
            attempts += 1

        if len(current_population) < self.population_size:
            LOGGER.warning(
                "Could not generate full unique new population, filling remaining slots with duplicates."
            )
            while len(current_population) < self.population_size:
                current_population.append(self.grammar.fuzz(self.start_symbol))

        return current_population

    def fix_individual(
        self, individual: DerivationTree, failing_trees: List[FailingTree]
    ) -> DerivationTree:
        fixes_made = 0
        for failing_tree in failing_trees:
            for operator, value, side in failing_tree.suggestions:
                if operator == Comparison.EQUAL and side == ComparisonSide.LEFT:
                    suggested_tree = self.grammar.parse(
                        str(value), start=failing_tree.tree.symbol.symbol
                    )
                    if suggested_tree is None:
                        continue
                    individual = individual.replace(failing_tree.tree, suggested_tree)
                    fixes_made += 1
        return individual, fixes_made
