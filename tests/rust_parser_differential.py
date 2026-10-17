"""
Differential testing of the Python Earley parser against its Rust port.

Both parsers run the same scenario (start symbol, mode, input split into
chunks for iterative parsing); everything observable is recorded and must be
identical:

* the complete parse table after every chunk -- every item of every column,
  in order, with every edge (predecessor, filler, Leo chain, parameters),
* `parsed_positions()`, `max_position()`, `can_continue()`, `current_tree()`,
* every derivation `tree_at()` yields at every parsed position, complete and
  incomplete, in order, including `origin_repetitions` (the iteration counters
  of the repetition nodes are reset to the same value before each run),
* the trees `Parser.parse_multiple()` yields (collapsed and with control flow),
* the type of any exception raised.

Used by `tests/test_rust_parser_differential.py` and
`scripts/rust_parser_differential.py`.
"""

import itertools
import random
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from typing import Any, AnyStr, Optional

from fandango.language.grammar import ParsingMode
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.parser.iterative_parser import IterativeParser
from fandango.language.grammar.parser.parse_state import (
    LeoNest,
    ParseState,
)
from fandango.language.grammar.parser.parser import Parser
from fandango.language.grammar.parser.rust_iterative_parser import (
    RustIterativeParser,
)
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.symbols.symbol import Symbol
from fandango.language.tree import DerivationTree

#: Derivations compared per parsed position (ambiguity can be exponential).
MAX_TREES = 25


def symbol_sig(symbol: Symbol) -> tuple[Any, ...]:
    value = symbol.value()
    return (
        type(symbol).__name__,
        type(value._value).__name__,
        value._value,
        tuple(value._trailing_bits),
        symbol.is_regex,
    )


def tree_sig(tree: Optional[DerivationTree]) -> Optional[list[Any]]:
    """
    A flat, preorder signature of everything a tree holds: class, attribute
    names (in order), symbol, parameters, `origin_repetitions`, and which
    nodes and `sources` lists are the same object (the index where an object
    first occurs). The lazily filled caches `hash_cache` and `_size` are left
    out: Python fills them in tree objects it shares between derivations.
    """
    if tree is None:
        return None
    out: list[Any] = []
    first_seen: dict[int, int] = {}
    first_sources: dict[int, int] = {}
    stack = [tree]
    while stack:
        node = stack.pop()
        out.append(
            (
                first_seen.setdefault(id(node), len(out)),
                type(node).__name__,
                tuple(vars(node)),
                symbol_sig(node.symbol),
                node.sender,
                node.recipient,
                node.read_only,
                tuple(node.origin_repetitions),
                first_sources.setdefault(id(node._sources), len(out)),
                len(node.sources),
                None if node.parent is None else first_seen.get(id(node.parent), -1),
                len(node.children),
            )
        )
        stack.extend(reversed(node.children))
    return out


def params_sig(params: Any) -> tuple[Any, ...]:
    return tuple(sorted(params or ()))


def alt_sig(symbols: Any) -> tuple[Any, ...]:
    return tuple((symbol_sig(s), params_sig(p)) for s, p in symbols)


# ----- parse tables -------------------------------------------------------


def _py_state(state: ParseState) -> tuple[Any, ...]:
    return (
        state.nonterminal.name(),
        state.position,
        alt_sig(state.symbols),
        state.dot,
        state.partial_matched_length,
        state.force_completed,
    )


def python_table_sig(parser: IterativeParser) -> list[Any]:
    table = []
    for column in parser._table:
        items = []
        for state in column:
            edges = []
            for edge in state.edges:
                previous = None if edge.previous is None else _py_state(edge.previous)
                filler = edge.filler
                if isinstance(filler, DerivationTree):
                    payload: Any = ("tree", symbol_sig(filler.symbol))
                elif isinstance(filler, ParseState):
                    payload = ("state", _py_state(filler))
                elif isinstance(filler, LeoNest):
                    payload = (
                        "leo",
                        _py_state(filler.inner),
                        [_py_state(s) for s in (filler.chain or [])],
                        params_sig(filler.top_params),
                    )
                else:
                    payload = ("list", [tree_sig(t) for t in filler])
                edges.append((previous, payload, params_sig(edge.params)))
            items.append((_py_state(state), edges))
        table.append(items)
    return table


def rust_table_sig(parser: RustIterativeParser) -> list[Any]:
    def state(desc: tuple[int, int, int, int, int, bool]) -> tuple[Any, ...]:
        nt, position, alt, dot, partial, fc = desc
        symbol = parser._symbols[nt]
        assert isinstance(symbol, NonTerminal)
        return (
            symbol.name(),
            position,
            alt_sig(parser._alts[alt]),
            dot,
            partial,
            fc,
        )

    def params(params_id: int) -> tuple[Any, ...]:
        return params_sig(parser._params[params_id].items())

    table = []
    for column in parser._core.dump_table():
        items = []
        for desc, raw_edges in column:
            edges = []
            for previous, kind, payload, params_id in raw_edges:
                if kind == 0:
                    sig: Any = ("tree", symbol_sig(parser._terminal(*payload)))
                elif kind == 1:
                    sig = ("state", state(payload))
                elif kind == 2:
                    inner, chain, top_params = payload
                    sig = (
                        "leo",
                        state(inner),
                        [state(s) for s in chain],
                        params(top_params),
                    )
                else:
                    sig = ("list", [tree_sig(t) for t in parser._parser_trees(payload)])
                edges.append(
                    (
                        None if previous is None else state(previous),
                        sig,
                        params(params_id),
                    )
                )
            items.append((state(desc), edges))
        table.append(items)
    return table


# ----- scenarios ----------------------------------------------------------


@dataclass
class Scenario:
    word: str | bytes
    start: str = "<start>"
    mode: ParsingMode = ParsingMode.COMPLETE
    #: Sizes of the pieces `word` is consumed in; None: all at once.
    chunks: Optional[list[int]] = None
    starter_bit: int = -1
    check_tables: bool = True
    check_current_tree: bool = True
    #: Also compare `Parser.parse_multiple` (single consume, with cache).
    check_parser: bool = True
    hookin_parent: Optional[DerivationTree] = None

    def pieces(self) -> list[str | bytes]:
        if not self.chunks:
            return [self.word]
        pieces = []
        i = 0
        for size in self.chunks:
            pieces.append(self.word[i : i + size])
            i += size
        if i < len(self.word):
            pieces.append(self.word[i:])
        return pieces


@dataclass
class Observation:
    events: list[tuple[Any, Any]] = field(default_factory=list)

    def record(self, label: Any, fn: Callable[[], Any]) -> bool:
        try:
            self.events.append((label, fn()))
            return True
        except RecursionError as e:
            self.events.append((label, ("EXCEPTION", "RecursionError", str(e)[:60])))
            return False
        except Exception as e:  # noqa: BLE001 - the type is what we compare
            self.events.append((label, ("EXCEPTION", type(e).__name__)))
            return False


def repetition_nodes(rules: dict[NonTerminal, Node]) -> list[Repetition]:
    found: list[Repetition] = []
    seen: set[int] = set()
    stack: list[Node] = list(rules.values())
    while stack:
        node = stack.pop()
        if id(node) in seen:
            continue
        seen.add(id(node))
        if isinstance(node, Repetition):
            found.append(node)
        stack.extend(node.children())
    return found


def _trees(parser: Any, position: int, incomplete: bool) -> list[Any]:
    return [
        (tree_sig(tree), flag)
        for tree, flag in itertools.islice(
            parser.tree_at(position, incomplete=incomplete), MAX_TREES
        )
    ]


def _parsed(parser: Parser, scenario: Scenario, include_controlflow: bool) -> list[Any]:
    return [
        tree_sig(tree)
        for tree in itertools.islice(
            parser.parse_multiple(
                scenario.word,
                scenario.start,
                mode=scenario.mode,
                include_controlflow=include_controlflow,
            ),
            MAX_TREES,
        )
    ]


def observe(
    parser_class: type[IterativeParser] | type[RustIterativeParser],
    backend: str,
    rules: dict[NonTerminal, Node],
    scenario: Scenario,
) -> Observation:
    obs = Observation()
    parser = parser_class(rules)
    table_sig: Callable[[Any], list[Any]] = (
        python_table_sig if backend == "python" else rust_table_sig
    )
    if not obs.record(
        "new_parse",
        lambda: parser.new_parse(
            scenario.start, scenario.mode, scenario.hookin_parent, scenario.starter_bit
        ),
    ):
        return obs
    incomplete = scenario.mode == ParsingMode.INCOMPLETE
    for i, piece in enumerate(scenario.pieces()):
        if not obs.record(("consume", i), partial(parser.consume, piece)):
            return obs
        obs.record(("positions", i), parser.parsed_positions)
        obs.record(("max_position", i), parser.max_position)
        obs.record(("consumed", i), parser.consumed_length)
        if scenario.check_tables:
            obs.record(("table", i), lambda: table_sig(parser))
        obs.record(("can_continue", i), parser.can_continue)
        if scenario.check_current_tree:
            obs.record(("current_tree", i), lambda: tree_sig(parser.current_tree()))
            obs.record(
                ("collapsed_current_tree", i),
                lambda: tree_sig(parser.collapse(parser.current_tree())),
            )
        offsets = list(parser.parsed_positions())
        offsets.append(parser.consumed_length())
        for offset in dict.fromkeys(offsets):
            obs.record(
                ("tree_at", i, offset),
                partial(_trees, parser, offset, incomplete),
            )
    if scenario.check_parser:
        for include_controlflow in (False, True):
            p = Parser(rules, backend=backend)
            obs.record(
                ("parse_multiple", include_controlflow),
                partial(_parsed, p, scenario, include_controlflow),
            )
            obs.record(
                ("max_position_parser", include_controlflow),
                p._iter_parser.max_position,
            )
    return obs


@dataclass
class Difference:
    label: Any
    python: Any
    rust: Any

    def __str__(self) -> str:
        def short(x: Any) -> str:
            s = repr(x)
            return s if len(s) < 600 else s[:600] + "..."

        python, rust, path = self.python, self.rust, []
        # Descend to the first differing element.
        while (
            isinstance(python, (list, tuple))
            and isinstance(rust, (list, tuple))
            and len(python) == len(rust)
        ):
            index = next(
                i for i, (a, b) in enumerate(zip(python, rust, strict=True)) if a != b
            )
            path.append(index)
            python, rust = python[index], rust[index]
        return f"{self.label} at {path}:\n  python: {short(python)}\n  rust:   {short(rust)}"


def compare(rules: dict[NonTerminal, Node], scenario: Scenario) -> Optional[Difference]:
    """Run `scenario` on both parsers; the first difference, or None."""
    repetitions = repetition_nodes(rules)
    iterations = [node.iteration for node in repetitions]
    py = observe(IterativeParser, "python", rules, scenario)
    for node, iteration in zip(repetitions, iterations, strict=True):
        node.iteration = iteration
    rs = observe(RustIterativeParser, "rust", rules, scenario)
    for (label_py, value_py), (label_rs, value_rs) in itertools.zip_longest(
        py.events, rs.events, fillvalue=(None, None)
    ):
        if label_py != label_rs or value_py != value_rs:
            return Difference(
                label_py if label_py is not None else label_rs, value_py, value_rs
            )
    return None


# ----- inputs -------------------------------------------------------------


def serialize(tree: DerivationTree) -> tuple[str | bytes, int]:
    """The word `Parser.parse_forest` parses for `tree`, and its starter bit."""
    starter_bit = -1
    if tree.contains_bits():
        starter_bit = (tree.count_terminals() - 1) % 8
    if tree.should_be_serialized_to_bytes():
        bit_string = tree.to_bits()
        return int(bit_string, 2).to_bytes((len(bit_string) + 7) // 8), starter_bit
    return tree.to_string(), starter_bit


def _edit(word: AnyStr, b: AnyStr, i: int, choice: int) -> AnyStr:
    if choice == 0:
        return word[:i] + word[i + 1 :]
    if choice == 1:
        return word[:i] + b + word[i:]
    if choice == 2:
        return word[:i] + b + word[i + 1 :]
    return word[:i] + word[i:] + word[i:]  # duplicate the tail


def mutate(word: str | bytes, rng: random.Random) -> str | bytes:
    """A random small edit of `word`."""
    if not word:
        return word
    i = rng.randrange(len(word))
    choice = rng.randrange(4)
    if isinstance(word, bytes):
        b = bytes([rng.choice([word[rng.randrange(len(word))], rng.randrange(256)])])
        return _edit(word, b, i, choice)
    c = rng.choice([word[rng.randrange(len(word))], chr(rng.randrange(32, 127))])
    return _edit(word, c, i, choice)


def random_chunks(length: int, rng: random.Random) -> list[int]:
    chunks = []
    remaining = length
    while remaining > 0:
        size = rng.choice([1, 1, 2, 3, 5, max(1, remaining // 2)])
        chunks.append(min(size, remaining))
        remaining -= size
    return chunks


def scenarios_for(
    word: str | bytes,
    start: str,
    rng: random.Random,
    starter_bit: int = -1,
    check_tables: bool = True,
) -> list[Scenario]:
    """Complete, incomplete, chunked, prefix and mutated variants of `word`."""
    result = [
        Scenario(word, start, starter_bit=starter_bit, check_tables=check_tables),
        Scenario(
            word,
            start,
            ParsingMode.INCOMPLETE,
            starter_bit=starter_bit,
            check_tables=check_tables,
        ),
    ]
    if len(word) > 1:
        result.append(
            Scenario(
                word,
                start,
                rng.choice([ParsingMode.COMPLETE, ParsingMode.INCOMPLETE]),
                chunks=random_chunks(len(word), rng),
                starter_bit=starter_bit,
                check_tables=check_tables,
                check_parser=False,
            )
        )
        cut = rng.randrange(1, len(word))
        result.append(
            Scenario(
                word[:cut],
                start,
                ParsingMode.INCOMPLETE,
                starter_bit=starter_bit,
                check_tables=check_tables,
            )
        )
    mutated = mutate(word, rng)
    result.append(
        Scenario(
            mutated,
            start,
            rng.choice([ParsingMode.COMPLETE, ParsingMode.INCOMPLETE]),
            starter_bit=starter_bit,
            check_tables=check_tables,
        )
    )
    return result


def terminal_words(rules: dict[NonTerminal, Node]) -> list[str | bytes]:
    """The literal terminals of the grammar, to build odd inputs from."""
    words: list[str | bytes] = []
    stack: list[Node] = list(rules.values())
    seen: set[int] = set()
    while stack:
        node = stack.pop()
        if id(node) in seen:
            continue
        seen.add(id(node))
        symbol = getattr(node, "symbol", None)
        if isinstance(symbol, Terminal) and not symbol.is_regex:
            value = symbol.value()._value
            if isinstance(value, (str, bytes)):
                words.append(value)
        stack.extend(node.children())
    return words


# ----- random grammars ----------------------------------------------------

_RANDOM_TERMINALS = [
    "'a'",
    "'b'",
    "''",
    "'ab'",
    "'ba'",
    "r'a+'",
    "r'b*'",
    "r'(ab)+'",
    "r'a?b?'",
]


def random_spec(rng: random.Random, nonterminals: int = 4) -> str:
    """
    A small random grammar over {a, b}: epsilon rules, cycles, left and right
    recursion, ambiguity, EBNF operators and regexes, to reach the corners of
    the Earley parser (Leo items, cycle checks, empty completions).
    """
    names = [f"<n{i}>" for i in range(nonterminals)]

    def element(depth: int) -> str:
        roll = rng.random()
        if roll < 0.45 or depth > 1:
            return (
                rng.choice(names)
                if rng.random() < 0.5
                else rng.choice(_RANDOM_TERMINALS)
            )
        if roll < 0.55:
            return "(" + alternative(depth + 1) + ")" + rng.choice(["*", "+", "?"])
        if roll < 0.62:
            low = rng.randrange(0, 3)
            high = max(1, low + rng.randrange(0, 3))
            return f"({element(depth + 1)}){{{low},{high}}}"
        if roll < 0.7:
            return "(" + alternative(depth + 1) + " | " + alternative(depth + 1) + ")"
        return rng.choice(names)

    def alternative(depth: int) -> str:
        return " ".join(element(depth) for _ in range(rng.randrange(1, 4)))

    lines = [
        f"<start> ::= {rng.choice(names)}"
        + (f" {rng.choice(names)}" if rng.random() < 0.3 else "")
    ]
    for name in names:
        alternatives = [alternative(0) for _ in range(rng.randrange(1, 4))]
        if rng.random() < 0.8:
            # Mostly productive, so Fandango's loop check accepts the grammar.
            alternatives.append(rng.choice(_RANDOM_TERMINALS))
        lines.append(f"{name} ::= " + " | ".join(alternatives))
    return "\n".join(lines) + "\n"


def random_words(rng: random.Random, count: int) -> list[str]:
    return [
        "".join(rng.choice("ab") for _ in range(rng.choice([0, 1, 2, 3, 4, 6, 9])))
        for _ in range(count)
    ]
