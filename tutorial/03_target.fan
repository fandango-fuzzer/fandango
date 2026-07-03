# FDP stage 3b: constraints + execution feedback (hit a specific branch).
# Directed testing: every input must drive the server through the "apply:login"
# branch, i.e. be a message the server actually accepts as a login. Feedback is
# behavioural: the constraint RUNS fdp.process and checks the recorded trace.
#
# Swap the target label to steer elsewhere, e.g. "apply:pong" (only PING),
# or use fdp_cover.response(str(<start>)) == "ERR_NOAUTH" for negative testing
# (well-formed privileged messages sent with no session).

<start>   ::= <message>
<message> ::= <ver> " " <body> " LEN=" <len> " CRC=" <crc>

<ver>     ::= "FDP1" | "FDP2"

<body>      ::= <login> | <message_msg> | <subscribe> | "PING" | "QUIT"
<login>       ::= "LOGIN user=" <name> <passopt>
<passopt>     ::= "&pass=" <word> | ""
<message_msg> ::= "MSG to=" <name> "&body=" <text>
<subscribe>   ::= "SUB chan=" <name>

<len>     ::= <digit>+
<crc>     ::= <hex>{4}

<name>    ::= r'[a-z]+'
<word>    ::= r'[a-z0-9]+'
<text>    ::= r'[a-z0-9 ]+'
<digit>   ::= r'[0-9]'
<hex>     ::= r'[0-9a-f]'

# well-formedness (as in stage 2)
where str(<len>) == str(len(str(<body>)))
where str(<crc>) == fdp.crc16hex(str(<body>))
where 1 <= len(str(<body>)) <= 64

# execution feedback: demand each input execute a specific target branch.
where fdp_cover.reaches(str(<start>), "apply:login")

import fdp
import fdp_cover
