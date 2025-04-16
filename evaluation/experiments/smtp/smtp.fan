import base64
import socket

def encode64(input):
    return base64.b64encode(input.encode('utf-8')).decode('utf-8')

def decode64(input):
    return base64.b64decode(input.encode('utf-8')).decode('utf-8')

fandango_is_client = True

<start> ::= <state_setup>
<state_setup> ::= <Server:response_setup><state_logged_out>
<state_logged_out> ::= <exchange_login>
<state_logged_in> ::= <exchange_quit>

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
<exchange_quit> ::= <Client:request_quit><Server:response_quit>(<state_logged_out> | '')
<request_quit> ::= 'QUIT\r\n'
<response_quit> ::= '221 Bye\r\n'




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

    def on_send(self, message: str|bytes, recipient: str, response_setter: Callable[[str, str], None]):
        pass
