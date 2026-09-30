# <ok> after <a> is in the grammar, but the server always answers <a> with <err>.
# <after_ok> can only be reached behind that <ok>, so the guider keeps aiming for it.
<start> ::= <Fuzzer:Extern:hello> <rule> <Fuzzer:Extern:quit>
<rule> ::= (<Fuzzer:Extern:a> <Extern:Fuzzer:ok> <after_ok>) | (<Fuzzer:Extern:a> <Extern:Fuzzer:err>) | (<Fuzzer:Extern:c> <Extern:Fuzzer:ok>)
<after_ok> ::= <Fuzzer:Extern:x>
<hello> ::= 'hello\n'
<quit> ::= 'quit\n'
<a> ::= 'a\n'
<c> ::= 'c\n'
<x> ::= 'x\n'
<ok> ::= 'ok\n'
<err> ::= 'err\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: DerivationTree, recipient: str):
        if str(message) == "a\n":
            self.receive("err\n", "Extern")
        elif str(message) == "c\n":
            self.receive("ok\n", "Extern")

    def start(self):
        pass

    def stop(self):
        pass


class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self):
        pass

    def stop(self):
        pass
