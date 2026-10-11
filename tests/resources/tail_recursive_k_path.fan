# Tail recursion: the <p> below <P> has the same future at every depth of <S>, and the same last matches of
# (<S>, <S>, <P>, <q>), as more than ANCESTOR_LOOKBACK symbols lie between. Only from depth 2 on can <q> complete it.
<start> ::= <S>
<S> ::= <Fuzzer:Extern:a> <S> | <P>
<P> ::= <d1> <Fuzzer:Extern:q>
<d1> ::= <d2>
<d2> ::= <d3>
<d3> ::= <d4>
<d4> ::= <d5>
<d5> ::= <d6>
<d6> ::= <d7>
<d7> ::= <Fuzzer:Extern:p>
<a> ::= 'a\n'
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
