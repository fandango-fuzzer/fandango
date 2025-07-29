from fandango.api import Fandango
from fandango.language import NonTerminal
from fandango.language.grammar.node_visitors.grammar_graph_converter import GrammarGraphConverterVisitor
from tests.utils import RESOURCES_ROOT


def get_grammar(path):
    with open(path) as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    return fandango.grammar


def test_forecast_1():
    grammar = get_grammar(RESOURCES_ROOT / "grammar.fan")
    converter = GrammarGraphConverterVisitor(grammar.rules, NonTerminal("<start>"))
    graph = converter.process()
    print(graph)