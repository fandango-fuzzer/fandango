<start> ::= <ServerControl:ClientControl:response_server_info> <state_logged_out>

<state_logged_out> ::= ((<ClientControl:ServerControl:request_login_user_ok> \
                            <ServerControl:ClientControl:response_login_user> \
                            <ClientControl:ServerControl:request_login_pass_fail> \
                          ) \
                               | \
                          (<ClientControl:ServerControl:request_login_user_fail> \
                            <ServerControl:ClientControl:response_login_user> \
                            (<ClientControl:ServerControl:request_login_pass_fail>|<ClientControl:ServerControl:request_login_pass_ok>) \
                          )) \
                           <ServerControl:ClientControl:response_login_pass_fail> \
                           <ClientControl:ServerControl:request_quit><ServerControl:ClientControl:response_quit>

<response_server_info> ::= r'(220-(?:[\x20-\x7E]*\r\n))*220 (?:[\x20-\x7E]*)\r\n'

<request_login_user_ok> ::= 'USER the_user\r\n'
<response_login_user> ::= '331 ' <command_tail> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'

<request_login_user_fail> ::= 'USER ' r'^(?!the_user$)([a-zA-Z0-9_]+)' '\r\n'
<request_login_pass_fail> ::= 'PASS ' r'^(?!the_password$)([a-zA-Z0-9_]+)' '\r\n'
<response_login_pass_fail> ::= '530 ' <command_tail> '\r\n'
<request_quit> ::= 'QUIT\r\n'
<response_quit> ::= '221 ' <command_tail> '\r\n'

<command_tail> ::= r'[\x20-\x7E]+'