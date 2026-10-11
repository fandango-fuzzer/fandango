import heapq
import itertools
from abc import ABC, abstractmethod
from collections.abc import Callable, Hashable
from typing import Optional

from fandango.errors import FandangoError
from fandango.io.navigation.graph.grammar_navigator.grammar_graph_converter import (
    GrammarGraphNode,
)

Entry = tuple[GrammarGraphNode, Hashable]


class NavigatorTimedOutError(FandangoError):
    pass


class SearchTarget(ABC):
    """What a path search wants to reach."""

    @abstractmethod
    def is_reached(self, node: GrammarGraphNode) -> bool:
        """True if node reaches the target."""

    @abstractmethod
    def estimate(self, node: GrammarGraphNode) -> int:
        """Returns the estimated cost from node to the target."""

    @abstractmethod
    def state(self, node: GrammarGraphNode) -> Hashable:
        """Returns a key shared by the nodes that the search may treat as one."""

    def can_complete(self, node: GrammarGraphNode) -> bool:
        """False if no path from node can reach the target."""
        return True

    def can_complete_in(self, context: Hashable, node: GrammarGraphNode) -> bool:
        """False if no path from node, in the context, can reach the target."""
        return self.can_complete(node)

    def estimate_in(self, context: Hashable, node: GrammarGraphNode) -> int:
        """Returns the estimated cost from node to the target, for a path in the context."""
        return self.estimate(node)

    def start_context(self) -> Hashable:
        """What the target needs to know about the path that led to the start of the search. Never None."""
        return ()

    def enter(self, context: Hashable, node: GrammarGraphNode) -> Optional[Hashable]:
        """The context after the path steps onto node, or None if the path may not enter it."""
        return context


class PathSearch:
    """Searches the cheapest path from a graph node to a target, with A*."""

    def __init__(
        self,
        target: SearchTarget,
        cost_of_entering: Callable[[GrammarGraphNode], int],
        max_comparisons: int,
    ):
        """cost_of_entering gives what it costs to step onto a node."""
        self._target = target
        self._cost_of_entering = cost_of_entering
        self._max_comparisons = max_comparisons
        self.comparisons = 0
        """How many nodes the last search compared with the target."""

    def cheapest_path(
        self, start: GrammarGraphNode
    ) -> Optional[list[GrammarGraphNode]]:
        """
        Returns the cheapest path from start to a node that reaches the target, or None if there is none.
        """
        self.comparisons = 0
        if self._is_reached(start):
            return []
        target = self._target
        insertion_order = itertools.count()
        # A path reaches a node within a context, which the target derives from the nodes on the path.
        start_entry = (start, target.start_context())
        if not target.can_complete_in(start_entry[1], start):
            return None
        best_costs = {(target.state(start), start_entry[1]): 0}
        came_from: dict[Entry, Optional[Entry]] = {start_entry: None}
        closed: set[Hashable] = set()
        frontier = [
            (
                target.estimate_in(start_entry[1], start),
                next(insertion_order),
                0,
                start_entry,
            )
        ]
        while frontier:
            _, _, cost, current = heapq.heappop(frontier)
            current_node, context = current
            state = (target.state(current_node), context)
            if state in closed or cost > best_costs[state]:
                continue
            if self._is_reached(current_node):
                return self._path_to(current, came_from)
            closed.add(state)
            for neighbor in current_node.reaches:
                neighbor_context = target.enter(context, neighbor)
                if neighbor_context is None:
                    continue
                neighbor_state = (target.state(neighbor), neighbor_context)
                if neighbor_state in closed:
                    continue
                neighbor_cost = cost + self._cost_of_entering(neighbor)
                if neighbor_cost >= best_costs.get(neighbor_state, neighbor_cost + 1):
                    continue
                best_costs[neighbor_state] = neighbor_cost
                neighbor_entry = (neighbor, neighbor_context)
                came_from[neighbor_entry] = current
                heapq.heappush(
                    frontier,
                    (
                        neighbor_cost + target.estimate_in(neighbor_context, neighbor),
                        next(insertion_order),
                        neighbor_cost,
                        neighbor_entry,
                    ),
                )
        return None

    def _is_reached(self, node: GrammarGraphNode) -> bool:
        """Compares node with the target. Raises once more than max_comparisons nodes were compared."""
        self.comparisons += 1
        if self.comparisons > self._max_comparisons:
            raise NavigatorTimedOutError(
                f"Couldn't find route to target NonTerminal after {self.comparisons} comparisons. "
                "Giving up. Does the grammar contain unbreakable cycles?"
            )
        return self._target.is_reached(node)

    @staticmethod
    def _path_to(
        entry: Entry, came_from: dict[Entry, Optional[Entry]]
    ) -> list[GrammarGraphNode]:
        """Returns the path from the start of the search to the node of entry, without the start."""
        path = []
        current = entry
        while (previous := came_from[current]) is not None:
            path.append(current[0])
            current = previous
        return list(reversed(path))
