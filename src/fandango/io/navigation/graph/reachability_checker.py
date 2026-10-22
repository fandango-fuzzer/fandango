from collections.abc import Sequence
from typing import NamedTuple, Optional

from fandango.io.navigation.graph.visitor.continuing_nodevisitor import (
    ContinuingNodeVisitor,
)
from fandango.io.navigation.step import Step
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree


class KPathMatcher:
    """Tells how many leading symbols of a k-path a sequence of symbols ends with, one symbol at a time."""

    def __init__(self, k_path: Sequence[Symbol]):
        self._k_path = list(k_path)
        # Per matched length, the next shorter length that the matched symbols also end with.
        self._fallbacks = [0] * len(self._k_path)
        matched = 0
        for i in range(1, len(self._k_path)):
            while matched > 0 and self._k_path[i] != self._k_path[matched]:
                matched = self._fallbacks[matched - 1]
            if self._k_path[i] == self._k_path[matched]:
                matched += 1
            self._fallbacks[i] = matched

    def matched_after(self, matched: int, symbol: Symbol) -> int:
        """Returns the matched length after symbol is appended to a sequence with the given matched length."""
        if matched == len(self._k_path):
            matched = self._fallbacks[matched - 1]
        while matched > 0 and self._k_path[matched] != symbol:
            matched = self._fallbacks[matched - 1]
        if self._k_path[matched] == symbol:
            matched += 1
        return matched

    def matched_lengths(self, symbols: Sequence[Symbol]) -> list[int]:
        """Returns the matched length after each prefix of the symbols, starting with the empty one."""
        if not self._k_path:
            return [0] * (len(symbols) + 1)
        lengths = [0]
        for symbol in symbols:
            lengths.append(self.matched_after(lengths[-1], symbol))
        return lengths


class ReachabilityResult(NamedTuple):
    path_reachable: bool
    completable_by_extension: bool


class ExtensionAnalyzer(ContinuingNodeVisitor):
    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        self.open_path: tuple[Symbol, ...] = tuple()
        self.extension_points: list[tuple[tuple[Symbol, ...], Symbol]] = []
        self._captured = False

    def analyze(self, tree: Optional[DerivationTree]) -> None:
        self.open_path = tuple()
        self.extension_points = []
        self._captured = False
        self.find(tree)

    def _current_open_path(self) -> tuple[Symbol, ...]:
        return tuple(
            symbol
            for symbol, is_exploring in self.current_path
            if not is_exploring and not Step.is_control_flow(symbol)
        )

    def _capture_open_path(self, open_path: tuple[Symbol, ...]) -> None:
        if self._captured:
            return
        self._captured = True
        self.open_path = open_path

    def onNonTerminalNodeVisit(
        self, node: NonTerminalNode, is_exploring: bool
    ) -> tuple[bool, bool]:
        if not is_exploring:
            return True, True
        open_path = self._current_open_path()
        self._capture_open_path(open_path)
        self.extension_points.append((open_path, node.symbol))
        return True, False

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool) -> bool:
        if is_exploring:
            self._capture_open_path(self._current_open_path())
        return True

    def __repr__(self) -> str:
        return f"ExtensionAnalyzer(open_path={self.open_path!r}, extension_points={self.extension_points!r})"


class ReachabilityChecker(ContinuingNodeVisitor):
    """
    For a given grammar and DerivationTree, this class
    finds possible upcoming message types, the nonterminals that generate them and the paths where the messages
    can be added to the DerivationTree.
    """

    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        self.seen_symbols: set[Symbol] = set()
        self.path_reached = False
        self.k_path_to_reach: KPath = tuple()
        self._matcher = KPathMatcher(())

    def find_reachability(
        self,
        *,
        k_path_to_reach: KPath,
        tree: Optional[DerivationTree] = None,
    ) -> ReachabilityResult:
        if not k_path_to_reach:
            return ReachabilityResult(False, False)
        self.path_reached = False
        self.k_path_to_reach = k_path_to_reach
        self._matcher = KPathMatcher(k_path_to_reach)
        self.seen_symbols.clear()
        super().find(tree)
        completable = self._completable_by_extension(tree)
        return ReachabilityResult(self.path_reached, completable)

    def _completable_by_extension(self, tree: Optional[DerivationTree]) -> bool:
        if tree is None:
            return False
        continuation = ExtensionAnalyzer(self.grammar)
        continuation.analyze(tree)
        if not continuation.open_path:
            return False
        k_path = tuple(self.k_path_to_reach)
        # The whole k-path is already realized on the rightmost open path.
        if self._matcher.matched_lengths(continuation.open_path)[-1] == len(k_path):
            return True
        # A still-open node on the rightmost path already realizes a non-empty
        # prefix of the k-path and can produce the next k-path symbol as a child
        # by extension. So we need to check if any open nonterminal along that
        # path can produce the next k-path symbol.
        for parent_path, child in continuation.extension_points:
            if not isinstance(child, NonTerminal):
                continue
            matched_by_prefix = self._matcher.matched_lengths(parent_path)
            for j in range(len(parent_path), 0, -1):
                match_len = matched_by_prefix[j]
                if not 0 < match_len < len(k_path):
                    continue
                if child != k_path[match_len]:
                    continue
                if self.test_reachability_from_node(
                    NonTerminalNode(child, []), k_path[match_len:]
                ):
                    return True
        return False

    def test_reachability_from_node(
        self, node: NonTerminalNode, k_path_to_reach: KPath
    ) -> bool:
        current_nodes: list[Node] = [node]
        chain_found = True
        for symbol in k_path_to_reach:
            current_nodes = list(
                filter(
                    lambda n: symbol == n.to_symbol(),
                    current_nodes,
                )
            )
            if not current_nodes:
                chain_found = False
                break
            current = current_nodes[0]
            current_nodes = list(current.descendents(self.grammar, True))
        return chain_found

    def onNonTerminalNodeVisit(
        self, node: NonTerminalNode, is_exploring: bool
    ) -> tuple[bool, bool]:
        if not is_exploring:
            return True, True
        first = self.k_path_to_reach[0]
        if node.symbol in self.seen_symbols:
            return True, False
        self.seen_symbols.add(node.symbol)
        if first == node.symbol:
            if self.test_reachability_from_node(node, self.k_path_to_reach):
                self.path_reached = True
            return False, False

        current_path = tuple(map(lambda x: x[0], self.current_path_collapsed))
        matched = self._matcher.matched_lengths(current_path)[-1]
        if matched == 0:
            return True, True
        if self.test_reachability_from_node(node, self.k_path_to_reach[matched - 1 :]):
            self.path_reached = True
        return False, False

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool) -> bool:
        if is_exploring:
            self.seen_symbols.add(node.symbol)
        return True

    def __repr__(self) -> str:
        return (
            f"ReachabilityChecker(k_path_to_reach={self.k_path_to_reach!r}, path_reached={self.path_reached!r}, "
            f"seen_symbols={self.seen_symbols!r})"
        )
