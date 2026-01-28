include('smtp.fan')

class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://localhost:8025"
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.OPEN,
            uri="tcp://localhost:8025"
        )
        self.start()
