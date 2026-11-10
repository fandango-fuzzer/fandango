import functools
from typing import Optional

import regex

from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Option, Plus, Repetition, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.parser.parse_state import (
    RuleAlternative,
    RuleSymbol,
)
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import TreeValueType

DraftAlternatives = list[list[RuleSymbol]]

#: The code points below 256 a word can begin with (None: any), and whether it can be empty
FirstCharacters = tuple[Optional[frozenset[int]], bool]


class GrammarCompiler(
    NodeVisitor[
        DraftAlternatives,
        DraftAlternatives,
    ]
):
    """
    Compiling a grammar into the rule tables the Earley parser works on.
    """

    def __init__(self, grammar_rules: dict[NonTerminal, Node]):
        self.grammar_rules: dict[NonTerminal, Node] = grammar_rules
        self._rules: dict[NonTerminal, set[RuleAlternative]] = {}
        self._implicit_rules: dict[NonTerminal, set[RuleAlternative]] = {}
        self._draft_implicit_rules: dict[NonTerminal, DraftAlternatives] = {}
        self._context_rules: dict[NonTerminal, tuple[Node, RuleSymbol]] = dict()
        self._tmp_rules: dict[NonTerminal, set[RuleAlternative]] = {}
        #: Control-flow nodes by the name of the symbol standing in for them.
        self._nodes: dict[str, Node] = {}
        self._columns_per_byte_cache: dict[NonTerminal, int] = {}
        self._first_characters: dict[NonTerminal, FirstCharacters] = {}
        self._rule_alternatives_by_lookahead: dict[
            tuple[NonTerminal, int], set[RuleAlternative]
        ] = {}
        self._process()

    def compile_bounded_repetition(
        self,
        node: Repetition,
        rule_symbol: RuleSymbol,
        tree: DerivationTree,
    ) -> RuleSymbol:
        """
        Recompile a repetition whose bounds depend on the context of the already parsed tree.
        """
        [[symbol]] = self.visitRepetition(node, rule_symbol, tree)
        return symbol

    def _process(self) -> None:
        self._rules.clear()
        self._implicit_rules.clear()
        self._draft_implicit_rules.clear()
        self._context_rules.clear()
        for nonterminal in self.grammar_rules:
            self.set_rule(nonterminal, self.visit(self.grammar_rules[nonterminal]))

        for nonterminal, alternatives in self._draft_implicit_rules.items():
            self._implicit_rules[nonterminal] = {tuple(a) for a in alternatives}
        self._draft_implicit_rules.clear()
        self._first_characters = self._compute_first_characters(
            {**self._implicit_rules, **self._rules}
        )

    def set_rule(self, nonterminal: NonTerminal, rule: DraftAlternatives) -> None:
        self._rules[nonterminal] = {tuple(a) for a in rule}

    def set_implicit_rule(self, rule: DraftAlternatives) -> RuleSymbol:
        nonterminal = NonTerminal(f"<*{len(self._draft_implicit_rules)}*>")
        self._draft_implicit_rules[nonterminal] = rule
        return (nonterminal, frozenset())

    def set_context_rule(self, node: Node, rule_symbol: RuleSymbol) -> NonTerminal:
        nonterminal = NonTerminal(f"<*ctx_{len(self._context_rules)}*>")
        self._context_rules[nonterminal] = (node, rule_symbol)
        return nonterminal

    def set_tmp_rule(self, rule: DraftAlternatives) -> RuleSymbol:
        nonterminal = NonTerminal(f"<*tmp_{len(self._tmp_rules)}*>")
        self._tmp_rules[nonterminal] = {tuple(a) for a in rule}
        return (nonterminal, frozenset())

    def _clear_tmp(self) -> None:
        self._tmp_rules.clear()

    def context_rule(
        self, nonterminal: NonTerminal
    ) -> Optional[tuple[Node, RuleSymbol]]:
        """The repetition and its element if `nonterminal` stands for one whose bounds depend on the parsed tree."""
        return self._context_rules.get(nonterminal)

    def has_context_rules(self) -> bool:
        return len(self._context_rules) != 0

    def rule_alternatives(
        self, nonterminal: NonTerminal, lookahead: Optional[int]
    ) -> Optional[set[RuleAlternative]]:
        """
        The alternatives of the rule of `nonterminal`, or None if it has none
        (a context rule). With `lookahead`, a code point below 256 as the next
        character, only those a parse can take: those that can begin with it
        or be empty.
        """
        rule = self._rules.get(nonterminal)
        if rule is None:
            rule = self._implicit_rules.get(nonterminal)
        if rule is None:
            # Temporary rules are compiled while parsing, without first characters
            return self._tmp_rules.get(nonterminal)
        if lookahead is None:
            return rule
        key = (nonterminal, lookahead)
        if key not in self._rule_alternatives_by_lookahead:
            alternatives = set()
            for alternative in rule:
                characters, can_be_empty = self._rule_alternative_first_characters(
                    alternative, self._first_characters
                )
                if can_be_empty or characters is None or lookahead in characters:
                    alternatives.add(alternative)
            self._rule_alternatives_by_lookahead[key] = alternatives
        return self._rule_alternatives_by_lookahead[key]

    def default_result(self) -> DraftAlternatives:
        return []

    def aggregate_results(
        self,
        aggregate: DraftAlternatives,
        result: DraftAlternatives,
    ) -> DraftAlternatives:
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result = self.visitChildren(node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitConcatenation(self, node: Concatenation) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: DraftAlternatives = [[]]
        for child in node.children():
            to_add = self.visit(child)
            new_result = []
            for r in result:
                for a in to_add:
                    new_result.append(r + a)
            result = new_result
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitRepetition(
        self,
        node: Repetition,
        element: Optional[RuleSymbol] = None,
        tree: Optional[DerivationTree] = None,
    ) -> DraftAlternatives:
        repetition_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[repetition_nt.name()] = node
        is_context = node.bounds_constraint is not None

        if element is None:
            alternatives = self.visit(node.node)
            element = self.set_implicit_rule(alternatives)

            if is_context:
                context_nt = self.set_context_rule(node, element)
                self.set_rule(repetition_nt, [[(context_nt, frozenset())]])
                return [[(repetition_nt, frozenset())]]

        more = None
        if node.bounds_constraint is not None:
            assert tree is not None
            rightmost_leaf = tree
            while len(rightmost_leaf.children) != 0:
                rightmost_leaf = rightmost_leaf.children[-1]
            node_min, _ = node.bounds_constraint.min(rightmost_leaf)
            node_max, _ = node.bounds_constraint.max(rightmost_leaf)
        else:
            node_min = node.min
            node_max = node.max
        for _rep in range(node_min, node_max):
            alts = [[element]]
            if more is not None:
                alts.append([element, more])
            if is_context:
                more = self.set_tmp_rule(alts)
            else:
                more = self.set_implicit_rule(alts)
        alts = [node_min * [element]]
        if more is not None:
            alts.append(node_min * [element] + [more])
        if is_context:
            return [[self.set_tmp_rule(alts)]]
        min_symbol = self.set_implicit_rule(alts)
        self.set_rule(repetition_nt, [[min_symbol]])
        return [[(repetition_nt, frozenset())]]

    def visitStar(self, node: Star) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: DraftAlternatives = [[]]
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitPlus(self, node: Plus) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        alternatives: DraftAlternatives = []
        nt = self.set_implicit_rule(alternatives)
        for r in self.visit(node.node):
            alternatives.append(r)
            alternatives.append(r + [nt])
        result = [[nt]]
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitOption(self, node: Option) -> DraftAlternatives:
        intermediate_nt = NonTerminal(f"<__{node.id}>")
        self._nodes[intermediate_nt.name()] = node
        result: DraftAlternatives = [[]] + self.visit(node.node)
        self.set_rule(intermediate_nt, result)
        return [[(intermediate_nt, frozenset())]]

    def visitNonTerminalNode(self, node: NonTerminalNode) -> DraftAlternatives:
        params = dict()
        if node.sender is not None:
            params["sender"] = node.sender
        if node.recipient is not None:
            params["recipient"] = node.recipient
        parameters = frozenset(params.items())
        return [[(node.symbol, parameters)]]

    def visitTerminalNode(self, node: TerminalNode) -> DraftAlternatives:
        return [[(node.symbol, frozenset())]]

    def columns_per_byte_for(self, start: NonTerminal) -> int:
        """
        8 if any binary terminal is reachable from `start`, else 1.
        """
        cached = self._columns_per_byte_cache.get(start)
        if cached is not None:
            return cached

        result = 1
        seen: set[NonTerminal] = set()
        stack: list[NonTerminal] = [start]
        while stack:
            nonterminal = stack.pop()
            if nonterminal in seen:
                continue
            seen.add(nonterminal)

            alternatives = self._rules.get(nonterminal)
            if alternatives is None:
                alternatives = self._implicit_rules.get(nonterminal)
            if alternatives is None:
                context = self._context_rules.get(nonterminal)
                if context is not None:
                    inner = context[1][0]
                    if isinstance(inner, NonTerminal):
                        stack.append(inner)
                    continue
                result = 8
                break

            for alternative in alternatives:
                for rule_symbol in alternative:
                    symbol = rule_symbol[0]
                    if symbol.is_terminal:
                        if symbol.is_type(TreeValueType.TRAILING_BITS_ONLY):
                            result = 8
                            stack.clear()
                            break
                    elif isinstance(symbol, NonTerminal):
                        stack.append(symbol)
                if result == 8:
                    break
            if result == 8:
                break

        self._columns_per_byte_cache[start] = result
        return result

    def _compute_first_characters(
        self,
        rules: dict[NonTerminal, set[RuleAlternative]],
    ) -> dict[NonTerminal, FirstCharacters]:
        """The first characters of every rule, grown until no rule changes any more."""
        first: dict[NonTerminal, FirstCharacters] = {
            nonterminal: (frozenset(), False) for nonterminal in rules
        }
        changed = True
        while changed:
            changed = False
            for nonterminal, alternatives in rules.items():
                of_alternatives = [
                    GrammarCompiler._rule_alternative_first_characters(a, first)
                    for a in alternatives
                ]
                characters = (
                    None
                    if any(c is None for c, _ in of_alternatives)
                    else frozenset().union(
                        *(c for c, _ in of_alternatives if c is not None)
                    )
                )
                result = (characters, any(empty for _, empty in of_alternatives))
                if result != first[nonterminal]:
                    first[nonterminal] = result
                    changed = True
        return first

    @staticmethod
    @functools.cache
    def _terminal_first_characters(terminal: Terminal) -> FirstCharacters:
        if terminal.is_type(TreeValueType.TRAILING_BITS_ONLY):
            return None, False
        text = terminal.value().to_string()
        if not terminal.is_regex:
            return (frozenset({ord(text[0])}), False) if text else (frozenset(), True)
        pattern = regex.compile(text)  # type: ignore[no-untyped-call]
        first = frozenset(
            c for c in range(256) if pattern.fullmatch(chr(c), partial=True)
        )
        empty = pattern.fullmatch("", partial=True)
        return first, empty is not None and not empty.partial

    @staticmethod
    def _rule_alternative_first_characters(
        alternative: RuleAlternative, first: dict[NonTerminal, FirstCharacters]
    ) -> FirstCharacters:
        characters: Optional[frozenset[int]] = frozenset()
        for symbol, _ in alternative:
            if isinstance(symbol, Terminal):
                symbol_characters, can_be_empty = (
                    GrammarCompiler._terminal_first_characters(symbol)
                )
            else:
                assert isinstance(symbol, NonTerminal)
                # Context and temporary rules are compiled while parsing: anything
                symbol_characters, can_be_empty = first.get(symbol, (None, True))
            if characters is None or symbol_characters is None:
                characters = None
            else:
                characters |= symbol_characters
            if not can_be_empty:
                return characters, False
        return characters, True
