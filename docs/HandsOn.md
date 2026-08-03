---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:handson)=
# Hands-On: Fuzzing a Protocol End to End

The rest of this book introduces Fandango feature by feature. This part does
the opposite: it takes **one** program and fuzzes it five times over, each pass
adding a single idea, and measures what each idea buys you in code coverage of
that program.

Everything here is an *exercise*. The files live in the [`tutorial/`
directory](https://github.com/fandango-fuzzer/fandango/tree/main/tutorial) of
the Fandango repository, and each block leaves blanks for you to fill in. A
self-check tells you when a block is complete, so you can work through the
whole thing without an instructor.

```{tip}
Clone the Fandango repository and everything you need is in `tutorial/`: the
target, the exercises, the protocol spec, and the self-check.
```

(sec:handson-target)=
## The Target: FDP

The target is **FDP**, the Fandango Demo Protocol: a tiny, text-based, stateful
messaging protocol invented for this tutorial. It is text so that every input
is human-readable and can be edited by hand when you are debugging your own
grammar.

One message is one line:

```
FDP1 LOGIN user=alice LEN=16 CRC=339a
```

* `FDP1` is the anchor and version (`1` or `2`)
* `LOGIN` is the message type, one of `LOGIN`, `MSG`, `SUB`, `PING`, `QUIT`
* `user=alice` is the payload: `key=value` records joined by `&`
* `LEN=16` is the decimal length of the *body*, the `LOGIN user=alice` part
* `CRC=339a` is the CRC-16/CCITT of that same body, as four hex digits

FDP is specified like an RFC in
[`tutorial/docs/FDP-SPEC.txt`](https://github.com/fandango-fuzzer/fandango/blob/main/tutorial/docs/FDP-SPEC.txt),
and the exercises refer to it by section. The reference implementation,
`fdp.py`, is a four-stage pipeline:

```
frame  ->  parse  ->  validate  ->  apply
```

Each stage consumes the *typed* result of the previous one and rejects
malformed input as early as it can. A later stage cannot run unless every
earlier stage succeeded, and some `apply` branches need session state that only
an *earlier message on the same connection* can set.

That last property is what makes this worth doing. The coverage gradient below
is not staged with artificial `if`s: it falls out of real data dependencies, so
reaching deeper genuinely requires better inputs.

(sec:handson-arc)=
## The Arc

| Block | You add | Reaches |
|---|---|---|
| [0. Random bytes](sec:handson-random) | nothing | the framing checks |
| [1. Grammar](sec:handson-grammar) | structure | the parser |
| [2. Constraints](sec:handson-lang) | semantics (length, checksum) | the handlers |
| [3. Execution feedback](sec:handson-feedback) | the target's own behaviour | every single-message branch |
| [4. Protocol](sec:handson-protocol) | statefulness | the login-gated handlers |

Measured against `fdp.py`, with the reference solution for each block:

```
spec                            label                     lines   funnel (cumulative reach)
------------------------------------------------------------------------------------------
00_random.fan                   random bytes                 14   frame:200  parse:0    validate:0    apply:0
01_grammar.fan                  grammar only                 45   frame:200  parse:200  validate:200  apply:0
02_constraints.fan              grammar + constraints        78   frame:5    parse:5    validate:5    apply:5
03_coverage.fan                 + coverage feedback          82   frame:5    parse:5    validate:5    apply:5
03_target.fan                   + targeted line              77   frame:200  parse:200  validate:200  apply:200
04a_session.fan                 stateful session             94   frame:800  parse:800  validate:800  apply:800
```

The *funnel* reads left to right: how many inputs got as far as each pipeline
stage. Random bytes never leave `frame`. A grammar gets every input to
`validate` and no further, because `LEN` and `CRC` are still wrong. Constraints
are what first push inputs into `apply`.

Two rows deserve a note, because a naive reading of the `lines` column is
misleading.

Rows 3 and 4 are run at **five inputs each**, on purpose, so they are a fair
same-budget comparison. That is where feedback earns its keep, and
{ref}`block 3 <sec:handson-feedback>` shows the two outputs side by side.

Row 5 covers *fewer* lines than row 4 and is still the point of its block: it
is **directed**, every input is a `LOGIN`, so it deliberately trades breadth
for precision.

(sec:handson-setup)=
## Setup

You need Python 3.10 or later and Fandango itself; the target and all helper
scripts use only the standard library. From a checkout of the Fandango
repository:

```shell
$ cd tutorial
$ pip install -e ..
```

Standalone, `pip install fandango-fuzzer` does the same job. Check the install:

```shell
$ fandango --version
$ python fdp_validate.py --step random --spec exercises/00_random.fan
```

If that ends in `PASS`, you are ready for {ref}`block 0 <sec:handson-random>`.

```{important}
Run every command from the `tutorial/` directory, so that specs can
`import fdp`.
```

(sec:handson-loop)=
## How a Block Works

Every block is the same short loop.

1. **Open the exercise** in `exercises/`. Its header states the goal, what to
   read in the FDP spec, which chapter of this book covers the idea, and the exact
   commands to run and to validate.
2. **Fill in the `# TODO` markers.** That is the only part you write.
3. **Run it** to see what comes out:
   ```shell
   $ fandango fuzz -f exercises/01_grammar.fan -n 5
   ```
4. **Validate it.** This is the part that tells you whether you are *done*,
   rather than merely producing output.
5. **`PASS` means move on.**

Every exercise below carries its solution in a dropdown, holding the complete
spec rather than a snippet. Nothing is spoiled unless you click, so use them
freely rather than staying stuck.

To run a solution rather than read it, save it under `solutions/` in the
tutorial directory, keeping the file name:

```shell
$ python fdp_harness.py --spec solutions/02_constraints.fan --n 200
```

With all of them in place the reference ladder runs end to end and reproduces
the coverage table above:

```shell
$ python fdp_harness.py --all --n 200
```

```{note}
`solutions/` is deliberately absent from the repository and is listed in
`.gitignore`, so a checkout never spoils the exercises. Creating it yourself is
the intended way to get the reference ladder running.
```

(sec:handson-validator)=
## Knowing When You Are Done

Sample output tells you a spec runs. It does not tell you the spec is
*complete*. That is what `fdp_validate.py` is for:

```shell
$ python fdp_validate.py --step grammar --spec exercises/01_grammar.fan
```

The target has small **beacons** planted at the branches each block is meant to
unlock. Reaching one means you have found it. The validator generates inputs
from your spec, runs them through the target, and reports which beacons your
inputs tripped. Here is a grammar that is missing the `SUB` alternative:

```
step 'grammar': structurally valid lines: every body type parses
checking exercises/01_grammar.fan  (n=200, seed=18)
------------------------------------------------------------------------------
coverage : 45 lines in fdp.py (reference solution reaches 45)
bugs     : 4 / 5 found for this step (bugs are the pass/fail signal, not the raw line count)
   [x] shape:LOGIN     a LOGIN message parsed (right structure)
   [x] shape:MSG       a MSG message parsed (right structure)
   [x] shape:PING      a PING message parsed (right structure)
   [x] shape:QUIT      a QUIT message parsed (right structure)
   [ ] shape:SUB       a SUB message parsed (right structure)
       -> add the SUB alternative to <body> and give it the fields it needs
------------------------------------------------------------------------------
FAIL: 1 bug(s) left to find (shape:SUB). Fix the grammar and re-run.
```

Note that this incomplete grammar reaches **45 lines, exactly as many as the
complete one**. Line coverage alone would have called it finished. The beacon
is what catches the gap, which is a small lesson in its own right about what
coverage numbers can and cannot tell you.

For a plain coverage number with no pass/fail, use the harness instead:

```shell
$ python fdp_harness.py --spec exercises/02_constraints.fan --n 200
```

(sec:handson-building)=
## Each Block Builds on the Last

From block 2 onwards, an exercise does not restate the previous one. It
[includes](sec:hatching) it:

```
include('01_grammar.fan')
```

So your own work carries forward: the grammar you wrote in block 1 is what
block 2 constrains, and the constraints you wrote in block 2 are what block 3
steers. Exercise 2 is six lines long, because the grammar is not repeated in
it.

This has a consequence worth knowing before you start. If Fandango reports an
undefined symbol in a later block, the gap is almost always in an *earlier*
file. Get each block to `PASS` before moving on and this will not happen.

```{note}
Reproducibility: every command in this part uses `--random-seed 18` and
`PYTHONHASHSEED=0`, so the same spec always yields the same inputs and the same
numbers. Your output should match what is printed here exactly.
```


---

(sec:handson-random)=
## Block 0: Random Bytes

This is the warm-up, and the only block with nothing to fill in. Its job is to
establish the baseline that every later block is measured against.

The spec is one line, `exercises/00_random.fan`:

```
<start> ::= <byte>*
```

That is dumb fuzzing: no structure at all, just a random number of random
bytes. Run it:

```shell
$ fandango fuzz -f exercises/00_random.fan -n 3
```

```
z<A4>^_M-^G<Y
M-;<FC>^CM-^OM-^KM-^[J
RM-^_3M-^DM-0M/M-^I^C,\M-^KM-+M-^Z
```

Now measure what that reaches inside the target:

```shell
$ python fdp_validate.py --step random --spec exercises/00_random.fan
```

```
step 'random': raw bytes reaching the framing layer
checking exercises/00_random.fan  (n=200, seed=18)
------------------------------------------------------------------------------
coverage : 14 lines in fdp.py (reference solution reaches 14)
bugs     : 2 / 2 found for this step
   [x] raw-badmagic    a line without the FDP anchor was rejected (ERR_MAGIC)
   [x] raw-nonascii    a non-ASCII line was rejected (ERR_ENCODING)
------------------------------------------------------------------------------
PASS: found every bug for 'random'. Safe to move on to 'grammar'.
```

Fourteen lines, and the funnel says all 200 inputs died in `frame`. Not one
reached the parser.

### Why It Stops So Early

Look at where the target gives up:

```python
def frame(data: bytes):
    try:
        line = data.decode("ascii")
    except UnicodeDecodeError:
        return Response("frame", "ERR_ENCODING")
    line = line.rstrip("\n")
    if not line.startswith(PROTO):
        return Response("frame", "ERR_MAGIC")
    ...
```

Random bytes fail one of the first two checks essentially always. To get past
`startswith("FDP")` by chance you would need the first three bytes to land on
`F`, `D`, `P` exactly, and then everything after it still has to satisfy the
trailer regex, the type check, the length field, and the checksum.

This is the honest case for grammars, and it is worth sitting with for a
moment: the target is not hostile, it is not obfuscated, and it is 300 lines
long. Random bytes still see almost none of it. Those two beacons you did find
are both *rejection* paths.

```{note}
Both bugs pass here even though the inputs are garbage. That is the point: this
block's target is the framing layer, and garbage reaches the framing layer just
fine. Later blocks ask for much more.
```

Next: {ref}`give the inputs a shape <sec:handson-grammar>`.



---

(sec:handson-grammar)=
## Block 1: Grammar

**Exercise:** `exercises/01_grammar.fan` &nbsp;&nbsp; **Background:**
{ref}`sec:first-spec`

Now you describe the *shape* of an FDP message, so that inputs stop dying at
the anchor check. No constraints yet: `LEN` and `CRC` stay free, so the
messages will be structurally right and semantically wrong. That is expected,
and it is precisely what {ref}`block 2 <sec:handson-lang>` fixes.

### What Is Given

The frame of the message, and the leaf definitions:

```
<start>   ::= <message>
<message> ::= <ver> " " <body> " LEN=" <len> " CRC=" <crc>

<ver>     ::= "FDP1" | "FDP2"          # anchor + version
<len>     ::= <digit>+                  # unconstrained for now
<crc>     ::= <hex>{4}                  # unconstrained for now

<name>    ::= r'[a-z]+'
<word>    ::= r'[a-z0-9]+'
<text>    ::= r'[a-z0-9 ]+'
<digit>   ::= r'[0-9]'
<hex>     ::= r'[0-9a-f]'
```

### What You Write

Two things, from sections 3 to 6 of the FDP spec.

**`<body>` as an alternative** over the five message kinds. A body is
`"<TYPE> <payload>"`, for example `LOGIN user=alice`, or just `PING`.

**Each message kind and its records.** `LOGIN` carries a `user=` record and
*may* also carry `&pass=`. `MSG` carries `to=` and `&body=`. `SUB` carries
`chan=`. `PING` and `QUIT` carry no payload at all.

The optional password is the interesting one: think about how a grammar says
"either this record, or nothing".

````{admonition} Solution: 01_grammar.fan
:class: tip, dropdown

```
# Solution to Exercise 1. Structure only, no constraints.
# The FDP anchor, a valid version and message type, and a payload of key=value
# records; one alternative per message kind binds a type to the payload it
# expects.
#
# <len> and <crc> are still free tokens, so every line is rejected at the
# validation stage (length mismatch or bad checksum). This reaches the parser
# but not the handlers.
#
# A generated line looks like:  FDP1 LOGIN user=alice LEN=73 CRC=0af3

<start>   ::= <message>
<message> ::= <ver> " " <body> " LEN=" <len> " CRC=" <crc>

<ver>     ::= "FDP1" | "FDP2"                        # anchor + version (alternatives)

<body>      ::= <login> | <message_msg> | <subscribe> | "PING" | "QUIT"
<login>       ::= "LOGIN user=" <name> <passopt>     # optionality below
<passopt>     ::= "&pass=" <word> | ""               # optional pass record
<message_msg> ::= "MSG to=" <name> "&body=" <text>
<subscribe>   ::= "SUB chan=" <name>

<len>     ::= <digit>+                                # decimal, unconstrained for now
<crc>     ::= <hex>{4}                                # 4 hex digits, unconstrained for now

<name>    ::= r'[a-z]+'
<word>    ::= r'[a-z0-9]+'
<text>    ::= r'[a-z0-9 ]+'
<digit>   ::= r'[0-9]'
<hex>     ::= r'[0-9a-f]'
```

`<passopt>` expresses optionality as an alternative with an empty
string. Fandango also has a `?` operator, so `("&pass=" <word>)?` works too.

Note that the message type is never a nonterminal called `<type>`: `type` is a
reserved word in the `.fan` language.
````

### Running It

```shell
$ fandango fuzz -f exercises/01_grammar.fan -n 5
```

```
FDP2 PING LEN=5235706 CRC=945d
FDP2 SUB chan=pcpepepchucrlgzumz LEN=12654866796622412 CRC=27b8
FDP1 QUIT LEN=12 CRC=ae2a
FDP1 PING LEN=0311357877549 CRC=9d57
FDP2 SUB chan=xwvrrilgbvu LEN=41253 CRC=6a5a
```

These are recognisably FDP messages. They are also all wrong: `LEN=5235706`
for a four-character body, a 17-digit length, a leading-zero length. The
grammar constrains the *form* of `<len>` (some digits) and says nothing about
its *value*.

### What It Reaches

```shell
$ python fdp_validate.py --step grammar --spec exercises/01_grammar.fan
```

```
coverage : 45 lines in fdp.py (reference solution reaches 45)
bugs     : 5 / 5 found for this step
   [x] shape:LOGIN     a LOGIN message parsed (right structure)
   [x] shape:MSG       a MSG message parsed (right structure)
   [x] shape:PING      a PING message parsed (right structure)
   [x] shape:QUIT      a QUIT message parsed (right structure)
   [x] shape:SUB       a SUB message parsed (right structure)
------------------------------------------------------------------------------
PASS: found every bug for 'grammar'. Safe to move on to 'language'.
```

From 14 lines to 45, and the funnel now shows all 200 inputs reaching
`validate`. Structure alone carried every input through framing and parsing.

And there they stop. Every one is rejected at the length check:

```python
def validate(msg: Message):
    fr = msg.frame
    if fr.length != len(fr.body):
        return Response("validate", "ERR_LENGTH")
```

No handler has run yet. `apply` is still at zero. A grammar can say what a
message *looks like*, but `LEN` is not a shape, it is a *relationship* between
two parts of the input, and that is a different kind of statement.

Next: {ref}`say what the parts mean to each other <sec:handson-lang>`.



---

(sec:handson-lang)=
## Block 2: Constraints

**Exercise:** `exercises/02_constraints.fan` &nbsp;&nbsp; **Background:**
{ref}`sec:constraints`, {ref}`sec:hatching`

Block 1 ended with every input rejected at the length check. `LEN` and `CRC`
are not shapes, they are *relationships* between parts of the input, and a
grammar cannot express a relationship. A [constraint](sec:constraints) can.

### The Whole Exercise

This is the first block that builds on your own earlier work, so the file is
short:

```
include('01_grammar.fan')

# TODO 1 (length encoding) ...
# TODO 2 (checksum) ...
# TODO 3 (min/max) ...

import fdp
```

[`include()`](sec:hatching) pulls in your block 1 grammar, so `<body>`,
`<len>`, `<crc>` and the message kinds are all in scope here without being
repeated. You add three `where` clauses.

```{important}
Because the grammar is not restated, an undefined-symbol error in this block
means the gap is in your `01_grammar.fan`. Fix it there and this file starts
working, with nothing to change here.
```

### What You Write

**Length encoding.** `LEN` must equal the number of characters in `<body>`.
The fields are text, so compare them as strings.

**Checksum.** `CRC` must equal the CRC-16 of `<body>`. Do not re-derive the
algorithm: `fdp.py` has the reference implementation, and Appendix B of the FDP
spec says which helper.

**Bounds.** Keep the body between 1 and 64 characters.

````{admonition} Solution: 02_constraints.fan
:class: tip, dropdown

```
# Solution to Exercise 2. The grammar comes from Exercise 1 via include();
# only the three well-formedness constraints are new.
include('01_grammar.fan')

# length encoding: the LEN token equals the body length.
where str(<len>) == str(len(str(<body>)))

# checksum: the CRC token is the CRC-16/CCITT of the body. The algorithm is
# part of the protocol (see docs/FDP-SPEC.txt Appendix B); we call the
# reference implementation rather than re-deriving it here.
where str(<crc>) == fdp.crc16hex(str(<body>))

# min/max: keep the body within the server's accepted window.
where 1 <= len(str(<body>)) <= 64

import fdp
```

The `str(...)` on both sides matters. `<len>` is a derivation tree, not an
integer, and comparing it to a number would not do what you want. See
{ref}`sec:DerivationTree`.

Calling `fdp.crc16hex` from a constraint is worth noticing on its own: a `where`
clause is arbitrary Python, so a checksum, a compression step or a signature is
no harder to express than a length. Block 3 pushes that much further.
````

### Running It

```shell
$ fandango fuzz -f exercises/02_constraints.fan -n 5
```

```
FDP2 PING LEN=4 CRC=6427
FDP2 SUB chan=pcpepepchucrlgzumz LEN=27 CRC=f024
FDP1 QUIT LEN=4 CRC=9f54
FDP1 PING LEN=4 CRC=6427
FDP2 SUB chan=xwvrrilgbvu LEN=20 CRC=eac4
```

Every line now round-trips. `PING` has a four-character body and says `LEN=4`;
the checksums match. You can confirm the server agrees:

```shell
$ fandango fuzz -f exercises/02_constraints.fan -n 20 --file-mode binary -d /tmp/ex2
$ for f in /tmp/ex2/*; do echo "$(cat "$f")" | python fdp_server.py; done
```

### What It Reaches

```shell
$ python fdp_validate.py --step language --spec exercises/02_constraints.fan
```

```
coverage : 82 lines in fdp.py (reference solution reaches 82)
bugs     : 11 / 11 found for this step (bugs are the pass/fail signal, not the raw line count)
   [x] gate-crc        a message passed the CRC check
   [x] gate-fields     a message passed field validation
   [x] gate-length     a message passed the LEN check
   [x] gate-noauth     a privileged message bounced with no session (ERR_NOAUTH)
   [x] handler-login   a LOGIN was accepted (OK_LOGIN)
   [x] handler-ping    a PING was accepted (OK_PONG)
   [x] shape:LOGIN     a LOGIN message parsed (right structure)
   [x] shape:MSG       a MSG message parsed (right structure)
   [x] shape:PING      a PING message parsed (right structure)
   [x] shape:QUIT      a QUIT message parsed (right structure)
   [x] shape:SUB       a SUB message parsed (right structure)
------------------------------------------------------------------------------
PASS: found every bug for 'language'. Safe to move on to 'feedback'.
```

45 lines to 82, and for the first time inputs reach `apply`. Three `where`
clauses nearly doubled the reachable code, because they were the difference
between "looks like a message" and "is a message".

### Where This Stops

Look at what the validator reports for a privileged message:

```
[x] gate-noauth  a privileged message bounced with no session (ERR_NOAUTH)
```

A `SUB` or a `MSG` is now perfectly well-formed and still refused, because
`apply` wants an authenticated session:

```python
    # everything below requires an authenticated session
    if session.user is None:
        return Response("apply", "ERR_NOAUTH")
```

No single message can satisfy that, however well-formed. `OK_SUB`, `OK_MSG` and
`OK_QUIT` are unreachable from here by construction, and they stay unreachable
until {ref}`block 4 <sec:handson-protocol>`.

Before that, {ref}`block 3 <sec:handson-feedback>` asks a different question:
given a fixed budget of inputs, are you spending it well?



---

(sec:handson-feedback)=
## Block 3: Execution Feedback

**Exercises:** `exercises/03_coverage.fan`, `exercises/03_target.fan`
&nbsp;&nbsp; **Background:** {ref}`sec:constraints`, {ref}`sec:diversity`

After block 2 every input is well-formed and reaches the handlers. So what is
left to want?

Generate five inputs and look at them:

```
FDP2 PING LEN=4 CRC=6427
FDP2 SUB chan=pcpepepchucrlgzumz LEN=27 CRC=f024
FDP1 QUIT LEN=4 CRC=9f54
FDP1 PING LEN=4 CRC=6427
FDP2 SUB chan=xwvrrilgbvu LEN=20 CRC=eac4
```

Two `PING`s, two `SUB`s, one `QUIT`. No `LOGIN`. No `MSG`. Every input is
valid, and the *suite* is lopsided: five chances to exercise the target and it
never once tried a login. Each input was judged on its own, and nothing ever
asked whether the batch as a whole was any good.

That is the gap this block closes, and it does so with the same tool as
before, an ordinary `where` clause. The difference is what the clause knows
about.

### The Feedback Signal

`fdp.py` records, for every message, the internal branches it drove through.
`fdp_cover.py` runs a message through the target and reads that trace back:

```python
def reaches(message: str, label: str) -> bool:
    """True iff running this message executes the branch tagged `label`."""
    return label in _run(message).trace
```

This is *behavioural* feedback: the constraint runs the program under test and
judges the input by what the program actually did with it.

```{note}
The target reports its own branch trace rather than being traced line by line
with `sys.settrace`. Inside a search loop, line tracing is orders of magnitude
too slow. Real coverage-guided fuzzers instrument the target for the same
reason.
```

### Exercise 3a: Cover the Whole Population

`fdp_cover` keeps a shared record of every branch the population has covered so
far, so a new message can be judged against everything accepted before it. Your
job is one `where` clause that admits an input only if it reaches a branch that
no already-accepted input has.

```
include('02_constraints.fan')

# TODO: admit an input only if it grows the population's coverage
# where

import fdp_cover
```

````{admonition} Solution: 03_coverage.fan
:class: tip, dropdown

```
# Solution to Exercise 3a. Grammar and well-formedness come from Exercise 2;
# only the population-coverage feedback constraint is new.
include('02_constraints.fan')

# admit an input only if it grows the population's coverage, so the suite
# spreads across branches instead of cloning one accept path.
where fdp_cover.covers_new(str(<start>))

import fdp_cover
```

`covers_new` runs the message, takes the set of branches it reached, and
accepts it only if that set is not already a subset of what the population
covers. Accepted inputs are added to the record, so each later input is judged
against a higher bar.
````

Now the same five-input budget:

```shell
$ fandango fuzz -f exercises/03_coverage.fan -n 5
```

```
FDP2 PING LEN=4 CRC=6427
FDP2 SUB chan=pcpepepchucrlgzumz LEN=27 CRC=f024
FDP1 QUIT LEN=4 CRC=9f54
FDP1 LOGIN user=ocdfoatnlngrezn LEN=26 CRC=c7ba
FDP2 MSG to=gfhqbbeinbojkbdgbpet&body=t LEN=34 CRC=8d68
```

One of each. Same budget, same grammar, same constraints, same seed: the only
change is that an input now has to justify its place in the suite.

```
coverage : 82 lines in fdp.py (reference solution reaches 82)
bugs     : 11 / 11 found for this step
```

Against 78 lines for the undirected spec at the same budget. Ask for 200 inputs
instead and block 2 stumbles into every type eventually and also reaches 82.
That is the honest framing of what feedback bought: **not a higher ceiling, but
the same ceiling far sooner**. When each input is cheap that is a curiosity.
When each input costs a network round trip or a device flash, it is the whole
game.

```{important}
Use `-n 5` here. `covers_new` is a hard gate, and the target has exactly five
single-message branches to pioneer, so a sixth input satisfying it does not
exist. Asking for more does not print the five it found; Fandango keeps
searching to its budget and prints nothing. Sizing `-n` to the satisfiable
population is a real consideration whenever coverage is a `where` constraint.
```

### Exercise 3b: Aim at One Branch

The other use of behavioural feedback is directed: not "cover everything" but
"every input must do *this*". Demand that each input drive the `apply:login`
branch.

````{admonition} Solution: 03_target.fan
:class: tip, dropdown

```
# Solution to Exercise 3b. Grammar and well-formedness come from Exercise 2;
# only the directed-feedback constraint is new.
include('02_constraints.fan')

# demand each input execute a specific target branch.
where fdp_cover.reaches(str(<start>), "apply:login")

import fdp_cover
```
````

```shell
$ fandango fuzz -f exercises/03_target.fan -n 5
```

```
FDP1 LOGIN user=ocdfoatnlngrezn LEN=26 CRC=c7ba
FDP2 LOGIN user=ap&pass=7 LEN=20 CRC=4325
FDP1 LOGIN user=of&pass=5lqb7tb5ds6mvww LEN=34 CRC=19c8
FDP2 LOGIN user=uakqycttmodyae&pass=nntty8e0ba6ujawy73 LEN=49 CRC=148a
FDP2 LOGIN user=jxqpsonu LEN=19 CRC=3bfa
```

Every input is a login, and the variation has moved inside the login: with and
without a password, short and long names. This spec covers 77 lines, *fewer*
than either spec above, and that is the correct outcome. You asked for one
branch and got a suite that hammers it.

Change the label to `"apply:pong"` and you get only `PING`s. Swap in
`fdp_cover.response(str(<start>)) == "ERR_NOAUTH"` and you get well-formed
privileged messages sent with no session, which is negative testing: a suite of
inputs that are valid in every way except the one that matters.

### The Ceiling

Both variants stop at the same wall. `OK_SUB`, `OK_MSG` and `OK_QUIT` never
appear, no matter how the feedback is pointed, because the branches behind them
need a login that happened *earlier on the same connection*. There is no
single message that satisfies that.

Next: {ref}`stop generating messages and start generating conversations
<sec:handson-protocol>`.



---

(sec:handson-protocol)=
## Block 4: Protocol

**Exercises:** `exercises/04a_session.fan`, `exercises/04b_protocol.fan`
&nbsp;&nbsp; **Background:** {ref}`sec:protocols`, {ref}`sec:parties`

Three blocks in, a wall has held throughout: `OK_SUB`, `OK_MSG` and `OK_QUIT`
are unreachable. Not because the inputs are malformed, but because of this:

```python
    # everything below requires an authenticated session
    if session.user is None:
        return Response("apply", "ERR_NOAUTH")
```

The state that opens those branches is set by a *different message*, earlier on
the same connection. No amount of work on a single message gets there. The unit
of generation has to change.

### Exercise 4a: A Session as One Input

The measurement form: generate a whole conversation as one input, four
messages, newline-separated.

The per-message `LEN` and `CRC` constraints are given, one pair per message.
You write two things.

**The sequence.** Define `<start>` as the four messages in protocol order,
`LOGIN`, `SUB`, `MSG`, `QUIT`, joined by newlines.

**The stateful link.** You can only message a channel you have joined. Tie the
`MSG` target to the `SUB` channel.

````{admonition} Solution: 04a_session.fan
:class: tip, dropdown

```
# Solution to Exercise 4a: a whole stateful SESSION as one input.
# Four messages for one connection, newline-separated:
#     LOGIN -> SUB -> MSG -> QUIT
# Each message is well-formed (its own LEN and CRC), and one cross-message
# constraint ties the MSG's target to the subscribed channel, so the sequence
# reaches the deep handlers (OK_SUB, OK_MSG, OK_QUIT) that NO single message
# can. The harness replays all four lines through ONE Session, which is what
# makes this the coverage finale.
#
# The live, interactive version of this is 04b_protocol.fan + fdp_server.py.

<start>  ::= <login> "\n" <sub> "\n" <msg> "\n" <quit>

<login>  ::= "FDP1 " <b_login> " LEN=" <l1> " CRC=" <c1>
<sub>    ::= "FDP1 " <b_sub>   " LEN=" <l2> " CRC=" <c2>
<msg>    ::= "FDP1 " <b_msg>   " LEN=" <l3> " CRC=" <c3>
<quit>   ::= "FDP1 " <b_quit>  " LEN=" <l4> " CRC=" <c4>

<b_login> ::= "LOGIN user=" <name>
<b_sub>   ::= "SUB chan=" <chan>
<b_msg>   ::= "MSG to=" <dest> "&body=" <text>
<b_quit>  ::= "QUIT"

<name> ::= r'[a-z]+'
<chan> ::= r'[a-z]+'
<dest> ::= r'[a-z]+'
<text> ::= r'[a-z0-9 ]+'
<l1> ::= <digit>+
<l2> ::= <digit>+
<l3> ::= <digit>+
<l4> ::= <digit>+
<c1> ::= <hex>{4}
<c2> ::= <hex>{4}
<c3> ::= <hex>{4}
<c4> ::= <hex>{4}
<digit> ::= r'[0-9]'
<hex>   ::= r'[0-9a-f]'

where str(<l1>) == str(len(str(<b_login>)))
where str(<c1>) == fdp.crc16hex(str(<b_login>))
where str(<l2>) == str(len(str(<b_sub>)))
where str(<c2>) == fdp.crc16hex(str(<b_sub>))
where str(<l3>) == str(len(str(<b_msg>)))
where str(<c3>) == fdp.crc16hex(str(<b_msg>))
where str(<l4>) == str(len(str(<b_quit>)))
where str(<c4>) == fdp.crc16hex(str(<b_quit>))

where 1 <= len(str(<b_login>)) <= 64
where 1 <= len(str(<b_sub>)) <= 64
where 1 <= len(str(<b_msg>)) <= 64

where str(<dest>) == str(<chan>)

import fdp
```

That second constraint is the interesting one. It relates two fields in
*different messages*, which is exactly the kind of statement that makes a
conversation valid rather than merely well-formed. Without it, `MSG` addresses a
random channel, the server answers `ERR_NOSUB`, and the delivery path stays
dark.
````

```shell
$ fandango fuzz -f exercises/04a_session.fan -n 1
```

```
FDP1 LOGIN user=fzxlbqmciokhm LEN=24 CRC=2ad4
FDP1 SUB chan=yquhyrhm LEN=17 CRC=e3ee
FDP1 MSG to=yquhyrhm&body=m gtng 5dquiy LEN=34 CRC=9993
FDP1 QUIT LEN=4 CRC=9f54
```

Four messages, eight satisfied length and checksum constraints, and
`to=yquhyrhm` matching `chan=yquhyrhm` across two lines.

```shell
$ python fdp_validate.py --step protocol --spec exercises/04a_session.fan
```

```
coverage : 94 lines in fdp.py (reference solution reaches 94)
bugs     : 12 / 12 found for this step (bugs are the pass/fail signal, not the raw line count)
   [x] gate-crc        a message passed the CRC check
   [x] gate-fields     a message passed field validation
   [x] gate-length     a message passed the LEN check
   [x] handler-login   a LOGIN was accepted (OK_LOGIN)
   [x] session-authed  a message ran on an authenticated session
   [x] session-msg     a message was delivered (OK_MSG)
   [x] session-quit    a session closed cleanly (OK_QUIT)
   [x] session-sub     a channel subscription succeeded (OK_SUB)
   [x] shape:LOGIN     a LOGIN message parsed (right structure)
   [x] shape:MSG       a MSG message parsed (right structure)
   [x] shape:QUIT      a QUIT message parsed (right structure)
   [x] shape:SUB       a SUB message parsed (right structure)
------------------------------------------------------------------------------
PASS: found every bug for 'protocol'. Safe to move; that is the last step.
```

94 lines, and the four `session-*` beacons are lit for the first time. That is
the finale of the gradient: 14, 45, 82, 94.

### Exercise 4b: A Live Conversation

Generating a transcript is one thing; holding the conversation is another. In
this exercise Fandango is the *client*, and `fdp_server.py` is a real server
process on the other end of a pipe.

The vocabulary is {ref}`parties <sec:parties>`: `<In:x>` is a message Fandango
**sends**, `<Out:y>` is a reply it **receives and must match**. Your job is to
write the exchange.

The file [includes](sec:hatching) your 4a spec, so the messages, the constraints
and your cross-message link all carry over. What it adds is given: every message
now ends in a newline, since the server reads one line at a time, and the
replies get rules of their own.

````{admonition} Solution: 04b_protocol.fan
:class: tip, dropdown

```
# Solution to Exercise 4b. Messages, constraints and the stateful cross-message
# constraint come from Exercise 4a; only the live exchange and the
# newline-terminated / reply rules are new.
include('04a_session.fan')

<start> ::= <In:login> <Out:ok_login> <In:sub> <Out:ok_sub> <In:msg> <Out:ok_msg> <In:quit> <Out:ok_quit>

<login> ::= "FDP1 " <b_login> " LEN=" <l1> " CRC=" <c1> "\n"
<sub>   ::= "FDP1 " <b_sub>   " LEN=" <l2> " CRC=" <c2> "\n"
<msg>   ::= "FDP1 " <b_msg>   " LEN=" <l3> " CRC=" <c3> "\n"
<quit>  ::= "FDP1 " <b_quit>  " LEN=" <l4> " CRC=" <c4> "\n"

<ok_login> ::= "OK_LOGIN " <rest> "\n"
<ok_sub>   ::= "OK_SUB " <rest> "\n"
<ok_msg>   ::= "OK_MSG " <rest> "\n"
<ok_quit>  ::= "OK_QUIT " <rest> "\n"
<rest>     ::= r'[^\n]*'
```
````

```shell
$ fandango -v talk -f exercises/04b_protocol.fan -n 1 python fdp_server.py
```

```
In:  <login>    'FDP1 LOGIN user=oigiwdkqvy LEN=21 CRC=8bc5\n'
Out: <ok_login> 'OK_LOGIN oigiwdkqvy\n'
In:  <sub>      'FDP1 SUB chan=vgacmvy LEN=16 CRC=9ebe\n'
Out: <ok_sub>   'OK_SUB vgacmvy\n'
In:  <msg>      'FDP1 MSG to=vgacmvy&body=7rk7pgszpo09 LEN=32 CRC=0169\n'
Out: <ok_msg>   'OK_MSG 1\n'
In:  <quit>     'FDP1 QUIT LEN=4 CRC=9f54\n'
Out: <ok_quit>  'OK_QUIT delivered=1\n'
```

A complete protocol run: authenticated, subscribed, delivered one message,
closed cleanly. `OK_QUIT delivered=1` is the server confirming that the message
actually arrived, which is only true because `to=vgacmvy` matched the channel
subscribed two messages earlier.

```{note}
A warning about "population size reduced to 1" is expected here and harmless.
```

### When the Server Disagrees

This is the part worth remembering, because it is how the technique finds real
bugs.

If the server's reply does not match the `<Out:...>` you predicted, Fandango
stops with `Could not parse received message fragments`, and the error contains
a `Received messages:` line showing what the server actually said.

That mismatch is a bug report. Your spec is a statement about how the protocol
is supposed to behave; the server disagreeing with it is either a bug in your
model or a bug in the server, and either way you want to know. Try reordering
the exchange to send `<In:msg>` before `<In:login>` and watch `ERR_NOAUTH` come
back where you predicted `OK_MSG`.

### Where You Landed

```
random bytes         14 lines    died at the framing checks
+ grammar            45 lines    reached the parser
+ constraints        82 lines    reached the handlers
+ feedback           82 lines    same ceiling, 40x fewer inputs
+ statefulness       94 lines    the login-gated handlers opened
```

Each step added one idea, and every step was expressed in the same two
constructs: a grammar rule and a `where` clause. Nothing here was special-cased
for FDP, and the four ideas transfer directly to any format or protocol with a
length field, a checksum, a handler table and a state machine, which is to say
most of them.

