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

(sec:parties)=
# Customizing Party Communication

In the [previous chapter](sec:protocols), we have seen how to define and test protocol interactions with Fandango.
In this chapter, we describe additional ways to control communication behavior.

## Party Classes

All the communication between Fandango and its parties takes place via dedicated _classes_.
In fact, prefixes like `Client` and `Server` in [protocol testing](sec:protocols) or `In` and `Out` when [checking outputs](sec:outputs) all stand for predefined _classes_ that implement a set of methods to handle the communication:

* `Client` and `Server` are `NetworkParty` classes, detailed in the [`FandangoParty` reference](FandangoParty.md).
* `In` and `Out` are `FandangoParty` classes, detailed in the [`FandangoParty` reference](FandangoParty.md).

The fact that these are classes allows you to _implement your own communication classes_ and define code that should be executed when starting, stopping, or communicating with a party.
This is typically done by _subclassing_ one of the existing classes.

## Extending Party Functionality

### Starting a Party

The `NetworkParty` class has a `start()` method that is invoked whenever the respective party is started.
You can extend this method to execute additional code, for instance to create configuration files.
To this end, simply subclass the respective party class and override its `start()` method:

```python
def create_configuration_file() -> None:
    ... # Your code goes here

class MyClient(Client):
    def start(self) -> None:
        create_configuration_file()
        super().start()  # Invoke the start() method of the superclass
```

This definition goes right into the `.fan` file.

:::{important}
In the grammar, be sure to use your own class name - in this case, `MyClient`. Only then will your definition be used.
```python
<start> ::= <MyClient:send> <Server:respond>
<send> ::= ...
```
:::

:::{tip}
You can also _override_ existing class names. With this hack, you do not have to change the grammar:

```python
class Client(Client):  # extends the original `Client` class
    def start(self) -> None:
        create_configuration_file()
        super().start()  # Invoke the start() method of the superclass
```
:::

See the [`FandangoParty` reference](sec:start-api) for details on `start()`.


### Stopping a Party

In the same way as extending starting a party, one can also hook into _stopping_ a party – for cleanup actions, for instance.
The `stop()` method is useful for this:

```python
def cleanup_server() -> None:
    ... # Your code goes here

class Server(Server):
    def stop(self):
        cleanup_server()
        super().stop()  # Invoke the stop() method of the superclass
```

Again, this definition goes right into the `.fan` file.
See the [`FandangoParty` reference](sec:stop-api) for details on `stop()`.


### Sending Messages

Whenever Fandango wants to send messages to a party, it invokes its `send()` message.
As with `start()` and `stop()`, above, you can extend the `send()` method for your own needs.
This includes

* altering messages (e.g. encrypt or compress them)
* logging information
* reacting to specific messages

Here is an example in which we compress the `DerivationTree` passed via a `compress()` function.

```python
def compress(msg: bytes) -> bytes:
    compressed_message = ... # Your code goes here
    return compressed_message

class Server(Server):
    def send(self, message: DerivationTree | bytes | str, recipient: Optional[str]):
        compressed_message = compress(message.to_bytes())
        super().send(compressed_message, recipient)
```

```{important}
When called from Fandango, `message` always is of type [`DerivationTree`](DerivationTree.md);
this allows you to access its constituents (as in `to_bytes()`, above).
However, the `FandangoParty` classes all support sending `DerivationTree`, `str`, and `bytes` types, so you do not have to re-create a `DerivationTree` object when calling `send()`.
```

```{note}
For encodings, compression, and other alterations, you can also use a [data converter](sec:conversion) instead.
```

See the [`FandangoParty` reference](sec:send-api) for details on `send()`.



### Receiving Messages

Whenever Fandango receives messages from a party, it invokes its `receive()` message.
Again, you can extend this for your own needs.

Here is an example in which we decompress the message received via a `decompress()` function.

```python
def decompress(msg: bytes) -> bytes:
    decompressed_message = ... # Your code goes here
    return decompressed_message

class Server(Server):
    def receive(self, message: str | bytes, sender: Optional[str]):
        decompressed_message = decompress(message)
        super().receive(decompressed_message, sender)
```

Again, this definition goes right into the `.fan` file.
See the [`FandangoParty` reference](sec:receive-api) for details on `receive()`.


## Own Network Parties

If your setting uses more than just `client` or `server` parties, or if the existing `--client` and `--server` options to Fandango are not sufficient, you can define your own network parties by subclassing one of the [`NetworkParty` classes](sec:networkparty-class).

```{margin}
`Server_1` and `Server_2` could also be two channels to the same server; likewise with the client.
```

As an example, consider a protocol where two clients `Client_1` and `Client_2` connect to the servers `Server_1` and `Server_2`, respectively.
Using the [`NetworkParty` constructor](sec:networkparty-class), the respective `.fan` file would contain these definitions:

```python
class Client_1(NetworkParty):
    def __init__(self):
        super().__init__("localhost:8000",
                         ownership=Ownership.FANDANGO_PARTY,
                         endpoint_type=EndpointType.CONNECT)

class Server_1(NetworkParty):
    def __init__(self):
        super().__init__("localhost:8000",
                         ownership=Ownership.EXTERNAL_PARTY,
                         endpoint_type=EndpointType.OPEN)

class Client_2(NetworkParty):
    def __init__(self):
        super().__init__("localhost:8000",
                         ownership=Ownership.FANDANGO_PARTY,
                         endpoint_type=EndpointType.CONNECT)

class Server_2(NetworkParty):
    def __init__(self):
        super().__init__("localhost:8001",
                         ownership=Ownership.EXTERNAL_PARTY,
                         endpoint_type=EndpointType.OPEN)
```

The grammar can then use `Client_1`, `Client_2`, `Server_1`, and `Server_2` as prefixes, and specify a protocol that involves all four parties.
As specified, Fandango would operate as client (1 and 2) and fuzz the two servers.

```{tip}
Use one `.fan` file to specify the protocol, and a second one (which [includes](sec:hatching) the first) to specify details on where and how the clients and servers are located.
This allows alternate settings to also make use (= include) the protocol spec - say, a setting in which Fandango acts as server(s) to fuzz the clients.
```

(sec:party-instance)=
## Accessing Network Parties at Runtime

If the party configuration changes at runtime (see the [FTP](sec:ftp) case study for an example), you may need to access the individual party objects.
Use [`PARTY.instance()`](sec:instance-api) for this, where `PARTY` is the class of the respective party.

For instance, to stop the `Server` object, use

```python
... Server.instance().stop()
```

If you have given your party an individual name, pass its name as a string argument.
In this case, the class is ignored; `FandangoParty` will do fine. The code

```python
... FandangoParty.instance("Server").stop()
```

is equivalent to the above.


In the next chapters, we look at how [FTP](sec:ftp) and [DNS](sec:dns) protocol specs make use of these features.