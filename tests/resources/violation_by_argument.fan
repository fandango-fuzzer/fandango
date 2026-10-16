# The server answers <cmd> within the grammar, unless its argument is <bad>: then it sends something the grammar does
# not allow. Whether <cmd> violates depends on its content.
<start> ::= <Fuzzer:Extern:hello> <state>
<state> ::= (<exchange_cmd> <state>) | <Fuzzer:Extern:quit>
<exchange_cmd> ::= <Fuzzer:Extern:cmd> <Extern:Fuzzer:ok>
<cmd> ::= 'cmd ' <argument> '\n'
<argument> ::= <good> | <bad>
<good> ::= 'a' | 'b' | 'c'
<bad> ::= '!'
<hello> ::= 'hello\n'
<quit> ::= 'quit\n'
<ok> ::= 'ok\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: DerivationTree, recipient: str):
        if str(message).startswith("cmd "):
            self.receive("boom\n" if "!" in str(message) else "ok\n", "Extern")

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
