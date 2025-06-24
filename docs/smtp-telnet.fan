<start> ::= <Out:telnet_intro> <smtp>
<telnet_intro> ::= \
    r"Trying.*" "\r\n" \
    r"Connected.*" "\r\n" \
    r"Escape.*" "\r\n"

<smtp> ::= <Out:m220> <In:quit> <Out:m221>
<m220> ::= "220 " r".*" "\r\n"
<quit> ::= "QUIT\r\n"
<m221> ::= "221 " r".*" "\r\n"
