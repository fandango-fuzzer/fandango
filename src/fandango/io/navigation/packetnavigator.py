from typing import Optional

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.grammarnavigator import GrammarNavigator
from fandango.io.navigation.stategrammarconverter import StateGrammarConverter
from fandango.io.navigation.packetiterativeparser import PacketIterativeParser
from fandango.language import Grammar, DerivationTree
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphNode,
)
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode


class PacketNavigator(GrammarNavigator):

    def __init__(
        self, grammar: Grammar, start_symbol: NonTerminal = NonTerminal("<start>")
    ):
        reduced_rules = StateGrammarConverter(grammar.grammar_settings).process(
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
        self._packet_symbols: set[NonTerminal] = set(
            map(lambda x: x.symbol, grammar.get_protocol_messages(start_symbol))
        )
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
        path: list[Optional[GrammarGraphNode]],
    ) -> list[Optional[PacketNonTerminal | NonTerminal]]:
        path = list(
            filter(lambda n: n is None or isinstance(n.node, NonTerminalNode), path)
        )
        symbol_path: list[Optional[PacketNonTerminal | NonTerminal]] = []
        for n in path:
            if n is None:
                symbol_path.append(None)
                continue
            assert isinstance(n.node, NonTerminalNode)
            if n.node.sender is not None:
                symbol_path.append(
                    PacketNonTerminal(
                        n.node.sender,
                        n.node.recipient,
                        StateGrammarConverter.to_non_terminal(n.node.symbol),
                    )
                )
            else:
                symbol_path.append(NonTerminal(n.node.symbol.name()))
        return symbol_path

    def _includes_k_paths(self, k_paths: set[KPath], controlflow_tree: DerivationTree):
        if len(k_paths) == 0:
            return True
        packet_k_paths = set()
        for k_path in k_paths:
            packet_path: KPath = tuple()
            for symbol in k_path:
                if symbol in self._packet_symbols:
                    assert isinstance(symbol, NonTerminal)
                    symbol = StateGrammarConverter.to_packet_non_terminal(symbol)
                packet_path += (symbol,)
            packet_k_paths.add(packet_path)
        k = max(1, max(map(lambda x: len(x), k_paths)))
        col_tree = self.grammar.collapse(controlflow_tree)
        if col_tree is None:
            return False
        covered_k_paths = self.grammar._extract_k_paths_from_tree(col_tree, k)
        return len(packet_k_paths.difference(covered_k_paths)) == 0

    def _find_trees_including_k_paths(self, k_paths: set[KPath], tree: DerivationTree):
        match_k_paths_trees = []
        process_trees = []
        for suggested_tree, is_complete in self.get_controlflow_tree(tree):
            process_trees.append((suggested_tree, is_complete))
            if self._includes_k_paths(k_paths, suggested_tree):
                match_k_paths_trees.append((suggested_tree, is_complete))
        if len(match_k_paths_trees) != 0:
            return match_k_paths_trees, True
        return process_trees, False

    def astar_tree_including_k_paths(
        self,
        *,
        tree: DerivationTree,
        destination_k_path: tuple[NonTerminal, ...],
        included_k_paths: Optional[set[KPath]] = None,
    ) -> Optional[list[Optional[PacketNonTerminal | NonTerminal]]]:
        if included_k_paths is None:
            included_k_paths = set()
        paths = []
        found_trees, include_k_paths = self._find_trees_including_k_paths(
            included_k_paths, tree
        )
        for suggested_tree, is_complete in found_trees:
            path = self.astar_tree(
                tree=suggested_tree, destination_k_path=destination_k_path
            )
            if path is None:
                continue
            paths.append(path)
        paths.sort(key=lambda path: len(path))
        if len(paths) == 0:
            return None
        return paths[0]

    def astar_tree(
        self,
        *,
        tree: DerivationTree,
        destination_k_path: KPath,
    ) -> Optional[list[Optional[PacketNonTerminal | NonTerminal]]]:
        search_destination_symbols = []
        for symbol in destination_k_path:
            if symbol in self._packet_symbols:
                search_destination_symbols.append(
                    StateGrammarConverter.to_packet_non_terminal(symbol)
                )
            else:
                search_destination_symbols.append(symbol)
        path = super().astar_tree(
            tree=tree, destination_k_path=tuple(search_destination_symbols)
        )
        if path is None:
            return None
        return self._to_symbols(path)

    def astar_search_end(
        self,
        tree: DerivationTree,
        included_k_paths: Optional[set[KPath]] = None,
    ) -> Optional[list[PacketNonTerminal | NonTerminal]]:
        if included_k_paths is None:
            included_k_paths = set()
        paths: list[list[PacketNonTerminal | NonTerminal]] = []
        found_trees, include_k_paths = self._find_trees_including_k_paths(
            included_k_paths, tree
        )
        for suggested_tree, is_complete in found_trees:
            if is_complete:
                return []
            node_path = super().astar_search_end(suggested_tree)
            path_symbols: list[PacketNonTerminal | NonTerminal] = []
            for symbol in self._to_symbols(list(node_path)):
                assert symbol is not None
                path_symbols.append(symbol)
            paths.append(path_symbols)

        if len(paths) == 0:
            return None
        paths.sort(key=lambda path: len(path))
        return paths[0]
