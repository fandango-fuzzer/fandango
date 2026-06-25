from typing import Optional

from fandango.io.navigation.stategrammarconverter import StateGrammarConverter
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class ProtocolModel:
    """
    Read-only protocol structure derived from the grammar.
    The state-grammar message symbols and permutation peer groups.
    """

    def __init__(self, grammar: Grammar, start_symbol: NonTerminal):
        self._grammar = grammar
        self.state_grammar_symbols = self._get_state_grammar_symbols(start_symbol)
        self.permutation_groups = self._build_permutation_groups()

    def group_messages_by_nt(
        self,
        trees: list[DerivationTree],
        non_terminals: Optional[set[NonTerminal]] = None,
    ) -> dict[NonTerminal, list[DerivationTree]]:
        """Group message subtrees by their NonTerminal symbol."""
        if non_terminals is None:
            non_terminals = self.state_grammar_symbols
        messages: list[DerivationTree] = []
        for tree in trees:
            for subtree in tree.flatten():
                if subtree.symbol in non_terminals:
                    messages.append(subtree)
        messages_by_nt: dict[NonTerminal, list[DerivationTree]] = {}
        for msg in messages:
            assert isinstance(msg.symbol, NonTerminal)
            messages_by_nt.setdefault(msg.symbol, []).append(msg)
        return messages_by_nt

    def _get_state_grammar_symbols(
        self, starting_symbol: NonTerminal
    ) -> set[NonTerminal]:
        state_grammar = StateGrammarConverter(self._grammar.grammar_settings).process(
            self._grammar.rules, starting_symbol
        )
        symbols = set(state_grammar.keys())
        symbols.update(
            map(
                lambda x: x.symbol,
                self._grammar.get_protocol_messages(starting_symbol),
            )
        )
        symbols = set(filter(lambda x: x in self._grammar.rules, symbols))
        return symbols

    def _build_permutation_groups(
        self,
    ) -> dict[NonTerminal, frozenset[NonTerminal]]:
        groups: dict[NonTerminal, frozenset[NonTerminal]] = {}
        for rule in self._grammar.rules.values():
            self._collect_permutation_groups(rule, groups)
        return groups

    def _collect_permutation_groups(
        self, node: Node, groups: dict[NonTerminal, frozenset[NonTerminal]]
    ) -> None:
        if isinstance(node, Alternative) and node.is_permutation:
            symbols: set[NonTerminal] = set()
            self._collect_packet_symbols_from_node(node, symbols)
            if len(symbols) > 1:
                group = frozenset(symbols)
                for sym in symbols:
                    groups[sym] = group
        for child in node.children():
            self._collect_permutation_groups(child, groups)

    @staticmethod
    def _collect_packet_symbols_from_node(
        node: Node, result: set[NonTerminal]
    ) -> None:
        if isinstance(node, NonTerminalNode) and node.sender is not None:
            result.add(node.symbol)
        else:
            for child in node.children():
                ProtocolModel._collect_packet_symbols_from_node(child, result)
