# ==========================================
# PNG specification with constructive IDAT
# ==========================================

:import struct
:import zlib
:import math
:import random

# ------------------------------------------
# Helpers
# ------------------------------------------

def to_u32(bs):
    """
    Convert a sequence of 4 bytes (big-endian) into
    an unsigned 32-bit integer.

    Args:
        bs (list[int] or bytes): Exactly 4 bytes.

    Returns:
        int: Parsed unsigned integer.
    """
    return struct.unpack(">I", bytes(bs))[0]


def from_u32(n):
    """
    Convert an integer into a 4-byte big-endian list.

    Args:
        n (int): Integer in range [0, 2^32-1].

    Returns:
        list[int]: 4-byte big-endian representation.
    """
    return list(struct.pack(">I", n))


def crc_ok(t, d, c):
    """
    Verify that a PNG chunk CRC is correct.

    The CRC is computed over:
        chunk_type || chunk_data

    Args:
        t (list[int]): 4-byte chunk type.
        d (list[int]): Chunk payload.
        c (list[int]): 4-byte CRC field.

    Returns:
        bool: True if CRC matches PNG specification.
    """
    return (zlib.crc32(bytes(t + d)) & 0xffffffff) == to_u32(c)


def crc_bytes(t, d):
    """
    Compute the PNG CRC field for a chunk.

    Args:
        t (bytes or list[int]): 4-byte chunk type.
        d (list[int]): Chunk payload.

    Returns:
        list[int]: 4-byte big-endian CRC.
    """
    return from_u32(zlib.crc32(bytes(t + d)) & 0xffffffff)


def valid_ihdr(bitdepth, colortype):
    """
    Check whether a (bitdepth, colortype) combination
    is valid according to the PNG specification.

    PNG allows only certain combinations, e.g.:
        ColorType 2 (RGB) supports 8 or 16 bits.

    Args:
        bitdepth (int)
        colortype (int)

    Returns:
        bool: True if combination is legal.
    """
    valid = {
        0: {1,2,4,8,16},
        2: {8,16},
        3: {1,2,4,8},
        4: {8,16},
        6: {8,16}
    }
    return colortype in valid and bitdepth in valid[colortype]


def channels(colortype):
    """
    Return number of color channels for a PNG color type.

    Mapping:
        0 → Grayscale (1)
        2 → RGB (3)
        3 → Indexed (1)
        4 → Grayscale + Alpha (2)
        6 → RGBA (4)

    Args:
        colortype (int)

    Returns:
        int: Number of channels.
    """
    return {0:1, 2:3, 3:1, 4:2, 6:4}[colortype]


def scanline_size(width, bitdepth, colortype):
    """
    Compute number of bytes in a PNG scanline
    excluding the filter byte.

    Formula:
        ceil(width * channels * bitdepth / 8)

    Args:
        width (int)
        bitdepth (int)
        colortype (int)

    Returns:
        int: Number of pixel bytes per scanline.
    """
    bits = width * channels(colortype) * bitdepth
    return math.ceil(bits / 8)


def generate_scanlines(width, height, bitdepth, colortype):
    """
    Construct raw PNG image data (before compression).

    Each scanline consists of:
        1 filter byte (0–4)
        pixel bytes

    Filter types are randomly selected.
    Pixel bytes are uniformly random.

    Args:
        width (int)
        height (int)
        bitdepth (int)
        colortype (int)

    Returns:
        list[int]: Raw uncompressed image bytes.
    """
    size = scanline_size(width, bitdepth, colortype)
    raw = []
    for _ in range(height):
        filter_type = random.randint(0,4)
        raw.append(filter_type)
        raw.extend(random.randint(0,255) for _ in range(size))
    return raw


def generate_idat(width, height, bitdepth, colortype):
    """
    Generate a complete, valid PNG IDAT chunk.

    Steps:
        1. Generate raw scanlines
        2. Compress using zlib (DEFLATE)
        3. Compute correct chunk length
        4. Compute correct CRC

    Args:
        width (int)
        height (int)
        bitdepth (int)
        colortype (int)

    Returns:
        list[int]: Full IDAT chunk bytes including:
            length || 'IDAT' || compressed_data || crc
    """
    raw = generate_scanlines(width, height, bitdepth, colortype)
    compressed = list(zlib.compress(bytes(raw)))
    length = from_u32(len(compressed))
    crc = crc_bytes(b'IDAT', compressed)
    return length + list(b'IDAT') + compressed + crc

# ------------------------------------------
# Basic terminals
# ------------------------------------------

<byte> ::= b'.'
<uint32> ::= <byte>{4}

# ------------------------------------------
# PNG signature
# ------------------------------------------

<signature> ::= b'\x89PNG\r\n\x1a\n'

# ------------------------------------------
# IHDR
# ------------------------------------------

<ihdr> ::= <len_13> b'IHDR' <ihdr_body> <crc>
where crc_ok(b'IHDR', <ihdr_body>, <crc>)

<len_13> ::= <uint32>
where to_u32(<len_13>) == 13

<ihdr_body> ::=
    <width>
    <height>
    <bitdepth>
    <colortype>
    b'\x00'     # compression
    b'\x00'     # filter
    <interlace>

<width> ::= <uint32>
where 1 <= to_u32(<width>) <= 32

<height> ::= <uint32>
where 1 <= to_u32(<height>) <= 32

<bitdepth> ::= b'\x08' | b'\x10'

<colortype> ::= b'\x02' | b'\x06'

<interlace> ::= b'\x00'

where valid_ihdr(<bitdepth>[0], <colortype>[0])

<crc> ::= <uint32>

# ------------------------------------------
# PLTE (optional)
# ------------------------------------------

<plte> ::= <len_plte> b'PLTE' <data> <crc>
where to_u32(<len_plte>) % 3 == 0
where crc_ok(b'PLTE', <data>, <crc>)

<len_plte> ::= <uint32>

# ------------------------------------------
# Custom IDAT generator
# ------------------------------------------

<idat> ::= <generated_idat>

<generated_idat> ::=
    :python generate_idat(
        to_u32(<width>),
        to_u32(<height>),
        <bitdepth>[0],
        <colortype>[0]
    )

# ------------------------------------------
# IEND
# ------------------------------------------

<iend> ::= b'\x00\x00\x00\x00IEND\xaeB`\x82'

# ------------------------------------------
# Top-level PNG
# ------------------------------------------

<start> ::=
    <signature>
    <ihdr>
    <plte>?
    <idat>
    <iend>
