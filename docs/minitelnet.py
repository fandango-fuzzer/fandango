#!/usr/bin/env python

import socket
import os
import time
import re


def sanitize_hostname(s: str, alt_hostname: str = "smtp.example.com") -> str:
    """Remove actual host names from server responses for reproducibility."""
    hostname = socket.gethostname()
    insensitive_hostname = re.compile(re.escape(hostname), re.IGNORECASE)
    return insensitive_hostname.sub(alt_hostname, s)


def telnet(commands: list[str], port=8025, host="localhost"):
    """Simulate a telnet session to port on host."""

    print(f"Trying {host}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"Connected to {host}.")
    print("Escape character is '^]'.")

    r = s.makefile("rw")
    while True:
        line = r.readline()
        if not line:
            break
        print(f"{sanitize_hostname(line.strip())}")
        if commands:
            cmd = commands.pop(0)
            print(f"{cmd.strip()}")
            r.write(cmd)
            r.flush()
    s.close()
    print("Connection closed by foreign host.")


if __name__ == "__main__":
    os.system("pkill -f aiosmtpd")
    os.system("python -m aiosmtpd -n &")
    time.sleep(0.5)  # Give the server a moment to start

    commands = ["HELO relay.example.org\r\n", "QUIT\r\n"]
    telnet(commands)

    os.system("pkill -f aiosmtpd")
