from fandango.errors import FandangoValueError
from fandango.language import NonTerminal, Terminal, DerivationTree, Grammar
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Option, Plus, Star
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.grammar.parser.parser import Parser
from fandango.language.tree_value import TreeValueType


class RuleCompletionTester(NodeVisitor):

    def __init__(self, grammar: Grammar):
        self._grammar = grammar
        self._rule_grammars: dict[NonTerminal, Node] = dict()
        for key, rule in grammar.rules.items():
            self._rule_grammars[key] = self.visit(rule)
        self._parser = Parser(self._rule_grammars)

    def check_complete(self, tree: DerivationTree):
        if not isinstance(tree.symbol, NonTerminal):
            return True
        reduced_tree = DerivationTree(tree.symbol)
        for child in tree.children:
            if isinstance(child.symbol, Terminal):
                reduced_tree.add_child(DerivationTree(child.symbol))
            else:
                nt_symbol_dummy = NonTerminal("<_symbol_" + child.symbol.name()[1:])
                symbol_tree = DerivationTree(nt_symbol_dummy)
                symbol_tree.add_child(DerivationTree(Terminal(nt_symbol_dummy.name())))
                reduced_tree.add_child(symbol_tree)
        return self._parser.parse(word=reduced_tree, start=tree.symbol) is not None


    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.append(result)
        return aggregate

    def visitConcatenation(self, node: Concatenation):
        return Concatenation(
            self.visitChildren(node),
            self._grammar._grammar_settings,
            node.id,
        )

    def visitTerminalNode(self, node: TerminalNode):
        return TerminalNode(node.symbol, self._grammar._grammar_settings)

    def visitAlternative(self, node: Alternative):
        return Alternative(
            self.visitChildren(node),
            self._grammar._grammar_settings,
            node.id,
        )

    def visitRepetition(self, node: Repetition):
        repetition = Repetition(
            self.visit(node.node),
            self._grammar._grammar_settings,
            node.id,
            node.min,
            node.internal_max,
        )
        repetition.bounds_constraint = node.bounds_constraint
        return repetition

    def visitOption(self, node: Option):
        return Option(
            self.visit(node.node),
            self._grammar._grammar_settings,
            node.id,
        )

    def visitPlus(self, node: Plus):
        return Plus(self.visit(node.node), self._grammar._grammar_settings, node.id)

    def visitStar(self, node: Star):
        return Star(
            self.visit(node.node),
            self._grammar._grammar_settings,
            node.id,
        )

    def visitCharSet(self, node: CharSet):
        return CharSet(node.chars, self._grammar._grammar_settings)

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol.is_type(TreeValueType.STRING):
            symbol = NonTerminal("<_symbol_" + node.symbol.name()[1:])
        else:
            raise FandangoValueError("NonTerminal symbol must be a string!")
        repl_node = NonTerminalNode(
            symbol,
            self._grammar._grammar_settings,
            node.sender,
            node.recipient,
        )
        self._rule_grammars[symbol] = TerminalNode(
            Terminal(symbol.value()), self._grammar._grammar_settings
        )
        return repl_node
