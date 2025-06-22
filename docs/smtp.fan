<start> ::= <smtp>
<smtp> ::= <Server:m220> <Client:helo> <Server:m250> <Client:quit> <Server:m221>
<m220> ::= "220 " <hostname> " " r".*" "\r\n"
<helo> ::= "HELO " <hostname> "\r\n"
<m250> ::= "250 " <hostname> " " r".*" "\r\n"
<quit> ::= "QUIT\r\n"
<m221> ::= "221 " r".*" "\r\n"

<hostname> ::= r"[-a-zA-Z0-9.:]*" := "host.example.com"

fandango_is_client = True

# class Client(ConnectParty):
#     def __init__(self):
#         super().__init__("localhost:8025", ownership=Ownership.FANDANGO_PARTY,
#         endpoint_type=EndpointType.CONNECT)
#         self.start()

# class Server(ConnectParty):
#     def __init__(self):
#         super().__init__("localhost:8025", ownership=Ownership.EXTERNAL_PARTY)
#         endpoint_type=EndpointType.CONNECT,
#         self.start()

class Client(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY if fandango_is_client else Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT,
            uri="tcp://localhost:8025"
        )
        self.start()

class Server(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.EXTERNAL_PARTY if fandango_is_client else Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.OPEN,
            uri="tcp://localhost:9025"
        )
        self.start()
