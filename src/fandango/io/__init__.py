#!/usr/bin/env python3

import enum
import logging
import re
from uuid import UUID

import select
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
from typing import Hashable
from _contextvars import ContextVar

EnvKey = Hashable


class EnvContext:
    contextVar: Optional[ContextVar[Optional[UUID]]] = ContextVar(
        "CURRENT_ENV_KEY", default=None
    )


CURRENT_ENV_KEY: EnvContext = EnvContext()


class Protocol(enum.Enum):
    """
    The protocol used for network communication.
    * `Protocol.TCP` - the TCP protocol
    * `Procotol.UDP` - the UDP protocol
    """

    TCP = "TCP"
    UDP = "UDP"


class IpType(enum.Enum):
    """
    The IP address type.
    * `IpType.IPV4` - IPv4 address
    * `IpType.IPV6` - IPv6 address
    """

    IPV4 = "IPv4"
    IPV6 = "IPv6"


class ConnectionMode(enum.Enum):
    """
    Connection mode for a FandangoParty.
    * `ConnectionMode.OPEN` - Fandango opens a server socket and waits for incoming connections and behaves as a server.
    * `ConnectionMode.CONNECT` - Fandango connects to an already running server socket and behaves as a client.
    * `ConnectionMode.EXTERNAL` - The party is an external party; no connection is made by Fandango. Messages annotated with this party are not produced by Fandango, but are expected to be received from an external party.
    """

    OPEN = "Open"
    CONNECT = "Connect"
    EXTERNAL = "External"


# We use the following URI format for specifying a party:
# [name=][protocol:][//][host:]port
# See end of this file for some examples and tests.
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

    def __init__(
        self, *, connection_mode: ConnectionMode, party_name: Optional[str] = None
    ):
        """Constructor.
        :param connection_mode: ConnectionMode of the party. See `ConnectionMode` above for details.
        :param party_name: Optional name of the party. If None, the class name is used.
        """
        if party_name is None:
            self.party_name = type(self).__name__
        else:
            self.party_name = party_name
        self._connection_mode = connection_mode
        self.io_instance = FandangoIO.instance()
        self.io_instance.parties[self.party_name] = self

    @classmethod
    def instance(cls, party_name: Optional[str] = None) -> "FandangoParty":
        """
        Retrieves the instance of the `party_name` object (default: class name).
        :return: the instance of this object
        """
        if party_name is None:
            party_name = cls.__name__
        return FandangoIO.instance().parties[party_name]

    @property
    def connection_mode(self) -> ConnectionMode:
        """
        :return: connection mode of the party
        """
        return self._connection_mode

    def is_fuzzer_controlled(self) -> bool:
        """
        :return: True if this party is owned by Fandango, False if it is an external party.
        """
        return (
            self.connection_mode == ConnectionMode.CONNECT
            or self.connection_mode == ConnectionMode.OPEN
        )

    def send(
        self, message: DerivationTree | str | bytes, recipient: Optional[str]
    ) -> None:
        """
        Called to send a message to this party.
        :param message: The message to send.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        """
        print(f"({self.party_name}): {str(message)}")

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        """
        Called when a message has been received by this party.
        :param message: The content of the message.
        :param sender: The sender of the message.
        """
        if sender is None:
            parties = list(
                map(
                    lambda x: x.party_name,
                    filter(
                        lambda party: not party.is_fuzzer_controlled(),
                        self.io_instance.parties.values(),
                    ),
                )
            )
            if len(parties) == 1:
                sender = parties[0]
            else:
                raise FandangoValueError(
                    f"Party {self.party_name}: Could not determine sender of message received. Please explicitly provide the sender to the receive() method."
                )
        self.io_instance.add_receive(sender, self.party_name, message)

    def on_send(self, message: DerivationTree, recipient: Optional[str]) -> None:
        """Deprecated. Use send() instead."""
        raise FandangoError(
            f"Party {self.party_name}: on_send() has been deprecated. Use send() instead."
        )

    def receive_msg(
        self, sender: Optional[str], message: str, recipient: Optional[str]
    ) -> None:
        """Deprecated. Use receive() instead."""
        raise FandangoError(
            f"Party {self.party_name}: receive_msg() has been deprecated. Use receive() instead; note the changed argument order"
        )

    def start(self) -> None:
        raise NotImplementedError("start() method not implemented")

    def stop(self) -> None:
        raise NotImplementedError("stop() method not implemented")


class ProtocolImplementation(ABC):
    """
    Base class for all protocol implementations.
    """

    def __init__(
        self,
        *,
        connection_mode: ConnectionMode = ConnectionMode.CONNECT,
        ip_type: IpType = IpType.IPV4,
        ip: Optional[str],
        port: Optional[int],
        party_instance: FandangoParty,
    ):
        """
        Initialize a protocol implementation.

        :param connection_mode: A ConnectionMode; see above
        :param ip_type: An IpType; see above
        :param ip: The IP address to connect to or bind to
        :param port: The port to connect to or bind to
        :param party_instance: The FandangoParty instance using this protocol implementation
        """
        self.connection_mode = connection_mode
        self.ip = ip
        self.port = port
        self.ip_type = ip_type
        self._party_instance = party_instance

    def send(
        self, message: DerivationTree | str | bytes, recipient: Optional[str]
    ) -> None:
        """
        Invoked whenever Fandango wants to send a message as this party.
        :param message: the message to send (a `DerivationTree` instance)
        :param recipient: the recipient of the message (the name of a `FandangoParty`). Only present if the grammar specifies a recipient.
        """
        raise NotImplementedError("send() method not implemented")

    def start(self) -> None:
        """
        Invoked when protocol communication (re)starts.
        """
        raise NotImplementedError("start() method not implemented")

    def stop(self) -> None:
        """
        Invoked when protocol communication stops.
        """
        raise NotImplementedError("stop() method not implemented")

    @property
    def protocol_type(self) -> Protocol:
        """
        :return: The protocol type (`Protocol`) of this protocol implementation.
        """
        raise NotImplementedError("protocol_type property not implemented")

    @property
    def party_name(self) -> str:
        """
        :return: The name of the party using this protocol implementation.
        """
        return self._party_instance.party_name


class UdpTcpProtocolImplementation(ProtocolImplementation):
    """
    The implementation of TCP/UDP protocols.
    """

    BUFFER_SIZE_UDP = 1024  # Size of the buffer for receiving data
    BUFFER_SIZE_TCP = 1  # Size of the buffer for receiving data

    def __init__(
        self,
        *,
        connection_mode: ConnectionMode = ConnectionMode.CONNECT,
        protocol_type: Protocol,
        ip_type: IpType = IpType.IPV4,
        ip: Optional[str] = None,
        port: Optional[int] = None,
        party_instance: Optional[FandangoParty] = None,
    ):
        """
        Initialize a UDP/TCP protocol implementation.
        See `ProtocolImplementation.__init__()` for parameter documentation.
        """
        if party_instance is None:
            raise FandangoValueError("party_instance must not be None")
        super().__init__(
            connection_mode=connection_mode,
            ip_type=ip_type,
            ip=ip,
            port=port,
            party_instance=party_instance,
        )
        self._running = False
        assert protocol_type == Protocol.TCP or protocol_type == Protocol.UDP
        self._buffer_size = (
            UdpTcpProtocolImplementation.BUFFER_SIZE_TCP
            if protocol_type == Protocol.TCP
            else UdpTcpProtocolImplementation.BUFFER_SIZE_UDP
        )
        self._protocol_type = protocol_type
        self._sock: Optional[socket.socket] = None
        self._connection: Optional[socket.socket] = None
        self._send_thread: Optional[threading.Thread] = None
        self.current_remote_addr = None
        self._lock = threading.Lock()

    @property
    def protocol_type(self) -> Protocol:
        """
        :return: the protocol type of this socket.
        """
        return self._protocol_type

    def start(self) -> None:
        """
        Starts the UDP/TCP party according to the given configuration.
        If the party is already running or is not controlled by Fandango,
        it does nothing.
        """
        if self._running:
            return
        if not self._party_instance.is_fuzzer_controlled():
            return
        self.stop()
        self._create_socket()
        self._connect()

    def _create_socket(self) -> None:
        """
        Helper method; Creates a socket based on the protocol type (TCP/UDP) and IP type (IPv4/IPv6).
        """
        protocol = (
            socket.SOCK_STREAM
            if self._protocol_type == Protocol.TCP
            else socket.SOCK_DGRAM
        )
        ip_type = socket.AF_INET if self.ip_type == IpType.IPV4 else socket.AF_INET6
        self._sock = socket.socket(ip_type, protocol)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _connect(self) -> None:
        """
        Helper method; Connects or binds the socket based on the endpoint type (Open/Connect).
        """
        assert self.connection_mode != ConnectionMode.EXTERNAL
        if self.connection_mode == ConnectionMode.OPEN:
            assert self._sock is not None
            self._sock.bind((self.ip, self.port))
            if self.protocol_type == Protocol.TCP:
                self._sock.listen(1)
        self._running = True
        self._send_thread = threading.Thread(target=self._listen, daemon=True)
        self._send_thread.daemon = True
        self._send_thread.start()

    def stop(self) -> None:
        """Stops the current party."""
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

    def _wait_accept(self) -> None:
        """
        Helper method:
        * For TCP, waits for a connection to be accepted
        * Does nothing for UDP.
        """
        assert self.connection_mode != ConnectionMode.EXTERNAL
        with self._lock:
            if self._connection is None:
                if self.protocol_type == Protocol.TCP:
                    if self.connection_mode == ConnectionMode.OPEN:
                        assert self._sock is not None
                        while self._running:
                            rlist, _, _ = select.select([self._sock], [], [], 0.00001)
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
                            _, wlist, _ = select.select([], [self._sock], [], 0.00001)
                            if wlist:
                                self._connection = self._sock
                                break
                        self._sock.setblocking(True)
                else:
                    # For UDP, we do not need to accept a connection
                    assert self._sock is not None
                    self._connection = self._sock

    def _listen(self) -> None:
        """
        Helper method: Listens for incoming messages and forwards them to the party instance.
        """

        self._wait_accept()
        if not self._running:
            return

        while self._running:
            try:
                assert self._connection is not None
                rlist, _, _ = select.select([self._connection], [], [], 0.00001)
                if rlist and self._running:
                    if self.protocol_type == Protocol.TCP:
                        data = self._connection.recv(self._buffer_size)
                    else:
                        data, addr = self._connection.recvfrom(self._buffer_size)
                        self.current_remote_addr = addr
                    if len(data) == 0:
                        continue  # Keep waiting if connection is open but no data
                    self._party_instance.receive(data, None)
            except Exception:
                self._running = False
                break

    def send(
        self, message: DerivationTree | str | bytes, recipient: Optional[str]
    ) -> None:
        """
        Called when Fandango wants to send a message as this party.
        :param message: The message to send.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient.
        :raises FandangoError: If the party is not running.
        """
        assert self.connection_mode != ConnectionMode.EXTERNAL
        if not self._running:
            raise FandangoError(
                f"Party {self.party_name!r} not running. Invoke start() first."
            )
        self._wait_accept()

        assert self._connection is not None
        if isinstance(message, DerivationTree):
            send_data = message.to_bytes(encoding="utf-8")
        elif isinstance(message, str):
            send_data = message.encode("utf-8")
        elif isinstance(message, bytes):
            send_data = message
        else:
            raise FandangoValueError(
                f"Invalid message type: {type(message)}. Must be DerivationTree, str, or bytes."
            )
        if self.protocol_type == Protocol.TCP:
            self._connection.sendall(send_data)
        else:
            if self.connection_mode == ConnectionMode.OPEN:
                if self.current_remote_addr is None:
                    raise FandangoValueError(
                        f"Party {self.party_name!r} received no data yet. No address to send to."
                    )
                self._connection.sendto(send_data, self.current_remote_addr)
            else:
                self._connection.sendto(send_data, (self.ip, self.port))


class NetworkParty(FandangoParty):
    """
    A Fandango party that represents a remote UDP/TCP party (client or server).
    """

    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 8000
    DEFAULT_PROTOCOL = Protocol.TCP

    def __init__(
        self,
        uri: str,
        *,
        connection_mode: ConnectionMode = ConnectionMode.CONNECT,
    ):
        """
        NetworkParty constructor.
        :param uri: The party specification of the party to connect to. Format: `[name=][protocol:][//][host:]port`. Must match the `RE_PARTY` regex.

        :param connection_mode: ConnectionMode of the party:
        * `ConnectionMode.OPEN` - Fandango opens a server socket and waits for incoming connections and behaves as a server.
        * `ConnectionMode.CONNECT` - Fandango connects to an already running server socket and behaves as a client.
        * `ConnectionMode.EXTERNAL` - The party is an external party; no connection is made by Fandango. Messages annotated with this party are not produced by Fandango, but are expected to be received from an external party.
        """
        party_name, prot, host, port = split_party_spec(uri)
        super().__init__(connection_mode=connection_mode, party_name=party_name)
        self.protocol_impl = None

        if prot is None:
            prot = self.DEFAULT_PROTOCOL.value
        protocol = Protocol(prot)
        if host is None:
            host = self.DEFAULT_IP
        try:
            info = socket.getaddrinfo(host, None, socket.AF_INET)
            ip = info[0][4][0]
            ip_type = IpType.IPV4
        except socket.gaierror:
            info = socket.getaddrinfo(host, None, socket.AF_INET6)
            ip = info[0][4][0]
            ip_type = IpType.IPV6
        if isinstance(ip, int):
            raise FandangoValueError(
                f"Party {self.party_name}: Invalid IP address: {ip}"
            )
        if port is None:
            protocol = self.DEFAULT_PORT

        if protocol == Protocol.TCP or protocol == Protocol.UDP:
            self.protocol_impl = UdpTcpProtocolImplementation(
                connection_mode=connection_mode,
                protocol_type=protocol,
                ip_type=ip_type,
                ip=ip,
                port=port,
                party_instance=self,
            )
        else:
            raise FandangoValueError(
                f"Party {self.party_name}: Unsupported protocol: {protocol}"
            )

    # We defer all methods to the protocol implementation
    def send(
        self, message: DerivationTree | str | bytes, recipient: Optional[str]
    ) -> None:
        assert self.protocol_impl is not None
        self.protocol_impl.send(message, recipient)

    def start(self) -> None:
        assert self.protocol_impl is not None
        self.protocol_impl.start()

    def stop(self) -> None:
        assert self.protocol_impl is not None
        self.protocol_impl.stop()

    @property
    def ip(self) -> Optional[str]:
        assert self.protocol_impl is not None
        return self.protocol_impl.ip

    @ip.setter
    def ip(self, host: Optional[str]) -> None:
        """
        Sets the IP address for the connection; applied after a (re)start of the connection party.
        :param host: The hostname or IP address to set.
        """
        assert self.protocol_impl is not None

        info = socket.getaddrinfo(host, None, socket.AF_INET)
        ip = info[0][4][0]
        if isinstance(ip, int):
            raise FandangoValueError(
                f"Party {self.party_name}: Invalid IP address: {ip}"
            )
        self.protocol_impl.ip = ip

    @property
    def port(self) -> Optional[int]:
        assert self.protocol_impl is not None
        return self.protocol_impl.port

    @port.setter
    def port(self, port: Optional[int]) -> None:
        """Sets the port for the connection. Applied after a (re)start of the connection party."""
        assert self.protocol_impl is not None
        self.protocol_impl.port = port


class StdOut(FandangoParty):
    """
    Standard output party for sending messages to stdout. The party can only send messages, but not receive any.
    The party is always owned by Fandango (ConnectionMode.CONNECT), meaning it sends messages generated by Fandango.
    """

    def __init__(self) -> None:
        super().__init__(connection_mode=ConnectionMode.CONNECT)
        self.stream = sys.stdout

    def send(
        self, message: DerivationTree | str | bytes, recipient: Optional[str]
    ) -> None:
        if isinstance(message, DerivationTree):
            self.stream.write(message.to_string())
        elif isinstance(message, str):
            self.stream.write(message)
        elif isinstance(message, bytes):
            self.stream.buffer.write(message)
        else:
            raise FandangoValueError(
                f"Invalid message type: {type(message)}. Must be DerivationTree, str, or bytes."
            )

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass


class StdIn(FandangoParty):
    """
    Standard input party for reading messages from stdin. The party can only receive messages, but not send any.
    The connection mode of this party is always ConnectionMode.EXTERNAL, meaning it is an external party.
    """

    def __init__(self) -> None:
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)
        self.running = True
        self.stream = sys.stdin
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()

    def _listen_loop(self) -> None:
        while self.running:
            rlist, _, _ = select.select([self.stream], [], [], 0.1)
            if rlist:
                read = sys.stdin.readline()
                if read == "":
                    self.running = False
                    break
                self.receive(read, self.party_name)
            else:
                time.sleep(0.1)


class Out(FandangoParty):
    """
    Standard output party for receiving messages from an external process set using set_program_command(command: str).
    The party can only receive messages, but not send any.
    The connection mode of this party is always ConnectionMode.EXTERNAL, meaning it is an external party.
    """

    def __init__(self) -> None:
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)
        self.proc = ProcessManager.instance().get_process()
        threading.Thread(target=self._listen_loop, daemon=True).start()

    def _listen_loop(self) -> None:
        while True:
            if self.proc.stdout is not None:
                line = self.proc.stdout.read(1)
                self.receive(line, self.party_name)


class In(FandangoParty):
    """
    Standard input party for sending messages to an external process set using set_program_command(command: str).
    The party can only send messages, but not receive any.
    The connection mode of this party is always ConnectionMode.CONNECT, meaning it sends messages generated by Fandango.
    """

    def __init__(self) -> None:
        super().__init__(connection_mode=ConnectionMode.CONNECT)
        self.proc = ProcessManager.instance().get_process()
        self._close_post_transmit = False

    @property
    def close_post_transmit(self) -> bool:
        """
        Returns whether the stdin of the process should be closed after transmitting a message.
        """
        return self._close_post_transmit

    @close_post_transmit.setter
    def close_post_transmit(self, value: bool) -> None:
        """
        Sets whether the stdin of the process should be closed after transmitting a message.
        """
        if self._close_post_transmit == value:
            return
        self._close_post_transmit = value

    def send(
        self, message: DerivationTree | str | bytes, recipient: Optional[str]
    ) -> None:
        if self.proc.stdin is not None:
            if isinstance(message, DerivationTree):
                self.proc.stdin.write(message.to_string())
            elif isinstance(message, str):
                self.proc.stdin.write(message)
            elif isinstance(message, bytes):
                self.proc.stdin.write(message.decode("utf-8"))
            else:
                raise FandangoValueError(
                    f"Party {self.party_name}: Invalid message type: {type(message)}. Must be DerivationTree, str, or bytes."
                )
            self.proc.stdin.flush()
            if self.close_post_transmit:
                self.proc.stdin.close()


class FandangoIO(object):
    """
    Singleton class for managing all `FandangoParty` parties.
    This object keeps track of all communication parties and relates them to Fandango.
    Used internally by Fandango; do not use directly.
    """

    _instances: dict[EnvKey, "FandangoIO"] = {}
    _lock = threading.Lock()

    @classmethod
    def instance(cls) -> "FandangoIO":
        """
        Returns the singleton instance of FandangoIO. If it does not exist, it creates one.
        Only use this method to access the FandangoIO instance.
        """
        try:
            assert CURRENT_ENV_KEY.contextVar is not None
            env_key = CURRENT_ENV_KEY.contextVar.get()
        except LookupError:
            raise RuntimeError(
                "FandangoIO.instance() called without an active environment"
            )

        with cls._lock:
            if env_key not in cls._instances:
                cls._instances[env_key] = cls()
            return cls._instances[env_key]

    def __init__(self) -> None:
        """
        Constructor for the FandangoIO class. Singleton! Do not call this method directly. Call instance() instead.
        """
        self.receive: list[tuple[str, str, str | bytes]] = []
        self.parties: dict[str, FandangoParty] = {}
        self.receive_lock = threading.Lock()

    def reset_parties(self) -> None:
        """
        Restart all parties.
        """
        with self.receive_lock:
            for party in self.parties.values():
                party.stop()
            self.receive.clear()
            for party in self.parties.values():
                party.start()

    def get_fuzzer_parties(self) -> set[FandangoParty]:
        """
        Returns the set of all parties controlled by Fandango.
        """
        return set(filter(lambda i: i.is_fuzzer_controlled(), self.parties.values()))

    def add_receive(self, sender: str, receiver: str, message: str | bytes) -> None:
        """
        Forwards an external received message to Fandango for processing.
        :param sender: The sender of the message.
        :param receiver: The receiver of the message.
        :param message: The message received from the sender.
        """
        with self.receive_lock:
            if isinstance(message, bytes):
                for fragment_int in message:
                    self.receive.append((sender, receiver, bytes([fragment_int])))
            else:
                for fragment_str in message:
                    self.receive.append((sender, receiver, fragment_str))

    def received_msg(self) -> bool:
        """
        Returns True iff there are any received messages from external parties.
        """
        with self.receive_lock:
            return len(self.receive) != 0

    def get_full_fragments(
        self,
    ) -> list[tuple[str, str, str | bytes]]:
        """
        Returns a list of all received messages from external parties, combining consecutive fragments from the same sender to the same receiver.
        """
        fragments: list[tuple[str, str, str | bytes]] = []
        prev_sender: Optional[str] = None
        prev_recipient: Optional[str] = None
        for idx, (sender, recipient, msg_fragment) in enumerate(
            self.get_received_msgs()
        ):
            if (
                prev_sender != sender
                or prev_recipient != recipient
                or (
                    type(fragments[-1][2]) != type(msg_fragment) if fragments else False
                )
            ):
                prev_sender = sender
                prev_recipient = recipient
                fragments.append((sender, recipient, msg_fragment))
            elif isinstance(fragments[-1][2], bytes) and isinstance(
                msg_fragment, bytes
            ):
                new_constructed_msg_bytes = fragments[-1][2] + msg_fragment
                fragments[-1] = (sender, recipient, new_constructed_msg_bytes)
            else:
                assert isinstance(fragments[-1][2], str) and isinstance(
                    msg_fragment, str
                )
                new_constructed_msg_str = fragments[-1][2] + msg_fragment
                fragments[-1] = (sender, recipient, new_constructed_msg_str)
        return fragments

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

    def clear_by_party(self, party_name: str, to_idx: int) -> None:
        """Clears all received messages from a specific party up to a given index."""

        with self.receive_lock:
            self.receive = [
                (sender, receiver, msg)
                for idx, (sender, receiver, msg) in enumerate(self.receive)
                if not (sender == party_name and idx <= to_idx)
            ]

    def transmit(
        self, sender: str, recipient: Optional[str], message: DerivationTree
    ) -> None:
        """
        Called by Fandango to transmit a message from a sender to a recipient using the sender's party definition.
        :param sender: The sender of the message. Needs to be equal to the class name of the corresponding party definition.
        :param recipient: The recipient of the message. Only present if the grammar specifies a recipient. Can be used by the party definition to send the message to the correct recipient.
        :param message: The message to send.
        """
        if sender in self.parties.keys():
            self.parties[sender].send(message, recipient)


class ProcessManager(object):
    """
    Singleton class for managing the subprocess used by In/Out parties.
    Used internally by Fandango; do not use directly.
    """

    _instances: dict[EnvKey, "ProcessManager"] = {}
    _lock = threading.Lock()

    def __init__(self) -> None:
        """
        Constructor for the ProcessManager class. Singleton! Do not call this method directly. Call instance() instead.
        """
        self._command: Optional[str | list[str]] = None
        self.lock = threading.Lock()
        self.proc: Optional[subprocess.Popen[str]] = None
        self.text = True

    @classmethod
    def instance(cls) -> "ProcessManager":
        """
        Returns the singleton instance of ProcessManager. If it does not exist, it creates one.
        """
        try:
            assert CURRENT_ENV_KEY.contextVar is not None
            env_key = CURRENT_ENV_KEY.contextVar.get()
        except LookupError:
            raise RuntimeError(
                "ProcessManager.instance() called without an active environment"
            )

        with cls._lock:
            if env_key not in cls._instances:
                cls._instances[env_key] = cls()
            return cls._instances[env_key]

    def get_process(self) -> subprocess.Popen[str]:
        """
        Returns the current process if it exists, otherwise starts a new one based on the command set.
        """
        with self.lock:
            if not self.proc:
                self._start_process()
        if self.proc is None:
            raise FandangoValueError(
                "This spec requires interaction. Use `--party=PARTY` or `fandango talk` with this spec."
            )
        return self.proc

    @property
    def command(self) -> Optional[str | list[str]]:
        """Returns the command to be executed to start the process."""
        return self._command

    def set_command(self, value: str | list[str], text: bool = True) -> None:
        """Sets the command to be executed to start the process."""
        assert isinstance(
            value, (str, list)
        ), "Command must be a string or a list of strings"
        with self.lock:
            if self._command == value:
                return
            self._command = value
        self.text = text

    def _start_process(self) -> None:
        command = self.command
        if command is None:
            return

        LOGGER.info(f"Starting subprocess with command {command}")
        self.proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=self.text,
        )


def set_program_command(command: str | list[str], text: bool = True) -> None:
    """
    Set the command to be executed by In/Out parties.
    The parameters are passed to `subprocess.Popen()`:
    :param command: The command to execute - either as a string or as a list of strings.
    :param text: Whether to open the process in text mode (True, default) or binary mode (False).
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
