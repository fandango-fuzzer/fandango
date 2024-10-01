# evolution/algorithm.py

import copy
import random
import time
from typing import List, Set, Tuple

from fandango.constraints.base import Constraint
from fandango.language.grammar import Grammar, DerivationTree, NonTerminal, Terminal, Alternative, Node, Concatenation, \
    Repetition
from fandango.language.parse import parse_file


class FANDANGO:
    def __init__(
            self,
            grammar: Grammar,
            constraints: List[Constraint],
            population_size: int = 100,
            mutation_rate: float = 0.2,
            crossover_rate: float = 0.7,
            max_generations: int = 100,
            elitism_rate: float = 0.1,
            verbose: bool = True,
            constraintsOverSuite: bool = False
    ):
        """
        Initialize the FANDANGO genetic algorithm.
        """
        self.grammar = grammar
        self.constraints = constraints
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations
        self.elitism_rate = elitism_rate
        self.tournament_size = max(10, int(0.1 * population_size))
        self.verbose = verbose
        self.constraintsOverSuite = constraintsOverSuite

        # Initialize population
        self.population = self.generate_initial_population(grammar, population_size)
        self.fitness_cache = {}
        self.fitness, _ = self.evaluate_population(self.population, constraints)
        self.solution = None

        self.mutations_made = 0
        self.crossovers_made = 0

    def generate_initial_population(self, grammar: Grammar, population_size: int) -> List[DerivationTree]:
        """
        Generates an initial population of derivation trees using the fuzzer.

        :param grammar: The Grammar object containing production rules.
        :param population_size: The desired size of the population.
        :return: A list of diverse derivation trees.
        """
        population = []
        for _ in range(population_size):
            population.append(grammar.fuzz())

        return population

    def extract_terminals(self, node: Node) -> List[str]:
        """
        Extracts terminal symbols from a grammar node.

        :param node: The grammar node to extract terminals from.
        :return: A list of terminal symbols.
        """
        terminals = []
        if isinstance(node, Terminal):
            terminals.append(node.symbol)
        elif isinstance(node, NonTerminal):
            # Non-terminals do not contain terminals directly
            pass
        elif isinstance(node, Alternative):
            for sub_node in node.alternatives:
                terminals.extend(self.extract_terminals(sub_node))
        elif isinstance(node, Concatenation):
            for sub_node in node.nodes:
                terminals.extend(self.extract_terminals(sub_node))
        elif isinstance(node, Repetition):
            terminals.extend(self.extract_terminals(node.node))
        return terminals

    def evaluate_fitness(
            self, individual: DerivationTree, constraints: List[Constraint]
    ) -> Tuple[float, Set[DerivationTree]]:
        """
        Evaluates the fitness of an individual derivation tree, using a cache to avoid redundant computations.
        """
        # Use the hash representation as the cache key
        individual_hash = hash(individual)
        if individual_hash in self.fitness_cache:
            return self.fitness_cache[individual_hash]

        total_fitness = 0.0
        total_constraints = len(constraints)
        failing_nodes = set()

        for constraint in constraints:
            fitness_result = constraint.fitness(individual)
            total_fitness += fitness_result.fitness()
            failing_nodes.update(fitness_result.failing_trees)

        # Normalize the fitness score to be between 0 and 1
        fitness_score = (
            total_fitness / total_constraints if total_constraints > 0 else 0.0
        )

        # Cache the result
        self.fitness_cache[individual_hash] = (fitness_score, failing_nodes)

        return fitness_score, failing_nodes

    def evaluate_population(
            self, population: List[DerivationTree], constraints: List[Constraint]
    ) -> Tuple[List[Tuple[DerivationTree, float, Set[DerivationTree]]], List[DerivationTree]]:
        """
        Evaluates the fitness of each individual in the population, using caching.
        """
        evaluated_population = []
        valid_inputs = []
        for individual in population:
            fitness_score, failing_nodes = self.evaluate_fitness(
                individual, constraints
            )
            evaluated_population.append((individual, fitness_score, failing_nodes))
            if fitness_score >= 0.95:
                valid_inputs.append(individual)
        return evaluated_population, valid_inputs

    def select_elites(
            self, population: List[Tuple[DerivationTree, float, Set[DerivationTree]]]
    ) -> List[DerivationTree]:
        """
        Select the elite individuals from the population based on their fitness scores.

        :param population: A list of tuples containing the individual, its fitness score, and failing nodes.
        :return: A list of elite individuals.
        """
        # Sort the population by fitness score in descending order
        sorted_population = sorted(population, key=lambda x: x[1], reverse=True)

        # Determine the number of elites
        num_elites = max(1, int(self.elitism_rate * len(population)))

        # Select the elite individuals
        elites = [individual for individual, _, _ in sorted_population[:num_elites]]

        return elites

    @staticmethod
    def fitness_proportionate_selection(
            population: List[Tuple[DerivationTree, float, Set[DerivationTree]]]
    ) -> DerivationTree:
        """
        Select an individual from the population using fitness-proportionate selection. Uses choices with k based on
        fitness.

        :param population: A list of tuples containing the individual, its fitness score, and failing nodes.
        :return: A selected parent individual.
        """
        total_fitness = sum(fitness for _, fitness, _ in population)

        if total_fitness == 0:
            return random.choice(population)[0]

        probabilities = [fitness / total_fitness for _, fitness, _ in population]
        return random.choices(population, weights=probabilities, k=1)[0][0]

    def crossover(
            self, population: List[Tuple[DerivationTree, float, Set[DerivationTree]]]
    ) -> List[DerivationTree]:
        """
        Perform crossover operations to produce offspring.

        :param population: A list of tuples containing the individual, its fitness score, and failing nodes.
        :return: A list of offspring individuals.
        """
        offspring = self.select_elites(population)

        while len(offspring) < self.population_size:
            # Select parents using fitness-proportionate selection
            parent1 = self.fitness_proportionate_selection(population)
            parent2 = self.fitness_proportionate_selection(population)
            while parent2 == parent1:
                parent2 = self.fitness_proportionate_selection(population)

            # Decide whether to perform crossover
            if random.random() < self.crossover_rate:
                # Perform crossover to produce two offspring
                child1, child2 = self.crossover_parents(parent1, parent2)

                # Compute the fitness and store it in the cache
                child1_hash = hash(child1)
                child2_hash = hash(child2)

                self.fitness_cache[child1_hash] = self.evaluate_fitness(
                    child1, self.constraints
                )
                self.fitness_cache[child2_hash] = self.evaluate_fitness(
                    child2, self.constraints
                )

                # Add offspring to the new population
                offspring.extend([child1, child2])
            else:
                # No crossover; add the parents to the new population
                offspring.extend([copy.deepcopy(parent1), copy.deepcopy(parent2)])

        # Trim the offspring list to match the population size
        offspring = offspring[: self.population_size]

        return offspring

    def crossover_parents(
            self, parent1: DerivationTree, parent2: DerivationTree
    ) -> Tuple[DerivationTree, DerivationTree]:
        """
        Crossover two parent derivation trees to produce two offspring, focusing on failing subtrees.

        :param parent1: The first parent derivation tree.
        :param parent2: The second parent derivation tree.
        :return: Two offspring derivation trees.
        """
        # Make deep copies of the parents to create offspring
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)

        # Get failing nodes from parents
        failing_nodes_parent1 = self.get_failing_nodes(child1)
        failing_nodes_parent2 = self.get_failing_nodes(child2)

        # Find matching failing nodes
        matching_failing_nodes = self.get_matching_nodes(
            failing_nodes_parent1, failing_nodes_parent2
        )

        if matching_failing_nodes:
            # Swap at a matching failing node
            node1, node2 = random.choice(matching_failing_nodes)
        else:
            # Find any matching non-terminal nodes
            matching_nodes = self.get_matching_nonterminal_nodes(child1, child2)
            if matching_nodes:
                node1, node2 = random.choice(matching_nodes)
            else:
                # No matching nodes; return the original children
                return child1, child2

        # Swap subtrees at the selected nodes
        self.swap_subtrees(node1, node2)

        return child1, child2

    def get_failing_nodes(self, tree: DerivationTree) -> List[DerivationTree]:
        """
        Retrieve the list of failing nodes for a given tree from the fitness cache.

        :param tree: The derivation tree.
        :return: A list of failing nodes.
        """
        individual_hash = hash(tree)
        fitness_info = self.fitness_cache.get(individual_hash)
        if fitness_info:
            return list(fitness_info[1])  # The set of failing nodes
        else:
            # If not in cache, evaluate fitness
            fitness_score, failing_nodes = self.evaluate_fitness(tree, self.constraints)
            return list(failing_nodes)

    @staticmethod
    def get_matching_nodes(
            nodes1: List[DerivationTree], nodes2: List[DerivationTree]
    ) -> List[Tuple[DerivationTree, DerivationTree]]:
        """
        Find all pairs of nodes from two lists where the non-terminal symbols match.

        :param nodes1: A list of nodes from the first tree.
        :param nodes2: A list of nodes from the second tree.
        :return: A list of tuples containing matching nodes from both lists.
        """
        nodes_dict2 = {}
        for node in nodes2:
            if isinstance(node.symbol, NonTerminal):
                nodes_dict2.setdefault(node.symbol.symbol, []).append(node)

        matching_nodes = []
        for node1 in nodes1:
            if isinstance(node1.symbol, NonTerminal):
                symbol = node1.symbol.symbol
                if symbol in nodes_dict2:
                    for node2 in nodes_dict2[symbol]:
                        matching_nodes.append((node1, node2))

        return matching_nodes

    @staticmethod
    def get_matching_nonterminal_nodes(
            tree1: DerivationTree, tree2: DerivationTree
    ) -> List[Tuple[DerivationTree, DerivationTree]]:
        """
        Find all pairs of nodes from two trees where the non-terminal symbols match.

        :param tree1: The first derivation tree.
        :param tree2: The second derivation tree.
        :return: A list of tuples containing matching nodes from both trees.
        """
        nodes1 = []
        nodes2 = {}

        def collect_nodes(node, nodes_list):
            if isinstance(node.symbol, NonTerminal):
                nodes_list.append(node)
            for child in node.children:
                collect_nodes(child, nodes_list)

        def collect_nodes_dict(node, nodes_dict):
            if isinstance(node.symbol, NonTerminal):
                nodes_dict.setdefault(node.symbol.symbol, []).append(node)
            for child in node.children:
                collect_nodes_dict(child, nodes_dict)

        collect_nodes(tree1, nodes1)
        collect_nodes_dict(tree2, nodes2)

        matching_nodes = []
        for node1 in nodes1:
            symbol = node1.symbol.symbol
            if symbol in nodes2:
                for node2 in nodes2[symbol]:
                    matching_nodes.append((node1, node2))

        return matching_nodes

    def swap_subtrees(self, node1: DerivationTree, node2: DerivationTree):
        """
        Swap the subtrees rooted at node1 and node2.

        :param node1: The node in the first tree.
        :param node2: The node in the second tree.
        """
        # Swap the nodes in their respective parents
        parent1 = node1.parent
        parent2 = node2.parent

        if parent1 is None or parent2 is None:
            # Cannot swap root nodes
            return

        # Find the indices of node1 and node2 in their parents' children
        index1 = parent1.children.index(node1)
        index2 = parent2.children.index(node2)

        # Swap the nodes
        parent1.children[index1], parent2.children[index2] = node2, node1

        # Update parent references
        node1.parent = parent2
        node2.parent = parent1

        self.crossovers_made += 1

    def mutation(
            self, population: List[Tuple[DerivationTree, float, Set[DerivationTree]]]
    ) -> List[DerivationTree]:
        """
        Apply mutation operations to the population, focusing on failing nodes.

        :param population: A list of tuples containing the individual, its fitness score, and failing nodes.
        :return: A new list of mutated individuals.
        """
        mutated_population = []
        for individual, fitness_score, failing_nodes in population:
            # Decide whether to mutate this individual
            if random.random() < self.mutation_rate:
                # Make a deep copy of the individual to avoid modifying the original
                mutated_individual = copy.deepcopy(individual)
                # If there are failing nodes, focus mutation on them
                if failing_nodes:
                    node_to_mutate = random.choice(list(failing_nodes))
                else:
                    # If there are no failing nodes, select a random node to mutate
                    node_to_mutate = self.select_random_node(mutated_individual)

                # Perform the mutation
                self.mutate_node(node_to_mutate)

                # Compute the fitness and store it in the cache
                mutated_individual_hash = hash(mutated_individual)
                self.fitness_cache[mutated_individual_hash] = self.evaluate_fitness(
                    mutated_individual, self.constraints
                )

                mutated_population.append(mutated_individual)
            else:
                # No mutation; keep the individual as is
                mutated_population.append(individual)

        return mutated_population

    def mutate_node(self, node: DerivationTree):
        """
        Mutate a node in the derivation tree by replacing it with a new subtree generated from the same non-terminal.

        :param node: The node to mutate.
        """
        if isinstance(node.symbol, NonTerminal):
            non_terminal = node.symbol.symbol
            # Generate a new subtree from the same non-terminal
            new_subtree = NonTerminal(non_terminal).fuzz(self.grammar.rules)[0]
            # Replace the node's children and symbol with those of the new subtree
            node.symbol = new_subtree.symbol
            node.children = new_subtree.children
            # Update parent references in the children
            for child in node.children:
                child.parent = node
        else:
            # If the node is a terminal, replace it with a new terminal
            node.symbol = node.symbol.fuzz(self.grammar.rules)[0].symbol

        self.mutations_made += 1

    @staticmethod
    def select_random_node(tree: DerivationTree) -> DerivationTree:
        """
        Select a random node from the derivation tree.

        :param tree: The derivation tree to select from.
        :return: A randomly selected node.
        """
        nodes = []

        def traverse(node):
            nodes.append(node)
            for child in node.children:
                traverse(child)

        traverse(tree)
        return random.choice(nodes)

    def evolve(self):
        """
        Run the genetic algorithm to evolve the population over multiple generations.
        """
        valid_solutions = set()

        for generation in range(1, self.max_generations + 1):
            if self.verbose:
                print(f"Generation {generation}")

            # Evaluate population
            evaluated_population, valid_inputs = self.evaluate_population(
                self.population, self.constraints
            )

            valid_solutions.update(str(individual) for individual in valid_inputs)

            # Check for termination condition
            total_fitness = sum(
                fitness for _, fitness, _ in evaluated_population
            ) / len(evaluated_population)
            if self.verbose:
                print(f"Average fitness in generation {generation}: {total_fitness}")

            if total_fitness >= 0.95 or generation == self.max_generations or (len(
                    valid_solutions) >= self.population_size and not self.constraintsOverSuite):
                if self.verbose:
                    print("Termination condition met.")
                    print(f"Total mutations made: {self.mutations_made}")
                    print(f"Total crossovers made: {self.crossovers_made}")
                break

            # Selection and Crossover
            offspring = self.crossover(evaluated_population)

            # Mutation
            evaluated_offspring, _ = self.evaluate_population(offspring, self.constraints)
            mutated_offspring = self.mutation(evaluated_offspring)

            # remove the valid inputs from the mutated_offspring
            for valid_input in valid_inputs:
                if valid_input in mutated_offspring:
                    mutated_offspring.remove(valid_input)

            # After mutation, remove duplicates
            unique_individuals = {}
            for individual in mutated_offspring:
                key = str(individual)
                if key not in unique_individuals:
                    unique_individuals[key] = individual

            # Fill gaps with new individuals if necessary
            while len(unique_individuals) < self.population_size:
                new_individual = self.grammar.fuzz()
                key = str(new_individual)
                if key not in unique_individuals:
                    unique_individuals[key] = new_individual

            # Update population
            self.population = list(unique_individuals.values())[:self.population_size]

            if self.verbose:
                print(f"Population size: {len(self.population)}")
                print(f"Valid solutions: {len(valid_solutions)}")
                print(f"Population: {self.population}")

        self.solution = valid_solutions


if __name__ == "__main__":
    grammar_, constraints_ = parse_file("../../evaluation/int/int.fan")

    fandango = FANDANGO(grammar_, constraints_, max_generations=1000, verbose=True, constraintsOverSuite=True)

    start_time = time.time()
    fandango.evolve()
    end_time = time.time()

    print(f"\nBest solution found (in {end_time - start_time:.2f}s):")
    print(fandango.solution)
