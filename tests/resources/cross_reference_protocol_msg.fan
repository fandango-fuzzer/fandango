<start> ::= <Party:msg_a><Party:msg_b>
<msg_a> ::= 'example'
<msg_b> ::= <msg_a>

class Party(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(
        self,
        message: DerivationTree,
        recipient: str
    ):
        pass
        
