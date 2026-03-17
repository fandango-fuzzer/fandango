"""Suite-level fitness functions for test suite evaluation."""

from beartype.typing import Dict, Any, List
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
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
        trees = [
            tree
            for individual in chromosome
            for tree in individual.to_derivation_trees()
        ]
        for tree in trees:
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


class KPathCoverageFitnessFunction(SuiteFitnessFunction):
    """
    Measures the fraction of grammar k-paths exercised by a suite.

    This fitness function evaluates how many distinct k-paths (sequences of k
    symbols in the grammar graph) are covered by the derivation trees in a test
    suite.

    Formula: fitness = |covered k-paths| / |total k-paths in grammar|

    The fitness value ranges from 0.0 (no paths covered) to 1.0 (all paths covered).
    This is a maximizing fitness function.

    Note: This fitness function uses hash-based caching. It assumes Suite objects
    are immutable after fitness evaluation. If you mutate a suite after evaluation,
    call clear_cache() to invalidate cached results.
    """

    def __init__(
        self,
        grammar: Grammar,
        k: int = 2,
        start_symbol: NonTerminal = NonTerminal("<start>"),
    ):
        """
        Initialize the KPathCoverageFitnessFunction.

        Args:
            grammar: The grammar defining the universe of paths
            k: The path length (k >= 1); k=2 gives edges, k=1 gives individual nodes
            start_symbol: The start symbol for path generation (default: <start>)

        Raises:
            ValueError: If k < 1
        """
        if k < 1:
            raise ValueError(f"k must be >= 1, got {k}")
        self._grammar = grammar
        self._k = k
        self._start_symbol = start_symbol
        # Generate all k-paths from the grammar
        # Handle case where start_symbol doesn't exist in grammar
        if start_symbol in grammar.rules:
            self._all_paths = grammar.generate_all_k_paths(
                k=k, non_terminal=start_symbol
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
            Fitness value in [0.0, 1.0] representing the fraction of k-paths covered

        Raises:
            TypeError: If chromosome is not a Suite
        """
        if not isinstance(chromosome, Suite):
            raise TypeError(
                f"KPathCoverageFitnessFunction requires a Suite, got {type(chromosome).__name__}"
            )

        # Check cache first
        suite_hash = hash(chromosome)
        if suite_hash in self._cache:
            return self._cache[suite_hash]

        # Handle edge cases
        if len(self._all_paths) == 0:
            # No k-paths in grammar - consider it fully covered
            self._cache[suite_hash] = 1.0
            return 1.0

        if len(chromosome) == 0:
            # Empty suite - no coverage
            self._cache[suite_hash] = 0.0
            return 0.0

        # Collect covered paths from all trees in the suite
        covered_paths = set()
        trees = [
            tree
            for individual in chromosome
            for tree in individual.to_derivation_trees()
        ]
        for tree in trees:
            tree_paths = self._grammar._extract_k_paths_from_tree(tree, k=self._k)
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
            True if all k-paths are covered (fitness >= 1.0), False otherwise
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


class GraphCoverageFitnessFunction(SuiteFitnessFunction):
    """
    Measures graph coverage as a normalized weighted sum of k-path coverages.

    Formula: fitness = (∑_{k=1}^{max_k} (1/k) * cov(k)) / H_{max_k}

    where cov(k) = KPathCoverageFitnessFunction(k).fitness(suite)
    and H_{max_k} = ∑_{k=1}^{max_k} 1/k (harmonic normalization).

    The fitness value ranges from 0.0 to 1.0. This is a maximizing fitness function.
    """

    def __init__(
        self,
        grammar: Grammar,
        max_k: int = 3,
        start_symbol: NonTerminal = NonTerminal("<start>"),
    ):
        """
        Args:
            grammar: The grammar defining the universe of paths
            max_k: Upper bound for k (inclusive); computes coverage for k ∈ [1, max_k]
            start_symbol: The start symbol for path generation (default: <start>)

        Raises:
            ValueError: If max_k < 1
        """
        if max_k < 1:
            raise ValueError(f"max_k must be >= 1, got {max_k}")
        self._grammar = grammar
        self._max_k = max_k
        self._start_symbol = start_symbol

        # Pre-instantiate one KPathCoverageFitnessFunction per k
        self._k_fns: list[tuple[int, KPathCoverageFitnessFunction]] = [
            (k, KPathCoverageFitnessFunction(grammar, k=k, start_symbol=start_symbol))
            for k in range(1, max_k + 1)
        ]

        # Pre-compute harmonic normalization constant H_{max_k}
        self._h_max_k: float = sum(1.0 / k for k in range(1, max_k + 1))

        self._cache: Dict[Any, float] = {}

    def fitness(self, chromosome: Chromosome) -> float:
        if not isinstance(chromosome, Suite):
            raise TypeError(
                f"GraphCoverageFitnessFunction requires a Suite, got {type(chromosome).__name__}"
            )

        suite_hash = hash(chromosome)
        if suite_hash in self._cache:
            return self._cache[suite_hash]

        weighted_sum = sum(
            (1.0 / k) * k_fn.fitness(chromosome) for k, k_fn in self._k_fns
        )

        fitness_value = weighted_sum / self._h_max_k
        self._cache[suite_hash] = fitness_value
        return fitness_value

    def is_covered(self, suite: Suite) -> bool:
        return self.fitness(suite) >= 1.0

    def is_maximising(self) -> bool:
        return True

    @property
    def cache(self) -> Dict[Any, Any]:
        return self._cache

    def clear_cache(self) -> None:
        self._cache.clear()


class SoftConstraintsFitnessFunction(SuiteFitnessFunction):
    """
    Measures the average soft-constraint satisfaction across all individuals in a suite.

    For each individual, evaluates each SoftValue, normalizes via TDigest, and
    accounts for optimization direction. Returns the mean score across all individuals
    and all soft constraints. Returns 1.0 if there are no soft constraints.

    No caching — TDigest is adaptive/stateful; scores change as the distribution evolves.
    """

    def __init__(self, constraints: List[SoftValue]) -> None:
        self._constraints = list(constraints)

    def fitness(self, chromosome: Chromosome) -> float:
        if not isinstance(chromosome, Suite):
            raise TypeError(
                f"SoftConstraintsFitnessFunction requires a Suite, got {type(chromosome).__name__}"
            )

        if not self._constraints:
            return 1.0

        if len(chromosome) == 0:
            return 0.0

        individual_scores = []
        for individual in chromosome:
            constraint_scores = []
            for soft in self._constraints:
                result = soft.fitness(individual.tree)
                raw = result.fitness()
                soft.tdigest.update(raw)
                normalized = soft.tdigest.score(raw)
                score = (
                    normalized if soft.optimization_goal == "max" else 1 - normalized
                )
                constraint_scores.append(score)
            individual_scores.append(sum(constraint_scores) / len(constraint_scores))

        return sum(individual_scores) / len(individual_scores)

    def is_covered(self, suite: Suite) -> bool:
        return self.fitness(suite) >= 1.0

    def is_maximising(self) -> bool:
        return True

    @property
    def cache(self) -> Dict[Any, Any]:
        return {}

    def clear_cache(self) -> None:
        pass


def PathCoverageFitnessFunction(
    grammar: Grammar,
    start_symbol: NonTerminal = NonTerminal("<start>"),
) -> KPathCoverageFitnessFunction:
    """Backward-compatible alias for KPathCoverageFitnessFunction(k=2)."""
    return KPathCoverageFitnessFunction(grammar, k=2, start_symbol=start_symbol)


class ConstraintsFitnessFunction(SuiteFitnessFunction):
    """
    Measures the fraction of suite individuals satisfying all hard constraints.

    Formula: fitness = |satisfying individuals| / |suite size|

    Returns 1.0 when there are no constraints (vacuously satisfied).
    The fitness value ranges from 0.0 to 1.0. This is a maximizing fitness function.
    """

    def __init__(self, constraints: List[Constraint]) -> None:
        self._constraints = list(constraints)
        self._cache: Dict[Any, float] = {}

    def fitness(self, chromosome: Chromosome) -> float:
        if not isinstance(chromosome, Suite):
            raise TypeError(
                f"ConstraintsFitnessFunction requires a Suite, got {type(chromosome).__name__}"
            )

        if not self._constraints:
            return 1.0

        suite_hash = hash(chromosome)
        if suite_hash in self._cache:
            return self._cache[suite_hash]

        if len(chromosome) == 0:
            self._cache[suite_hash] = 0.0
            return 0.0

        satisfied = sum(
            1
            for ind in chromosome
            if all(c.fitness(ind.tree).fitness() >= 1.0 for c in self._constraints)
        )
        value = satisfied / len(chromosome)
        self._cache[suite_hash] = value
        return value

    def is_covered(self, suite: Suite) -> bool:
        return self.fitness(suite) >= 1.0

    def is_maximising(self) -> bool:
        return True

    @property
    def cache(self) -> Dict[Any, Any]:
        return self._cache

    def clear_cache(self) -> None:
        self._cache.clear()
