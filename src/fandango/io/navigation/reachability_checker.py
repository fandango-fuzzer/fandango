from typing import NamedTuple, Optional

from fandango.io.navigation.visitor.continuing_nodevisitor import ContinuingNodeVisitor
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree


class ReachabilityResult(NamedTuple):
    path_reachable: bool
    completable_by_extension: bool


def _is_controlflow_symbol(symbol: Symbol) -> bool:
    return isinstance(symbol, NonTerminal) and symbol.name().startswith("<__")


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
            if not is_exploring and not _is_controlflow_symbol(symbol)
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
        if len(self.find_longest_suffix(continuation.open_path, k_path)) == len(k_path):
            return True
        # A still-open node on the rightmost path already realizes a non-empty
        # prefix of the k-path and can produce the next k-path symbol as a child
        # by extension. So we need to check if any open nonterminal along that
        # path can produce the next k-path symbol.
        for parent_path, child in continuation.extension_points:
            if not isinstance(child, NonTerminal):
                continue
            for j in range(len(parent_path), 0, -1):
                match_len = len(self.find_longest_suffix(parent_path[:j], k_path))
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
        match = self.find_longest_suffix(current_path, tuple(self.k_path_to_reach))
        if len(match) == 0:
            return True, True
        if self.test_reachability_from_node(
            node, self.k_path_to_reach[len(match) - 1 :]
        ):
            self.path_reached = True
        return False, False

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool) -> bool:
        if is_exploring:
            self.seen_symbols.add(node.symbol)
        return True

    def find_longest_suffix(
        self, path: tuple[Symbol, ...], suffix_path: tuple[Symbol, ...]
    ) -> tuple[Symbol, ...]:
        max_overlap = 0
        search_len = len(suffix_path)
        chain_len = len(path)
        for i in range(1, min(search_len, chain_len) + 1):
            if path[-i:] == suffix_path[:i]:
                max_overlap = i
        return suffix_path[:max_overlap]
