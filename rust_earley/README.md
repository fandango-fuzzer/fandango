# fandango_earley_rs — Fandango's Earley parser in Rust

A literal port of `IterativeParser` / `ForestBuilder`
(`src/fandango/language/grammar/parser/`) to Rust, usable as an alternative
parser backend next to the Python one. It produces the same parse tables, the
same derivations in the same order, and the same `DerivationTree` objects.

## Build

```sh
pip install maturin            # or: uv pip install maturin
cd rust_earley
maturin develop --release      # installs `fandango_earley_rs` into the active venv
```

## Use

```python
from fandango.language.grammar.parser.parser import Parser
parser = Parser(grammar.rules, backend="rust")   # or "python" (default)
```

or for everything Fandango parses (`Grammar` creates its `Parser` without a
backend argument):

```sh
FANDANGO_PARSER=rust fandango fuzz -f spec.fan
```

`RustIterativeParser` (`rust_iterative_parser.py`) has the public API of
`IterativeParser`: `new_parse`, `consume`, `can_continue`, `current_tree`,
`parsed_positions`, `tree_at`, `consumed_length`, `max_position`, `collapse`.

## What runs where

| Rust | Python (via callbacks) |
|---|---|
| predict / scan / complete, Leo items, cycle checks, column snapshots | grammar compilation (`GrammarCompiler`), symbol interning |
| forest: `children_of`, `derivations_of`, ambiguity cache | regex matching (`Terminal.regex_check_multiple_lengths`), cached per input position |
| duplicate detection, building the `DerivationTree` objects | context-dependent repetitions (`compile_bounded_repetition` on the incomplete tree) |
| `collapse` | |

## How equivalence is kept

* Every Python structure has a counterpart (`ParseState` → `State` in an
  arena, object identity → index), and every operation runs in the same order.
* `predict` adds items in the iteration order of a Python `set`, which depends
  on `ParseState.__hash__` (string hashes, column index). `pyset.rs` recomputes
  CPython's tuple hash and simulates its set insertion, bit for bit
  (verified for CPython 3.11–3.14, 64 bit).
* Trees are built the way `to_derivation_tree` does it — by occurrence in
  preorder (numbering `origin_repetitions`), then bottom-up looking children up
  by node — so a node occurring twice becomes one shared object, exactly as in
  Python (which makes the later `collapse` raise `KeyError`; reproduced too).
* Tree objects get exactly the attributes `DerivationTree.__init__` would set.

## Known differences

* Duplicate derivations are recognized by a 128-bit structural fingerprint,
  Python uses `hash(tree)` (64 bit): they differ only on a Python hash collision.
* Mixing `str` and `bytes` chunks in one parse raises `NotImplementedError`.
* Where Python's `construct_incomplete_tree` would loop forever (cyclic
  waiters), Rust raises `RecursionError`.
* Non-terminal symbol objects in trees are equal, but not necessarily the
  identical objects Python would use.
* `PacketIterativeParser` (which overrides `construct_incomplete_tree` and
  works on `ParseState`/`Column` objects) still uses the Python parser.

## Testing and benchmarking

```sh
python -m pytest tests/test_rust_parser_differential.py   # targeted differential tests
python scripts/rust_parser_differential.py                # all .fan specs of the repo
python scripts/rust_parser_benchmark.py                   # speed comparison
FANDANGO_PARSER=rust python -m pytest tests               # whole suite on the Rust backend
```
