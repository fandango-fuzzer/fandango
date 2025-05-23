<start> ::= <ServerControl:ClientControl:response_server_info>
                          ((<ClientControl:ServerControl:request_login_user_ok>
                            <ServerControl:ClientControl:response_login_user>
                            <ClientControl:ServerControl:request_login_pass_fail>
                          )
                               |
                          (<ClientControl:ServerControl:request_login_user_fail>
                            <ServerControl:ClientControl:response_login_user>
                            (<ClientControl:ServerControl:request_login_pass_fail>|<ClientControl:ServerControl:request_login_pass_ok>)
                          ))
                           <ServerControl:ClientControl:response_login_pass_fail>
                           <ClientControl:ServerControl:request_quit>

<response_server_info> ::= '220 ' r'[a-zA-Z0-9\_\.\(\) ]+\s' '[' r'[a-zA-Z0-9\:\.]+' ']\r\n'
<request_login_user_ok> ::= 'USER the_user\r\n'
<response_login_user> ::= '331 ' <command_tail> '\r\n'
<request_login_pass_ok> ::= 'PASS the_password\r\n'
<command_tail> ::= r'([a-zA-Z0-9\_\. ]+)'
<wrong_user_name> ::= r'^(?!the_user\r\n$)([a-zA-Z0-9_]+)'
<wrong_user_password> ::= r'^(?!the_password\r\n$)([a-zA-Z0-9_]+)'
<request_login_user_fail> ::= 'USER ' <wrong_user_name> '\r\n'
<request_login_pass_fail> ::= 'PASS ' <wrong_user_password> '\r\n'
<response_login_pass_fail> ::= '530 ' <command_tail> '\r\n'
<request_quit> ::= 'QUIT\r\n'

import socket
import threading
import select
fandango_is_client = True

class ClientControl(FandangoAgent):
    def __init__(self):
        super().__init__(fandango_is_client)
        self.server_domain = "liggesmeyer.net"
        if not self.is_fandango():
            return
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.server_domain, 21))
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