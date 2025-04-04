from random import randint

<start> ::= <state_setup>

<state_setup> ::= <exchange_socket_connect> <state_logged_out>
<state_logged_out> ::= <exchange_login>
<state_post_login> ::= <exchange_set_client><exchange_set_utf8><state_logged_in>
<state_logged_in> ::= ''

<exchange_socket_connect> ::= <response_server_info>
<response_server_info> ::= '220 ProFTPD Server (Debian) [1.2.3.4]\r\n'

<exchange_login> ::= <exchange_login_ok> | <exchange_login_fail>
<exchange_login_ok> ::= <request_login_user_ok><response_login_user><request_login_pass_ok><response_login_pass_ok><state_post_login>
<exchange_login_fail> ::= (<request_login_user_ok> | <request_login_user_fail>)<response_login_user><request_login_pass_fail><response_login_pass_fail><state_logged_out>



<request_login_user_ok> ::= 'USER the_user\r\n'
<response_login_user> ::= '331 Password required for the_user\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<response_login_pass_ok> ::= '230 User the_user logged in\r\n'

<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 Login incorrect.\r\n'

<exchange_set_client> ::= <request_set_client><response_set_client>
<request_set_client> ::= 'CLNT ' <client_name> '\r\n'
<response_set_client> ::= '200 OK\r\n'

<exchange_set_utf8> ::= <exchange_set_utf8><response_set_utf8>
<request_set_utf8> ::= 'OPTS UTF8 ON\r\n'
<response_set_utf8> ::= '200 UTF8 set to on\r\n'

<exchange_set_type> ::= <request_set_type><response_set_type>
<request_set_type> ::= 'TYPE I\r\n'
<response_set_type> ::= '200 Type set to I\r\n'

<exchange_set_passive> ::= <request_set_passive><response_set_passive>
<request_set_passive> ::= 'EPSV\r\n'
<response_set_passive> ::= '229 Entering Extended Passive Mode (|||' <open_port> '|)\r\n'

<exchange_pwd> ::= <request_pwd><response_pwd>
<request_pwd> ::= PWD\r\n
<response_pwd> ::= '257 \"' <directory> '\" is the current directory\r\n'
<directory> ::= '/' | ('/' <filesystem_name>)+
<file> ::= <filesystem_name> ('.' <filesystem_name>)?
<filesystem_name> ::= r"[a-zA-Z0-9]+"
<client_name> ::= r"[a-zA-Z0-9]+"

<wrong_user_name> ::= r"[a-zA-Z0-9]*"
<wrong_user_password> ::= r"[a-zA-Z0-9]*"

<open_port> ::= <passive_port> := open_data_agent(<open_port_param>)
<open_port_param> ::= <passive_port> := open_data_agent(<open_port>)
<passive_port> ::= <number> := randint(50000, 50100)


def open_data_port(port: int):
    FandangoIO.instance().roles['ClientDataAgent'].updatePort(int)
    FandangoIO.instance().roles['ServerDataAgent'].updatePort(int)