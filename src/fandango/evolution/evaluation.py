import random
from typing import Union

from fandango.constraints.base import Constraint, SoftValue
from fandango.constraints.fitness import FailingTree
from fandango.language.grammar import DerivationTree, Grammar
from fandango.logger import LOGGER


class Evaluator:
    def __init__(
        self,
        grammar: Grammar,
        constraints: list[Union[Constraint, SoftValue]],
        expected_fitness: float,
        diversity_k: int,
        diversity_weight: float,
        warnings_are_errors: bool = False,
    ):
        self.grammar = grammar
        self.constraints = constraints
        self.soft_constraints: list[SoftValue] = []
        self.hard_constraints: list[Constraint] = []
        self.expected_fitness = expected_fitness
        self.diversity_k = diversity_k
        self.diversity_weight = diversity_weight
        self.warnings_are_errors = warnings_are_errors
        self.fitness_cache: dict[int, tuple[float, list[FailingTree]]] = {}
        self.solution = []
        self.solution_set = set()
        self.checks_made = 0

        for constraint in constraints:
            if isinstance(constraint, SoftValue):
                self.soft_constraints.append(constraint)
            else:
                self.hard_constraints.append(constraint)

    def compute_diversity_bonus(
        self, individuals: list[DerivationTree]
    ) -> dict[int, float]:
        k = self.diversity_k
        ind_kpaths: dict[int, set] = {}
        for idx, tree in enumerate(individuals):
            # Assuming your grammar is available in evaluator
            paths = self.grammar._extract_k_paths_from_tree(tree, k)
            ind_kpaths[idx] = paths

        frequency: dict[tuple, int] = {}
        for paths in ind_kpaths.values():
            for path in paths:
                frequency[path] = frequency.get(path, 0) + 1

        bonus: dict[int, float] = {}
        for idx, paths in ind_kpaths.items():
            if paths:
                bonus_score = sum(1.0 / frequency[path] for path in paths) / len(paths)
            else:
                bonus_score = 0.0
            bonus[idx] = bonus_score * self.diversity_weight
        return bonus

    def evaluate_hard_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        hard_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self.hard_constraints:
            try:
                result = constraint.fitness(individual)

                if result.success:
                    hard_fitness += result.fitness()
                else:
                    failing_trees.extend(result.failing_trees)
                    hard_fitness += result.fitness()
                self.checks_made += 1
            except Exception as e:
                LOGGER.error(f"Error evaluating hard constraint {constraint}: {e}")
                hard_fitness += 0.0
        try:
            hard_fitness /= len(self.hard_constraints)
        except ZeroDivisionError:
            hard_fitness = 1.0
        return hard_fitness, failing_trees

    def evaluate_soft_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        soft_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self.soft_constraints:
            try:
                result = constraint.fitness(individual)

                # failing_trees are required for mutations;
                # with soft constraints, we never know when they are fully optimized.
                failing_trees.extend(result.failing_trees)

                constraint.tdigest.update(result.fitness())
                normalized_fitness = constraint.tdigest.score(result.fitness())

                if constraint.optimization_goal == "max":
                    soft_fitness += normalized_fitness
                else:  # "min"
                    soft_fitness += 1 - normalized_fitness
            except Exception as e:
                LOGGER.error(f"Error evaluating soft constraint {constraint}: {e}")
                soft_fitness += 0.0

        soft_fitness /= len(self.soft_constraints)
        return soft_fitness, failing_trees

    def evaluate_individual(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        key = hash(individual)
        if key in self.fitness_cache:
            if (
                self.fitness_cache[key][0] >= self.expected_fitness
                and key not in self.solution_set
            ):
                self.solution_set.add(key)
                self.solution.append(individual)
            return self.fitness_cache[key]

        hard_fitness, hard_failing_trees = self.evaluate_hard_constraints(individual)

        if self.soft_constraints == []:
            fitness = hard_fitness
        else:
            if hard_fitness < 1.0:
                fitness = (
                    hard_fitness * len(self.hard_constraints) / len(self.constraints)
                )
            else:  # hard_fitness == 1.0
                soft_fitness, soft_failing_trees = self.evaluate_soft_constraints(
                    individual
                )

                fitness = (
                    hard_fitness * len(self.hard_constraints)
                    + soft_fitness * len(self.soft_constraints)
                ) / len(self.constraints)

        if fitness >= self.expected_fitness and key not in self.solution_set:
            self.solution_set.add(key)
            self.solution.append(individual)

        failing_trees = hard_failing_trees + (soft_failing_trees or [])

        self.fitness_cache[key] = (fitness, failing_trees)
        return fitness, failing_trees

    def evaluate_population(
        self, population: list[DerivationTree]
    ) -> list[tuple[DerivationTree, float, list[FailingTree]]]:
        evaluation = []
        for individual in population:
            fitness, failing_trees = self.evaluate_individual(individual)
            evaluation.append((individual, fitness, failing_trees))
        if self.diversity_k > 0 and self.diversity_weight > 0:
            bonus_map = self.compute_diversity_bonus(population)
            new_evaluation = []
            for idx, (ind, fitness, failing_trees) in enumerate(evaluation):
                new_fitness = fitness + bonus_map.get(idx, 0.0)
                new_evaluation.append((ind, new_fitness, failing_trees))
            evaluation = new_evaluation
        return evaluation

    def select_elites(
        self,
        evaluation: list[tuple[DerivationTree, float, list]],
        elitism_rate: float,
        population_size: int,
    ) -> list[DerivationTree]:
        return [
            x[0]
            for x in sorted(evaluation, key=lambda x: x[1], reverse=True)[
                : int(elitism_rate * population_size)
            ]
        ]

    def tournament_selection(
        self, evaluation: list[tuple[DerivationTree, float, list]], tournament_size: int
    ) -> tuple[DerivationTree, DerivationTree]:
        tournament = random.sample(evaluation, k=tournament_size)
        tournament.sort(key=lambda x: x[1], reverse=True)
        parent1 = tournament[0][0]
        if len(tournament) == 2:
            parent2 = tournament[1][0] if tournament[1][0] != parent1 else parent1
        else:
            parent2 = (
                tournament[1][0] if tournament[1][0] != parent1 else tournament[2][0]
            )
        return parent1, parent2
