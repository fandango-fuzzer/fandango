#!/usr/bin/env python3

import enum
import logging
import re
import select
import shlex
import socket
import subprocess
import sys
import threading
import time
from abc import ABC
from typing import Optional

from fandango.errors import FandangoError, FandangoValueError
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER


class Protocol(enum.Enum):
    TCP = "TCP"
    UDP = "UDP"


class EndpointType(enum.Enum):
    OPEN = "Open"
    CONNECT = "Connect"


class IpType(enum.Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class Ownership(enum.Enum):
    FANDANGO_PARTY = "FandangoParty"
    EXTERNAL_PARTY = "ExternalParty"


RE_PARTY = re.compile(
    r"""
((?P<name>[a-zA-Z0-9_]+)=)?            # Optional party name followed by =
((?P<protocol>([tT][Cc][pP]|[uU][dD][pP])):)?  # Optional protocol prefixed by :
(//)?                                  # Optional // separator
((?P<host>([^:]+|\[(?P<ipv6>.*)\])):)? # hostname(IPv6 in [...])
(?P<port>[0-9]+)                       # Port
""",
    re.VERBOSE,
)


def split_party_spec(
    spec: str,
) -> tuple[Optional[str], Optional[str], Optional[str], int]:
    """
    Splits a party specification into the party name and the party definition.
    :param spec: The party specification to split.
    :return: A tuple containing
        - The party name (str) or None if not specified
        - The party protocol (str) or None if not specified
        - The party host (str) or None if not specified
        - The party port (int)
    """
    match = RE_PARTY.match(spec)
    if not match:
        raise FandangoValueError(f"Invalid party specification: {spec}")
    name = match.group("name")
    host = match.group("ipv6") or match.group("host")
    port = int(match.group("port"))
    protocol = match.group("protocol")
    if protocol is not None:
        protocol = protocol.upper()
    return name, protocol, host, port


class FandangoParty(ABC):
    """Base class for all parties in Fandango."""

    def __init__(self, *, ownership: Ownership, party_name: Optional[str] = None):
        """Constructor.
        :param ownership: Ownership of the party, either Ownership.FUZZER or Ownership.EXTERNAL. FUZZER means the party is controlled by Fandango, while EXTERNAL means it is an external party.
        """
        if party_name is None:
            self.party_name = type(self).__name__
        else:
            self.party_name = party_name
        self._ownership = ownership
        FandangoIO.instance().parties[self.party_name] = self

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
        return self.ownership == Ownership.FANDANGO_PARTY

    def on_send(self, message: DerivationTree, recipient: Optional[str]) -> None:
        """
        Called when fandango wants to send a message as this party.
        :param message: The message to send.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        """
        print(f"({self.party_name}): {message.to_string()}")

    def receive_msg(self, sender: Optional[str], message: str | bytes) -> None:
        """
        Called when a message has been received by this party.
        :param sender: The sender of the message.
        :param message: The sender of the message.
        """
        if sender is None:
            parties = list(
                map(
                    lambda x: x.party_name,
                    filter(
                        lambda party: not party.is_fuzzer_controlled(),
                        FandangoIO.instance().parties.values(),
                    ),
                )
            )
            if len(parties) == 1:
                sender = parties[0]
            else:
                raise FandangoValueError(
                    f"Could not determine sender of message received by {self.party_name}. Please explicitly provide the sender to the receive_msg method."
                )
        FandangoIO.instance().add_receive(sender, self.party_name, message)


class ProtocolDecorator(ABC):
    def __init__(
        self,
        *,
        endpoint_type: EndpointType = EndpointType.CONNECT,
        ip_type: IpType = IpType.IPV4,
        ip: Optional[str],
        port: Optional[int],
        party_instance: FandangoParty,
    ):
        self.endpoint_type = endpoint_type
        self.ip = ip
        self.port = port
        self.ip_type = ip_type
        self._party_instance = party_instance

    def on_send(self, message: DerivationTree, recipient: Optional[str]):
        raise NotImplementedError("Please Implement this method")

    def start(self):
        raise NotImplementedError("Please Implement this method")

    def stop(self):
        raise NotImplementedError("Please Implement this method")

    @property
    def protocol_type(self) -> Protocol:
        raise NotImplementedError("Please Implement this method")


class UdpTcpProtocolDecorator(ProtocolDecorator):
    BUFFER_SIZE = 1024  # Size of the buffer for receiving data

    def __init__(
        self,
        *,
        endpoint_type: EndpointType = EndpointType.CONNECT,
        protocol_type: Protocol,
        ip_type: IpType = IpType.IPV4,
        ip: Optional[str] = None,
        port: Optional[int] = None,
        party_instance: Optional[FandangoParty] = None,
    ):
        if party_instance is None:
            raise FandangoValueError("party_instance must not be None")
        super().__init__(
            endpoint_type=endpoint_type,
            ip_type=ip_type,
            ip=ip,
            port=port,
            party_instance=party_instance,
        )
        self._running = False
        assert protocol_type == Protocol.TCP or protocol_type == Protocol.UDP
        self._protocol_type = protocol_type
        self._sock: Optional[socket.socket] = None
        self._connection: Optional[socket.socket] = None
        self._send_thread: Optional[threading.Thread] = None
        self.current_remote_addr = None
        self._lock = threading.Lock()

    @property
    def protocol_type(self) -> Protocol:
        """Returns the protocol type of this socket."""
        return self._protocol_type

    def start(self):
        """Starts the socket party according to the given configuration. If the party is already
        running or ownership is not set to Ownership.FUZZER, it does nothing."""
        if self._running:
            return
        if not self._party_instance.is_fuzzer_controlled():
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
        self._sock = socket.socket(ip_type, protocol)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _connect(self):
        if self.endpoint_type == EndpointType.OPEN:
            assert self._sock is not None
            self._sock.bind((self.ip, self.port))
            if self.protocol_type == Protocol.TCP:
                self._sock.listen(1)
        self._running = True
        self._send_thread = threading.Thread(target=self._listen, daemon=True)
        self._send_thread.daemon = True
        self._send_thread.start()

    def stop(self):
        """Stops the current socket."""
        self._running = False
        if self._send_thread is not None:
            self._send_thread.join()
            self._send_thread = None
        if self._connection is not None:
            try:
                self._connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self._connection.close()
            except OSError:
                pass
            self._connection = None
        if self._sock is not None:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None

    def _wait_accept(self):
        with self._lock:
            if self._connection is None:
                if self.protocol_type == Protocol.TCP:
                    if self.endpoint_type == EndpointType.OPEN:
                        assert self._sock is not None
                        while self._running:
                            rlist, _, _ = select.select([self._sock], [], [], 0.1)
                            if rlist:
                                self._connection, _ = self._sock.accept()
                                break
                    else:
                        assert self._sock is not None
                        self._sock.setblocking(False)
                        try:
                            self._sock.connect((self.ip, self.port))
                        except BlockingIOError:
                            pass
                        while self._running:
                            _, wlist, _ = select.select([], [self._sock], [], 0.1)
                            if wlist:
                                self._connection = self._sock
                                break
                        self._sock.setblocking(True)
                else:
                    # For UDP, we do not need to accept a connection
                    assert self._sock is not None
                    self._connection = self._sock

    def _listen(self):
        self._wait_accept()
        if not self._running:
            return

        while self._running:
            try:
                assert self._connection is not None
                rlist, _, _ = select.select([self._connection], [], [], 0.1)
                if rlist and self._running:
                    if self.protocol_type == Protocol.TCP:
                        data = self._connection.recv(self.BUFFER_SIZE)
                    else:
                        data, addr = self._connection.recvfrom(self.BUFFER_SIZE)
                        self.current_remote_addr = addr
                    if len(data) == 0:
                        continue  # Keep waiting if connection is open but no data
                    self._party_instance.receive_msg(None, data)
            except Exception:
                self._running = False
                break

    def on_send(self, message: DerivationTree, recipient: Optional[str]):
        """Called when Fandango wants to send a message as this party.
        :param message: The message to send.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        :raises FandangoError: If the socket is not running.
        """
        if not self._running:
            raise FandangoError("Socket not running. Invoke start() first.")
        self._wait_accept()

        assert self._connection is not None
        if message.contains_bits():
            send_data = message.to_bytes()
        else:
            send_data = message.to_string().encode("utf-8")
        if self.protocol_type == Protocol.TCP:
            self._connection.sendall(send_data)
        else:
            if self.endpoint_type == EndpointType.OPEN:
                if self.current_remote_addr is None:
                    raise FandangoValueError(
                        "Client received no data yet. No address to send to."
                    )
                self._connection.sendto(send_data, self.current_remote_addr)
            else:
                self._connection.sendto(send_data, (self.ip, self.port))


class ConnectParty(FandangoParty):
    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 8000
    DEFAULT_PROTOCOL = Protocol.TCP

    def __init__(
        self,
        uri: str,
        *,
        ownership: Ownership = Ownership.FANDANGO_PARTY,
        endpoint_type: EndpointType = EndpointType.CONNECT,
    ):
        party_name, prot, host, port = split_party_spec(uri)
        super().__init__(ownership=ownership, party_name=party_name)
        self.protocol_impl = None

        if prot is None:
            prot = self.DEFAULT_PROTOCOL.value
        protocol = Protocol(prot)
        if host is None:
            host = self.DEFAULT_IP
        info = socket.getaddrinfo(host, None, socket.AF_INET)
        ip = info[0][4][0]
        if isinstance(ip, int):
            raise FandangoValueError(f"Invalid IP address: {ip}")
        if port is None:
            protocol = self.DEFAULT_PORT

        if protocol == Protocol.TCP or protocol == Protocol.UDP:
            self.protocol_impl = UdpTcpProtocolDecorator(
                endpoint_type=endpoint_type,
                protocol_type=protocol,
                ip_type=IpType.IPV4,
                ip=ip,
                port=port,
                party_instance=self,
            )
        else:
            raise FandangoValueError(f"Unsupported protocol: {protocol}")

    def on_send(self, message: DerivationTree, recipient: Optional[str]) -> None:
        if self.protocol_impl is None:
            raise FandangoError("Protocol implementation not initialized.")
        self.protocol_impl.on_send(message, recipient)

    def start(self):
        if self.protocol_impl is None:
            raise FandangoError("Protocol implementation not initialized.")
        self.protocol_impl.start()

    def stop(self):
        if self.protocol_impl is None:
            raise FandangoError("Protocol implementation not initialized.")
        self.protocol_impl.stop()

    @property
    def ip(self):
        if self.protocol_impl is None:
            raise FandangoError("Protocol implementation not initialized.")
        return self.protocol_impl.ip

    @ip.setter
    def ip(self, host: str):
        """Sets the ip for the connection. Applied after a (re)start of the connection party."""
        if self.protocol_impl is None:
            raise FandangoError("Protocol implementation not initialized.")
        info = socket.getaddrinfo(host, None, socket.AF_INET)
        ip = info[0][4][0]
        if isinstance(ip, int):
            raise FandangoValueError(f"Invalid IP address: {ip}")
        self.protocol_impl.ip = ip

    @property
    def port(self):
        if self.protocol_impl is None:
            raise FandangoError("Protocol implementation not initialized.")
        return self.protocol_impl.port

    @port.setter
    def port(self, port: int):
        """Sets the port for the connection. Applied after a (re)start of the connection party."""
        if self.protocol_impl is None:
            raise FandangoError("Protocol implementation not initialized.")
        self.protocol_impl.port = port


class StdOut(FandangoParty):
    """Standard output party for sending messages to stdout. The party can only send messages, but not receive any.
    The party is always owned by Fandango (Ownership.FUZZER), meaning it sends messages generated by Fandango.
    """

    def __init__(self):
        super().__init__(ownership=Ownership.FANDANGO_PARTY)
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
        super().__init__(ownership=Ownership.EXTERNAL_PARTY)
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
                self.receive_msg(self.party_name, read)
            else:
                time.sleep(0.1)


class Out(FandangoParty):
    """Standard output party for receiving messages from an external process set using set_program_command(command: str).
    The party can only receive messages, but not send any.
    The ownership of this party is always Ownership.EXTERNAL, meaning it is an external party.
    """

    def __init__(self):
        super().__init__(ownership=Ownership.EXTERNAL_PARTY)
        self.proc = ProcessManager.instance().get_process()
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self):
        while True:
            if self.proc.stdout is not None:
                line = self.proc.stdout.readline()
                self.receive_msg(self.party_name, line)


class In(FandangoParty):
    """Standard input party for sending messages to an external process set using set_program_command(command: str).
    The party can only send messages, but not receive any.
    The ownership of this party is always Ownership.FUZZER, meaning it sends messages generated by Fandango.
    """

    def __init__(self):
        super().__init__(ownership=Ownership.FANDANGO_PARTY)
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
        if self.proc.stdin is not None:
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

    def get_process(self) -> subprocess.Popen:
        """Returns the current process if it exists, otherwise starts a new one based on the command set."""
        with self.lock:
            if not self.proc:
                self._start_process()
        if self.proc is None:
            raise FandangoValueError(
                "This spec requires interaction. Use `--party=PARTY` or `fandango talk` with this spec."
            )
        return self.proc

    @property
    def command(self) -> str | list[str] | None:
        """Returns the command to be executed to start the process."""
        return self._command

    def set_command(self, value: str | list[str], text: bool = True):
        """Sets the command to be executed to start the process."""
        assert isinstance(
            value, (str, list)
        ), "Command must be a string or a list of strings"
        with self.lock:
            if self._command == value:
                return
            self._command = value
        self.text = text

    def _start_process(self):
        command = self.command
        if command is None:
            return
        if isinstance(command, str):
            command = shlex.split(command)

        LOGGER.info(f"Starting subprocess {command!r}")
        self.proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=self.text,
        )


def set_program_command(command: str | list[str], text: bool = True):
    """
    Set the command to be executed by the ProcessManager.
    :param command: The command to execute.
    """
    LOGGER.info(f"Setting command {command!r}")
    ProcessManager.instance().set_command(command, text)


if __name__ == "__main__":
    # Some tests for the split_party_spec function
    assert split_party_spec("25") == (None, None, None, 25)
    assert split_party_spec("tcp://localhost:25") == (None, "TCP", "localhost", 25)
    assert split_party_spec("tcp:127.0.0.1:25") == (None, "TCP", "127.0.0.1", 25)
    assert split_party_spec("udp://[::1]:25") == (None, "UDP", "::1", 25)
    assert split_party_spec("tcp://cispa.de:25") == (None, "TCP", "cispa.de", 25)
    assert split_party_spec("SMTP=[::1]:25") == ("SMTP", None, "::1", 25)

    # Demonstrator code to show how to use the classes
    from fandango import Fandango

    SPEC = r"""
    <start> ::= <In:input> <Out:output>
    <input> ::= <string>
    <output> ::= <string>
    <string> ::= r'.*\n'
    where str(<input>) == str(<output>)

    set_program_command("cat")
    """
    fandango = Fandango(SPEC, logging_level=logging.INFO)
    fandango.fuzz()
