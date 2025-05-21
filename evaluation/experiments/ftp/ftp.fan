from random import randint
import math

fandango_is_client = True

<start> ::= <state_setup>

<state_setup> ::= <exchange_socket_connect> <state_logged_out>
<state_logged_out> ::= (<exchange_auth_tls><state_logged_out>) | (<exchange_auth_ssl><state_logged_out>) | (<exchange_login>)
<state_logged_in> ::= (<exchange_mlsd><state_finished>) | (<logged_in_cmds><state_logged_in>)
<state_finished> ::= ''

<logged_in_cmds> ::= <exchange_set_type> | <exchange_pwd> | <exchange_syst> | <exchange_feat> | <exchange_set_client> | <exchange_set_utf8> | <exchange_set_type> | <exchange_set_epassive>
<exchange_socket_connect> ::= <ServerControl:ClientControl:response_server_info>
<response_server_info> ::= '220 ' r'[a-zA-Z0-9\_\.\(\) ]+\s' '[' r'[a-zA-Z0-9\:\.]+' ']\r\n'

<exchange_auth_tls> ::= <ClientControl:ServerControl:request_auth_tls><ServerControl:ClientControl:response_auth_tls>
<request_auth_tls> ::= 'AUTH TLS\r\n'
<response_auth_tls> ::= '500 ' <command_tail> '\r\n'

<exchange_auth_ssl> ::= <ClientControl:ServerControl:request_auth_ssl><ServerControl:ClientControl:response_auth_ssl>
<request_auth_ssl> ::= 'AUTH SSL\r\n'
<response_auth_ssl> ::= '500 ' <command_tail> '\r\n'

<exchange_login> ::= <exchange_login_fail> | <exchange_login_ok>
<exchange_login_ok> ::= <ClientControl:ServerControl:request_login_user_ok><ServerControl:ClientControl:response_login_user><ClientControl:ServerControl:request_login_pass_ok><ServerControl:ClientControl:response_login_pass_ok><state_logged_in>
<exchange_login_fail> ::= (<ClientControl:ServerControl:request_login_user_ok>
                            <ServerControl:ClientControl:response_login_user>
                            <ClientControl:ServerControl:request_login_pass_fail>
                          )
                               |
                          (<ClientControl:ServerControl:request_login_user_fail>
                            <ServerControl:ClientControl:response_login_user>
                            (<ClientControl:ServerControl:request_login_pass_fail>|<ClientControl:ServerControl:request_login_pass_ok>)
                          )
                           <ServerControl:ClientControl:response_login_pass_fail>
                           (<state_logged_out> | (<ServerControl:ClientControl:response_login_throttled><state_finished>))

where (not contains_nt(<start>, NonTerminal('<request_mlsd>')))
    or (contains_nt(<start>, NonTerminal('<request_set_epassive>')) and contains_nt(<start>, NonTerminal('<request_set_type>')))

def contains_nt(tree, nt):
    for msg in tree.find_role_msgs():
        if msg.msg.symbol == nt:
            return True
    return False

<request_login_user_ok> ::= 'USER the_user\r\n'
<response_login_user> ::= '331 ' <command_tail> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<response_login_pass_ok> ::= '230 ' <command_tail> '\r\n'
<command_tail> ::= r'([a-zA-Z0-9\_\. ]+)'

<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 ' <command_tail> '\r\n'
<response_login_throttled> ::= 'FTP session closed.\r\n'

<exchange_syst> ::= <ClientControl:ServerControl:request_syst><ServerControl:ClientControl:response_syst>
<request_syst> ::= 'SYST\r\n'
<response_syst> ::= '215 ' <syst_name> '\r\n'
<syst_name> ::= r'[a-zA-Z0-9\: ]+' := 'Linux'

<exchange_set_client> ::= <ClientControl:ServerControl:request_set_client><ServerControl:ClientControl:response_set_client>
<request_set_client> ::= 'CLNT ' <client_name> '\r\n'
<response_set_client> ::= '200 ' <command_tail> '\r\n'

<exchange_set_utf8> ::= <ClientControl:ServerControl:request_set_utf8><ServerControl:ClientControl:response_set_utf8>
<request_set_utf8> ::= 'OPTS UTF8 ON\r\n'
<response_set_utf8> ::= '200 ' <command_tail> '\r\n'

<exchange_feat> ::= <ClientControl:ServerControl:request_feat><ServerControl:ClientControl:response_feat>
<request_feat> ::= 'FEAT\r\n'
<response_feat> ::= '211-Features:\r\n' <feat_entry>+ '211 End\r\n' := feat_response()
<feat_entry> ::= ' ' r'[a-zA-Z0-9\*\;\-\. ]+' '\r\n'

def feat_response():
    features = '211-Features:\r\n CLNT\r\n EPRT\r\n EPSV\r\n HOST\r\n LANG en-US*\r\n MDTM\r\n MFF modify;UNIX.group;UNIX.mode;\r\n MFMT\r\n MLST modify*;perm*;size*;type*;unique*;UNIX.group*;UNIX.groupname*;UNIX.mode*;UNIX.owner*;UNIX.ownername*;\r\n211 End\r\n'
    return features

<exchange_set_type> ::= <ClientControl:ServerControl:request_set_type><ServerControl:ClientControl:response_set_type>
<request_set_type> ::= 'TYPE I\r\n'
<response_set_type> ::= '200 ' <command_tail> '\r\n'

<exchange_set_epassive> ::= <ClientControl:ServerControl:request_set_epassive><ServerControl:ClientControl:response_set_epassive>
<request_set_epassive> ::= 'EPSV\r\n'
<response_set_epassive> ::= '229 Entering Extended Passive Mode (|||' <open_port> '|)\r\n'

<exchange_mlsd> ::= <ClientControl:ServerControl:request_mlsd><ServerControl:ClientControl:open_mlsd><mlsd_transfer>
<request_mlsd> ::= 'MLSD\r\n'
<open_mlsd> ::= '150 Opening BINARY mode data connection for MLSD\r\n'
<mlsd_transfer> ::= <ServerData:ClientData:mlsd_data>+<ServerControl:ClientControl:finalize_mlsd>
<finalize_mlsd> ::= '226 Transfer complete\r\n'
<mlsd_data> ::= (<mlsd_data_folder> | <mlsd_data_file>)+
<mlsd_data_folder> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_folder> ';type=' <mlsd_type_folder> ';unique=' <mlsd_unique> ';UNIX.group=' <mlsd_data_user_uid> ';UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=' <mlsd_data_user_uid> ';UNIX.ownername=the_user; ' <mlsd_folder> '\r\n'
<mlsd_data_file> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_file> ';size=' <mlsd_size> ';type=' <mlsd_type_file> ';unique=' <mlsd_unique> ';UNIX.group=' <mlsd_data_user_uid> ';UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=' <mlsd_data_user_uid> ';UNIX.ownername=the_user; ' <mlsd_file> '\r\n'
<mlsd_data_user_uid> ::= <number>
<mlsd_unique> ::= r'[A-Z0-9]+'

where int(<mlsd_data_user_uid>.<number>) < 1000

where forall <data> in <mlsd_transfer>.<mlsd_data>:
    forall <mlsd_folder> in <data>..<mlsd_folder>:
        is_unique_folder_and_file(<mlsd_folder>, <data>)

where forall <data> in <mlsd_transfer>.<mlsd_data>:
    forall <mlsd_file> in <data>..<mlsd_file>:
        is_unique_folder_and_file(<mlsd_file>, <data>)

where forall <data> in <mlsd_transfer>.<mlsd_data>:
    exists <mlsd_folder> in <data>..<mlsd_folder>:
        str(<mlsd_folder>) == '.'

where forall <data> in <mlsd_transfer>.<mlsd_data>:
    exists <mlsd_folder> in <data>..<mlsd_folder>:
        str(<mlsd_folder>) == '..'

where forall <data_folder> in <mlsd_data_folder>:
    ((str(<data_folder>.<mlsd_folder>) != '.') or (str(<data_folder>.<mlsd_type_folder>) == 'cdir'))
    and ((str(<data_folder>.<mlsd_folder>) == '.') or (str(<data_folder>.<mlsd_type_folder>) != 'cdir'))

where forall <data_folder> in <mlsd_data_folder>:
    ((str(<data_folder>.<mlsd_folder>) != '..') or (str(<data_folder>.<mlsd_type_folder>) == 'pdir'))
    and ((str(<data_folder>.<mlsd_folder>) == '..') or (str(<data_folder>.<mlsd_type_folder>) != 'pdir'))

def is_unique_folder_and_file(current_file_or_folder, data):
    files_and_dirs = data.find_all_trees(NonTerminal('<mlsd_folder>'))
    files_and_dirs.extend(data.find_all_trees(NonTerminal('<mlsd_file>')))
    seen = False
    for entry in files_and_dirs:
        if str(entry) == str(current_file_or_folder):
            if seen:
                return False
            seen = True
    return True

<modify_timestamp> ::= <year><month><day><hour><minute><second>
<year> ::= <number_tail>{4} := "{:04d}".format(randint(0, 9999))
<month> ::= <number_tail>{2} := "{:02d}".format(randint(1, 12))
<day> ::= <number_tail>{2} := "{:02d}".format(randint(1, 28))
<hour> ::= <number_tail>{2} := "{:02d}".format(randint(0, 23))
<minute> ::= <number_tail>{2} := "{:02d}".format(randint(0, 59))
<second> ::= <number_tail>{2} := "{:02d}".format(randint(0, 59))
<mlsd_type_folder> ::= 'cdir' | 'pdir' | 'dir'
<mlsd_type_file> ::= 'file'
#<mlsd_unique> ::= '2BUA' | '2BUB' | '2BUC' | '2CUA' | '2CUB' | '2CUC' | '2CUD'
<mlsd_perm_folder> ::= 'flcdmpe' | 'fle'
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

<wrong_user_name> ::= r'^(?!the_user\r\n$)([a-zA-Z0-9_]+)'
<wrong_user_password> ::= r'^(?!the_password\r\n$)([a-zA-Z0-9_]+)'

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
import select

class ClientControl(FandangoAgent):
    def __init__(self):
        super().__init__(fandango_is_client)
        if not self.is_fandango():
            return
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect(("liggesmeyer.net", 21))
        server_thread = threading.Thread(target=self.listen_loop)
        server_thread.daemon = True
        server_thread.start()

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        self.sock.sendall(message.to_string().encode("utf-8"))

    def listen_loop(self):
        while True:
            readable, n, n2 = select.select([self.sock], [], [], 1.0)
            if readable:
                try:
                    response, n3 = self.sock.recvfrom(1024)
                    if not response:
                        self.receive_msg("ServerControl", "FTP session closed.\r\n")
                        self.sock.close()
                        break
                    self.receive_msg("ServerControl", response.decode("utf-8"))
                except ConnectionResetError:
                    break

class ServerControl(FandangoAgent):
    def __init__(self):
        super().__init__(not fandango_is_client)
        self.sock = None
        self.send_thread = None
        self.running = False
        if not self.is_fandango():
            return
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        try:
            if not self.running:
                raise Exception("Socket not running!")
            self.conn.send(message.to_string().encode("utf-8"))
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
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.sock.connect(("liggesmeyer.net", self.port))
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

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        try:
            if not self.running:
                raise Exception("Socket not running!")
            self.sock.sendall(message.to_string().encode("utf-8"))
        except Exception as e:
            print("Error sending message: " + str(e))


class ServerData(FandangoAgent):
    def __init__(self):
        super().__init__(not fandango_is_client)
        self.sock = None
        self.port = None
        self.conn = None
        self.address = None
        self.send_thread = None
        self.running = False
        self.lock = threading.Lock()

    def _create_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self.sock.bind(("::1", self.port))
        self.sock.listen(1)
        self.running = True
        self.send_thread = threading.Thread(target=self._listen, daemon=True)
        self.send_thread.start()

    def close(self):
        self.running = False
        if self.send_thread is not None:
            self.send_thread.join()
            self.send_thread = None
        if self.conn is not None:
            self.conn.shutdown(socket.SHUT_RDWR)
            self.conn = None
        if self.sock is None:
            return
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass  # socket might already be closed
        self.sock.close()

    def wait_accept(self):
        with self.lock:
            if self.conn is None:
                self.conn, self.address = self.sock.accept()

    def update_port(self, new_port: int):
        self.port = new_port
        if not self.is_fandango():
            return
        self.close()
        self._create_socket()
        self.connect()

    def _listen(self):
        self.wait_accept()
        while self.running:
            try:
                data = self.conn.recv(1024)
                if len(data) == 0:
                    continue
                if data:
                    self.receive_msg("ClientData", data.decode("utf-8"))
                else:
                    print("Listen, disable socket")
                    self.running = False
                    break
            except Exception as e:
                self.running = False
                break

    def on_send(self, message: DerivationTree, recipient: str, response_setter: Callable[[str, str], None]):
        if not self.running:
            raise Exception("Socket not running!")
        self.wait_accept()
        self.conn.send(message.to_string().encode("utf-8"))
        self.conn.shutdown(socket.SHUT_RDWR)
        self.conn = None