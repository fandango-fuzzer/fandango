from fandango.language.parse import parse


def test_can_parse_grammar_settings():
    raw_spec = """
<start> ::= "a"

setting <start> havoc_probability=0.5
"""
    grammar, constraints = parse(raw_spec, use_cache=False)
    assert grammar is not None
    assert constraints is not None
