# No <cmd> satisfies the constraint, so the fuzzer can never send the second message of a session.
<start> ::= <Fuzzer:Extern:hello> <Fuzzer:Extern:cmd> <Extern:Fuzzer:ok>
<cmd> ::= 'cmd ' <digit> '\n'
<hello> ::= 'hello\n'
<ok> ::= 'ok\n'

where int(str(<cmd>.<digit>)) > 9


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: DerivationTree, recipient: str):
        if str(message).startswith("cmd "):
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
