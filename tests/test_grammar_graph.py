from fandango.api import Fandango
from fandango.io.PacketNavigator import PacketNavigator
from fandango.language import NonTerminal
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.node_visitors.grammar_graph_converter import GrammarGraphConverterVisitor
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from tests.utils import RESOURCES_ROOT, DOCS_ROOT


def get_grammar(path):
    with open(path) as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    return fandango.grammar


def test_graph_1():
    grammar = get_grammar(RESOURCES_ROOT / "minimal_io.fan")
    converter = GrammarGraphConverterVisitor(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    navigator = PacketNavigator(graph)
    start_node = graph.start.reaches[0].reaches[0].reaches[0]
    goal_node = graph.start.reaches[0].reaches[0].reaches[0].reaches[0].reaches[0].reaches[0].reaches[0]
    path = navigator.astar(start_node, goal_node)
    path = filter(lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None, path)
    path = map(lambda n: n.node.symbol, path)
    path = list(path)
    print(path)


def test_graph_2():
    grammar = get_grammar(RESOURCES_ROOT / "minimal_io.fan")
    converter = GrammarGraphConverterVisitor(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    tree_to_continue = grammar.parse("ping\npong\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True)
    navigator = PacketNavigator(graph)
    path = navigator.astar_tree(tree_to_continue, NonTerminal("<paff>"))
    path = filter(lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None, path)
    path = map(lambda n: n.node.symbol, path)
    path = list(path)
    print(path)

def test_graph_3():
    grammar = get_grammar(DOCS_ROOT / "smtp_extended.fan")
    converter = GrammarGraphConverterVisitor(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    tree_to_continue = grammar.parse("ping\npong\n", mode=ParsingMode.INCOMPLETE, include_controlflow=True)
    navigator = PacketNavigator(graph)
    path = navigator.astar_tree(tree_to_continue, NonTerminal("<paff>"))
    path = filter(lambda n: isinstance(n.node, NonTerminalNode) and n.node.sender is not None, path)
    path = map(lambda n: n.node.symbol, path)
    path = list(path)
    print(path)