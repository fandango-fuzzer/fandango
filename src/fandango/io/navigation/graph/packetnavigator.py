from collections.abc import Generator
from typing import Optional

from fandango.io.navigation.graph.blocked_step_pruner import BlockedStepPruner
from fandango.io.navigation.graph.grammarnavigator import GrammarNavigator
from fandango.io.navigation.graph.packetiterativeparser import (
    NavigatorPacketIterativeParser,
)
from fandango.io.navigation.graph.stategrammarconverter import StateGrammarConverter
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.route import PlannedPacket, Route
from fandango.io.navigation.step import Step
from fandango.language import DerivationTree, Grammar
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphNode,
)
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols.non_terminal import NonTerminal


class PacketNavigator(GrammarNavigator):
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: Optional[NonTerminal] = None,
        blocked_steps: frozenset[Step] = frozenset(),
        state_rules: Optional[dict[NonTerminal, Node]] = None,
    ):
        """
        Navigates the state grammar of the grammar, around the blocked steps.
        state_rules is that state grammar if it was already built, as with_blocked_steps passes it on.
        """
        if start_symbol is None:
            start_symbol = NonTerminal("<start>")
        if state_rules is None:
            state_rules = StateGrammarConverter(grammar.grammar_settings).process(
                grammar.rules, start_symbol
            )
        self._protocol_grammar = grammar
        self._state_rules = state_rules
        self.blocked_steps = blocked_steps
        self._derivable_by_k_path: dict[KPath, bool] = {}
        self._pruner = BlockedStepPruner(grammar.grammar_settings)
        reduced_rules = self._pruner.prune(state_rules, start_symbol, blocked_steps)
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
        self._parser = NavigatorPacketIterativeParser(reduced_rules)
        self.set_message_cost(1)

    def gen_with_blocked_steps(
        self, blocked_steps: frozenset[Step]
    ) -> "PacketNavigator":
        """Returns a new navigator for the same grammar that routes around the blocked steps."""
        return PacketNavigator(
            self._protocol_grammar, self._start_symbol, blocked_steps, self._state_rules
        )

    def is_derivable(self, destination_k_path: KPath) -> bool:
        """True if the k-path still exists in the grammar without the blocked steps."""
        if len(self.blocked_steps) == 0 or len(destination_k_path) == 0:
            return True
        derivable = self._derivable_by_k_path.get(destination_k_path)
        if derivable is None:
            names = [str(symbol) for symbol in self._search_k_path(destination_k_path)]
            references = self._reference_graph()
            derivable = names[0] in references and all(
                child in references.get(parent, ())
                for parent, child in zip(names, names[1:], strict=False)
            )
            self._derivable_by_k_path[destination_k_path] = derivable
        return derivable

    def get_controlflow_tree(
        self, tree: DerivationTree
    ) -> Generator[tuple[DerivationTree, bool], None, None]:
        messages = list(tree.protocol_msgs())
        if not messages:
            yield DerivationTree(NonTerminal("<start>")), False
            return
        history_nts = ""
        for message in messages:
            assert isinstance(message.msg.symbol, NonTerminal)
            history_nts += message.msg.symbol.name()
        self._parser.reference_tree = tree
        self._parser.parse_history(history_nts)
        for suggested_tree, is_complete in self._parser.tree_at(
            self._parser.consumed_length(), incomplete=True
        ):
            if StateGrammarConverter.matches_history(suggested_tree, messages):
                yield suggested_tree, is_complete

    def _step_of_graph_node(self, graph_node: GrammarGraphNode) -> Optional[Step]:
        """The step that produces the packet of the graph node."""
        path: list[NonTerminal] = []
        current: Optional[GrammarGraphNode] = graph_node
        while current is not None:
            if not self._pruner.is_made_up(current.node):
                symbol = current.node.to_symbol()
                assert isinstance(symbol, NonTerminal)
                path.append(symbol)
            current = current.parent
        return Step.of_path(path[::-1])

    def _to_route(self, path: list[Optional[GrammarGraphNode]]) -> Route:
        path = list(
            filter(lambda n: n is None or isinstance(n.node, NonTerminalNode), path)
        )
        route: Route = []
        for n in path:
            if n is None:
                route.append(None)
                continue
            assert isinstance(n.node, NonTerminalNode)
            if n.node.sender is not None:
                packet = PacketNonTerminal(
                    n.node.sender,
                    n.node.recipient,
                    StateGrammarConverter.to_non_terminal(n.node.symbol),
                )
                route.append(PlannedPacket(packet, self._step_of_graph_node(n)))
            else:
                route.append(NonTerminal(n.node.symbol.name()))
        return route

    def _includes_k_paths(
        self, k_paths: set[KPath], controlflow_tree: DerivationTree
    ) -> bool:
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

    def _find_trees_including_k_paths(
        self, k_paths: set[KPath], tree: DerivationTree
    ) -> tuple[list[tuple[DerivationTree, bool]], bool]:
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
        destination_k_path: KPath,
        included_k_paths: Optional[set[KPath]] = None,
    ) -> Optional[Route]:
        if included_k_paths is None:
            included_k_paths = set()
        routes: list[Route] = []
        found_trees, include_k_paths = self._find_trees_including_k_paths(
            included_k_paths, tree
        )
        for suggested_tree, _is_complete in found_trees:
            path = self.astar_tree(
                tree=suggested_tree, destination_k_path=destination_k_path
            )
            if path is None:
                continue
            routes.append(self._to_route(path))
        routes.sort(key=len)
        if len(routes) == 0:
            return None
        return routes[0]

    def astar_tree(
        self,
        *,
        tree: DerivationTree,
        destination_k_path: KPath,
    ) -> Optional[list[GrammarGraphNode | None]]:
        path = super().astar_tree(
            tree=tree, destination_k_path=self._search_k_path(destination_k_path)
        )
        return path

    def _search_k_path(self, k_path: KPath) -> KPath:
        search_symbols = []
        for symbol in k_path:
            if symbol in self._packet_symbols:
                search_symbols.append(
                    StateGrammarConverter.to_packet_non_terminal(symbol)
                )
            else:
                search_symbols.append(symbol)
        return tuple(search_symbols)

    def astar_search_end_including_k_paths(
        self,
        tree: DerivationTree,
        included_k_paths: Optional[set[KPath]] = None,
    ) -> Optional[Route]:
        if included_k_paths is None:
            included_k_paths = set()
        routes: list[Route] = []
        found_trees, include_k_paths = self._find_trees_including_k_paths(
            included_k_paths, tree
        )
        for suggested_tree, is_complete in found_trees:
            if is_complete:
                return []
            node_path = super().astar_search_end(suggested_tree)
            routes.append(self._to_route(list(node_path)))

        if len(routes) == 0:
            return None
        routes.sort(key=len)
        return routes[0]
