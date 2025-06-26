from fandango import DerivationTree
from fandango.io.packetforecaster import PacketForecaster
from fandango.language import Grammar, NonTerminal
from tests.utils import RESOURCES_ROOT
from fandango.api import Fandango


def get_grammar():
    with open(RESOURCES_ROOT / "forecaster.fan") as f:
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
    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<d>", "<e>", "<c>"]}
    assert_prediction(prediction, expected)


def test_forecast_2():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("d", mode=Grammar.Parser.ParsingMode.INCOMPLETE)

    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<e>", "<c>"]}
    assert_prediction(prediction, expected)


def test_forecast_3():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("de", mode=Grammar.Parser.ParsingMode.INCOMPLETE)

    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<e>", "<c>"]}
    assert_prediction(prediction, expected)


def test_forecast_4():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dec", mode=Grammar.Parser.ParsingMode.INCOMPLETE)

    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<c>", "<g>", "<h>"]}
    assert_prediction(prediction, expected)


def test_forecast_5():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dc", mode=Grammar.Parser.ParsingMode.INCOMPLETE)

    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<c>", "<g>", "<h>"]}
    assert_prediction(prediction, expected)


def test_forecast_6():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dcc", mode=Grammar.Parser.ParsingMode.INCOMPLETE)

    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected = {"StdOut": ["<g>", "<h>"]}
    assert_prediction(prediction, expected)


def test_forecast_7():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dccg", mode=Grammar.Parser.ParsingMode.INCOMPLETE)

    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected: dict[str, list[str]] = {}
    assert_prediction(prediction, expected)


def test_forecast_8():
    grammar = get_grammar()
    forecaster = PacketForecaster(grammar)
    tree = grammar.parse("dcch", mode=Grammar.Parser.ParsingMode.INCOMPLETE)

    prediction: PacketForecaster.ForecastingResult = forecaster.predict(tree)
    expected: dict[str, list[str]] = {}
    assert_prediction(prediction, expected)
