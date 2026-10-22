<start> ::= <state>
<state> ::= <Fuzzer:x> <end_state> | <Fuzzer:y> <inner> | <Fuzzer:z> <end_state>
<inner> ::= <Fuzzer:p> <end_state> | <Fuzzer:q> <end_state>
<end_state> ::= <Fuzzer:done>

<x> ::= "x"
<y> ::= "y"
<z> ::= "z"
<p> ::= "p"
<q> ::= "q"
<done> ::= "d"


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)
