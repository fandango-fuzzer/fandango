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
Checking outputs is currently in beta.
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

With [`fandango talk`](sec:outputs), we have seen a Fandango facility that allows us to connect to the standard input and output channels of a given program and interact with it.
The idea would now be to use the `telnet` program for this very purpose.
By invoking

```shell
$ fandango talk -f smtp-telnet.fan telnet 8025
```

we could interact with the `telnet` program as described above.
All we now need is a grammar that describes the `telnet` interaction.
