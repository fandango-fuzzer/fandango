import argparse
import re
import socket
import ssl
import threading

PASV_RE = re.compile(rb"^(227[ -].*?\()\d+,\d+,\d+,\d+,(\d+),(\d+)(\).*)$", re.S)
EPSV_RE = re.compile(rb"^(229[ -].*?\(\|\|\|)(\d+)(\|\).*)$", re.S)


class Session:
    def __init__(self):
        self.upstream = None
        self.ssl_context = None
        self.tls_active = False
        self.data_tls = False
        self.data_port = None
        self.tls_pending = None
        self.lock = threading.Lock()


current = Session()


def tls_context():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def close(sock):
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    try:
        sock.close()
    except OSError:
        pass


def client_to_server(client, session):
    pending = b""
    while True:
        try:
            chunk = client.recv(65536)
        except OSError:
            break
        if not chunk:
            break
        pending += chunk
        *lines, pending = pending.split(b"\n")
        commands = [line.strip().upper() for line in lines]
        auth_tls = not session.tls_active and any(c.startswith(b"AUTH TLS") for c in commands)
        if auth_tls:
            session.tls_pending = threading.Event()
        try:
            with session.lock:
                session.upstream.sendall(chunk)
        except OSError:
            break
        if auth_tls:
            session.tls_pending.wait(5)
        for command in commands:
            if session.tls_active and command.startswith(b"PROT P"):
                session.data_tls = True
            elif session.tls_active and command.startswith(b"PROT C"):
                session.data_tls = False
    close(session.upstream)


def rewrite_reply(line, session, data_port):
    match = PASV_RE.match(line)
    if match:
        session.data_port = int(match.group(2)) * 256 + int(match.group(3))
        return b"%s127,0,0,1,%d,%d%s" % (match.group(1), data_port // 256, data_port % 256, match.group(4))
    match = EPSV_RE.match(line)
    if match:
        session.data_port = int(match.group(2))
        return b"%s%d%s" % (match.group(1), data_port, match.group(3))
    return line


def server_to_client(client, session, data_port):
    pending = b""
    while True:
        try:
            chunk = session.upstream.recv(65536)
        except OSError:
            break
        if not chunk:
            break
        pending += chunk
        *lines, pending = pending.split(b"\n")
        for line in lines:
            reply = rewrite_reply(line + b"\n", session, data_port)
            try:
                client.sendall(reply)
            except OSError:
                return
            if session.tls_pending is not None and not session.tls_pending.is_set():
                if reply.startswith(b"234"):
                    upgrade(session)
                session.tls_pending.set()
    if pending:
        try:
            client.sendall(pending)
        except OSError:
            pass
    close(client)


def upgrade(session):
    try:
        with session.lock:
            session.ssl_context = tls_context()
            session.upstream = session.ssl_context.wrap_socket(session.upstream, server_hostname="localhost")
            session.tls_active = True
    except (OSError, ssl.SSLError):
        close(session.upstream)


def serve_control(client, server_port, data_port):
    global current
    session = Session()
    try:
        session.upstream = socket.create_connection(("127.0.0.1", server_port), timeout=10)
        session.upstream.settimeout(None)
    except OSError:
        close(client)
        return
    current = session
    threading.Thread(target=client_to_server, args=(client, session), daemon=True).start()
    server_to_client(client, session, data_port)


def pump(src, dst):
    while True:
        try:
            chunk = src.recv(65536)
        except OSError:
            break
        if not chunk:
            break
        try:
            dst.sendall(chunk)
        except OSError:
            break
    close(dst)
    close(src)


def serve_data(client):
    session = current
    if session.data_port is None:
        close(client)
        return
    try:
        upstream = socket.create_connection(("127.0.0.1", session.data_port), timeout=10)
        upstream.settimeout(None)
        if session.data_tls and session.ssl_context is not None:
            upstream = session.ssl_context.wrap_socket(upstream, server_hostname="localhost")
    except (OSError, ssl.SSLError):
        close(client)
        return
    threading.Thread(target=pump, args=(client, upstream), daemon=True).start()
    pump(upstream, client)


def listen(port, handler, *args):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen(16)
    while True:
        client, _ = server.accept()
        threading.Thread(target=handler, args=(client, *args), daemon=True).start()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--server-port", type=int, default=2200)
    p.add_argument("--control-port", type=int, default=2121)
    p.add_argument("--data-port", type=int, default=50100)
    args = p.parse_args()
    threading.Thread(target=listen, args=(args.data_port, serve_data), daemon=True).start()
    listen(args.control_port, serve_control, args.server_port, args.data_port)


if __name__ == "__main__":
    main()
