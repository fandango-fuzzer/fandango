import select
import socket
import sys
import threading
import time
from typing import Callable, Tuple

from fandango import FandangoError
from fandango.language.tree import DerivationTree


class FandangoParty(object):

    def __init__(self, is_fandango: bool):
        self.class_name = type(self).__name__
        self._is_fandango = is_fandango
        FandangoIO.instance().parties[self.class_name] = self

    """
    :return: True, if the party is substituted by fandango.
    """

    def is_fandango(self):
        return self._is_fandango

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
    def __init__(self, is_fandango: bool, is_server: bool, is_ipv4: bool = False, ip: str = "::1",
                 port: int = 8021, is_tcp: bool = True):
        super().__init__(is_fandango)
        self.running = False
        self._is_ipv4 = is_ipv4
        self._is_tcp = is_tcp
        self._ip = ip
        self._port = port
        self.is_server = is_server
        self.sock = None
        self.connection = None
        self.send_thread = None
        self.lock = threading.Lock()

    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, value: str):
        self._ip = value
        self._apply_attr_update()

    @property
    def is_tcp(self) -> bool:
        return self._is_tcp

    @is_tcp.setter
    def is_tcp(self, value: bool):
        self._is_tcp = value
        self._apply_attr_update()

    @property
    def is_ipv4(self) -> bool:
        return self._is_ipv4

    @is_ipv4.setter
    def is_ipv4(self, value: bool):
        self._is_ipv4 = value
        self._apply_attr_update()

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int):
        if self._port == value:
            return
        self._port = value
        self._apply_attr_update()

    def start(self):
        if self.running:
            return
        if not self.is_fandango():
            return
        self.close()
        self._create_socket()
        self._connect()

    def _apply_attr_update(self):
        if not self.running:
            return
        self.start()

    def _create_socket(self):
        protocol = socket.SOCK_STREAM if self._is_tcp else socket.SOCK_DGRAM
        ip_type = socket.AF_INET if self._is_ipv4 else socket.AF_INET6
        self.sock = socket.socket(ip_type, protocol)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _connect(self):
        if self.is_server:
            self.sock.bind((self._ip, self._port))
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
                if self.is_server:
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
        sender = "Client" if self.is_server else "Server"
        self.receive_msg(sender, data.decode("utf-8"))

class SocketServer(SocketParty):
    def __init__(self, is_fandango: bool, is_ipv4: bool = False, ip: str = "::1",
                 port: int = 8021, is_tcp: bool = True):
        super().__init__(is_fandango, True, is_ipv4, ip, port, is_tcp)


class SocketClient(SocketParty):
    def __init__(self, is_fandango: bool, is_ipv4: bool = False, ip: str = "::1",
                 port: int = 8021, is_tcp: bool = True):
        super().__init__(is_fandango, False, is_ipv4, ip, port, is_tcp)

class STDOUT(FandangoParty):

    def __init__(self):
        super().__init__(True)

class STDIN(FandangoParty):
    def __init__(self):
        super().__init__(False)
        self.running = True
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()

    def listen_loop(self):
        while self.running:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                read = sys.stdin.readline()
                if read == '':
                    self.running = False
                    break
                self.receive_msg('STDIN', read)
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
        self.transmit: Tuple[str, str, DerivationTree] | None = None
        self.receive = list[(str, str, str)]()
        self.parties = dict[str, FandangoParty]()
        self.receive_lock = threading.Lock()

    def run_com_loop(self):
        if self.transmit is not None:
            sender, recipient, msg = self.transmit
            if sender in self.parties.keys():
                self.parties[sender].on_send(msg, recipient, self.parties[sender].receive_msg)
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
