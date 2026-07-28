<start> ::= <Client:hello> <after_hello> <Client:join>
<after_hello> ::= (<upload> || <heartbeat> || <fun>)

<upload> ::= <Client:Server:put> <Server:Client:stored> <Client:Server:commit> <Server:Client:committed>
<heartbeat> ::= <Client:Server:ping> <Server:Client:pong>
<fun> ::= <Client:Server:fun_talk> <Server:Client:fun_answer>

<hello> ::= 'HELLO\n'
<put> ::= 'PUT report.txt\n'
<stored> ::= 'STORED report.txt\n'
<commit> ::= 'COMMIT report.txt\n'
<committed> ::= 'COMMITTED report.txt\n'
<join> ::= 'JOIN\n'
<fun_talk> ::= 'FUN\n'
<fun_answer> ::= 'FUN ANSWER\n'

<ping> ::= 'PING\n'
<pong> ::= 'PONG\n'


class Client(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: DerivationTree, recipient: str):
        replies = {
            "PUT report.txt\n": "STORED report.txt\n",
            "COMMIT report.txt\n": "COMMITTED report.txt\n",
            "PING\n": "PONG\n",
        }
        reply = replies.get(str(message))
        if reply is not None:
            self.receive(reply, "Server")


class Server(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)
