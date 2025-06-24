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

(sec:protocols)=
# Testing Protocols

In [the chapter on checking outputs](sec:outputs), we already have seen how to interact with external programs.
In this chapter, we will extend this concept to full _protocol testing_ across networks.
This includes:

* Acting as a network _client_ and interacting with network servers  using generated inputs
* Acting as a network _server_ and interacting with network clients using generated inputs.

```{admonition} Under Construction
:class: attention
Protocol testing is currently in beta.
Check out [the list of open issues](https://github.com/fandango-fuzzer/fandango/issues).
```

## Interacting with an SMTP server

The Simple Mail Transfer Protocol (SMTP) is, as the name suggests, a simple protocol through which mail clients can connect to a server to send mail to recipients.
A [typical interaction with an SMTP server](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) `smtp.example.com`, sending a mail from `bob@example.org` to `alice@example.com`, is illustrated below:

```{mermaid}
sequenceDiagram
    SMTP Client->>SMTP Server: (connect)
    SMTP Server->>SMTP Client: 220 smtp.example.com ESMTP Postfix
    SMTP Client->>SMTP Server: HELO relay.example.org
    SMTP Server->>SMTP Client: 250 Hello relay.example.org, glad to meet you
    SMTP Client->>SMTP Server: MAIL FROM:<bob@example.org>
    SMTP Server->>SMTP Client: 250 Ok
    SMTP Client->>SMTP Server: RCPT TO:<alice@example.com>
    SMTP Server->>SMTP Client: 250 Ok
    SMTP Client->>SMTP Server: DATA
    SMTP Server->>SMTP Client: 354 End data with <CR><LF>.<CR><LF>
    SMTP Client->>SMTP Server: From: "Bob Example" <bob@example.org>
    SMTP Client->>SMTP Server: To: "Alice Example" <alice@example.com>
    SMTP Client->>SMTP Server: Subject: Protocol Testing with I/O Grammars
    SMTP Client->>SMTP Server: (mail body)
    SMTP Client->>SMTP Server: .
    SMTP Server->>SMTP Client: 250 Ok: queued as 12345
    SMTP Client->>SMTP Server: QUIT
    SMTP Server->>SMTP Client: 221 Bye
    SMTP Server->>SMTP Client: (closes the connection)
```

Our job will be to _automate this interaction_ using Fandango.
For this, we need two things:

1. An SMTP server to send commands to
2. A `.fan` spec that encodes this interaction.


## An SMTP server for experiments

For illustrating protocol testing, we need to run an SMTP server, which we will run locally on our machine.
(No worries - the local SMTP server can not actually send mails across the Internet.)

The Python `aiosmtpd` server will do the trick:

```shell
$ pip install aiosmtpd
```

Once installed, we can run the server locally; normally, it runs on port 8025:

```shell
$ python -m aiosmtpd -d -n
INFO:mail.log:Server is listening on localhost:8025
```

We can now connect to the server on the given port and send it commands.
The `telnet` command is handy for this.
We give it a hostname (`localhost` for our local machine) and a port (8025 for our local SMTP server.)

Once connected, anything we type into the `telnet` input will automatically be relayed to the given port, and hence to the SMTP server.
For instance, a `QUIT` command (followed by Return) will terminate the connection.

```shell
$ telnet localhost 8025
Trying ::1...
Connected to localhost.
Escape character is '^]'.
220 localhost.example.com Python SMTP 1.4.6
QUIT
221 Bye
Connection closed by foreign host.
```

Try this for yourself! What happens if you invoke `telnet`, introducing yourself with  `HELO client.example.com`?

:::{admonition} Solution
:class: tip, dropdown
When sending `HELO client.example.com`, the server replies with its own hostname.
This is the name of the local computer, in our example `localhost.example.com`.

```shell
$ telnet localhost 8025
Trying ::1...
Connected to localhost.
Escape character is '^]'.
220 localhost.example.com Python SMTP 1.4.6
HELO client.example.com
250 localhost.example.com
QUIT
221 Bye
```
:::




## A simple SMTP grammar

```{margin}
We use `telnet` only for illustrative purposes here; later in this chapter, you will see how to have Fandango directly connect to servers (and clients!)
```

With [`fandango talk`](sec:outputs), we have seen a Fandango facility that allows us to connect to the standard input and output channels of a given program and interact with it.
The idea would now be to use the `telnet` program for this very purpose.
By invoking

```shell
$ fandango talk -f smtp-telnet.fan telnet 8025
```

we could interact with the `telnet` program as described above.
All we now need is a grammar that describes the `telnet` interaction.

The following grammar has two parts:

1. First, we expect some output from the `telnet` program.
2. Then, we interact with the SMTP server - just sending a `QUIT` command and then exiting.

A typical interaction thus would be:

```{mermaid}
sequenceDiagram
    Fandango->>telnet: (invoke)
    telnet->>Fandango: Trying ::1...
    telnet->>Fandango: Connected to localhost.
    telnet->>Fandango: Escape character is '^]'.
    SMTP Server (via telnet)->>Fandango: 220 localhost.example.com Python SMTP 1.4.6
    Fandango->>SMTP Server (via telnet): QUIT
    SMTP Server (via telnet)->>Fandango: 221 Bye
    SMTP Server (via telnet)->>telnet: (closes connection)
    telnet->>Fandango: (ends execution)
```

The following I/O grammar [smtp-telnet.fan](smtp-telnet.fan) implements this interaction via `telnet`:

1. First, `<telnet-intro>` lets Fandango expect the `telnet` introduction;
2. Then, `<smtp>` takes care of the actual SMTP interaction.

```{code-cell}
:tags: ["remove-input"]
!cat smtp-telnet.fan
```

```{note}
Again, note that `In` and `Out` describe the interaction from the _perspective of the program under test_; hence, `Out` is what `telnet` and the SMTP server produce, whereas `In` is what the SMTP server (and telnet) get as input.
```

With this, we can now connect to our (hopefully still running) SMTP server and actually send it a `QUIT` command:

```shell
$ fandango talk -f smtp-telnet.fan telnet 8025
```

% FIXME: Add output

To track the data that is actually exchanged, use the verbose `-v` flag.
The `In:` and `Out:` log messages show the data that is being exchanged.

```shell
$ fandango -v talk -f smtp-telnet.fan telnet 8025
```

% FIXME: Add output


## Interacting as Network Client

Using `telnet` to communicate with servers generally works, but it has a number of drawbacks.
Most importantly, `telnet` is meant for _human_ interaction.
Hence, our I/O grammars have to reflect the `telnet` output (which actually might change depending on operating system and configuration); also, `telnet` is not suited for transmitting binary data.

Fortunately, Fandango offers a means to be invoked _directly as a network client_, not requiring external programs such as `telnet`.
The `fandango talk` option `--client` allows Fandango to be used as a network client.
The argument to `--client` is a network address to connect to.
In the simplest form, it is just a port number on the local machine.

Hence, to have Fandango act as an SMTP client for the local server, we can enter

```shell
$ fandango talk -f SPEC.fan --client 8025
```

Since Fandango directly talks to the SMTP server now, we can also simplify the grammar by removing the `<telnet_intro>` part.
Also, there is no more `In` and `Out` parties, since we do not interact with the standard input and output of an invoked program.
Instead,

* `Client` is the party representing the _client_, connecting to an external server on the network.
* `Server` is the party representing a _server_ on the network, accepting connections from clients.

Consequently,

* all outputs produced by the _client_ (and processed by the server) are prefixed with `Client:` in the respective nonterminals; and
* all outputs produced by the _server_ (and processed by the client) are prefixed with `Server:`.

With this, we can reframe and simplify our SMTP grammar, using `Client` and `Server` to describe the respective interactions.
The spec [`smtp-simple.fan`](smtp-simple.fan) reads as follows:

```{code-cell}
:tags: ["remove-input"]
!cat smtp-simple.fan
```

Note how we added `<hostname>` as additional specification of the hostname that is typically part of the initial server message.

With this, we have Fandango act as client and connect to the (hopefully still running) server on port 8025:

```shell
$ fandango talk -f smtp-simple.fan --client 8025
```

% FIXME: Describe output

```{mermaid}
sequenceDiagram
    Fandango->>SMTP Server: (connect)
    SMTP Server->>Fandango: 220 host.example.com <more data>
    Fandango->>SMTP Server: QUIT
    SMTP Server->>Fandango: 221 <more data>
    SMTP Server->>Fandango: (closes connection)
```

From here on, we can have Fandango directly "talk" to network components such as servers.


## Interacting as Network Server

Obviously, our SMTP specification is still very limited.
Before we go and extend it, let us first highlight a particular Fandango feature.
From the same specification, Fandango can act as a _client_ and as a _server_.
When invoked with the `--server` option, Fandango will _create_ a server at the given port and accept client connections.
So if we invoke

```shell
$ fandango talk -f smtp-simple.fan --server 8125
```

we can then connect to our running Fandango "SMTP Server" and interact with it according to the `smtp-simple.fan` spec:

```shell
$ telnet localhost 8125
Trying ::1...
Connected to localhost.
Escape character is '^]'.
220 host.example.com 26%
QUIT
221 26yn
```

As server, Fandango produces its own `220` and `221` messages, effectively _fuzzing the client_.
Note how the interaction diagram reflects how Fandango is now taking the role of the client:

```{mermaid}
sequenceDiagram
    SMTP Client (or telnet)->>Fandango: (connect)
    Fandango->>SMTP Client (or telnet): 220 host.example.com <random data>
    SMTP Client (or telnet)->>Fandango: QUIT
    Fandango->>SMTP Client (or telnet): 221 <random data>
    Fandango->>SMTP Client (or telnet): (closes connection)
```

```{admonition} Under Construction
:class: attention
Fandango can actually create and mock an arbitrary number of clients and servers, all interacting with each other.
The interface for this is currently under construction.
```


## A Bigger Protocol Spec

So far, our SMTP server is not great at testing SMTP clients – all it can handle is a single `QUIT` command.
Let us extend it a bit with a few more commands, reflecting the interaction in the introduction:

```{code-cell}
:tags: ["remove-input"]
!cat smtp-extended.fan
```

This spec can actually handle the initial interaction (check it!).
You may note the following points:

First, the commands (and replies) follow a particular _order_, implying the _state_ the server and client are in.
In the "happy" path (assuming no errors), this is the order of possible commands:

% Can't have <...> here, as they'd render as HTML tags
```{mermaid}
stateDiagram
    [*] --> 1: ‹connect›
    1 --> 2: ‹helo›
    2 --> 3: ‹mail_from›
    3 --> 3: ‹mail_to›
    3 --> 4: ‹mail_to›
    4 --> 5: ‹data›
    5 --> [*]: ‹quit›
```

Note how the I/O grammar (and the above state diagram) accepts multiple `<mail_to>` interactions, allowing mails to be sent to multiple destinations.

Second, the spec actually accounts for errors, always entering an `<error>` state if the client command received cannot be parsed properly.
Hence, the state diagram induced in the above grammar actually looks like this:

% Can't have <...> here, as they'd render as HTML tags
```{mermaid}
stateDiagram
    [*] --> 1: ‹connect›
    1 --> 2: ‹helo›
    2 --> [*]: ‹error›
    2 --> 3: ‹mail_from›
    3 --> [*]: ‹error›
    3 --> 3: ‹mail_to›
    3 --> 4: ‹mail_to›
    4 --> 5: ‹data›
    4 --> [*]: ‹error›
    5 --> [*]: ‹quit›
    5 --> [*]: ‹error›
```

As described in the [chapter on checking outputs](sec:outputs), we can use the `fuzz` command to actually show generated outputs of individual parties:

```shell
$ fandango fuzz --party=Client -f smtp-extended.fan
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --party=Client -f smtp-extended.fan -n 1
assert _exit_code == 0 
```

```shell
$ fandango fuzz --party=Server -f smtp-extended.fan
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --party=Server -f smtp-extended.fan -n 1
assert _exit_code == 0 
```

That's it for now. GO and thoroughly test your programs!
