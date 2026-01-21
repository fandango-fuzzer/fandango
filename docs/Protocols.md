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

::::{grid}
:reverse:

:::{grid-item}
:columns: 12 5 5 5

```{image} FandangoIO.png
:width: 300px
:class: sd-m-auto
```

:::

:::{grid-item}
:columns: 12 7 7 7
:child-align: justify
:class: sd-fs-5

In [the chapter on checking outputs](sec:outputs), we already have seen how to interact with external programs.
In this chapter, we will extend this concept to full _protocol testing_ across networks.
::::

Fandango can test protocols.
In particular, it can

* act as a network _client_ and interact with network _servers_; and
* act as a network _server_ and interact with network _clients_.



## Interacting with an SMTP server

Let us start with a simple example.
The [Simple Mail Transfer Protocol](https://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol) (SMTP, [RFC 821](https://datatracker.ietf.org/doc/html/rfc821)) is a protocol through which mail clients can connect to a server to send mail to recipients.
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

Once installed, we can run the server locally.
Normally, it runs on port 8025:

```shell
$ python -m aiosmtpd -d -n &
```

```{code-cell}
:tags: ["remove-input"]
import os
import time

os.system("pkill -f aiosmtpd")
os.system("python -m aiosmtpd -n &")
time.sleep(1);  # Wait for server to be ready
```

% Check if everything works
```{code-cell}
:tags: ["remove-input", "remove-output"]
from minitelnet import telnet

commands = [
    "HELO relay.example.org\r\n",
    "QUIT\r\n"
]
telnet(commands)
```

We can now connect to the server on the given port and send it commands.
The `telnet` command is handy for this.
We give it a hostname (`localhost` for our local machine) and a port (8025 for our local SMTP server.)

Once connected, anything we type into the `telnet` input will automatically be relayed to the given port, and hence to the SMTP server.
For instance, entering a `QUIT` command (followed by Return) into telnet will be forwarded to the SMTP server, which will terminate the connection:

```shell
$ telnet localhost 8025
```

```{code-cell}
:tags: ["remove-input"]
from minitelnet import telnet

telnet(["QUIT\r\n"])
```

Try this for yourself!
What happens if you invoke `telnet`, introducing yourself with `HELO client.example.org`?

:::{admonition} Solution
:class: tip, dropdown
When sending `HELO client.example.org`, the server replies with its own hostname.
This is the name of the local computer, in our example `smtp.example.com`.

% Can't have code cells in admonitions :-(
```shell
$ telnet localhost 8025
Trying localhost...
Connected to localhost.
Escape character is '^]'.
220 smtp.example.com Python SMTP 1.4.6
HELO client.example.org
250 smtp.example.com
QUIT
221 Bye
Connection closed by foreign host.
```
:::


```{tip}
To interrupt a telnet session, type the escape character (`CTRL + ]`).
At the `telnet>` prompt, enter `help` for possible commands;
`quit` exits the telnet program.
```


## A simple SMTP grammar

```{margin}
We use `telnet` only for illustrative purposes here; later in this chapter, you will see how to have Fandango directly connect to servers (and clients!)
```

With [`fandango talk`](sec:outputs), we have seen a Fandango facility that allows us to connect to the standard input and output channels of a given program and interact with it.
The idea would now be to use the `telnet` program for this very purpose.
By invoking

```shell
$ fandango talk -f smtp-telnet.fan telnet localhost 8025
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
    SMTP Server (via telnet)->>Fandango: 220 smtp.example.com Python SMTP 1.4.6
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

```{margin}
The `-n 1` option limits fuzzing to one interaction.
Without `-n 1`, Fandango keeps on generating inputs until [grammar coverage](sec:diversity) is achieved.
```

```shell
$ fandango talk -f smtp-telnet.fan -n 1 telnet localhost 8025
```

```{code-cell}
:tags: ["remove-input"]
!fandango talk -f smtp-telnet.fan -n 1 telnet localhost 8025
assert _exit_code == 0
```

To track the data that is actually exchanged, use the verbose `-v` flag.
The `In:` and `Out:` log messages show the data that is being exchanged.

```shell
$ fandango -v talk -f smtp-telnet.fan -n 1 telnet localhost 8025
```

```{code-cell}
:tags: ["remove-input"]
!fandango -v talk -f smtp-telnet.fan -n 1 telnet localhost 8025
assert _exit_code == 0
```

```{versionchanged} 1.1
As of version 1.1, Fandango by default

* keeps on generating interactions until stopped (or limited by the `-n` option)
* aims for [grammar coverage](sec:diversity), thus covering states and message alternatives
```



## Interacting as Network Client

Using `telnet` to communicate with servers generally works, but it has a number of drawbacks.
Most importantly, `telnet` is meant for _human_ interaction.
Hence, our I/O grammars have to reflect the `telnet` output (which actually might change depending on operating system and configuration); also, `telnet` is not suited for transmitting binary data.

Fortunately, Fandango offers a means to be invoked _directly as a network client_, not requiring external programs such as `telnet`.
The `fandango talk` option `--client` allows Fandango to be used as a network client.
The argument to `--client` is a network address to connect to.
In the simplest form, it is just a port number on the local machine.
Hence, to have Fandango act as an SMTP client for the local server, we would use
the option `--client 8025`.

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
$ fandango talk -f smtp-simple.fan -n 1 --client 8025
```

```{code-cell}
:tags: ["remove-input"]
!fandango talk -f smtp-simple.fan -n 1 --client 8025
assert _exit_code == 0
```

```{mermaid}
sequenceDiagram
    Fandango->>SMTP Server: (connect)
    SMTP Server->>Fandango: 220 smtp.example.com <more data>
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

```{margin}
The option `-n 100` ensures the server will run for 100 interactions.
```

```shell
$ fandango talk -f smtp-simple.fan -n 100 --server 8125
```

```{code-cell}
:tags: ["remove-input"]

import os
import time

os.system("pkill -f smtp-simple.fan")
os.system("fandango talk -f smtp-simple.fan -n 100 --server 8125 &")
time.sleep(1);  # Wait for server to be ready
```

we can then connect to our running Fandango "SMTP Server" and interact with it according to the `smtp-simple.fan` spec:

```shell
$ telnet localhost 8125
```

```{code-cell}
:tags: ["remove-input"]
from minitelnet import telnet

telnet(["QUIT\r\n"], port=8125)
```

Note that as server, Fandango produces its own `220` and `221` messages, effectively _fuzzing the client_.
Note how the interaction diagram reflects how Fandango is now taking the role of the client:

```{mermaid}
sequenceDiagram
    SMTP Client (or telnet)->>Fandango: (connect)
    Fandango->>SMTP Client (or telnet): 220 smtp.example.com <random data>
    SMTP Client (or telnet)->>Fandango: QUIT
    Fandango->>SMTP Client (or telnet): 221 <random data>
    Fandango->>SMTP Client (or telnet): (closes connection)
```

(sec:smtp-extended)=
## A Bigger Protocol Spec

So far, our SMTP server is not great at testing SMTP clients – all it can handle is a single `QUIT` command.
Let us extend it a bit with a few more commands, reflecting the interaction in the introduction:

```{code-cell}
:tags: ["remove-input"]
!cat smtp-extended.fan
```

This spec can actually handle the initial interaction (check it!).


## From State Diagrams to Grammars

In the [extended SMTP spec](sec:smtp-extended), you may note that the interactions follow a particular _order_, implying the _state_ the server and client are in.
In the "happy" path (assuming no errors), the order of possible states and interactions can be visualized as a _state diagram_:

% Can't have <...> here, as they'd render as HTML tags
```{mermaid}
stateDiagram
    [*] --> #lt;connect#gt;
    #lt;connect#gt; --> #lt;helo#gt;: #lt;Server#colon;id#gt;
    #lt;helo#gt; --> #lt;mail_from#gt;: #lt;Client#colon;HELO#gt; #lt;Server#colon;hello#gt;
    #lt;mail_from#gt; --> #lt;mail_to#gt;: #lt;Client#colon;MAIL_FROM#gt; #lt;Server#colon;ok#gt;
    #lt;mail_to#gt; --> #lt;data#gt;: #lt;Client#colon;RCPT_TO#gt; #lt;Server#colon;ok#gt;
    #lt;mail_to#gt; --> #lt;mail_to#gt;: #lt;Client#colon;RCPT_TO#gt; #lt;Server#colon;ok#gt;
    #lt;data#gt; --> #lt;quit#gt;: #lt;Client#colon;DATA#gt; #lt;Server#colon;end_data#gt; #lt;Client#colon;message#gt;
    #lt;quit#gt; --> [*]: #lt;Client#colon;QUIT#gt; #lt;Server#colon;bye#gt;
```

In this state diagram,

* every _rounded rectangle_ stands for a _state_;
* _arrows_ denote possible _transitions_ between these states;
* _labels_ on the transitions denote the interactions that take place when transitioning from one state to another; and
* any _path_ through the state diagram indicates a valid sequence of states (and hence a valid sequence of interactions).

State diagrams often contain _loops_.
Both the SMTP grammar (and the above state diagram) accepts multiple `<mail_to>` interactions, allowing mails to be sent to multiple destinations.

Note how the set of paths through the state diagram corresponds to the possible sequence of productions in the SMTP specification.
Both the state diagram and the grammar effectively specify the same sequence of interactions; the grammar on top also specifies the syntax of individual messages.

```{note}
In Fandango, you can apply [constraints](sec:constraints) to all nonterminals, whether they stand for states, interactions, messages, or parts thereof.
```


### Converting State Diagrams to Grammars

Often, a protocol specification is already given in the form of such a state diagram, also known as a _labeled transition system_ (LTS) or as a  _finite state automaton_ (FSA).
You can convert these into Fandango grammars as follows:

1. Every _state_ $S$ in the diagram becomes a _nonterminal_ $S$ in the grammar.
2. Every _transition_ $A \rightarrow B$ in the diagram becomes an _expansion_ of $A$ into $B$, or $A ::= B$.
3. If there are multiple _alternatives_ outgoing from $A$, each of them becomes a separate alternative for the expansion of $A$.

Apply these rules are to the SMTP state diagram, and check how they correspond to the Fandango SMTP spec.


### Modeling Errors

Our SMTP spec above actually accounts for _errors_, always having the server enter an `<error>` state if the client command received cannot be parsed properly.
Hence, the state diagram induced by the above grammar actually looks like this:

% Can't have <...> here, as they'd render as HTML tags
```{mermaid}
stateDiagram
    [*] --> #lt;connect#gt;
    #lt;connect#gt; --> #lt;helo#gt;: #lt;Server#colon;id#gt;
    #lt;connect#gt; --> [*]: #lt;Server#colon;error#gt;
    #lt;helo#gt; --> #lt;mail_from#gt;: #lt;Client#colon;HELO#gt; #lt;Server#colon;hello#gt;
    #lt;mail_from#gt; --> #lt;mail_to#gt;: #lt;Client#colon;MAIL_FROM#gt; #lt;Server#colon;ok#gt;
    #lt;mail_from#gt; --> [*]: #lt;Server#colon;error#gt;
    #lt;mail_to#gt; --> #lt;data#gt;: #lt;Client#colon;RCPT_TO#gt; #lt;Server#colon;ok#gt;
    #lt;mail_to#gt; --> #lt;mail_to#gt;: #lt;Client#colon;RCPT_TO#gt; #lt;Server#colon;ok#gt;
    #lt;mail_to#gt; --> [*]: #lt;Server#colon;error#gt;
    #lt;data#gt; --> #lt;quit#gt;: #lt;Client#colon;DATA#gt; #lt;Server#colon;end_data#gt; #lt;Client#colon;message#gt;
    #lt;data#gt; --> [*]: #lt;Server#colon;error#gt;
    #lt;quit#gt; --> [*]: #lt;Client#colon;QUIT#gt; #lt;Server#colon;bye#gt;
```

Having such `<error>` transitions as part of the spec allows Fandango to also cover and trigger these.


## Extracting State Diagrams

You can use Fandango to _automatically extract state diagrams_ such as the above.
Such a visualization can be helpful for debugging.

* `fandango convert --to=mermaid` produces input for the [Mermaid](https://mermaid.ai/open-source/intro/) visualizer.
* `fandango convert --to=dot` produces an input in DOT format for the [Graphviz](https://graphviz.org) visualizer.
* `fandango convert --to=state` produces a generic textual representation.

This assumes the grammar actually embeds a state diagram - the last nonterminal in each expansion is supposed to be a new state, and the nonterminals next to last will become part of the transition.


### Visualizing State Diagrams with Mermaid

To produce the above state diagram for SMTP as an SVG file [smtp-mermaid.svg](smtp-mermaid.svg),
use the [Mermaid `mmdc` command-line interface](https://github.com/mermaid-js/mermaid-cli):

```shell
$ fandango convert --to=mermaid smtp-extended.fan | mmdc -i - -o smtp-mermaid.svg
```

This is the resulting SVG image:

```{image} smtp-mermaid.svg
```


### Visualizing State Diagrams with Graphviz (DOT)

To produce a similar SVG file [smtp-dot.svg](smtp-dot.svg) using Graphviz,
use the [`dot` command-line interface](https://graphviz.org/doc/info/command.html):

```{margin}
Besides `svg`, Graphviz supports [dozens of output formats](https://graphviz.org/docs/outputs/), including `jpg`, `png`, `pdf`, and many more.
```

```shell
$ fandango convert --to=dot smtp-extended.fan | dot -T svg -o smtp-dot.svg
```

This is the resulting SVG image:

```{image} smtp-dot.svg
```

Which one is nicer? Pick your favorite.


### Extracting State Diagrams as Plain Text

If you want to read or further process the diagram, a simple textual representation is available as well:

```shell
$ fandango convert --to=state smtp-extended.fan
```

```{code-cell}
:tags: ["remove-input"]
!fandango convert --to=state smtp-extended.fan
assert _exit_code == 0 
```


## Simulating Individual Parties

As described in the [chapter on checking outputs](sec:outputs), we can use the `fuzz` command to actually show generated outputs of individual parties:

```shell
$ fandango fuzz --party=Client -f smtp-extended.fan
```

% | tr -d '\015' removes CR characters, which are rendered as NL in jupyter book
```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --party=Client -f smtp-extended.fan -n 1 | tr -d '\015'
assert _exit_code == 0
```

```shell
$ fandango fuzz --party=Server -f smtp-extended.fan
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --party=Server -f smtp-extended.fan -n 1 | tr -d '\015'
assert _exit_code == 0 
```

That's it for now. GO and thoroughly test your programs!

% Let's kill our server(s)
```{code-cell}
:tags: ["remove-input"]
os.system("pkill -f aiosmtpd")
os.system("pkill -f smtp-simple.fan");
```
