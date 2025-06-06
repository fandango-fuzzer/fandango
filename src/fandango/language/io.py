import enum
import select
import socket
import sys
import threading
import time
from typing import Callable, Tuple

from fandango import FandangoError
from fandango.language.tree import DerivationTree


class ProtocolType(enum.Enum):
    TCP = ("TCP",)
    UDP = "UDP"


class EndpointType(enum.Enum):
    SERVER = ("Server",)
    CLIENT = "Client"


class IpType(enum.Enum):
    IPV4 = ("IPv4",)
    IPV6 = "IPv6"


class Ownership(enum.Enum):
    FUZZER = ("Fuzzer",)
    EXTERNAL = "External"


class FandangoParty(object):

    def __init__(self, ownership: Ownership):
        self.class_name = type(self).__name__
        self._ownership = ownership
        FandangoIO.instance().parties[self.class_name] = self

    """
    :return: True, if the party is substituted by fandango.
    """

    @property
    def ownership(self) -> Ownership:
        return self._ownership

    def is_fuzzer_controlled(self) -> bool:
        """
        Returns True if this party is owned by Fandango, False if it is an external party.
        """
        return self.ownership == Ownership.FUZZER

    """
    Called when fandango wants to send a message as this party.
    
    :message: The message to send.
    :response_setter: If the recipient of the message answers during the function call, this method can be called to set the response.
        First parameter of response_setter is the name of the other party. The second is the message, that it answered with.
    """

    def on_send(
        self,
        message: DerivationTree,
        recipient: str,
        response_setter: Callable[[str, str], None],
    ):
        print(f"({self.class_name}): {message.to_string()}")

    """
    Call if a message has been received by this party.
    """

    def receive_msg(self, sender: str, message: str) -> None:
        FandangoIO.instance().add_receive(sender, self.class_name, message)


class SocketParty(FandangoParty):
    def __init__(
        self,
        *,
        ownership: Ownership,
        endpoint_type: EndpointType,
        ip_type: IpType = IpType.IPV4,
        ip: str = "127.0.0.1",
        port: int = 8021,
        protocol_type: ProtocolType = ProtocolType.TCP,
    ):
        super().__init__(ownership)
        self.running = False
        self._ip_type = ip_type
        self._protocol_type = protocol_type
        self._ip = ip
        self._port = port
        self._endpoint_type = endpoint_type
        self.sock = None
        self.connection = None
        self.send_thread = None
        self.lock = threading.Lock()

    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, value: str):
        if self._ip == value:
            return
        self._ip = value

    @property
    def endpoint_type(self) -> EndpointType:
        return self._endpoint_type

    @endpoint_type.setter
    def endpoint_type(self, value: EndpointType):
        if self._endpoint_type == value:
            return
        self._endpoint_type = value

    @property
    def ip_type(self) -> IpType:
        return self._ip_type

    @ip_type.setter
    def ip_type(self, value: IpType):
        if self._ip_type == value:
            return
        self._ip_type = value

    @property
    def protocol_type(self) -> ProtocolType:
        return self._protocol_type

    @protocol_type.setter
    def protocol_type(self, value: ProtocolType):
        if self._protocol_type == value:
            return
        self._protocol_type = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int):
        if self._port == value:
            return
        self._port = value

    def start(self):
        if self.running:
            return
        if not self.is_fuzzer_controlled():
            return
        self.stop()
        self._create_socket()
        self._connect()

    def _create_socket(self):
        protocol = (
            socket.SOCK_STREAM
            if self._protocol_type == ProtocolType.TCP
            else socket.SOCK_DGRAM
        )
        ip_type = socket.AF_INET if self.ip_type == IpType.IPV4 else socket.AF_INET6
        self.sock = socket.socket(ip_type, protocol)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _connect(self):
        if self.endpoint_type == EndpointType.SERVER:
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)
        self.running = True
        self.send_thread = threading.Thread(target=self._listen, daemon=True)
        self.send_thread.daemon = True
        self.send_thread.start()

    def stop(self):
        self.running = False
        if self.send_thread is not None:
            self.send_thread.join()
            self.send_thread = None
        if self.connection is not None:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.connection.close()
            except OSError:
                pass
            self.connection = None
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None

    def wait_accept(self):
        with self.lock:
            if self.connection is None:
                if self.endpoint_type == EndpointType.SERVER:
                    while self.running:
                        rlist, _, _ = select.select([self.sock], [], [], 0.1)
                        if rlist:
                            self.connection, _ = self.sock.accept()
                            break
                else:
                    self.sock.setblocking(False)
                    try:
                        self.sock.connect((self._ip, self._port))
                    except BlockingIOError as e:
                        pass
                    while self.running:
                        _, wlist, _ = select.select([], [self.sock], [], 0.1)
                        if wlist:
                            self.connection = self.sock
                            break
                    self.sock.setblocking(True)

    def _listen(self):
        self.wait_accept()
        if not self.running:
            return

        while self.running:
            try:
                rlist, _, _ = select.select([self.connection], [], [], 0.1)
                if rlist and self.running:
                    data = self.connection.recv(1024)
                    if len(data) == 0:
                        continue  # Keep waiting if connection is open but no data
                    self.receive(data)
            except Exception:
                self.running = False
                break

    def on_send(
        self,
        message: DerivationTree,
        recipient: str,
        response_setter: Callable[[str, str], None],
    ):
        if not self.running:
            raise FandangoError("Socket not running!")
        self.wait_accept()
        self.transmit(message, recipient)

    def transmit(self, message: DerivationTree, recipient: str):
        if message.contains_bits():
            self.connection.sendall(message.to_bytes())
        else:
            self.connection.sendall(message.to_string().encode("utf-8"))

    def receive(self, data: bytes):
        sender = "Client" if self.endpoint_type == EndpointType.SERVER else "Server"
        self.receive_msg(sender, data.decode("utf-8"))


class SocketServer(SocketParty):
    def __init__(
        self,
        *,
        ownership: Ownership,
        ip_type: IpType = IpType.IPV4,
        ip: str = "127.0.0.1",
        port: int = 8021,
        protocol_type: ProtocolType = ProtocolType.TCP,
    ):
        super().__init__(
            ownership=ownership,
            endpoint_type=EndpointType.SERVER,
            ip_type=ip_type,
            ip=ip,
            port=port,
            protocol_type=protocol_type,
        )


class SocketClient(SocketParty):
    def __init__(
        self,
        *,
        ownership: Ownership,
        ip_type: IpType = IpType.IPV4,
        ip: str = "127.0.0.1",
        port: int = 8021,
        protocol_type: ProtocolType = ProtocolType.TCP,
    ):
        super().__init__(
            ownership=ownership,
            endpoint_type=EndpointType.CLIENT,
            ip_type=ip_type,
            ip=ip,
            port=port,
            protocol_type=protocol_type,
        )


class STDOUT(FandangoParty):

    def __init__(self):
        super().__init__(Ownership.FUZZER)

    def on_send(
        self,
        message: DerivationTree,
        recipient: str,
        response_setter: Callable[[str, str], None],
    ):
        print({message.to_string()})


class STDIN(FandangoParty):
    def __init__(self):
        super().__init__(Ownership.EXTERNAL)
        self.running = True
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()

    def listen_loop(self):
        while self.running:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                read = sys.stdin.readline()
                if read == "":
                    self.running = False
                    break
                self.receive_msg("STDIN", read)
            else:
                time.sleep(0.1)


class FandangoIO:
    __instance = None

    @classmethod
    def instance(cls) -> "FandangoIO":
        if cls.__instance is None:
            FandangoIO()
        return cls.__instance

    def __init__(self):
        if FandangoIO.__instance is not None:
            raise Exception("Singleton already created!")
        FandangoIO.__instance = self
        self.transmit: tuple[str, str, DerivationTree] | None = None
        self.receive = list[(str, str, str)]()
        self.parties = dict[str, FandangoParty]()
        self.receive_lock = threading.Lock()

    def run_com_loop(self):
        if self.transmit is not None:
            sender, recipient, msg = self.transmit
            if sender in self.parties.keys():
                self.parties[sender].on_send(
                    msg, recipient, self.parties[sender].receive_msg
                )
        self.clear_transmit_msgs()

    def clear_transmit_msgs(self):
        self.transmit = None

    def add_receive(self, sender: str, receiver: str, message: str) -> None:
        with self.receive_lock:
            self.receive.append((sender, receiver, message))

    def received_msg(self):
        with self.receive_lock:
            return len(self.receive) != 0

    def get_received_msgs(self):
        with self.receive_lock:
            return list(self.receive)

    def clear_received_msg(self, idx: int):
        with self.receive_lock:
            del self.receive[idx]

    def clear_received_msgs(self):
        with self.receive_lock:
            self.receive.clear()

    def set_transmit(
        self, sender: str, recipient: str | None, message: DerivationTree
    ) -> None:
        self.transmit = (sender, recipient, message)
