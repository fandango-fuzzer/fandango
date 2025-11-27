from collections.abc import Sequence
from fandango.errors import FandangoValueError
from fandango.language import NonTerminal, Terminal, Symbol
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Option, Plus, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.tree_value import TreeValueType


class StateGrammarConverter(NodeVisitor):
    """
    Converts a grammar into a reduced form, where all protocol message defining NonTerminalNodes are replaced with
    a TerminalNode that describes the protocol message type.
    Message defining NonTerminals are replaced with a Terminal, in the form of <_packet_<message_type>>.
    This allows the PacketForecaster to predict upcoming
    protocol messages without parsing each protocol message again.
    """

    def __init__(self, grammar_settings: Sequence[HasSettings]):
        self._grammar_settings = grammar_settings
        self._reduced: dict[NonTerminal, Node] = dict()
        self.seen_keys: set[NonTerminal] = set()
        self.processed_keys: set[NonTerminal] = set()

    @staticmethod
    def to_packet_non_terminal(symbol: Symbol) -> Symbol:
        if not isinstance(symbol, NonTerminal) or symbol.name().startswith("<_packet_"):
            return symbol
        return NonTerminal(f"<_packet_{symbol.name()[1:]}")

    @staticmethod
    def to_non_terminal(symbol: NonTerminal) -> NonTerminal:
        if symbol.name().startswith("<_packet_"):
            return NonTerminal(f"<{symbol.name()[9:]}")
        else:
            return NonTerminal(symbol.name())

    def process(
        self,
        rules: dict[NonTerminal, Node],
        start_symbol: NonTerminal = NonTerminal("<start>"),
    ) -> dict[NonTerminal, Node]:
        """
        Applies the grammar reduction to the provided grammar.
        """
        self._reduced = dict()
        self.seen_keys = set()
        self.seen_keys.add(start_symbol)
        self.processed_keys = set()
        diff_keys = self.seen_keys - self.processed_keys
        while len(diff_keys) != 0:
            key = diff_keys.pop()
            self._reduced[key] = self.visit(rules[key])
            self.processed_keys.add(key)
            diff_keys = self.seen_keys - self.processed_keys
        return self._reduced

    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.append(result)
        return aggregate

    def visitConcatenation(self, node: Concatenation):
        return Concatenation(
            self.visitChildren(node),
            self._grammar_settings,
            node.id,
        )

    def visitTerminalNode(self, node: TerminalNode):
        return TerminalNode(node.symbol, self._grammar_settings)

    def visitAlternative(self, node: Alternative):
        return Alternative(
            self.visitChildren(node),
            self._grammar_settings,
            node.id,
        )

    def visitRepetition(self, node: Repetition):
        repetition = Repetition(
            self.visit(node.node),
            self._grammar_settings,
            node.id,
            node.min,
            node.internal_max,
        )
        repetition.bounds_constraint = node.bounds_constraint
        return repetition

    def visitOption(self, node: Option):
        return Option(
            self.visit(node.node),
            self._grammar_settings,
            node.id,
        )

    def visitPlus(self, node: Plus):
        return Plus(self.visit(node.node), self._grammar_settings, node.id)

    def visitStar(self, node: Star):
        return Star(
            self.visit(node.node),
            self._grammar_settings,
            node.id,
        )

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.sender is None and node.recipient is None:
            self.seen_keys.add(node.symbol)
            return node

        if node.symbol.is_type(TreeValueType.STRING):
            symbol = NonTerminal("<_packet_" + node.symbol.name()[1:])
        else:
            raise FandangoValueError("NonTerminal symbol must be a string!")
        repl_node = NonTerminalNode(
            symbol,
            self._grammar_settings,
            node.sender,
            node.recipient,
        )
        self._reduced[symbol] = TerminalNode(
            Terminal(node.symbol.value()), self._grammar_settings
        )
        self.seen_keys.add(symbol)
        self.processed_keys.add(symbol)
        return repl_node
