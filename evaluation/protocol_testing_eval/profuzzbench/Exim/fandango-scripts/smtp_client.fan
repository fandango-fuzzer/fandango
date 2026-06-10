include('smtp.fan')

# The client connects to the Exim daemon under test (started by run_fandango.sh).
# The server side is EXTERNAL: its responses are read from the real Exim server
# and parsed against the grammar.
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://127.0.0.1:8025"
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://127.0.0.1:8025"
        )
        self.start()
