#!/usr/bin/env python3

import enum
import select
import shlex
import socket
import subprocess
import sys
import threading
import time
import logging

from abc import ABC
from typing import Optional

from fandango import FandangoError
from fandango.language.tree import DerivationTree


class Protocol(enum.Enum):
    TCP = "TCP"
    UDP = "UDP"


class EndpointType(enum.Enum):
    SERVER = "Server"
    CLIENT = "Client"


class IpType(enum.Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class Ownership(enum.Enum):
    FUZZER = "Fuzzer"
    EXTERNAL = "External"


class FandangoParty(ABC):
    """Base class for all parties in Fandango."""

    def __init__(self, ownership: Ownership):
        """Constructor.
        :param ownership: Ownership of the party, either Ownership.FUZZER or Ownership.EXTERNAL. FUZZER means the party is controlled by Fandango, while EXTERNAL means it is an external party.
        """
        self.class_name = type(self).__name__
        self._ownership = ownership
        FandangoIO.instance().parties[self.class_name] = self

    @property
    def ownership(self) -> Ownership:
        """
        :return: ownership of the party
        """
        return self._ownership

    def is_fuzzer_controlled(self) -> bool:
        """
        Returns True if this party is owned by Fandango, False if it is an external party.
        """
        return self.ownership == Ownership.FUZZER

    def on_send(self, message: DerivationTree, recipient: Optional[str]) -> None:
        """
        Called when fandango wants to send a message as this party.
        :param message: The message to send.
        """
        print(f"({self.class_name}): {message.to_string()}")

    def receive_msg(self, sender: str, message: str | bytes) -> None:
        """
        Called when a message has been received by this party.
        :param sender: The sender of the message.
        :param message: The sender of the message.
        """
        FandangoIO.instance().add_receive(sender, self.class_name, message)


class SocketParty(FandangoParty):
    """Base class for communicating with parties via sockets."""

    BUFFER_SIZE = 1024  # Size of the buffer for receiving data

    def __init__(
        self,
        *,
        ownership: Ownership,
        endpoint_type: EndpointType,
        ip_type: IpType = IpType.IPV4,
        ip: str = "127.0.0.1",
        port: int = 8021,
        protocol_type: Protocol = Protocol.TCP,
    ):
        """Constructor.
        :param ownership: Ownership of the party, either Ownership.FUZZER or Ownership.EXTERNAL. FUZZER means the party is controlled by Fandango, while EXTERNAL means it is an external party.
        :param endpoint_type: Type of the endpoint, either EndpointType.SERVER or EndpointType.CLIENT.
        :param ip_type: Type of IP address, either IpType.IPV4 or IpType.IPV6.
        :param ip: IP address (as a string) to bind to or connect to.
        :param port: Port (integer) to bind to or connect to.
        :param protocol_type: Protocol to use, either Protocol.TCP or Protocol.UDP."""
        super().__init__(ownership)
        self.running = False
        self._ip_type: IpType = ip_type
        self._protocol_type: Protocol = protocol_type
        self._ip: str = ip
        self._port: int = port
        self._endpoint_type: EndpointType = endpoint_type
        self.sock: Optional[socket.socket] = None
        self.connection: Optional[socket.socket] = None
        self.send_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

    @property
    def ip(self) -> str:
        """Returns the IP address that this party is bound (endpoint_type == EndpointType.SERVER) to
        or connected to (endpoint_type == EndpointType.CLIENT)."""
        return self._ip

    @ip.setter
    def ip(self, value: str):
        """Sets the IP address that this party is bound (endpoint_type == EndpointType.SERVER) to
        or connected to (endpoint_type == EndpointType.CLIENT)."""
        if self._ip == value:
            return
        self._ip = value

    @property
    def endpoint_type(self) -> EndpointType:
        """Returns the type of endpoint, either EndpointType.SERVER or EndpointType.CLIENT."""
        return self._endpoint_type

    @endpoint_type.setter
    def endpoint_type(self, value: EndpointType):
        """Sets the type of endpoint, either EndpointType.SERVER or EndpointType.CLIENT."""
        if self._endpoint_type == value:
            return
        self._endpoint_type = value

    @property
    def ip_type(self) -> IpType:
        """Returns the type of IP address, either IpType.IPV4 or IpType.IPV6."""
        return self._ip_type

    @ip_type.setter
    def ip_type(self, value: IpType):
        """Sets the type of IP address, either IpType.IPV4 or IpType.IPV6."""
        if self._ip_type == value:
            return
        self._ip_type = value

    @property
    def protocol_type(self) -> Protocol:
        """Returns the protocol type, either Protocol.TCP or Protocol.UDP."""
        return self._protocol_type

    @protocol_type.setter
    def protocol_type(self, value: Protocol):
        """Sets the protocol type, either Protocol.TCP or Protocol.UDP."""
        if self._protocol_type == value:
            return
        self._protocol_type = value

    @property
    def port(self) -> int:
        """Returns the port that this party is bound (endpoint_type == EndpointType.SERVER) to
        or connected to (endpoint_type == EndpointType.CLIENT)."""
        return self._port

    @port.setter
    def port(self, value: int):
        """Sets the port that this party is bound (endpoint_type == EndpointType.SERVER) to
        or connected to (endpoint_type == EndpointType.CLIENT)."""
        if self._port == value:
            return
        self._port = value

    def start(self):
        """Starts the socket party according to the given configuration. If the party is already
        running or ownership is not set to Ownership.FUZZER, it does nothing."""
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
            if self._protocol_type == Protocol.TCP
            else socket.SOCK_DGRAM
        )
        ip_type = socket.AF_INET if self.ip_type == IpType.IPV4 else socket.AF_INET6
        self.sock = socket.socket(ip_type, protocol)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _connect(self):
        if self.endpoint_type == EndpointType.SERVER:
            assert self.sock is not None
            self.sock.bind((self.ip, self.port))
            self.sock.listen(1)
        self.running = True
        self.send_thread = threading.Thread(target=self._listen, daemon=True)
        self.send_thread.daemon = True
        self.send_thread.start()

    def stop(self):
        """Stops the current socket."""
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

    def _wait_accept(self):
        with self.lock:
            if self.connection is None:
                if self.endpoint_type == EndpointType.SERVER:
                    assert self.sock is not None
                    while self.running:
                        rlist, _, _ = select.select([self.sock], [], [], 0.1)
                        if rlist:
                            self.connection, _ = self.sock.accept()
                            break
                else:
                    assert self.sock is not None
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
        self._wait_accept()
        if not self.running:
            return

        while self.running:
            try:
                assert self.connection is not None
                rlist, _, _ = select.select([self.connection], [], [], 0.1)
                if rlist and self.running:
                    data = self.connection.recv(self.BUFFER_SIZE)
                    if len(data) == 0:
                        continue  # Keep waiting if connection is open but no data
                    self.receive(data)
            except Exception:
                self.running = False
                break

    def on_send(self, message: DerivationTree, recipient: Optional[str]):
        """Called when Fandango wants to send a message as this party.
        :param message: The message to send.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        :raises FandangoError: If the socket is not running.
        """
        if not self.running:
            raise FandangoError("Socket not running. Invoke start() first.")
        self._wait_accept()
        self.transmit(message, recipient)

    def transmit(self, message: DerivationTree, recipient: Optional[str]):
        """Transmits a message using the configured socket.
        :param message: The message to transmit.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        """
        assert self.connection is not None
        if message.contains_bits():
            self.connection.sendall(message.to_bytes())
        else:
            self.connection.sendall(message.to_string().encode("utf-8"))

    def receive(self, data: bytes):
        """Receives data from the socket and forwards it to fandango.
        :param data: The data received from the socket.
        """
        sender = "Client" if self.endpoint_type == EndpointType.SERVER else "Server"
        self.receive_msg(sender, data.decode("utf-8"))


class SocketServer(SocketParty):
    """Socket server class for handling incoming connections and exchanging messages.
    Equivalent to the SocketParty class, but with the endpoint_type set to SERVER."""

    def __init__(
        self,
        *,
        ownership: Ownership,
        ip_type: IpType = IpType.IPV4,
        ip: str = "127.0.0.1",
        port: int = 8021,
        protocol_type: Protocol = Protocol.TCP,
    ):
        """Constructor.
        :param ownership: Ownership of the party, either Ownership.FUZZER or Ownership.EXTERNAL. FUZZER means the party is controlled by Fandango, while EXTERNAL means it is an external party.
        :param ip_type: Type of IP address, either IpType.IPV4 or IpType.IPV6.
        :param ip: IP address (as a string) to bind to or connect to.
        :param port: Port (integer) to bind to or connect to.
        :param protocol_type: Protocol to use, either Protocol.TCP or Protocol.UDP."""
        super().__init__(
            ownership=ownership,
            endpoint_type=EndpointType.SERVER,
            ip_type=ip_type,
            ip=ip,
            port=port,
            protocol_type=protocol_type,
        )


class SocketClient(SocketParty):
    """Socket client class for connecting to a server and exchanging messages.
    Equivalent to the SocketParty class, but with the endpoint_type set to SERVER."""

    def __init__(
        self,
        *,
        ownership: Ownership,
        ip_type: IpType = IpType.IPV4,
        ip: str = "127.0.0.1",
        port: int = 8021,
        protocol_type: Protocol = Protocol.TCP,
    ):
        """Constructor.
        :param ownership: Ownership of the party, either Ownership.FUZZER or Ownership.EXTERNAL. FUZZER means the party is controlled by Fandango, while EXTERNAL means it is an external party.
        :param ip_type: Type of IP address, either IpType.IPV4 or IpType.IPV6.
        :param ip: IP address (as a string) to bind to or connect to.
        :param port: Port (integer) to bind to or connect to.
        :param protocol_type: Protocol to use, either Protocol.TCP or Protocol.UDP."""
        super().__init__(
            ownership=ownership,
            endpoint_type=EndpointType.CLIENT,
            ip_type=ip_type,
            ip=ip,
            port=port,
            protocol_type=protocol_type,
        )


class StdOut(FandangoParty):
    """Standard output party for sending messages to stdout. The party can only send messages, but not receive any.
    The party is always owned by Fandango (Ownership.FUZZER), meaning it sends messages generated by Fandango.
    """

    def __init__(self):
        super().__init__(Ownership.FUZZER)
        self.stream = sys.stdout

    def on_send(self, message: DerivationTree, recipient: Optional[str]):
        """Called by Fandango, when it wants to write a message to StdOut.
        :param message: The message to send.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        """
        self.stream.write(message.to_string())


class StdIn(FandangoParty):
    """Standard input party for reading messages from stdin. The party can only receive messages, but not send any.
    The ownership of this party is always Ownership.EXTERNAL, meaning it is an external party.
    """

    def __init__(self):
        super().__init__(Ownership.EXTERNAL)
        self.running = True
        self.stream = sys.stdin
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()

    def _listen_loop(self):
        while self.running:
            rlist, _, _ = select.select([self.stream], [], [], 0.1)
            if rlist:
                read = sys.stdin.readline()
                if read == "":
                    self.running = False
                    break
                self.receive_msg(self.class_name, read)
            else:
                time.sleep(0.1)


class Out(FandangoParty):
    """Standard output party for receiving messages from an external process set using set_program_command(command: str).
    The party can only receive messages, but not send any.
    The ownership of this party is always Ownership.EXTERNAL, meaning it is an external party.
    """

    def __init__(self):
        super().__init__(Ownership.EXTERNAL)
        self.proc = ProcessManager.instance().get_process()
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        while True:
            line = self.proc.stdout.readline()
            self.receive_msg(self.class_name, line)


class In(FandangoParty):
    """Standard input party for sending messages to an external process set using set_program_command(command: str).
    The party can only send messages, but not receive any.
    The ownership of this party is always Ownership.FUZZER, meaning it sends messages generated by Fandango.
    """

    def __init__(self):
        super().__init__(Ownership.FUZZER)
        self.proc = ProcessManager.instance().get_process()
        self._close_post_transmit = False

    @property
    def close_post_transmit(self) -> bool:
        """Returns whether the stdin of the process should be closed after transmitting a message."""
        return self._close_post_transmit

    @close_post_transmit.setter
    def close_post_transmit(self, value: bool):
        """Sets whether the stdin of the process should be closed after transmitting a message."""
        if self._close_post_transmit == value:
            return
        self._close_post_transmit = value

    def on_send(self, message: DerivationTree, recipient: Optional[str]):
        """Called by Fandango, when it wants to write a message to the external process.
        :param message: The message to send.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        """

        self.proc.stdin.write(message.to_string())
        self.proc.stdin.flush()
        if self.close_post_transmit:
            self.proc.stdin.close()


class FandangoIO(object):
    """Singleton class for managing Fandango's input/output operations."""

    _instance: Optional["FandangoIO"] = None

    @classmethod
    def instance(cls) -> "FandangoIO":
        """Returns the singleton instance of FandangoIO. If it does not exist, it creates one.
        Only use this method to access the FandangoIO instance.
        """
        if cls._instance is None:
            FandangoIO()
        assert cls._instance is not None
        return cls._instance

    def __init__(self):
        """Constructor for the FandangoIO class. Singleton! Do not call this method directly. Call instance() instead."""
        assert FandangoIO._instance is None, "FandangoIO singleton already created"
        FandangoIO._instance = self
        self.receive = list[tuple[str, str, str | bytes]]()
        self.parties = dict[str, FandangoParty]()
        self.receive_lock = threading.Lock()

    def add_receive(self, sender: str, receiver: str, message: str | bytes) -> None:
        """Forwards an external, received message to Fandango for processing.
        :param sender: The sender of the message.
        :param receiver: The receiver of the message.
        :param message: The message received from the sender.
        """
        with self.receive_lock:
            self.receive.append((sender, receiver, message))

    def received_msg(self) -> bool:
        """Checks if there are any received messages from external parties."""
        with self.receive_lock:
            return len(self.receive) != 0

    def get_received_msgs(self) -> list[tuple[str, str, str | bytes]]:
        """Returns a list of all received messages from external parties."""
        with self.receive_lock:
            return list(self.receive)

    def clear_received_msg(self, idx: int) -> None:
        """Clears a specific received message by its index."""
        with self.receive_lock:
            del self.receive[idx]

    def clear_received_msgs(self) -> None:
        """Clears all received messages."""
        with self.receive_lock:
            self.receive.clear()

    def transmit(
        self, sender: str, recipient: Optional[str], message: DerivationTree
    ) -> None:
        """Called by Fandango to transmit a message from a sender to a recipient using the sender's party definition.
        :param sender: The sender of the message. Needs to be equal to the class name of the corresponding party definition.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient. Can be used by the party definition to send the message to the correct recipient.
        :param message: The message to send.
        """
        if sender in self.parties.keys():
            self.parties[sender].on_send(message, recipient)


class ProcessManager(object):
    _instance: Optional["ProcessManager"] = None

    def __init__(self):
        """Constructor for the ProcessManager class. Singleton! Do not call this method directly. Call instance() instead."""
        assert (
            ProcessManager._instance is None
        ), "ProcessManager singleton already created"
        ProcessManager._instance = self
        self._command = None
        self.lock = threading.Lock()
        self.proc = None

    @classmethod
    def instance(cls) -> "ProcessManager":
        """Returns the singleton instance of ProcessManager. If it does not exist, it creates one."""
        if cls._instance is None:
            ProcessManager()
        assert cls._instance is not None
        return cls._instance

    def get_process(self):
        """Returns the current process if it exists, otherwise starts a new one based on the command set."""
        with self.lock:
            if not self.proc:
                self._start_process()
            return self.proc

    @property
    def command(self):
        """Returns the command to be executed to start the process."""
        return self._command

    @command.setter
    def command(self, value: str):
        """Sets the command to be executed to start the process."""
        with self.lock:
            if self._command == value:
                return
            self._command = value

    def _start_process(self):
        command = self.command
        if command is None:
            return
        self.proc = subprocess.Popen(
            shlex.split(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )


def set_program_command(command: str):
    """
    Set the command to be executed by the ProcessManager.
    :param command: The command to execute.
    """
    ProcessManager.instance().command = command


if __name__ == "__main__":
    # Demonstrator code to show how to use the classes
    from fandango import Fandango

    SPEC = """
    <start> ::= <In:input> <Out:output>
    <input> ::= <string>
    <output> ::= <string>
    <string> ::= r'(.|\\n)*'
    where <input> == <output>

    x = set_program_command("cat")
    """
    fandango = Fandango(SPEC, logging_level=logging.INFO)
    fandango.fuzz()
