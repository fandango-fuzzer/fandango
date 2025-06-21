<start> ::= <smtp>
<smtp> ::= <Server:m220> <Client:helo> <Server:m250> <Client:quit> <Server:m221>
<m220> ::= "220 " <hostname> " " r".*" "\n"
<helo> ::= "HELO " <hostname> "\n"
<m250> ::= "250 " <hostname> " " r".*" "\n"
<quit> ::= "QUIT\n"
<m221> ::= "221 " r".*" "\n"

<hostname> ::= r"[-a-zA-Z0-9.:]*" := "host.example.com"

class Client(ConnectParty):
    def __init__(self):
        super().__init__("localhost:8025", ownership=Ownership.FANDANGO_PARTY)

class Server(ConnectParty):
    def __init__(self):
        super().__init__("localhost:8025", ownership=Ownership.EXTERNAL_PARTY)
