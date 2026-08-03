# EXERCISE 4a - A stateful session (measurement form)
#
# Goal: build a whole conversation as ONE input: four messages for one
# connection, newline-separated, in the order the protocol requires. This is
# what reaches the deep handlers (OK_SUB, OK_MSG, OK_QUIT) that no single
# message can. The per-message length/checksum constraints are given; you add
# the sequence and the one stateful cross-message constraint.
#
# Read:  docs/FDP-SPEC.txt, section 7 (session state machine)
# Docs:  testing protocols -> https://fandango-fuzzer.github.io/Protocols.html
# Run:   python fdp_harness.py --spec exercises/04a_session.fan --n 200
# Validate: python fdp_validate.py --step protocol --spec exercises/04a_session.fan

# ---------------------------------------------------------------------------
# TODO 1: define <start> as the four messages in order - LOGIN, then SUB, then
#         MSG, then QUIT - concatenated with a newline ("\n") between each.
#         The four nonterminals (<login>, <sub>, <msg>, <quit>) are defined
#         just below.
# <start> ::=
# ---------------------------------------------------------------------------

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

# per-message length + checksum (given: one pair per message)
where str(<l1>) == str(len(str(<b_login>)))
where str(<c1>) == fdp.crc16hex(str(<b_login>))
where str(<l2>) == str(len(str(<b_sub>)))
where str(<c2>) == fdp.crc16hex(str(<b_sub>))
where str(<l3>) == str(len(str(<b_msg>)))
where str(<c3>) == fdp.crc16hex(str(<b_msg>))
where str(<l4>) == str(len(str(<b_quit>)))
where str(<c4>) == fdp.crc16hex(str(<b_quit>))

# min/max (as in stage 2): keep every body within the server's accepted
# window. (<b_quit> is the constant "QUIT", nothing to bound.)
where 1 <= len(str(<b_login>)) <= 64
where 1 <= len(str(<b_sub>)) <= 64
where 1 <= len(str(<b_msg>)) <= 64

# ---------------------------------------------------------------------------
# TODO 2 (stateful constraint): you can only message a channel you joined. Add
#        a constraint that ties the MSG target (<dest>) to the SUB channel
#        (<chan>) so they are always equal - this is the cross-message link
#        that makes the conversation valid.
# where
# ---------------------------------------------------------------------------

import fdp
