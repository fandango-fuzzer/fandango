import random
from typing import Counter, Optional, Union
from collections.abc import Generator, Sequence

from fandango.constraints.constraint import Constraint
from fandango.constraints.repetition_bounds import RepetitionBoundsConstraint
from fandango.constraints.soft import SoftValue
from fandango.constraints.failing_tree import (
    ApplyAllSuggestions,
    FailingTree,
    NopSuggestion,
    Suggestion,
)
from fandango.evolution import GeneratorWithReturn
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.logger import LOGGER, print_exception


class Evaluator:
    def __init__(
        self,
        grammar: Grammar,
        constraints: list[Constraint | SoftValue],
        expected_fitness: float,
        diversity_k: int,
        diversity_weight: float,
        warnings_are_errors: bool = False,
    ):
        self._grammar = grammar
        self._soft_constraints: list[SoftValue] = []
        self._hard_constraints: list[Constraint] = []
        self._repetition_bounds_constraints: list[RepetitionBoundsConstraint] = []
        self._expected_fitness = expected_fitness
        self._diversity_k = diversity_k
        self._diversity_weight = diversity_weight
        self._warnings_are_errors = warnings_are_errors
        self._fitness_cache: dict[int, tuple[float, list[FailingTree], Suggestion]] = {}
        self._solution_set: set[int] = set()
        self._checks_made = 0

        for constraint in constraints:
            if isinstance(constraint, SoftValue):
                self._soft_constraints.append(constraint)
            elif isinstance(constraint, RepetitionBoundsConstraint):
                self._repetition_bounds_constraints.append(constraint)
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
    ) -> tuple[float, list[FailingTree], Suggestion]:
        return self._evaluate_constraints(individual, self._hard_constraints)

    def evaluate_repetition_bounds_constraints(
        self, individual: DerivationTree,
    ) -> tuple[float, list[FailingTree], Suggestion]:
        return self._evaluate_constraints(
            individual, self._repetition_bounds_constraints
        )

    def _evaluate_constraints(
        self, individual: DerivationTree, constraints: Sequence[Constraint]
    ) -> tuple[float, list[FailingTree], Suggestion]:
        if len(constraints) == 0:
            return 1.0, [], NopSuggestion()

        fitness = 0.0
        failing_trees: list[FailingTree] = []
        suggestions = []
        for constraint in constraints:
            try:
                result = constraint.fitness(individual)
                fitness += result.fitness()
                failing_trees.extend(result.failing_trees)
                if result.suggestion is not None:
                    suggestions.append(result.suggestion)
                self._checks_made += 1
            except Exception as e:
                LOGGER.error(
                    f"Error evaluating constraint {constraint.format_as_spec()}"
                )
                print_exception(e)

        # normalize to 0 <= fitness <= 1
        fitness /= len(constraints)
        return (
            fitness,
            failing_trees,
            ApplyAllSuggestions(suggestions),
        )

    def evaluate_soft_constraints(
        self, individual: DerivationTree
    ) -> tuple[float, list[FailingTree]]:
        if not self._soft_constraints:
            return 1.0, []

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
                LOGGER.error(
                    f"Error evaluating soft constraint {constraint.format_as_spec()}: {e}"
                )
                soft_fitness += 0.0

        soft_fitness /= len(self._soft_constraints)
        return soft_fitness, failing_trees

    def evaluate_individual(
        self,
        individual: DerivationTree,
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree], Suggestion]]:
        key = hash(individual)
        if key in self._fitness_cache:
            return self._fitness_cache[key]

        total_constraint_count = (
            len(self._hard_constraints)
            + len(self._repetition_bounds_constraints)
            + len(self._soft_constraints)
        )

        fitness, failing_trees, suggestion = self.evaluate_hard_constraints(individual)

        fully_solved_so_far = fitness == 1.0

        if total_constraint_count > 0:
            # normalize the fitness to the number of hard constraints
            fitness = fitness / (total_constraint_count) * len(self._hard_constraints)

        if len(self._repetition_bounds_constraints) > 0:
            # all hard constraints are satisfied, so we can evaluate the repetition bounds constraints
            rep_fitness, rep_failing_trees, rep_suggestion = (
                self.evaluate_repetition_bounds_constraints(individual)
            )
            rep_suggestion.rec_set_allow_repetition_full_delete(fully_solved_so_far)
            suggestion = ApplyAllSuggestions([suggestion, rep_suggestion])
            failing_trees.extend(rep_failing_trees)

            fully_solved_so_far = fully_solved_so_far and rep_fitness == 1.0

            # normalize the fitness to the number of constraints
            fitness += (
                rep_fitness
                / total_constraint_count
                * len(self._repetition_bounds_constraints)
            )

        if len(self._soft_constraints) > 0 and fully_solved_so_far:
            # all hard and repetition bounds constraints are satisfied, so we can evaluate the soft constraints
            soft_fitness, soft_failing_trees = self.evaluate_soft_constraints(
                individual
            )

            failing_trees.extend(soft_failing_trees)

            fitness += (
                soft_fitness / total_constraint_count * len(self._soft_constraints)
            )

        if fitness >= self._expected_fitness and key not in self._solution_set:
            self._solution_set.add(key)
            yield individual

        self._fitness_cache[key] = (fitness, failing_trees, suggestion)
        return fitness, failing_trees, suggestion

    def evaluate_population(self, population: list[DerivationTree]) -> Generator[
        DerivationTree,
        None,
        list[tuple[DerivationTree, float, list[FailingTree], Suggestion]],
    ]:
        evaluation = []
        for ind in population:
            ind_eval = yield from self.evaluate_individual(ind)
            evaluation.append((ind, *ind_eval))

        if self._diversity_k > 0 and self._diversity_weight > 0:
            bonuses = self.compute_diversity_bonus(population, [])
            evaluation = [
                (ind, fitness + bonus, failing_trees, suggestion)
                for (ind, fitness, failing_trees, suggestion), bonus in zip(
                    evaluation, bonuses
                )
            ]
        return evaluation

    def select_elites(
        self,
        evaluation: list[tuple[DerivationTree, float, list[FailingTree], Suggestion]],
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
        evaluation: list[tuple[DerivationTree, float, list[FailingTree], Suggestion]],
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
        self._past_trees: list[DerivationTree] = []

    def get_past_msgs(
        self, packet_type: Optional[PacketNonTerminal] = None
    ) -> set[DerivationTree]:
        msgs = []
        for tree in self._past_trees:
            msgs.extend(tree.protocol_msgs())
        msg_trees = set(map(lambda x: x.msg, msgs))
        if packet_type is None:
            return msg_trees
        return {
            msg
            for msg in msg_trees
            if isinstance(msg.symbol, NonTerminal)
            and PacketNonTerminal(msg.sender, msg.recipient, msg.symbol) == packet_type
        }

    def start_next_message(self, past_trees: list[DerivationTree]) -> None:
        self._hold_back_solutions.clear()
        self._solution_set.clear()
        self._fitness_cache.clear()
        self._past_trees = past_trees
        for tree in past_trees:
            for msg in tree.protocol_msgs():
                tree = msg.msg
                key = (msg.sender, msg.recipient, tree)
                self._submitted_solutions.add(hash(key))

    def _is_path_start_with(self, state_path: KPath, path: KPath) -> int:
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
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree], Suggestion]]:
        key = hash(individual)
        if key in self._fitness_cache:
            return self._fitness_cache[key]

        generator = GeneratorWithReturn(super().evaluate_individual(individual))
        generator.collect()
        fitness, failing_trees, suggestion = generator.return_value
        self._fitness_cache[key] = (fitness, failing_trees, suggestion)

        if fitness < self._expected_fitness:
            return fitness, failing_trees, suggestion

        if len(individual.protocol_msgs()) != 0:
            msg = individual.protocol_msgs()[-1].msg
            assert isinstance(msg.symbol, NonTerminal)
            msg_key = PacketNonTerminal(msg.sender, msg.recipient, msg.symbol)
            msg_hash = hash(msg)
        else:
            msg = None
            msg_key = None
            msg_hash = None

        if fitness >= self._expected_fitness:
            if msg is None:
                yield individual
            else:
                assert msg_hash is not None and msg_key is not None
                state_path_tree = msg.get_path()
                if len(state_path_tree) > self._diversity_k:
                    state_path_tree = state_path_tree[-self._diversity_k :]
                state_path = tuple(map(lambda x: x.symbol, state_path_tree))
                assert isinstance(msg.symbol, NonTerminal)
                uncovered_paths = self._grammar.get_uncovered_k_paths(
                    list(self.get_past_msgs(msg_key)),
                    self._diversity_k,
                    msg.symbol,
                    True,
                )

                overlap_to_root = any(
                    0 < self._is_path_start_with(state_path, path) < self._diversity_k
                    for path in uncovered_paths
                )

                old_coverage = self._grammar.compute_kpath_coverage(
                    list(self.get_past_msgs(msg_key)),
                    self._diversity_k,
                    msg.symbol,
                    overlap_to_root=overlap_to_root,
                )
                new_coverage = self._grammar.compute_kpath_coverage(
                    list(self.get_past_msgs(msg_key)) + [msg],
                    self._diversity_k,
                    msg.symbol,
                    overlap_to_root=overlap_to_root,
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

        self._fitness_cache[key] = (fitness, failing_trees, suggestion)
        return fitness, failing_trees, suggestion

    def evaluate_population(self, population: list[DerivationTree]) -> Generator[
        DerivationTree,
        None,
        list[tuple[DerivationTree, float, list[FailingTree], Suggestion]],
    ]:
        evaluation: list[
            tuple[DerivationTree, float, list[FailingTree], Suggestion]
        ] = []
        for ind in population:
            ind_eval = yield from self.evaluate_individual(ind)
            evaluation.append((ind, *ind_eval))

        if self._diversity_k > 0 and self._diversity_weight > 0:
            fill_up_by_msg_nt: dict[PacketNonTerminal, list[DerivationTree]] = {}
            for ind in [*self._past_trees, *population]:
                msgs = ind.protocol_msgs()
                for i, msg in enumerate(msgs):
                    assert msg.sender is not None
                    assert isinstance(msg.msg.symbol, NonTerminal)
                    key = PacketNonTerminal(msg.sender, msg.recipient, msg.msg.symbol)
                    if key not in fill_up_by_msg_nt:
                        fill_up_by_msg_nt[key] = []
                    fill_up_by_msg_nt[key].append(msg.msg)

            for i, ind in enumerate(population):
                if len(ind.protocol_msgs()) == 0:
                    continue
                last_msg = ind.protocol_msgs()[-1]
                assert isinstance(last_msg.msg.symbol, NonTerminal)
                key = PacketNonTerminal(
                    last_msg.sender, last_msg.recipient, last_msg.msg.symbol
                )
                bonuses = self.compute_diversity_bonus([ind], fill_up_by_msg_nt[key])
                evaluation[i] = (
                    ind,
                    evaluation[i][1] + bonuses[0],
                    evaluation[i][2],
                    evaluation[i][3],
                )

        return evaluation
