# <ok> after <a> is in the grammar, but the server always answers <a> with <err>.
# <after_ok> can only be reached behind that <ok>, so the guider keeps aiming for it.
# <note> is in the grammar, but the server always answers <bye> with <done>.
# Blocking <note> leaves <notes> deriving nothing, so <closing> gets an Option around <done>.
<start> ::= <Fuzzer:Extern:hello> <rule> <closing> <Fuzzer:Extern:quit>
<rule> ::= (<Fuzzer:Extern:a> <Extern:Fuzzer:ok> <after_ok>) | (<Fuzzer:Extern:a> <Extern:Fuzzer:err>) | (<Fuzzer:Extern:c> <Extern:Fuzzer:ok>)
<after_ok> ::= <Fuzzer:Extern:x>+
<closing> ::= <Fuzzer:Extern:bye> (<notes> | <Extern:Fuzzer:done>)
<notes> ::= <Extern:Fuzzer:note>*
<hello> ::= 'hello\n'
<quit> ::= 'quit\n'
<a> ::= 'a\n'
<c> ::= 'c\n'
<x> ::= 'x\n'
<ok> ::= 'ok\n'
<err> ::= 'err\n'
<bye> ::= 'bye\n'
<done> ::= 'done\n'
<note> ::= 'note\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: DerivationTree, recipient: str):
        if str(message) == "a\n":
            self.receive("err\n", "Extern")
        elif str(message) == "c\n":
            self.receive("ok\n", "Extern")
        elif str(message) == "bye\n":
            self.receive("done\n", "Extern")

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
