# FDP stage 4 (measurement form): a whole stateful SESSION as one input.
# Four messages for one connection, newline-separated:
#     LOGIN -> SUB -> MSG -> QUIT
# Each message is well-formed (its own LEN and CRC), and one cross-message
# constraint ties the MSG's target to the subscribed channel, so the sequence
# actually reaches the deep handlers (OK_SUB, OK_MSG, OK_QUIT) that NO single
# message can reach. Replayed through one Session by the harness (--session),
# this is the coverage finale: the bar that jumps past the constraint stage.
#
# The live, interactive version of this is 04_protocol.fan + fdp_server.py.

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

# per-message length + checksum (as in stage 2, once per message)
where str(<l1>) == str(len(str(<b_login>)))
where str(<c1>) == fdp.crc16hex(str(<b_login>))
where str(<l2>) == str(len(str(<b_sub>)))
where str(<c2>) == fdp.crc16hex(str(<b_sub>))
where str(<l3>) == str(len(str(<b_msg>)))
where str(<c3>) == fdp.crc16hex(str(<b_msg>))
where str(<l4>) == str(len(str(<b_quit>)))
where str(<c4>) == fdp.crc16hex(str(<b_quit>))

# stateful cross-message constraint: you can only message a channel you joined.
where str(<dest>) == str(<chan>)

import fdp
