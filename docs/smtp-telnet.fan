<start> ::= <Out:telnet_intro> <smtp>
<telnet_intro> ::= \
    r"Trying.*" "\n" \
    r"Connected.*" "\n" \
    r"Escape.*" "\n"

<smtp> ::= <Out:m220> <In:quit> <Out:m221>
<m220> ::= "220 " r".*" "\n"
<quit> ::= "QUIT\n"
<m221> ::= "221 " r".*" "\n"
