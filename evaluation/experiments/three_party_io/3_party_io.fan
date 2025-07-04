<start> ::= <Client:ServerA:request><ServerA:ServerB:challenge_ab><ServerB:ServerA:challenge_ba><ServerA:Client:challenge_c><Client:ServerA:resolve><ServerA:Client:validate>
<request> ::= '{}'
<challenge_ab> ::= '{"nr_high":' <number_high>',"nr_low":' <number_low>'}'
<challenge_ba> ::= '{"nr_high":' <number_high>',"nr_low":' <number_low>',"nr_mid":' <number_mid>'}'
<challenge_c> ::= '{"nr_high":' <number_high>',"nr_low":' <number_low>',"nr_mid":' <number_mid>'}'
<resolve> ::= '{"nr":' <number> '}'
<validate> ::= '{"result":true}'
<number_high> ::= <number>
<number_low> ::= <number>
<number_mid> ::= <number>
<number> ::= <digit_start> <digit_tail>*
<digit_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<digit_tail> ::= '0' | <digit_start>

where 100 >= int(<number_high>)
where int(<number_high>) > (int(<number_low>) + 3)
where int(<challenge_ab>.<number_high>) == int(<challenge_ba>.<number_high>)
where int(<challenge_ab>.<number_high>) == int(<challenge_c>.<number_high>)
where int(<challenge_ab>.<number_low>) == int(<challenge_ba>.<number_low>)
where int(<challenge_ab>.<number_low>) == int(<challenge_c>.<number_low>)
where int(<challenge_ba>.<number_mid>) == int(<challenge_c>.<number_mid>)
where int(<number_mid>) > (int(<number_low>) + 1)
where int(<number_high>) > (int(<number_mid>) + 1)
where (int(<number_high>) > int(<resolve>.<number>) and int(<resolve>.<number>) > int(<number_mid>)) or (int(<number_mid>) > int(<resolve>.<number>) and int(<resolve>.<number>) > int(<number_low>))

import requests
import json

class Client(FandangoParty):

        def __init__(self):
            super().__init__(True)

        def on_send(self, message: str, recipient: str):
            x = requests.post("http://127.0.0.1:8080/api/hello", json = json.loads(message))
            self.receive_msg("ServerA", x.text.strip())

class ServerA(FandangoParty):

        def __init__(self):
            super().__init__(True)

        def on_send(self, message: str, recipient: str):
            x = requests.post("http://127.0.0.1:8081/api/hello", json = json.loads(message))
            self.receive_msg("ServerB", x.text.strip())

class ServerB(FandangoParty):

        def __init__(self):
            super().__init__(False)
