include('ftp-cmds.fan')
import ssl
import time
import types

# The classes ClientControl and ServerControl are the party definitions for the control connection.
class ClientControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://127.0.0.1:2200"
        )
        self.tls_active = False
        self._recv_buffer = b""
        self.start()

    def upgrade_tls(self):
        proto = self.protocol_impl
        raw_sock = proto._connection
        if raw_sock is None:
            print("No active socket yet")
            return
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        proto._running = False
        proto._send_thread.join()
        tls_sock = ctx.wrap_socket(
            raw_sock,
            server_hostname="localhost",
            do_handshake_on_connect=False,
        )
        tls_sock.do_handshake()
        proto._connection = tls_sock
        proto._running = True
        proto._send_thread = threading.Thread(target=proto._listen, daemon=True)
        proto._send_thread.start()
        self.tls_active = True
        ClientData.instance().use_tls = True

    def send(self, message: str | bytes, recipient: Optional[str]) -> None:
        super().send(message, recipient)
        if self.tls_active:
            # Disabled because LightFTP seems to have a bug here
            #if str(message).startswith("PROT C"):
            #    print("DATA TLS DISABLE")
            #    ClientData.instance().use_tls = False
            if str(message).startswith("PROT P"):
                ClientData.instance().use_tls = True

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        if message is None:
            return
        super().receive(message.decode("utf-8"), sender="ServerControl")
        print(message.decode("utf-8"))


class ServerControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://127.0.0.1:2200"
        )
        self.start()

class ClientData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://127.0.0.1:50100"
        )
        self.use_tls = False
        self.protocol_impl._wait_accept = types.MethodType(ClientData._wait_accept, self.protocol_impl)

    def _wait_accept(self) -> None:
        assert self.connection_mode != ConnectionMode.EXTERNAL
        with self._lock:
            if self._connection is None:
                assert self._sock is not None
                self._sock.setblocking(False)
                try:
                    self._sock.connect((self.ip, self.port))
                except BlockingIOError:
                    pass
                while self._running:
                    _, wlist, _ = select.select([], [self._sock], [], 0.01)
                    if wlist:
                        print("SO_ERROR =", self._sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR))
                        self._connection = self._sock
                        self._sock.setblocking(True)
                        if self._party_instance.use_tls:
                            self._sock.setblocking(True)
                            ctx = self._party_instance.io_instance.parties['ClientControl'].protocol_impl._connection.context
                            try:
                                self._connection = ctx.wrap_socket(
                                    self._connection,
                                    server_hostname="localhost",
                                    do_handshake_on_connect=True,
                                )
                            except ConnectionResetError:
                                self._running = False
                        break



    def receive(self, message: str | bytes | None, sender: Optional[str]) -> None:
        if message is None:
            super().receive("999 Data socket closed.\r\n", sender="SocketControlServer")
            print("999 Data socket closed.\r\n")
            print("SocketControlServer: 999 Data socket closed.\r\n")
            return
        super().receive(message.decode("utf-8"), sender="ServerData")
        print(message.decode("utf-8"))


class ServerData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://127.0.0.1:50100"
        )

class SocketControlServer(FandangoParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL
        )

    def start(self):
        pass

    def stop(self):
        pass

class SocketControlClient(FandangoParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT
        )

    def send(self, message: str | bytes, recipient: Optional[str]) -> None:
        if str(message).startswith("999"):
            ClientData.instance().stop()
            ServerData.instance().stop()
        if str(message).startswith("998"):
            ClientControl.instance().upgrade_tls()
        print(str(message))

    def start(self):
        pass

    def stop(self):
        pass

