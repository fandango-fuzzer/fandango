from typing import Optional, Set

from fandango.io.navigation.pathutils import find_longest_suffix
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
        self.seen_symbols: set[Symbol] = set()
        self.path_reached = False
        self.k_path_to_reach: KPath = tuple()

    def find_reachability(
        self,
        *,
        k_path_to_reach: KPath,
        tree: Optional[DerivationTree] = None,
    ):
        if not k_path_to_reach:
            return False
        self.path_reached = False
        self.k_path_to_reach = k_path_to_reach
        self.seen_symbols.clear()
        super().find(tree)
        return self.path_reached

    def test_reachability_from_node(self, node: NonTerminalNode, k_path_to_reach: KPath):
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


    def onNonTerminalNodeVisit(self, node: NonTerminalNode, is_exploring: bool):
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
        match = find_longest_suffix(current_path, tuple(self.k_path_to_reach))
        if len(match) == 0:
            return True, True
        if self.test_reachability_from_node(node, self.k_path_to_reach[len(match)-1:]):
            self.path_reached = True
        return False, False


    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool):
        if is_exploring:
            self.seen_symbols.add(node.symbol)
        return True