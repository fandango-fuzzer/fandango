<start> ::= <Fuzzer:Extern:query> (<Extern:Fuzzer:nt_pass> | <Extern:Fuzzer:nt_fail>)
<query> ::= 'hello'
<nt_pass> ::= 'response'
<nt_fail> ::= 'response'
where str(<nt_fail>) == "world"


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message, recipient):
        # Immediately simulate Extern's reply so the protocol algorithm
        # receives it before waiting for a remote message.
        self.receive("response", "Extern")


class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)