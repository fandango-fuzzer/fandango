from random import randint
import math

fandango_is_client = False

# The starting symbol from which the fuzzer starts generating messages.
<start> ::= <state_setup>

# Setup stage that directs server to send a welcome message and leads over to the logged out state.
<state_setup> ::= <service_ready> <state_logged_out_1>

# Logged out state. Client is not logged in yet. Client might ask for ssl or tls auth, which gets rejected by the server.
# Client is allowed to log in unencrypted.
# Note the commented-out nonterminals below. When enabled they limit the number of login failures to 2 before a successful login is required. This is required, since our testing target (vsftpd) disconnects the client after 3 failed login attempts.
# We commented-out those states, since we used a k-path "k" that is small enough to not trigger that behaviour on purpose. Instead the limit_errors-constraint below ensures that we do not generate too many failing auth requests in a row.
<state_logged_out_1> ::= (<exchange_auth_tls><state_logged_out_1>) | (<exchange_auth_ssl><state_logged_out_1>) | (<exchange_login_fail><state_logged_out_1>) | (<exchange_login_ok><state_logged_in>)
#<state_logged_out_1> ::= (<exchange_auth_tls><state_logged_out_1>) | (<exchange_auth_ssl><state_logged_out_1>) | (<exchange_login_fail><state_logged_out_2>) | (<exchange_login_ok><state_logged_in>)
#<state_logged_out_2> ::= (<exchange_auth_tls><state_logged_out_2>) | (<exchange_auth_ssl><state_logged_out_2>) | (<exchange_login_fail><state_logged_out_3>) | (<exchange_login_ok><state_logged_in>)
#<state_logged_out_3> ::= (<exchange_auth_tls><state_logged_out_3>) | (<exchange_auth_ssl><state_logged_out_3>) | (<exchange_login_ok><state_logged_in>)

where limit_failed_logins(<start>, NonTerminal('<exchange_login_fail>'))
where limit_errors(<start>)

def less_than(tree, symbol_to_find, number):
    count = len(tree.find_all_trees(symbol_to_find))
    return count < number

def limit_failed_logins(tree, symbol_to_find):
    return less_than(tree, symbol_to_find, 3)

# Limits number of errors to 10. Our testing target (vsftpd) disconnects the client at 10 failed attempts in a row.
def limit_errors(tree):
    nts = [NonTerminal('<request_auth_ssl>'), NonTerminal('<response_auth_ssl>'), NonTerminal('<request_auth_tls>'), NonTerminal('<response_auth_tls>')]
    count = 0
    for msg in tree.protocol_msgs()[::-1]:
        if msg.msg.symbol not in nts:
            return True
        count += 1
        if count > 10:
            return False

<state_logged_in> ::= (<logged_in_cmds><state_logged_in>) | (<exchange_set_type><state_in_binary>) | (<exchange_set_epassive><state_in_passive>)
<state_in_binary> ::= (<logged_in_cmds><state_in_binary>) | (<exchange_set_epassive><state_in_binary_passive>)
<state_in_passive> ::= (<logged_in_cmds><state_in_passive>) | (<exchange_set_type> <state_in_binary_passive>)
<state_in_binary_passive> ::= (<logged_in_cmds><state_in_binary_passive>) | (<exchange_list><state_in_binary>) | (<exchange_quit><state_finished>)

<state_finished> ::= ''

# The logged in state. If the client is logged in, it is allowed to send the following commands.
<logged_in_cmds> ::= <exchange_pwd> | <exchange_syst> | <exchange_feat> | <exchange_set_utf8>
<service_ready> ::= <ServerControl:ClientControl:response_server_info>
<response_server_info> ::= r'(220-(?:[\x20-\x7E]*\r\n))*220 (?:[\x20-\x7E]*)\r\n'

<exchange_quit> ::= <ClientControl:ServerControl:request_quit><ServerControl:ClientControl:response_quit>
<request_quit> ::= 'QUIT\r\n'
<response_quit> ::= '221 ' <command_tail> '\r\n'

<exchange_auth_tls> ::= <ClientControl:ServerControl:request_auth_tls><ServerControl:ClientControl:response_auth_tls>
<request_auth_tls> ::= 'AUTH TLS\r\n'
<response_auth_tls> ::= r'(530|500)' ' ' <command_tail> '\r\n'

<exchange_auth_ssl> ::= <ClientControl:ServerControl:request_auth_ssl><ServerControl:ClientControl:response_auth_ssl>
<request_auth_ssl> ::= 'AUTH SSL\r\n'
<response_auth_ssl> ::= r'(530|500)' ' ' <command_tail> '\r\n'

# A successful login consist of the correct username and password and leads to the logged in state.
<exchange_login_ok> ::= <ClientControl:ServerControl:request_login_user_ok><ServerControl:ClientControl:response_login_user><ClientControl:ServerControl:request_login_pass_ok><ServerControl:ClientControl:response_login_pass_ok>

# A failed login consist of incorrect username and incorrect password, incorrect username and correct
# password or correct username and incorrect password. The rule ends with the fuzzer going back into the logged out state.
<exchange_login_fail> ::= ((<ClientControl:ServerControl:request_login_user_ok> \
                            <ServerControl:ClientControl:response_login_user> \
                            <ClientControl:ServerControl:request_login_pass_fail> \
                          ) \
                               | \
                          (<ClientControl:ServerControl:request_login_user_fail> \
                            <ServerControl:ClientControl:response_login_user> \
                            (<ClientControl:ServerControl:request_login_pass_fail>|<ClientControl:ServerControl:request_login_pass_ok>) \
                          )) \
                           <ServerControl:ClientControl:response_login_pass_fail>

<request_login_user_ok> ::= 'USER the_user\r\n'
<response_login_user> ::= '331 ' <command_tail> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<response_login_pass_ok> ::= '230 ' <command_tail> '\r\n'
<command_tail> ::= r'[\x20-\x7E]+'

<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 ' <command_tail> '\r\n'

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
    features = '211-Features:\r\n EPSV\r\n211 End\r\n'
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
# <list_data> gets sent using the data-channel. Therefore, we use ServerData and ClientData as sending and receiving parties.
<list_transfer> ::= <ServerData:ClientData:list_data>?<ServerControl:ClientControl:finalize_list>
<finalize_list> ::= '226 ' <command_tail> '\r\n'
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


# PWD requests the current working directory. The server answers with a (random) path.
<exchange_pwd> ::= <ClientControl:ServerControl:request_pwd><ServerControl:ClientControl:response_pwd>
<request_pwd> ::= 'PWD\r\n'
<response_pwd> ::= '257 \"' <directory> '\" is the current directory\r\n'
<directory> ::= '/' | ('/' <filesystem_name>)+
<filesystem_name> ::= r'[a-zA-Z0-9_]+'
# <client_name> ::= r'[a-zA-Z0-9]+'

<wrong_user_name> ::= r'^(?!the_user$)([a-zA-Z0-9_]+)'
<wrong_user_password> ::= r'^(?!the_password$)([a-zA-Z0-9_]+)'

# When producing or parsing <open_port> we call the open_data_port generator function to reconfigure the data parties.
# This method gets called both when parsing and producing.
# When producing, the parameter <open_port_param> also gets generated by FANDANGO. <open_port_param> consists of
# <passive_port> and another generator that depends on <open_port>. This generator doesn't get executed when generating
# parameters for the generator from <open_port> to not get caught in an infinite loop between those two generators.
# Instead we generate <passive_port> directly without invoking the generator.
# When parsing <open_port> FANDANGO derives the argument <open_port_param> used in the generator by executing the generator
# from <open_port_param> which depends on <open_port>
<open_port> ::= <passive_port> := open_data_port(int(<open_port_param>))
<open_port_param> ::= <passive_port> := open_data_port(int(<open_port>))
# We use a generator to randomly generate a port in [50100, 50100] when generating a passive port.
<passive_port> ::= r'[1-9][0-9]{0,4}' := randint(50100, 50100)

# open_data_port(port) is a generator. When executed, it returns the value
# given to it and reconfigures the data party definitions to use that port.
def open_data_port(port) -> int:
    try:
        client_data = ClientData.instance()
        server_data = ServerData.instance()
    except KeyError:
        # Party instances not created
        return port

    if client_data.port != port:
        client_data.stop()
        client_data.port = port
    if server_data.port != port:
        server_data.stop()
        server_data.port = port
    client_data.start()
    server_data.start()
    return port
