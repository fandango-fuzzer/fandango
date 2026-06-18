import unittest
from typing import TypeGuard

from fandango.api import Fandango
from fandango.io.navigation.grammarnavigator import GrammarNavigator
from fandango.io.navigation.packetnavigator import PacketNavigator
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.reachability_checker import ReachabilityChecker
from fandango.io.navigation.stategrammarconverter import StateGrammarConverter
from fandango.language import DerivationTree, NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.grammar import KPath, Grammar
from fandango.language.grammar.node_visitors.grammar_graph_converter import (
    GrammarGraphNode,
)
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.parse.parse import parse
from tests.utils import DOCS_ROOT, EVALUATION_ROOT, RESOURCES_ROOT


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

        def _is_valid_sender_node(
            n: GrammarGraphNode | None,
        ) -> TypeGuard[GrammarGraphNode]:
            return (
                n is not None
                and isinstance(n.node, NonTerminalNode)
                and n.node.sender is not None
            )

        path = navigator.astar_tree(
            tree=tree_to_continue, destination_k_path=(NonTerminal("<paff>"),)
        )

        path_iter: list[GrammarGraphNode | None] = path or []

        path_filtered: list[GrammarGraphNode] = list(
            filter(_is_valid_sender_node, path_iter)
        )

        path_list = [n.node.to_symbol() for n in path_filtered]
        self.assertEqual(path_list, [NonTerminal("<puff>"), NonTerminal("<paff>")])

    def test_packet_navigator(self):
        grammar = self.get_grammar(DOCS_ROOT / "smtp-extended.fan")
        navigator = PacketNavigator(grammar, NonTerminal("<start>"))
        tree_to_continue = grammar.parse(
            "220 abc ESMTP Postfix\r\nHELO abc\r\n",
            mode=ParsingMode.INCOMPLETE,
            include_controlflow=True,
        )
        packet_tree, _ = next(navigator.get_controlflow_tree(tree=tree_to_continue))
        path = navigator.astar_tree_symbols(
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
        path = navigator.astar_tree_symbols(
            tree=packet_tree, destination_k_path=(NonTerminal("<helo>"),)
        )
        assert path is not None
        if None not in path:
            self.assertFalse("Expected symbol to be not reachable")

    def test_packet_navigator_symbol_not_extensible(self):
        grammar = self.get_grammar(RESOURCES_ROOT / "navigation_io.fan")
        checker = ReachabilityChecker(grammar)

        tree_to_continue = grammar.parse(
            "a",
            mode=ParsingMode.INCOMPLETE,
            include_controlflow=True,
        )
        k_path: KPath = (
            NonTerminal("<start>"),
            NonTerminal("<test>"),
            NonTerminal("<state_4>"),
        )
        result_1 = checker.find_reachability(
            k_path_to_reach=k_path, tree=tree_to_continue
        )
        self.assertTrue(result_1.path_reachable)
        self.assertTrue(result_1.completable_by_extension)

        tree_to_continue = grammar.parse(
            "ac",
            mode=ParsingMode.INCOMPLETE,
            include_controlflow=True,
        )
        k_path = (
            NonTerminal("<start>"),
            NonTerminal("<test>"),
            NonTerminal("<state_4>"),
        )
        result_1 = checker.find_reachability(
            k_path_to_reach=k_path, tree=tree_to_continue
        )
        self.assertFalse(result_1.path_reachable)
        self.assertFalse(result_1.completable_by_extension)

        k_path = (
            NonTerminal("<start>"),
            NonTerminal("<test>"),
            NonTerminal("<H>"),
        )
        result_1 = checker.find_reachability(
            k_path_to_reach=k_path, tree=tree_to_continue
        )
        self.assertTrue(result_1.path_reachable)
        self.assertTrue(result_1.completable_by_extension)

        k_path = (
            NonTerminal("<start>"),
            NonTerminal("<test>"),
            NonTerminal("<G>"),
        )
        result_1 = checker.find_reachability(
            k_path_to_reach=k_path, tree=tree_to_continue
        )
        self.assertFalse(result_1.path_reachable)
        self.assertFalse(result_1.completable_by_extension)

        tree_to_continue = grammar.parse(
            "ad",
            mode=ParsingMode.INCOMPLETE,
            include_controlflow=True,
        )
        k_path = (
            NonTerminal("<start>"),
            NonTerminal("<test>"),
            NonTerminal("<state_4>"),
        )
        result_1 = checker.find_reachability(
            k_path_to_reach=k_path, tree=tree_to_continue
        )
        self.assertTrue(result_1.path_reachable)
        self.assertTrue(result_1.completable_by_extension)

        k_path = (
            NonTerminal("<start>"),
            NonTerminal("<test>"),
            NonTerminal("<G>"),
        )
        result_1 = checker.find_reachability(
            k_path_to_reach=k_path, tree=tree_to_continue
        )
        self.assertTrue(result_1.path_reachable)
        self.assertFalse(result_1.completable_by_extension)

    def test_smtp(self):
        packet_history = (
            "<response_setup><request_ehlo><response_ehlo><request_auth><response_auth_expect_user>"
            "<request_auth_user_correct><response_auth_expect_pass><request_auth_pass_incorrect>"
            "<response_auth_fail><request_auth><response_auth_expect_user><request_auth_user_incorrect>"
            "<response_auth_expect_pass><request_auth_pass_incorrect><response_auth_fail><request_auth>"
            "<response_auth_expect_user><request_auth_user_correct><response_auth_expect_pass>"
            "<request_auth_pass_correct><response_auth_success><request_mail_from><response_mail_from>"
        )
        dest_k_path = (
            NonTerminal("<exchange_login_valid>"),
            NonTerminal("<state_logged_in>"),
            NonTerminal("<state_logged_in>"),
            NonTerminal("<state_logged_in>"),
            NonTerminal("<state_logged_in>"),
        )
        client_def = """
class Client(FandangoParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT
        )

class Server(FandangoParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL
        )
        """

        with open(EVALUATION_ROOT / "protocol_testing_eval/smtp/smtp.fan") as f:
            grammar, constraints = parse(
                [f, client_def],
                use_stdlib=False,
            )
        assert grammar is not None
        reduced_rules = StateGrammarConverter(grammar.grammar_settings).process(
            grammar.rules, NonTerminal("<start>")
        )
        state_grammar = Grammar(
            grammar_settings=grammar.grammar_settings,
            rules=reduced_rules,
            fuzzing_mode=grammar.fuzzing_mode,
            local_variables=grammar._local_variables,
            global_variables=grammar._global_variables,
        )
        checker = ReachabilityChecker(state_grammar)
        hist_tree = state_grammar.parse(
            word=packet_history, mode=ParsingMode.INCOMPLETE, include_controlflow=True
        )
        assert hist_tree is not None

        result = checker.find_reachability(k_path_to_reach=dest_k_path, tree=hist_tree)
        self.assertTrue(result.path_reachable)
        self.assertTrue(result.completable_by_extension)

        navigator = PacketNavigator(grammar, NonTerminal("<start>"))
        path = navigator.astar_tree_symbols(
            tree=hist_tree, destination_k_path=dest_k_path
        )
        self.assertIsNotNone(path)
