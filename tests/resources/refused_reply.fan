# Two exchanges lead to <goal>. The server answers <a> with <err> instead of <ok_a>, <b> with <ok_b>.
<start> ::= <Fuzzer:Extern:hello> <state>
<state> ::= (<exchange_a> <goal>) | (<exchange_b> <goal>) | <Fuzzer:Extern:quit>
<exchange_a> ::= <Fuzzer:Extern:a> <Extern:Fuzzer:ok_a>
<exchange_b> ::= <Fuzzer:Extern:b> <Extern:Fuzzer:ok_b>
<goal> ::= <Fuzzer:Extern:g> <Extern:Fuzzer:done>
<hello> ::= 'hello\n'
<quit> ::= 'quit\n'
<a> ::= 'a\n'
<b> ::= 'b\n'
<g> ::= 'g\n'
<ok_a> ::= 'ok_a\n'
<ok_b> ::= 'ok_b\n'
<done> ::= 'done\n'


class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: DerivationTree, recipient: str):
        if str(message) == "a\n":
            self.receive("err\n", "Extern")
        elif str(message) == "b\n":
            self.receive("ok_b\n", "Extern")
        elif str(message) == "g\n":
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
