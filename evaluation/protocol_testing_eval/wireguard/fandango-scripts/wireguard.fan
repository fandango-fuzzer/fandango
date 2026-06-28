# 10 LOC
import base64
import struct
import time
from hashlib import blake2s
from typing import Optional

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from fandango.io import ConnectionMode, NetworkParty
from fandango.language import DerivationTree

# 21 LOC
FAST_TIMERS = False

if FAST_TIMERS:
    REKEY_TIMEOUT_SECONDS         = 3
    KEEPALIVE_SECONDS             = 6
    NEW_HANDSHAKE_TIMEOUT_SECONDS = KEEPALIVE_SECONDS + REKEY_TIMEOUT_SECONDS  # = 9
    REKEY_ATTEMPT_TIME_SECONDS    = 12
    REKEY_AFTER_TIME_SECONDS      = 15
    REJECT_AFTER_TIME_SECONDS     = 18
else:
    KEEPALIVE_SECONDS             = 10   # Keepalive-Timeout
    REKEY_AFTER_TIME_SECONDS      = 120  # Rekey-After-Time
    REJECT_AFTER_TIME_SECONDS     = 180  # Reject-After-Time
    REKEY_ATTEMPT_TIME_SECONDS    = 90   # Rekey-Attempt-Time
    REKEY_TIMEOUT_SECONDS         = 5    # Rekey-Timeout
    NEW_HANDSHAKE_TIMEOUT_SECONDS = KEEPALIVE_SECONDS + REKEY_TIMEOUT_SECONDS  # = 15

# Timer IDs
TIMER_ID_KEEPALIVE         = 1
TIMER_ID_REKEY_AFTER_TIME  = 2
TIMER_ID_REJECT_AFTER_TIME = 3
TIMER_ID_REKEY_TIMEOUT     = 4
TIMER_ID_REKEY_ATTEMPT     = 5
TIMER_ID_NEW_HANDSHAKE     = 6

# 16 LOC
CONSTRUCTION = b"Noise_IKpsk2_25519_ChaChaPoly_BLAKE2s"
IDENTIFIER = b"WireGuard v1 zx2c4 Jason@zx2c4.com"
LABEL_MAC1 = b"mac1----"
LABEL_COOKIE = b"cookie--"

unencrypted_ephemeral = b"\x00"
# Responder's ephemeral public key extracted from the received handshake response.
responder_ephemeral_public: bytes = (
    x25519.X25519PrivateKey.from_private_bytes(b"\x01" * 32)
    .public_key()
    .public_bytes_raw()
)
tai_64n = b""
responder_sender_index: bytes = b"\x00" * 4

session_sending_key = b"\x00" * 32
session_receiving_key = b"\x00" * 32
sending_key_counter = 0
receiving_key_counter = 0

# 15 LOC
class Client(NetworkParty):
    def __init__(self):
        super().__init__(
            "udp://localhost:51820",
            connection_mode=ConnectionMode.CONNECT,
        )
        self.start()

    def receive(self, message: str | bytes | None, sender: Optional[str]) -> None:
        increment_receiving_key_counter()
        super().receive(message, "Server")

    def send(
        self, message: DerivationTree | str | bytes, recipient: Optional[str]
    ) -> None:
        increment_sending_key_counter()
        super().send(message, recipient)

# 7 LOC
class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            "udp://localhost:51820",
            connection_mode=ConnectionMode.EXTERNAL,
        )
        self.start()

# 2 LOC
def get_session_sending_key() -> bytes:
    return session_sending_key

# 2 LOC
def get_responder_ephemeral() -> bytes:
    return responder_ephemeral_public

# 3 LOC
def set_responder_ephemeral(data: bytes) -> None:
    global responder_ephemeral_public
    responder_ephemeral_public = data

# 2 LOC
def get_responder_sender_index() -> bytes:
    return responder_sender_index

# 3 LOC
def set_responder_sender_index(data: bytes) -> None:
    global responder_sender_index
    responder_sender_index = data

# 2 LOC
def get_sending_key_counter_as_bytes() -> bytes:
    return struct.pack("<Q", sending_key_counter)

# 3 LOC
def increment_sending_key_counter() -> None:
    global sending_key_counter
    sending_key_counter += 1

# 3 LOC
def increment_receiving_key_counter() -> None:
    global receiving_key_counter
    receiving_key_counter += 1

# 2 LOC
def get_tai_64n() -> bytes:
    return tai_64n

# 7 LOC
def TAI64N() -> bytes:
    t = time.time()
    secs = int(t) + 0x400000000000000A
    nanos = int((t - int(t)) * 1e9)
    global tai_64n
    tai_64n = struct.pack(">Q", secs) + struct.pack(">I", nanos)
    return tai_64n

# 2 LOC
def MAC(key: bytes, data: bytes) -> bytes:
    return blake2s(data, key=key, digest_size=16).digest()

# 2 LOC
def DH(private: x25519.X25519PrivateKey, public: x25519.X25519PublicKey) -> bytes:
    return private.exchange(public)

# 4 LOC
def AEAD(key: bytes, nonce: int | bytes, plaintext: bytes, ad: bytes) -> bytes:
    if isinstance(nonce, int):
        nonce = b"\x00" * 4 + struct.pack("<Q", nonce)
    return ChaCha20Poly1305(key).encrypt(nonce, plaintext, ad)

# 2 LOC
def HASH(data: bytes) -> bytes:
    return blake2s(data, digest_size=32).digest()

# 4 LOC
def HMAC_blake2s(key: bytes, data: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.BLAKE2s(32))
    h.update(data)
    return h.finalize()

# 34 LOC
def create_handshake_initiation_full(
    initiator_static_private,
    initiator_ephemeral_private,
    responder_static_public,
    timestamp64n,
):
    chaining_key = HASH(CONSTRUCTION)
    hash_ = HASH(
        HASH(chaining_key + IDENTIFIER) + responder_static_public.public_bytes_raw()
    )

    ephemeral_public = initiator_ephemeral_private.public_key().public_bytes_raw()
    hash_ = HASH(hash_ + ephemeral_public)

    temp = HMAC_blake2s(chaining_key, ephemeral_public)
    chaining_key = HMAC_blake2s(temp, b"\x01")

    dh1 = DH(initiator_ephemeral_private, responder_static_public)
    temp = HMAC_blake2s(chaining_key, dh1)
    chaining_key = HMAC_blake2s(temp, b"\x01")
    key = HMAC_blake2s(temp, chaining_key + b"\x02")

    static_public = initiator_static_private.public_key().public_bytes_raw()
    encrypted_static = AEAD(key, 0, static_public, hash_)
    hash_ = HASH(hash_ + encrypted_static)

    dh2 = DH(initiator_static_private, responder_static_public)
    temp = HMAC_blake2s(chaining_key, dh2)
    chaining_key = HMAC_blake2s(temp, b"\x01")
    key = HMAC_blake2s(temp, chaining_key + b"\x02")

    encrypted_timestamp = AEAD(key, 0, timestamp64n, hash_)
    hash_ = HASH(hash_ + encrypted_timestamp)

    msg = b""
    msg += ephemeral_public
    msg += encrypted_static
    msg += encrypted_timestamp
    global unencrypted_ephemeral
    unencrypted_ephemeral = ephemeral_public

    return msg, chaining_key, hash_

# 13 LOC
def create_handshake_initiation(
    initiator_static_private,
    initiator_ephemeral_private,
    responder_static_public,
    timestamp64n,
):
    msg, _, _ = create_handshake_initiation_full(
        initiator_static_private,
        initiator_ephemeral_private,
        responder_static_public,
        timestamp64n,
    )
    return msg

# 6 LOC
def initiator_mac_1(
    msg: bytes, responder_static_public: x25519.X25519PublicKey
) -> bytes:
    mac1_key = HASH(LABEL_MAC1 + responder_static_public.public_bytes_raw())
    mac1 = MAC(mac1_key, msg)
    return mac1

# 40 LOC
def derive_session_keys(
    initiator_static_private,
    initiator_ephemeral_private,
    responder_static_public,
    timestamp64n,
    resp_ephemeral_bytes: bytes,
    psk: bytes,
):
    if psk is None:
        psk = b"\x00" * 32
    _, ck, h = create_handshake_initiation_full(
        initiator_static_private,
        initiator_ephemeral_private,
        responder_static_public,
        timestamp64n,
    )

    resp_eph_pub = x25519.X25519PublicKey.from_public_bytes(resp_ephemeral_bytes)

    h = HASH(h + resp_ephemeral_bytes)
    temp = HMAC_blake2s(ck, resp_ephemeral_bytes)
    ck = HMAC_blake2s(temp, b"\x01")

    dh1 = DH(initiator_ephemeral_private, resp_eph_pub)
    temp = HMAC_blake2s(ck, dh1)
    ck = HMAC_blake2s(temp, b"\x01")

    dh2 = DH(initiator_static_private, resp_eph_pub)
    temp = HMAC_blake2s(ck, dh2)
    ck = HMAC_blake2s(temp, b"\x01")

    temp = HMAC_blake2s(ck, psk)
    ck = HMAC_blake2s(temp, b"\x01")
    tau = HMAC_blake2s(temp, ck + b"\x02")
    h = HASH(h + tau)

    temp1 = HMAC_blake2s(ck, b"")
    temp2 = HMAC_blake2s(temp1, b"\x01")
    temp3 = HMAC_blake2s(temp1, temp2 + b"\x02")
    sending_key = temp2
    receiving_key = temp3

    global session_sending_key, session_receiving_key
    session_sending_key = sending_key
    session_receiving_key = receiving_key

    global sending_key_counter, receiving_key_counter
    sending_key_counter = 0
    receiving_key_counter = 0

    return sending_key, receiving_key

# 7 LOC
def encrypt_transport(
    sending_key: bytes, counter_bytes: bytes, plaintext: bytes
) -> bytes:
    if plaintext is None:
        plaintext = b""
    pad_len = (16 - len(plaintext) % 16) % 16
    padded = plaintext + b"\x00" * pad_len
    counter = struct.unpack("<Q", counter_bytes)[0]
    return AEAD(sending_key, counter, padded, b"")





initiator_static_private = x25519.X25519PrivateKey.from_private_bytes(
    base64.b64decode("2HfMsoxG4PsoK4mrH4obxS42sBJcBivXJKDZZoTp/U8=")
)
PRESHARED_KEY = base64.b64decode("Mre8QycOhWQE0tMVayZT8bfQc8l045CPFCbO/2Mczoo=")
initiator_ephemeral_private = x25519.X25519PrivateKey.from_private_bytes(
    b'\xd8w\xcc\xb2\x8cF\xe0\xfb(+\x89\xab\x1f\x8a\x1b\xc5.6\xb0\x12\\\x06+\xd7$\xa0\xd9f\x84\xe9\xfdO'
)
responder_static_public = x25519.X25519PublicKey.from_public_bytes(
    base64.b64decode("Ui+tZoBJP6gufK/8oppEoHzcl1AdtihQQH4eWMs+Hm4=")
)


def capture_responder_handshake(sender_index, ephemeral) -> bool:
    set_responder_sender_index(bytes(sender_index))
    set_responder_ephemeral(bytes(ephemeral))
    return True


def generate_icmp_checksum(icmp_packet_tree) -> bytes:
    data = bytearray(bytes(icmp_packet_tree))
    data[2] = 0
    data[3] = 0
    if len(data) % 2 == 1:
        data.append(0)
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF
    return checksum.to_bytes(2, byteorder="big")



<start> ::= <handshake_with_retransmit>

<handshake_with_retransmit> ::= \
    <TimerControl:rekey_attempt_start> <handshake_attempt>

<handshake_attempt> ::= \
    <area_msg_initiator> [[ <TimerControl:rekey_timeout_start> <await_handshake_response> ]]

<await_handshake_response> ::= \
    <area_msg_responder> <post_response> \
  | <TimerEvent:rekey_timeout_expired> <handshake_attempt> \
  | <TimerEvent:rekey_attempt_expired> <TimerControl:rekey_timeout_cancel> \
  | <Server:cookie_reply> <await_handshake_response>

<post_response> ::= <TimerControl:rekey_timeout_cancel> <TimerControl:rekey_attempt_cancel> <session_phase>

<session_phase> ::= \
    <area_derive_msg_key> \
    <TimerControl:rekey_after_time_start> \
    <TimerControl:reject_after_time_start> \
    <Client:transport_data> \
    [[ <TimerControl:keepalive_cancel> <TimerControl:new_handshake_start> <Server:server_transport_data> ]] \
    <session_established>

<session_established> ::= \
    <Client:transport_data> [[ <TimerControl:keepalive_cancel> <TimerControl:new_handshake_start> <Server:server_transport_data> ]] <session_loop> \
  | <Server:server_transport_data> <TimerControl:new_handshake_cancel> <TimerControl:keepalive_cancel> <TimerControl:keepalive_start> <session_loop> \
  | <TimerEvent:keepalive_expired> <Client:keepalive_data> <session_loop> \
  | <TimerEvent:rekey_after_time_expired> [[ <reject_after_time_drain> <new_handshake_drain> <keepalive_drain> ]] <handshake_with_retransmit> \
  | <TimerEvent:new_handshake_expired> [[ <reject_after_time_drain> <rekey_after_time_drain> <keepalive_drain> ]] <handshake_with_retransmit> \
  | <TimerEvent:reject_after_time_expired>

<keepalive_drain>         ::= <TimerControl:keepalive_cancel>         | <TimerEvent:keepalive_expired>
<rekey_after_time_drain>  ::= <TimerControl:rekey_after_time_cancel>  | <TimerEvent:rekey_after_time_expired>
<reject_after_time_drain> ::= <TimerControl:reject_after_time_cancel> | <TimerEvent:reject_after_time_expired>
<new_handshake_drain>     ::= <TimerControl:new_handshake_cancel>     | <TimerEvent:new_handshake_expired>

<session_loop> ::= <session_established> | ""


# TIMER NONTERMINALS
<timer_start>   ::= "start: "   <timer_id> " (" <timer_timeout> ")\n"
<timer_cancel>  ::= "cancel: "  <timer_id> "\n"
<timer_expired> ::= "expired: " <timer_id> "\n"
<timer_id>      ::= <number>
<timer_timeout> ::= <digit><digit>?<digit>?
<number>        ::= r"[1-9][0-9]*"
<digit>         ::= r"[0-9]"

# 1. Keepalive (ID=1, §6.5)
<keepalive_start>   ::= <timer_start>
<keepalive_cancel>  ::= <timer_cancel>
<keepalive_expired> ::= <timer_expired>
where all(str(<env>..<keepalive_start>..<timer_timeout>) == str(KEEPALIVE_SECONDS) for <env> in *<keepalive_start>)
where all(str(<env>..<keepalive_start>..<timer_id>)      == str(TIMER_ID_KEEPALIVE)  for <env> in *<keepalive_start>)
where all(str(<env>..<keepalive_cancel>..<timer_id>)     == str(TIMER_ID_KEEPALIVE)  for <env> in *<keepalive_cancel>)
where all(str(<env>..<keepalive_expired>..<timer_id>)    == str(TIMER_ID_KEEPALIVE)  for <env> in *<keepalive_expired>)

# 2. Rekey-After-Time (ID=2, §6.2)
<rekey_after_time_start>   ::= <timer_start>
<rekey_after_time_cancel>  ::= <timer_cancel>
<rekey_after_time_expired> ::= <timer_expired>
where all(str(<env>..<rekey_after_time_start>..<timer_timeout>) == str(REKEY_AFTER_TIME_SECONDS) for <env> in *<rekey_after_time_start>)
where all(str(<env>..<rekey_after_time_start>..<timer_id>)      == str(TIMER_ID_REKEY_AFTER_TIME) for <env> in *<rekey_after_time_start>)
where all(str(<env>..<rekey_after_time_cancel>..<timer_id>)     == str(TIMER_ID_REKEY_AFTER_TIME) for <env> in *<rekey_after_time_cancel>)
where all(str(<env>..<rekey_after_time_expired>..<timer_id>)    == str(TIMER_ID_REKEY_AFTER_TIME) for <env> in *<rekey_after_time_expired>)

# 3. Reject-After-Time (ID=3, §6.2)
<reject_after_time_start>   ::= <timer_start>
<reject_after_time_cancel>  ::= <timer_cancel>
<reject_after_time_expired> ::= <timer_expired>
where all(str(<env>..<reject_after_time_start>..<timer_timeout>) == str(REJECT_AFTER_TIME_SECONDS) for <env> in *<reject_after_time_start>)
where all(str(<env>..<reject_after_time_start>..<timer_id>)      == str(TIMER_ID_REJECT_AFTER_TIME) for <env> in *<reject_after_time_start>)
where all(str(<env>..<reject_after_time_cancel>..<timer_id>)     == str(TIMER_ID_REJECT_AFTER_TIME) for <env> in *<reject_after_time_cancel>)
where all(str(<env>..<reject_after_time_expired>..<timer_id>)    == str(TIMER_ID_REJECT_AFTER_TIME) for <env> in *<reject_after_time_expired>)

# 4. Rekey-Timeout (ID=4, §6.4)
<rekey_timeout_start>   ::= <timer_start>
<rekey_timeout_cancel>  ::= <timer_cancel>
<rekey_timeout_expired> ::= <timer_expired>
where all(str(<env>..<rekey_timeout_start>..<timer_timeout>) == str(REKEY_TIMEOUT_SECONDS) for <env> in *<rekey_timeout_start>)
where all(str(<env>..<rekey_timeout_start>..<timer_id>)      == str(TIMER_ID_REKEY_TIMEOUT) for <env> in *<rekey_timeout_start>)
where all(str(<env>..<rekey_timeout_cancel>..<timer_id>)     == str(TIMER_ID_REKEY_TIMEOUT) for <env> in *<rekey_timeout_cancel>)
where all(str(<env>..<rekey_timeout_expired>..<timer_id>)    == str(TIMER_ID_REKEY_TIMEOUT) for <env> in *<rekey_timeout_expired>)

# 5. Rekey-Attempt-Time (ID=5, §6.4)
<rekey_attempt_start>   ::= <timer_start>
<rekey_attempt_cancel>  ::= <timer_cancel>
<rekey_attempt_expired> ::= <timer_expired>
where all(str(<env>..<rekey_attempt_start>..<timer_timeout>) == str(REKEY_ATTEMPT_TIME_SECONDS) for <env> in *<rekey_attempt_start>)
where all(str(<env>..<rekey_attempt_start>..<timer_id>)      == str(TIMER_ID_REKEY_ATTEMPT) for <env> in *<rekey_attempt_start>)
where all(str(<env>..<rekey_attempt_cancel>..<timer_id>)     == str(TIMER_ID_REKEY_ATTEMPT) for <env> in *<rekey_attempt_cancel>)
where all(str(<env>..<rekey_attempt_expired>..<timer_id>)    == str(TIMER_ID_REKEY_ATTEMPT) for <env> in *<rekey_attempt_expired>)

# 6. New-Handshake / dead-peer (ID=6, §6.5)
<new_handshake_start>   ::= <timer_start>
<new_handshake_cancel>  ::= <timer_cancel>
<new_handshake_expired> ::= <timer_expired>
where all(str(<env>..<new_handshake_start>..<timer_timeout>) == str(NEW_HANDSHAKE_TIMEOUT_SECONDS) for <env> in *<new_handshake_start>)
where all(str(<env>..<new_handshake_start>..<timer_id>)      == str(TIMER_ID_NEW_HANDSHAKE) for <env> in *<new_handshake_start>)
where all(str(<env>..<new_handshake_cancel>..<timer_id>)     == str(TIMER_ID_NEW_HANDSHAKE) for <env> in *<new_handshake_cancel>)
where all(str(<env>..<new_handshake_expired>..<timer_id>)    == str(TIMER_ID_NEW_HANDSHAKE) for <env> in *<new_handshake_expired>)


# HANDSHAKE MESSAGES║
<area_msg_initiator> ::= <StdOut:tai64n><Client:msg_initiator>
<tai64n> ::= <byte>{12} := TAI64N()

<msg_initiator> ::= <msg_initiator_computed_params> <mac_1> <mac_2>
<msg_initiator_computed_params> ::= <type_initiator> 0{24} <sender_index> <msg_initiator_encrypted_params>
<type_initiator> ::= 0{7}1
<sender_index> ::= <byte>{4}
<msg_initiator_encrypted_params> ::= <byte>* := create_handshake_initiation(
                    initiator_static_private, initiator_ephemeral_private,
                    responder_static_public, get_tai_64n())
<unencrypted_ephemeral> ::= <byte>{32}
<mac_1> ::= <byte>{16}
<mac_2> ::= <byte>{16}
where all(bytes(<env>..<msg_initiator>.<mac_1>) == initiator_mac_1(bytes(<env>..<msg_initiator_computed_params>),
    responder_static_public) for <env> in *<area_msg_initiator>)

<area_msg_responder> ::= <Server:msg_responder>
<msg_responder> ::= <type_responder> 0{24} <sender_index> <receiver_index> <unencrypted_ephemeral> \
                    <encrypted_nothing> <mac_1> <mac_2>
<type_responder> ::= 0{6} 1 0
<receiver_index> ::= <sender_index>
<encrypted_nothing> ::= <byte>{16}
where bytes(<msg_initiator>..<sender_index>) == bytes(<msg_responder>.<receiver_index>)
where all(capture_responder_handshake(bytes(<m>.<sender_index>), bytes(<m>.<unencrypted_ephemeral>))
          for <m> in *<msg_responder>)


<area_derive_msg_key> ::= <byte>* := derive_session_keys(
        initiator_static_private, initiator_ephemeral_private,
        responder_static_public, get_tai_64n(),
        get_responder_ephemeral(), PRESHARED_KEY)[0]


<transport_data> ::= <type_data> 0{24} <data_receiver_index> <data_counter> <transport_encrypted_payload>
<keepalive_data> ::= <type_data> 0{24} <data_receiver_index> <data_counter> <keepalive_encrypted_payload>
<transport_encrypted_payload> ::= <byte>* := encrypt_transport(
    get_session_sending_key(), get_sending_key_counter_as_bytes(), bytes(<ip_packet>))
<keepalive_encrypted_payload> ::= <byte>* := encrypt_transport(
    get_session_sending_key(), get_sending_key_counter_as_bytes(), bytes(<empty_packet>))
<type_data>             ::= 0{4} 0 1 0 0
<data_receiver_index>   ::= <byte>{4} := get_responder_sender_index()
<data_counter>          ::= <byte>{8} := get_sending_key_counter_as_bytes()

<server_transport_data> ::= <type_data> 0{24} <byte>{4} <byte>{8} <byte>*

<empty_packet> ::= b""
<ip_packet> ::= <version> <ip_header_length> <service_fields> <total_len> \
                <ip_identifier> <ip_flags> <ip_fragment_offset> <ip_ttl> \
                <ip_protocol> <ip_checksum> <ip_source_address> \
                <ip_destination_address> <ip_payload>
<version> ::=  0 1 0 0 # IPv4
<ip_header_length> ::= 0 1 0 1 # 20 bytes
<service_fields> ::= 0{8}
<total_len> ::= 0{8} 0{2} 1{4} 0{2}    # 60 = IP(20) + ICMP(40)
<ip_identifier> ::= <byte>{2}
<ip_flags> ::= 0{3}
<ip_fragment_offset> ::= 0{13}
<ip_ttl> ::= 0 1 0{6}
<ip_protocol> ::= 0{7} 1 # ICMP A ping the server answers
<ip_checksum> ::= 0{16} # Disabled
<ip_source_address> ::= 0{4} 1 0 1 0  0{4} 1 1 0 1  0{4} 1 1 0 1  0{6} 1 0 # 10.13.13.2
<ip_destination_address> ::= 0{4} 1 0 1 0  0{4} 1 1 0 1  0{4} 1 1 0 1  0{7} 1 # 10.13.13.1
<ip_payload> ::= <icmp_packet>

<icmp_packet> ::= <icmp_type> <icmp_code> <icmp_checksum> <icmp_identifier> <icmp_sequence> <icmp_data>
<icmp_type> ::= 0{4} 1 0 0 0 # type 8 = echo request
<icmp_code> ::= 0{8}
<icmp_checksum> ::= <byte>{2}
<icmp_identifier> ::= <byte>{2}
<icmp_sequence> ::= <byte>{2}
<icmp_data> ::= <byte>{32}

<byte> ::= <bit>{8}
<bit> ::= 0 | 1
where all(bytes(<i>.<icmp_checksum>) == generate_icmp_checksum(<i>) for <i> in *<icmp_packet>)

<cookie_reply> ::= <type_cookie_reply> 0{24} <byte>{4} <byte>{24} <byte>+
<type_cookie_reply> ::= 0{6} 1 1
