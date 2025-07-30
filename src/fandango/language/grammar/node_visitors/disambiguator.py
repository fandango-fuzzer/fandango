from typing import TYPE_CHECKING
from collections.abc import Sequence
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Star, Plus, Option
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Terminal, Slice
from fandango.language.symbols.symbol import Symbol

if TYPE_CHECKING:
    import fandango


class Disambiguator(NodeVisitor):
    def __init__(
        self,
        grammar: "fandango.language.grammar.grammar.Grammar",
        grammar_settings: Sequence[HasSettings],
    ):
        self.known_disambiguations: dict[
            Node,
            dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]],
        ] = {}
        self.grammar = grammar
        self._grammar_settings = grammar_settings

    def visit(
        self, node: Node
    ) -> dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]]:
        if node in self.known_disambiguations:
            return self.known_disambiguations[node]
        result = super().visit(node)
        self.known_disambiguations[node] = result
        return result

    def visitAlternative(
        self, node: Alternative
    ) -> dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]]:
        child_endpoints: dict[
            tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]
        ] = {}
        for child in node.children():
            endpoints = self.visit(child)
            for children in endpoints:
                # prepend the alternative to all paths
                if children not in child_endpoints:
                    child_endpoints[children] = []
                # join observed paths (these are impossible to disambiguate)
                child_endpoints[children].extend(
                    (node,) + path for path in endpoints[children]
                )

        return child_endpoints

    def visitConcatenation(
        self, node: Concatenation
    ) -> dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]]:
        child_endpoints: dict[
            tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]
        ] = {(): []}
        for child in node.children():
            next_endpoints: dict[
                tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]
            ] = {}
            endpoints = self.visit(child)
            for children in endpoints:
                for existing in child_endpoints:
                    concatenation = existing + children
                    if concatenation not in next_endpoints:
                        next_endpoints[concatenation] = []
                    next_endpoints[concatenation].extend(child_endpoints[existing])
                    next_endpoints[concatenation].extend(endpoints[children])
            child_endpoints = next_endpoints

        return {
            children: [(node,) + path for path in child_endpoints[children]]
            for children in child_endpoints
        }

    def visitRepetition(
        self, node: Repetition
    ) -> dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]]:
        # repetitions are alternatives over concatenations
        implicit_alternative = next(node.descendents(self.grammar))
        return self.visit(implicit_alternative)

    def visitStar(
        self, node: Star
    ) -> dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitPlus(
        self, node: Plus
    ) -> dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitOption(
        self, node: Option
    ) -> dict[tuple[NonTerminal | Terminal | Slice, ...], list[tuple[Node, ...]]]:
        implicit_alternative = Alternative(
            [
                Concatenation([], self._grammar_settings),
                Concatenation([node.node], self._grammar_settings),
            ],
            self._grammar_settings,
        )
        return self.visit(implicit_alternative)

    def visitNonTerminalNode(
        self, node: NonTerminalNode
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitTerminalNode(
        self, node: TerminalNode
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitCharSet(
        self, node: CharSet
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return {
            (Terminal(c),): [(node, TerminalNode(Terminal(c), self._grammar_settings))]
            for c in node.chars
        }
