from collections.abc import Generator
from typing import Optional

from fandango.io.navigation.graph.blocked_step_pruner import (
    BlockedStepPruner,
    KPathTranslation,
)
from fandango.io.navigation.graph.grammarnavigator import GrammarNavigator
from fandango.io.navigation.graph.packetiterativeparser import (
    NavigatorPacketIterativeParser,
)
from fandango.io.navigation.graph.rule_recursion_tester import RuleRecursionTester
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
from fandango.language.symbols import NonTerminal, Symbol


class PacketNavigator(GrammarNavigator):
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: Optional[NonTerminal] = None,
        blocked_steps: frozenset[Step] = frozenset(),
        state_rules: Optional[dict[NonTerminal, Node]] = None,
        packet_symbols: Optional[set[NonTerminal]] = None,
    ):
        """
        Navigates the state grammar of the grammar, around the blocked steps.
        state_rules is that state grammar and packet_symbols are the grammar's message symbols.
        """
        if start_symbol is None:
            start_symbol = NonTerminal("<start>")
        if state_rules is None:
            state_rules = StateGrammarConverter(grammar.grammar_settings).process(
                grammar.rules, start_symbol
            )
        if packet_symbols is None:
            packet_symbols = {
                message.symbol
                for message in grammar.get_protocol_messages(start_symbol)
            }
        self._protocol_grammar = grammar
        self._state_rules = state_rules
        self._references = RuleRecursionTester(state_rules)
        self.blocked_steps = blocked_steps
        self._history_of_contained_k_paths: tuple[
            tuple[Optional[str], Optional[str], Symbol], ...
        ] = tuple()
        self._contained_by_k_paths: dict[frozenset[KPath], bool] = {}
        self._pruner = BlockedStepPruner(grammar.grammar_settings)
        reduced_rules = self._pruner.prune(state_rules, start_symbol, blocked_steps)
        self._k_paths = KPathTranslation(reduced_rules)
        self._pruned_k_paths_by_k_path: dict[KPath, list[KPath]] = {}
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
        self._packet_symbols = packet_symbols
        self._parser = NavigatorPacketIterativeParser(reduced_rules)
        self.set_message_cost(1)
        self.last_target_step: Optional[Step] = None
        self.last_target_packets: list[PlannedPacket] = []

    def gen_with_blocked_steps(
        self, blocked_steps: frozenset[Step]
    ) -> "PacketNavigator":
        """Returns a new navigator for the same grammar that routes around the blocked steps."""
        return PacketNavigator(
            self._protocol_grammar,
            self._start_symbol,
            blocked_steps,
            self._state_rules,
            self._packet_symbols,
        )

    def contains_k_paths(self, k_paths: set[KPath], tree: DerivationTree) -> bool:
        """True if a control-flow tree the messages held by tree contains the requested k-paths."""
        history = tuple(
            (record.sender, record.recipient, record.msg.symbol)
            for record in tree.protocol_msgs()
        )
        if history != self._history_of_contained_k_paths:
            self._history_of_contained_k_paths = history
            self._contained_by_k_paths.clear()
        key = frozenset(k_paths)
        if key not in self._contained_by_k_paths:
            _trees, contained = self._find_trees_including_k_paths(k_paths, tree)
            self._contained_by_k_paths[key] = contained
        return self._contained_by_k_paths[key]

    def is_derivable(self, destination_k_path: KPath) -> bool:
        """True if the k-path still exists in the grammar without the blocked steps."""
        if len(self.blocked_steps) == 0 or len(destination_k_path) == 0:
            return True
        return len(self._pruned_k_paths(destination_k_path)) != 0

    def _pruned_k_paths(self, k_path: KPath) -> list[KPath]:
        pruned = self._pruned_k_paths_by_k_path.get(k_path)
        if pruned is None:
            pruned = self._k_paths.to_pruned_k_paths(self._search_k_path(k_path))
            self._pruned_k_paths_by_k_path[k_path] = pruned
        return pruned

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

    def _step_of_graph_node(self, graph_node: GrammarGraphNode) -> Step:
        """The step that produces the packet of the graph node."""
        path: list[NonTerminal] = []
        current: Optional[GrammarGraphNode] = graph_node
        while current is not None:
            if not self._pruner.is_made_up(current.node):
                symbol = current.node.to_symbol()
                assert isinstance(symbol, NonTerminal)
                path.append(self._pruner.original(symbol))
            current = current.parent
        return Step.of_path(path[::-1], self._references.is_recursive_call)

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
                route.append(self._planned_packet(n))
            else:
                route.append(self._pruner.original(n.node.symbol))
        return route

    def _planned_packet(self, graph_node: GrammarGraphNode) -> PlannedPacket:
        assert isinstance(graph_node.node, NonTerminalNode)
        assert graph_node.node.sender is not None
        packet = PacketNonTerminal(
            graph_node.node.sender,
            graph_node.node.recipient,
            StateGrammarConverter.to_non_terminal(graph_node.node.symbol),
        )
        return PlannedPacket(packet, self._step_of_graph_node(graph_node))

    def _packets_within(self, target: GrammarGraphNode) -> list[PlannedPacket]:
        """The packets inside target along its continuation, as far as the continuation does not branch."""
        packets: list[PlannedPacket] = []
        visited = {id(target.node)}
        current = target
        while len(current.reaches) == 1:
            current = current.reaches[0]
            if id(current.node) in visited or not self._is_within(current, target):
                break
            visited.add(id(current.node))
            if (
                isinstance(current.node, NonTerminalNode)
                and current.node.sender is not None
            ):
                packets.append(self._planned_packet(current))
        return packets

    @staticmethod
    def _is_within(graph_node: GrammarGraphNode, ancestor: GrammarGraphNode) -> bool:
        current: Optional[GrammarGraphNode] = graph_node
        while current is not None:
            if current is ancestor:
                return True
            current = current.parent
        return False

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
        covered_k_paths = {
            tuple(
                self._pruner.original(symbol)
                if isinstance(symbol, NonTerminal)
                else symbol
                for symbol in k_path
            )
            for k_path in self.grammar._extract_k_paths_from_tree(col_tree, k)
        }
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
        routes: list[tuple[Route, Optional[GrammarGraphNode]]] = []
        found_trees, include_k_paths = self._find_trees_including_k_paths(
            included_k_paths, tree
        )
        for suggested_tree, _is_complete in found_trees:
            path = self.astar_tree(
                tree=suggested_tree, destination_k_path=destination_k_path
            )
            if path is None:
                continue
            routes.append((self._to_route(path), path[-1] if len(path) != 0 else None))
        self.last_target_step = None
        self.last_target_packets = []
        if len(routes) == 0:
            return None
        route, target = min(
            routes, key=lambda route_and_target: len(route_and_target[0])
        )
        if (
            target is not None
            and isinstance(target.node, NonTerminalNode)
            and target.node.sender is None
        ):
            self.last_target_step = self._step_of_graph_node(target)
            self.last_target_packets = self._packets_within(target)
        return route

    def astar_tree(
        self,
        *,
        tree: DerivationTree,
        destination_k_path: KPath,
    ) -> Optional[list[GrammarGraphNode | None]]:
        paths = []
        for pruned_k_path in self._pruned_k_paths(destination_k_path):
            path = super().astar_tree(tree=tree, destination_k_path=pruned_k_path)
            if path is not None:
                paths.append(path)
        return min(paths, key=len, default=None)

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

    def __repr__(self) -> str:
        return (
            f"PacketNavigator({len(self.grammar.rules)} rules, "
            f"blocked_steps={sorted(self.blocked_steps, key=repr)!r}, {self._k_paths!r})"
        )
