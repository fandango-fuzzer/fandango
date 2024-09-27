import copy
import random
from typing import Set

from fandango.evolution.fitness import evaluate_fitness
from fandango.language.grammar import Grammar, NonTerminal, DerivationTree


def random_subtree_replacement(
    individual: DerivationTree, grammar: Grammar
) -> DerivationTree:
    # Deep copy the individual to avoid modifying the original
    mutant = copy.deepcopy(individual)

    # Collect all non-terminal nodes in the tree
    non_terminal_nodes = []

    def collect_non_terminals(node):
        if isinstance(node.symbol, NonTerminal):
            non_terminal_nodes.append(node)
        for child in node.children:
            collect_non_terminals(child)

    collect_non_terminals(mutant)

    if not non_terminal_nodes:
        # No non-terminal nodes to mutate
        return mutant

    # Select a random non-terminal node
    node_to_replace = random.choice(non_terminal_nodes)
    parent_node = node_to_replace.parent

    # Generate a new subtree from the same non-terminal symbol
    new_subtree = generate_tree_from_symbol(grammar, node_to_replace.symbol)

    # Replace the old subtree with the new subtree
    if parent_node:
        index = parent_node.children.index(node_to_replace)
        parent_node.children[index] = new_subtree
        new_subtree.parent = parent_node
    else:
        # If the node to replace is the root, return the new subtree
        mutant = new_subtree
        mutant.parent = None

    return mutant


def generate_tree_from_symbol(grammar: Grammar, symbol: NonTerminal) -> DerivationTree:
    # Generate a new derivation tree starting from the given non-terminal symbol
    return symbol.fuzz(grammar.rules)[0]


def constraint_guided_mutation(
    individual: DerivationTree, failing_nodes: Set[DerivationTree], grammar: Grammar
) -> DerivationTree:
    # Deep copy the individual
    mutant = copy.deepcopy(individual)

    # If there are no failing nodes, default to random mutation
    if not failing_nodes:
        return random_subtree_replacement(mutant, grammar)

    # Select a failing node to mutate
    node_to_mutate = random.choice(list(failing_nodes))
    parent_node = node_to_mutate.parent

    # Generate a new subtree from the same non-terminal symbol
    new_subtree = generate_tree_from_symbol(grammar, node_to_mutate.symbol)

    # Replace the failing node's subtree with the new subtree
    if parent_node:
        index = parent_node.children.index(node_to_mutate)
        parent_node.children[index] = new_subtree
        new_subtree.parent = parent_node
    else:
        # If the node to mutate is the root
        mutant = new_subtree
        mutant.parent = None

    return mutant


if __name__ == "__main__":
    from fandango.language.parse import parse_file

    # Parse grammar from src/evaluation/csv/csv.fan
    grammar, constraints, _ = parse_file("../../evaluation/csv/csv.fan")

    print("Random subtree replacement:")
    # Generate a random derivation tree
    tree = generate_tree_from_symbol(grammar, NonTerminal("<start>"))
    print(tree)

    # Mutate the tree by replacing a random subtree
    mutated_tree = random_subtree_replacement(tree, grammar)
    print(mutated_tree)

    print("\nConstraint-guided mutation:")
    # Generate a random derivation tree
    tree = generate_tree_from_symbol(grammar, NonTerminal("<start>"))
    print(tree)

    # Mutate the tree by replacing a failing subtree
    _, failing_nodes = evaluate_fitness(tree, constraints, {})
    mutated_tree = constraint_guided_mutation(tree, failing_nodes, grammar)

    print(mutated_tree)
