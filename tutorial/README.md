# FDP: one target, built up across the whole tutorial

This directory is a single running example for the Fandango tutorial. Every
block reuses **one** toy protocol, **FDP** (Fandango Demo Protocol), and adds
exactly one layer on top of the previous block. As the specs climb from random
bytes to a stateful conversation, they reach steadily deeper into the same
target program, and the coverage they achieve grows with them.

## The target: FDP

A tiny **text** messaging protocol (text so students can read and hand-edit
every input). One message is one line:

```
FDP1 LOGIN user=alice LEN=16 CRC=339a
```

* `FDP1` / `FDP2`  anchor + version
* `LOGIN | MSG | SUB | PING | QUIT`  message type
* `key=value&...`  payload records
* `LEN=`  decimal length of the body (`"<TYPE> <payload>"`)
* `CRC=`  CRC-16/CCITT of that body, 4 hex digits

The reference implementation `fdp.py` is a four-stage pipeline where each stage
consumes the typed result of the previous one and rejects malformed input
early:

```
frame  ->  parse  ->  validate  ->  apply
```

A later stage cannot run unless every earlier stage succeeded, and some
`apply` branches need session state a *previous* message set. That data
dependency is what makes the coverage gradient real rather than staged with
`if`s.

## The coverage gradient (n=1000, seed=42)

```
spec                    lines in fdp.py   what the inputs do
00_random.fan                    14        die at the framing checks
01_grammar.fan                   45        reach the parser, die at the length gate
02_constraints.fan               82        reach the handlers (single messages)
03_coverage.fan                  80        directed: full accept paths only
03_target.fan                    77        directed: the login branch only
04_session.fan                   94        stateful: the deep handlers open up
```

Reproduce it:

```
PYTHONHASHSEED=0 python fdp_harness.py --all --n 1000 --seed 42
```

The feedback rungs (80, 77) cover *fewer* aggregate lines than plain
constraints on purpose: within a single message the constraint spec already
saturates what is reachable, so feedback buys **precision** (steer generation
to a chosen behaviour), not breadth. The remaining coverage is unlocked only by
**statefulness**, which is the finale.

## Map to the tutorial blocks

| Block | Files | One-line demo |
|---|---|---|
| Grammars (hands-on) | `01_grammar.fan` | `fandango fuzz -f 01_grammar.fan -n 5` |
| Constraints (hands-on) | `02_constraints.fan` | `fandango fuzz -f 02_constraints.fan -n 5` |
| Execution feedback (hands-on) | `03_coverage.fan`, `03_target.fan`, `fdp_cover.py` | `fandango fuzz -f 03_target.fan -n 5` |
| Protocol fuzzing (hands-on) | `04_protocol.fan`, `fdp_server.py` | see below |

`00_random.fan` is the opener ("look how little random fuzzing reaches").
`04_session.fan` is the measurement form of the protocol stage (a whole session
as one input, so the harness can score its coverage).

## The live protocol demo

Fandango plays the client and drives the reference server through a stateful
`LOGIN -> SUB -> MSG -> QUIT` conversation:

```
PYTHONHASHSEED=0 fandango talk -f 04_protocol.fan -n 1 --random-seed 42 \
    ../.venv/bin/python fdp_server.py
```

Send the messages out of order (e.g. `MSG` before `LOGIN`) and the server
answers `ERR_NOAUTH`: the handlers that deliver messages are reachable only
after a login earlier in the same session.

## Files

```
fdp.py            reference implementation (the target); self-instruments its branches
fdp_server.py     line-oriented REPL server for `fandango talk`
fdp_cover.py      execution-feedback helpers (run the target, read back what it did)
fdp_harness.py    reproducible coverage harness (--all / --spec, --n, --seed)
00_random.fan     <byte>* baseline
01_grammar.fan    structure only
02_constraints.fan  + length, checksum, min/max
03_coverage.fan   + execution feedback: reward high-coverage inputs
03_target.fan     + execution feedback: demand a specific branch
04_session.fan    a full stateful session as one input (measurement)
04_protocol.fan   the interactive <In>/<Out> version for `fandango talk`
```

## Notes and gotchas

* `type` is a reserved word in the `.fan` language; that is why the message
  type is never a nonterminal named `<type>`.
* Coverage-guided generation is expressed as an ordinary `where` constraint
  that *runs* the target (behavioural feedback). Line tracing (`sys.settrace`)
  inside a constraint is far too slow in the search loop, so the target reports
  its own branch trace instead (`fdp.Response.trace`), the way AFL-style
  coverage-guided fuzzers instrument their targets.
* `MAX_BODY = 64` keeps size-limit behaviour easy to reach in a demo.
