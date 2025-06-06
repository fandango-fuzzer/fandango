import random
import socket
import string


def send_socket(sock, message):
    sock.sendall(message.encode("utf-8"))


def scan_socket(sock):
    response, _ = sock.recvfrom(1024)
    return response.decode("utf-8")


def random_string():
    return "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(random.randint(10, 20))
    )


def fuzz():
    server_domain = "localhost"
    server_port = 21
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((server_domain, server_port))
    auth_failing(sock)


def auth_failing(sock):
    scan_socket(sock)
    user_request = valid_login_user_msg()
    user_valid = True
    if random.random() < 0.5:
        user_valid = False
        user_request = invalid_login_user_msg()
    send_socket(sock, user_request)
    user_response = scan_socket(sock)
    assert user_response.startswith("331 ") and user_response.endswith("\r\n")
    password_request = invalid_login_password_msg()
    if not user_valid and random.random() < 0.5:
        password_request = valid_login_password_msg()
    send_socket(sock, password_request)
    password_response = scan_socket(sock)
    assert password_response.startswith("530 ") and password_response.endswith("\r\n")
    send_socket(sock, "QUIT\r\n")


def valid_login_user_msg():
    return "USER correct_user\r\n"


def invalid_login_user_msg():
    user_name = random_string()
    while user_name == "correct_user":
        user_name = random_string()
    return "USER " + user_name + "\r\n"


def valid_login_password_msg():
    return "PASS correct_pass\r\n"


def invalid_login_password_msg():
    password = random_string()
    while password == "correct_pass":
        password = random_string()
    return "PASS " + password + "\r\n"


if __name__ == "__main__":
    fuzz()
