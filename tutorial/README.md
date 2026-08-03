# Fandango Hands-On Tutorial

A hands-on tutorial for [Fandango](https://fandango-fuzzer.github.io/), built
around **one** small target that grows across five blocks. You start with random
bytes and end with Fandango holding a stateful conversation with a server, and
you watch code coverage of the target climb at every step.

The prose walkthrough of these exercises, block by block and with the solutions
behind spoiler dropdowns, is the **Hands-On** part of the Fandango
documentation: <https://fandango-fuzzer.github.io/HandsOn.html>. This file is
the short version, for working directly in the checkout.

The target is **FDP**, the Fandango Demo Protocol: a tiny, text-based, stateful
messaging protocol. It is fully specified in [`docs/FDP-SPEC.txt`](docs/FDP-SPEC.txt)
(read it like an RFC). Text was chosen so every input is human-readable and easy
to debug.

> There is no `solutions/` directory in this tree, so that browsing the
> exercises never spoils them. Each exercise's complete solution is published as
> a spoiler dropdown in the documentation:
> <https://fandango-fuzzer.github.io/HandsOn.html>. Copy them into a
> `solutions/` directory here (it is gitignored) and `fdp_harness.py --all` and
> `fdp_validate.py --record` work too; everything else works without them.

## Setup

You need Python 3.10+ and one dependency, Fandango itself. Inside this
repository, an editable install of the checkout is what you want:

```
pip install -e ..
```

Standalone, `pip install fandango-fuzzer` does the same job. Either way that is
all; the target and helper scripts use only the Python standard library. Check
your install from this directory:

```
fandango --version
python fdp_validate.py --step random --spec exercises/00_random.fan
```

The second command generates a batch of random inputs, runs them through the
target, and checks them against the recorded expectations for the warm-up step.
If it ends with `PASS`, you are ready.

> Run every command from this directory, so that specs can `import fdp`.

## The five blocks

You work through five blocks in order. Each adds one idea and unlocks more of the
target:

| # | Block | You edit | The idea |
|---|---|---|---|
| 0 | Warm-up | (nothing) | random bytes: the baseline, and why we need more |
| 1 | Grammars | `exercises/01_grammar.fan` | structure: alternatives, repetition, optionality |
| 2 | Constraints | `exercises/02_constraints.fan` | semantics: length, checksum, field rules |
| 3 | Execution feedback | `exercises/03_coverage.fan`, `exercises/03_target.fan` | use the target's own behaviour to steer generation |
| 4 | Protocol fuzzing | `exercises/04a_session.fan`, `exercises/04b_protocol.fan` | stateful sessions, then live interactive testing |

`exercises/00_random.fan` is the warm-up baseline; there is nothing to fill in,
it is just there to show how little raw random fuzzing reaches.

From block 2 on, an exercise does not restate the previous one: it pulls it in
with [`include()`](https://fandango-fuzzer.github.io/Hatching.html), so your own
grammar and constraints carry forward and each file holds only what is new.
Exercise 2 is six lines long for that reason. The flip side is that an
undefined-symbol error in a later block usually means the gap is in an earlier
file, so get each block to `PASS` before moving on.

## How a block works (the loop)

For every block you repeat the same short loop:

1. **Open the exercise** in `exercises/`. Its header tells you everything you
   need: the goal, what to `Read` in the spec, a `Docs:` link to the matching
   [Fandango reference](https://fandango-fuzzer.github.io/) page, a `Run:`
   command, and the exact `Validate:` command. The body has `# TODO` markers
   marking where you write.
2. **Fill in the TODOs.** Add the grammar rules and constraints the header asks
   for (see "Working with .fan grammars" below).
3. **Run it** to see what your spec generates:
   ```
   fandango fuzz -f exercises/00_random.fan -n 5
   ```
   Five sample inputs print. Eyeball them: do they look like the block wants?
4. **Validate it** with the `Validate:` command from the header. It tells you
   whether your grammar is complete for the block and, if not, exactly what is
   missing (see "Validating your grammar" below).
5. **`PASS` means move on.** When the validator prints `PASS`, that block is done.

Stuck? The exercise's `Read` and `Docs` lines point you at the right spec section
and Fandango page for that block. Also, feel free to ask us questions at any point :)

## Working with .fan grammars

A Fandango spec (a `.fan` file) has two parts: a **grammar** and, optionally,
**constraints**.

**Grammar rules** describe the structure of an input. A rule names a symbol
(`<...>`) and lists how to build it:

```
<message> ::= <ver> " " <body> " LEN=" <len> " CRC=" <crc>
<ver>     ::= "FDP1" | "FDP2"          # | means alternatives: this OR that
<body>    ::= <login> | "PING" | "QUIT"
<len>     ::= <digit>+                  # +  one or more   *  zero or more   ?  optional
<digit>   ::= r'[0-9]'                  # r'...' is a regex describing a terminal
```

Generation starts at `<start>` and expands symbols, picking among alternatives,
until only literal text is left.

**Constraints** are `where` clauses: Python predicates over the grammar symbols
that rule out inputs a grammar alone cannot. They are how you express semantics:

```
where str(<len>) == str(len(str(<body>)))         # LEN must equal the body length
where str(<crc>) == fdp.crc16hex(str(<body>))      # CRC must be the body's checksum
```

A `where` clause can call any Python, including helpers that run the target
itself. That is exactly how the execution-feedback block (3) works.

An FDP message is one line: the anchor and version (`FDP1`), a body of the form
`TYPE payload`, then `LEN=` the body length and `CRC=` its checksum. For example,
the body `LOGIN user=alice` is 16 characters long, so a complete line is:

```
FDP1 LOGIN user=alice LEN=16 CRC=339a
```

See [`docs/FDP-SPEC.txt`](docs/FDP-SPEC.txt) for the full message format, and each
exercise's `Docs:` link for the Fandango syntax that block needs.

## Validating your grammar (the bug hunt)

Running a spec shows you a few sample inputs, but not whether your grammar is
*complete* for the block. That is what the validator is for:

```
python fdp_validate.py --step grammar --spec exercises/01_grammar.fan
```

`--step` is one of `random`, `grammar`, `language`, `feedback`, `protocol` (the
five blocks, in order). Every exercise header carries its exact `Validate:`
command, so you can copy it straight from the file.

**How it works.** The target `fdp.py` has small **bug** beacons planted at the
branches each block is meant to reach. A "bug" is one of those branches: when your
grammar drives an input all the way to it, you have *found* that bug. The
validator generates inputs from your spec, runs them through the target, and
collects which bugs they trip. A grammar that reaches every bug for its block is
complete.

**Reading the output.** For each block the validator reports three things:

* **coverage** - how many lines of `fdp.py` your inputs reach, next to the
  reference number for that block;
* **bugs** - a checklist of the branches this block should unlock. `[x]` is found,
  `[ ]` is still missing, and each missing one comes with a `->` hint about what
  your grammar is not yet producing;
* **missing lines** - any lines the reference reaches that you do not, shown with
  their source, so you can see exactly what you leave out.

A grammar that is not finished yet looks like this:

```
$ python fdp_validate.py --step grammar --spec exercises/01_grammar.fan
step 'grammar': structurally valid lines: every body type parses
...
bugs     : 4 / 5 found for this step
   [x] shape:LOGIN     a LOGIN message parsed (right structure)
   [x] shape:MSG       a MSG message parsed (right structure)
   [x] shape:PING      a PING message parsed (right structure)
   [x] shape:QUIT      a QUIT message parsed (right structure)
   [ ] shape:SUB       a SUB message parsed (right structure)
       -> add the SUB alternative to <body> and give it the fields it needs
FAIL: 1 bug(s) left to find (shape:SUB). Fix the grammar and re-run.
```

Read the missing bug and its hint, fix the grammar (here: add the `SUB`
alternative to `<body>`), and re-run. When every bug is found you get:

```
PASS: found every bug for 'grammar'. Safe to move on to 'language'.
```

That `PASS` is your signal the block is complete.

If your spec does not even run (a fresh exercise still has `# TODO`s in it), the
validator says so and prints Fandango's own error above, which usually names the
symbol you have not defined yet.

**One subtlety for the `feedback` block.** It is checked at just five inputs, on
purpose. With so few inputs an undirected grammar is lopsided and misses a body
type, so only a coverage-guided spec finds all the bugs. That gap is the whole
point of the block.

For a plain coverage number of any spec (no pass/fail, no bugs), use the harness
directly:

```
python fdp_harness.py --spec exercises/02_constraints.fan --n 500
```

## The payoff: coverage grows as the spec gets smarter

As your specs get smarter, they reach deeper into `fdp.py`. This is the whole
arc, block by block:

```
step        lines in fdp.py   what the inputs do
random            14          die at the framing checks
grammar           45          reach the parser, die at the length gate
language          78  (n=5)   5 random valid messages, lopsided: no LOGIN
feedback          82  (n=5)   5 diverse messages: feedback covers all 5 types
(directed)        77          steered: one branch only (every input a LOGIN)
protocol          94          stateful: the deep handlers open up
```

Three things to notice. Structure and semantics unlock code the previous stage
could not touch (14 -> 45 -> 78). The two `n=5` rows are a same-budget
comparison, and they are where execution feedback earns its keep: given only five
inputs, undirected constrained generation is lopsided and never happens to
produce a LOGIN, so the login handler stays dark (78); coverage feedback spends
each input on a branch the others miss and so covers all five body types (82).
That is the payoff, **diversity**: reaching what undirected sampling leaves out at
the same budget. (Ask for many more inputs and plain constraints eventually
stumble into every type too, so both saturate at 82; feedback is what gets you
there with a handful of inputs, which matters when each input is expensive to
run.) The last of the coverage is unlocked only by **statefulness** (94), the
finale.

Runs are reproducible: a fixed `--seed` (default 18) plus `PYTHONHASHSEED=0`, so
the same spec always yields the same inputs and the same numbers.

## The live protocol demo

Once Exercise 4b is filled in, Fandango plays the client and drives the reference
server through a full `LOGIN -> SUB -> MSG -> QUIT` conversation:

```
fandango -v talk -f exercises/04b_protocol.fan -n 1 python fdp_server.py
```

Send the messages out of order (try it: `MSG` before `LOGIN`) and the server
answers `ERR_NOAUTH`. The handlers that deliver messages are reachable only after
a login earlier in the same session; that is what stateful protocol testing is
about.

## What is in here

```
docs/FDP-SPEC.txt   the target protocol, specified like an RFC
fdp.py             the target: a frame -> parse -> validate -> apply pipeline
fdp_server.py      line-oriented server for `fandango talk`
fdp_cover.py       execution-feedback helpers (run the target, read what it did)
fdp_harness.py     coverage harness for any spec (--spec, --n, --seed)
fdp_validate.py    per-step self-check for your own grammar (--step, --spec)
fdp_reference.json the recorded expectations the validator checks you against
exercises/         starter specs with TODOs (what you edit)
```

## A couple of gotchas

* `type` is a reserved word in the `.fan` language, so a message type is never a
  nonterminal named `<type>`.
* Execution feedback here is *behavioural*: a constraint runs the target and reads
  back what it did (`fdp_cover`), using the branch trace the target records about
  itself. Line-by-line tracing inside a constraint is far too slow in a search
  loop.
