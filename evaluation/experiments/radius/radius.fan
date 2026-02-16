import hashlib

def radius_user_password(password: bytes,
                         shared_secret: bytes,
                         request_authenticator: bytes) -> bytes:
    """
    Encode RADIUS User-Password attribute value (RFC 2865).
    """
    if len(request_authenticator) != 16:
        raise ValueError("Request Authenticator must be 16 bytes")

    # RFC limit: String field is 16..128 octets
    MAX_STRING_LEN = 128
    # Pad to multiple of 16
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
        # bi = MD5(S + prev)
        bi = hashlib.md5(shared_secret + prev).digest()
        # ci = pi XOR bi
        ci = bytes(a ^ b for a, b in zip(block, bi))
        result += ci
        prev = ci

    return result