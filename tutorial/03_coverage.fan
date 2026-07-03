# FDP stage 3a: constraints + execution feedback (maximise coverage).
# Same well-formed frames as stage 2, plus one execution-feedback constraint:
# each input must drive through at least 11 distinct branches of the target,
# i.e. all the way to a terminal handler (a full accept path), not just up to
# the auth guard. Feedback is behavioural: the constraint RUNS fdp.process and
# reads back the branch trace the target records about itself (no sys.settrace,
# so it stays fast inside Fandango's search loop).

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

# execution feedback: reward inputs that reach a terminal handler branch.
where fdp_cover.cover_count(str(<start>)) >= 11

import fdp
import fdp_cover
