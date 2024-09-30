# initialization.py

import random
from typing import List, Set, Tuple

from fandango.language.grammar import Grammar, DerivationTree, NonTerminal, Terminal, Node, Repetition, Concatenation, \
    Alternative, Star, Plus, Option
from fandango.language.parse import parse_file


def generate_k_paths(
        grammar: Grammar,
        start_symbol: str = "<start>",
        k: int = 2
) -> Set[Tuple[Node, ...]]:
    """
    Generate all unique k-paths in the grammar starting from the start symbol.

    :param grammar: The grammar used to generate k-paths.
    :param start_symbol: The starting non-terminal symbol in the grammar.
    :param k: The length of paths to generate.
    :return: A set of k-paths, each represented as a tuple of Nodes.
    """
    paths = set()

    def dfs(node: Node, current_path: List[Node]):
        if len(current_path) == k:
            paths.add(tuple(current_path))
            return
        if isinstance(node, NonTerminal):
            if node.symbol not in grammar.rules:
                return
            expansions = grammar.rules[node.symbol]
            if isinstance(expansions, Alternative):
                alternatives = expansions.alternatives
            else:
                alternatives = [expansions]
            for expansion in alternatives:
                dfs(expansion, current_path + [expansion])
        elif isinstance(node, (Concatenation, Repetition, Star, Plus, Option)):
            for child in node.nodes:
                dfs(child, current_path + [child])
        elif isinstance(node, Terminal):
            paths.add(tuple(current_path + [node]))

    dfs(NonTerminal(start_symbol), [])
    return paths


def generate_k_path_population(
        grammar: Grammar,
        population_size: int,
        start_symbol: str = "<start>",
        k: int = 2,
        max_depth: int = 10
) -> List[DerivationTree]:
    """
    Create an initial population of derivation trees using the k-path algorithm.

    :param grammar: The grammar used to generate derivation trees.
    :param population_size: The desired number of individuals in the population.
    :param start_symbol: The starting non-terminal symbol in the grammar.
    :param k: The length of paths to cover in the grammar.
    :param max_depth: The maximum depth to which the derivation tree can be expanded.
    :return: A list of derivation trees covering as many unique k-paths as possible.
    """
    forest = []
    P = list(generate_k_paths(grammar, start_symbol, k))
    random.shuffle(P)
    P = set(P)  # Convert back to set for efficient removal
    paths_used = set()

    while P and len(forest) < population_size:
        p = P.pop()
        paths_used.add(p)
        r = DerivationTree(NonTerminal(start_symbol))
        Q = [(r, 0)]  # Queue of (node, depth)
        while Q:
            current_node, depth = Q.pop(0)
            if depth > max_depth:
                continue
            # Get the next uncovered node in p
            n = None
            for node in p:
                if node not in paths_used:
                    n = node
                    break
            if n is None:
                n = "X"
            # Get possible expansions for current_node
            if isinstance(current_node.symbol, NonTerminal):
                symbol = current_node.symbol.symbol
                if symbol not in grammar.rules:
                    continue
                expansions = grammar.rules[symbol]
                if isinstance(expansions, Alternative):
                    alternatives = expansions.alternatives
                else:
                    alternatives = [expansions]
                # Select an expansion
                if n != "X":
                    # Choose expansion closest to n
                    m = min(
                        alternatives,
                        key=lambda alt: 0 if alt == n else 1
                    )
                else:
                    # Choose expansion with fewest k-paths used
                    m = min(
                        alternatives,
                        key=lambda alt: len(generate_k_paths_from_node(alt, grammar, k) & paths_used)
                    )
                # Fill current_node with m
                children = expand_node(m, grammar)
                current_node.children = children
                for child in children:
                    child.parent = current_node
                # Remove covered k-paths
                new_paths = generate_k_paths_from_node(m, grammar, k)
                P -= new_paths
                paths_used.update(new_paths)
                # Add child slots to Q
                for child in children:
                    Q.append((child, depth + 1))
        forest.append(r)
    return forest


def generate_k_paths_from_node(node: Node, grammar: Grammar, k: int) -> Set[Tuple[Node, ...]]:
    """
    Generate k-paths starting from a specific node.

    :param node: The starting node.
    :param grammar: The grammar used for expansion.
    :param k: The length of paths to generate.
    :return: A set of k-paths.
    """
    paths = set()

    def dfs(current_node: Node, current_path: List[Node]):
        if len(current_path) == k:
            paths.add(tuple(current_path))
            return
        if isinstance(current_node, NonTerminal):
            symbol = current_node.symbol
            if symbol not in grammar.rules:
                return
            expansions = grammar.rules[symbol]
            if isinstance(expansions, Alternative):
                alternatives = expansions.alternatives
            else:
                alternatives = [expansions]
            for expansion in alternatives:
                dfs(expansion, current_path + [expansion])
        elif isinstance(current_node, (Concatenation, Repetition, Star, Plus, Option)):
            for child in current_node.nodes:
                dfs(child, current_path + [child])
        elif isinstance(current_node, Terminal):
            paths.add(tuple(current_path + [current_node]))

    dfs(node, [])
    return paths


def expand_node(node: Node, grammar: Grammar) -> List[DerivationTree]:
    """
    Expand a node into a list of derivation tree nodes.

    :param node: The node to expand.
    :param grammar: The grammar used for expansion.
    :return: A list of DerivationTree nodes.
    """
    if isinstance(node, Terminal):
        return [DerivationTree(node)]
    elif isinstance(node, NonTerminal):
        symbol = node.symbol
        if symbol not in grammar.rules:
            return []
        expansions = grammar.rules[symbol]
        if isinstance(expansions, Alternative):
            expansion = random.choice(expansions.alternatives)
        else:
            expansion = expansions
        return expand_node(expansion, grammar)
    elif isinstance(node, Concatenation):
        children = []
        for child in node.nodes:
            children.extend(expand_node(child, grammar))
        return children
    elif isinstance(node, Repetition):
        repetitions = random.randint(node.min, node.max)
        children = []
        for _ in range(repetitions):
            children.extend(expand_node(node.node, grammar))
        return children
    else:
        return []


if __name__ == "__main__":
    grammar, constraints = parse_file("../../evaluation/csv/csv.fan")

    population = generate_k_path_population(grammar, 10, k=10)

    for individual in population:
        print(individual)
        print((len(population)))
