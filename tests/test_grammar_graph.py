from fandango.api import Fandango
from fandango.io.navigation.grammarnavigator import GrammarNavigator
from fandango.language import NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.node_visitors.grammar_graph_converter import GrammarGraphConverter
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from tests.utils import RESOURCES_ROOT, DOCS_ROOT


def get_grammar(path):
    with open(path) as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=True, use_cache=False)
    return fandango.grammar


def test_graph_1():
    grammar = get_grammar(RESOURCES_ROOT / "minimal_io.fan")
    converter = GrammarGraphConverter(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    navigator = GrammarNavigator(graph)
    start_node = graph.start.reaches[0].reaches[0].reaches[0]
    goal_node = graph.start.reaches[0].reaches[0].reaches[0].reaches[0].reaches[0].reaches[0].reaches[0]
    path = navigator.astar(start_node, goal_node)
    path = filter(lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None, path)
    path = map(lambda n: n.node.symbol, path)
    path = list(path)
    print(path)


def test_graph_2():
    grammar = get_grammar(RESOURCES_ROOT / "minimal_io.fan")
    converter = GrammarGraphConverter(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    tree_to_continue = grammar.parse("ping\npong\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True)
    navigator = GrammarNavigator(graph)
    path = navigator.astar_tree(tree_to_continue, NonTerminal("<paff>"))
    path = filter(lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None, path)
    path = map(lambda n: n.node.symbol, path)
    path = list(path)
    print(path)

def test_graph_3():
    grammar = get_grammar(DOCS_ROOT / "smtp-extended.fan")
    converter = GrammarGraphConverter(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    tree_to_continue = grammar.parse("220 abc ESMTP Postfix\r\nHELO abc\r\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True)
    navigator = GrammarNavigator(graph)
    navigator.set_message_cost(1)
    path = navigator.astar_tree(tree_to_continue, NonTerminal("<end_data>"))
    path = filter(lambda n: isinstance(n.node, (NonTerminalNode, TerminalNode)), path)
    path = map(lambda n: n.node.symbol, path)
    path = list(path)
    print(path)