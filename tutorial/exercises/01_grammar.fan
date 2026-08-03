# EXERCISE 1 - Grammars
#
# Goal: describe the STRUCTURE of an FDP message. No constraints yet, so LEN
# and CRC stay free: your messages will be structurally right but rejected
# later at validation. That is expected, and it is exactly what Exercise 2
# fixes.
#
# Read:  docs/FDP-SPEC.txt, sections 3-6 (message format and the message types)
# Docs:  Fandango grammars (alternatives, repetition, optionality) -> https://fandango-fuzzer.github.io/FirstSpec.html
# Run:   fandango fuzz -f exercises/01_grammar.fan -n 5
# Validate: python fdp_validate.py --step grammar --spec exercises/01_grammar.fan
#
# A well-formed line looks like:  FDP1 LOGIN user=alice LEN=73 CRC=0af3
# (LEN and CRC are wrong for now; that is fine at this stage.)

<start>   ::= <message>
<message> ::= <ver> " " <body> " LEN=" <len> " CRC=" <crc>

<ver>     ::= "FDP1" | "FDP2"          # anchor + version (given)
<len>     ::= <digit>+                  # unconstrained for now (given)
<crc>     ::= <hex>{4}                  # unconstrained for now (given)

# ---------------------------------------------------------------------------
# TODO 1: define <body> as an ALTERNATIVE (the "|" operator) over the five
#   message kinds from the spec. A body is "<TYPE> <payload>", e.g.
#   "LOGIN user=alice" or just "PING". (FDP-SPEC sections 3-6 list all five.)
#
# <body> ::=

# TODO 2: define each message kind and its payload records (see FDP-SPEC 3-6).
#   - LOGIN carries a "user=" record and MAY also carry a "&pass=" record.
#     For the optional part, think about how a grammar expresses "either this
#     record, or nothing at all".
#   - MSG carries "to=" and "&body=" records.
#   - SUB carries a "chan=" record.
#   - PING and QUIT carry no payload (just the literals "PING" / "QUIT").
#
# <login>       ::=
# <passopt>     ::=
# <message_msg> ::=
# <subscribe>   ::=
# ---------------------------------------------------------------------------

<name>    ::= r'[a-z]+'        # given helpers
<word>    ::= r'[a-z0-9]+'
<text>    ::= r'[a-z0-9 ]+'
<digit>   ::= r'[0-9]'
<hex>     ::= r'[0-9a-f]'
