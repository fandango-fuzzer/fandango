include('ftp.fan')

# The classes ClientControl and ServerControl are the party definitions for the control connection.
class ClientControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://[::1]:25521"
        )
        self.start()

    def send(self, message: str | bytes, recipient: Optional[str]) -> None:
        if str(message).startswith("LIST"):
            ClientData.instance().start()
        super().send(message, recipient)

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        # 150 indicates the start of a data transfer. We start the data parties then in order to connect to the ftp servers data socket.
        if message.decode("utf-8").startswith("226"):
            ClientData.instance().stop()
        # We set ServerControl as the sender for all received messages.
        # Fandango can only automatically infer the sender of a message for specification 2 two party definitions.
        # In this specification we have 4 parties, so we need to set the sender incoming messages manually.
        super().receive(message.decode("utf-8"), sender="ServerControl")


class ServerControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://[::1]:25522"
        )
        self.start()

# The classes ClientData and ServerData are the party definitions for the data connection.
class ClientData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://[::1]:50100"
        )

    # Tell FANDANGO that all received messages come from ServerData.
    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ServerData")


class ServerData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://[::1]:50100"
        )
