import random
from typing import List, Optional

from fandango.language.grammar import (
    DerivationTree,
    Node,
    Terminal,
    NonTerminal,
    Alternative,
    Concatenation,
    Repetition,
    Grammar,
)


def generate_initial_population(
    grammar: Grammar, population_size: int
) -> List[DerivationTree]:
    """
    Generates an initial population of derivation trees using the fuzzer.
    Ensures diversity by varying the depth and choices in the grammar expansion.

    :param grammar: The Grammar object containing production rules.
    :param population_size: The desired size of the population.
    :return: A list of diverse derivation trees.
    """
    population = []
    seen_trees = set()

    max_attempts = population_size * 10  # To prevent infinite loops
    attempts = 0

    while len(population) < population_size and attempts < max_attempts:
        # Generate a new derivation tree
        tree = generate_tree_with_random_depth(grammar, max_depth=random.randint(1, 10))

        # Use the string representation as a simple hash to detect duplicates
        tree_str = str(tree)
        if tree_str not in seen_trees:
            population.append(tree)
            seen_trees.add(tree_str)

        attempts += 1

    if len(population) < population_size:
        print(f"Warning: Could only generate {len(population)} unique individuals.")

    return population


def generate_tree_with_random_depth(
    grammar: Grammar,
    max_depth: int,
    current_depth: int = 0,
    symbol: Optional[NonTerminal] = None,
) -> DerivationTree:
    """
    Recursively generates a derivation tree with a random structure, up to a maximum depth.

    :param grammar: The Grammar object containing production rules.
    :param max_depth: The maximum depth allowed for the tree.
    :param current_depth: The current depth in the recursion.
    :param symbol: The current NonTerminal symbol to expand.
    :return: A DerivationTree object.
    """
    if symbol is None:
        symbol = NonTerminal("<start>")  # Assuming <start> is the starting symbol

    # Base case: If maximum depth reached, select only terminals
    if current_depth >= max_depth or symbol.symbol not in grammar.rules:
        # Try to select a terminal expansion if possible
        node = grammar.rules.get(symbol.symbol, Terminal(""))
        if isinstance(node, Terminal):
            return DerivationTree(node)
        else:
            # Select a random terminal from the possible expansions
            terminals = extract_terminals(node)
            if terminals:
                terminal_symbol = random.choice(terminals)
                return DerivationTree(Terminal(terminal_symbol))
            else:
                # If no terminals are available, return an empty tree
                return DerivationTree(Terminal(""))

    # Recursive case: Expand the non-terminal symbol
    node = grammar.rules[symbol.symbol]

    if isinstance(node, Alternative):
        # Randomly select one of the alternatives
        selected_node = random.choice(node.alternatives)
    else:
        selected_node = node

    children = []
    if isinstance(selected_node, Concatenation):
        for sub_node in selected_node.nodes:
            if isinstance(sub_node, NonTerminal):
                child = generate_tree_with_random_depth(
                    grammar, max_depth, current_depth + 1, sub_node
                )
                children.append(child)
            elif isinstance(sub_node, Terminal):
                children.append(DerivationTree(sub_node))
            elif isinstance(sub_node, (Alternative, Concatenation)):
                # Recurse into nested structures
                child = generate_tree_with_random_depth(
                    grammar, max_depth, current_depth + 1, NonTerminal(sub_node)
                )
                children.append(child)
            elif isinstance(sub_node, Repetition):
                # Generate a random number of repetitions
                repetitions = random.randint(
                    sub_node.min, min(sub_node.max, 3)
                )  # Limit repetitions for diversity
                for _ in range(repetitions):
                    rep_child = generate_tree_with_random_depth(
                        grammar, max_depth, current_depth + 1, sub_node.node
                    )
                    children.append(rep_child)
    elif isinstance(selected_node, NonTerminal):
        child = generate_tree_with_random_depth(
            grammar, max_depth, current_depth + 1, selected_node
        )
        children.append(child)
    elif isinstance(selected_node, Terminal):
        children.append(DerivationTree(selected_node))
    elif isinstance(selected_node, Repetition):
        # Handle repetitions
        repetitions = random.randint(selected_node.min, min(selected_node.max, 3))
        for _ in range(repetitions):
            rep_child = generate_tree_with_random_depth(
                grammar, max_depth, current_depth + 1, selected_node.node
            )
            children.append(rep_child)
    else:
        # If the node type is unhandled, return an empty tree
        return DerivationTree(Terminal(""))

    return DerivationTree(symbol, children)


def extract_terminals(node: Node) -> List[str]:
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
            terminals.extend(extract_terminals(sub_node))
    elif isinstance(node, Concatenation):
        for sub_node in node.nodes:
            terminals.extend(extract_terminals(sub_node))
    elif isinstance(node, Repetition):
        terminals.extend(extract_terminals(node.node))
    return terminals


if __name__ == "__main__":
    from fandango.language.parse import parse_file

    # Parse grammar from src/evaluation/csv/csv.fan
    grammar, constraints, _ = parse_file("../../evaluation/csv/csv.fan")

    # Generate an initial population of 10 derivation trees
    population = generate_initial_population(grammar, 500)

    for tree in population:
        print(tree)
