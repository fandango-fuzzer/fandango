from collections.abc import Callable, Generator, Hashable
from typing import Optional

from fandango.io.navigation.graph.blocked_step_pruner import (
    BlockedStepPruner,
    KPathTranslation,
)
from fandango.io.navigation.graph.grammar_navigator import GrammarNavigator
from fandango.io.navigation.graph.grammar_navigator.grammar_graph_converter import (
    GrammarGraphNode,
)
from fandango.io.navigation.graph.grammar_navigator.path_search import SearchTarget
from fandango.io.navigation.graph.grammar_navigator.rule_costs import RuleCosts
from fandango.io.navigation.graph.packetiterativeparser import (
    NavigatorPacketIterativeParser,
)
from fandango.io.navigation.graph.rule_recursion_tester import RuleRecursionTester
from fandango.io.navigation.graph.stategrammarconverter import StateGrammarConverter
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.route import GuidePath, PlannedPacket, Route
from fandango.io.navigation.step import Step
from fandango.language import DerivationTree, Grammar
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.symbols import NonTerminal, Symbol

# Sender and packet symbol of an earlier message
Predecessor = tuple[str, str]
RuledOutPredecessors = dict[PacketNonTerminal, frozenset[Predecessor]]


def packet_type_of(node: Node) -> Optional[PacketNonTerminal]:
    if not isinstance(node, NonTerminalNode) or node.sender is None:
        return None
    return PacketNonTerminal(
        node.sender, node.recipient, StateGrammarConverter.to_non_terminal(node.symbol)
    )


class PredecessorAvoidingTarget(SearchTarget):
    """
    A target reached only by routes that send no packet after a predecessor that rules it out in the run.
    The context of a route is the set of predecessors it sent, the history's included. The estimate in a context
    counts the packets it rules out as unreachable, so the search heads for routes around them.
    """

    def __init__(
        self,
        target_with: Callable[[RuleCosts], SearchTarget],
        costs_without: Callable[[frozenset[PacketNonTerminal]], RuleCosts],
        ruled_out: RuledOutPredecessors,
        history_predecessors: frozenset[Predecessor],
    ):
        """
        target_with builds the target on given costs; costs_without gives the costs with some packets unreachable.
        """
        self._target_with = target_with
        self._costs_without = costs_without
        self._ruled_out = ruled_out
        self._marks = frozenset().union(*ruled_out.values())
        self._start = history_predecessors & self._marks
        self._targets_by_unsendable: dict[
            frozenset[PacketNonTerminal], SearchTarget
        ] = {}
        self._target = self._target_without(frozenset())

    def is_reached(self, node: GrammarGraphNode) -> bool:
        return self._target.is_reached(node)

    def estimate(self, node: GrammarGraphNode) -> int:
        return self._target.estimate(node)

    def estimate_in(self, context: Hashable, node: GrammarGraphNode) -> int:
        assert isinstance(context, frozenset)
        return self._target_in(context).estimate(node)

    def can_complete_in(self, context: Hashable, node: GrammarGraphNode) -> bool:
        assert isinstance(context, frozenset)
        return self._target_in(context).can_complete(node)

    def _target_in(self, context: frozenset[Predecessor]) -> SearchTarget:
        """The target on costs that count the packets the context rules out as unreachable."""
        return self._target_without(
            frozenset(
                packet
                for packet, predecessors in self._ruled_out.items()
                if predecessors & context
            )
        )

    def _target_without(self, unsendable: frozenset[PacketNonTerminal]) -> SearchTarget:
        """The target on costs that count the unsendable packets as unreachable."""
        target = self._targets_by_unsendable.get(unsendable)
        if target is None:
            target = self._target_with(self._costs_without(unsendable))
            self._targets_by_unsendable[unsendable] = target
        return target

    def state(self, node: GrammarGraphNode) -> Hashable:
        return self._target.state(node)

    def start_context(self) -> Hashable:
        return self._start

    def enter(self, context: Hashable, node: GrammarGraphNode) -> Optional[Hashable]:
        assert isinstance(context, frozenset)
        entered = self._context_after(context, node)
        # Predecessors only add up along a route, so a target out of reach now stays out of reach
        if entered is None or not self.can_complete_in(entered, node):
            return None
        return entered

    def _context_after(
        self, context: frozenset[Predecessor], node: GrammarGraphNode
    ) -> Optional[frozenset[Predecessor]]:
        """The context after the route enters node, or None if the node sends a packet the context rules out."""
        packet = packet_type_of(node.node)
        if packet is None:
            return context
        if self._is_ruled_out(packet, context):
            return None
        assert packet.sender is not None
        predecessor = (packet.sender, packet.symbol.name())
        if predecessor not in self._marks:
            return context
        return context | {predecessor}

    def _is_ruled_out(self, packet: PacketNonTerminal, context: frozenset) -> bool:
        return bool(self._ruled_out.get(packet, frozenset()) & context)


class PacketNavigator(GrammarNavigator):
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: Optional[NonTerminal] = None,
        blocked_steps: frozenset[Step] = frozenset(),
        state_rules: Optional[dict[NonTerminal, Node]] = None,
        packet_symbols: Optional[set[NonTerminal]] = None,
        step_costs: Callable[[], dict[Step, int]] = dict,
        ruled_out_predecessors: Callable[[], RuledOutPredecessors] = dict,
    ):
        """
        Navigates the state grammar of the grammar, around the blocked steps.
        state_rules is that state grammar and packet_symbols are the grammar's message symbols.
        step_costs gives the costs that packet steps, as in their calling rule, add to their message.
        ruled_out_predecessors gives per packet type the earlier packets, as sender and symbol, after which no route
        sends it in the same run.
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
        self._step_costs = step_costs
        self._ruled_out_predecessors = ruled_out_predecessors
        self._costs_by_unsendable: dict[frozenset[PacketNonTerminal], RuleCosts] = {}
        self._seen_step_costs: dict[Step, int] = {}
        self._rule_step_by_node_id = self._rule_steps()
        self._step_cost_by_node_id: dict[int, int] = {}
        self._parser = NavigatorPacketIterativeParser(reduced_rules)
        self.set_message_cost(1)

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
            self._step_costs,
            self._ruled_out_predecessors,
        )

    def _rule_steps(self) -> dict[int, Step]:
        """Maps the id of each packet node in the rules to its step as in its calling rule."""
        steps: dict[int, Step] = {}

        def collect(node: Node, path: tuple[NonTerminal, ...]) -> None:
            if isinstance(node, NonTerminalNode):
                if node.sender is not None:
                    steps[id(node)] = Step((*path, self._pruner.original(node.symbol)))
                return
            if node.is_controlflow and not self._pruner.is_made_up(node):
                symbol = node.to_symbol()
                assert isinstance(symbol, NonTerminal)
                path = (*path, self._pruner.original(symbol))
            for child in node.children():
                collect(child, path)

        for symbol, body in self.grammar.rules.items():
            collect(body, (self._pruner.original(symbol),))
        return steps

    def _update_step_costs(self) -> None:
        """Reads the step costs. Clears the distances if they changed."""
        costs = self._step_costs()
        if costs != self._seen_step_costs:
            self._seen_step_costs = costs
            self._step_cost_by_node_id = {
                node_id: costs[step]
                for node_id, step in self._rule_step_by_node_id.items()
                if step in costs
            }
            self._costs.clear()
            self._costs_by_unsendable.clear()

    def _message_cost_of(self, node: Node) -> int:
        return super()._message_cost_of(node) + self._step_cost_by_node_id.get(
            id(node), 0
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
    ) -> Optional[GuidePath]:
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
        if len(routes) == 0:
            return None
        route, target = min(
            routes, key=lambda route_and_target: len(route_and_target[0])
        )
        if (
            target is None
            or not isinstance(target.node, NonTerminalNode)
            or target.node.sender is not None
        ):
            return GuidePath(route)
        return GuidePath(route, self._step_of_graph_node(target))

    def astar_tree(
        self,
        *,
        tree: DerivationTree,
        destination_k_path: KPath,
    ) -> Optional[list[GrammarGraphNode | None]]:
        self._update_step_costs()
        pruned_k_paths = self._pruned_k_paths(destination_k_path)
        if not pruned_k_paths:
            return None
        return self.astar_tree_to_any(tree=tree, destination_k_paths=pruned_k_paths)

    def _search_target(
        self,
        target_with: Callable[[RuleCosts], SearchTarget],
        tree: Optional[DerivationTree],
    ) -> SearchTarget:
        ruled_out = self._ruled_out_predecessors()
        if not ruled_out:
            return target_with(self._costs)
        return PredecessorAvoidingTarget(
            target_with,
            self._costs_without,
            ruled_out,
            self._predecessors_in(tree),
        )

    def _costs_without(self, unsendable: frozenset[PacketNonTerminal]) -> RuleCosts:
        """The costs of the messages, with the unsendable packets unreachable."""
        if not unsendable:
            return self._costs
        costs = self._costs_by_unsendable.get(unsendable)
        if costs is None:

            def message_cost_of(node: Node) -> int:
                if packet_type_of(node) in unsendable:
                    return RuleCosts.UNREACHABLE
                return self._message_cost_of(node)

            costs = RuleCosts(
                self.grammar.rules, message_cost_of, self.message_cost == 0
            )
            self._costs_by_unsendable[unsendable] = costs
        return costs

    @staticmethod
    def _predecessors_in(tree: Optional[DerivationTree]) -> frozenset[Predecessor]:
        """The packets of the control-flow tree, as sender and symbol."""
        if tree is None:
            return frozenset()
        predecessors = set()
        for record in tree.protocol_msgs():
            assert record.sender is not None
            symbol = StateGrammarConverter.to_non_terminal(record.msg.nonterminal)
            predecessors.add((record.sender, symbol.name()))
        return frozenset(predecessors)

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
        self._update_step_costs()
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
