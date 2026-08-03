# EXERCISE 4b - Interactive protocol fuzzing (fandango talk)
#
# Goal: turn the session into a live, two-party interaction. Fandango plays the
# client; fdp_server.py is the server. <In:x> is a message Fandango SENDS;
# <Out:y> is a reply it RECEIVES and must match. You write the interaction
# itself; everything else is carried forward or given.
#
# Your Exercise 4a spec is carried forward by the include() below - the message
# rules, the per-message LEN/CRC constraints, and the stateful cross-message
# constraint you wrote there all still apply. Two things change for a live
# conversation, and both are given: every message now ends in a newline (the
# server reads one line at a time), and the server's replies get rules of their
# own so Fandango can recognise them.
#
# Read:  docs/FDP-SPEC.txt, section 7; README.md ("The live protocol demo")
# Docs:  party communication (talk) -> https://fandango-fuzzer.github.io/Parties.html
#        building one spec on another -> https://fandango-fuzzer.github.io/Hatching.html
# Run:   fandango -v talk -f exercises/04b_protocol.fan -n 1 python fdp_server.py

# When it works, the whole conversation is logged as it progresses:
#
#     In:  <login>    'FDP1 LOGIN user=... LEN=... CRC=...'
#     Out: <ok_login> 'OK_LOGIN ...'
#     ...             (the SUB and MSG exchanges)
#     Out: <ok_quit>  'OK_QUIT delivered=1'
#
# A WARNING about "population size reduced to 1" is expected and harmless.

# Info:
# If the server's reply does not match the <Out:...> you predicted, Fandango
# stops with "Could not parse received message fragments". Look for the
# "Received messages:" line in that error: it shows what the server actually
# said (e.g. an ERR_* code) - that reply is your bug report.

# Validate: python fdp_validate.py --step protocol --spec exercises/04a_session.fan
#           (grades the protocol block via 4a, the measurement form. This live
#           variant is checked by the conversation above completing.)

include('04a_session.fan')

# ---------------------------------------------------------------------------
# TODO: define <start> as the exchange, alternating what Fandango SENDS and what
#       the server REPLIES, in this order:
#
#         -> login   <- ok_login
#         -> sub     <- ok_sub
#         -> msg     <- ok_msg
#         -> quit    <- ok_quit
#
#       A sent message wraps its nonterminal in <In:...>; an expected reply
#       wraps its nonterminal in <Out:...>. The message and reply nonterminals
#       are all defined below.
#
#       Replace the placeholder line: it exists only so an unfinished exercise
#       fails with a clear "undefined symbol" instead of silently reusing the
#       non-interactive <start> that 4a defines.
<start> ::= <TODO_write_the_exchange_here>
# ---------------------------------------------------------------------------

# The four messages again, now newline-terminated: `talk` sends one line per
# message, where 4a joined them with "\n" inside <start>. Redefining a rule
# from an included spec overrides it (given).
<login> ::= "FDP1 " <b_login> " LEN=" <l1> " CRC=" <c1> "\n"
<sub>   ::= "FDP1 " <b_sub>   " LEN=" <l2> " CRC=" <c2> "\n"
<msg>   ::= "FDP1 " <b_msg>   " LEN=" <l3> " CRC=" <c3> "\n"
<quit>  ::= "FDP1 " <b_quit>  " LEN=" <l4> " CRC=" <c4> "\n"

# What the server is expected to say back (given).
<ok_login> ::= "OK_LOGIN " <rest> "\n"
<ok_sub>   ::= "OK_SUB " <rest> "\n"
<ok_msg>   ::= "OK_MSG " <rest> "\n"
<ok_quit>  ::= "OK_QUIT " <rest> "\n"
<rest>     ::= r'[^\n]*'
