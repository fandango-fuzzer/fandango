<start> ::= <exchange>{1,3}
<exchange> ::= <Fuzzer:Extern:note> <Extern:Fuzzer:note>
<note> ::= 'A\n' | 'B\n' | 'C\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: DerivationTree, recipient: str):
        self.receive(str(message), "Extern")


class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)
