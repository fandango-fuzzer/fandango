import hashlib
import os
from struct import pack, unpack
from typing import Optional
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.io import NetworkParty, ConnectionMode, Protocol

# Re-use the radius_user_password function logic
def radius_user_password(password: bytes,
                         shared_secret: bytes,
                         request_authenticator: bytes) -> bytes:
    if len(request_authenticator) != 16:
        raise ValueError("Request Authenticator must be 16 bytes")

    MAX_STRING_LEN = 128
    pad_len = (16 - (len(password) % 16)) % 16
    padded = password + b"\x00" * pad_len

    if len(padded) == 0:
        padded = b"\x00" * 16
    if len(padded) > MAX_STRING_LEN:
        raise ValueError("Encoded User-Password exceeds 128 bytes")

    result = b""
    prev = request_authenticator
    for i in range(0, len(padded), 16):
        block = padded[i:i+16]
        bi = hashlib.md5(shared_secret + prev).digest()
        ci = bytes(a ^ b for a, b in zip(block, bi))
        result += ci
        prev = ci

    return result

def gen_authenticator():
    return os.urandom(16)

def calc_response_authenticator(packet_without_auth: bytes, request_authenticator: bytes, shared_secret: bytes) -> bytes:
    # Response Authenticator = MD5(Code + ID + Length + RequestAuthenticator + Attributes + SharedSecret)
    # packet_without_auth contains Code + ID + Length (with zeroed Auth field) + Attributes
    pre_image = packet_without_auth[:4] + request_authenticator + packet_without_auth[20:] + shared_secret
    return hashlib.md5(pre_image).digest()

SHARED_SECRET = b"testing123"

<start> ::= <exchange_normal> | <exchange_challenge>

# Normal Authentication
<exchange_normal> ::= <Client:access_request_initial> <Server:access_accept_reject>

# Challenge-Response Authentication
<exchange_challenge> ::= <Client:access_request_initial> <Server:access_challenge> <Client:access_request_challenge> <Server:access_accept_reject>

<access_accept_reject> ::= <access_accept> | <access_reject>

# RADIUS Packet: Code(1), ID(1), Length(2), Authenticator(16), Attributes(...)
<access_request_initial> ::= <code_request> <id> <length> <request_authenticator> <attributes_request_initial>
<access_request_challenge> ::= <code_request> <id> <length> <request_authenticator> <attributes_request_challenge>
<access_accept> ::= <code_accept> <id> <length> <response_authenticator> <attributes_response>
<access_reject> ::= <code_reject> <id> <length> <response_authenticator> <attributes_response>
<access_challenge> ::= <code_challenge> <id> <length> <response_authenticator> <attributes_challenge>

<code_request> ::= 0 0 0 0 0 0 0 1 := pack("B", 1)
<code_accept> ::= 0 0 0 0 0 0 1 0 := pack("B", 2)
<code_reject> ::= 0 0 0 0 0 0 1 1 := pack("B", 3)
<code_challenge> ::= 0 0 0 0 1 0 1 1 := pack("B", 11)

<id> ::= <byte>
<length> ::= <byte>{2}
<request_authenticator> ::= <byte>{16} := gen_authenticator()
<response_authenticator> ::= <byte>{16}

# Attributes
<attributes_request_initial> ::= <attr_user_name> <attr_user_password> <attr_nas_ip>?
<attributes_request_challenge> ::= <attr_user_name> <attr_user_password> <attr_state> <attr_nas_ip>?
<attributes_response> ::= <attr_reply_message>*
<attributes_challenge> ::= <attr_reply_message>* <attr_state>

<attr_user_name> ::= 0 0 0 0 0 0 0 1 <attr_len> <attr_val_user_name>
<attr_user_password> ::= 0 0 0 0 0 0 1 0 <attr_len> <attr_val_user_password>
<attr_nas_ip> ::= 0 0 0 0 0 1 0 0 0 0 0 0 0 1 1 0 <byte>{4}
<attr_reply_message> ::= 0 0 0 1 0 0 1 0 <attr_len> <byte>{int(bytes(<attr_len>)[0])-2}
<attr_state> ::= 0 0 0 1 1 0 0 0 <attr_len> <byte>{int(bytes(<attr_len>)[0])-2}

<attr_len> ::= <byte>

<attr_val_user_name> ::= "username" | "challengeuser"
<attr_val_user_password> ::= <byte>{16, 128}

<byte> ::= <bit>{8}
<bit> ::= 0 | 1

# Constraints

# 1. Length field must match packet length
where forall <p> in <access_request_initial>:
    bytes(<p>.<length>) == pack(">H", len(bytes(<p>)))
where forall <p> in <access_request_challenge>:
    bytes(<p>.<length>) == pack(">H", len(bytes(<p>)))
where forall <p> in <access_accept>:
    bytes(<p>.<length>) == pack(">H", len(bytes(<p>)))
where forall <p> in <access_reject>:
    bytes(<p>.<length>) == pack(">H", len(bytes(<p>)))
where forall <p> in <access_challenge>:
    bytes(<p>.<length>) == pack(">H", len(bytes(<p>)))


# 2. Attribute length must match attribute content
where forall <a> in <attr_user_name>:
    bytes(<a>.<attr_len>) == pack("B", len(bytes(<a>)))
where forall <a> in <attr_user_password>:
    bytes(<a>.<attr_len>) == pack("B", len(bytes(<a>)))
where forall <a> in <attr_reply_message>:
    bytes(<a>.<attr_len>) == pack("B", len(bytes(<a>)))
where forall <a> in <attr_state>:
    bytes(<a>.<attr_len>) == pack("B", len(bytes(<a>)))

# 3. ID must match in exchange
where forall <ex> in <exchange_normal>:
    <ex>.<access_accept_reject>.<id> == <ex>.<access_request_initial>.<id>

where forall <ex> in <exchange_challenge>:
    <ex>.<access_challenge>.<id> == <ex>.<access_request_initial>.<id> and \
    <ex>.<access_request_challenge>.<id> == pack("B", (int(bytes(<ex>.<access_request_initial>.<id>)[0]) + 1) % 256) and \
    <ex>.<access_accept_reject>.<id> == <ex>.<access_request_challenge>.<id>

# 4. Response Authenticator verification
where forall <ex> in <exchange_normal>:
    bytes(<ex>.<access_accept_reject>.<response_authenticator>) == calc_response_authenticator(bytes(<ex>.<access_accept_reject>), bytes(<ex>.<access_request_initial>.<request_authenticator>), SHARED_SECRET)

where forall <ex> in <exchange_challenge>:
    bytes(<ex>.<access_challenge>.<response_authenticator>) == calc_response_authenticator(bytes(<ex>.<access_challenge>), bytes(<ex>.<access_request_initial>.<request_authenticator>), SHARED_SECRET) and \
    bytes(<ex>.<access_accept_reject>.<response_authenticator>) == calc_response_authenticator(bytes(<ex>.<access_accept_reject>), bytes(<ex>.<access_request_challenge>.<request_authenticator>), SHARED_SECRET)

# 5. User-Password encoding
where forall <ex> in <exchange_normal>:
    if bytes(<ex>.<access_request_initial>.<attributes_request_initial>.<attr_user_name>.<attr_val_user_name>) == b"username":
        bytes(<ex>.<access_request_initial>.<attributes_request_initial>.<attr_user_password>.<attr_val_user_password>) == radius_user_password(b"password", SHARED_SECRET, bytes(<ex>.<access_request_initial>.<request_authenticator>))

where forall <ex> in <exchange_challenge>:
    if bytes(<ex>.<access_request_initial>.<attributes_request_initial>.<attr_user_name>.<attr_val_user_name>) == b"challengeuser":
        bytes(<ex>.<access_request_initial>.<attributes_request_initial>.<attr_user_password>.<attr_val_user_password>) == radius_user_password(b"test123", SHARED_SECRET, bytes(<ex>.<access_request_initial>.<request_authenticator>)) and \
        bytes(<ex>.<access_request_challenge>.<attributes_request_challenge>.<attr_user_password>.<attr_val_user_password>) == radius_user_password(b"test123", SHARED_SECRET, bytes(<ex>.<access_request_challenge>.<request_authenticator>))

# 6. State handling in Challenge-Response
where forall <ex> in <exchange_challenge>:
    bytes(<ex>.<access_request_challenge>.<attributes_request_challenge>.<attr_state>) == bytes(<ex>.<access_challenge>.<attributes_challenge>.<attr_state>)


class RADIUSParty(NetworkParty):
    def send(self, message, recipient):
        if isinstance(message, DerivationTree):
            message = message.to_bytes()
        super().send(message, recipient)

class Client(RADIUSParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.CONNECT,
            uri="udp://127.0.0.1:1812"
        )
        self.start()

class Server(RADIUSParty):
    def __init__(self):
        super().__init__(
            connection_mode=ConnectionMode.EXTERNAL,
            uri="udp://127.0.0.1:1812"
        )
        self.start()
