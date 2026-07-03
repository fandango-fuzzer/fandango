# FDP stage 1: grammar only, no constraints (text protocol).
# Structurally correct lines: the FDP anchor, a valid version and message type,
# and a payload of key=value records. One alternative per message kind binds a
# type to the payload it expects.
#
# BUT <len> and <crc> are still free tokens, so every line is rejected at the
# validation stage (length mismatch or bad checksum). This reaches the parser
# but not the handlers: it is the "why constraints" motivation, live.
#
# A generated line looks like:  FDP1 LOGIN user=alice LEN=73 CRC=0af3

<start>   ::= <message>
<message> ::= <ver> " " <body> " LEN=" <len> " CRC=" <crc>

<ver>     ::= "FDP1" | "FDP2"                        # anchor + version (alternatives)

# body = "<TYPE> <payload>"; one alternative per message kind.
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
