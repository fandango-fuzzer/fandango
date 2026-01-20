
<start> ::= <Client:request><Server:response>

<request> ::= '/quotes/' <request_number>
<response> ::= '[' <quote> (', ' <quote>)* ']'
<quote> ::= '{"id": "' <number> '", "quote": "' <quote_string> '"}'
<quote_string> ::= r'(?:[^"\\]|\\["\\/bfnrt]|\\u[0-9a-fA-F]{4})*'

where len(<response>.find_all_trees(NonTerminal('<quote>'))) == int(<request>.<request_number>)

<number> ::= r'[0-9]+'
<request_number> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

import json
import requests
class Client(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)
        self.url = "https://dune-api-a4iq.onrender.com"

    def send(self, message: DerivationTree, recipient: str):
        response = requests.get(self.url + message.to_string())
        self.receive(json.dumps(response.json()), sender="Server")

    def start(self):
        pass

    def stop(self):
        pass

class Server(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self):
        pass

    def stop(self):
        pass