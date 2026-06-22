from random import randint

DATA_PORT = 50100

<start> ::= <banner_exchange> <unauthenticated_state>
<banner_exchange> ::= <ServerControl:greeting_block>
<greeting_block> ::= '220' <response_tail> := '220 LightFTP server v2.0a ready\r\n'

<unauthenticated_state> ::= <unauthenticated_exchanges>
<unauthenticated_exchanges> ::= <AUTH_exchange> <authenticated_state> \
                              | <AUTH_TLS_upgrade> <unauthenticated_tls_state>
<unauthenticated_tls_state> ::= <AUTH_exchange> <authenticated_state>

<authenticated_state> ::= (<control_exchanges> <authenticated_state>) \
                        | ((<PASV_exchange> | <EPSV_exchange>) <data_exchanges> <authenticated_state>) \
                        | <QUIT_exchange>
<control_exchanges> ::= (<PROT_exchange> | <PBSZ_exchange> | <OPTS_exchange> | <FEAT_exchange> \
                       | <SIZE_exchange> | <REST_exchange> | <TYPE_exchange> | <SITE_exchange> \
                       | <NOOP_exchange> | <SYST_exchange> | <PORT_exchange> | <HELP_exchange> \
                       | (<RNFR_exchange> <RNTO_exchange>?) | <RMD_exchange> | <MKD_exchange> \
                       | <PWD_exchange> | <CWD_exchange> | <CDUP_exchange> | <DELE_exchange>)
<data_exchanges> ::= <STOR_exchange> | <LIST_exchange> | <ABOR_exchange> \
                   | <APPE_exchange> | <RETR_exchange> | <MLSD_exchange>

<AUTH_exchange> ::= <ClientControl:USER> <ServerControl:USER_response> <ClientControl:PASS> <ServerControl:PASS_response>
<QUIT_exchange> ::= <ClientControl:QUIT> <ServerControl:QUIT_response>
<PORT_exchange> ::= <ClientControl:PORT> <ServerControl:PORT_response>
<DELE_exchange> ::= <ClientControl:DELE> <ServerControl:DELE_response>
<RNFR_exchange> ::= <ClientControl:RNFR> <ServerControl:RNFR_response>
<RNTO_exchange> ::= <ClientControl:RNTO> <ServerControl:RNTO_response>
<CWD_exchange> ::= <ClientControl:CWD> <ServerControl:CWD_response>
<CDUP_exchange> ::= <ClientControl:CDUP> <ServerControl:CDUP_response>
<PWD_exchange> ::= <ClientControl:PWD> <ServerControl:PWD_response>
<MKD_exchange> ::= <ClientControl:MKD> <ServerControl:MKD_response>
<RMD_exchange> ::= <ClientControl:RMD> <ServerControl:RMD_response>
<HELP_exchange> ::= <ClientControl:HELP> <ServerControl:HELP_response>
<SYST_exchange> ::= <ClientControl:SYST> <ServerControl:SYST_response>
<NOOP_exchange> ::= <ClientControl:NOOP> <ServerControl:NOOP_response>
<SITE_exchange> ::= <ClientControl:SITE> <ServerControl:SITE_response>
<TYPE_exchange> ::= <ClientControl:TYPE> <ServerControl:TYPE_response>
<PASV_exchange> ::= <ClientControl:PASV> <ServerControl:PASV_response>

<close_data_either> ::= <SocketControlClient:close_data> | <SocketControlServer:close_data>

<ABOR_exchange> ::= <ClientControl:ABOR> (<ServerControl:ABOR_response> <close_data_either> | <close_data_either> <ServerControl:ABOR_response>)
<APPE_exchange> ::= <ClientControl:APPE> <ServerControl:Response_150> (<ClientData:APPE_data>* <close_data_either>)? <ServerControl:Response_226>
<LIST_exchange> ::= <ClientControl:LIST> <ServerControl:Response_150> <ServerData:LIST_data>? (<SocketControlServer:close_data> <ServerControl:Response_226> | <ServerControl:Response_226> <ServerData:LIST_data>? <SocketControlServer:close_data>)
<REST_exchange> ::= <ClientControl:REST> <ServerControl:REST_response>
<RETR_exchange> ::= <ClientControl:RETR> <ServerControl:Response_150> <ServerData:RETR_data>? (<SocketControlServer:close_data> <ServerControl:Response_226> | <ServerControl:Response_226> <ServerData:RETR_data>? <SocketControlServer:close_data>)
<STOR_exchange> ::= <ClientControl:STOR> <ServerControl:Response_150> (<ClientData:STOR_data>* <close_data_either>)? <ServerControl:Response_226>
<FEAT_exchange> ::= <ClientControl:FEAT> <ServerControl:FEAT_response>
<SIZE_exchange> ::= <ClientControl:SIZE> <ServerControl:SIZE_response>
<OPTS_exchange> ::= <ClientControl:OPTS> <ServerControl:OPTS_response>
<MLSD_exchange> ::= <ClientControl:MLSD> <ServerControl:Response_150> <ServerData:MLSD_data>? (<SocketControlServer:close_data> <ServerControl:Response_226> | <ServerControl:Response_226> <ServerData:MLSD_data>? <SocketControlServer:close_data>)
<AUTH_TLS_upgrade> ::= <ClientControl:AUTH_TLS> <ServerControl:AUTH_TLS_response> <SocketControlClient:AUTH_TLS_negotiate>
<PBSZ_exchange> ::= <ClientControl:PBSZ> <ServerControl:PBSZ_response>
<PROT_exchange> ::= <ClientControl:PROT> <ServerControl:PROT_response>
<EPSV_exchange> ::= <ClientControl:EPSV> <ServerControl:EPSV_response>

<APPE_data> ::= r"[\s\S]*" := 'appended by fandango\r\n'

<data_line> ::= r"[^\r\n]*" r"\r?\n"
<data_tail> ::= r"[^\r\n]+"
<data_lines> ::= <data_line>+ <data_tail>? | <data_tail>
<LIST_data> ::= <data_lines> := '-rw-r--r-- 1 0 0 10 Jan 01 00:00 exist_append.txt\r\n'
<RETR_data> ::= <data_lines> := "I'm a file\n"
<STOR_data> ::= r"[\s\S]*" := 'stored by fandango\r\n'
<MLSD_data> ::= <data_lines> := 'type=file;size=10;modify=20240101000000; exist_append.txt\r\n'

<close_data> ::= <close_data_inner>
<close_data_inner> ::= '999 Data socket closed.' <crlf>
<AUTH_TLS_negotiate> ::= '998 TLS upgrade.' <crlf>


where str(<APPE>.<file>) == "exist_append.txt"
where str(<RETR>.<file>) == "exist_append.txt"
where str(<DELE>.<file>) != "exist_append.txt"

where str(<LIST>.<directory>) == "dir_1" or str(<LIST>.<directory>) == "dir_1/dir_2"
where str(<RNFR>.<dir_file>) == "dir_1/dir_2/rn_1.txt" or str(<RNFR>.<dir_file>) == "dir_1/dir_2/rn_2.txt"
where str(<RNTO>.<dir_file>) == "dir_1/dir_2/rn_1.txt" or str(<RNTO>.<dir_file>) == "dir_1/dir_2/rn_2.txt"
where str(<MLSD>.<directory>) == "dir_1" or str(<MLSD>.<directory>) == "dir_1/dir_2"

<QUIT> ::= "QUIT" <crlf>
<USER> ::= "USER" <space> <word> <crlf>
<PASS> ::= "PASS" <space> <text> <crlf>
<PORT> ::= "PORT" <space> <ip_6_tuple> <crlf>
<RNFR> ::= "RNFR" <space> <dir_file> <crlf>
<RNTO> ::= "RNTO" <space> <dir_file> <crlf>
<DELE> ::= "DELE" <space> <file> <crlf>
<CDUP> ::= "CDUP" <crlf>
<CWD> ::= "CWD" <space> <directory> <crlf>
<PWD> ::= "PWD" <crlf>
<MKD> ::= "MKD" <space> <filesystem_name> <crlf>
<RMD> ::= "RMD" <space> <filesystem_name> <crlf>
<SYST> ::= "SYST" <crlf>
<HELP> ::= "HELP" <crlf>
<NOOP> ::= "NOOP" <crlf>
<SITE> ::= "SITE" <space> <text> <crlf>
<TYPE> ::= "TYPE" <space> ("A" (<space> "N")? | "I") <crlf>
<PASV> ::= "PASV" <crlf>
<ABOR> ::= "ABOR" <crlf>
<APPE> ::= "APPE" <space> <file> <crlf>
<LIST> ::= "LIST" (<space> <directory>)? <crlf>
<REST> ::= "REST" <space> <marker> <crlf>
<RETR> ::= "RETR" <space> <file> <crlf>
<STOR> ::= "STOR" <space> <file> <crlf>
<FEAT> ::= "FEAT" <crlf>
<SIZE> ::= "SIZE" <space> <dir_file> <crlf>
<OPTS> ::= "OPTS" <space> <text> <crlf>
<MLSD> ::= "MLSD" (<space> <directory>)? <crlf>
<AUTH_TLS> ::= "AUTH" <space> "TLS" <crlf>
<PBSZ> ::= "PBSZ" <space> <number> <crlf>
<PROT> ::= "PROT" <space> ("C" | "P") <crlf>
<EPSV> ::= "EPSV" <crlf>

# LightFTP's SITE only implements the "HELP" sub-command.
where str(<SITE>.<text>) == "HELP"

<resp_code> ::= r'\d\d\d'
<USER_response> ::= <resp_code> <response_tail> := '331 User webadmin OK. Password required\r\n'
<PASS_response> ::= <resp_code> <response_tail> := '230 User logged in, proceed.\r\n'
<QUIT_response> ::= <resp_code> <response_tail> := '221 Goodbye!\r\n'
<PORT_response> ::= <resp_code> <response_tail> := '200 Command okay.\r\n'
<DELE_response> ::= <resp_code> <response_tail> := '250 Requested file action okay, completed.\r\n'
<RNFR_response> ::= <resp_code> <response_tail> := '350 File exists. Ready to rename.\r\n'
<RNTO_response> ::= <resp_code> <response_tail> := '250 Requested file action okay, completed.\r\n'
<CWD_response> ::= <resp_code> <response_tail> := '250 Requested file action okay, completed.\r\n'
<CDUP_response> ::= <resp_code> <response_tail> := '250 Requested file action okay, completed.\r\n'
<PWD_response> ::= <resp_code> <response_tail> := '257 "/" is a current directory.\r\n'
<MKD_response> ::= <resp_code> <response_tail> := '257 Directory created.\r\n'
<RMD_response> ::= <resp_code> <response_tail> := '250 Requested file action okay, completed.\r\n'
<SYST_response> ::= <resp_code> <response_tail> := '215 UNIX Type: L8\r\n'
<NOOP_response> ::= <resp_code> <response_tail> := '200 Command okay.\r\n'
<SITE_response> ::= <resp_code> <response_tail> := '200 chmod\r\n'
<TYPE_response> ::= <resp_code> <response_tail> := '200 Type set to I.\r\n'
<ABOR_response> ::= <resp_code> <response_tail> := '226 Transfer complete. Closing data connection.\r\n'
<REST_response> ::= <resp_code> <response_tail> := '350 REST supported. Ready to resume at byte offset  0\r\n'
<SIZE_response> ::= <resp_code> <response_tail> := '213 10\r\n'
<PBSZ_response> ::= <resp_code> <response_tail> := '200 Command okay.\r\n'
<PROT_response> ::= <resp_code> <response_tail> := '200 Command okay.\r\n'
<OPTS_response> ::= <resp_code> <response_tail> := '200 Always in UTF8 mode.\r\n'
<AUTH_TLS_response> ::= <resp_code> <response_tail> := '234 AUTH command OK. Initializing TLS connection.\r\n'

<Response_150> ::= '150' <response_tail> := '150 File status okay; about to open data connection.\r\n'
<Response_226> ::= '226' <response_tail> := '226 Transfer complete. Closing data connection.\r\n'

<FEAT_response> ::= <multiline_response> := feat_response()
<HELP_response> ::= <multiline_response> := help_response()
<multiline_response> ::= r"[\s\S]*"

def feat_response() -> str:
    return ("211-Extensions supported:\r\n PASV\r\n UTF8\r\n TVFS\r\n REST STREAM\r\n "
            "SIZE\r\n MLSD\r\n AUTH TLS\r\n PBSZ\r\n PROT\r\n EPSV\r\n211 End.\r\n")

def help_response() -> str:
    return ("214-The following commands are recognized.\r\n"
            " ABOR APPE AUTH CDUP CWD  DELE EPSV FEAT HELP LIST MKD MLSD NOOP OPTS\r\n"
            " PASS PASV PBSZ PORT PROT PWD  QUIT REST RETR RMD RNFR RNTO SITE SIZE\r\n"
            " STOR SYST TYPE USER\r\n214 Help OK.\r\n")

<PASV_response> ::= '227 Entering Passive Mode (' <pasv_socket> ').' <crlf>
<pasv_socket> ::= <socket_addr> := set_pasv_socket(<open_pasv_socket>)
<open_pasv_socket> ::= <socket_addr> := set_pasv_socket(<pasv_socket>)
<socket_addr> ::= <pasv_ip_1> "," <pasv_ip_2> "," <pasv_ip_3> "," <pasv_ip_4> "," <pasv_port_hi> "," <pasv_port_lo>
<pasv_ip_1> ::= r'[0-9]+' := "127"
<pasv_ip_2> ::= r'[0-9]+' := "0"
<pasv_ip_3> ::= r'[0-9]+' := "0"
<pasv_ip_4> ::= r'[0-9]+' := "1"
<pasv_port_hi> ::= r'[0-9]+' := str(DATA_PORT // 256)
<pasv_port_lo> ::= r'[0-9]+' := str(DATA_PORT % 256)

<EPSV_response> ::= '229 Entering Extended Passive Mode (|||' <open_port> '|)\r\n'

<response_tail> ::= <space> <text> <crlf>
<text> ::= r"[^\r\n\x80-\xFF]+"
<word> ::= r"[\x00-\x1F\x21-\x7F]+"
<number> ::= r"(0|[1-9][0-9]*)"
<space> ::= " "
<crlf> ::= "\r\n"
<ip_6_tuple> ::= <ip_number_1> "," <ip_number> "," <ip_number> "," <ip_number> "," <port_nr_1> "," <port_nr_2>
<ip_number_1> ::= <ip_number>
<ip_number> ::= r'[0-9]+' := str(randint(0, 254))
<port_nr_1> ::= r'[0-9]+' := str(randint(1, 255))
<port_nr_2> ::= r'[0-9]+' := str(randint(1, 255))
<dir_file> ::= (<directory> '/')? <file>
<directory> ::= "/" | "/"? <filesystem_name> ("/" <filesystem_name>)* "/"?
<file> ::= <filesystem_name> ('.' <filesystem_name>)?
<filesystem_name> ::= r'[a-zA-Z0-9\_]+'
<marker> ::= r"[a-zA-Z0-9\-\.]+"

<open_port> ::= <passive_port> := open_data_port(int(<open_port_param>))
<open_port_param> ::= <passive_port> := open_data_port(int(<open_port>))
<passive_port> ::= r'[1-9][0-9]{0,4}' := DATA_PORT

where str(<USER>.<word>) == "webadmin"
where str(<PASS>.<text>) == "ubuntu"

where int(str(<PORT>..<ip_number>)) < 256
where int(str(<PORT>..<ip_number_1>)) > 0
where int(str(<port_nr_2>)) < 256
where forall <port_req> in <PORT>:
    int(str(<port_req>..<port_nr_1>)) * 256 + int(str(<port_req>..<port_nr_2>)) < 65536
where forall <port_req> in <PORT>:
    int(str(<port_req>..<port_nr_1>)) * 256 + int(str(<port_req>..<port_nr_2>)) > 1023


_last_data_port = [None]
def _reconfigure_data_parties(port) -> None:
    try:
        client_data = ClientData.instance()
        server_data = ServerData.instance()
    except KeyError:
        return
    fuzzer_data = server_data if server_data.is_fuzzer_controlled() else client_data
    impl = fuzzer_data.protocol_impl
    already_live = _last_data_port[0] == port and impl is not None and impl._running
    if already_live:
        return
    _last_data_port[0] = port
    for party in (client_data, server_data):
        party.stop()
        party.port = port
        party.start()

def set_pasv_socket(pasv_socket) -> str:
    pasv_socket = pasv_socket[0]
    port = (int(pasv_socket[8]) * 256) + int(pasv_socket[10])
    _reconfigure_data_parties(port)
    return str(pasv_socket)

def open_data_port(port) -> int:
    _reconfigure_data_parties(port)
    return port
