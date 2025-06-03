import concurrent.futures
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
        self.__grammar = grammar
        self.__constraints = constraints
        self.__soft_constraints: list[SoftValue] = []
        self.__hard_constraints: list[Constraint] = []
        self.__expected_fitness = expected_fitness
        self.__diversity_k = diversity_k
        self.__diversity_weight = diversity_weight
        self.__warnings_are_errors = warnings_are_errors
        self.__fitness_cache: dict[int, tuple[float, list[FailingTree]]] = {}
        self.__solution = []
        self.__solution_set = set()
        self.__checks_made = 0

        for constraint in constraints:
            if isinstance(constraint, SoftValue):
                self.__soft_constraints.append(constraint)
            elif isinstance(constraint, Constraint):
                self.__hard_constraints.append(constraint)
            else:
                raise ValueError(f"Invalid constraint type: {type(constraint)}")

    def solution_count(self) -> int:
        """
        :return: The number of perfect solutions found so far.
        """
        return len(self.__solution)
    
    def truncate_solution(self, desired_solutions: int) -> None:
        """
        Truncates the solution set to the desired number of solutions.

        :param desired_solutions: The number of solutions to keep.
        """
        self.__solution = self.__solution[:desired_solutions]

    def get_solutions(self) -> list[DerivationTree]:
        """
        :return: The list of perfect solutions found so far.
        """
        return self.__solution
    
    def get_fitness_check_count(self) -> int:   
        """
        :return: The number of fitness checks made so far.
        """
        return self.__checks_made

    def compute_mutation_pool(self, population: list[DerivationTree]) -> list[DerivationTree]:
        """
        Computes the mutation pool for the given population.

        The mutation pool is computed by sampling the population with replacement, where the probability of sampling an individual is proportional to its fitness.

        :param population: The population to compute the mutation pool for.
        :return: The mutation pool.
        """
        weights = [self.__fitness_cache[hash(ind)][0] for ind in population]
        if not all(w == 0 for w in weights):
            return random.choices(
                population, weights=weights, k=len(population)
            )
        else:
            return population
        
    def flush_fitness_cache(self) -> None:
        """
        For soft constraints, the normalized fitness may change over time as we observe more inputs, this method flushes the fitness cache if the grammar contains any soft constraints.
        """
        if len(self.__soft_constraints) > 0:
            self.__fitness_cache = {}

    def compute_diversity_bonus(
        self, individuals: list[DerivationTree]
    ) -> dict[int, float]:
        k = self.__diversity_k
        ind_kpaths: dict[int, set] = {}
        for idx, tree in enumerate(individuals):
            # Assuming your grammar is available in evaluator
            paths = self.__grammar._extract_k_paths_from_tree(tree, k)
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
            bonus[idx] = bonus_score * self.__diversity_weight
        return bonus

    def evaluate_hard_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        if len(self.__hard_constraints) == 0:
            return 1.0, []

        hard_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self.__hard_constraints:
            try:
                result = constraint.fitness(individual)

                if result.success:
                    hard_fitness += result.fitness()
                else:
                    failing_trees.extend(result.failing_trees)
                    hard_fitness += result.fitness()
                self.__checks_made += 1
            except Exception as e:
                LOGGER.error(f"Error evaluating hard constraint {constraint}: {e}")
                hard_fitness += 0.0
        hard_fitness /= len(self.__hard_constraints)
        return hard_fitness, failing_trees

    def evaluate_soft_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        soft_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self.__soft_constraints:
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

        soft_fitness /= len(self.__soft_constraints)
        return soft_fitness, failing_trees

    def evaluate_individual(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        key = hash(individual)
        if key in self.__fitness_cache:
            if (
                self.__fitness_cache[key][0] >= self.__expected_fitness
                and key not in self.__solution_set
            ):
                self.__solution_set.add(key)
                self.__solution.append(individual)
            return self.__fitness_cache[key]

        hard_fitness, hard_failing_trees = self.evaluate_hard_constraints(individual)

        if self.__soft_constraints == []:
            fitness = hard_fitness
        else:
            if hard_fitness < 1.0:
                fitness = (
                    hard_fitness * len(self.__hard_constraints) / len(self.__constraints)
                )
            else:  # hard_fitness == 1.0
                soft_fitness, soft_failing_trees = self.evaluate_soft_constraints(
                    individual
                )

                fitness = (
                    hard_fitness * len(self.__hard_constraints)
                    + soft_fitness * len(self.__soft_constraints)
                ) / len(self.__constraints)

        if fitness >= self.__expected_fitness and key not in self.__solution_set:
            self.__solution_set.add(key)
            self.__solution.append(individual)
        try:
            failing_trees = hard_failing_trees + soft_failing_trees
        except NameError:
            failing_trees = hard_failing_trees

        self.__fitness_cache[key] = (fitness, failing_trees)
        return fitness, failing_trees

    def evaluate_population(
        self, population: list[DerivationTree]
    ) -> list[tuple[DerivationTree, float, list[FailingTree]]]:
        evaluation = []
        for individual in population:
            fitness, failing_trees = self.evaluate_individual(individual)
            evaluation.append((individual, fitness, failing_trees))
        if self.__diversity_k > 0 and self.__diversity_weight > 0:
            bonus_map = self.compute_diversity_bonus(population)
            new_evaluation = []
            for idx, (ind, fitness, failing_trees) in enumerate(evaluation):
                new_fitness = fitness + bonus_map.get(idx, 0.0)
                new_evaluation.append((ind, new_fitness, failing_trees))
            evaluation = new_evaluation
        return evaluation

    def evaluate_population_parallel(
        self, population: list[DerivationTree], num_workers: int = 4
    ) -> list[tuple[DerivationTree, float, list]]:
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
