<start> ::= <smtp>
<smtp> ::= <Server:m220> <Client:quit> <Server:m221>
<m220> ::= "220 " <hostname> " " r".*" "\r\n"
<quit> ::= "QUIT\r\n"
<m221> ::= "221 " r".*" "\r\n"

<hostname> ::= r"[-a-zA-Z0-9.:]*" := "host.example.com"
