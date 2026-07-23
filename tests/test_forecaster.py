from fandango.api import Fandango
from fandango.io.navigation.graph.packetforecaster import (
    ForecastingResult,
    PacketForecaster,
)
from fandango.language.grammar import ParsingMode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from tests.utils import RESOURCES_ROOT


def get_grammar(name: str="forecaster.fan"):
    with open(RESOURCES_ROOT / name) as f:
        spec = f.read()
    fandango = Fandango(spec, use_stdlib=False, use_cache=False)
    return fandango.grammar


def assert_prediction(prediction, expected: dict[str, list[str]]):
    assert len(prediction.get_msg_parties()) == len(expected)
    for role, nonterminals in expected.items():
        assert role in prediction
        assert len(nonterminals) == len(
            prediction.parties_to_packets[role].nt_to_packet
        )
        for nt in nonterminals:
            assert NonTerminal(nt) in prediction.parties_to_packets[role].nt_to_packet


def test_forecast_1():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = DerivationTree(NonTerminal("<start>"))
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<d>", "<e>", "<c>"]}
    assert_prediction(prediction, expected)


def test_forecast_2():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("d", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<e>", "<c>"]}
    assert_prediction(prediction, expected)


def test_forecast_3():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("de", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<e>", "<c>"]}
    assert_prediction(prediction, expected)


def test_forecast_4():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dec", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<c>", "<g>", "<i>"]}
    assert_prediction(prediction, expected)


def test_forecast_5():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dc", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<c>", "<g>", "<i>"]}
    assert_prediction(prediction, expected)


def test_forecast_6():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dcc", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<g>", "<i>"]}
    assert_prediction(prediction, expected)


def test_forecast_7():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dccg", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected: dict[str, list[str]] = {}
    assert_prediction(prediction, expected)


def test_forecast_8():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dcci", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected: dict[str, list[str]] = {}
    assert_prediction(prediction, expected)

def test_forecast_parallel():
    grammar = get_grammar(name="parallel_io.fan")
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("HELLO\n", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected: dict[str, list[str]] = {"Client": ["<put>", "<ping>"]}
    assert_prediction(prediction, expected)
    tree = grammar.parse("HELLO\nPUT report.txt\n", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"Server": ["<stored>"], "Client": ["<ping>"]}
    assert_prediction(prediction, expected)
    tree = grammar.parse("HELLO\nPUT report.txt\nPING\n", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"Server": ["<stored>", "<pong>"]}
    assert_prediction(prediction, expected)
    tree = grammar.parse("HELLO\nPUT report.txt\nSTORED report.txt\nPING\nPONG\n", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"Client": ["<commit>"]}
    assert_prediction(prediction, expected)
    tree = grammar.parse("HELLO\nPUT report.txt\nSTORED report.txt\nCOMMIT report.txt\nCOMMITTED report.txt\nPING\nPONG\n", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {"Client": ["<join>"]}
    assert_prediction(prediction, expected)
    tree = grammar.parse("HELLO\nPUT report.txt\nSTORED report.txt\nCOMMIT report.txt\nCOMMITTED report.txt\nPING\nPONG\nJOIN\n", mode=ParsingMode.INCOMPLETE)
    assert tree is not None
    prediction: ForecastingResult = forecaster.predict(tree)
    expected = {}
    assert_prediction(prediction, expected)
    assert len(prediction.complete_trees) != 0

