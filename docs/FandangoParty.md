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




(sec:fandangoparty-class)=
## The `FandangoParty` class

The `FandangoParty` class is an abstract base class, predefined within `.fan` files.

### Constructor

`FandangoParty` is an abstract base class. It is meant to serve as base class for subclasses and cannot be directly instantiated.

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
Note that the message sent to `send()` is of type `DerivationTree`.
```


(sec:receive-api)=
### The `receive()` method

On a `FandangoParty` object, the `receive()` method is invoked when data has been received by the party.

```python
receive(sender: Optional[str], message: str | bytes)) -> None
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
## Predefined classes

The following parties are predefined in Fandango:

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


### `Client` and `Server`

`Server` are `FandangoParty` classes created with the `--server` option on the `fandango` command line.

If `--client URI` is given, fandango becomes a `Client`, and the classes are created as

```python
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,
            ownership=Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.CONNECT,
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,
            ownership=Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.OPEN,
        )
        self.start()
```

If `--server URI` is given, fandango becomes a `Server`, and the classes are created as

```python
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,
            ownership=Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT,
        )
        self.start()

class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            URI,
            ownership=Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.OPEN,
        )
        self.start()
```
