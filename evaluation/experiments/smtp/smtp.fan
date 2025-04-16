import base64
import socket
from datetime import datetime, timezone
import random

fandango_is_client = False

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
<state_setup> ::= <Server:response_setup><Client:request_ehlo><Server:response_ehlo><state_logged_out>
<state_logged_out> ::= <exchange_login>
<state_logged_in> ::= <exchange_quit> |  <exchange_mail>

<exchange_login> ::= <Client:request_auth><Server:response_auth_expect_user>
    (<Client:request_auth_user_correct>|<Client:request_auth_user_incorrect>)<Server:response_auth_expect_pass>
    (<Client:request_auth_pass_correct>|<Client:request_auth_pass_incorrect>) ((<Server:response_auth_success><state_logged_in>)|(<Server:response_auth_fail><state_logged_out>))

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

<user_incorrect> ::= r'^(?!the_user)([a-zA-Z0-9]+)' := decode64(<user_incorrect_64>)
<pass_incorrect> ::= r'^(?!the_password)([a-zA-Z0-9]+)' := decode64(<pass_incorrect_64>)

where len(str(<request_auth_user_incorrect>)) >= 6


<response_setup> ::= '220 fake-smtp-server ESMTP FakeSMTPServer 2.2.1\r\n'
<request_ehlo> ::= 'EHLO ' <client_identifier> '\r\n'
<client_identifier> ::= r'[a-zA-Z0-9\-\. ]+'
<response_ehlo> ::= <response_ehlo_param>+<response_ehlo_end> := '250-fandango-server\r\n250-8BITMIME\r\n250-AUTH PLAIN LOGIN\r\n250 Ok\r\n'
<response_ehlo_param> ::= '250-' r'[a-zA-Z0-9\- ]+' '\r\n'
<response_ehlo_end> ::= '250 Ok\r\n'

<exchange_quit> ::= <Client:request_quit><Server:response_quit>(<state_logged_out> | '')
<request_quit> ::= 'QUIT\r\n'
<response_quit> ::= '221 Bye\r\n'


<exchange_mail> ::= <Client:request_mail_from><Server:response_mail_from>
    <Client:request_mail_to><Server:response_mail_to>
    <Client:request_mail_data><Server:response_mail_data>
    <Client:Server:mail_data><Server:response_submit><state_logged_in>

<mail_data> ::= <mail_header><mail_body>
<mail_header> ::= <mail_header_subject>
    <mail_header_from>
    <mail_header_to>
    <mail_header_date>
    <mail_header_mailer>
    <mail_header_mime>
    <mail_header_content_type>
    <mail_header_encoding>
    <mail_header_end>
<mail_body> ::= <mail_contents_64><mail_body_end>

<request_mail_from> ::= 'MAIL FROM:<' <email_address> '>\r\n'
<response_mail_from> ::= '250 Ok\r\n'
<request_mail_to> ::= 'RCPT TO:<' <email_address> '>\r\n'
<response_mail_to> ::= '250 Ok\r\n'
<request_mail_data> ::= 'DATA\r\n'
<response_mail_data> ::= '354 End data with <CR><LF>.<CR><LF>\r\n'

<mail_body_end> ::= '\r\n.\r\n'
<mail_contents_64> ::= r'[a-zA-Z0-9\+\\\=]+' := encode64(<mail_contents>)
<mail_contents> ::= r'([a-zA-Z0-9]+)' := decode64(<mail_contents_64>)

<mail_header_subject> ::= 'subject: ' r'[a-z]+' '\r\n'
<mail_header_from> ::= 'from: ' <email_address> '\r\n'
<mail_header_to> ::= 'to: ' <email_address> '\r\n'
<mail_header_date> ::= 'date: ' <unix_time_formatted> '\r\n'
<mail_header_mailer> ::= 'x-mailer: ' r'[a-z]+' '\r\n'
<mail_header_mime> ::= 'mime-version: 1.0\r\n'
<mail_header_content_type> ::= 'content-type: text/plain; charset=utf-8\r\n'
<mail_header_encoding> ::= 'content-transfer-encoding: base64\r\n'
<mail_header_end> ::= '\r\n'
<response_submit> ::= '250 Ok\r\n'
<email_address> ::= r'[a-z]+@[a-z]+\.[a-z]+'
<unix_time_formatted> ::= r'[a-zA-Z0-9\:\+\, ]+' := format_unix_time(int(<unix_time>))
<unix_time> ::= <unix_time_number> := str(str_to_unix_time(<unix_time_formatted>))
<unix_time_number> ::= r'[1-9][0-9]+' := str(random.randint(0, 2147483647))

where forall <mail> in <mail_data>:
    str(<mail>..<request_mail_from>.<email_address>) == str(<mail>..<mail_header_from>.<email_address>)
    and str(<mail>..<request_mail_to>.<email_address>) == str(<mail>..<mail_header_to>.<email_address>)


class Client(FandangoAgent):
    def __init__(self):
        super().__init__(fandango_is_client)
        if not self.is_fandango():
            return
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect(("127.0.0.1", 8025))
        server_thread = threading.Thread(target=self.listen_loop)
        server_thread.daemon = True
        server_thread.start()

    def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
        self.sock.sendall(message.encode("utf-8"))

    def listen_loop(self):
        while True:
            response, nothing = self.sock.recvfrom(1024)
            if len(response) == 0:
                self.receive_msg("Server", "SMTP session closed.\r\n")
                self.sock.close()
                break
            self.receive_msg("Server", response.decode("utf-8"))



class Server(FandangoAgent):
    def __init__(self):
        super().__init__(not fandango_is_client)
        self.sock = None
        self.send_thread = None
        self.running = False
        if not self.is_fandango():
            return
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", 8025))
        self.sock.listen(1)
        print("listening on port 8025")
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
                    self.receive_msg("Client", data.decode("utf-8"))
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
