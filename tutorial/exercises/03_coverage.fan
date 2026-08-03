# EXERCISE 3a - Execution feedback: maximise coverage of the WHOLE population
#
# WHERE WE ARE
#   After Exercise 2 every input is well-formed and reaches the target's
#   handlers. But generate a few batches and you'll notice they are lopsided -
#   several LOGINs, say, and little else. Each input is fine on its own, yet the
#   SUITE is narrow: as a group these inputs exercise only a slice of the target.
#
# THE GOAL
#   Maximise the coverage of the whole population - not of one input, but of the
#   batch taken together. We want inputs that between them reach as many
#   different parts of the target as possible. An input that only re-treads what
#   other inputs already cover is not pulling its weight; an input that reaches
#   something new is valuable.
#
# THE FEEDBACK SIGNAL
#   The target reports, for every message, the list of internal "branches" it
#   drove through (these are the fdp._mark(...) checkpoints in fdp.py). fdp_cover
#   runs a message through the target and reads that branch trace back - this is
#   behavioural feedback, no slow line-by-line tracing. It also keeps a shared
#   record, in a temporary file, of every branch the population has covered so
#   far, so each new message can be judged against everything accepted before it.
#
#   fdp_cover exposes one helper that uses that record as a gate:
#     - the message reaches a branch NOTHING has covered yet -> accept (and
#       remember the new branches, so the next message must find something else)
#     - the message only re-treads already-covered branches  -> reject
#   Redundant inputs are turned away; every accepted input adds coverage. That
#   is what pushes the population to spread across the target.
#
# Your Exercise 2 spec is carried forward by the include() below: its grammar
# and its three well-formedness constraints are already in force here, so this
# file adds only the feedback constraint.
#
# Read:  README.md ("Execution feedback"), and fdp_cover.py to find that helper
# Docs:  the feedback here is a where-constraint in Python -> https://fandango-fuzzer.github.io/Constraints.html
# Run:   fandango fuzz -f exercises/03_coverage.fan -n 5
# Validate: python fdp_validate.py --step feedback --spec exercises/03_coverage.fan
#
# WHAT TO EXPECT
#   With the constraint in place, `-n 5` returns five DIFFERENT messages - one
#   per body type (LOGIN, MSG, SUB, PING, QUIT) - which together reach every
#   branch a single message can. That is the whole population covering
#   everything it is able to.
#
#   Why exactly five? The deep apply branches (apply:authed / apply:sub /
#   apply:msg / apply:quit) are gated behind a prior LOGIN, so a single message
#   on a fresh session can never reach them. What remains is one distinct branch
#   per body type, so there are exactly FIVE inputs that each grow the coverage
#   union and no sixth that can.
#
#   IMPORTANT: size `-n` to that ceiling and use `-n 5` here. `covers_new` is a
#   hard gate, so once those five pioneers exist nothing else satisfies it.
#   Asking for more (say `-n 6` or `-n 20`) is unsatisfiable, and Fandango does
#   NOT stop and print the few it found: it keeps searching to its generation
#   budget and prints nothing at all. That is a property of gating coverage as a
#   `where` constraint, since the satisfiable population is finite, so match `-n`
#   to it (five).

include('02_constraints.fan')

# ---------------------------------------------------------------------------
# TODO (execution feedback): add a `where` constraint that admits an input only
#   if it grows the population's coverage - i.e. it reaches a branch no
#   already-accepted input has. This one line is what makes the batch spread
#   across the target instead of cloning a single accept path.
#
#   Find the fdp_cover helper that performs this population-coverage check for a
#   message, and apply it to the whole message line (the string of <start>).
# where
# ---------------------------------------------------------------------------

import fdp_cover
