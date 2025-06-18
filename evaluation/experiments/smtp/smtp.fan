import base64
import socket
from datetime import datetime, timezone
import random

def format_unix_time(unix_time):
    dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    return dt.strftime('%a, %d %b %Y %H:%M:%S %z')

def str_to_unix_time(unix_time_formatted):
    dt = datetime.strptime(unix_time_formatted, '%a, %d %b %Y %H:%M:%S %z')
    return int(dt.timestamp())

def encode64(input):
    return base64.b64encode(input.encode('utf-8')).decode('utf-8')

def decode64(input):
    return base64.b64decode(input.encode('utf-8')).decode('utf-8')

<start> ::= <state_setup>

# When setting up the connection the server sends a id message and exchange an ehlo. Afterwards the grammar leads over to <state_logged_out>.
<state_setup> ::= <Server:response_setup><Client:request_ehlo><Server:response_ehlo><state_logged_out>

# In state logged out the grammar accepts either a failing or a successful login.
<state_logged_out> ::= <exchange_login_valid> | <exchange_login_invalid>

# When logged in the grammar accepts either a quit (terminating the connection) or a mail exchange.
<state_logged_in> ::= <exchange_quit> |  <exchange_mail>

# A successful login consist of the correct username and password and leads to the logged in state.
<exchange_login_valid> ::= <Client:request_auth><Server:response_auth_expect_user><Client:request_auth_user_correct><Server:response_auth_expect_pass> \
    <Client:request_auth_pass_correct><Server:response_auth_success><state_logged_in>

# A failed login consist of incorrect username and incorrect password, incorrect username and correct
# password or correct username and incorrect password. The rule ends with the fuzzer going back into the logged out state.
<exchange_login_invalid> ::= <Client:request_auth><Server:response_auth_expect_user> \
                          ((<Client:request_auth_user_correct> \
                            <Server:response_auth_expect_pass> \
                            <Client:request_auth_pass_incorrect> \
                          ) \
                               | \
                          (<Client:request_auth_user_incorrect> \
                            <Server:response_auth_expect_pass> \
                            (<Client:request_auth_pass_incorrect>|<Client:request_auth_pass_correct>) \
                          )) \
                           <Server:response_auth_fail><state_logged_out>

<request_auth> ::= 'AUTH LOGIN\r\n'
<response_auth_expect_user> ::= '334 VXNlcm5hbWU6\r\n'
<request_auth_user_correct> ::= 'dGhlX3VzZXI=\r\n'
<request_auth_user_incorrect> ::= <user_incorrect_64> '\r\n'
<response_auth_expect_pass> ::= '334 UGFzc3dvcmQ6\r\n'
<request_auth_pass_correct> ::= 'dGhlX3Bhc3N3b3Jk\r\n'
<request_auth_pass_incorrect> ::= <pass_incorrect_64> '\r\n'
<response_auth_success> ::= '235 Authentication successful.\r\n'
<response_auth_fail> ::= '535 Authentication credentials invalid\r\n'

<user_incorrect_64> ::= r'[a-zA-Z0-9\+\\\=]+' := encode64(<user_incorrect>)
<pass_incorrect_64> ::= r'[a-zA-Z0-9\+\\\=]+' := encode64(<pass_incorrect>)

<user_incorrect> ::= r'^(?!the_user$)([a-zA-Z0-9_]+)' := decode64(<user_incorrect_64>)
<pass_incorrect> ::= r'^(?!the_password$)([a-zA-Z0-9_]+)' := decode64(<pass_incorrect_64>)

where len(str(<request_auth_user_incorrect>)) >= 6


<response_setup> ::= '220 ' r'[a-zA-Z0-9\-\. ]+' '\r\n'
<request_ehlo> ::= 'EHLO ' <client_identifier> '\r\n'
<client_identifier> ::= r'[a-zA-Z0-9\-\. ]+'
<response_ehlo> ::= <response_ehlo_param>+<response_ehlo_end> := '250-fandango-server\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
<response_ehlo_param> ::= '250-' r'[a-zA-Z0-9\- ]+' '\r\n'
<response_ehlo_end> ::= '250 Ok\r\n'

<exchange_quit> ::= <Client:request_quit><Server:response_quit><state_end>
<request_quit> ::= 'QUIT\r\n'
<response_quit> ::= '221 Bye\r\n'
<state_end> ::= ''

# When sending a mail the client to the server, the client first tells the server who he is and where to send the mail
# to, afterwards the client send mail headers and the mail body before finally submitting the mail and goind back to the logged in state.
<exchange_mail> ::= <Client:request_mail_from><Server:response_mail_from> \
    <Client:request_mail_to><Server:response_mail_to> \
    <Client:request_mail_data><Server:response_mail_data> \
    <Client:Server:mail_data><Server:response_submit><state_logged_in>

<mail_data> ::= <mail_header><mail_body>
<mail_header> ::= <mail_header_subject> \
    <mail_header_from> \
    <mail_header_to> \
    <mail_header_date> \
    <mail_header_mailer> \
    <mail_header_mime> \
    <mail_header_content_type> \
    <mail_header_encoding> \
    <mail_header_end>
<mail_body> ::= <mail_contents_64><mail_body_end>

<request_mail_from> ::= 'MAIL FROM:<' <email_address> '>\r\n'
<response_mail_from> ::= '250 Ok\r\n'
<request_mail_to> ::= 'RCPT TO:<' <email_address> '>\r\n'
<response_mail_to> ::= '250 Ok\r\n'
<request_mail_data> ::= 'DATA\r\n'
<response_mail_data> ::= '354 End data with <CR><LF>.<CR><LF>\r\n'

<mail_body_end> ::= '\r\n\r\n.\r\n'
<mail_contents_64> ::= r'[a-zA-Z0-9\+\\\=]+' := encode64(<mail_contents>)
<mail_contents> ::= r'([a-zA-Z0-9\r\n]+)' := decode64(<mail_contents_64>)

<mail_header_subject> ::= 'subject: ' r'[a-zA-Z0-9\-\_\:\. ]+' '\r\n'
<mail_header_from> ::= 'from: ' <email_address> '\r\n'
<mail_header_to> ::= 'to: ' <email_address> '\r\n'
<mail_header_date> ::= 'date: ' <unix_time_formatted> '\r\n'
<mail_header_mailer> ::= 'x-mailer: ' r'[a-zA-Z ]+' '\r\n'
<mail_header_mime> ::= 'mime-version: 1.0\r\n'
<mail_header_content_type> ::= 'content-type: text/plain; charset=utf-8\r\n'
<mail_header_encoding> ::= 'content-transfer-encoding: base64\r\n'
<mail_header_end> ::= '\r\n'
<response_submit> ::= '250 Ok\r\n'
<email_address> ::= r'[a-z]+@[a-z]+\.[a-z]+'
<unix_time_formatted> ::= r'[a-zA-Z0-9\:\+\, ]+' := format_unix_time(int(<unix_time>))
<unix_time> ::= <unix_time_number> := str(str_to_unix_time(str(<unix_time_formatted>)))
<unix_time_number> ::= r'[1-9][0-9]+' := str(random.randint(0, 2147483647))

where forall <mail> in <mail_data>:
    str(<mail>..<request_mail_from>.<email_address>) == str(<mail>..<mail_header_from>.<email_address>)
    and str(<mail>..<request_mail_to>.<email_address>) == str(<mail>..<mail_header_to>.<email_address>)

fandango_is_client = True

class Client(ConnectParty):
    def __init__(self):
        super().__init__(
            ownership=Ownership.FANDANGO_PARTY if fandango_is_client else Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT
            uri="tcp://localhost:8025"
        )
        self.start()

class Server(SocketServer):
    def __init__(self):
        super().__init__(
            ownership=Ownership.EXTERNAL if fandango_is_client else Ownership.FUZZER,
            ip_type=IpType.IPV4,
            ip="127.0.0.1",
            port=9025,
            protocol_type=Protocol.TCP
        )
        self.start()
