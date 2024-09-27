import random
import copy
from typing import Tuple, List, Dict

from fandango.language.grammar import DerivationTree, NonTerminal, Grammar


def random_crossover(
    parent1: DerivationTree, parent2: DerivationTree
) -> Tuple[DerivationTree, DerivationTree]:
    # Deep copy the parents to avoid modifying the originals
    offspring1 = copy.deepcopy(parent1)
    offspring2 = copy.deepcopy(parent2)

    # Collect potential crossover points (non-terminal nodes) from both parents
    crossover_points1 = collect_non_terminal_nodes(offspring1)
    crossover_points2 = collect_non_terminal_nodes(offspring2)

    if not crossover_points1 or not crossover_points2:
        # No crossover possible, return copies of the parents
        return offspring1, offspring2

    # Select random crossover points
    crossover_node1 = random.choice(crossover_points1)
    crossover_node2 = random.choice(crossover_points2)

    # Swap subtrees
    swap_subtrees(crossover_node1, crossover_node2)

    return offspring1, offspring2


def collect_non_terminal_nodes(tree: DerivationTree) -> List[DerivationTree]:
    non_terminal_nodes = []

    def traverse(node):
        if isinstance(node.symbol, NonTerminal):
            non_terminal_nodes.append(node)
        for child in node.children:
            traverse(child)

    traverse(tree)
    return non_terminal_nodes


def swap_subtrees(node1: DerivationTree, node2: DerivationTree):
    parent1 = node1.parent
    parent2 = node2.parent

    if parent1 is None or parent2 is None:
        # Cannot swap the root node
        return

    # Find the indices of the nodes in their parents' children lists
    index1 = parent1.children.index(node1)
    index2 = parent2.children.index(node2)

    # Swap the nodes
    parent1.children[index1], parent2.children[index2] = node2, node1

    # Update parent references
    node1.parent, node2.parent = parent2, parent1


def type_safe_crossover(
    parent1: DerivationTree, parent2: DerivationTree
) -> Tuple[DerivationTree, DerivationTree]:
    # Deep copy the parents
    offspring1 = copy.deepcopy(parent1)
    offspring2 = copy.deepcopy(parent2)

    # Collect nodes indexed by their non-terminal symbols
    nodes1 = collect_nodes_by_symbol(offspring1)
    nodes2 = collect_nodes_by_symbol(offspring2)

    # Find common non-terminal symbols
    common_symbols = set(nodes1.keys()) & set(nodes2.keys())

    if not common_symbols:
        # No compatible crossover points, return copies of parents
        return offspring1, offspring2

    # Select a random common symbol
    symbol = random.choice(list(common_symbols))

    # Select random nodes with the chosen symbol from both parents
    node1 = random.choice(nodes1[symbol])
    node2 = random.choice(nodes2[symbol])

    # Swap subtrees
    swap_subtrees(node1, node2)

    return offspring1, offspring2


def collect_nodes_by_symbol(tree: DerivationTree) -> Dict[str, List[DerivationTree]]:
    nodes_by_symbol = {}

    def traverse(node):
        if isinstance(node.symbol, NonTerminal):
            symbol = node.symbol.symbol
            if symbol not in nodes_by_symbol:
                nodes_by_symbol[symbol] = []
            nodes_by_symbol[symbol].append(node)
        for child in node.children:
            traverse(child)

    traverse(tree)
    return nodes_by_symbol


def generate_tree_from_symbol(grammar: Grammar, symbol: NonTerminal) -> DerivationTree:
    # Generate a new derivation tree starting from the given non-terminal symbol
    return symbol.fuzz(grammar.rules)[0]


if __name__ == "__main__":
    # Example usage
    from fandango.language.grammar import DerivationTree, NonTerminal
    from fandango.language.parse import parse_file

    # Load a grammar from a file
    grammar, constraints, _ = parse_file("../../evaluation/csv/csv.fan")

    # Generate two random derivation trees
    parent1 = generate_tree_from_symbol(grammar, NonTerminal("<start>"))
    parent2 = generate_tree_from_symbol(grammar, NonTerminal("<start>"))

    print("Performing random crossover:")
    print("Parent 1:" + str(parent1))
    print("Parent 2:" + str(parent2))

    offspring1, offspring2 = random_crossover(parent1, parent2)

    print("Offspring 1:" + str(offspring1))
    print("Offspring 2:" + str(offspring2))

    print("Performing type-safe crossover:")
    print("Parent 1:" + str(parent1))
    print("Parent 2:" + str(parent2))

    offspring1, offspring2 = type_safe_crossover(parent1, parent2)

    print("Offspring 1:" + str(offspring1))
    print("Offspring 2:" + str(offspring2))
