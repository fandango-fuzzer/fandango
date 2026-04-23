from typing import Optional

from fandango.io.navigation.visitor.continuing_nodevisitor import ContinuingNodeVisitor
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.nodes.node import Node
from fandango.language.tree import DerivationTree
from fandango.language import Grammar, Symbol, NonTerminal, Terminal
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode


class ReachabilityChecker(ContinuingNodeVisitor):
    """
    For a given grammar and DerivationTree, this class
    finds possible upcoming message types, the nonterminals that generate them and the paths where the messages
    can be added to the DerivationTree.
    """

    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        self.seen_states: set[tuple[Symbol, ...]] = set()
        self.path_reached = False
        self.k_path_to_reach: KPath = tuple()

    def find_reachability(
        self,
        *,
        k_path_to_reach: KPath,
        tree: Optional[DerivationTree] = None,
    ) -> bool:
        if not k_path_to_reach:
            return False
        self.path_reached = False
        self.k_path_to_reach = k_path_to_reach
        self.seen_states.clear()
        super().find(tree)
        return self.path_reached

    def test_reachability_from_node(
        self, node: NonTerminalNode, k_path_to_reach: KPath
    ) -> bool:
        current_nodes: list[Node] = [node]
        for symbol in k_path_to_reach:
            matching_nodes = [
                current_node
                for current_node in current_nodes
                if symbol == current_node.to_symbol()
            ]
            if not matching_nodes:
                return False

            next_nodes: list[Node] = []
            seen_node_ids: set[int] = set()
            for current_node in matching_nodes:
                for descendant in current_node.descendents(self.grammar, True):
                    descendant_id = id(descendant)
                    if descendant_id in seen_node_ids:
                        continue
                    seen_node_ids.add(descendant_id)
                    next_nodes.append(descendant)
            current_nodes = next_nodes
        return True

    def onNonTerminalNodeVisit(
        self, node: NonTerminalNode, is_exploring: bool
    ) -> tuple[bool, bool]:
        if not is_exploring:
            return True, True
        first = self.k_path_to_reach[0]
        current_path = tuple(map(lambda x: x[0], self.current_path_collapsed))[
            -len(self.k_path_to_reach) :
        ]
        if current_path in self.seen_states:
            return True, False
        self.seen_states.add(current_path)
        if first == node.symbol:
            if self.test_reachability_from_node(node, self.k_path_to_reach):
                self.path_reached = True
            return False, False

        match = self.find_longest_suffix(current_path, tuple(self.k_path_to_reach))
        if len(match) == 0:
            return True, True
        if self.test_reachability_from_node(
            node, self.k_path_to_reach[len(match) - 1 :]
        ):
            self.path_reached = True
        return False, False

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool) -> bool:
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
