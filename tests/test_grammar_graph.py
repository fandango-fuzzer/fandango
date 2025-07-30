from fandango.api import Fandango
from fandango.io.PacketNavigator import PacketNavigator
from fandango.language import NonTerminal
from fandango.language.grammar.node_visitors.grammar_graph_converter import GrammarGraphConverterVisitor
from tests.utils import RESOURCES_ROOT


def get_grammar(path):
    with open(path) as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    return fandango.grammar


def test_forecast_1():
    grammar = get_grammar(RESOURCES_ROOT / "minimal_io.fan")
    converter = GrammarGraphConverterVisitor(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    navigator = PacketNavigator(graph)
    start_node = graph.start
    goal_node = start_node.reaches[0].reaches[0].reaches[0].reaches[0].reaches[0].reaches[0].reaches[0]
    path = navigator.astar(start_node, goal_node)
    path = list(path)
    print(path)