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

```{versionadded} 1.1
These features are available in Fandango 1.1 and later.
```

The following diagram illustrates the classes and methods discussed in this chapter:

```{mermaid}
classDiagram
    class FandangoParty {
        <<abstract>>
        FandangoParty(connection_mode: ConnectionMode, party_name: str | None)
        send(message: DerivationTree | str | bytes, recipient: str | None)
        receive(message: str | bytes, sender: str | None)
        start()
        stop()
    }
    FandangoParty <|-- NetworkParty
    class NetworkParty{
        NetworkParty(uri: str, connection_mode: ConnectionMode)
        ip: str
        port: int
    }
    NetworkParty <|-- Server
    NetworkParty <|-- Client
    NetworkParty <|.. `(Own Classes)`
    FandangoParty <|-- In
    FandangoParty <|-- Out
    FandangoParty <|-- StdIn
    FandangoParty <|-- StdOut
    class ConnectionMode {
         <<enumeration>>
        OPEN
        CONNECT
        EXTERNAL
    }
    click FandangoParty href "#the-fandangoparty-class" "Base class for communicating with a party"
    click NetworkParty href "#the-networkparty-class" "Connect to an Internet party"
    click In href "#in-and-out" "Connect to standard input of an external program"
    click Out href "#in-and-out" "Connect to standard output of an external program"
    click StdIn href "#in-and-out" "Connect to standard input of Fandango"
    click StdOut href "#in-and-out" "Connect to standard output of Fandango"
    click Client href "#client-and-server" "Connect to a client"
    click Server href "#client-and-server" "Connect to a server"
    click ConnectionMode href "#the-fandangoparty-class" "Connection mode for a FandangoParty"
```

All classes are predefined within `.fan` files; they need not be imported.


(sec:fandangoparty-class)=
## The `FandangoParty` class

`FandangoParty` is an abstract base class. It is meant to serve as base class for subclasses and cannot be directly instantiated.

### Constructor

```python
FandangoParty(connection_mode: ConnectionMode, party_name: str | None = None)
```
* `connection_mode`: Can be one of three values:
    * `ConnectionMode.OPEN` - Fandango behaves as a _server_. It opens a port and waits for incoming connections.
    * `ConnectionMode.CONNECT` - Fandango behaves as a _client_. It uses an existing port and connects to it.
    * `ConnectionMode.EXTERNAL` - The party is an external party; no connection is made by Fandango. Messages annotated with this party are not produced by Fandango, but are expected to be received from an external party.
* `party_name`: The name of the party. If `None`, the class name is used.


(sec:send-api)=
### The `send()` method

On a `FandangoParty` object, the `send()` method is used to send a message (as a [`DerivationTree` object](sec:derivation-tree)) to a party.

```python
send(message: DerivationTree | str | bytes, recipient: Optional[str]) -> None
```

* `message: DerivationTree | str | bytes`: The message to send.
* `recipient: str`: The recipient of the message. Only present if the grammar specifies a recipient.

This method is typically overloaded and extended in subclasses.
For instance, to apply a `compress()` method to every message sent, write

```python
class CompressedNetworkParty(NetworkParty):
    def send(self, message: DerivationTree | str | bytes, recipient: Optional[str]) -> None:
        super().send(compress(message), recipient)
```

```{important}
Fandango itself will always invoke `send()` with a [`DerivationTree`](DerivationTree.md) as argument.
However, the `FandangoParty` classes all support sending `DerivationTree`, `str`, and `bytes` types, so you do not have to re-create a `DerivationTree` object when calling `send()`.
```



(sec:receive-api)=
### The `receive()` method

On a `FandangoParty` object, the `receive()` method is invoked when data has been received by the party.

```python
receive(message: str | bytes), sender: Optional[str]) -> None
```

* `message: str | bytes`: The message received.
* `recipient: str`: The sender of the message.

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


(sec:instance-api)=
### The `instance()` class method

`FandangoParty` provides an `instance()` class method that retrieves the last created instance of the given class.

```python
instance(party_name: str | None = None) -> FandangoParty
```

`instance()` is typically invoked prefixed with the respective class, as in 

```
Client.instance().stop()  # Stop the client
```

One can also invoke it with a party name; in that case, the class is ignored (use `FandangoParty`), and `instance()` retrieves the instance created with that name.

```
FandangoParty.instance("Client").stop()  # Equivalent to the above.
```



(sec:networkparty-class)=
## The `NetworkParty` class

The Fandango `NetworkParty` class (a subclass of `FandangoParty`) implements an Internet connection to a communication party.
It implements the `FandangoParty` methods, as described above, plus the following methods:


### Constructor

```python
NetworkParty(uri: str, connection_mode: ConnectionMode = ConnectionMode.CONNECT)
```

* `uri` (string): The party specification of the party to connect to.
   Format: `[NAME=][PROTOCOL:][//][HOST:]PORT`.
    - `NAME`: Party name. Default: the class name.
    - `PROTOCOL`: `tcp` (default) or `udp`.
    - `HOST`: host name; use `[...]` for IPv6 host names. Default: 127.0.0.1
    - `PORT`: the port to connect to (0-65535)
* `connection_mode`: Can be one of three values:
    * `ConnectionMode.OPEN` - Fandango behaves as a _server_. It opens the given URI and waits for incoming connections.
    * `ConnectionMode.CONNECT` - Fandango behaves as a _client_. It connects to the given URI.
    * `ConnectionMode.EXTERNAL` - The party is an external party; no connection is made by Fandango. Messages annotated with this party are not produced by Fandango, but are expected to be received from an external party.

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


(sec:stdin-stdout-parties)=
### `StdIn` and `StdOut`

`StdIn` and `StdOut` are `FandangoParty` classes connecting to the standard input and the standard output of Fandango.

```python
StdIn()
```

Constructor.

```python
StdOut()
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
            connection_mode=ConnectionMode.CONNECT,
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,  # the argument in `--client URI`
            connection_mode=ConnectionMode.EXTERNAL,
        )
        self.start()
```

If `--server URI` is given, `fandango` becomes a `Server`, and the classes are created as

```python
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,  # the argument in `--server URI`
            connection_mode=ConnectionMode.EXTERNAL,
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,  # the argument in `--server URI`
            connection_mode=ConnectionMode.OPEN,
        )
        self.start()
```
