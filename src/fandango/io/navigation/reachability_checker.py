from typing import Optional, Set

from fandango.io.navigation.visitor.continuing_nodevisitor import ContinuingNodeVisitor
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
        self.symbol_chain_to_reach: list[Symbol] = []

    def find_reachability(
        self,
        *,
        symbol_chain_to_reach: list[Symbol],
        tree: Optional[DerivationTree] = None,
    ):
        if not symbol_chain_to_reach:
            return False
        self.path_reached = False
        self.symbol_chain_to_reach = symbol_chain_to_reach
        self.seen_symbols.clear()
        super().find(tree)
        return self.path_reached

    def onNonTerminalNodeVisit(self, node: NonTerminalNode, is_exploring: bool):
        if not is_exploring:
            return True, True
        first = self.symbol_chain_to_reach[0]
        if node.symbol in self.seen_symbols:
            return True, False
        node_symbols = self._to_normal_symbol(node.symbol)
        self.seen_symbols.update(node_symbols)

        if first not in node_symbols:
            return True, True
        current_node = node
        chain_found = True
        for child_symbol in self.symbol_chain_to_reach[1:]:
            seen = set()
            work = set()
            work.add(current_node)
            while len(work) != 0:
                n = work.pop()
                if n in seen:
                    continue
                seen.add(n)
                work.update(n.descendents(self.grammar, True))
            child_nodes = list(
                filter(
                    lambda n: child_symbol in self._to_normal_symbol(n.to_symbol()),
                    seen,
                )
            )
            if not child_nodes:
                chain_found = False
                break
            current_node = child_nodes[0]
        if chain_found:
            self.path_reached = True
        return False, False

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool):
        if is_exploring:
            self.seen_symbols.add(node.symbol)
        return True

    def _to_normal_symbol(self, symbol: Symbol) -> set[Symbol]:
        returnme = set()
        returnme.add(symbol)
        if str(symbol).startswith("<_packet_"):
            if isinstance(symbol, NonTerminal):
                returnme.add(NonTerminal(f"<{symbol.name()[9:]}"))
            if isinstance(symbol, Terminal):
                returnme.add(Terminal(f"<{str(symbol)[9:]}"))
        return returnme
