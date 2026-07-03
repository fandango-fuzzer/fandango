# FDP stage 4 (interactive form): a stateful conversation for `fandango talk`.
# Fandango plays the client, fdp_server.py is the server. <In:x> is a message
# Fandango SENDS to the server; <Out:y> is a reply it RECEIVES. The exchange
# walks the protocol state machine:
#
#     -> LOGIN     <- OK_LOGIN
#     -> SUB       <- OK_SUB
#     -> MSG       <- OK_MSG
#     -> QUIT      <- OK_QUIT
#
# Run it with:
#     fandango talk -f 04_protocol.fan -n 1 ../.venv/bin/python fdp_server.py
#
# The same well-formedness constraints as stage 2 apply to every message, plus
# the stateful cross-message constraint that you can only message a channel you
# have joined. Send them out of order and the server answers ERR_NOAUTH.

<start> ::= <In:login> <Out:ok_login> <In:sub> <Out:ok_sub> <In:msg> <Out:ok_msg> <In:quit> <Out:ok_quit>

<login> ::= "FDP1 " <b_login> " LEN=" <l1> " CRC=" <c1> "\n"
<sub>   ::= "FDP1 " <b_sub>   " LEN=" <l2> " CRC=" <c2> "\n"
<msg>   ::= "FDP1 " <b_msg>   " LEN=" <l3> " CRC=" <c3> "\n"
<quit>  ::= "FDP1 " <b_quit>  " LEN=" <l4> " CRC=" <c4> "\n"

<b_login> ::= "LOGIN user=" <name>
<b_sub>   ::= "SUB chan=" <chan>
<b_msg>   ::= "MSG to=" <dest> "&body=" <text>
<b_quit>  ::= "QUIT"

<ok_login> ::= "OK_LOGIN " <rest> "\n"
<ok_sub>   ::= "OK_SUB " <rest> "\n"
<ok_msg>   ::= "OK_MSG " <rest> "\n"
<ok_quit>  ::= "OK_QUIT " <rest> "\n"
<rest>     ::= r'[^\n]*'

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

# per-message length + checksum
where str(<l1>) == str(len(str(<b_login>)))
where str(<c1>) == fdp.crc16hex(str(<b_login>))
where str(<l2>) == str(len(str(<b_sub>)))
where str(<c2>) == fdp.crc16hex(str(<b_sub>))
where str(<l3>) == str(len(str(<b_msg>)))
where str(<c3>) == fdp.crc16hex(str(<b_msg>))
where str(<l4>) == str(len(str(<b_quit>)))
where str(<c4>) == fdp.crc16hex(str(<b_quit>))

# stateful cross-message constraint: only message a channel you joined.
where str(<dest>) == str(<chan>)

import fdp
