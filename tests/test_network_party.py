import socket
import time
from typing import Optional

import pytest

from fandango.errors import FandangoError
from fandango.io import ConnectionMode, FandangoIO, NetworkParty, UdpTcpProtocolImplementation

GREETING = b"220 ready\r\n"


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


class RecordingClient(NetworkParty):
    def __init__(self, port: int):
        super().__init__(
            f"tcp://127.0.0.1:{port}", connection_mode=ConnectionMode.CONNECT
        )
        self.received: list[str | bytes] = []

    def receive(self, message: str | bytes | None, sender: Optional[str]) -> None:
        if message is not None:
            self.received.append(message)


def test_a_client_waits_for_server_socket() -> None:
    port = free_port()
    client = RecordingClient(port)
    client.start()
    try:
        time.sleep(0.2)
        with socket.socket() as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("127.0.0.1", port))
            server.listen(1)
            server.settimeout(5)
            connection, _ = server.accept()
            with connection:
                connection.sendall(GREETING)
                deadline = time.monotonic() + 5
                while not client.received and time.monotonic() < deadline:
                    time.sleep(0.01)
        assert client.received == [GREETING]
    finally:
        client.stop()
        FandangoIO.instance().parties.pop(client.party_name, None)


def test_a_server_socket_not_reachable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(UdpTcpProtocolImplementation, "CONNECT_TIMEOUT_S", 0.3)
    client = RecordingClient(free_port())
    client.start()
    try:
        started = time.monotonic()
        with pytest.raises(FandangoError, match="could not connect"):
            client.send(b"NOOP\r\n", None)
        assert time.monotonic() - started < 5
    finally:
        client.stop()
        FandangoIO.instance().parties.pop(client.party_name, None)
