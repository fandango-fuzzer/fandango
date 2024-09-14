import random
import copy

from typing import List, Tuple, Set

from fandango.constraints.base import Constraint, Fitness
from fandango.language.grammar import Grammar, DerivationTree, NonTerminal


class GeneticAlgorithmOptimizer:
    """
    A genetic algorithm optimizer for evolving derivation trees that satisfy a set of constraints.

    :param grammar: The grammar used to generate derivation trees
    :param constraints: A list of constraints to evaluate derivation trees
    :param population_size: The number of derivation trees in the population
    :param generations: The number of generations to evolve the population
    :param elite_fraction: The fraction of top-performing trees to carry over to the next generation
    :param mutation_rate: The probability of mutation for each derivation tree
    :param mutation_method: The mutation method, either 'random' or 'constraint_driven'
    :param crossover_rate: The probability of crossover for each pair of derivation trees
    :param crossover_method: The crossover method, either 'random' or 'constraint_driven'
    :param verbose: Whether to print progress during evolution
    """

    def __init__(self, grammar: Grammar, constraints: List[Constraint], population_size: int = 100,
                 generations: int = 100, elite_fraction: float = 0.1, mutation_rate: float = 0.01,
                 mutation_method: str = "random", crossover_rate: float = 0.2, crossover_method: str = "random",
                 verbose: bool = False):
        self.grammar = grammar
        self.constraints = constraints
        self.generations = generations
        self.population_size = population_size
        self.elite_fraction = elite_fraction
        self.mutation_rate = mutation_rate
        self.mutation_method = mutation_method
        self.crossover_rate = crossover_rate
        self.crossover_method = crossover_method
        self.verbose = verbose

        # Initialize population
        self.population = [self.grammar.fuzz() for _ in range(population_size)]

        self.current_fitness = sum([self.evaluate_fitness(tree)[0] for tree in self.population]) / population_size
        self.current_generation = 0

    def evaluate_fitness(self, tree: DerivationTree) -> Tuple[float, Set[DerivationTree]]:
        """
        Retrieves the fitness score and failing nodes for a derivation tree based on the constraint system.
        :param tree: The derivation tree to evaluate
        :return: A tuple containing a fitness score (normalized between 0 and 1) and a set of failing nodes
        """
        total_fitness = Fitness(0, 0, False)  # Initialize an empty fitness object
        failing_nodes = set()

        # Evaluate the fitness across all constraints
        for constraint in self.constraints:
            constraint_fitness = constraint.fitness(tree)
            total_fitness.solved += constraint_fitness.solved
            total_fitness.total += constraint_fitness.total

            # Assume that each constraint provides a method to get failing nodes
            constraint_failing_nodes = constraint.get_failing_nodes(tree)
            failing_nodes.update(constraint_failing_nodes)

        # Return normalized fitness as solved/total and the failing nodes
        fitness_score = total_fitness.fitness() if total_fitness.total > 0 else 0
        return fitness_score, failing_nodes

    # NOTE: THE SELECTION CAN CHOOSE THE SAME FATHER TWICE IF THERE IS NO OTHER GOOD FIT! (DISCUSS WITH TEAM)
    def select_parents(self) -> List[DerivationTree]:
        """
        Selects two parents from the population using fitness-proportional selection (roulette wheel).
        :return: Two parent derivation trees
        """
        fitness_scores = [self.evaluate_fitness(tree)[0] for tree in self.population]
        total_fitness = sum(fitness_scores)

        if total_fitness == 0:
            # In case all trees have zero fitness, select random parents
            return random.sample(self.population, 2)

        # Use fitness scores as weights for selection
        parent1 = random.choices(self.population, weights=fitness_scores, k=1)[0]
        parent2 = random.choices(self.population, weights=fitness_scores, k=1)[0]

        return [parent1, parent2]

    def select_next_generation(self):
        """
        Selects the next generation of derivation trees based on the current population.
        """
        # Keep a deep copy of the current population
        prev_population = [copy.deepcopy(tree) for tree in self.population]

        next_generation = []

        # Evaluate fitness and collect failing nodes for the current population
        fitness_scores = []
        for tree in self.population:
            fitness, _ = self.evaluate_fitness(tree)
            fitness_scores.append(fitness)

        # Select the best-performing trees to carry over to the next generation
        next_generation.extend(self._select_elites())

        while len(next_generation) < self.population_size:
            parent1, parent2 = self.select_parents()

            # Perform crossover to produce offspring
            if random.random() < self.crossover_rate:
                children = self.crossover(parent1, parent2)
            else:
                children = [copy.deepcopy(parent1), copy.deepcopy(parent2)]

            for child in children:
                if random.random() < self.mutation_rate:
                    child = self.mutate(child)

                next_generation.append(child)
                if len(next_generation) >= self.population_size:
                    break

        # Evaluate fitness of the new generation
        new_fitness_scores = []
        for tree in next_generation:
            fitness, _ = self.evaluate_fitness(tree)
            new_fitness_scores.append(fitness)

        prev_gen_fitness = sum(fitness_scores) / len(fitness_scores)
        current_gen_fitness = sum(new_fitness_scores) / len(new_fitness_scores)

        if current_gen_fitness >= prev_gen_fitness:
            self.population = next_generation
            if self.verbose:
                print("Fitness increased or remained the same.")
        else:
            self.population = prev_population
            if self.verbose:
                print("Fitness decreased. Reverting to previous generation.")

        self.current_generation += 1

    def _select_elites(self) -> List[DerivationTree]:
        """
        Selects the best-performing derivation trees (elites) to carry over to the next generation.
        :return: A list of elite derivation trees
        """
        # Calculate the number of elites to carry over
        num_elites = max(1, int(self.population_size * self.elite_fraction))

        # Sort the population by fitness in descending order
        fitness_scores = [self.evaluate_fitness(tree) for tree in self.population]
        sorted_population = [tree for _, tree in sorted(zip(fitness_scores, self.population), key=lambda pair: pair[0], reverse=True)]

        # Return the top-performing trees
        return sorted_population[:num_elites]

    def crossover(self, parent1: DerivationTree, parent2: DerivationTree) -> List[DerivationTree]:
        """
        Perform intelligent crossover between two parent derivation trees focusing on failing parts.
        :param parent1: First parent tree
        :param parent2: Second parent tree
        :return: A list of two new offspring derivation trees
        """
        if self.crossover_method == "random":
            return self._random_crossover(parent1, parent2)
        elif self.crossover_method == "constraint_driven":
            return self._constraint_driven_crossover(parent1, parent2)
        else:
            raise ValueError("Invalid crossover method. Choose 'random' or 'constraint_driven'.")

    def _random_crossover(self, parent1: DerivationTree, parent2: DerivationTree) -> List[DerivationTree]:
        offspring1 = copy.deepcopy(parent1)
        offspring2 = copy.deepcopy(parent2)

        crossover_point1, parent_node1 = self._random_crossover_point(offspring1)
        crossover_point2, parent_node2 = self._random_crossover_point(offspring2)

        if crossover_point1 is None or crossover_point2 is None:
            return [offspring1, offspring2]

        if parent_node1 and parent_node2:
            parent_node1.children.remove(crossover_point1)
            parent_node1.children.append(crossover_point2)
            parent_node2.children.remove(crossover_point2)
            parent_node2.children.append(crossover_point1)
        else:
            if parent_node1 is None:
                offspring1 = crossover_point2
            if parent_node2 is None:
                offspring2 = crossover_point1

        return [offspring1, offspring2]

    def _random_crossover_point(self, tree: DerivationTree) -> (DerivationTree, DerivationTree):
        all_nodes = []
        self._collect_nodes(tree, all_nodes, None)

        # Exclude root nodes
        valid_nodes = [(node, parent) for node, parent in all_nodes if parent is not None]

        if not valid_nodes:
            return None, None

        node, parent = random.choice(valid_nodes)
        return node, parent

    def _collect_nodes(self, tree: DerivationTree, all_nodes: List[Tuple[DerivationTree, DerivationTree]],
                       parent: DerivationTree):
        """
        Helper function to collect all nodes in a tree along with their parent nodes.
        :param tree: The derivation tree to traverse
        :param all_nodes: The list that accumulates nodes and parents
        :param parent: The parent node of the current tree node
        :return: The updated list of nodes and parents
        """
        if tree is None:
            return
        all_nodes.append((tree, parent))  # Store the current node and its parent
        for child in tree.children:
            self._collect_nodes(child, all_nodes, tree)  # Recursively collect children

    def _constraint_driven_crossover(self, parent1: DerivationTree, parent2: DerivationTree) -> List[DerivationTree]:
        """
        Perform intelligent crossover between two parent derivation trees focusing on failing parts.
        :param parent1: First parent tree
        :param parent2: Second parent tree
        :return: Two offspring derivation trees
        """
        offspring1 = copy.deepcopy(parent1)
        offspring2 = copy.deepcopy(parent2)

        # Get the failing nodes for both parents
        _, failing_nodes1 = self.evaluate_fitness(offspring1)
        _, failing_nodes2 = self.evaluate_fitness(offspring2)

        if failing_nodes1 and failing_nodes2:
            # Select failing nodes to swap
            node1 = random.choice(list(failing_nodes1))
            node2 = random.choice(list(failing_nodes2))

            parent_node1 = node1.parent
            parent_node2 = node2.parent

            if parent_node1 and parent_node2:
                # Swap the nodes between parents
                index1 = parent_node1.children.index(node1)
                index2 = parent_node2.children.index(node2)

                parent_node1.children[index1] = node2
                parent_node2.children[index2] = node1

                # Update parent references
                node2.parent = parent_node1
                node1.parent = parent_node2
            else:
                # If one of the nodes is root, swap entire subtrees
                if parent_node1 is None:
                    offspring1 = node2
                    offspring1.parent = None
                else:
                    parent_node1.children[parent_node1.children.index(node1)] = node2
                    node2.parent = parent_node1

                if parent_node2 is None:
                    offspring2 = node1
                    offspring2.parent = None
                else:
                    parent_node2.children[parent_node2.children.index(node2)] = node1
                    node1.parent = parent_node2
        else:
            # If no failing nodes, perform random crossover to maintain diversity
            offspring1, offspring2 = self._random_crossover(offspring1, offspring2)

        return [offspring1, offspring2]

    def mutate(self, tree: DerivationTree) -> DerivationTree:
        """
        Apply intelligent mutation to a derivation tree focusing on failing parts.
        :param tree: The derivation tree to mutate
        :return: The mutated derivation tree
        """
        tree_copy = copy.deepcopy(tree)

        # Get the failing nodes
        _, failing_nodes = self.evaluate_fitness(tree_copy)

        if failing_nodes:
            # Select a failing node to mutate
            node_to_mutate = random.choice(list(failing_nodes))
            parent_node = node_to_mutate.parent

            # Replace the failing node with a new subtree generated from the same symbol
            new_subtree = NonTerminal(node_to_mutate.symbol.symbol).fuzz(self.grammar.rules)[0]
            new_subtree.parent = parent_node

            if parent_node:
                index = parent_node.children.index(node_to_mutate)
                parent_node.children[index] = new_subtree
            else:
                # If the failing node is the root, replace the entire tree
                tree_copy = new_subtree
                tree_copy.parent = None
        else:
            # No failing nodes, perform random mutation to maintain diversity
            tree_copy = self._random_mutation(tree_copy)

        return tree_copy

    def _random_mutation(self, tree: DerivationTree) -> DerivationTree:
        node_to_mutate, parent_node = self._random_crossover_point(tree)

        if parent_node:
            parent_node.children.remove(node_to_mutate)
            parent_node.children.append(self.grammar.fuzz())
        else:
            tree = self.grammar.fuzz()

        return tree

    def evolve(self) -> [DerivationTree]:
        """
        Evolves the population for a specified number of generations.
        :return: The final population of derivation trees
        """
        for generation in range(self.generations):
            # Evolve the population to the next generation
            self.select_next_generation()

            # Evaluate the fitness of the new population
            fitness_scores = [self.evaluate_fitness(tree)[0] for tree in self.population]
            self.current_fitness = sum(fitness_scores) / len(fitness_scores)

            if self.verbose:
                print(f"Generation {generation + 1}: average fitness = {self.current_fitness:.4f}")

            # Stop early if the entire population reaches perfect fitness
            if self.current_fitness > 0.80:
                print(f"All individuals have perfect fitness in generation {generation + 1}")
                break

        return self.population
