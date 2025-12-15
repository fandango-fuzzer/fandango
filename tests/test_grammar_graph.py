import unittest

from fandango.api import Fandango
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.grammarnavigator import GrammarNavigator
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.language import NonTerminal, DerivationTree
from fandango.language.grammar import ParsingMode
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
        navigator = GrammarNavigator(grammar)
        tree = DerivationTree(NonTerminal("<start>"))
        path = navigator.astar_search_end(tree)
        path = filter(
            lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None,
            path,
        )
        path_symbols = map(lambda n: n.node.to_symbol(), path)
        path_symbols_list = list(path_symbols)
        self.assertEqual(
            path_symbols_list,
            [
                NonTerminal("<ping>"),
                NonTerminal("<pong>"),
                NonTerminal("<puff>"),
                NonTerminal("<paff>"),
            ],
        )

    def test_grammar_walk(self):
        grammar = self.get_grammar(RESOURCES_ROOT / "minimal_io.fan")
        tree_to_continue = grammar.parse(
            "ping\npong\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        navigator = GrammarNavigator(grammar)
        path = navigator.astar_tree(
            tree=tree_to_continue, destination_k_path=(NonTerminal("<paff>"),)
        )
        path = filter(
            lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None,
            path,
        )
        path = map(lambda n: n.node.symbol, path)
        path = list(path)
        self.assertEqual(path, [NonTerminal("<puff>"), NonTerminal("<paff>")])

    def test_packet_navigator(self):
        grammar = self.get_grammar(DOCS_ROOT / "smtp-extended.fan")
        navigator = PacketNavigator(grammar, NonTerminal("<start>"))
        tree_to_continue = grammar.parse(
            "220 abc ESMTP Postfix\r\nHELO abc\r\n",
            mode=ParsingMode.INCOMPLETE,
            include_controlflow=True,
        )
        packet_tree, _ = next(navigator.get_controlflow_tree(tree=tree_to_continue))
        path = navigator.astar_tree(
            tree=packet_tree, destination_k_path=(NonTerminal("<end_data>"),)
        )
        self.assertEqual(
            path,
            [
                PacketNonTerminal("StdOut", None, NonTerminal("<hello>")),
                NonTerminal("<mail_from>"),
                PacketNonTerminal("StdOut", None, NonTerminal("<MAIL_FROM>")),
                PacketNonTerminal("StdOut", None, NonTerminal("<ok>")),
                NonTerminal("<mail_to>"),
                PacketNonTerminal("StdOut", None, NonTerminal("<RCPT_TO>")),
                PacketNonTerminal("StdOut", None, NonTerminal("<ok>")),
                NonTerminal("<data>"),
                PacketNonTerminal("StdOut", None, NonTerminal("<DATA>")),
                PacketNonTerminal("StdOut", None, NonTerminal("<end_data>")),
            ],
        )

    def test_packet_navigator_symbol_not_reachable(self):
        grammar = self.get_grammar(DOCS_ROOT / "smtp-extended.fan")
        navigator = PacketNavigator(grammar, NonTerminal("<start>"))
        tree_to_continue = grammar.parse(
            "220 abc ESMTP Postfix\r\nHELO abc\r\n",
            mode=ParsingMode.INCOMPLETE,
            include_controlflow=True,
        )
        packet_tree, _ = next(navigator.get_controlflow_tree(tree=tree_to_continue))
        path = navigator.astar_tree(
            tree=packet_tree, destination_k_path=(NonTerminal("<helo>"),)
        )
        assert path is not None
        if None not in path:
            self.assertFalse("Expected symbol to be not reachable")
