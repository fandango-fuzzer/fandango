<start> ::= <Client:request><Server:challenge><Client:resolve><Server:validate>;
<request> ::= '{}';
<challenge> ::= '{"nr_high":' <number_high>',"nr_low":' <number_low>'}';
<resolve> ::= '{"nr":' <number> '}';
<validate> ::= '{"result":true}';
<number_high> ::= <number>;
<number_low> ::= <number>;
<number> ::= <digit_start> <digit_tail>*;
<digit_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;
<digit_tail> ::= '0' | <digit_start>;

int(<challenge>.<number_high>) > int(<resolve>.<number>);
int(<challenge>.<number_low>) < int(<resolve>.<number>);

import requests
import json

class Client(FandangoAgent):

        def __init__(self):
            super().__init__(True)

        def on_send(self, message: str, response_setter: Callable[[str, str], None]):
            x = requests.post("http://127.0.0.1:5000/api/hello", json = json.loads(message))
            response_setter("Server", x.text.strip())

class Server(FandangoAgent):

        def __init__(self):
            super().__init__(False)
