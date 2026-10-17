"""
Differential tests: the Rust port of the Earley parser must behave exactly
like the Python parser (same tables, same derivations in the same order).
See `tests/rust_parser_differential.py` for what is compared.
"""

import random

import pytest

from fandango.language.grammar import ParsingMode
from fandango.language.grammar.parser.rust_iterative_parser import (
    rust_parser_available,
)
from fandango.language.parse.parse import parse

from .rust_parser_differential import (
    Scenario,
    compare,
    mutate,
    random_chunks,
    random_spec,
    random_words,
    scenarios_for,
    serialize,
    terminal_words,
)
from .utils import RESOURCES_ROOT

pytestmark = pytest.mark.skipif(
    not rust_parser_available(), reason="fandango_earley_rs is not built"
)

SPECS: dict[str, str] = {
    "node_types": """
<start> ::= <record>+
<record> ::= <key> '=' <value> <flags> ';'
<key> ::= r'[a-z]+'
<value> ::= <number> | <quoted> | <empty>
<number> ::= <digit>{1,4}
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<quoted> ::= '"' <char>* '"'
<char> ::= 'x' | 'y'
<empty> ::= ''
<flags> ::= <flag>?
<flag> ::= '!'
""",
    "ambiguous": "<start> ::= <e>\n<e> ::= <e> '+' <e> | '1'\n",
    "right_recursive": '<start> ::= <A>\n<A> ::= "a" <A> | "a"\n',
    "left_recursive": '<start> ::= <A>\n<A> ::= <A> "a" | "a"\n',
    "epsilon": """
<start> ::= <a> <b> <c>
<a> ::= <a> <a> | '' | 'x'
<b> ::= <c> <c> | ''
<c> ::= <b> | 'y' | ''
""",
    "nullable_chain": """
<start> ::= <x>* 'z'
<x> ::= <y> <y>
<y> ::= '' | 'a' | <x>
""",
    "regex": r"""
<start> ::= <item> (',' <item>)*
<item> ::= <word> | <number> | <word> <number>
<word> ::= r'[a-z]+' | r'(ab)+' | r'a*b?'
<number> ::= r'[0-9]+(\.[0-9]*)?'
""",
    "bytes": r"""
<start> ::= <magic> <len> <payload>+
<magic> ::= b'\x89PNG' | b'GIF8' | b'\x00'
<len> ::= rb'[\x00-\x7f]'
<payload> ::= b'\xff' | b'ab' | rb'[a-c]{2}'
""",
    "bits": """
<start> ::= <byte>+
<byte> ::= <bit>{8}
<bit> ::= 0 | 1
""",
    "bits_mixed": """
<start> ::= <flags> <bit5> <tail>
<flags> ::= <flag>{3}
<flag> ::= 0 | 1
<tail> ::= 'A'*
<bit5> ::= 0 0 0 0 0 | 1 1 1 1 1 | 0 1 0 1 0
""",
    "csv_like": """
<start> ::= <line> ('\\n' <line>)*
<line> ::= <cell> (',' <cell>)*
<cell> ::= <unquoted> | '"' <quoted> '"'
<unquoted> ::= <c>*
<quoted> ::= (<c> | ',' | '""')*
<c> ::= 'a' | 'b' | ' '
""",
    "expr": """
<start> ::= <expr>
<expr> ::= <term> | <expr> '+' <term> | <expr> '-' <term>
<term> ::= <factor> | <term> '*' <factor> | <term> '/' <factor>
<factor> ::= <number> | '(' <expr> ')' | '-' <factor>
<number> ::= <digit>+ ('.' <digit>+)?
<digit> ::= '0' | '1' | '2' | '3' | '9'
""",
    "options_nested": """
<start> ::= (<a>? <b>?)* 'e'
<a> ::= 'a' | 'aa'
<b> ::= 'b'? 'a'?
""",
    "unicode": """
<start> ::= <w>+
<w> ::= 'ä' | 'ö' | '€' | '𝄞' | r'[α-ω]+'
""",
}

INPUTS: dict[str, list[str | bytes]] = {
    "node_types": ['ab=12;cd="xy"!;ef=;', "a=;", 'q="";', "ab=12;cd", "x=1234;"],
    "ambiguous": ["1", "1+1", "1+1+1", "1+1+1+1", "1+", "+1"],
    "right_recursive": ["a", "aaaa", "a" * 40, ""],
    "left_recursive": ["a", "aaaa", "a" * 40, "aab"],
    "epsilon": ["", "x", "y", "xy", "xxyy", "yx", "xyy"],
    "nullable_chain": ["z", "az", "aaz", "aaaz", "a"],
    "regex": ["abc", "ab12", "ababab,1.5,x", "abab3.", "aab,", "12,ab"],
    "bytes": [b"\x89PNG\x05\xffab", b"GIF8\x01ac", b"\x00\x00\xff\xff", b"\x89PN"],
    "bits": [b"A", b"AB", b"\x00\xff"],
    "bits_mixed": [b"\x00AA", b"\xffA", b"\x0a"],
    "csv_like": ['a,b\n"a,b",', 'ab, a\n""""', "a,,b", '"a'],
    "expr": ["1+2*3", "(1-2)/-3.0", "((1))", "1+", "9.99*(3"],
    "options_nested": ["e", "aabe", "abaabae", "bbbe", "aaa"],
    "unicode": ["äö€𝄞", "αβγä", "ö𝄞ω"],
}


def _grammar(spec: str):
    grammar, _ = parse(spec, use_stdlib=False, use_cache=False)
    assert grammar is not None
    return grammar


def _assert_same(rules, scenario: Scenario) -> None:
    difference = compare(rules, scenario)
    assert difference is None, str(difference)


@pytest.mark.parametrize(
    "name,word",
    [(name, word) for name, words in INPUTS.items() for word in words],
)
def test_handwritten(name: str, word: str | bytes) -> None:
    rules = _grammar(SPECS[name]).rules
    rng = random.Random(f"{name}:{word!r}")
    for mode in (ParsingMode.COMPLETE, ParsingMode.INCOMPLETE):
        _assert_same(rules, Scenario(word, mode=mode))
    if len(word) > 1:
        for _ in range(3):
            _assert_same(
                rules,
                Scenario(
                    word,
                    mode=rng.choice([ParsingMode.COMPLETE, ParsingMode.INCOMPLETE]),
                    chunks=random_chunks(len(word), rng),
                    check_parser=False,
                ),
            )


@pytest.mark.parametrize("name", sorted(SPECS))
def test_fuzzed(name: str) -> None:
    grammar = _grammar(SPECS[name])
    grammar.prime()
    rng = random.Random(name)
    words = terminal_words(grammar.rules)
    for i in range(6):
        tree = grammar.fuzz(max_nodes=rng.choice([10, 20, 40]))
        word, starter_bit = serialize(tree)
        for scenario in scenarios_for(
            word, "<start>", rng, starter_bit, check_tables=len(word) < 100
        ):
            _assert_same(grammar.rules, scenario)
        if words and not isinstance(word, bytes) and i % 2 == 0:
            odd = "".join(str(rng.choice(words)) for _ in range(rng.randrange(1, 6)))
            _assert_same(grammar.rules, Scenario(mutate(odd, rng)))


@pytest.mark.parametrize("name", ["node_types", "expr", "csv_like", "bytes"])
def test_other_start_symbols(name: str) -> None:
    grammar = _grammar(SPECS[name])
    grammar.prime()
    for nonterminal in sorted(grammar.rules, key=lambda nt: nt.name()):
        for _ in range(2):
            tree = grammar.fuzz(nonterminal, max_nodes=20)
            word, starter_bit = serialize(tree)
            _assert_same(
                grammar.rules,
                Scenario(word, nonterminal.name(), starter_bit=starter_bit),
            )
            _assert_same(
                grammar.rules,
                Scenario(
                    word,
                    nonterminal.name(),
                    ParsingMode.INCOMPLETE,
                    starter_bit=starter_bit,
                ),
            )


@pytest.mark.parametrize(
    "resource",
    [
        "dynamic_repetition.fan",
        "dynamic_repetition_2.fan",
        "global_var_bounds.fan",
        "bitstream.fan",
        "bitstream-a.fan",
        "csv.fan",
        "byte_alternative.fan",
        "high_bytes.fan",
        "incomplete.fan",
        "ambiguous_io.fan",
        "cross_reference_protocol_msg.fan",
    ],
)
def test_resources(resource: str) -> None:
    path = RESOURCES_ROOT / resource
    with open(path) as fh:
        grammar, _ = parse(fh, use_stdlib=True, use_cache=False, check=False)
    assert grammar is not None
    grammar.prime()
    rng = random.Random(resource)
    for _ in range(6):
        try:
            tree = grammar.fuzz(max_nodes=rng.choice([20, 50]))
        except Exception:  # noqa: BLE001 - some specs need constraints to fuzz
            continue
        word, starter_bit = serialize(tree)
        for scenario in scenarios_for(word, "<start>", rng, starter_bit):
            _assert_same(grammar.rules, scenario)


@pytest.mark.parametrize("seed", range(60))
def test_random_grammars(seed: int) -> None:
    rng = random.Random(seed)
    spec = random_spec(rng)
    try:
        grammar, _ = parse(spec, use_stdlib=False, use_cache=False, check=False)
    except Exception:  # noqa: BLE001 - e.g. unbreakable loops
        pytest.skip("Fandango does not accept this grammar")
    assert grammar is not None
    for word in random_words(rng, 6):
        for mode in (ParsingMode.COMPLETE, ParsingMode.INCOMPLETE):
            difference = compare(grammar.rules, Scenario(word, mode=mode))
            assert difference is None, f"{spec}\n{word!r}\n{difference}"
        if len(word) > 1:
            difference = compare(
                grammar.rules,
                Scenario(
                    word,
                    mode=ParsingMode.INCOMPLETE,
                    chunks=random_chunks(len(word), rng),
                    check_parser=False,
                ),
            )
            assert difference is None, f"{spec}\n{word!r}\n{difference}"
