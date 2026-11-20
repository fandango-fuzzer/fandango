"""The k-paths of a grammar and of the derivation trees it derives, with the caches that keep them fast."""

from typing import NamedTuple, Optional

from cachetools import LRUCache

from fandango.errors import FandangoValueError
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.node_visitors.disambiguator import Disambiguator
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol, Terminal
from fandango.language.tree import DerivationTree, index_by_reference
from fandango.language.tree_value import TreeValueType
from fandango.utils import cache_size

KPath = tuple[Symbol, ...]

# k, non-terminal, overlap_to_root, coverage goal and input parties: everything the k-paths of a grammar depend on
_KPathsKey = tuple[int, NonTerminal, bool, CoverageGoal, frozenset[str]]


class _TreeKPaths(NamedTuple):
    """K-paths of a tree node."""

    starting_here: set[KPath]
    """K-paths starting at the node."""
    at_or_below: set[KPath]
    """K-paths starting at the node or any node below it."""


class GrammarKPaths:
    """Computes the k-paths of a grammar and of its derivation trees, caching them per grammar."""

    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        # A plain dict: the keys are bounded by the grammar, and a hit costs a single lookup
        self._k_path_cache: dict[_KPathsKey, set[KPath]] = {}
        # Keys are the hashes of `_KPathsKey` objects
        self._tree_k_path_cache: LRUCache[int, _TreeKPaths] = LRUCache(
            maxsize=cache_size()
        )
        # The k-paths from <start> by each symbol they contain, with the k they reach up to
        self._k_paths_by_symbol: LRUCache[
            tuple[CoverageGoal, frozenset[str]], tuple[int, dict[Symbol, list[KPath]]]
        ] = LRUCache(maxsize=cache_size())
        # (non-terminal, word, is_bits) -> rule terminals matching the word. An LRU, as the words come from the trees
        self._rule_terminals_cache: LRUCache[
            tuple[NonTerminal, str | bytes | int, bool], frozenset[Terminal]
        ] = LRUCache(maxsize=cache_size())

    def generate_all(
        self,
        *,
        k: int,
        non_terminal: Optional[NonTerminal] = None,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        """
        Computes the *k*-paths for this grammar, constructively. See: doi.org/10.1109/ASE.2019.00027

        :param k: The length of the paths.
        :param non_terminal: The non-terminal from which to start generating paths.
        :param overlap_to_root: Whether to include paths that contain the starting symbol but are overlapping with symbols towards the root direction.
        :param coverage_goal: The coverage goal to consider when generating paths.
        :param input_parties: The parties whose messages count as inputs, under STATE_INPUTS and INPUTS.
        :return: All paths of length up to *k* within this grammar.
        """
        cache_key: _KPathsKey = (
            k,
            NonTerminal("<start>") if non_terminal is None else non_terminal,
            overlap_to_root,
            coverage_goal,
            frozenset(input_parties or ()),
        )
        k_paths = self._k_path_cache.get(cache_key)
        if k_paths is None:
            k_paths = self._k_path_cache[cache_key] = self._compute_k_paths(*cache_key)
        return k_paths

    def _compute_k_paths(
        self,
        k: int,
        non_terminal: NonTerminal,
        overlap_to_root: bool,
        coverage_goal: CoverageGoal,
        input_parties: frozenset[str],
    ) -> set[KPath]:
        initial: set[Node] = set()
        starter_node = NonTerminalNode(non_terminal, self._grammar.grammar_settings)

        initial_work: list[Node] = [starter_node]
        if coverage_goal == CoverageGoal.INPUTS:
            initial_work.append(starter_node)
            while initial_work:
                node = initial_work.pop(0)
                if node in initial:
                    continue
                initial.add(node)
                initial_work.extend(
                    node.descendents(self._grammar, filter_controlflow=True)
                )
            initial_work = [
                node
                for node in initial
                if isinstance(node, NonTerminalNode) and node.sender in input_parties
            ]
        initial.clear()
        while initial_work:
            node = initial_work.pop(0)
            if node in initial:
                continue
            initial.add(node)
            for descendent in node.descendents(self._grammar, filter_controlflow=True):
                if isinstance(descendent, NonTerminalNode):
                    if coverage_goal == CoverageGoal.STATE_INPUTS_OUTPUTS:
                        initial_work.append(descendent)
                    elif coverage_goal == CoverageGoal.STATE_INPUTS:
                        if (
                            descendent.sender is None
                            or descendent.sender in input_parties
                        ):
                            initial_work.append(descendent)
                    elif coverage_goal == CoverageGoal.INPUTS:
                        initial_work.append(descendent)
                    else:
                        raise ValueError(f"Unknown coverage goal: {coverage_goal}")
                else:
                    initial_work.append(descendent)

        work: list[set[tuple[Node, ...]]] = [set((x,) for x in initial)]

        for _ in range(len(work), k):
            next_work = set(work[-1])
            for base in work[-1]:
                for descendent in base[-1].descendents(
                    self._grammar, filter_controlflow=True
                ):
                    if isinstance(descendent, NonTerminalNode):
                        if coverage_goal == CoverageGoal.STATE_INPUTS:
                            if (
                                descendent.sender is not None
                                and descendent.sender not in input_parties
                            ):
                                continue
                    next_work.add(base + (descendent,))
            work.append(next_work)

        symbol_work = []
        for work_k in work:
            symbol_work_k: set[tuple[Symbol, ...]] = set()
            symbol_work.append(symbol_work_k)
            for path in work_k:
                symbol_work_k.add(tuple(node.to_symbol() for node in path))

        if overlap_to_root:
            index_key = (coverage_goal, input_parties)
            indexed = self._k_paths_by_symbol.get(index_key)
            if indexed is None or indexed[0] < k:
                k_paths_by_symbol: dict[Symbol, list[KPath]] = {}
                for k_path in self.generate_all(
                    k=k, coverage_goal=coverage_goal, input_parties=set(input_parties)
                ):
                    for symbol in set(k_path):
                        k_paths_by_symbol.setdefault(symbol, []).append(k_path)
                indexed = (k, k_paths_by_symbol)
                self._k_paths_by_symbol[index_key] = indexed
            for k_path in indexed[1].get(non_terminal, []):
                for idx in range(len(k_path) - 1, k):
                    symbol_work[idx].add(k_path)

        return symbol_work[k - 1]

    def compute_coverage(
        self, derivation_trees: list[DerivationTree], k: int
    ) -> tuple[float, int, int]:
        """
        Compute the coverage of k-paths in the grammar based on the given derivation trees.

        :param derivation_trees: A list of derivation trees (solutions produced by FANDANGO).
        :param k: The length of the paths (k).
        :return: A float between 0 and 1 representing the coverage.
        """

        # Compute all possible k-paths in the grammar
        all_k_paths = self.generate_all(k=k)

        disambiguator = Disambiguator(self._grammar, self._grammar.grammar_settings)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            for path in self._grammar.traverse_derivation(tree, disambiguator):
                # for length in range(1, k + 1):
                for window in range(len(path) - k + 1):
                    covered_k_paths.add(path[window : window + k])

        # Compute coverage
        if not all_k_paths:
            raise FandangoValueError("No k-paths found in the grammar")

        return (
            len(covered_k_paths) / len(all_k_paths),
            len(covered_k_paths),
            len(all_k_paths),
        )

    def extract_from_tree(
        self,
        tree: DerivationTree,
        k: int,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        """Returns the k-paths found in a derivation tree, starting at the tree or below it, and with
        `overlap_to_root` also the ones reaching up into its ancestors."""
        parties = frozenset(input_parties or set())
        outside_in_goal = coverage_goal != CoverageGoal.INPUTS
        # Messages do not nest, so the message enclosing the tree decides whether it counts.
        message = tree
        while message.sender is None:
            parent = message.parent
            # ... or case for unmounted trees
            if parent is None or index_by_reference(parent.children, message) is None:
                break
            message = parent
        in_goal = self._in_k_path_coverage_goal(
            message, outside_in_goal, coverage_goal, parties
        )

        k_paths: set[KPath] = set()
        if in_goal is None:
            return k_paths
        starting_here, at_or_below = self._k_paths_at_or_below(
            tree, in_goal, k, coverage_goal, parties, inside_message=False
        )
        k_paths |= at_or_below

        if overlap_to_root and in_goal:
            # Paths start up to k-1 levels above the tree, reached through child edges.
            prefix: KPath = tuple()
            node = tree
            for _ in range(k - 1):
                parent = node.parent
                # ... or case for unmounted trees
                if parent is None or index_by_reference(parent.children, node) is None:
                    break
                # Above the enclosing message, nodes are outside of any message.
                if node.sender is not None and not outside_in_goal:
                    break
                prefix = (parent.symbol,) + prefix
                k_paths |= {
                    prefix + path
                    for path in starting_here
                    if len(prefix) + len(path) <= k
                }
                node = parent
        return k_paths

    @staticmethod
    def _in_k_path_coverage_goal(
        node: DerivationTree,
        parent_in_goal: Optional[bool],
        coverage_goal: CoverageGoal,
        input_parties: frozenset[str],
    ) -> Optional[bool]:
        """
        Returns whether `node` counts for the coverage goal, given whether its parent does.
        True: the node counts. False: only nodes below it may count. None: nothing at or below it counts.
        """
        if parent_in_goal is None or node.sender is None:
            return parent_in_goal
        if coverage_goal == CoverageGoal.INPUTS:
            # Only the messages of input parties count, entirely.
            return True if parent_in_goal or node.sender in input_parties else None
        if (
            coverage_goal == CoverageGoal.STATE_INPUTS
            and node.sender not in input_parties
        ):
            return None
        return parent_in_goal

    def _k_paths_at_or_below(
        self,
        tree: DerivationTree,
        in_goal: bool,
        k: int,
        coverage_goal: CoverageGoal,
        input_parties: frozenset[str],
        inside_message: bool,
    ) -> _TreeKPaths:
        """Returns the k-paths starting at `tree` and the k-paths starting at or below `tree`."""
        k_paths_by_node: dict[int, _TreeKPaths] = {}
        # Post-order, like the recursion it replaces: a subtree is done and cached before its later siblings are
        # visited, so an equal subtree further on is a cache hit.
        # (node, in_goal, inside_message, children_done, cache_key): a node to visit, or, once children_done, a
        # non-terminal whose children are done; cache_key is None if its result is not cached.
        pending: list[tuple[DerivationTree, bool, bool, bool, Optional[int]]] = [
            (tree, in_goal, inside_message, False, None)
        ]
        while pending:
            node, node_in_goal, node_inside_message, children_done, cache_key = (
                pending.pop()
            )
            if children_done:
                k_paths = self._k_paths_at_non_terminal(
                    node, node_in_goal, k, k_paths_by_node
                )
                if cache_key is not None:
                    self._tree_k_path_cache[cache_key] = k_paths
                k_paths_by_node[id(node)] = k_paths
                continue
            if isinstance(node.symbol, Terminal):
                k_paths_by_node[id(node)] = self._k_paths_at_terminal(
                    node, node_in_goal
                )
                continue
            if node.sender is not None or not node_inside_message:
                cache_key = hash((node, k, node_in_goal, coverage_goal, input_parties))
                if cache_key in self._tree_k_path_cache:
                    k_paths_by_node[id(node)] = self._tree_k_path_cache[cache_key]
                    continue
            pending.append((node, node_in_goal, node_inside_message, True, cache_key))
            child_inside_message = node_inside_message or node.sender is not None
            # Reversed, so that the children are visited from left to right
            for child in reversed(node.children):
                child_in_goal = self._in_k_path_coverage_goal(
                    child, node_in_goal, coverage_goal, input_parties
                )
                if child_in_goal is not None:
                    pending.append(
                        (child, child_in_goal, child_inside_message, False, None)
                    )
        return k_paths_by_node[id(tree)]

    def _k_paths_at_terminal(self, tree: DerivationTree, in_goal: bool) -> _TreeKPaths:
        if not in_goal or tree.parent is None:
            return _TreeKPaths(set(), set())
        assert isinstance(tree.symbol, Terminal)
        assert isinstance(tree.parent.symbol, NonTerminal)
        matching_paths: set[KPath] = {
            (terminal,)
            for terminal in self._rule_terminals_matching(
                tree.parent.symbol, tree.symbol
            )
        }
        return _TreeKPaths(matching_paths, matching_paths)

    @staticmethod
    def _k_paths_at_non_terminal(
        tree: DerivationTree,
        in_goal: bool,
        k: int,
        k_paths_by_node: dict[int, _TreeKPaths],
    ) -> _TreeKPaths:
        symbol = tree.symbol
        assert isinstance(symbol, NonTerminal)
        starting_here: set[KPath] = {(symbol,)} if in_goal else set()
        at_or_below: set[KPath] = set()
        for child in tree.children:
            if id(child) not in k_paths_by_node:
                continue
            starting_at_child, at_or_below_child = k_paths_by_node.pop(id(child))
            if in_goal:
                for path in starting_at_child:
                    if len(path) < k:
                        starting_here.add((symbol,) + path)
            at_or_below |= at_or_below_child
        at_or_below |= starting_here
        return _TreeKPaths(starting_here, at_or_below)

    def _rule_terminals_matching(
        self, non_terminal: NonTerminal, terminal: Terminal
    ) -> frozenset[Terminal]:
        """Returns the terminals in the rule of `non_terminal` that accept the value of `terminal`."""
        value = terminal.value()
        word: str | bytes | int
        if value.is_type(TreeValueType.STRING):
            word = value.to_string()
        elif value.is_type(TreeValueType.BYTES):
            word = value.to_bytes()
        else:
            word = value.to_int()
        is_bits = value.is_type(TreeValueType.TRAILING_BITS_ONLY)
        # Keyed by the word, not the terminal: terminals compare equal whether or not they are regexes
        cache_key = (non_terminal, word, is_bits)
        if cache_key in self._rule_terminals_cache:
            return self._rule_terminals_cache[cache_key]
        rule_nodes = NonTerminalNode(
            non_terminal, self._grammar.grammar_settings
        ).descendents(self._grammar, filter_controlflow=True)
        matching = frozenset(
            rule_node.symbol
            for rule_node in rule_nodes
            if isinstance(rule_node, TerminalNode)
            and rule_node.symbol.is_type(TreeValueType.TRAILING_BITS_ONLY) == is_bits
            and rule_node.symbol.check(word)[0]
        )
        self._rule_terminals_cache[cache_key] = matching
        return matching
