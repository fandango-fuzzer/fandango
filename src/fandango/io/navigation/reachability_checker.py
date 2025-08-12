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
        self.seen_symbols: set[tuple[Optional[str], Optional[str], Symbol]] = set()
        self.search_sender = None
        self.search_recipient = None

    def find_reachability(
        self,
        *,
        symbol_to_reach: Symbol,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        tree: Optional[DerivationTree] = None,
    ):
        self.search_sender = sender
        self.search_recipient = recipient
        self.seen_symbols.clear()
        super().find(tree)
        key = (self.search_sender, self.search_recipient, symbol_to_reach)
        return key in self.seen_symbols

    def onNonTerminalNodeVisit(self, node: NonTerminalNode, is_exploring: bool):
        if is_exploring:
            sender = None if self.search_sender is None else node.sender
            recipient = None if self.search_recipient is None else node.recipient
            key = (sender, recipient, node.symbol)
            if key not in self.seen_symbols:
                self.seen_symbols.add(key)
                return True, True
            return True, False
        return True, True

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool):
        if is_exploring:
            self.seen_symbols.add((None, None, node.symbol))
        return True
