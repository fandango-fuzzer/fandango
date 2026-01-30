<start> ::= <Fuzzer:Extern:ping><Extern:Fuzzer:pong><Fuzzer:Extern:puff><Extern:Fuzzer:paff>
<ping> ::= 'ping\n'
<pong> ::= 'pong\n'
<puff> ::= 'puff\n'
<paff> ::= 'paff\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(
        self,
        message: DerivationTree,
        recipient: str
    ):
        if str(message) == "ping\n":
            self.receive("pong\n", "Extern")
        elif str(message) == "puff\n":
            self.receive("paff\n", "Extern")

class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)