include('ftp.fan')
import os

PORT = int(os.environ.get("FTP_PORT", "2200"))
CONTROL_URI = f"tcp://127.0.0.1:{PORT}"
DATA_URI = "tcp://127.0.0.1:50100"


class ClientControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri=CONTROL_URI,
        )
        self.start()


class ServerControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.OPEN,
            uri=CONTROL_URI,
        )
        self.start()

    def receive(self, message: str | bytes | None, sender: Optional[str]) -> None:
        if message is None:
            return
        super().receive(message.decode("utf-8"), sender="ClientControl")


class ClientData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri=DATA_URI,
        )


class ServerData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.OPEN,
            uri=DATA_URI,
        )

    def receive(self, message: str | bytes | None, sender: Optional[str]) -> None:
        if message is None:
            super().receive("999 Data socket closed.\r\n", sender="SocketControlClient")
            return
        super().receive(message.decode("utf-8"), sender="ClientData")


class SocketControlServer(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message: str | bytes, recipient: Optional[str]) -> None:
        if str(message).startswith("999"):
            ServerData.instance().stop()

    def start(self):
        pass

    def stop(self):
        pass


class SocketControlClient(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def start(self):
        pass

    def stop(self):
        pass
