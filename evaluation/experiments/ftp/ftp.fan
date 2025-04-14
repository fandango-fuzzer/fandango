from random import randint
import math

fandango_is_client = True

<start> ::= <state_setup>

<state_setup> ::= <exchange_socket_connect> <exchange_auth_tls>? <exchange_auth_ssl>? <state_logged_out>
<state_logged_out> ::= <exchange_login>
<state_post_login> ::= <state_logged_in> #<exchange_syst>?<exchange_feat>?<exchange_set_client><exchange_set_utf8><exchange_set_type>
<state_logged_in> ::= (<exchange_set_type><state_bin_mode>) | (<any_state_cmds><state_logged_in>)
<state_bin_mode> ::= (<exchange_mlsd><state_finished>) | (<any_state_cmds><state_bin_mode>)
<state_finished> ::= ''

<any_state_cmds> ::= <exchange_pwd> | <exchange_syst> | <exchange_feat> | <exchange_set_client> | <exchange_set_utf8> | <exchange_set_type> | <exchange_set_epassive>
<exchange_socket_connect> ::= <ServerControl:ClientControl:response_server_info>
<response_server_info> ::= '220 ProFTPD Server (Debian) [1.2.3.4]\r\n'

<exchange_auth_tls> ::= <ClientControl:ServerControl:request_auth_tls><ServerControl:ClientControl:response_auth_tls>
<request_auth_tls> ::= 'AUTH TLS\r\n'
<response_auth_tls> ::= '500 AUTH not understood\r\n'

<exchange_auth_ssl> ::= <ClientControl:ServerControl:request_auth_ssl><ServerControl:ClientControl:response_auth_ssl>
<request_auth_ssl> ::= 'AUTH SSL\r\n'
<response_auth_ssl> ::= '500 AUTH not understood\r\n'

<exchange_login> ::= <exchange_login_ok> | <exchange_login_fail>
<exchange_login_ok> ::= <ClientControl:ServerControl:request_login_user_ok><ServerControl:ClientControl:response_login_user><ClientControl:ServerControl:request_login_pass_ok><ServerControl:ClientControl:response_login_pass_ok><state_post_login>
<exchange_login_fail> ::= (<ClientControl:ServerControl:request_login_user_ok> | <ClientControl:ServerControl:request_login_user_fail>)
                           <ServerControl:ClientControl:response_login_user><ClientControl:ServerControl:request_login_pass_fail>
                           <ServerControl:ClientControl:response_login_pass_fail>((<ServerControl:ClientControl:response_login_throttled><state_finished>)|<state_logged_out>)

where forall <ex> in <exchange_login_ok>:
    str(<ex>.<request_login_user_ok>.<correct_username>) == str(<ex>.<response_login_user>.<user_name>)
where forall <ex> in <exchange_login_fail>:
    str(<ex>.<request_login_user_ok>.<correct_username>) == str(<ex>.<response_login_user>.<user_name>)
where forall <ex> in <exchange_login_fail>:
    str(<ex>.<request_login_user_fail>.<wrong_user_name>) == str(<ex>.<response_login_user>.<user_name>)

<request_login_user_ok> ::= 'USER ' <correct_username> '\r\n'
<correct_username> ::= 'the_user'
<response_login_user> ::= '331 Password required for ' <user_name> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<response_login_pass_ok> ::= '230 User the_user logged in\r\n'

<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 Login incorrect.\r\n'
<response_login_throttled> ::= 'FTP session closed.\r\n'

<exchange_syst> ::= <ClientControl:ServerControl:request_syst><ServerControl:ClientControl:response_syst>
<request_syst> ::= 'SYST\r\n'
<response_syst> ::= '215 ' <syst_name> '\r\n'
<syst_name> ::= r'[a-zA-Z0-9\: ]+' := 'Linux'

<exchange_set_client> ::= <ClientControl:ServerControl:request_set_client><ServerControl:ClientControl:response_set_client>
<request_set_client> ::= 'CLNT ' <client_name> '\r\n'
<response_set_client> ::= '200 OK\r\n'

<exchange_set_utf8> ::= <ClientControl:ServerControl:request_set_utf8><ServerControl:ClientControl:response_set_utf8>
<request_set_utf8> ::= 'OPTS UTF8 ON\r\n'
<response_set_utf8> ::= '200 UTF8 set to on\r\n'

<exchange_feat> ::= <ClientControl:ServerControl:request_feat><ServerControl:ClientControl:response_feat>
<request_feat> ::= 'FEAT\r\n'
<response_feat> ::= '211-Features:\r\n' <feat_entry>+ '211 End\r\n' := feat_response()
<feat_entry> ::= ' ' r'[a-zA-Z0-9\*\;\-\. ]+' '\r\n'

def feat_response():
    features = '211-Features:\r\n CLNT\r\n EPRT\r\n EPSV\r\n HOST\r\n LANG en-US*\r\n MDTM\r\n MFF modify;UNIX.group;UNIX.mode;\r\n MFMT\r\n MLST modify*;perm*;size*;type*;unique*;UNIX.group*;UNIX.groupname*;UNIX.mode*;UNIX.owner*;UNIX.ownername*;\r\n211 End\r\n'
    return features

<exchange_set_type> ::= <ClientControl:ServerControl:request_set_type><ServerControl:ClientControl:response_set_type>
<request_set_type> ::= 'TYPE I\r\n'
<response_set_type> ::= '200 Type set to I\r\n'

<exchange_set_epassive> ::= <ClientControl:ServerControl:request_set_epassive><ServerControl:ClientControl:response_set_epassive>
<request_set_epassive> ::= 'EPSV\r\n'
<response_set_epassive> ::= '229 Entering Extended Passive Mode (|||' <open_port> '|)\r\n'

#<exchange_set_passive> ::= <ClientControl:ServerControl:request_set_passive><ServerControl:ClientControl:response_set_passive>
#<request_set_passive> ::= 'PASV\r\n'
#<response_set_passive> ::= '227 Entering Passive Mode (127,0,0,1,'<pasv_passive_port>')\r\n'
#<pasv_passive_port> ::= <number>','<number> := to_pasv_syntax(<open_port>)

def to_pasv_syntax(port_nr):
    port_nr = int(port_nr)
    upper_frac = math.floor(port_nr / 256)
    lower_frac = port_nr % 256
    return str(upper_frac) + ',' + str(lower_frac)

<exchange_mlsd> ::= <ClientControl:ServerControl:request_mlsd><ServerControl:ClientControl:open_mlsd><mlsd_transfer>
<request_mlsd> ::= 'MLSD\r\n'
<open_mlsd> ::= '150 Opening BINARY mode data connection for MLSD\r\n'
<mlsd_transfer> ::= <ServerData:ClientData:mlsd_data>*<ServerControl:ClientControl:finalize_mlsd>
<finalize_mlsd> ::= '226 Transfer complete\r\n'
<mlsd_data> ::= (<mlsd_data_folder> | <mlsd_data_file>)+
<mlsd_data_folder> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_folder> ';type=' <mlsd_type_folder> ';unique=' <mlsd_unique> ';UNIX.group=33;UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=33;UNIX.ownername=the_user; ' <mlsd_folder>'\r\n'
<mlsd_data_file> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_file> ';size=' <mlsd_size> ';type=' <mlsd_type_file> ';unique=' <mlsd_unique> ';UNIX.group=33;UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=33;UNIX.ownername=the_user; ' <mlsd_file>'\r\n'

<modify_timestamp> ::= <year><month><day><hour><minute><second>
<year> ::= <number_tail>{4} := "{:04d}".format(randint(0, 9999))
<month> ::= <number_tail>{2} := "{:02d}".format(randint(1, 12))
<day> ::= <number_tail>{2} := "{:02d}".format(randint(1, 31))
<hour> ::= <number_tail>{2} := "{:02d}".format(randint(0, 23))
<minute> ::= <number_tail>{2} := "{:02d}".format(randint(0, 59))
<second> ::= <number_tail>{2} := "{:02d}".format(randint(0, 59))
<mlsd_type_folder> ::= 'cdir' | 'pdir' | 'dir' | 'file'
<mlsd_type_file> ::= 'file'
<mlsd_unique> ::= '2BUA' | '2BUB' | '2BUC' | '2CUA' | '2CUB' | '2CUD'
<mlsd_perm_folder> ::= 'flcdmpe'
<mlsd_perm_file> ::= 'adfrw'
<mlsd_size> ::= <number>

<mlsd_permission> ::= '0' <permission_byte>{3}
<permission_byte> ::= <number_tail> := randint(0, 7)
<mlsd_folder> ::= '.' | '..' | <filesystem_name>
<mlsd_file> ::= <filesystem_name> ('.' r'[a-zA-Z0-9]+')?

<exchange_pwd> ::= <ClientControl:ServerControl:request_pwd><ServerControl:ClientControl:response_pwd>
<request_pwd> ::= 'PWD\r\n'
<response_pwd> ::= '257 \"' <directory> '\" is the current directory\r\n'
<directory> ::= '/' | ('/' <filesystem_name>)+
<file> ::= <filesystem_name> ('.' <filesystem_name>)?
<filesystem_name> ::= r'[a-zA-Z0-9]+'
<client_name> ::= r'[a-zA-Z0-9]+'

<user_name> ::= r'[a-zA-Z0-9\_]+'
<wrong_user_name> ::= r'^(?!the_user)([a-zA-Z0-9\_]+)'
<wrong_user_password> ::= r'^(?!the_password)([a-zA-Z0-9\_]*)'

<open_port> ::= <passive_port> := open_data_port(int(<open_port_param>))
<open_port_param> ::= <passive_port> := open_data_port(int(<open_port>))
<passive_port> ::= <number> := randint(50000, 50100)

<number> ::= '0' | (<number_start> <number_tail>*)
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tail> ::= '0' | <number_start>

def open_data_port(port):
    FandangoIO.instance().roles['ClientData'].update_port(port)
    FandangoIO.instance().roles['ServerData'].update_port(port)
    return port

import socket
import threading

class ClientControl(FandangoAgent):
    def __init__(self):
        super().__init__(fandango_is_client)
        if not self.is_fandango():
            return
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.connect(("::1", 21))
        server_thread = threading.Thread(target=self.listen_loop)
        server_thread.daemon = True
        server_thread.start()

    def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
        self.sock.sendall(message.encode("utf-8"))

    def listen_loop(self):
        while True:
            response, nothing = self.sock.recvfrom(1024)
            if len(response) == 0:
                self.receive_msg("ServerControl", "FTP session closed.\r\n")
                self.sock.close()
                break
            self.receive_msg("ServerControl", response.decode("utf-8"))

class ServerControl(FandangoAgent):
    def __init__(self):
        super().__init__(not fandango_is_client)
        self.sock = None
        self.send_thread = None
        self.running = False
        if not self.is_fandango():
            return
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.bind(("::1", 50200))
        self.sock.listen(1)
        self.conn, self.address = self.sock.accept()
        self.running = True
        self.send_thread = threading.Thread(target=self._listen, daemon=True)
        self.send_thread.start()

    def _listen(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if len(data) == 0:
                    continue
                if data:
                    self.receive_msg("ClientControl", data.decode("utf-8"))
                else:
                    self.running = False
                    break
            except Exception as e:
                self.running = False
                break

    def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
        try:
            if not self.running:
                raise Exception("Socket not running!")
            self.conn.send(message.encode("utf-8"))
        except Exception as e:
            print("Error sending message: " + str(e))

class ClientData(FandangoAgent):
    def __init__(self):
        super().__init__(fandango_is_client)
        self.sock = None
        self.port = None
        self.listen_thread = None
        self.running = False

    def _create_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect(("::1", self.port))
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
        self.port = new_port
        if not self.is_fandango():
            return
        self.close()
        self._create_socket()
        self.connect()

    def _listen(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if len(data) == 0:
                    continue
                if data:
                    self.receive_msg("ServerData", data.decode("utf-8"))
                else:
                    self.running = False
                    break
            except Exception as e:
                self.running = False
                break

    def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
        try:
            if not self.running:
                raise Exception("Socket not running!")
            self.sock.sendall(message)
        except Exception as e:
            print("Error sending message: " + str(e))


class ServerData(FandangoAgent):
    def __init__(self):
        super().__init__(not fandango_is_client)
        self.sock = None
        self.port = None
        self.send_thread = None
        self.running = False

    def _create_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    def connect(self):
        self.sock.bind(("::1", self.port))
        self.running = True
        self.send_thread = threading.Thread(target=self._listen, daemon=True)
        self.send_thread.start()

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
        self.port = new_port
        if not self.is_fandango():
            return
        self.close()
        self._create_socket()
        self.connect()

    def _listen(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if len(data) == 0:
                    continue
                if data:
                    self.receive_msg("ClientData", data.decode("utf-8"))
                else:
                    self.running = False
                    break
            except Exception as e:
                self.running = False
                break

    def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
        try:
            if not self.running:
                raise Exception("Socket not running!")
            self.sock.sendall(message)
        except Exception as e:
            print("Error sending message: " + str(e))