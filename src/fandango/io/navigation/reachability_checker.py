from typing import Optional, Set

from fandango.io.navigation.visitor.continuing_nodevisitor import ContinuingNodeVisitor
from fandango.language.tree import DerivationTree
from fandango.language import Grammar, Symbol
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
        self.seen_symbols: Set[Symbol] = set()

    def find_reachability(self, symbol_to_reach: Symbol, tree: Optional[DerivationTree] = None):
        self.seen_symbols.clear()
        super().find(tree)
        return symbol_to_reach in self.seen_symbols

    def onNonTerminalNodeVisit(self, node: NonTerminalNode, is_exploring: bool):
        if is_exploring:
            if node.symbol not in self.seen_symbols:
                self.seen_symbols.add(node.symbol)
                return True, True
            return True, False
        return True, True

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool):
        if is_exploring:
            self.seen_symbols.add(node.symbol)
        return True