# <a> is matched more than ANCESTOR_LOOKBACK symbols above the cheap route to <b>, which takes one <p>
# where the shallow alternative takes three.
<start> ::= <a>
<a> ::= <d1> <b> | <Fuzzer:Extern:p> <Fuzzer:Extern:p> <Fuzzer:Extern:p> <b>
<d1> ::= <d2>
<d2> ::= <d3>
<d3> ::= <d4>
<d4> ::= <d5>
<d5> ::= <d6>
<d6> ::= <d7>
<d7> ::= <Fuzzer:Extern:p>
<b> ::= <Fuzzer:Extern:q>
<p> ::= 'p\n'
<q> ::= 'q\n'
class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)
        self.greeted = False

    def send(self, message: DerivationTree, recipient: str):
        if str(message) == "ehlo\n":
            self.greeted = True
            self.receive("ok\n", "Extern")
        elif str(message) == "help\n":
            self.receive("garbage\n" if self.greeted else "helptext\n", "Extern")

    def start(self):
        self.greeted = False

    def stop(self):
        pass


class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self):
        pass

    def stop(self):
        pass
