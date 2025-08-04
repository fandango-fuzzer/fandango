import unittest

from fandango.api import Fandango
from fandango.io.navigation.grammarnavigator import GrammarNavigator
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.language import NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphConverter,
)
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from tests.utils import RESOURCES_ROOT, DOCS_ROOT


class TestGrammarGraph(unittest.TestCase):
    def get_grammar(self, path):
        with open(path) as f:
            spec = f.read()
        fandango = Fandango(spec, use_stdlib=True, use_cache=False)
        return fandango.grammar

    def test_graph_navigator(self):
        grammar = self.get_grammar(RESOURCES_ROOT / "minimal_io.fan")
        converter = GrammarGraphConverter(grammar.rules, NonTerminal("<start>"))
        graph = converter.process()
        navigator = GrammarNavigator(graph)
        start_node = graph.start.reaches[0]
        goal_node = (
            graph.start.reaches[0]
            .reaches[0]
            .reaches[0]
            .reaches[0]
            .reaches[0]
            .reaches[0]
            .reaches[0]
        )
        path = navigator.astar(start_node, goal_node)
        path = filter(
            lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None,
            path,
        )
        path = map(lambda n: n.node.symbol, path)
        path = list(path)
        self.assertEqual(path, [NonTerminal('<ping>'), NonTerminal('<pong>'), NonTerminal('<puff>')])

    def test_grammar_walk(self):
        grammar = self.get_grammar(RESOURCES_ROOT / "minimal_io.fan")
        tree_to_continue = grammar.parse(
            "ping\npong\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        navigator = GrammarNavigator(grammar)
        path = navigator.astar_tree(tree_to_continue, NonTerminal("<paff>"))
        path = filter(
            lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None,
            path,
        )
        path = map(lambda n: n.node.symbol, path)
        path = list(path)
        self.assertEqual(path, [NonTerminal('<puff>'), NonTerminal('<paff>')])

    def test_packet_navigator(self):
        grammar = self.get_grammar(DOCS_ROOT / "smtp-extended.fan")
        navigator = PacketNavigator(grammar, NonTerminal("<start>"))
        tree_to_continue = grammar.parse(
            "220 abc ESMTP Postfix\r\nHELO abc\r\n",
            mode=ParsingMode.INCOMPLETE,
            include_controlflow=True,
        )
        path = navigator.astar_tree(tree_to_continue, NonTerminal("<end_data>"))
        self.assertEqual(
            path,
            [
                NonTerminal("<hello>"),
                NonTerminal("<MAIL_FROM>"),
                NonTerminal("<ok>"),
                NonTerminal("<RCPT_TO>"),
                NonTerminal("<ok>"),
                NonTerminal("<DATA>"),
                NonTerminal("<end_data>"),
            ],
        )
