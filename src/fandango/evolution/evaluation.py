from collections.abc import Generator

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.constraints.failing_tree import FailingTree
from fandango.language import DerivationTree, Grammar
from fandango.logger import LOGGER


class Evaluator:
    def __init__(
        self,
        grammar: Grammar,
        constraints: list[Constraint | SoftValue],
    ):
        self._grammar = grammar
        self._soft_constraints: list[SoftValue] = []
        self._hard_constraints: list[Constraint] = []
        self._checks_made = 0

        for constraint in constraints:
            if isinstance(constraint, SoftValue):
                self._soft_constraints.append(constraint)
            elif isinstance(constraint, Constraint):
                self._hard_constraints.append(constraint)
            else:
                raise ValueError(f"Invalid constraint type: {type(constraint)}")

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
                    f"Error evaluating hard constraint {constraint.format_as_spec()}: {e}"
                )
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
                LOGGER.error(
                    f"Error evaluating soft constraint {constraint.format_as_spec()}: {e}"
                )
                soft_fitness += 0.0

        soft_fitness /= len(self._soft_constraints)
        return soft_fitness, failing_trees

    def evaluate_individual(
        self,
        individual: DerivationTree,
    ) -> Generator[DerivationTree, None, tuple[float, list[FailingTree]]]:

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

        if fitness >= 1.0:
            yield individual

        return fitness, failing_trees

    def evaluate_population(
        self,
        population: list[DerivationTree],
    ) -> Generator[
        DerivationTree, None, list[tuple[DerivationTree, float, list[FailingTree]]]
    ]:
        results: list[tuple[DerivationTree, float, list[FailingTree]]] = []
        for individual in population:
            fitness, failing_trees = yield from self.evaluate_individual(individual)
            results.append((individual, fitness, failing_trees))
        return results
