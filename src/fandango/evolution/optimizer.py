import random
from typing import List, Tuple

from fandango.constraints.base import Constraint, Fitness
from fandango.language.grammar import Grammar, DerivationTree


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
                 mutation_method: str = "random", crossover_rate: float = 0.7, crossover_method: str = "random",
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

        self.current_fitness = sum([self.evaluate_fitness(tree) for tree in self.population]) / population_size
        self.current_generation = 0

    def evaluate_fitness(self, tree: DerivationTree) -> float:
        """
        Retrieves the fitness score for a derivation tree based on the constraint system.
        :param tree: The derivation tree to evaluate
        :return: A fitness score, normalized between 0 and 1
        """
        total_fitness = Fitness(0, 0, False)  # Initialize an empty fitness object

        # Evaluate the fitness across all constraints
        for constraint in self.constraints:
            constraint_fitness = constraint.fitness(tree)
            total_fitness.solved += constraint_fitness.solved
            total_fitness.total += constraint_fitness.total

        # Return normalized fitness as solved/total
        return total_fitness.fitness() if total_fitness.total > 0 else 0

    # NOTE: THE SELECTION CAN CHOOSE THE SAME FATHER TWICE IF THERE IS NO OTHER GOOD FIT! (DISCUSS WITH TEAM)
    def select_parents(self) -> List[DerivationTree]:
        """
        Selects two parents from the population using fitness-proportional selection (roulette wheel).
        :return: Two parent derivation trees
        """
        fitness_scores = [self.evaluate_fitness(tree) for tree in self.population]
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
        next_generation = []

        # Select the best-performing trees to carry over to the next generation
        next_generation.extend(self._select_elites())

        # Fill up the rest of the population with offspring
        # NOTE: DO WE FILL THE POP WITH OFFSPRING UNTIL WE REACH POP SIZE? OR DO WE FEED THE PARENTS OVER AND OVER BASED ON THE CROSS% (DISCUSS WITH TEAM)
        while len(next_generation) < self.population_size:
            # Select two parents
            parent1, parent2 = self.select_parents()

            # Perform crossover to produce offspring
            if random.random() < self.crossover_rate:
                children = self.crossover(parent1, parent2)
            else:
                children = [parent1, parent2]

            if random.random() < self.mutation_rate:
                children = [self.mutate(child) for child in children]

            next_generation.extend(children)

        # Update the population
        self.population = next_generation[:self.population_size]
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
        sorted_population = [tree for _, tree in
                             sorted(zip(fitness_scores, self.population), key=lambda pair: pair[0], reverse=True)]

        # Return the top-performing trees
        return sorted_population[:num_elites]

    def crossover(self, parent1: DerivationTree, parent2: DerivationTree) -> List[
        DerivationTree]:
        """
        Perform crossover between two parent derivation trees using the specified method.
        :param parent1: First parent tree
        :param parent2: Second parent tree
        :param method: The crossover method, either 'random' or 'constraint_driven'
        :return: A list of two new offspring derivation trees
        """
        if self.crossover_method == "random":
            return self._random_crossover(parent1, parent2)
        elif self.crossover_method == "constraint_driven":
            # NOTE: SHOULD WE ALLOW TO CROSSOVER TWO PERFECT PARENTS? IN THIS CASE, SHOULD WE CROSSOVER UNTIL WE HAVE PERFECT POPULATION? (DISCUSS WITH TEAM)
            raise ValueError("Method not implemented yet")
        else:
            raise ValueError("Invalid crossover method. Choose 'random' or 'constraint_driven'.")

    def _random_crossover(self, parent1: DerivationTree, parent2: DerivationTree) -> List[DerivationTree]:
        """
        Perform random crossover between two parent derivation trees.
        :param parent1: First parent tree
        :param parent2: Second parent tree
        :return: Two offspring derivation trees
        """
        # Randomly select crossover points in both parents
        crossover_point1, parent_node1 = self._random_crossover_point(parent1)
        crossover_point2, parent_node2 = self._random_crossover_point(parent2)

        # Swap the subtrees
        if parent_node1 and parent_node2:
            parent_node1.children.remove(crossover_point1)
            parent_node1.children.append(crossover_point2)

            parent_node2.children.remove(crossover_point2)
            parent_node2.children.append(crossover_point1)

        return [parent1, parent2]

    def _random_crossover_point(self, tree: DerivationTree) -> (DerivationTree, DerivationTree):
        """
        Selects a random crossover point in a derivation tree.
        :param tree: The derivation tree to search
        :return: A tuple of the selected node and its parent
        """
        # Flatten the tree into a list of nodes and their parents
        all_nodes = []
        self._collect_nodes(tree, all_nodes, None)

        # Select a random node for crossover
        node, parent = random.choice(all_nodes)
        return node, parent

    def _collect_nodes(self, tree: DerivationTree, all_nodes: List[Tuple[DerivationTree, DerivationTree]],
                       parent: DerivationTree):
        """
        Helper function to collect all nodes in a tree along with their parent nodes.
        :param tree: The derivation tree to traverse
        :param all_nodes: The list that accumulates nodes and parents
        :param parent: The parent node of the current tree node
        """
        all_nodes.append((tree, parent))  # Store the current node and its parent
        for child in tree.children:
            self._collect_nodes(child, all_nodes, tree)  # Recursively collect children

    def mutate(self, tree: DerivationTree) -> DerivationTree:
        """
        Apply mutation to a derivation tree using the specified method.
        :param tree: The derivation tree to mutate
        :return: The mutated derivation tree
        """
        if self.mutation_method == "random":
            return self._random_mutation(tree)
        elif self.mutation_method == "constraint_driven":
            raise ValueError("Method not implemented yet")
        else:
            raise ValueError("Invalid mutation method. Choose 'random' or 'constraint_driven'.")

    def _random_mutation(self, tree: DerivationTree) -> DerivationTree:
        """
        Apply random mutation to a derivation tree.
        :param tree: The derivation tree to mutate
        :return: The mutated derivation tree
        """

        if random.random() < self.mutation_rate:
            # Select a random node in the tree to mutate
            node_to_mutate, parent_node = self._random_crossover_point(tree)

            # Replace the node with a random subtree
            if parent_node:
                parent_node.children.remove(node_to_mutate)
                parent_node.children.append(self.grammar.fuzz())

            return tree

    # CHECK TEST TO GET AN EXPLANATION OF THE ERROR
    def evolve(self) -> [DerivationTree]:
        """
        Evolves the population for a specified number of generations.
        :return: The final population of derivation trees
        """
        for generation in range(self.generations):
            # Evolve the population to the next generation
            self.select_next_generation()

            # Evaluate the fitness of the new population
            fitness_scores = [self.evaluate_fitness(tree) for tree in self.population]
            self.current_fitness = sum(fitness_scores) / self.population_size

            if self.verbose:
                print(f"Generation {generation + 1}: average fitness = {self.current_fitness:.4f}")

            # Stop early if the entire population reaches perfect fitness
            if all(fitness == 1.0 for fitness in fitness_scores):
                print(f"All individuals have perfect fitness in generation {generation + 1}")
                break

        return self.population
