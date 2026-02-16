"""Suite-level fitness functions for test suite evaluation."""

from beartype.typing import Dict, Any
from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.chromosomes.suite import Suite
from fandango.evolution.fitness.base import SuiteFitnessFunction
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal


class SymbolCoverageFitnessFunction(SuiteFitnessFunction):
    """
    Measures the fraction of grammar NonTerminal symbols covered by a suite.

    This fitness function evaluates how many distinct non-terminal symbols from
    the grammar are exercised by the derivation trees in a test suite.

    Formula: fitness = |covered symbols| / |total symbols reachable from start_symbol|

    The fitness value ranges from 0.0 (no symbols covered) to 1.0 (all symbols covered).
    This is a maximizing fitness function.

    Note: This fitness function uses hash-based caching. It assumes Suite objects
    are immutable after fitness evaluation. If you mutate a suite after evaluation,
    call clear_cache() to invalidate cached results.
    """

    def __init__(
        self, grammar: Grammar, start_symbol: NonTerminal = NonTerminal("<start>")
    ):
        """
        Initialize the SymbolCoverageFitnessFunction.

        Args:
            grammar: The grammar defining the universe of symbols
            start_symbol: The start symbol for coverage computation (default: <start>)
        """
        self._grammar = grammar
        self._start_symbol = start_symbol
        self._all_symbols = self._compute_reachable_symbols(grammar, start_symbol)
        self._cache: Dict[Any, float] = {}

    @staticmethod
    def _compute_reachable_symbols(
        grammar: Grammar, start_symbol: NonTerminal
    ) -> set[NonTerminal]:
        """
        Compute all non-terminal symbols reachable from start_symbol.

        Args:
            grammar: The grammar to analyze
            start_symbol: The starting non-terminal

        Returns:
            Set of all non-terminal symbols reachable from start_symbol
        """
        if start_symbol not in grammar.rules:
            return set()

        from fandango.language.grammar.nodes.non_terminal import NonTerminalNode

        reachable: set[NonTerminal] = set()
        work_list = [start_symbol]

        while work_list:
            current = work_list.pop(0)
            if current in reachable:
                continue

            reachable.add(current)

            # Get the rule for this non-terminal
            if current not in grammar.rules:
                continue

            rule_node = grammar.rules[current]

            # Find all non-terminal descendants in this rule
            descendants = rule_node.descendents(grammar, filter_controlflow=True)
            for desc in descendants:
                if isinstance(desc, NonTerminalNode):
                    nt_symbol = desc.to_symbol()
                    if (
                        isinstance(nt_symbol, NonTerminal)
                        and nt_symbol not in reachable
                    ):
                        work_list.append(nt_symbol)

        return reachable

    def fitness(self, chromosome: Chromosome) -> float:
        """
        Evaluate fitness of a chromosome.

        Args:
            chromosome: A Suite chromosome to evaluate

        Returns:
            Fitness value in [0.0, 1.0] representing the fraction of symbols covered

        Raises:
            TypeError: If chromosome is not a Suite
        """
        if not isinstance(chromosome, Suite):
            raise TypeError(
                f"SymbolCoverageFitnessFunction requires a Suite, got {type(chromosome).__name__}"
            )

        # Check cache first
        suite_hash = hash(chromosome)
        if suite_hash in self._cache:
            return self._cache[suite_hash]

        # Handle edge cases
        if len(self._all_symbols) == 0:
            # Empty grammar - consider it fully covered
            self._cache[suite_hash] = 1.0
            return 1.0

        if len(chromosome) == 0:
            # Empty suite - no coverage
            self._cache[suite_hash] = 0.0
            return 0.0

        # Collect covered symbols from all trees in the suite
        covered_symbols: set[NonTerminal] = set()
        for individual in chromosome:
            tree = individual.tree
            tree_symbols = tree.get_non_terminal_symbols(exclude_read_only=False)

            # Only count symbols that exist in the grammar
            covered_symbols.update(tree_symbols.intersection(self._all_symbols))

            # If we've covered all symbols, return 1.0
            if len(covered_symbols) == len(self._all_symbols):
                self._cache[suite_hash] = 1.0
                return 1.0

        # Compute coverage ratio
        fitness_value = len(covered_symbols) / len(self._all_symbols)
        self._cache[suite_hash] = fitness_value
        return fitness_value

    def is_covered(self, suite: Suite) -> bool:
        """
        Check if the suite satisfies coverage goals.

        Args:
            suite: The suite to check

        Returns:
            True if all symbols are covered (fitness >= 1.0), False otherwise
        """
        return self.fitness(suite) >= 1.0

    def is_maximising(self) -> bool:
        """
        Whether this fitness function is maximizing (True) or minimizing (False).

        Returns:
            True (this fitness function is maximizing)
        """
        return True

    @property
    def cache(self) -> Dict[Any, Any]:
        """
        Fitness cache for memoization.

        Returns:
            Dictionary mapping suite hashes to fitness values
        """
        return self._cache

    def clear_cache(self) -> None:
        """
        Clear the fitness cache.

        Use this method if you mutate a Suite after it has been evaluated,
        to ensure fresh fitness computation on the next call.
        """
        self._cache.clear()


class PathCoverageFitnessFunction(SuiteFitnessFunction):
    """
    Measures the fraction of grammar 2-paths (edges) exercised by a suite.

    This fitness function evaluates how many distinct 2-paths (edges in the
    grammar graph) are covered by the derivation trees in a test suite.

    Formula: fitness = |covered 2-paths| / |total 2-paths in grammar|

    The fitness value ranges from 0.0 (no paths covered) to 1.0 (all paths covered).
    This is a maximizing fitness function.

    Note: This fitness function uses hash-based caching. It assumes Suite objects
    are immutable after fitness evaluation. If you mutate a suite after evaluation,
    call clear_cache() to invalidate cached results.
    """

    def __init__(
        self, grammar: Grammar, start_symbol: NonTerminal = NonTerminal("<start>")
    ):
        """
        Initialize the PathCoverageFitnessFunction.

        Args:
            grammar: The grammar defining the universe of paths
            start_symbol: The start symbol for path generation (default: <start>)
        """
        self._grammar = grammar
        self._start_symbol = start_symbol
        # Generate all 2-paths from the grammar (cached at grammar level)
        # Handle case where start_symbol doesn't exist in grammar
        if start_symbol in grammar.rules:
            self._all_paths = grammar.generate_all_k_paths(
                k=2, non_terminal=start_symbol
            )
        else:
            self._all_paths = set()
        self._cache: Dict[Any, float] = {}

    def fitness(self, chromosome: Chromosome) -> float:
        """
        Evaluate fitness of a chromosome.

        Args:
            chromosome: A Suite chromosome to evaluate

        Returns:
            Fitness value in [0.0, 1.0] representing the fraction of 2-paths covered

        Raises:
            TypeError: If chromosome is not a Suite
        """
        if not isinstance(chromosome, Suite):
            raise TypeError(
                f"PathCoverageFitnessFunction requires a Suite, got {type(chromosome).__name__}"
            )

        # Check cache first
        suite_hash = hash(chromosome)
        if suite_hash in self._cache:
            return self._cache[suite_hash]

        # Handle edge cases
        if len(self._all_paths) == 0:
            # No 2-paths in grammar - consider it fully covered
            self._cache[suite_hash] = 1.0
            return 1.0

        if len(chromosome) == 0:
            # Empty suite - no coverage
            self._cache[suite_hash] = 0.0
            return 0.0

        # Collect covered paths from all trees in the suite
        covered_paths = set()
        for individual in chromosome:
            tree = individual.tree
            tree_paths = self._grammar._extract_k_paths_from_tree(tree, k=2)
            # Only count paths that exist in the grammar
            covered_paths.update(tree_paths.intersection(self._all_paths))

            # Early exit optimization: if we've covered all paths, return 1.0
            if len(covered_paths) == len(self._all_paths):
                self._cache[suite_hash] = 1.0
                return 1.0

        # Compute coverage ratio
        fitness_value = len(covered_paths) / len(self._all_paths)
        self._cache[suite_hash] = fitness_value
        return fitness_value

    def is_covered(self, suite: Suite) -> bool:
        """
        Check if the suite satisfies coverage goals.

        Args:
            suite: The suite to check

        Returns:
            True if all 2-paths are covered (fitness >= 1.0), False otherwise
        """
        return self.fitness(suite) >= 1.0

    def is_maximising(self) -> bool:
        """
        Whether this fitness function is maximizing (True) or minimizing (False).

        Returns:
            True (this fitness function is maximizing)
        """
        return True

    @property
    def cache(self) -> Dict[Any, Any]:
        """
        Fitness cache for memoization.

        Returns:
            Dictionary mapping suite hashes to fitness values
        """
        return self._cache

    def clear_cache(self) -> None:
        """
        Clear the fitness cache.

        Use this method if you mutate a Suite after it has been evaluated,
        to ensure fresh fitness computation on the next call.
        """
        self._cache.clear()
