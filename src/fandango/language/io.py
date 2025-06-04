import socket
import threading
from typing import Callable, Tuple

from fandango import FandangoError
from fandango.language.tree import DerivationTree


class FandangoAgent(object):

    def __init__(self, is_fandango: bool):
        self.class_name = type(self).__name__
        self._is_fandango = is_fandango
        FandangoIO.instance().roles[self.class_name] = self

    """
    :return: True, if the party is substituted by fandango.
    """

    def is_fandango(self):
        return self._is_fandango

    """
    Called when fandango wants to send a message as this party.
    
    :message: The message to send.
    :response_setter: If the recipient of the message answers during the function call, this method can be called to set the response.
        First parameter of response_setter if the role of the other party. The second is the message, that it answered with.
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

class SocketAgent(FandangoAgent):
    def __init__(self, is_fandango: bool, is_server: bool, is_ipv4: bool = False, ip: str = "::1",
                 port: int = 0, is_tcp: bool = True):
        super().__init__(is_fandango)
        self.is_ipv4 = is_ipv4
        self.is_tcp = is_tcp
        self.ip = ip
        self.port = port
        self.is_server = is_server

        self.sock = None
        self.connection = None
        self.send_thread = None
        self.running = False
        self.lock = threading.Lock()
        self._create_socket()
        self.connect()

    def _create_socket(self):
        protocol = socket.SOCK_STREAM if self.is_tcp else socket.SOCK_DGRAM
        ip_type = socket.AF_INET if self.is_ipv4 else socket.AF_INET6
        self.sock = socket.socket(ip_type, protocol)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        if self.is_server:
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)
        self.running = True
        self.send_thread = threading.Thread(target=self._listen, daemon=True)
        self.send_thread.daemon = True
        self.send_thread.start()

    def close(self):
        self.running = False
        if self.send_thread is not None:
            self.send_thread.join()
            self.send_thread = None
        if self.connection is not None:
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            self.connection = None
        if self.sock is not None:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()

    def wait_accept(self):
        with self.lock:
            if self.connection is None:
                if self.is_server:
                    self.connection, _ = self.sock.accept()
                else:
                    self.sock.connect((self.ip, self.port))
                    self.connection = self.sock

    def update_port(self, new_port: int):
        self.port = new_port
        if not self.is_fandango():
            return
        self.close()
        self._create_socket()
        self.connect()

    def _listen(self):
        self.wait_accept()
        while self.running:
            try:
                data = self.connection.recv(1024)
                if len(data) == 0:
                    continue
                if data:
                    self.receive(data)
                else:
                    self.running = False
                    break
            except Exception as e:
                self.running = False
                break

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
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
        self.receive_msg("Client", data.decode("utf-8"))

class SocketServer(SocketAgent):
    def __init__(self, is_fandango: bool, is_ipv4: bool = False, ip: str = "::1",
                 port: int = 0, is_tcp: bool = True):
        super().__init__(is_fandango, True, is_ipv4, ip, port, is_tcp)


class SocketClient(SocketAgent):
    def __init__(self, is_fandango: bool, is_ipv4: bool = False, ip: str = "::1",
                 port: int = 0, is_tcp: bool = True):
        super().__init__(is_fandango, False, is_ipv4, ip, port, is_tcp)

class STDOUT(FandangoAgent):

    def __init__(self):
        super().__init__(True)


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
        self.transmit: Tuple[str, str, DerivationTree] | None = None
        self.receive = list[(str, str, str)]()
        self.roles = dict[str, FandangoAgent]()
        self.receive_lock = threading.Lock()

    def run_com_loop(self):
        if self.transmit is not None:
            role, recipient, msg = self.transmit
            if role in self.roles.keys():
                self.roles[role].on_send(msg, recipient, self.roles[role].receive_msg)
        self.clear_transmit_msgs()

    def clear_transmit_msgs(self):
        self.transmit = None

    def add_receive(self, role: str, receiver: str, message: str) -> None:
        with self.receive_lock:
            self.receive.append((role, receiver, message))

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
        self, role: str, recipient: str | None, message: DerivationTree
    ) -> None:
        self.transmit = (role, recipient, message)
