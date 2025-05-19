
<start> ::= <Client:request><Server:response>

<request> ::= '/quotes/' <number>
<response> ::= '[' <quote> (', ' <quote>)* ']'
<quote> ::= '{\'id\': \'' <number> '\', \'quote\': \'' <quote_string> '\'}'
<quote_string> ::= (r'[a-zA-Z0-9\.\,\?\!\-\:\–\—\’ ]+' | '\'')+

where int(<request>.<number>) > 0 and int(<request>.<number>) < 10
where len(<response>.find_all_trees(NonTerminal('<quote>'))) == int(<request>.<number>)

<number> ::= <number_start> <number_tail>*
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tail> ::= '0' | <number_start>

import json
import requests
class Client(FandangoAgent):
    def __init__(self):
        super().__init__(True)
        if not self.is_fandango():
            return
        self.url = "https://dune-api-a4iq.onrender.com"

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        response = requests.get(self.url + message.to_string())
        self.receive_msg("Server", str(response.json()).replace("\"", '\''))

class Server(FandangoAgent):
    def __init__(self):
        super().__init__(False)