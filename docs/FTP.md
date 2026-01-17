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

(sec:ftp)=
# Case Study: FTP

This FTP specification allows testing FTP clients and servers.
It demonstrates how additional channels (`ClientData` and `ServerData`) are created on demand, based on the ports returned by the FTP server.

```{versionadded} 1.1
These features are available in Fandango 1.1 and later.
```

## The FTP Parties

In contrast to other (simpler) protocols, FTP maintains _two_ communication channels: one for _control_ (issuing commands and getting responses), and one for _data_ (for transferring data).
In our spec, we name these `ClientControl` and `ClientData` as well as `ServerControl` and `ServerData`.

A very simple interaction involving all four, first logging in, and then sending a `LIST` command to get the contents of the current directory, is illustrated below.

```{mermaid}
sequenceDiagram
    box Client
    participant ClientData
    participant ClientControl
    end
    box Server
    participant ServerControl
    participant ServerData
    end
    ClientControl ->> ServerControl: (connect)
    ServerControl ->> ClientControl: 220 FTP Server ready.
    ClientControl ->> ServerControl: USER the_user
    ServerControl ->> ClientControl: 331 Password required for the_user.
    ClientControl ->> ServerControl: PASS the_password
    ServerControl ->> ClientControl: 230 User the_user logged in.
    ClientControl ->> ServerControl: LIST
    ServerControl ->> ClientControl: 150 Opening ASCII mode data connection for file list
    ServerData ->> ClientData: (data)
    ServerControl ->> ClientControl: 226 Transfer complete.
    ClientControl ->> ServerControl: (disconnect)
```

### Control Parties

In our setting, we assume that Fandango is acting as _client_ to test an FTP server.
Fandango connects to a server running on port 25521 on the local host.
Whenever it receives a `150` message initiating a data transfer, it starts the `ClientData` party.

```python
class ClientControl(NetworkParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY
            endpoint_type=EndpointType.CONNECT,
            uri="tcp://[::1]:25521"
        )
        self.start()

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        if message.decode("utf-8").startswith("150"):
            # FIXME: Make this ClientData.start()?
            FandangoIO.instance().parties["ClientData"].start()
```

When the server sends a `226` message, this indicates the end of a data transfer;
so we stop the `ServerData` instance to disconnect.

```python
class ServerControl(NetworkParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.EXTERNAL_PARTY
            endpoint_type=EndpointType.OPEN,
            uri="tcp://[::1]:25522"
        )
        self.start()

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ClientControl")

    def send(self, message: DerivationTree, recipient: str):
        super().send(message, recipient)
        if message.to_string().startswith("226"):
            FandangoIO.instance().parties['ServerData'].stop()
```


### Data Parties

In our setting, the FTP data transfer takes place via port 50100 on the local host.

```python
class ClientData(NetworkParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY
            endpoint_type=EndpointType.CONNECT,
            uri="tcp://[::1]:50100"
        )

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ServerData")
```

```python
class ServerData(NetworkParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.EXTERNAL_PARTY
            endpoint_type=EndpointType.OPEN,
            uri="tcp://[::1]:50100"
        )

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ClientData")
```




## Connecting to the FTP Server

The interaction with an FTP server starts with the server `ServerControl` sending a 220 message `<response_server_info>` to the client `ClientControl`, indicating that it is ready for a new user.
Afterwards, we are in the state `state_logged_out_1`.

```python
<start> ::= <state_setup>
<state_setup> ::= <service_ready> <state_logged_out_1>
<service_ready> ::= <ServerControl:ClientControl:response_server_info>
<response_server_info> ::= r'(220-(?:[\x20-\x7E]*\r\n))*220 (?:[\x20-\x7E]*)\r\n'
```

## Logging In

While we're logged out (in state `<state_logged_out_1>`), we can

* via username and password (`<exchange_login_...>`)

Login with username and password can

* fail (`<exchange_login_fail>`, after which we still stay logged out); or
* succeed (`<exchange_login_ok>`), then, we are logged in (`<state_logged_in>`).

We only support logging in via username and password, so authentication via

* TLS (`<exchange_auth_tls>`) or
* SSL (`<exchange_auth_ssl>`)

are never successful, we remain logged out.

```{mermaid}
stateDiagram
    [*] --> state_logged_out_1
    state_logged_out_1 --> state_logged_out_1: exchange_auth_tls | exchange_auth_ssl | exchange_login_fail
    state_logged_out_1 --> state_logged_in: exchange_login_ok
```

```python
<state_logged_out_1> ::= (
  <exchange_login_ok> <state_logged_in> |
  <exchange_login_fail> <state_logged_out_1>
  <exchange_auth_tls> <state_logged_out_1> |
  <exchange_auth_ssl> <state_logged_out_1> |
  )
```

### Logging in with username and password

Our FTP server assumes one user with username `the_user` and a password `the_password`.

```{mermaid}
sequenceDiagram
    ClientControl ->> ServerControl: (connect)
    ServerControl ->> ClientControl: 220 FTP Server ready.
    ClientControl ->> ServerControl: USER the_user
    ServerControl ->> ClientControl: 331 Password required for the_user.
    ClientControl ->> ServerControl: PASS the_password
    ServerControl ->> ClientControl: 230 User the_user logged in.
```

```python
<exchange_login_ok> ::= (
    <ClientControl:ServerControl:request_login_user_ok>
    <ServerControl:ClientControl:response_login_user>
    <ClientControl:ServerControl:request_login_pass_ok>
    <ServerControl:ClientControl:response_login_pass_ok>
)
```

```python
<request_login_user_ok> ::= 'USER the_user\r\n'
<response_login_user> ::= '331 ' <command_tail> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<response_login_pass_ok> ::= '230 ' <command_tail> '\r\n'
```

### Failure to log in

There are two ways logging in can go wrong - an incorrect password (not `the_password`):

```
<wrong_user_password> ::= r'^(?!the_password$)([a-zA-Z0-9_]+)'
```

and an incorrect username (not `the_user`):

```python
<wrong_user_name> ::= r'^(?!the_user$)([a-zA-Z0-9_]+)'
```

Let's discuss these two options:

```python
<exchange_login_fail> ::= <exchange_wrong_password> | <exchange_wrong_username>
```

First, we can have the client send a correct username, but a wrong password.

```python
<exchange_wrong_password> ::= (
  <ClientControl:ServerControl:request_login_user_ok>
  <ServerControl:ClientControl:response_login_user>
  <ClientControl:ServerControl:request_login_pass_fail>
  <ServerControl:ClientControl:response_login_pass_fail>)
```

```python
<request_login_user_ok> ::= 'USER the_user\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 ' <command_tail> '\r\n'
<command_tail> ::= r'[\x20-\x7E]+'
```

Second, we can have the client send an incorrect username (with a correct or incorrect password).

```python
<exchange_wrong_username> ::= (
   <ClientControl:ServerControl:request_login_user_fail>
   <ServerControl:ClientControl:response_login_user>
     (<ClientControl:ServerControl:request_login_pass_fail> |
      <ClientControl:ServerControl:request_login_pass_ok>)
   <ServerControl:ClientControl:response_login_pass_fail>
  )
```

```python
<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
```

In both cases, we end up staying logged out (`<state_logged_out_1>`).


### (Not) logging in via TLS and SSL

We do not support logging in via TLS and SSL and accept a 500 (syntax error) or 530 (not logged in) message from the server.

```python
<exchange_auth_tls> ::= <ClientControl:ServerControl:request_auth_tls><ServerControl:ClientControl:response_auth_tls>
<request_auth_tls> ::= 'AUTH TLS\r\n'
<response_auth_tls> ::= r'(530|500)' ' ' <command_tail> '\r\n'
```

```python
<exchange_auth_ssl> ::= <ClientControl:ServerControl:request_auth_ssl><ServerControl:ClientControl:response_auth_ssl>
<request_auth_ssl> ::= 'AUTH SSL\r\n'
<response_auth_ssl> ::= r'(530|500)' ' ' <command_tail> '\r\n'
```


## FTP Commands

When the client is logged in, it can send commands to the server.
In the `<state_logged_in>` state, we support the commands listed in `<logged_in_cmds>`.

The `<exchange_set_type>` and `<exchange_set_passive>` commands change the FTP state; see [States](sec:ftp-states) below.

```{mermaid}
stateDiagram
    [*] --> state_logged_out_1
    state_logged_out_1 --> state_logged_in: exchange_login_ok

    state_logged_in --> state_logged_in: logged_in_cmds
    state_logged_in --> state_in_binary: exchange_set_type
    state_logged_in --> state_in_passive: exchange_set_epassive
```

```
<state_logged_in> ::= <logged_in_cmds> <state_logged_in>
 | <exchange_set_type> <state_in_binary>
 | <exchange_set_epassive> <state_in_passive>
```

```python
<logged_in_cmds> ::= (
    <exchange_pwd> | 
    <exchange_syst> | 
    <exchange_feat> | 
    <exchange_set_utf8>)
```

### The PWD command

PWD requests the current working directory. The server answers with a (random) path.

```python
<exchange_pwd> ::= (
  <ClientControl:ServerControl:request_pwd>
  <ServerControl:ClientControl:response_pwd>
)
<request_pwd> ::= 'PWD\r\n'
<response_pwd> ::= '257 \"' <directory> '\" is the current directory\r\n'
<directory> ::= '/' | ('/' <filesystem_name>)+
<filesystem_name> ::= r'[a-zA-Z0-9_]+'
<client_name> ::= r'[a-zA-Z0-9]+'
```


### The SYST command

With the `SYST` command, we can request a `215` reply, followed by the server system name.
We use `Linux` as default.

```python
<exchange_syst> ::= (
  <ClientControl:ServerControl:request_syst>
  <ServerControl:ClientControl:response_syst>
)
<request_syst> ::= 'SYST\r\n'
<response_syst> ::= '215 ' <syst_name> '\r\n'
<syst_name> ::= r'[\x20-\x7E]+' := 'Linux'
```


### The FEAT command

The FEAT command returns a list of features that the server supports. If Fandango generates the feature list, we return a fixed value generated with the generator.
When receiving a feature list, we parse it according to the provided regex.

```python
<exchange_feat> ::= (
  <ClientControl:ServerControl:request_feat>
  <ServerControl:ClientControl:response_feat>
)
<request_feat> ::= 'FEAT\r\n'
<response_feat> ::= '211-Features:\r\n' <feat_entry>+ '211 End\r\n' := feat_response()
<feat_entry> ::= ' ' r'[\x20-\x7E]+' '\r\n'

def feat_response():
    features = '211-Features:\r\n EPSV\r\n211 End\r\n'
    return features
```


### The OPTS UTF8 command

We can send a command to set the character set to UTF-8, expecting a `200` (okay) response.

```python
<exchange_set_utf8> ::= (
   <ClientControl:ServerControl:request_set_utf8>
   <ServerControl:ClientControl:response_set_utf8>
)
<request_set_utf8> ::= 'OPTS UTF8 ON\r\n'
<response_set_utf8> ::= '200 ' <command_tail> '\r\n'
```

(sec:ftp-states)=
## More FTP States

```{mermaid}
stateDiagram
    [*] --> state_logged_out_1
    state_logged_out_1 --> state_logged_in: exchange_login_ok

    state_logged_in --> state_logged_in: logged_in_cmds
    state_logged_in --> state_in_binary: exchange_set_type
    state_logged_in --> state_in_passive: exchange_set_epassive

    state_in_binary --> state_in_binary: logged_in_cmds
    state_in_binary --> state_in_binary_passive: exchange_set_epassive

    state_in_passive --> state_in_passive: logged_in_cmds
    state_in_passive --> state_in_binary_passive: exchange_set_type

    state_in_binary_passive --> state_in_binary_passive: logged_in_cmds
    state_in_binary_passive --> state_in_binary: exchange_list
    state_in_binary_passive --> state_finished: exchange_quit

    state_finished --> [*]
```

```python
<state_in_binary> ::= (<logged_in_cmds><state_in_binary>) | (<exchange_set_epassive><state_in_binary_passive>)
<state_in_passive> ::= (<logged_in_cmds><state_in_passive>) | (<exchange_set_type> <state_in_binary_passive>)
<state_in_binary_passive> ::= (<logged_in_cmds><state_in_binary_passive>) | (<exchange_list><state_in_binary>) | (<exchange_quit><state_finished>)

```


## The LIST command

```{admonition} Under Construction
:class: attention
Extended documentation for this case study is under construction.
```


## The QUIT command

```python
<state_finished> ::= ''
```

```{admonition} Under Construction
:class: attention
Extended documentation for this case study is under construction.
```

% ```{code-cell}
% :tags: ["remove-input"]
% !cat ../evaluation/experiments/ftp/ftp.fan
% assert _exit_code == 0
