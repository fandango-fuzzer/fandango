# scatter_search.py
from typing import List, Tuple

from fandango.constraints.fitness import Comparison, ComparisonSide
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.population import PopulationManager
from fandango.language.grammar import Grammar
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


class ScatterSearch:
    def __init__(
        self,
        grammar: Grammar,
        evaluator: Evaluator,
        pop_manager: PopulationManager,
        reference_set_size: int = 20,
        max_iterations: int = 100,
    ):
        self.grammar = grammar
        self.evaluator = evaluator
        self.pop_manager = pop_manager
        self.reference_set_size = reference_set_size
        self.max_iterations = max_iterations

        self.fixes_made = 0

        # Generate an initial population
        self.initial_population = self.pop_manager.generate_random_initial_population(
            self.fix_individual
        )
        # Evaluate the initial population
        self.evaluation = self.evaluator.evaluate_population(self.initial_population)
        # Select the initial reference set
        self.reference_set = self.select_reference_set(self.evaluation)

    def select_reference_set(
        self, evaluation: List[Tuple[DerivationTree, float, list]]
    ) -> List[DerivationTree]:
        sorted_eval = sorted(evaluation, key=lambda x: x[1], reverse=True)
        reference_set = [ind for ind, _, _ in sorted_eval[: self.reference_set_size]]
        return reference_set

    def path_relinking(
        self, sol_a: DerivationTree, sol_b: DerivationTree
    ) -> List[DerivationTree]:
        path = []
        differences = self.get_differences(sol_a, sol_b)
        current_solution = sol_a
        for diff in differences:
            new_subtree = self.get_corresponding_subtree(sol_b, diff)
            new_solution = current_solution.replace(diff, new_subtree)
            new_solution = self.local_improvement(new_solution)
            path.append(new_solution)
            current_solution = new_solution
        return path

    def get_differences(
        self, sol_a: DerivationTree, sol_b: DerivationTree
    ) -> List[DerivationTree]:
        differences = []

        def compare_nodes(node_a: DerivationTree, node_b: DerivationTree):
            if node_a.symbol != node_b.symbol:
                differences.append(node_a)
            else:
                for child_a, child_b in zip(node_a.children, node_b.children):
                    compare_nodes(child_a, child_b)

        compare_nodes(sol_a, sol_b)
        return differences

    def get_corresponding_subtree(
        self, sol: DerivationTree, target: DerivationTree
    ) -> DerivationTree:
        if sol.symbol == target.symbol:
            return sol
        for child in sol.children:
            result = self.get_corresponding_subtree(child, target)
            if result is not None:
                return result
        return target

    def local_improvement(self, solution: DerivationTree) -> DerivationTree:
        # Optionally, integrate your existing repair method.
        return solution

    def update_reference_set(self, candidates: List[DerivationTree]):
        combined = self.reference_set + candidates
        evaluation = self.evaluator.evaluate_population(combined)
        sorted_eval = sorted(evaluation, key=lambda x: x[1], reverse=True)
        self.reference_set = [
            ind for ind, _, _ in sorted_eval[: self.reference_set_size]
        ]

    def search(self) -> List[DerivationTree]:
        iteration = 0
        while iteration < self.max_iterations:
            new_candidates = []
            for i in range(len(self.reference_set)):
                for j in range(i + 1, len(self.reference_set)):
                    sol_a = self.reference_set[i]
                    sol_b = self.reference_set[j]
                    path = self.path_relinking(sol_a, sol_b)
                    new_candidates.extend(path)
            if new_candidates:
                self.update_reference_set(new_candidates)
            iteration += 1
        return self.reference_set

    def fix_individual(self, individual: DerivationTree) -> DerivationTree:
        _, failing_trees = self.evaluator.evaluate_individual(individual)
        for failing_tree in failing_trees:
            if failing_tree.tree.read_only:
                continue
            for operator, value, side in failing_tree.suggestions:
                if (
                    operator == Comparison.EQUAL
                    and side == ComparisonSide.LEFT
                    and isinstance(value, (str, bytes, DerivationTree))
                ):
                    suggested_tree = self.grammar.parse(
                        value, start=failing_tree.tree.symbol.symbol
                    )
                    if suggested_tree is None:
                        continue
                    individual = individual.replace(failing_tree.tree, suggested_tree)
                    self.fixes_made += 1
        return individual


if __name__ == "__main__":
    file = open("src/fandango/scatter/test.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    evaluator = Evaluator(grammar, constraints)
    pop_manager = PopulationManager(grammar, "<start>", 100)

    scatter = ScatterSearch(grammar, evaluator, pop_manager)
    result = scatter.search()

    for tree in result:
        print(str(tree))
        print()
