<start> ::= <state>
<state> ::= <exchange> <state> | <exchange>
<exchange> ::= <Fuzzer:cmd> <Extern:reply>
<cmd> ::= <verb> <arg>
<verb> ::= 'GET' | 'PUT'
<arg> ::= <digit>+
<digit> ::= r'[01]'
<reply> ::= <code>
<code> ::= '200' | '404'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)
