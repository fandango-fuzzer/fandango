import struct
import time
from hashlib import blake2s
from typing import Optional

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from fandango.io import ConnectionMode, NetworkParty
from fandango.language import DerivationTree, NonTerminal

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
        self, message: DerivationTree | str | bytes, recipient: Optional[str] = None
    ) -> None:
        increment_sending_key_counter()
        super().send(message, recipient)


class Server(NetworkParty):
    def __init__(self):
        super().__init__(
            "udp://localhost:51820",
            connection_mode=ConnectionMode.EXTERNAL,
        )
        self.start()

    def receive(self, message: bytes | str | None, sender: Optional[str]) -> None:
        # msg_responder: type(1)=0x02, reserved(3), sender_index at 4..8, ephemeral at 12..44
        if isinstance(message, bytes) and len(message) >= 44 and message[0] == 0x02:
            set_responder_sender_index(message[4:8])
            set_responder_ephemeral(message[12:44])
        super().receive(message, sender)


def get_session_sending_key() -> bytes:
    return session_sending_key


def get_session_receiving_key() -> bytes:
    return session_receiving_key


def get_unencrypted_ephemeral() -> bytes:
    return unencrypted_ephemeral


def get_responder_ephemeral() -> bytes:
    return responder_ephemeral_public


def set_responder_ephemeral(data: bytes) -> None:
    global responder_ephemeral_public
    responder_ephemeral_public = data


def get_responder_sender_index() -> bytes:
    return responder_sender_index


def set_responder_sender_index(data: bytes) -> None:
    global responder_sender_index
    responder_sender_index = data


def get_sending_key_counter() -> int:
    return sending_key_counter


def get_sending_key_counter_as_bytes() -> bytes:
    return struct.pack("<Q", sending_key_counter)


def get_receiving_key_counter() -> int:
    return receiving_key_counter


def get_receiving_key_counter_as_bytes() -> bytes:
    return struct.pack("<Q", receiving_key_counter)


def increment_sending_key_counter() -> None:
    global sending_key_counter
    sending_key_counter += 1


def increment_receiving_key_counter() -> None:
    global receiving_key_counter
    receiving_key_counter += 1


def get_tai_64n() -> bytes:
    return tai_64n


def TAI64N() -> bytes:
    t = time.time()
    secs = int(t) + 0x400000000000000A
    nanos = int((t - int(t)) * 1e9)
    global tai_64n
    tai_64n = struct.pack(">Q", secs) + struct.pack(">I", nanos)
    return tai_64n


def MAC(key: bytes, data: bytes) -> bytes:
    return blake2s(data, key=key, digest_size=16).digest()


def DH(private: x25519.X25519PrivateKey, public: x25519.X25519PublicKey) -> bytes:
    return private.exchange(public)


def AEAD(key: bytes, nonce: int | bytes, plaintext: bytes, ad: bytes) -> bytes:
    if isinstance(nonce, int):
        nonce = b"\x00" * 4 + struct.pack("<Q", nonce)
    return ChaCha20Poly1305(key).encrypt(nonce, plaintext, ad)


def HASH(data: bytes) -> bytes:
    return blake2s(data, digest_size=32).digest()


def HMAC_blake2s(key: bytes, data: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.BLAKE2s(32))
    h.update(data)
    return h.finalize()


def AEAD_decrypt(key: bytes, nonce: int | bytes, ciphertext: bytes, ad: bytes) -> bytes:
    if isinstance(nonce, int):
        nonce = b"\x00" * 4 + struct.pack("<Q", nonce)
    return ChaCha20Poly1305(key).decrypt(nonce, ciphertext, ad)


def create_handshake_initiation_full(
    initiator_static_private,
    initiator_ephemeral_private,
    responder_static_public,
    timestamp64n,
):
    """
    Pure function. Returns (msg_bytes, final_chaining_key, final_hash).
    No side effects — safe to call multiple times with the same inputs.
    """
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


def create_handshake_initiation(
    initiator_static_private,
    initiator_ephemeral_private,
    responder_static_public,
    timestamp64n,
):
    """Thin wrapper for the grammar constraint — returns only the message bytes."""
    msg, _, _ = create_handshake_initiation_full(
        initiator_static_private,
        initiator_ephemeral_private,
        responder_static_public,
        timestamp64n,
    )
    return msg


def initiator_mac_1(
    msg: bytes, responder_static_public: x25519.X25519PublicKey
) -> bytes:
    mac1_key = HASH(LABEL_MAC1 + responder_static_public.public_bytes_raw())
    mac1 = MAC(mac1_key, msg)
    return mac1


def derive_session_keys(
    initiator_static_private,
    initiator_ephemeral_private,
    responder_static_public,
    timestamp64n,
    resp_ephemeral_bytes: bytes,
    psk: bytes = b"\x00" * 32,
):
    """
    Derives WireGuard session keys following Noise_IKpsk2 (WireGuard paper §5.4.4).

    Recomputes the initiator's chaining key from scratch, then mirrors the
    responder's operations: mix in the responder's ephemeral, two DH results,
    and the PSK via KDF3.  Returns (sending_key, receiving_key) and updates
    the session-key globals.
    """
    # Reproduce chaining key and hash at end of the initiation message
    _, ck, h = create_handshake_initiation_full(
        initiator_static_private,
        initiator_ephemeral_private,
        responder_static_public,
        timestamp64n,
    )

    resp_eph_pub = x25519.X25519PublicKey.from_public_bytes(resp_ephemeral_bytes)

    # KDF1(C, e_r_pub): mix responder's ephemeral into chaining key and hash
    h = HASH(h + resp_ephemeral_bytes)
    temp = HMAC_blake2s(ck, resp_ephemeral_bytes)
    ck = HMAC_blake2s(temp, b"\x01")

    # KDF1(C, DH(e_i, e_r))
    dh1 = DH(initiator_ephemeral_private, resp_eph_pub)
    temp = HMAC_blake2s(ck, dh1)
    ck = HMAC_blake2s(temp, b"\x01")

    # KDF1(C, DH(s_i, e_r))
    dh2 = DH(initiator_static_private, resp_eph_pub)
    temp = HMAC_blake2s(ck, dh2)
    ck = HMAC_blake2s(temp, b"\x01")

    # KDF3(C, PSK) → (new_C, tau, k_psk)  — the "psk2" step of Noise_IKpsk2
    temp = HMAC_blake2s(ck, psk)
    ck = HMAC_blake2s(temp, b"\x01")
    tau = HMAC_blake2s(temp, ck + b"\x02")
    # k_psk = HMAC_blake2s(temp, tau + b'\x03')  # used by responder for AEAD, not needed here
    h = HASH(h + tau)

    # KDF2(C, ε) → (T_send, T_recv)
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


def encrypt_transport(
    sending_key: bytes, counter_bytes: bytes, plaintext: bytes = b""
) -> bytes:
    """
    Pure function. Encrypts a transport payload (default: empty = keepalive).
    Plaintext is zero-padded to a multiple of 16 before encryption.
    """
    # plaintext = b''
    pad_len = (16 - len(plaintext) % 16) % 16
    padded = plaintext + b"\x00" * pad_len
    counter = struct.unpack("<Q", counter_bytes)[0]
    return AEAD(sending_key, counter, padded, b"")


def decrypt_transport(key, counter_bytes, ciphertext):
    counter = struct.unpack("<Q", counter_bytes)[0]
    padded = AEAD_decrypt(key, counter, ciphertext, b"")
    return padded.rstrip(b"\x00")


def count_data_packets(packet_nt):
    return len(
        packet_nt.prefix()
        .get_root()
        .find_all_nodes(NonTerminal("<data_counter>"), exclude_read_only=False)
    )


def generate_udp_checksum(udp_packet_tree: DerivationTree):
    data = bytearray(bytes(udp_packet_tree))
    data[6] = 0
    data[7] = 0

    if len(data) % 2 == 1:
        data.append(0)
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF
    if checksum == 0:
        checksum = 0xFFFF
    return checksum.to_bytes(2, byteorder="big")


def encrypt_cookie(
    nonce: DerivationTree, unencrypted_cookie: DerivationTree, responder_static_public
) -> bytes:
    tau = HASH(LABEL_COOKIE + responder_static_public.public_bytes_raw())
    encrypted_cookie = AEAD(
        tau, bytes(nonce), bytes(unencrypted_cookie), b"LAST_RECEIVED_MSG__MAC_1"
    )
    return encrypted_cookie


def decrypt_cookie(cookie_reply: DerivationTree, responder_static_public) -> bytes:
    nonce = bytes(cookie_reply)[:24]
    ciphertext = bytes(cookie_reply)[24:]
    tau = HASH(LABEL_COOKIE + responder_static_public.public_bytes_raw())
    return AEAD_decrypt(tau, nonce, ciphertext, b"LAST_RECEIVED_MSG__MAC_1")


def extract_cookie_nonce(cookie_reply: DerivationTree) -> bytes:
    return bytes(cookie_reply)[:24]


def generate_cookie() -> bytes:
    client = Client.instance()
    assert isinstance(client, NetworkParty)
    initiator_ip = client.ip
    assert initiator_ip is not None
    responder_changing_secret_every_two_minutes = b"CHANGE_ME"  # TODO
    return MAC(responder_changing_secret_every_two_minutes, initiator_ip.encode())
