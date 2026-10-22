import heapq
from collections.abc import Callable, Sequence
from typing import Optional

from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol


class RuleCosts:
    """
    Computes what the messages derived by grammar rules cost at least:
    for a node, up to a target symbol, and from one symbol to another.
    """

    UNREACHABLE = 100_000

    def __init__(
        self,
        rules: dict[NonTerminal, Node],
        message_cost_of: Callable[[Node], int],
        count_references: bool = False,
        unrestricted: Optional["RuleCosts"] = None,
    ):
        """
        message_cost_of gives the cost of the message that a node sends.
        count_references makes entering a symbol cost 1 instead, for rules whose messages cost nothing.
        unrestricted are the costs without the restrictions, if message_cost_of makes some messages unreachable.
        """
        self._rules = rules
        self._unrestricted = unrestricted
        self._message_cost_of = message_cost_of
        self._count_references = count_references
        self._cheapest_costs: Optional[dict[NonTerminal, int]] = None
        # symbol -> symbols whose rule references it -> cheapest cost within that rule, from its start up to and
        # including entering the reference.
        self._cached_reaching_costs_in_rules: Optional[dict[str, dict[str, int]]] = None
        self._distances_by_target: dict[str, dict[str, int]] = {}
        self._costs_without_messages: dict[frozenset[Node], RuleCosts] = {}

    def clear(self) -> None:
        """Forgets every computed cost, as after the message costs changed."""
        self._cheapest_costs = None
        self._cached_reaching_costs_in_rules = None
        self._distances_by_target.clear()
        self._costs_without_messages.clear()

    def without_messages(self, nodes: frozenset[Node]) -> "RuleCosts":
        """Returns these costs with the messages of the nodes unreachable."""
        if not nodes:
            return self
        costs = self._costs_without_messages.get(nodes)
        if costs is None:
            message_cost_of = self._message_cost_of

            def message_cost_without(node: Node) -> int:
                if node in nodes:
                    return self.UNREACHABLE
                return message_cost_of(node)

            costs = RuleCosts(
                self._rules,
                message_cost_without,
                self._count_references,
                unrestricted=self,
            )
            self._costs_without_messages[nodes] = costs
        return costs

    def cost_of(self, node: Node) -> int:
        """Returns the cost of the cheapest messages that node derives."""
        if isinstance(node, NonTerminalNode):
            return self._message_cost_of(node) + self._cheapest_cost_below(node)
        if isinstance(node, Alternative):
            return min(map(self.cost_of, node.children()))
        if isinstance(node, Repetition):
            return node.min * self.cost_of(node.node)
        return sum(map(self.cost_of, node.children()))

    def cost_into(self, node: Node, distances: dict[str, int]) -> int:
        """Returns the cheapest cost from before node to the target of distances below node."""
        if isinstance(node, (NonTerminalNode, TerminalNode)):
            return self._entering_cost(node) + distances.get(
                str(node.symbol), self.UNREACHABLE
            )
        if isinstance(node, Concatenation):
            return self.cost_ahead(node.children(), distances, self.UNREACHABLE)
        return min(
            (self.cost_into(child, distances) for child in node.children()),
            default=self.UNREACHABLE,
        )

    def cost_ahead(
        self, nodes: Sequence[Node], distances: dict[str, int], beyond: int
    ) -> int:
        """
        Returns the cheapest cost to the target of distances:
        below one of the nodes in sequence, or after them at cost beyond.
        """
        cost = self.UNREACHABLE
        before = 0
        for node in nodes:
            cost = min(cost, before + self.cost_into(node, distances))
            before += self.cost_of(node)
        return min(cost, before + beyond, self.UNREACHABLE)

    def cost_from(self, node: Node, distances: dict[str, int], after: int) -> int:
        """Returns the cheapest cost from the entered node to the target of distances, below it or after its end."""
        if isinstance(node, NonTerminalNode):
            # The message of the node itself is sent already.
            return min(
                distances.get(str(node.symbol), self.UNREACHABLE),
                self._cheapest_cost_below(node) + after,
            )
        if isinstance(node, TerminalNode):
            return min(distances.get(str(node.symbol), self.UNREACHABLE), after)
        return self.cost_ahead([node], distances, after)

    def costs_after(
        self,
        node: Node,
        parent: Node,
        distances_by_target: Sequence[dict[str, int]],
        after_parent: tuple[int, ...],
    ) -> tuple[int, ...]:
        """Returns the cheapest cost from the end of node to each target, given those from the end of its parent."""
        if isinstance(parent, (NonTerminalNode, Alternative)):
            return after_parent
        targets = list(zip(distances_by_target, after_parent, strict=True))
        if isinstance(parent, Repetition):
            if parent.max == 1:
                return after_parent
            # Another round or the end. Ignores how many rounds are left.
            return tuple(
                min(self.cost_into(node, distances), after)
                for distances, after in targets
            )
        siblings = parent.children()
        following = siblings[
            next(i for i, sibling in enumerate(siblings) if sibling is node) + 1 :
        ]
        return tuple(
            self.cost_ahead(following, distances, after) for distances, after in targets
        )

    def is_derivable(self, symbol: Symbol) -> bool:
        """
        False if the symbol's rule has a derivation without the restrictions but none with them. True for every symbol
        if there are no restrictions.
        """
        if (
            self._unrestricted is None
            or not isinstance(symbol, NonTerminal)
            or symbol not in self._rules
        ):
            return True
        return self._can_finish(symbol) or not self._unrestricted._can_finish(symbol)

    def _can_finish(self, symbol: NonTerminal) -> bool:
        """True if some derivation of the symbol's rule costs less than UNREACHABLE."""
        return self._cheapest_cost_below(NonTerminalNode(symbol, [])) < self.UNREACHABLE

    def distances_to(self, target: Symbol) -> dict[str, int]:
        """Returns the cheapest cost from the start of every symbol's rule to target."""
        key = str(target)
        cached = self._distances_by_target.get(key)
        if cached is not None:
            return cached
        reaching_costs = self._reaching_costs_in_rules()
        distances: dict[str, int] = {key: 0}
        nearest = [(0, key)]
        while nearest:
            cost, symbol = heapq.heappop(nearest)
            if cost > distances[symbol]:
                continue
            for rule, cost_in_rule in reaching_costs.get(symbol, {}).items():
                if cost + cost_in_rule < distances.get(rule, self.UNREACHABLE):
                    distances[rule] = cost + cost_in_rule
                    heapq.heappush(nearest, (distances[rule], rule))
        self._distances_by_target[key] = distances
        return distances

    def _entering_cost(self, node: Node) -> int:
        """Returns the cost of entering the symbol of node."""
        return 1 if self._count_references else self._message_cost_of(node)

    def _cheapest_cost_below(self, node: NonTerminalNode) -> int:
        """Returns the cost of the cheapest messages that the rule of node's symbol derives."""
        if self._cheapest_costs is None:
            self._cheapest_costs = {}
            changed = True
            while changed:
                changed = False
                for symbol, body in self._rules.items():
                    cost = self.cost_of(body)
                    if cost < self._cheapest_costs.get(symbol, self.UNREACHABLE):
                        self._cheapest_costs[symbol] = cost
                        changed = True
        return self._cheapest_costs.get(node.symbol, self.UNREACHABLE)

    def _reaching_costs_in_rules(self) -> dict[str, dict[str, int]]:
        """
        Returns per symbol the rules that reference it, each with the cheapest cost within that rule from its start up
        to and including entering the reference.
        """
        if self._cached_reaching_costs_in_rules is not None:
            return self._cached_reaching_costs_in_rules
        reaching_costs: dict[str, dict[str, int]] = {}

        def references(rule: str, node: Node, before: int) -> None:
            if isinstance(node, (NonTerminalNode, TerminalNode)):
                cost = before + self._entering_cost(node)
                rules = reaching_costs.setdefault(str(node.symbol), {})
                if cost < rules.get(rule, self.UNREACHABLE):
                    rules[rule] = cost
                return
            for child in node.children():
                references(rule, child, before)
                if isinstance(node, Concatenation):
                    before += self.cost_of(child)

        for symbol, body in self._rules.items():
            references(str(symbol), body, 0)
        self._cached_reaching_costs_in_rules = reaching_costs
        return reaching_costs
