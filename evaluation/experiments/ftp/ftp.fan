from random import randint

<start> ::= <state_setup>

<state_setup> ::= <exchange_socket_connect> <state_logged_out>
<state_logged_out> ::= <exchange_login>
<state_post_login> ::= <exchange_set_client><exchange_set_utf8><state_logged_in>
<state_logged_in> ::= ''

<exchange_socket_connect> ::= <ServerControl:ClientControl:response_server_info>
<response_server_info> ::= '220 ProFTPD Server (Debian) [1.2.3.4]\r\n'

<exchange_login> ::= <exchange_login_ok> | <exchange_login_fail>
<exchange_login_ok> ::= <ClientControl:ServerControl:request_login_user_ok><ServerControl:ClientControl:response_login_user><ClientControl:ServerControl:request_login_pass_ok><ServerControl:ClientControl:response_login_pass_ok><state_post_login>
<exchange_login_fail> ::= (<ClientControl:ServerControl:request_login_user_ok> | <ClientControl:ServerControl:request_login_user_fail>)<ServerControl:ClientControl:response_login_user><ClientControl:ServerControl:request_login_pass_fail><ServerControl:ClientControl:response_login_pass_fail><state_logged_out>

where forall <ex> in <exchange_login_ok>:
    str(<ex>.<request_login_user_ok>.<correct_username>) == str(<ex>.<response_login_user>.<user_name>)
where forall <ex> in <exchange_login_fail>:
    str(<ex>.<request_login_user_ok>.<correct_username>) == str(<ex>.<response_login_user>.<user_name>)
    or str(<ex>.<request_login_user_fail>.<wrong_user_name>) == str(<ex>.<response_login_user>.<user_name>)

<request_login_user_ok> ::= 'USER ' <correct_username> '\r\n'
<correct_username> ::= 'the_user'
<response_login_user> ::= '331 Password required for ' <user_name> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<response_login_pass_ok> ::= '230 User the_user logged in\r\n'

<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 Login incorrect.\r\n'

<exchange_set_client> ::= <ClientControl:ServerControl:request_set_client><ServerControl:ClientControl:response_set_client>
<request_set_client> ::= 'CLNT ' <client_name> '\r\n'
<response_set_client> ::= '200 OK\r\n'

<exchange_set_utf8> ::= <ClientControl:ServerControl:request_set_utf8><ServerControl:ClientControl:response_set_utf8>
<request_set_utf8> ::= 'OPTS UTF8 ON\r\n'
<response_set_utf8> ::= '200 UTF8 set to on\r\n'

<exchange_set_type> ::= <ClientControl:ServerControl:request_set_type><ServerControl:ClientControl:response_set_type>
<request_set_type> ::= 'TYPE I\r\n'
<response_set_type> ::= '200 Type set to I\r\n'

<exchange_set_passive> ::= <ClientControl:ServerControl:request_set_passive><ServerControl:ClientControl:response_set_passive>
<request_set_passive> ::= 'EPSV\r\n'
<response_set_passive> ::= '229 Entering Extended Passive Mode (|||' <open_port> '|)\r\n'

<exchange_mlsd> ::= <ClientControl:ServerControl:request_mlsd><ServerControl:ClientControl:open_mlsd><mlsd_transfer>
<request_mlsd> ::= 'MLSD\r\n'
<open_mlsd> ::= '150 Opening BINARY mode data connection for MLSD\r\n'
<mlsd_transfer> ::= (<ServerData:mlsd_data><mlsd_transfer>) | <ServerControl:ClientControl:finalize_mlsd>
<finalize_mlsd> ::= '226 Transfer complete\r\n'
<mlsd_data> ::= 'modify=' <modify_timestamp> ';perm=flcdmpe;type=' <mlsd_type> ';unique=2CUA;UNIX.group=33;UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=33;UNIX.ownername=the_user; <mlsd_folder>\r\n'


<modify_timestamp> ::= <year><month><day><hour><minute><second>
<year> ::= <number_tail>{4} := "{:04d}".format(randint(0, 9999))
<month> ::= <number_tail>{2} := "{:02d}".format(randint(1, 12))
<day> ::= <number_tail>{2} := "{:02d}".format(randint(1, 31))
<hour> ::= <number_tail>{2} := "{:02d}".format(randint(0, 23))
<minute> ::= <number_tail>{2} := "{:02d}".format(randint(0, 59))
<second> ::= <number_tail>{2} := "{:02d}".format(randint(0, 59))
<mlsd_type> ::= 'cdir' | 'pdir' | 'dir'

<mlsd_permission> ::= '0' <permission_byte>{3}
<permission_byte> ::= <number_tail> := randint(0, 7)
<mlsd_folder> ::= '.' | '..' | <filesystem_name>

<exchange_pwd> ::= <ClientControl:ServerControl:request_pwd><ServerControl:ClientControl:response_pwd>
<request_pwd> ::= 'PWD\r\n'
<response_pwd> ::= '257 \"' <directory> '\" is the current directory\r\n'
<directory> ::= '/' | ('/' <filesystem_name>)+
<file> ::= <filesystem_name> ('.' <filesystem_name>)?
<filesystem_name> ::= r'[a-zA-Z0-9]+'
<client_name> ::= r'[a-zA-Z0-9]+'

<user_name> ::= <wrong_user_name>
<wrong_user_name> ::= r'[a-zA-Z0-9\_]+'
<wrong_user_password> ::= r'[a-zA-Z0-9]*'

<open_port> ::= <passive_port> := open_data_agent(<open_port_param>)
<open_port_param> ::= <passive_port> := open_data_agent(<open_port>)
<passive_port> ::= <number> := randint(50000, 50100)

<exchange_feat> ::= <ClientControl:ServerControl:request_feat><ServerControl:ClientControl:response_feat>
<request_feat> ::= 'FEAT\r\n'
<response_feat> ::= r'[a-zA-Z0-9]+' (' ' r'[a-zA-Z0-9\*\.\;]+')* '\r\n'
<response_feat_end> ::= '211 End\r\n'










#<username> ::= <string>
#<password> ::= <string>
#<account-information> ::= <string>
#<string> ::= <char> | <char><string>
#<char> ::= '!' | '\"' | '#' | '$' | '%' | '&' | '\'' | '(' | ')' | '*' | '+' | ',' | '-' | '.' | '/' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | '[' | '\' | ']' | '^' | '_' | '`' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '{' | '|' | '}' | '~'
#<marker> ::= <pr-string>
#<pr-string> ::= <pr-char> | <pr-char><pr-string>
#<pr-char> ::= '!' | '\"' | '#' | '$' | '%' | '&' | '\'' | '(' | ')' | '*' | '+' | ',' | '-' | '.' | '/' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | '[' | '\' | ']' | '^' | '_' | '`' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '{' | '|' | '}' | '~'
#<byte-size> ::= <ftp_number>
#<host-port> ::= <host-number>,<port-number>
#<host-number> ::= <ftp_number>,<ftp_number>,<ftp_number>,<ftp_number>
#<port-number> ::= <ftp_number>,<ftp_number>
#<form-code> ::= N | T | C
#<type-code> ::= A [<sp> <form-code>] | E [<sp> <form-code>] | I | L <sp> <byte-size>
#<structure-code> ::= F | R | P
#<mode-code> ::= S | B | C
#<pathname> ::= <string>
#<decimal-integer> ::= any decimal integer


#<ftp_number> ::= <number> := randint(1, 255)
<number> ::= '0' | (<number_start> <number_tail>*)
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tail> ::= '0' | <number_start>


def open_data_port(port):
    FandangoIO.instance().roles['ClientData'].update_port(port)
    FandangoIO.instance().roles['ServerData'].update_port(port)

import socket
import threading

class ClientControl(FandangoAgent):
        def __init__(self):
            super().__init__(True)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("127.0.0.1", 21))
            server_thread = threading.Thread(target=self.listen_loop)
            server_thread.daemon = True
            server_thread.start()

        def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
            self.sock.sendall(message.encode("utf-8"))

        def listen_loop(self):
            while True:
                response, nothing = self.sock.recvfrom(1024)
                self.receive_msg("ServerControl", response.decode("utf-8"))

class ServerControl(FandangoAgent):
    def __init__(self):
        super().__init__(False)

class ClientData(FandangoAgent):
    def __init__(self):
        super().__init__(True)
        self.sock = None
        self.port = None
        self.listen_thread = None
        self.running = False

    def _create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect(("127.0.0.1", self.port))
        self.running = True
        self.listen_thread = threading.Thread(target=self._listen, daemon=True)
        self.listen_thread.start()

    def close(self):
        self.running = False
        if self.sock is None:
            return
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass  # socket might already be closed
        self.sock.close()

    def update_port(self, new_port: int):
        self.close()
        self.port = new_port
        self._create_socket()
        self.connect()

    def _listen(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data:
                    self.receive_msg("ServerControl", data)
                else:
                    self.running = False
                    break
            except Exception as e:
                self.running = False
                break

    def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
        with self.lock:
            try:
                if not self.running:
                    raise Exception("Socket not running!")
                self.sock.sendall(message)
            except Exception as e:
                print("Error sending message: " + str(e))


class ServerData(FandangoAgent):
    def __init__(self):
        super().__init__(False)
