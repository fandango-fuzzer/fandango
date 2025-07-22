<start> ::= <Fuzzer:Extern:ping><Extern:Fuzzer:pong><Fuzzer:Extern:puff><Extern:Fuzzer:paff>
<ping> ::= 'ping\n'
<pong> ::= 'pong\n'
<puff> ::= 'puff\n'
<paff> ::= 'paff\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(ownership=Ownership.FANDANGO_PARTY)

    def on_send(
        self,
        message: DerivationTree,
        recipient: str
    ):
        if str(message) == "ping\n":
            self.receive_msg("Extern", "pong\n")
        elif str(message) == "puff\n":
            self.receive_msg("Extern", "paff\n")

class Extern(FandangoParty):
    def __init__(self):
        super().__init__(ownership=Ownership.EXTERNAL_PARTY)