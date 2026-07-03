# FDP stage 2: grammar + semantic constraints (text protocol).
# Same grammar as stage 1, now made *well-formed* by three constraints:
#   - length encoding: LEN counts the body characters
#   - checksum:        CRC is the CRC-16 over the body
#   - min/max:         the body stays within the size the server accepts
# Now every line passes validation and reaches the message handlers in apply():
# this is the "why constraints unlock behaviour" jump, live.
#
# A generated line now round-trips:  FDP1 LOGIN user=alice LEN=16 CRC=... and
# the server accepts it.

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

# --- semantic constraints ---------------------------------------------------
# length encoding: the LEN token equals the body length.
where str(<len>) == str(len(str(<body>)))

# checksum: the CRC token is the CRC-16/CCITT of the body.
where str(<crc>) == crc16hex(str(<body>))

# min/max: keep the body within the server's accepted window.
where 1 <= len(str(<body>)) <= 64

def crc16hex(text: str) -> str:
    crc = 0xFFFF
    for b in text.encode('ascii'):
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return format(crc, '04x')
