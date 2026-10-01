from collections.abc import Sequence
from typing import NamedTuple, Optional

from fandango.io.navigation.graph.rule_recursion_tester import RuleRecursionTester
from fandango.io.navigation.step import Step
from fandango.language.grammar.grammar import KPath
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol

BlockedPath = tuple[NonTerminal, ...]


class Pruned(NamedTuple):
    node: Optional[Node]
    removes_parent: bool = False


class BlockedStepPruner(NodeVisitor[list[Pruned], Pruned]):
    """
    Removes the blocked steps from a state grammar.
    """

    COPY_MARK = "#"

    @staticmethod
    def original(symbol: NonTerminal) -> NonTerminal:
        """The symbol of the state grammar that a copy or its control flow stands for."""
        name = symbol.name()
        if BlockedStepPruner.COPY_MARK not in name:
            return symbol
        return NonTerminal(name[: name.index(BlockedStepPruner.COPY_MARK)] + ">")

    def __init__(self, grammar_settings: Sequence[HasSettings]):
        self._grammar_settings = grammar_settings
        self._state_rules: dict[NonTerminal, Node] = {}
        self._blocked_paths: dict[NonTerminal, frozenset[BlockedPath]] = {}
        """Per rule of the pruned grammar, the paths from its body that are blocked."""
        self._copies: dict[tuple[NonTerminal, frozenset[BlockedPath]], NonTerminal] = {}
        self._pruned: dict[NonTerminal, Pruned] = {}
        """The rules pruned so far. A rule deriving nothing anymore has no node."""
        self._current_rule: Optional[NonTerminal] = None
        self._current_path: list[NonTerminal] = []
        self._made_up_ids: set[str] = set()

    def prune(
        self,
        state_rules: dict[NonTerminal, Node],
        start_symbol: NonTerminal,
        blocked_steps: frozenset[Step],
    ) -> dict[NonTerminal, Node]:
        self._state_rules = state_rules
        self._blocked_paths = {}
        for step in blocked_steps:
            self._blocked_paths[step.path[0]] = self._blocked_paths.get(
                step.path[0], frozenset()
            ).union([step.path[1:]])
        self._copies = {}
        self._pruned = {}
        self._made_up_ids = set()
        pending = set(self._blocked_paths)
        while pending:
            rule = pending.pop()
            self._pruned[rule] = self._prune_rule(rule)
            if self._pruned[rule].node is None:
                pending.update(self._referrers(rule))
        return self._reachable_rules(self._rules(), start_symbol)

    def _prune_rule(self, rule: NonTerminal) -> Pruned:
        """Always from the original body: blocked paths name its control-flow nodes."""
        saved = self._current_rule, self._current_path
        self._current_rule, self._current_path = rule, []
        body = self.visit(self._state_rules[self.original(rule)])
        self._current_rule, self._current_path = saved
        return body

    def _copy_of(
        self, symbol: NonTerminal, blocked_paths: frozenset[BlockedPath]
    ) -> NonTerminal:
        """The rule of symbol without the blocked paths, copied on first use."""
        copy = self._copies.get((symbol, blocked_paths))
        if copy is None:
            copy = NonTerminal(
                f"{symbol.name()[:-1]}{self.COPY_MARK}{len(self._copies) + 1}>"
            )
            self._copies[(symbol, blocked_paths)] = copy
            self._blocked_paths[copy] = blocked_paths
            self._pruned[copy] = self._prune_rule(copy)
        return copy

    def _id(self, node: Alternative | Concatenation | Repetition) -> str:
        """Copies get the mark in their control-flow ids too, since parsers key control flow by id."""
        assert self._current_rule is not None
        name = self._current_rule.name()
        if self.COPY_MARK not in name:
            return node.id
        return node.id + name[name.index(self.COPY_MARK) : -1]

    def _rules(self) -> dict[NonTerminal, Node]:
        rules = dict(self._state_rules)
        for symbol, pruned in self._pruned.items():
            if pruned.node is None:
                rules.pop(symbol, None)
            else:
                rules[symbol] = pruned.node
        return rules

    def _referrers(self, symbol: NonTerminal) -> set[NonTerminal]:
        return {
            rule
            for rule, body in self._rules().items()
            if symbol in RuleRecursionTester.referenced_symbols(body)
        }

    @staticmethod
    def _reachable_rules(
        rules: dict[NonTerminal, Node], start_symbol: NonTerminal
    ) -> dict[NonTerminal, Node]:
        reachable_symbols = {start_symbol}
        pending_symbols = [start_symbol]
        while pending_symbols:
            symbol = pending_symbols.pop()
            if symbol not in rules:
                continue
            for referenced in RuleRecursionTester.referenced_symbols(rules[symbol]):
                if referenced not in reachable_symbols:
                    reachable_symbols.add(referenced)
                    pending_symbols.append(referenced)
        return {
            symbol: body
            for symbol, body in rules.items()
            if symbol in reachable_symbols
        }

    def default_result(self) -> list[Pruned]:
        return []

    def aggregate_results(
        self, aggregate: list[Pruned], result: Pruned
    ) -> list[Pruned]:
        aggregate.append(result)
        return aggregate

    def visitNonTerminalNode(self, node: NonTerminalNode) -> Pruned:
        assert self._current_rule is not None
        path = (*self._current_path, node.symbol)
        blocked_paths = self._blocked_paths.get(self._current_rule, frozenset())
        if path in blocked_paths:
            return Pruned(None, removes_parent=True)
        symbol = node.symbol
        own_paths = self._blocked_paths.get(symbol, frozenset())
        paths = own_paths.union(
            blocked_path[len(path) :]
            for blocked_path in blocked_paths
            if blocked_path[: len(path)] == path
        )
        if paths != own_paths:
            symbol = self._copy_of(symbol, paths)
        pruned = self._pruned.get(symbol)
        if pruned is not None and pruned.node is None:
            return pruned
        if symbol == node.symbol:
            return Pruned(node)
        return Pruned(
            NonTerminalNode(symbol, self._grammar_settings, node.sender, node.recipient)
        )

    def visitTerminalNode(self, node: TerminalNode) -> Pruned:
        return Pruned(node)

    def visitCharSet(self, node: CharSet) -> Pruned:
        return Pruned(node)

    def _visit_children(
        self, node: Alternative | Concatenation | Repetition
    ) -> list[Pruned]:
        symbol = node.to_symbol()
        assert isinstance(symbol, NonTerminal)
        self._current_path.append(symbol)
        pruned_children = self.visitChildren(node)
        self._current_path.pop()
        return pruned_children

    def visitConcatenation(self, node: Concatenation) -> Pruned:
        nodes: list[Node] = []
        for pruned_child in self._visit_children(node):
            if pruned_child.removes_parent:
                return Pruned(None, removes_parent=True)
            if pruned_child.node is not None:
                nodes.append(pruned_child.node)
        if len(nodes) == 0:
            return Pruned(None, removes_parent=False)
        concatenation = Concatenation(nodes, self._grammar_settings, self._id(node))
        return Pruned(concatenation)

    def visitAlternative(self, node: Alternative) -> Pruned:
        alternatives: list[Node] = []
        may_derive_nothing = False
        for pruned_alternative in self._visit_children(node):
            if pruned_alternative.node is not None:
                alternatives.append(pruned_alternative.node)
            elif not pruned_alternative.removes_parent:
                may_derive_nothing = True
        if len(alternatives) == 0:
            return Pruned(None, removes_parent=not may_derive_nothing)
        node_id = self._id(node)
        remaining = Alternative(
            alternatives,
            self._grammar_settings,
            node_id,
            is_permutation=node.is_permutation,
        )
        if may_derive_nothing:
            option = Option(
                remaining, self._grammar_settings, f"{NodeType.OPTION}:{node_id}"
            )
            self._made_up_ids.add(option.id)
            return Pruned(option)
        return Pruned(remaining)

    def is_made_up(self, node: Node) -> bool:
        """True if the last prune made up the node. This node.id is not contained in the original grammar."""
        return isinstance(node, Option) and node.id in self._made_up_ids

    def visitRepetition(self, node: Repetition) -> Pruned:
        (body,) = self._visit_children(node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        repetition = Repetition(
            body.node,
            self._grammar_settings,
            self._id(node),
            node.min,
            node.internal_max,
        )
        repetition.bounds_constraint = node.bounds_constraint
        return Pruned(repetition)

    def visitOption(self, node: Option) -> Pruned:
        (body,) = self._visit_children(node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        option = Option(body.node, self._grammar_settings, self._id(node))
        return Pruned(option)

    def visitPlus(self, node: Plus) -> Pruned:
        (body,) = self._visit_children(node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        plus = Plus(body.node, self._grammar_settings, self._id(node))
        return Pruned(plus)

    def visitStar(self, node: Star) -> Pruned:
        (body,) = self._visit_children(node)
        if body.node is None:
            return self._repetition_without_body(node, body)
        star = Star(body.node, self._grammar_settings, self._id(node))
        return Pruned(star)

    @staticmethod
    def _repetition_without_body(node: Repetition, body: Pruned) -> Pruned:
        """A repetition whose body is gone is removed if it must repeat also propagate removals to parents."""
        return (
            Pruned(None, removes_parent=True)
            if body.removes_parent and node.min > 0
            else Pruned(None, removes_parent=False)
        )


class KPathTranslation:
    """Translates k-paths of the state grammar into those of the pruned grammar, which run through copies as well."""

    def __init__(self, pruned_rules: dict[NonTerminal, Node]):
        self._references: dict[Symbol, set[NonTerminal]] = {
            symbol: RuleRecursionTester.referenced_symbols(body)
            for symbol, body in pruned_rules.items()
        }
        self._instances: dict[Symbol, list[NonTerminal]] = {}
        for symbol in pruned_rules:
            self._instances.setdefault(BlockedStepPruner.original(symbol), []).append(
                symbol
            )
        self._translations: dict[KPath, list[KPath]] = {}

    def __repr__(self) -> str:
        copies = {
            str(original): [symbol.name() for symbol in instances]
            for original, instances in self._instances.items()
            if len(instances) > 1
        }
        return f"KPathTranslation({len(self._references)} rules, copies={copies})"

    def pruned_k_paths(self, k_path: KPath) -> list[KPath]:
        translation = self._translations.get(k_path)
        if translation is None:
            translation = [()]
            for original_symbol in k_path:
                translation = [
                    path + (symbol,)
                    for path in translation
                    for symbol in self._instances.get(original_symbol, ())
                    if len(path) == 0 or symbol in self._references[path[-1]]
                ]
            self._translations[k_path] = translation
        return translation
