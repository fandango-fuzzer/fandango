from typing import NamedTuple, Optional

from fandango.io.navigation.visitor.continuing_nodevisitor import ContinuingNodeVisitor
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import Symbol, NonTerminal
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
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
        self.next_children: set[Symbol] = set()
        self._captured = False

    def analyze(self, tree: Optional[DerivationTree]) -> None:
        self.open_path = tuple()
        self.next_children = set()
        self._captured = False
        self.find(tree)

    def _capture_open_path(self) -> None:
        if self._captured:
            return
        self._captured = True
        self.open_path = tuple(
            symbol
            for symbol, is_exploring in self.current_path
            if not is_exploring and not _is_controlflow_symbol(symbol)
        )

    def onNonTerminalNodeVisit(
        self, node: NonTerminalNode, is_exploring: bool
    ) -> tuple[bool, bool]:
        if not is_exploring:
            return True, True
        self._capture_open_path()
        self.next_children.add(node.symbol)
        return True, False

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool) -> bool:
        if is_exploring:
            self._capture_open_path()
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
        open_path = continuation.open_path
        if not open_path:
            return False
        k_path = tuple(self.k_path_to_reach)
        match = continuation.find_longest_suffix(open_path, k_path)
        if len(match) == 0:
            return False
        if len(match) == len(k_path):
            return True
        next_symbol = k_path[len(match)]
        if next_symbol not in continuation.next_children:
            return False
        if not isinstance(next_symbol, NonTerminal):
            return False
        return self.test_reachability_from_node(
            NonTerminalNode(next_symbol, []), k_path[len(match) :]
        )

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
