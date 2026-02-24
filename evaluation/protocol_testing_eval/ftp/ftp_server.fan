include('ftp.fan')

# The classes ClientControl and ServerControl are the party definitions for the control connection.
class ClientControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://[::1]:25521"
        )
        self.start()

class ServerControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.OPEN,
            uri="tcp://[::1]:25522"
        )
        self.start()

    # Tell FANDANGO that all received messages come from ClientControl.
    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ClientControl")


# The classes ClientData and ServerData are the party definitions for the data connection.
class ClientData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://[::1]:50100"
        )


class ServerData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.OPEN,
            uri="tcp://[::1]:50100"
        )

    # Tell FANDANGO that all received messages come from ClientData.
    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ClientData")

class SocketControlServer(FandangoParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.OPEN
        )

    def send(self, message: str | bytes, recipient: Optional[str]) -> None:
        if str(message).startswith("Data socket closed.\r\n"):
            ServerData.instance().stop()

    def start(self):
        pass

    def stop(self):
        pass

class SocketControlClient(FandangoParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL
        )

    def start(self):
        pass

    def stop(self):
        pass