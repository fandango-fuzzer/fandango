from collections.abc import Generator, Hashable, Sequence
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
from fandango.io.navigation.graph.grammar_navigator.search_targets import (
    CostBasedTarget,
)
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
SuspectPredecessors = dict[PacketNonTerminal, frozenset[Predecessor]]


def packet_type_of(node: Node) -> Optional[PacketNonTerminal]:
    if not isinstance(node, NonTerminalNode) or node.sender is None:
        return None
    return PacketNonTerminal(
        node.sender, node.recipient, StateGrammarConverter.to_non_terminal(node.symbol)
    )


def predecessor_of(packet_type: PacketNonTerminal) -> Predecessor:
    """Identifies the packet type as predecessor by its sender and symbol."""
    assert packet_type.sender is not None
    return packet_type.sender, packet_type.symbol.name()


class SuspectAvoidingTarget(SearchTarget):
    """
    A target reached only by routes that send no packet after one of its suspect predecessors in the run.
    The context of a route is the set of predecessors it sent, the history's included. The estimate in a context
    counts the packets avoided in it as unreachable, so the search heads for routes around them.
    """

    def __init__(
        self,
        target: CostBasedTarget,
        costs: RuleCosts,
        message_nodes_by_packet_type: dict[PacketNonTerminal, frozenset[Node]],
        suspect_predecessors: SuspectPredecessors,
        history_predecessors: frozenset[Predecessor],
    ):
        """
        target is the target on costs; message_nodes_by_packet_type gives the rule nodes sending each packet.
        """
        self._unrestricted_target = target
        self._costs = costs
        self._message_nodes_by_packet_type = message_nodes_by_packet_type
        self._suspect_predecessors = suspect_predecessors
        self._tracked_predecessors = frozenset().union(*suspect_predecessors.values())
        self._start_context = history_predecessors & self._tracked_predecessors
        self._targets_by_avoided: dict[frozenset[PacketNonTerminal], SearchTarget] = {
            frozenset(): target
        }

    def is_reached(self, node: GrammarGraphNode) -> bool:
        return self._unrestricted_target.is_reached(node)

    def estimate(self, node: GrammarGraphNode) -> int:
        return self._unrestricted_target.estimate(node)

    def estimate_in(self, context: Hashable, node: GrammarGraphNode) -> int:
        assert isinstance(context, frozenset)
        return self._target_in(context).estimate(node)

    def can_complete_in(self, context: Hashable, node: GrammarGraphNode) -> bool:
        assert isinstance(context, frozenset)
        return self._target_in(context).can_complete(node)

    def _target_in(self, context: frozenset[Predecessor]) -> SearchTarget:
        """The target on costs that count the packets avoided in the context as unreachable."""
        return self._target_without(
            frozenset(
                packet_type
                for packet_type, predecessors in self._suspect_predecessors.items()
                if predecessors & context
            )
        )

    def _target_without(self, avoided: frozenset[PacketNonTerminal]) -> SearchTarget:
        """The target on costs that count the avoided packets as unreachable."""
        target = self._targets_by_avoided.get(avoided)
        if target is None:
            nodes = frozenset[Node]().union(
                *(
                    self._message_nodes_by_packet_type.get(packet_type, frozenset())
                    for packet_type in avoided
                )
            )
            target = self._unrestricted_target.with_costs(
                self._costs.without_messages(nodes)
            )
            self._targets_by_avoided[avoided] = target
        return target

    def state(self, node: GrammarGraphNode) -> Hashable:
        return self._unrestricted_target.state(node)

    def start_context(self) -> Hashable:
        return self._start_context

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
        """The context after the route enters node, or None if the node sends a packet avoided in the context."""
        packet_type = packet_type_of(node.node)
        if packet_type is None:
            return context
        if self._is_avoided(packet_type, context):
            return None
        predecessor = predecessor_of(packet_type)
        if predecessor not in self._tracked_predecessors:
            return context
        return context | {predecessor}

    def _is_avoided(
        self, packet_type: PacketNonTerminal, context: frozenset[Predecessor]
    ) -> bool:
        return bool(self._suspect_predecessors.get(packet_type, frozenset()) & context)


class PacketNavigator(GrammarNavigator):
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: Optional[NonTerminal] = None,
        blocked_steps: frozenset[Step] = frozenset(),
    ):
        """Navigates the state grammar of the grammar, around the blocked steps."""
        if start_symbol is None:
            start_symbol = NonTerminal("<start>")
        state_rules = StateGrammarConverter(grammar.grammar_settings).process(
            grammar.rules, start_symbol
        )
        self._protocol_grammar = grammar
        self._references = RuleRecursionTester(state_rules)
        self.blocked_steps = blocked_steps
        self._history_of_contained_k_paths: tuple[
            tuple[Optional[str], Optional[str], Symbol], ...
        ] = tuple()
        self._contained_by_k_paths: dict[frozenset[KPath], bool] = {}
        self._pruner = BlockedStepPruner(grammar.grammar_settings)
        reduced_rules = self._pruner.prune(state_rules, start_symbol, blocked_steps)
        self._k_paths = KPathTranslation(reduced_rules)
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
        self._packet_symbols = {
            message.symbol for message in grammar.get_protocol_messages(start_symbol)
        }
        self._step_costs: dict[Step, int] = {}
        self._suspect_predecessors: SuspectPredecessors = {}
        self._rule_step_by_node_id = self._rule_steps()
        self._message_nodes_by_packet_type = self._message_nodes()
        self._step_cost_by_node_id: dict[int, int] = {}
        self._parser = NavigatorPacketIterativeParser(reduced_rules)
        self.set_message_cost(1)

    def with_blocked_steps(self, blocked_steps: frozenset[Step]) -> "PacketNavigator":
        """Returns the same navigator routing around the blocked steps."""
        navigator = PacketNavigator(
            self._protocol_grammar, self._start_symbol, blocked_steps
        )
        navigator.set_step_costs(self._step_costs)
        navigator.set_suspect_predecessors(self._suspect_predecessors)
        return navigator

    def set_step_costs(self, costs: dict[Step, int]) -> None:
        """Sets the costs that packet steps, as in their calling rule, add to their message."""
        if costs != self._step_costs:
            self._step_costs = costs
            self._step_cost_by_node_id = {
                node_id: costs[step]
                for node_id, step in self._rule_step_by_node_id.items()
                if step in costs
            }
            self._costs.clear()

    def set_suspect_predecessors(
        self, suspect_predecessors: SuspectPredecessors
    ) -> None:
        """Sets per packet type the earlier packets after which routes avoid sending it."""
        self._suspect_predecessors = suspect_predecessors

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

    def _message_nodes(self) -> dict[PacketNonTerminal, frozenset[Node]]:
        """Maps each packet type to the nodes in the rules that send it."""
        nodes: dict[PacketNonTerminal, set[Node]] = {}
        pending = list(self.grammar.rules.values())
        while pending:
            node = pending.pop()
            packet_type = packet_type_of(node)
            if packet_type is not None:
                nodes.setdefault(packet_type, set()).add(node)
            elif not isinstance(node, NonTerminalNode):
                pending.extend(node.children())
        return {packet_type: frozenset(ids) for packet_type, ids in nodes.items()}

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
            self._contained_by_k_paths[key] = any(
                self._includes_k_paths(k_paths, controlflow_tree)
                for controlflow_tree, _ in self.controlflow_trees(tree)
            )
        return self._contained_by_k_paths[key]

    def is_derivable(self, destination_k_path: KPath) -> bool:
        """True if the k-path still exists in the grammar without the blocked steps."""
        if len(self.blocked_steps) == 0 or len(destination_k_path) == 0:
            return True
        return len(self._pruned_k_paths(destination_k_path)) != 0

    def _pruned_k_paths(self, spec_k_path: KPath) -> list[KPath]:
        return self._k_paths.to_pruned_k_paths(
            StateGrammarConverter.to_state_k_path(spec_k_path, self._packet_symbols)
        )

    def controlflow_trees(
        self, tree: DerivationTree
    ) -> Generator[tuple[DerivationTree, bool], None, None]:
        if next(tree.protocol_msgs(), None) is None:
            yield DerivationTree(NonTerminal("<start>")), False
            return
        yield from self._parser.controlflow_trees(tree)

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
        route: Route = []
        for node in path:
            if node is None:
                route.append(None)
            elif isinstance(node.node, NonTerminalNode):
                if node.node.sender is not None:
                    route.append(self._planned_packet(node))
                else:
                    route.append(self._pruner.original(node.node.symbol))
        return route

    def _planned_packet(self, graph_node: GrammarGraphNode) -> PlannedPacket:
        packet_type = packet_type_of(graph_node.node)
        assert packet_type is not None
        return PlannedPacket(packet_type, self._step_of_graph_node(graph_node))

    def _includes_k_paths(
        self, k_paths: set[KPath], controlflow_tree: DerivationTree
    ) -> bool:
        if len(k_paths) == 0:
            return True
        packet_k_paths = {
            StateGrammarConverter.to_state_k_path(k_path, self._packet_symbols)
            for k_path in k_paths
        }
        k = max(1, max(len(k_path) for k_path in k_paths))
        collapsed = self.grammar.collapse(controlflow_tree)
        if collapsed is None:
            return False
        covered_k_paths = {
            self._k_paths.to_state_k_path(k_path)
            for k_path in self.grammar._extract_k_paths_from_tree(collapsed, k)
        }
        return packet_k_paths <= covered_k_paths

    def _trees_including_k_paths(
        self, k_paths: set[KPath], tree: DerivationTree
    ) -> list[tuple[DerivationTree, bool]]:
        """The control-flow trees of tree that include the k-paths."""
        return [
            (controlflow_tree, is_complete)
            for controlflow_tree, is_complete in self.controlflow_trees(tree)
            if self._includes_k_paths(k_paths, controlflow_tree)
        ]

    def astar_tree_including_k_paths(
        self,
        *,
        tree: DerivationTree,
        destination_k_path: KPath,
        included_k_paths: Optional[set[KPath]] = None,
    ) -> Optional[GuidePath]:
        if included_k_paths is None:
            included_k_paths = set()
        routes: list[tuple[int, Route, Optional[GrammarGraphNode]]] = []
        found_trees = self._trees_including_k_paths(included_k_paths, tree)
        for suggested_tree, _is_complete in found_trees:
            path = self.astar_tree(
                controlflow_tree=suggested_tree, destination_k_path=destination_k_path
            )
            if path is None:
                continue
            routes.append(
                (
                    self._path_cost(path),
                    self._to_route(path),
                    path[-1] if len(path) != 0 else None,
                )
            )
        if len(routes) == 0:
            return None
        _, route, target = min(routes, key=lambda costed: (costed[0], len(costed[1])))
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
        controlflow_tree: Optional[DerivationTree] = None,
        destination_k_path: KPath,
    ) -> Optional[list[GrammarGraphNode | None]]:
        """Returns the cheapest path to the k-path, translated into the state grammar without the blocked steps."""
        pruned_k_paths = self._pruned_k_paths(destination_k_path)
        if not pruned_k_paths:
            return None
        return self._astar_tree_to_any(
            tree=controlflow_tree, destination_k_paths=pruned_k_paths
        )

    def _search_target(
        self, target: CostBasedTarget, tree: Optional[DerivationTree]
    ) -> SearchTarget:
        if not self._suspect_predecessors:
            return target
        return SuspectAvoidingTarget(
            target,
            self._costs,
            self._message_nodes_by_packet_type,
            self._suspect_predecessors,
            self._predecessors_in(tree),
        )

    @staticmethod
    def _predecessors_in(tree: Optional[DerivationTree]) -> frozenset[Predecessor]:
        """The packets of the control-flow tree, as sender and symbol."""
        if tree is None:
            return frozenset()
        return frozenset(
            predecessor_of(
                PacketNonTerminal(
                    record.sender,
                    record.recipient,
                    StateGrammarConverter.to_non_terminal(record.msg.nonterminal),
                )
            )
            for record in tree.protocol_msgs()
        )

    def astar_search_end_including_k_paths(
        self,
        tree: DerivationTree,
        included_k_paths: Optional[set[KPath]] = None,
    ) -> Optional[Route]:
        if included_k_paths is None:
            included_k_paths = set()
        routes: list[tuple[int, Route]] = []
        found_trees = self._trees_including_k_paths(included_k_paths, tree)
        for suggested_tree, is_complete in found_trees:
            if is_complete:
                return []
            node_path: list[Optional[GrammarGraphNode]] = list(
                self.astar_search_end(suggested_tree)
            )
            routes.append((self._path_cost(node_path), self._to_route(node_path)))

        if len(routes) == 0:
            return None
        _, route = min(routes, key=lambda costed: (costed[0], len(costed[1])))
        return route

    def _path_cost(self, path: Sequence[Optional[GrammarGraphNode]]) -> int:
        """Sums what entering the nodes of the path costs, as the search counts it."""
        return sum(
            self._message_cost_of(node.node) for node in path if node is not None
        )

    def __repr__(self) -> str:
        return (
            f"PacketNavigator({len(self.grammar.rules)} rules, "
            f"blocked_steps={sorted(self.blocked_steps, key=repr)!r}, {self._k_paths!r})"
        )
