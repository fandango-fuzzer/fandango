import random
from typing import Counter, Union, Optional
from collections.abc import Generator

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.constraints.fitness import FailingTree
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language import DerivationTree, Grammar, NonTerminal
from fandango.logger import LOGGER, print_exception


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
        self._grammar = grammar
        self._soft_constraints: list[SoftValue] = []
        self._hard_constraints: list[Constraint] = []
        self._expected_fitness = expected_fitness
        self._diversity_k = diversity_k
        self._diversity_weight = diversity_weight
        self._warnings_are_errors = warnings_are_errors
        self._fitness_cache: dict[int, tuple[float, list[FailingTree]]] = {}
        self._solution_set: set[int] = set()
        self._checks_made = 0

        for constraint in constraints:
            if isinstance(constraint, SoftValue):
                self._soft_constraints.append(constraint)
            elif isinstance(constraint, Constraint):
                self._hard_constraints.append(constraint)
            else:
                raise ValueError(f"Invalid constraint type: {type(constraint)}")

    @property
    def expected_fitness(self) -> float:
        return self._expected_fitness

    def get_fitness_check_count(self) -> int:
        """
        :return: The number of fitness checks made so far.
        """
        return self._checks_made

    def compute_mutation_pool(
        self, population: list[DerivationTree]
    ) -> list[DerivationTree]:
        """
        Computes the mutation pool for the given population.

        The mutation pool is computed by sampling the population with replacement, where the probability of sampling an individual is proportional to its fitness.

        :param population: The population to compute the mutation pool for.
        :return: The mutation pool.
        """
        weights = [self._fitness_cache[hash(ind)][0] for ind in population]
        if not all(w == 0 for w in weights):
            return random.choices(population, weights=weights, k=len(population))
        else:
            return population

    def flush_fitness_cache(self) -> None:
        """
        For soft constraints, the normalized fitness may change over time as we observe more inputs, this method flushes the fitness cache if the grammar contains any soft constraints.
        """
        if len(self._soft_constraints) > 0:
            self._fitness_cache = {}

    def compute_diversity_bonus(
        self,
        individuals: list[DerivationTree],
        fill_up: Optional[list[DerivationTree]] = None,
    ) -> list[float]:
        if fill_up is None:
            fill_up = []
        ind_kpaths = [
            self._grammar._extract_k_paths_from_tree(ind, self._diversity_k)
            for ind in individuals
        ]
        fill_up_kpaths = [
            self._grammar._extract_k_paths_from_tree(ind, self._diversity_k)
            for ind in fill_up
        ]
        frequencies = Counter(
            path for paths in ind_kpaths + fill_up_kpaths for path in paths
        )

        bonus = [
            (
                sum(1.0 / frequencies[path] for path in paths) / len(paths)
                if paths
                else 0.0
            )
            for paths in ind_kpaths
        ]
        return bonus

    def evaluate_hard_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        if len(self._hard_constraints) == 0:
            return 1.0, []

        hard_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self._hard_constraints:
            try:
                result = constraint.fitness(individual)

                if result.success:
                    hard_fitness += result.fitness()
                else:
                    failing_trees.extend(result.failing_trees)
                    hard_fitness += result.fitness()
                self._checks_made += 1
            except Exception as e:
                LOGGER.error(
                    f"Error evaluating hard constraint {constraint.format_as_spec()}"
                )
                print_exception(e)
                hard_fitness += 0.0
        hard_fitness /= len(self._hard_constraints)
        return hard_fitness, failing_trees

    def evaluate_soft_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        soft_fitness = 0.0
        failing_trees: list[FailingTree] = []
        for constraint in self._soft_constraints:
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

        soft_fitness /= len(self._soft_constraints)
        return soft_fitness, failing_trees

    def evaluate_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        fitness, failing_trees = self.evaluate_hard_constraints(individual)

        if self._soft_constraints:
            if fitness < 1.0:
                fitness = (
                    fitness
                    * len(self._hard_constraints)
                    / (len(self._hard_constraints) + len(self._soft_constraints))
                )
            else:  # fitness from hard constraints == 1.0
                soft_fitness, soft_failing_trees = self.evaluate_soft_constraints(
                    individual
                )

                failing_trees.extend(soft_failing_trees)

                fitness = (
                    fitness * len(self._hard_constraints)
                    + soft_fitness * len(self._soft_constraints)
                ) / (len(self._hard_constraints) + len(self._soft_constraints))
        return fitness, failing_trees

    def evaluate_individual(
        self,
        individual: DerivationTree,
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree]]]:
        key = hash(individual)
        if key in self._fitness_cache:
            return self._fitness_cache[key]

        fitness, failing_trees = self.evaluate_constraints(individual)

        if fitness >= self._expected_fitness and key not in self._solution_set:
            self._solution_set.add(key)
            yield individual

        self._fitness_cache[key] = (fitness, failing_trees)
        return fitness, failing_trees

    def evaluate_population(
        self, population: list[DerivationTree]
    ) -> Generator[
        DerivationTree, None, list[tuple[DerivationTree, float, list[FailingTree]]]
    ]:
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]] = []
        for ind in population:
            ind_eval = yield from self.evaluate_individual(ind)
            evaluation.append((ind, *ind_eval))

        if self._diversity_k > 0 and self._diversity_weight > 0:
            bonuses = self.compute_diversity_bonus(population, [])
            evaluation = [
                (ind, fitness + bonus, failing_trees)
                for (ind, fitness, failing_trees), bonus in zip(evaluation, bonuses)
            ]
        return evaluation

    def select_elites(
        self,
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]],
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
        self,
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]],
        tournament_size: int,
    ) -> tuple[DerivationTree, DerivationTree]:
        tournament = random.sample(evaluation, k=min(tournament_size, len(evaluation)))
        tournament.sort(key=lambda x: x[1], reverse=True)
        parent1 = tournament[0][0]
        if len(tournament) == 2:
            parent2 = tournament[1][0] if tournament[1][0] != parent1 else parent1
        else:
            parent2 = (
                tournament[1][0] if tournament[1][0] != parent1 else tournament[2][0]
            )
        return parent1, parent2


class IoEvaluator(Evaluator):
    def __init__(
        self,
        grammar: Grammar,
        constraints: list[Union[Constraint, SoftValue]],
        expected_fitness: float,
        diversity_k: int,
        diversity_weight: float,
        warnings_are_errors: bool = False,
    ):
        super().__init__(
            grammar,
            constraints,
            expected_fitness,
            diversity_k,
            diversity_weight,
            warnings_are_errors,
        )
        self._submitted_solutions: set[int] = set()
        self._hold_back_solutions: set[DerivationTree] = set()
        self._past_trees = []
        self._is_enable_guidance = True

    def enable_guidance(self, value):
        self._is_enable_guidance = value

    def get_past_msgs(
        self, packet_type: Optional[PacketNonTerminal] = None
    ) -> set[DerivationTree]:
        msgs = []
        for tree in self._past_trees:
            msgs.extend(tree.protocol_msgs())
        msgs = set(map(lambda x: x.msg, msgs))
        if packet_type is None:
            return msgs
        return set(
            filter(
                lambda msg: PacketNonTerminal(msg.sender, msg.recipient, msg.symbol)
                == packet_type,
                msgs,
            )
        )

    def start_next_message(self, past_trees: list[DerivationTree]) -> None:
        self._hold_back_solutions.clear()
        self._solution_set.clear()
        self._fitness_cache.clear()
        self._past_trees = past_trees
        for tree in past_trees:
            for msg in tree.protocol_msgs():
                msg = msg.msg
                key = (msg.sender, msg.recipient, msg)
                self._submitted_solutions.add(hash(key))

    def _is_path_start_with(self, state_path: tuple, path: tuple) -> int:
        n = len(state_path)
        m = len(path)
        max_overlap = min(n, m)
        for overlap in range(max_overlap, 0, -1):
            if state_path[-overlap:] == path[:overlap]:
                return overlap
        return 0

    def evaluate_individual(
        self,
        individual: DerivationTree,
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree]]]:
        key = hash(individual)
        if key in self._fitness_cache:
            return self._fitness_cache[key]

        fitness, failing_trees = self.evaluate_constraints(individual)
        self._fitness_cache[key] = (fitness, failing_trees)

        if fitness < self._expected_fitness:
            return fitness, failing_trees

        if len(individual.protocol_msgs()) != 0:
            msg = individual.protocol_msgs()[-1].msg
            msg_key = PacketNonTerminal(msg.sender, msg.recipient, msg.symbol)
            msg_hash = hash(msg)
        else:
            msg = None
            msg_key = None
            msg_hash = None

        if not self._is_enable_guidance:
            if key not in self._solution_set:
                self._solution_set.add(key)
                yield individual
            return fitness, failing_trees

        if fitness >= self._expected_fitness:
            if msg is None:
                yield individual
            else:
                state_path = msg.get_path()
                if len(state_path) > self._diversity_k:
                    state_path = state_path[-self._diversity_k :]
                state_path = tuple(map(lambda x: x.symbol, state_path))
                uncovered_paths = self._grammar.get_uncovered_k_paths(list(self.get_past_msgs(msg_key)), self._diversity_k, msg.symbol, True)
                overlap_to_root = any(filter(lambda path: 0 < self._is_path_start_with(state_path, path) < self._diversity_k, uncovered_paths))

                old_coverage = self._grammar.compute_kpath_coverage(
                    list(self.get_past_msgs(msg_key)), self._diversity_k, msg.symbol, overlap_to_root=overlap_to_root
                )
                new_coverage = self._grammar.compute_kpath_coverage(
                    list(self.get_past_msgs(msg_key)) + [msg],
                    self._diversity_k,
                    msg.symbol,
                    overlap_to_root=overlap_to_root
                )
                if old_coverage < new_coverage or new_coverage == 1.0:
                    if new_coverage < 1.0:
                        self._solution_set.add(msg_hash)
                    yield individual
                elif (
                    msg_hash not in self._submitted_solutions
                    and msg_hash not in self._solution_set
                    and msg_hash not in self._hold_back_solutions
                ):
                    self._hold_back_solutions.add(individual)

        self._fitness_cache[key] = (fitness, failing_trees)
        return fitness, failing_trees

    def evaluate_population(
        self, population: list[DerivationTree]
    ) -> Generator[
        DerivationTree, None, list[tuple[DerivationTree, float, list[FailingTree]]]
    ]:
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]] = []
        for ind in population:
            ind_eval = yield from self.evaluate_individual(ind)
            evaluation.append((ind, *ind_eval))

        if self._diversity_k > 0 and self._diversity_weight > 0:
            fill_up_by_msg_nt: dict[
                tuple[str, str, NonTerminal], list[DerivationTree]
            ] = {}
            for ind in population:
                msgs = ind.protocol_msgs()
                for i, msg in enumerate(msgs):
                    key = (msg.sender, msg.recipient, msg.msg.symbol)
                    if key not in fill_up_by_msg_nt:
                        fill_up_by_msg_nt[key] = []
                    if i != len(msgs) - 1:
                        fill_up_by_msg_nt[key].append(msg.msg)
            for ind in self._past_trees:
                for i, msg in enumerate(ind.protocol_msgs()):
                    key = (msg.sender, msg.recipient, msg.msg.symbol)
                    if key not in fill_up_by_msg_nt:
                        fill_up_by_msg_nt[key] = []
                    fill_up_by_msg_nt[key].append(msg.msg)

            for i, ind in enumerate(population):
                if len(ind.protocol_msgs()) == 0:
                    continue
                last_msg = ind.protocol_msgs()[-1]
                key = (last_msg.sender, last_msg.recipient, last_msg.msg.symbol)
                bonuses = self.compute_diversity_bonus([ind], fill_up_by_msg_nt[key])
                evaluation[i] = (ind, evaluation[i][1] + bonuses[0], evaluation[i][2])

        return evaluation
