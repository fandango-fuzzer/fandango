---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:fandangoparty)=
# FandangoParty Reference

All communication between Fandango and its parties is established via `FandangoParty` classes.
The following diagram illustrates the classes and methods discussed in this chapter:

```{mermaid}
classDiagram
    class FandangoParty {
        <<abstract>>
        FandangoParty(ownership: Ownership, party_name: str | None)
        send(message: DerivationTree, recipient: str | None)
        receive(message: str | bytes, sender: str | None)
        start()
        stop()
    }
    FandangoParty <|-- NetworkParty
    class NetworkParty{
        NetworkParty(uri: str, ownership: Ownership, endpoint_type: EndPointType)
        ip: str
        port: int
    }
    NetworkParty <|-- Server
    NetworkParty <|-- Client
    NetworkParty <|.. `(Own Classes)`
    FandangoParty <|-- In
    FandangoParty <|-- Out
    class Ownership {
         <<enumeration>>
        FANDANGO_PARTY
        EXTERNAL_PARTY
    }
    class EndPointType {
         <<enumeration>>
        CONNECT
        OPEN
    }
    click FandangoParty href "#the-fandangoparty-class" "Base class for communicating with a party"
    click NetworkParty href "#the-networkparty-class" "Connect to an Internet party"
    click In href "#in-and-out" "Connect to standard input of an external program"
    click Out href "#in-and-out" "Connect to standard output of an external program"
    click Client href "#client-and-server" "Connect to a client"
    click Server href "#client-and-server" "Connect to a server"
```

All classes are predefined within `.fan` files; they need not be imported.


(sec:fandangoparty-class)=
## The `FandangoParty` class

`FandangoParty` is an abstract base class. It is meant to serve as base class for subclasses and cannot be directly instantiated.

### Constructor

```python
FandangoParty(ownership: Ownership, party_name: Optional[str])
```

* `ownership`: Whether this party is
    - controlled by Fandango (`Ownership.FANDANGO_PARTY`); or
    - an external party (`Ownership.EXTERNAL_PARTY`).
* `party_name`: The name of the party. If `None`, the class name is used.


(sec:send-api)=
### The `send()` method

On a `FandangoParty` object, the `send()` method is used to send a message (as a [`DerivationTree` object](sec:derivation-tree)) to a party.

```python
send(message: DerivationTree, recipient: Optional[str]) -> None
```

* `message: DerivationTree`: The message to send.
* `recipient: str`: The recipient of the message. Only present if the grammar specifies a recipient.

This method is typically overloaded and extended in subclasses.
For instance, to apply a `compress()` method to every message sent, write

```python
class CompressedNetworkParty(NetworkParty):
    def send(self, message: DerivationTree, recipient: Optional[str]) -> None:
        super().send(compress(message), recipient)
```

```{important}
Note that the `message` argument to `send()` is of type `DerivationTree`.
```


(sec:receive-api)=
### The `receive()` method

On a `FandangoParty` object, the `receive()` method is invoked when data has been received by the party.

```python
receive(message: str | bytes), sender: Optional[str]) -> None
```

* `message: DerivationTree`: The message to send.
* `recipient: str`: The recipient of the message. Only present if the grammar specifies a recipient.

This method is typically overloaded and extended in subclasses.
For instance, to apply a `decompress()` method to every message received, write

```python
class CompressedNetworkParty(NetworkParty):
    def receive(self, message: DerivationTree, sender: Optional[str]) -> None:
        super().receive(uncompress(message), sender)
```


(sec:startstop-api)=
### The `start()` and `stop()` methods

On a `FandangoParty` object, the `start()` and `stop()` methods are invoked to establish or shut down a connection.

```python
start() -> None
stop() -> None
```

These methods can be used in subclasses to add additional behavior.


(sec:networkparty-class)=
## The `NetworkParty` class

The Fandango `NetworkParty` class (a subclass of `FandangoParty`) implements an Internet connection to a communication party.
It implements the `FandangoParty` methods, as described above, plus the following methods:


### Constructor

```python
NetworkParty(uri: str, ownership: Ownership, endpoint_type: EndPointType)
```

* `uri` (string): The party specification of the party to connect to.
   Format: `[NAME=][PROTOCOL:][//][HOST:]PORT`.
    - `NAME`: Party name. Default: the class name.
    - `PROTOCOL`: `tcp` (default) or `udp`.
    - `HOST`: host name; use `[...]` for IPv6 host names. Default: 127.0.0.1
    - `PORT`: the port to connect to (0-65535)
* `ownership`: Whether this party is
    - controlled by Fandango (`Ownership.FANDANGO_PARTY`, default); or
    - an external party (`Ownership.EXTERNAL_PARTY`).
* `endpoint_type`: Whether Fandango should
    - connect to an already running server socket (`EndpointType.CONNECT`, default); or
    - open a server socket and wait for incoming connections (`EndpointType.OPEN`).

### Properties

```python
ip: str
```
The IP address or host used. Can be assigned to.

```python
port: int
```
The port. Can be assigned to.


(sec:predefined-parties)=
## Predefined Parties

The following parties are predefined in Fandango:

(sec:in-out-parties)=
### `In` and `Out`

`In` and `Out` are `FandangoParty` classes connecting to the standard input and the standard output of an invoked program.

```python
In()
```

Constructor.

```python
Out()
```

Constructor.


(sec:client-server-parties)=
### `Client` and `Server`

`Server` are `NetworkParty` classes created with the `--server` option on the `fandango` executable command line.

If `--client URI` is given, `fandango` becomes a `Client`, and the classes are created as

```python
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,  # the argument in `--client URI`
            ownership=Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.CONNECT,
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,  # the argument in `--client URI`
            ownership=Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.OPEN,
        )
        self.start()
```

If `--server URI` is given, `fandango` becomes a `Server`, and the classes are created as

```python
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,  # the argument in `--server URI`
            ownership=Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT,
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,  # the argument in `--server URI`
            ownership=Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.OPEN,
        )
        self.start()
```
