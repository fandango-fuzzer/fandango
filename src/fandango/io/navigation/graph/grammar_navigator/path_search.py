import heapq
import itertools
from abc import ABC, abstractmethod
from collections.abc import Callable, Hashable
from typing import Optional

from fandango.errors import FandangoError
from fandango.io.navigation.graph.grammar_navigator.grammar_graph_converter import (
    GrammarGraphNode,
)


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
        """Returns the cheapest path from start to a node that reaches the target, or None if there is none."""
        self.comparisons = 0
        if self._is_reached(start):
            return [start]
        target = self._target
        insertion_order = itertools.count()
        best_costs = {target.state(start): 0}
        came_from: dict[GrammarGraphNode, Optional[GrammarGraphNode]] = {start: None}
        closed: set[Hashable] = set()
        frontier = [(target.estimate(start), next(insertion_order), 0, start)]
        while frontier:
            _, _, cost, current = heapq.heappop(frontier)
            state = target.state(current)
            if state in closed or cost > best_costs[state]:
                continue
            if self._is_reached(current):
                return self._path_to(current, came_from)
            closed.add(state)
            for neighbor in current.reaches:
                neighbor_state = target.state(neighbor)
                if neighbor_state in closed:
                    continue
                neighbor_cost = cost + self._cost_of_entering(neighbor)
                if neighbor_cost >= best_costs.get(neighbor_state, neighbor_cost + 1):
                    continue
                best_costs[neighbor_state] = neighbor_cost
                came_from[neighbor] = current
                heapq.heappush(
                    frontier,
                    (
                        neighbor_cost + target.estimate(neighbor),
                        next(insertion_order),
                        neighbor_cost,
                        neighbor,
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
        node: GrammarGraphNode,
        came_from: dict[GrammarGraphNode, Optional[GrammarGraphNode]],
    ) -> list[GrammarGraphNode]:
        """Returns the path from the start of the search to node."""
        path = []
        current: Optional[GrammarGraphNode] = node
        while current is not None:
            path.append(current)
            current = came_from[current]
        return list(reversed(path))
