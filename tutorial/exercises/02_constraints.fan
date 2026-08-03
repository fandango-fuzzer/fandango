# EXERCISE 2 - Semantic constraints
#
# Goal: make the messages WELL-FORMED so the server accepts them. Tie LEN and
# CRC to the body and bound the size; when all three hold, inputs get past
# validation and reach the handlers.
#
# Your grammar from Exercise 1 is carried forward by the include() below, so
# this file holds only what is new. Everything you defined there - <body>, the
# message kinds, their records - is in scope here, and the constraints you are
# about to write refer to those very symbols. If Fandango reports an undefined
# symbol, the gap is in your Exercise 1 grammar, not in this file.
#
# Read:  docs/FDP-SPEC.txt, sections 4-5 (LEN and CRC) and Appendix B (CRC algo)
# Docs:  Fandango constraints (where clauses) -> https://fandango-fuzzer.github.io/Constraints.html
#        building one spec on another -> https://fandango-fuzzer.github.io/Hatching.html
# Run:   fandango fuzz -f exercises/02_constraints.fan -n 5
# Validate: python fdp_validate.py --step language --spec exercises/02_constraints.fan
#
# Verify your inputs are accepted:
#   fandango fuzz -f exercises/02_constraints.fan -n 20 --file-mode binary -d /tmp/ex2
#   for f in /tmp/ex2/*; do echo "$(cat "$f")" | python fdp_server.py; done

include('01_grammar.fan')

# ---------------------------------------------------------------------------
# TODO 1 (length encoding): LEN must equal the number of characters in <body>.
#   The fields are text, so compare them as strings (both sides str(...)).
#   See FDP-SPEC section 4.
# where

# TODO 2 (checksum): CRC must equal the CRC-16 of <body>. Do NOT re-derive the
#   algorithm - call the reference implementation in fdp.py (see Appendix B for
#   which helper) on the body, and compare it to <crc>.
# where

# TODO 3 (min/max): keep the body length between 1 and 64 characters.
# where
# ---------------------------------------------------------------------------

import fdp
