
<start> ::= <test>
<test> ::= <Fuzzer:A> (<state_1> <state_2> | <state_3> <state_4> <start> | <Fuzzer:G> | " ") <Fuzzer:H>
<state_1> ::= <Fuzzer:C>
<state_2> ::= <Fuzzer:B>
<state_3> ::= <state_5>
<state_4> ::= <Extern:E>
<state_5> ::= <Extern:D> | <Fuzzer:G>

<A> ::= "a"
<B> ::= "b"
<C> ::= "c"
<D> ::= "d"
<E> ::= "e"
<F> ::= "f"
<G> ::= "g"
<H> ::= "h"



class Fuzzer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

class Extern(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)