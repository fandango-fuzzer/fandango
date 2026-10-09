<start> ::= <exchange>{1,4}
<exchange> ::= <ping> | <hello> | <bye>
<ping> ::= <Client:Server:ping_request> <Server:Client:pong>
<hello> ::= <Client:Server:hello_request> <Server:Client:hi>
<bye> ::= <Client:Server:bye_request> <Server:Client:ok>
<ping_request> ::= 'PING;'
<hello_request> ::= 'HELLO;'
<bye_request> ::= 'BYE;'
<pong> ::= 'PONG;'
<hi> ::= 'HI;'
<ok> ::= 'OK;'

REPLIES = {}
MAX_SENT = 60

class Client(FandangoParty):
    sent = 0

    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message, recipient):
        Client.sent += 1
        if Client.sent > MAX_SENT:
            raise TooManyMessages()
        reply = REPLIES.get(str(message), "ERR;")
        if reply:
            self.io_instance.add_receive("Server", "Client", reply)

    def stop(self):
        pass

class Server(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def stop(self):
        pass

class TooManyMessages(Exception):
    pass
