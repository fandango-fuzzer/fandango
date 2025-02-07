import concurrent.futures
import random
from typing import Dict, List, Tuple

from fandango.constraints.base import Constraint
from fandango.constraints.fitness import FailingTree
from fandango.language.grammar import DerivationTree, Grammar
from fandango.logger import LOGGER


class Evaluator:
    def __init__(
        self,
        grammar: Grammar,
        constraints: List[Constraint],
        expected_fitness: float,
        diversity_k: int,
        diversity_weight: float,
        warnings_are_errors: bool = False,
    ):
        self.grammar = grammar
        self.constraints = constraints
        self.expected_fitness = expected_fitness
        self.diversity_k = diversity_k
        self.diversity_weight = diversity_weight
        self.warnings_are_errors = warnings_are_errors
        self.fitness_cache: Dict[int, Tuple[float, List[FailingTree]]] = {}
        self.solution = []
        self.solution_set = set()
        self.checks_made = 0

    def compute_diversity_bonus(
        self, individuals: List[DerivationTree]
    ) -> Dict[int, float]:
        k = self.diversity_k
        ind_kpaths: Dict[int, set] = {}
        for idx, tree in enumerate(individuals):
            # Assuming your grammar is available in evaluator
            paths = self.grammar._extract_k_paths_from_tree(tree, k)
            ind_kpaths[idx] = paths

        frequency: Dict[tuple, int] = {}
        for paths in ind_kpaths.values():
            for path in paths:
                frequency[path] = frequency.get(path, 0) + 1

        bonus: Dict[int, float] = {}
        for idx, paths in ind_kpaths.items():
            if paths:
                bonus_score = sum(1.0 / frequency[path] for path in paths) / len(paths)
            else:
                bonus_score = 0.0
            bonus[idx] = bonus_score * self.diversity_weight
        return bonus

    def evaluate_individual(
        self, individual: DerivationTree
    ) -> Tuple[float, List[FailingTree]]:
        key = hash(individual)
        if key in self.fitness_cache:
            if (
                self.fitness_cache[key][0] >= self.expected_fitness
                and key not in self.solution_set
            ):
                self.solution_set.add(key)
                self.solution.append(individual)
            return self.fitness_cache[key]

        fitness = 0.0
        failing_trees: List[FailingTree] = []
        for constraint in self.constraints:
            try:
                result = constraint.fitness(individual)
                if result.success:
                    fitness += result.fitness()
                else:
                    failing_trees.extend(result.failing_trees)
                    fitness += result.fitness()
                self.checks_made += 1
            except Exception as e:
                LOGGER.error(f"Error evaluating constraint {constraint}: {e}")
                fitness += 0.0
        try:
            fitness /= len(self.constraints)
        except ZeroDivisionError:
            fitness = 1.0

        if fitness >= self.expected_fitness and key not in self.solution_set:
            self.solution_set.add(key)
            self.solution.append(individual)
        self.fitness_cache[key] = (fitness, failing_trees)
        return fitness, failing_trees

    def evaluate_population(
        self, population: List[DerivationTree]
    ) -> List[Tuple[DerivationTree, float, List[FailingTree]]]:
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

    def evaluate_population_parallel(
        self, population: List[DerivationTree], num_workers: int = 4
    ) -> List[Tuple[DerivationTree, float, List]]:
        evaluation = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_individual = {
                executor.submit(self.evaluate_individual, ind): ind
                for ind in population
            }
            for future in concurrent.futures.as_completed(future_to_individual):
                ind = future_to_individual[future]
                try:
                    # evaluate_individual returns a 2-tuple: (fitness, failing_trees)
                    fitness, failing_trees = future.result()
                    # Pack the individual with its evaluation so that we have a 3-tuple.
                    evaluation.append((ind, fitness, failing_trees))
                except Exception as e:
                    LOGGER.error(f"Error during parallel evaluation: {e}")
        return evaluation

    def select_elites(
        self,
        evaluation: List[Tuple[DerivationTree, float, List]],
        elitism_rate: float,
        population_size: int,
    ) -> List[DerivationTree]:
        return [
            x[0]
            for x in sorted(evaluation, key=lambda x: x[1], reverse=True)[
                : int(elitism_rate * population_size)
            ]
        ]

    def tournament_selection(
        self, evaluation: List[Tuple[DerivationTree, float, List]], tournament_size: int
    ) -> Tuple[DerivationTree, DerivationTree]:
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
