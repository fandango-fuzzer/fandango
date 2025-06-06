<start> ::= <Client:Server:request><Server:Client:challenge><Client:Server:resolve><Server:Client:validate>
<request> ::= '{}'
<challenge> ::= '{"nr_high":' <number_high>',"nr_low":' <number_low>'}'
<resolve> ::= '{"nr":' <number> '}'
<validate> ::= '{"result":true}'
<number_high> ::= <number>
<number_low> ::= <number>
<number> ::= <digit_start> <digit_tail>*
<digit_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<digit_tail> ::= '0' | <digit_start>

where int(<challenge>.<number_high>) > int(<resolve>.<number>)
where int(<challenge>.<number_low>) < int(<resolve>.<number>)
where int(<challenge>.<number_low>) < int(<challenge>.<number_high>) + 1

import requests
import json

class Client(FandangoParty):

        def __init__(self):
            super().__init__(True)

        def on_send(self, message: DerivationTree, recipient: str):
            x = requests.post("http://127.0.0.1:5000/api/hello", json = json.loads(message.to_string()))
            self.receive_msg("Server", x.text.strip())

class Server(FandangoParty):

        def __init__(self):
            super().__init__(False)
