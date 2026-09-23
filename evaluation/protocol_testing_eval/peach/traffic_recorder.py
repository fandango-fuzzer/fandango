"""
Format e.g.:

  {"time": 1758650000.123, "channel": "control", "conn": 3, "event": "data", "sender": "client", "data": "<base64>"}

event is "open", "data" or "close". sender is "client" (Peach/Fandango) or "server" (SUT).
For TCP, conn is one connection; for UDP, one client address.

  traffic_recorder.py --out traffic.jsonl --tcp 2121:2122:control --tcp 50100:50101:data
  traffic_recorder.py --out traffic.jsonl --udp 25567:25566:dns
"""
import argparse
import base64
import itertools
import json
import socket
import threading
import time

HOST = "127.0.0.1"


class Log:
    def __init__(self, path):
        self._file = open(path, "a", buffering=1)
        self._lock = threading.Lock()
        self._conn_ids = itertools.count(1)

    def new_conn(self):
        return next(self._conn_ids)

    def write(self, channel, conn, event, sender=None, data=None):
        record = {"time": time.time(), "channel": channel, "conn": conn, "event": event}
        if sender is not None:
            record["sender"] = sender
        if data is not None:
            record["data"] = base64.b64encode(data).decode("ascii")
        with self._lock:
            self._file.write(json.dumps(record) + "\n")


def pump(log, channel, conn, sender, src, dst, done):
    while True:
        try:
            chunk = src.recv(65536)
        except OSError:
            break
        if not chunk:
            break
        log.write(channel, conn, "data", sender, chunk)
        try:
            dst.sendall(chunk)
        except OSError:
            break
    try:
        dst.shutdown(socket.SHUT_WR)
    except OSError:
        pass
    log.write(channel, conn, "close", sender)
    done.release()


def relay_tcp(log, channel, client, target_port):
    conn = log.new_conn()
    try:
        server = socket.create_connection((HOST, target_port), timeout=10)
        server.settimeout(None)
    except OSError:
        client.close()
        return
    log.write(channel, conn, "open")
    done = threading.Semaphore(0)
    threading.Thread(target=pump, args=(log, channel, conn, "client", client, server, done), daemon=True).start()
    pump(log, channel, conn, "server", server, client, done)
    done.acquire()
    done.acquire()
    client.close()
    server.close()


def serve_tcp(log, listen_port, target_port, channel):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((HOST, listen_port))
    listener.listen(16)
    while True:
        client, _ = listener.accept()
        threading.Thread(target=relay_tcp, args=(log, channel, client, target_port), daemon=True).start()


def serve_udp(log, listen_port, target_port, channel):
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.bind((HOST, listen_port))
    upstreams = {}

    def replies(addr, conn, upstream):
        while True:
            try:
                data = upstream.recv(65536)
            except OSError:
                return
            log.write(channel, conn, "data", "server", data)
            listener.sendto(data, addr)

    while True:
        data, addr = listener.recvfrom(65536)
        if addr not in upstreams:
            conn = log.new_conn()
            upstream = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            upstream.connect((HOST, target_port))
            upstreams[addr] = (conn, upstream)
            log.write(channel, conn, "open")
            threading.Thread(target=replies, args=(addr, conn, upstream), daemon=True).start()
        conn, upstream = upstreams[addr]
        log.write(channel, conn, "data", "client", data)
        upstream.send(data)


def route(spec):
    listen_port, target_port, channel = spec.split(":")
    return int(listen_port), int(target_port), channel


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--tcp", type=route, action="append", default=[])
    p.add_argument("--udp", type=route, action="append", default=[])
    args = p.parse_args()
    log = Log(args.out)
    threads = [threading.Thread(target=serve_tcp, args=(log, *r), daemon=True) for r in args.tcp]
    threads += [threading.Thread(target=serve_udp, args=(log, *r), daemon=True) for r in args.udp]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
