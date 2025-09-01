from random import randint
import math

fandango_is_client = True

# The starting symbol from which the fuzzer starts generating messages.
<start> ::= <state_setup>

# Setup stage that directs server to send a welcome message and leads over to the logged out state.
<state_setup> ::= <exchange_socket_connect> <state_logged_out>

# Logged out state. Client is not logged in yet. Client might ask for ssl or tls auth, which gets rejected by the server.
# Client is allowed to log in unencrypted.
<state_logged_out> ::= (<exchange_auth_tls><state_logged_out>) | (<exchange_auth_ssl><state_logged_out>) | (<exchange_login>)
<state_logged_in> ::= (<exchange_list><state_finished>) | (<logged_in_cmds><state_logged_in>)
<state_finished> ::= ''

# The logged in state. If the client is logged in, it is allowed to send the following commands.
<logged_in_cmds> ::= <exchange_set_type> | <exchange_pwd> | <exchange_syst> | <exchange_feat> | <exchange_set_utf8> | <exchange_set_type> | <exchange_set_epassive>
<exchange_socket_connect> ::= <ServerControl:ClientControl:response_server_info>
<response_server_info> ::= r'(220-(?:[\x20-\x7E]*\r\n))*220 (?:[\x20-\x7E]*)\r\n'

<exchange_auth_tls> ::= <ClientControl:ServerControl:request_auth_tls><ServerControl:ClientControl:response_auth_tls>
<request_auth_tls> ::= 'AUTH TLS\r\n'
<response_auth_tls> ::= '5' ('3'|'0') '0 ' <command_tail> '\r\n'

<exchange_auth_ssl> ::= <ClientControl:ServerControl:request_auth_ssl><ServerControl:ClientControl:response_auth_ssl>
<request_auth_ssl> ::= 'AUTH SSL\r\n'
<response_auth_ssl> ::= '5' ('3'|'0') '0 ' <command_tail> '\r\n'

# When client client logs in, he can either login with the correct or incorrect credentials.
<exchange_login> ::= <exchange_login_fail> | <exchange_login_ok>

# A successful login consist of the correct username and password and leads to the logged in state.
<exchange_login_ok> ::= <ClientControl:ServerControl:request_login_user_ok><ServerControl:ClientControl:response_login_user><ClientControl:ServerControl:request_login_pass_ok><ServerControl:ClientControl:response_login_pass_ok><state_logged_in>

# A failed login consist of incorrect username and incorrect password, incorrect username and correct
# password or correct username and incorrect password. The rule ends with the fuzzer going back into the logged out state.
<exchange_login_fail> ::= (<ClientControl:ServerControl:request_login_user_ok> \
                            <ServerControl:ClientControl:response_login_user> \
                            <ClientControl:ServerControl:request_login_pass_fail> \
                          ) \
                               | \
                          (<ClientControl:ServerControl:request_login_user_fail> \
                            <ServerControl:ClientControl:response_login_user> \
                            (<ClientControl:ServerControl:request_login_pass_fail>|<ClientControl:ServerControl:request_login_pass_ok>) \
                          ) \
                           <ServerControl:ClientControl:response_login_pass_fail> \
                           (<state_logged_out> | (<ServerControl:ClientControl:response_login_throttled><state_finished>))

# This constraint ensured, that the client sent the EPSV command (opening a passive port, for transmitting data),
# before executing the mlsd command.
where (not contains_nt(<start>, NonTerminal('<request_list>'))) \
    or (contains_nt(<start>, NonTerminal('<request_set_epassive>')) and contains_nt(<start>, NonTerminal('<request_set_type>')))

def contains_nt(tree, nt):
    for msg in tree.protocol_msgs():
        if msg.msg.symbol == nt:
            return True
    return False

<request_login_user_ok> ::= 'USER the_user\r\n'
<response_login_user> ::= '331 ' <command_tail> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<response_login_pass_ok> ::= '230 ' <command_tail> '\r\n'
<command_tail> ::= r'[\x20-\x7E]+'

<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 ' <command_tail> '\r\n'
<response_login_throttled> ::= 'FTP session closed.\r\n'

# SYST command expects 215 + the name of the system back.
<exchange_syst> ::= <ClientControl:ServerControl:request_syst><ServerControl:ClientControl:response_syst>
<request_syst> ::= 'SYST\r\n'
<response_syst> ::= '215 ' <syst_name> '\r\n'
<syst_name> ::= r'[\x20-\x7E]+' := 'Linux'

<exchange_set_utf8> ::= <ClientControl:ServerControl:request_set_utf8><ServerControl:ClientControl:response_set_utf8>
<request_set_utf8> ::= 'OPTS UTF8 ON\r\n'
<response_set_utf8> ::= '200 ' <command_tail> '\r\n'

# The FEAT command returns a list of features that the server supports. If Fandango generates the feature list,
# we return a fixed value generated with the generator.
# When receiving a feature list, we parse it according to the provided regex.
<exchange_feat> ::= <ClientControl:ServerControl:request_feat><ServerControl:ClientControl:response_feat>
<request_feat> ::= 'FEAT\r\n'
<response_feat> ::= '211-Features:\r\n' <feat_entry>+ '211 End\r\n' := feat_response()
<feat_entry> ::= ' ' r'[\x20-\x7E]+' '\r\n'

def feat_response():
    features = '211-Features:\r\n EPRT\r\n EPSV\r\n HOST\r\n LANG en-US*\r\n MDTM\r\n MFF modify;UNIX.group;UNIX.mode;\r\n MFMT\r\n MLST modify*;perm*;size*;type*;unique*;UNIX.group*;UNIX.groupname*;UNIX.mode*;UNIX.owner*;UNIX.ownername*;\r\n211 End\r\n'
    return features

<exchange_set_type> ::= <ClientControl:ServerControl:request_set_type><ServerControl:ClientControl:response_set_type>
<request_set_type> ::= 'TYPE I\r\n'
<response_set_type> ::= '200 ' <command_tail> '\r\n'

# EPSV directs the server to open a port for data transmission. The server returns the port number.
# While parsing that port number into <open_port>, we run a generator that reconfigures the data party to connect to that port.
# While generating that port server side, we use the same generator function to open the port server side.
<exchange_set_epassive> ::= <ClientControl:ServerControl:request_set_epassive><ServerControl:ClientControl:response_set_epassive>
<request_set_epassive> ::= 'EPSV\r\n'
<response_set_epassive> ::= '229 Entering Extended Passive Mode (|||' <open_port> '|)\r\n'

<exchange_list> ::= <ClientControl:ServerControl:request_list><ServerControl:ClientControl:open_list><list_transfer>
<request_list> ::= 'LIST\r\n'
<open_list> ::= '150 ' <command_tail> '\r\n'
<list_transfer> ::= <ServerData:ClientData:list_data><ServerControl:ClientControl:finalize_list>
<finalize_list> ::= '226 ' <command_tail> '\r\n'
<list_data> ::= (<list_data_file>)* # (<list_data_folder> | <list_data_file>)*
<list_data_file> ::= <permissions> ' ' <number> ' ' <user> ' ' <group> ' ' <number> ' ' <date> ' ' <filename> '\r\n'
<filename>    ::= r'[\x20-\x7E]+'

<permissions> ::= <file_type> <perm> <perm> <perm>
<file_type>   ::= '-' | 'd' | 'l' | 'c' | 'b'
<perm>        ::= ('r' | '-') ('w' | '-') ('x' | '-')
<user>        ::= r'[0-9a-zA-Z_\-]+'
<group>       ::= r'[0-9a-zA-Z_\-]+'
<date>        ::= <month> ' ' <day> ' ' (<time> | <year>)
<month>       ::= 'Jan' | 'Feb' | 'Mar' | 'Apr' | 'May' | 'Jun' | 'Jul' | 'Aug' | 'Sep' | 'Oct' | 'Nov' | 'Dec'
<day>         ::= <number_tail>{2} := "{:02d}".format(randint(1, 28))
<time>        ::= <hour> ':' <minute>
<hour> ::= <number_tail>{2} := "{:02d}".format(randint(0, 23))
<minute> ::= <number_tail>{2} := "{:02d}".format(randint(0, 59))
<year>        ::= <number_tail>{4} := "{:04d}".format(randint(0, 9999))



# MLSD requests the server to send a list of files and folders included in the current working directory.
# This list is transmitted though the data channel.
<exchange_mlsd> ::= <ClientControl:ServerControl:request_mlsd><ServerControl:ClientControl:open_mlsd><mlsd_transfer>
<request_mlsd> ::= 'MLSD\r\n'
<open_mlsd> ::= '150 Opening BINARY mode data connection for MLSD\r\n'
<mlsd_transfer> ::= <ServerData:ClientData:mlsd_data><ServerControl:ClientControl:finalize_mlsd>
<finalize_mlsd> ::= '226 Transfer complete\r\n'
<mlsd_data> ::= (<mlsd_data_folder> | <mlsd_data_file>)+
<mlsd_data_folder> ::= <mlsd_data_folder_cdir> | <mlsd_data_folder_pdir> | <mlsd_data_folder_dir>
<mlsd_data_folder_cdir> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_folder> ';type=cdir;unique=' <mlsd_unique> ';UNIX.group=' <mlsd_data_user_uid> ';UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=' <mlsd_data_user_uid> ';UNIX.ownername=the_user; .\r\n'
<mlsd_data_folder_pdir> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_folder> ';type=pdir;unique=' <mlsd_unique> ';UNIX.group=' <mlsd_data_user_uid> ';UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=' <mlsd_data_user_uid> ';UNIX.ownername=the_user; ..\r\n'
<mlsd_data_folder_dir> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_folder> ';type=dir;unique=' <mlsd_unique> ';UNIX.group=' <mlsd_data_user_uid> ';UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=' <mlsd_data_user_uid> ';UNIX.ownername=the_user; ' <filesystem_name> '\r\n'
<mlsd_data_file> ::= 'modify=' <modify_timestamp> ';perm=' <mlsd_perm_file> ';size=' <mlsd_size> ';type=' <mlsd_type_file> ';unique=' <mlsd_unique> ';UNIX.group=' <mlsd_data_user_uid> ';UNIX.groupname=www-data;UNIX.mode=' <mlsd_permission> ';UNIX.owner=' <mlsd_data_user_uid> ';UNIX.ownername=the_user; ' <mlsd_file> '\r\n'
<mlsd_data_user_uid> ::= <number>
<mlsd_unique> ::= r'[A-Z0-9]+'

where int(<mlsd_data_user_uid>.<number>) < 1000

where forall <data> in <mlsd_data>: \
    len(<data>.find_all_nodes(NonTerminal('<mlsd_data_folder_cdir>'), exclude_read_only=False)) == 1 \
    and len(<data>.find_all_nodes(NonTerminal('<mlsd_data_folder_pdir>'), exclude_read_only=False)) == 1


where forall <data> in <mlsd_transfer>.<mlsd_data>: \
    forall <mlsd_file> in <data>..<mlsd_file>: \
        is_unique_folder_and_file(<mlsd_file>, <data>)


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
<mlsd_folder> ::= <filesystem_name>
<mlsd_file> ::= <filesystem_name> ('.' r'[a-zA-Z0-9]+')?

# PWD requests the current working directory. The server answers with a (random) path.
<exchange_pwd> ::= <ClientControl:ServerControl:request_pwd><ServerControl:ClientControl:response_pwd>
<request_pwd> ::= 'PWD\r\n'
<response_pwd> ::= '257 \"' <directory> '\" is the current directory\r\n'
<directory> ::= '/' | ('/' <filesystem_name>)+
<file> ::= <filesystem_name> ('.' <filesystem_name>)?
<filesystem_name> ::= r'[a-zA-Z0-9_]+'
<client_name> ::= r'[a-zA-Z0-9]+'

<wrong_user_name> ::= r'^(?!the_user\r\n$)([a-zA-Z0-9_]+)'
<wrong_user_password> ::= r'^(?!the_password\r\n$)([a-zA-Z0-9_]+)'

<open_port> ::= <passive_port> := open_data_port(int(<open_port_param>))
<open_port_param> ::= <passive_port> := open_data_port(int(<open_port>))
<passive_port> ::= <number> := randint(50100, 50100)

<number> ::= '0' | (<number_start> <number_tail>*)
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tail> ::= '0' | <number_start>

# open_data_port(port) is a generator. When executed, it returns the value that was given to it and reconfigures the
# data party definitions to use that port.
def open_data_port(port):
    FandangoIO.instance().parties['ClientData'].port = port
    FandangoIO.instance().parties['ClientData'].start()
    FandangoIO.instance().parties['ServerData'].port = port
    FandangoIO.instance().parties['ServerData'].start()
    return port

class ClientControl(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY if fandango_is_client else Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT,
            uri="tcp://localhost:25521"
        )
        self.start()

    def receive_msg(self, sender: Optional[str], message: str | bytes) -> None:
        super().receive_msg("ServerControl", message.decode("utf-8"))

class ServerControl(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.EXTERNAL_PARTY if fandango_is_client else Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.OPEN,
            uri="tcp://localhost:25521"
        )
        self.start()

    def receive_msg(self, sender: Optional[str], message: str | bytes) -> None:
        self.receive_msg("ClientControl", message.decode("utf-8"))

    def on_send(self, message: DerivationTree, recipient: str):
        super().on_send(message, recipient)
        if message.to_string().startswith("226"):
            FandangoIO.instance().parties['ServerData'].stop()

class ClientData(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY if fandango_is_client else Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT,
            uri="tcp://localhost:50100"
        )

    def receive_msg(self, sender: Optional[str], message: str | bytes) -> None:
        self.receive_msg("ServerData", message.decode("utf-8"))

class ServerData(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.EXTERNAL_PARTY if fandango_is_client else Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.OPEN,
            uri="tcp://localhost:50100"
        )

    def receive_msg(self, sender: Optional[str], message: str | bytes) -> None:
        self.receive_msg("ClientData", message.decode("utf-8"))