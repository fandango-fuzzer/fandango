from typing import Optional

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.grammarnavigator import GrammarNavigator
from fandango.io.navigation.grammarreducer import GrammarReducer
from fandango.io.navigation.packetiterativeparser import PacketIterativeParser
from fandango.language import Grammar, NonTerminal, DerivationTree, Terminal, Symbol
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphNode,
)
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode


class PacketNavigator(GrammarNavigator):

    def __init__(
        self, grammar: Grammar, start_symbol: NonTerminal = NonTerminal("<start>")
    ):
        reduced_rules = GrammarReducer(grammar.grammar_settings).process(
            grammar.rules, start_symbol
        )
        super().__init__(
            Grammar(
                grammar_settings=grammar.grammar_settings,
                rules=reduced_rules,
                fuzzing_mode=grammar.fuzzing_mode,
                local_variables=grammar._local_variables,
                global_variables=grammar._global_variables,
            ),
            start_symbol,
        )
        self._packet_symbols = set(map(lambda x: x[2], grammar.get_protocol_messages(start_symbol)))
        self._parser = PacketIterativeParser(reduced_rules)
        self.set_message_cost(1)

    def get_controlflow_tree(self, tree: DerivationTree):
        history_nts = ""
        for r_msg in tree.protocol_msgs():
            assert isinstance(r_msg.msg.symbol, NonTerminal)
            history_nts += r_msg.msg.symbol.name()

        if history_nts == "":
            yield DerivationTree(NonTerminal("<start>")), False
            return
        self._parser.detailed_tree = tree
        self._parser.new_parse(NonTerminal("<start>"), ParsingMode.INCOMPLETE)

        for suggested_tree, is_complete in self._parser.consume(history_nts):
            for orig_r_msg, r_msg in zip(
                tree.protocol_msgs(), suggested_tree.protocol_msgs()
            ):
                assert isinstance(r_msg.msg.symbol, NonTerminal)
                assert isinstance(orig_r_msg.msg.symbol, NonTerminal)
                if (
                    r_msg.msg.symbol.name()[9:] == orig_r_msg.msg.symbol.name()[1:]
                    and r_msg.sender == orig_r_msg.sender
                    and r_msg.recipient == orig_r_msg.recipient
                ):
                    pass  # Todo set children for computed length repetitions
                else:
                    break
            else:
                yield suggested_tree, is_complete

    @staticmethod
    def _to_symbols(
        path: list[GrammarGraphNode],
    ) -> list[Optional[PacketNonTerminal | NonTerminal]]:
        path = list(filter(lambda n: n is None or isinstance(n.node, NonTerminalNode), path))
        symbol_path = []
        for n in path:
            if n is None:
                symbol_path.append(None)
                continue
            if n.node.sender is not None:
                symbol_path.append(PacketNonTerminal(n.node.sender, n.node.recipient, NonTerminal(f"<{n.node.symbol.name()[9:]}" if n.node.symbol.name().startswith("<_packet_") else n.node.symbol.name())))
            else:
                symbol_path.append(NonTerminal(n.node.symbol.name()))
        return symbol_path

    def _includes_k_paths(self, k_paths: set[tuple[Symbol, ...]], controlflow_tree: DerivationTree):
        if len(k_paths) == 0:
            return True
        k = max(1, max(map(lambda x: len(x), k_paths)))
        col_tree = self.grammar.collapse(controlflow_tree)
        covered_k_paths = self.grammar._extract_k_paths_from_tree(col_tree, k)
        return len(k_paths.difference(covered_k_paths)) == 0

    def _find_trees_including_k_paths(self, k_paths: set[tuple[Symbol, ...]], tree: DerivationTree):
        match_k_paths_trees = []
        process_trees = []
        for suggested_tree, is_complete in self.get_controlflow_tree(tree):
            process_trees.append((suggested_tree, is_complete))
            if self._includes_k_paths(k_paths, self.grammar.collapse(suggested_tree)):
                match_k_paths_trees.append((suggested_tree, is_complete))
        if len(match_k_paths_trees) != 0:
            process_trees = match_k_paths_trees
        return process_trees

    def astar_tree(
        self,
        *,
        tree: DerivationTree,
        destination_symbols: list[NonTerminal],
        included_k_paths: Optional[set[tuple[Symbol, ...]]] = None
    ) -> Optional[list[PacketNonTerminal | NonTerminal]]:
        if included_k_paths is None:
            included_k_paths = set()
        paths = []
        search_destination_symbols = []
        for symbol in destination_symbols:
            if symbol in self._packet_symbols:
                search_destination_symbols.append(NonTerminal(f"<{symbol.name()[1:-1]}>"))
            else:
                search_destination_symbols.append(symbol)
        for suggested_tree, is_complete in self._find_trees_including_k_paths(included_k_paths, tree):
            path = super().astar_tree(
                tree=suggested_tree, destination_symbols=search_destination_symbols
            )
            if path is None:
                continue
            paths.append(self._to_symbols(list(path)))

        paths.sort(key=lambda path: len(path))
        if len(paths) == 0:
            return None
        return paths[0]

    def astar_search_end(
        self, tree: DerivationTree, included_k_paths: Optional[set[tuple[Symbol, ...]]] = None
    ) -> Optional[list[PacketNonTerminal | NonTerminal]]:
        if included_k_paths is None:
            included_k_paths = set()
        paths = []
        for suggested_tree, is_complete in self._find_trees_including_k_paths(included_k_paths, tree):
            if is_complete:
                return []
            path = super().astar_search_end(suggested_tree)
            paths.append(self._to_symbols(list(path)))
        paths.sort(key=lambda path: len(path))
        return paths[0]
