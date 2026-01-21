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

This Fandango specification allows testing [FTP](https://datatracker.ietf.org/doc/html/rfc959) (RFC 959, File Transfer Protocol) clients and servers.
It demonstrates

* how a nontrivial protocol with text commands is implemented; and
* how additional channels (`ClientData` and `ServerData`) are used on demand, based on the ports returned by the FTP server

The [`ftp.fan`](ftp.fan) Fandango FTP spec is available for download.
To test it, run an FTP server on the local host at port 50100, and invoke Fandango as

```{margin}
Omit `-n 1` if you want Fandango to test until protocol coverage is achieved.
```

```shell
$ fandango talk -n 1 -f ftp.fan
```

```{versionadded} 1.1
These features are available in Fandango 1.1 and later.
```

(sec:ftp-parties)=
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
Here, we use the [`instance()`](sec:party-instance) method to access and reconfigure the individual parties.


```python
class ClientControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://[::1]:25521"
        )
        self.start()

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        if message.decode("utf-8").startswith("150"):
            ClientData.instance().start()
```

When the server sends a `226` message, this indicates the end of a data transfer;
so we stop the `ServerData` instance to disconnect.

```python
class ServerControl(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://[::1]:25522"
        )
        self.start()

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ClientControl")

    def send(self, message: DerivationTree, recipient: str):
        super().send(message, recipient)
        if message.to_string().startswith("226"):
            ServerData.instance().stop()
```


### Data Parties

In our setting, the FTP data transfer takes place via port 50100 on the local host.

```python
class ClientData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="tcp://[::1]:50100"
        )

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ServerData")
```

```python
class ServerData(NetworkParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="tcp://[::1]:50100"
        )

    def receive(self, message: str | bytes, sender: Optional[str]) -> None:
        super().receive(message.decode("utf-8"), sender="ClientData")
```



(sec:ftp-connect)=
## Connecting to the FTP Server

The interaction with an FTP server starts with the server `ServerControl` sending a 220 message `<response_server_info>` to the client `ClientControl`, indicating that it is ready for a new user.
Afterwards, we are in the state `state_logged_out_1`.

```python
<start> ::= <state_setup>
<state_setup> ::= <service_ready> <state_logged_out_1>
<service_ready> ::= <ServerControl:ClientControl:response_server_info>
<response_server_info> ::= r'(220-(?:[\x20-\x7E]*\r\n))*220 (?:[\x20-\x7E]*)\r\n'
```

(sec:ftp-login)=
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
    [*] --> #lt;state_logged_out_1#gt;
    #lt;state_logged_out_1#gt; --> state_logged_out_1#gt;: #lt;exchange_auth_tls#gt; | #lt;exchange_auth_ssl#gt; | #lt;exchange_login_fail#gt;
    #lt;state_logged_out_1#gt; --> #lt;state_logged_in#gt;: #lt;exchange_login_ok
```

In our spec, this is modeled as exchanges followed by the resulting state.

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


## First FTP Commands

When the client is logged in, it can send commands to the server.
In the `<state_logged_in>` state, we support the commands listed in `<logged_in_cmds>`.

(The [`<exchange_set_type>`](sec:ftp-type) and [`<exchange_set_passive>`](sec:ftp-epsv) commands change the FTP state; see [States](sec:ftp-states) below.)

```{mermaid}
stateDiagram
    [*] --> #lt;state_logged_out_1#gt;
    #lt;state_logged_out_1#gt; --> #lt;state_logged_in#gt;: #lt;exchange_login_ok#gt;

    #lt;state_logged_in#gt; --> #lt;state_logged_in#gt;: #lt;logged_in_cmds#gt;
    #lt;state_logged_in#gt; --> #lt;state_in_binary#gt;: #lt;exchange_set_type#gt;
    #lt;state_logged_in#gt; --> #lt;state_in_passive#gt;: #lt;exchange_set_epassive#gt;
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

(sec:ftp-pwd)=
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

(sec:ftp-syst)=
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

(sec:ftp-feat)=
### The FEAT command

The FEAT command returns a list of features that the server supports.
If Fandango generates the feature list, we return a fixed value - in our model, we only support the [`EPSV`](sec:ftp-epsv) command.
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

(sec:ftp-opts)=
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
## Changing FTP States

Let us now explore more states.
In our model, the FTP server can be in four states:

1. `<state_logged_in>` - the default state
2. `<state_in_binary>` - binary mode
3. `<state_in_passive>` - passive mode
4. `<state_in_binary_passive>` - binary _and_ passive mode

Binary and passive modes are activated via [`<exchange_set_type>`](sec:ftp-type) and [`<exchange_set_epassive>`](sec:ftp-epsv) interactions, as shown below.
We want to be in binary _and_ passive mode, so we can actually retrieve data using `LIST` ([`<exchange_list>`](sec:ftp-list)) and finally quit ([`exchange_quit`](sec:ftp-quit)).

```{mermaid}
stateDiagram
    [*] --> #lt;state_logged_out_1#gt;
    #lt;state_logged_out_1#gt; --> #lt;state_logged_in#gt;: #lt;exchange_login_ok#gt;
    #lt;state_logged_in#gt; --> #lt;state_logged_in#gt;: #lt;logged_in_cmds#gt;
    #lt;state_logged_in#gt; --> #lt;state_in_binary#gt;: #lt;exchange_set_type#gt;
    #lt;state_logged_in#gt; --> #lt;state_in_passive#gt;: #lt;exchange_set_epassive#gt;
    #lt;state_in_passive#gt; --> #lt;state_in_passive#gt;: #lt;logged_in_cmds#gt;
    #lt;state_in_passive#gt; --> #lt;state_in_binary_passive#gt;: #lt;exchange_set_type#gt;
    #lt;state_in_binary_passive#gt; --> #lt;state_in_binary_passive#gt;: #lt;logged_in_cmds#gt;
    #lt;state_in_binary_passive#gt; --> #lt;state_in_binary#gt;: #lt;exchange_list#gt;
    #lt;state_in_binary_passive#gt; --> #lt;state_finished#gt;: #lt;exchange_quit#gt;
    #lt;state_in_binary#gt; --> #lt;state_in_binary#gt;: #lt;logged_in_cmds#gt;
    #lt;state_in_binary#gt; --> #lt;state_in_binary_passive#gt;: #lt;exchange_set_epassive#gt;
    #lt;state_finished#gt; --> [*]
```

```python
<state_in_binary> ::= (
  <logged_in_cmds> <state_in_binary> |
  <exchange_set_epassive> <state_in_binary_passive>
)
<state_in_passive> ::= (
  <logged_in_cmds> <state_in_passive> |
  <exchange_set_type> <state_in_binary_passive>
)
<state_in_binary_passive> ::= (
  <logged_in_cmds> <state_in_binary_passive> |
  <exchange_list> <state_in_binary> |
  <exchange_quit> <state_finished>
)
```

(sec:ftp-epsv)=
### The EPSV command - entering passive mode

```{margin}
By default, FTP uses "active" mode, in which the FTP server accesses a port on the client machine.
Since most firewalls block such behavior, "passive" mode is now the typical use.
```

The `EPSV` command directs the server to open a port for data transmission.
With this, we prepare client and server for actual data transfer.
The server returns the port number by which it can be accessed; we have to get and process it.

```python
<exchange_set_epassive> ::= \
  <ClientControl:ServerControl:request_set_epassive> \
  <ServerControl:ClientControl:response_set_epassive>

<request_set_epassive> ::= 'EPSV\r\n'
<response_set_epassive> ::= '229 Entering Extended Passive Mode (|||' <open_port> '|)\r\n'
```

When producing or parsing `<open_port>`, we call the `open_data_port()` generator function to reconfigure the data parties.
This method gets called both when parsing and producing:

* When _producing_, Fandango produces a parameter `<open_port_param>`.
  `<open_port_param>` consists of `<passive_port>` and another generator that depends on `<open_port>`.
  This generator does not get executed when generating parameters for the generator from `<open_port>`, such that we do not get caught in an infinite loop between those to generators.
  Instead, we generate `<passive_port>` directly without invoking the generator.
* When _parsing_ `<open_port>`, Fandango derives the argument `<open_port_param>` used in the generator by executing the generator from `<open_port_param>` which depends on `<open_port>`

```python
<open_port> ::= <passive_port> := open_data_port(int(<open_port_param>))
<open_port_param> ::= <passive_port> := open_data_port(int(<open_port>))
```

When generating a passive port, we use a generator to randomly generate a port in [50100, 50100]

```
<passive_port> ::= r'[1-9][0-9]{0,4}' := randint(50100, 50100)
```

The function `open_data_port(port)` is a generator.
When executed, it returns the value that was given to it and reconfigures the
data party definitions to use that port.
Again, we use the [`instance()`](sec:party-instance) method to access and reconfigure the individual parties.

```{margin}
As we may use the spec file to run with `fandango fuzz` as server or client, we protect against the fact that the `ClientData` or `ServerData` instances may not have been created.
```

```python
def open_data_port(port):
    try:
        client_data = ClientData.instance()
        server_data = ServerData.instance()
    except KeyError:
        # Party instances not created
        return port

    if client_data.port != port:
        client_data.stop()
        client_data.port = port
    if  server_data.port != port:
        server_data.stop()
        server_data.port = port
    client_data.start()
    server_data.start()
    return port
```

(sec:ftp-type)=
### The TYPE command - set binary mode

Using the FTP `TYPE` command, we can set the server into binary mode.

```python
<exchange_set_type> ::= (
  <ClientControl:ServerControl:request_set_type>
  <ServerControl:ClientControl:response_set_type>
)
<request_set_type> ::= 'TYPE I\r\n'
<response_set_type> ::= '200 ' <command_tail> '\r\n'
```


(sec:ftp-list)=
### The LIST command

Finally, after all these preparations, we can actually retrieve data via FTP.
The FTP `LIST` command makes the FTP server send the contents of the current directory.

```python
<exchange_list> ::= (
  <ClientControl:ServerControl:request_list>
  <ServerControl:ClientControl:open_list>
  <list_transfer>
)
<request_list> ::= 'LIST\r\n'
<open_list> ::= '150 ' <command_tail> '\r\n'
```

`<list_data>` gets sent using the data channel.
Therefore, we use `ServerData` and `ClientData` as sending and receiving parties.

```python
<list_transfer> ::= <ServerData:ClientData:list_data>?<ServerControl:ClientControl:finalize_list>
<finalize_list> ::= '226 ' <command_tail> '\r\n'
```

The list data itself contains file names, user names, permissions, and dates:

```python
<list_data> ::= (<list_data_file>)+
<list_data_file> ::= <permissions> ' '+ <link_count> ' ' <user> ' '+ <group> ' '+ <file_size> ' ' <date> ' ' <filename> '\r\n'
<filename>    ::= r'[\x20-\x7E]+'
<number>      ::= r'[0-9]+' := str(randint(1, 1000))
<file_size>   ::= <number> := str(randint(0, 9999999))
<link_count>  ::= <number>

<permissions> ::= <file_type> <perm> <perm> <perm>
<file_type>   ::= r'[-dlcb]'
<perm>        ::= r'[r-]' r'[w-]' r'[x-]'
<user>        ::= r'[0-9a-zA-Z_\-]+'
<group>       ::= r'[0-9a-zA-Z_\-]+'
<date>        ::= <month> ' ' <day> ' ' <time>
<month>       ::= r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
<day>         ::= r'[0-9]{2}' := "{:02d}".format(randint(1, 28))
<time>        ::= <hour> ':' <minute>
<hour>        ::= r'[0-9]{2}' := "{:02d}".format(randint(0, 23))
<minute>      ::= r'[0-9]{2}' := "{:02d}".format(randint(0, 59))
```

This is what a typical generated entry looks like:

```shell
$ fandango fuzz -f ftp.fan --start-symbol '<list_data>' --party ServerData -n 1
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f ftp.fan --start-symbol '<list_data>' --party ServerData -n 1
```


(sec:ftp-quit)=
### The QUIT command

After a number of `LIST` commands, it is time to quit.
We use the FTP `QUIT` command for this purpose.

```python
<exchange_quit> ::= (
  <ClientControl:ServerControl:request_quit>
  <ServerControl:ClientControl:response_quit>
)
<request_quit> ::= 'QUIT\r\n'
<response_quit> ::= '221 ' <command_tail> '\r\n'
```

After that, the FTP server enters `<state_finished>`.
There is no other interaction or state following, so we're done.

```python
<state_finished> ::= ''
```


## Example Interactions

We can use `fandango fuzz` in conjunction with the `--party` option to simulate the messages produced by a single party.

### A Typical Client Interaction

Here is a valid sequence of commands as issued by a client:

```shell
$ fandango fuzz -f ftp.fan --party ClientControl -n 1
```

% | tr -d '\015' removes CR characters, which are rendered as NL in jupyter book
```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f ftp.fan --party ClientControl -n 1 | tr -d '\015'
```

### A Typical Server Interaction

Here is a valid sequence of responses as issued by a server:

```shell
$ fandango fuzz -f ftp.fan --party ServerControl -n 1
```

% | tr -d '\015' removes CR characters, which are rendered as NL in jupyter book
```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f ftp.fan --party ServerControl -n 1 | tr -d '\015'
```

Now go and try things out for yourself!

% ```{code-cell}
% :tags: ["remove-input"]
% !cat ../evaluation/experiments/ftp/ftp.fan
% assert _exit_code == 0
