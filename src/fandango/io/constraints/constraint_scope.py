import enum
from typing import Optional

from fandango.constraints.base import GeneticBase
from fandango.constraints.comparison import ComparisonConstraint
from fandango.constraints.constraint import Constraint
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.exists import ExistsConstraint
from fandango.constraints.expression import ExpressionConstraint
from fandango.constraints.forall import ForallConstraint
from fandango.constraints.repetition_bounds import RepetitionBoundsConstraint
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.search import NonTerminalSearch
from fandango.language.symbols import NonTerminal


class ConstraintScope(enum.Enum):
    INSIDE = enum.auto()
    CROSSING = enum.auto()
    UNRELATED = enum.auto()


class _AccessPointCollector(ConstraintVisitor):
    def __init__(self, repetition_owners: dict[str, NonTerminal]):
        super().__init__()
        self._repetition_owners = repetition_owners
        self.symbols: Optional[set[NonTerminal]] = set()

    def do_continue(self, constraint: Constraint) -> bool:
        return not isinstance(constraint, (ForallConstraint, ExistsConstraint))

    def visit_expression_constraint(self, constraint: ExpressionConstraint) -> None:
        self._add_access_point(constraint.get_access_points(include_base=True))

    def visit_comparison_constraint(self, constraint: ComparisonConstraint) -> None:
        self._add_access_point(constraint.get_access_points(include_base=True))

    def visit_forall_constraint(self, constraint: ForallConstraint) -> None:
        self._visit_quantifier(
            constraint.bound, constraint.search, constraint.statement
        )

    def visit_exists_constraint(self, constraint: ExistsConstraint) -> None:
        self._visit_quantifier(
            constraint.bound, constraint.search, constraint.statement
        )

    def visit_conjunction_constraint(self, constraint: GeneticBase) -> None:
        pass

    def visit_disjunction_constraint(self, constraint: GeneticBase) -> None:
        pass

    def visit_implication_constraint(self, constraint: GeneticBase) -> None:
        pass

    def visit_repetition_bounds_constraint(
        self, constraint: RepetitionBoundsConstraint
    ) -> None:
        owner = self._repetition_owners.get(constraint.repetition_id)
        if owner is None:
            self.symbols = None
            return
        self._add_access_point([owner])
        for search in (constraint.search_min, constraint.search_max):
            if search is not None:
                self._add_access_point(search.get_access_points(include_base=True))

    def _visit_quantifier(
        self,
        bound: NonTerminal | str,
        search: NonTerminalSearch,
        statement: Constraint,
    ) -> None:
        self._add_access_point(search.get_access_points(include_base=True))
        # The statement reads the bound variable from the scope, not the tree.
        inner = _AccessPointCollector(self._repetition_owners)
        inner.visit(statement)
        if inner.symbols is None:
            self.symbols = None
            return
        if isinstance(bound, NonTerminal):
            inner.symbols.discard(bound)
        self._add_access_point(inner.symbols)

    def _add_access_point(self, symbols: list[NonTerminal] | set[NonTerminal]) -> None:
        if self.symbols is not None:
            self.symbols.update(symbols)


class ConstraintScopeAnalyzer:
    def __init__(self, grammar: Grammar):
        self._children: dict[NonTerminal, set[NonTerminal]] = {}
        self._repetition_owners: dict[str, NonTerminal] = {}
        for symbol, body in grammar.rules.items():
            children: set[NonTerminal] = set()
            pending: list[Node] = [body]
            while pending:
                node = pending.pop()
                if isinstance(node, NonTerminalNode):
                    children.add(node.symbol)
                    continue
                if isinstance(node, Repetition):
                    self._repetition_owners[node.id] = symbol
                pending.extend(node.children())
            if symbol in grammar.generators:
                children |= grammar.generator_dependencies(symbol)
            self._children[symbol] = children
        self._parents: dict[NonTerminal, set[NonTerminal]] = {}
        for symbol, children in self._children.items():
            for child in children:
                self._parents.setdefault(child, set()).add(symbol)
        self._access_points: dict[Constraint, Optional[frozenset[NonTerminal]]] = {}
        self._inside_and_above: dict[
            NonTerminal, tuple[set[NonTerminal], set[NonTerminal]]
        ] = {}

    def scope(
        self, non_terminal: NonTerminal, constraint: Constraint
    ) -> ConstraintScope:
        """Returns where the constraint reads the tree, relative to messages of the type."""
        access_points = self._access_points_of(constraint)
        symbols_going_down, symbols_going_up = self._inside_and_above_of(non_terminal)

        if not access_points or access_points.intersection(symbols_going_up):
            return ConstraintScope.CROSSING
        if access_points <= symbols_going_down:
            return ConstraintScope.INSIDE
        if access_points.intersection(symbols_going_down):
            return ConstraintScope.CROSSING
        return ConstraintScope.UNRELATED

    def _access_points_of(
        self, constraint: Constraint
    ) -> Optional[frozenset[NonTerminal]]:
        if constraint not in self._access_points:
            collector = _AccessPointCollector(self._repetition_owners)
            collector.visit(constraint)
            self._access_points[constraint] = (
                None if collector.symbols is None else frozenset(collector.symbols)
            )
        return self._access_points[constraint]

    def _inside_and_above_of(
        self, non_terminal: NonTerminal
    ) -> tuple[set[NonTerminal], set[NonTerminal]]:
        if non_terminal not in self._inside_and_above:
            self._inside_and_above[non_terminal] = (
                # (Other) NonTerminals non_terminal reaches (going down)
                self._reachable(non_terminal, self._children),
                # (Other) NonTerminals that reach non_terminal (going up)
                self._reachable(non_terminal, self._parents) - {non_terminal},
            )
        return self._inside_and_above[non_terminal]

    @staticmethod
    def _reachable(
        non_terminal: NonTerminal, edges: dict[NonTerminal, set[NonTerminal]]
    ) -> set[NonTerminal]:
        reachable = {non_terminal}
        pending = [non_terminal]
        while pending:
            for neighbor in edges.get(pending.pop(), ()):
                if neighbor not in reachable:
                    reachable.add(neighbor)
                    pending.append(neighbor)
        return reachable
