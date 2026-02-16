# ==========================================
# PNG specification with constructive IDAT
# ==========================================

import struct
import zlib
import math
import random

# ------------------------------------------
# Helpers
# ------------------------------------------

def to_u32(bs: bytes) -> int:
    """
    Convert a sequence of 4 bytes (big-endian) into
    an unsigned 32-bit integer.

    Args:
        bs (list[int] or bytes): Exactly 4 bytes.

    Returns:
        int: Parsed unsigned integer.
    """
    return struct.unpack(">I", bytes(bs))[0]


def from_u32(n: int) -> bytes:
    """
    Convert an integer into a 4-byte big-endian list.

    Args:
        n (int): Integer in range [0, 2^32-1].

    Returns:
        bytes: 4-byte big-endian representation.
    """
    return bytes(struct.pack(">I", n))


def crc(t: bytes, d: bytes) -> bytes:
    """
    Compute the PNG CRC field for a chunk.

    Args:
        t (bytes): 4-byte chunk type.
        d (bytes): Chunk payload.

    Returns:
        bytes: 4-byte big-endian CRC.
    """
    return from_u32(zlib.crc32(bytes(t + d)) & 0xffffffff)


def valid_ihdr(bitdepth: int, colortype: int) -> bool:
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


def channels(colortype: int) -> int:
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


def scanline_size(width: int, bitdepth: int, colortype: int) -> int:
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


def generate_scanlines(width: int, height: int, bitdepth: int, colortype: int) -> bytes:
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
        bytes: Raw uncompressed image bytes.
    """
    size = scanline_size(width, bitdepth, colortype)
    raw = []
    for _ in range(height):
        filter_type = random.randint(0,4)
        raw.append(filter_type)
        raw.extend(random.randint(0,255) for _ in range(size))
    return bytes(raw)


def generate_idat(width: int, height: int, bitdepth: int,
                  colortype: int) -> bytes:
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
        bytes: Full IDAT chunk bytes including:
            length || 'IDAT' || compressed_data || crc
    """
    raw = generate_scanlines(width, height, bitdepth, colortype)
    compressed = bytes(list(zlib.compress(bytes(raw))))
    length = from_u32(len(compressed))
    crc_value = crc(b'IDAT', bytes(compressed))
    return bytes(length + b'IDAT' + compressed + crc_value)

# ------------------------------------------
# Basic terminals
# ------------------------------------------

<uint32> ::= <byte>{4}

# ------------------------------------------
# PNG signature
# ------------------------------------------

# <signature> ::= b'\x89PNG\r\n\x1a\n'
<signature> ::= b'\211PNG\r\n\032\n'

# ------------------------------------------
# IHDR
# ------------------------------------------

<ihdr> ::= <len_ihdr> b'IHDR' <ihdr_body> <ihdr_crc>

<len_ihdr> ::= <uint32>
where <len_ihdr> == from_u32(len(bytes(<ihdr_body>)))

<ihdr_crc> ::= <uint32>
where <ihdr_crc> == crc(b'IHDR', bytes(<ihdr_body>))

<ihdr_body> ::= (
    <width>
    <height>
    <bitdepth>
    <colortype>
    b'\x00'     # compression - (deflate/inflate compression with a 32K sliding window)
    b'\x00'     # filter
    <interlace>)

<width> ::= <uint32>
where 1 <= to_u32(<width>) <= 32

<height> ::= <uint32>
where 1 <= to_u32(<height>) <= 32

# We fix width and height to 1 to avoid generating huge IDAT data.
where <width> == from_u32(1)
where <height> == from_u32(1)

<bitdepth> ::= b'\x08' | b'\x10'

<colortype> ::= b'\x02' | b'\x06'

<interlace> ::= b'\x00'

# Note: ord(b'\x02') == 2
where valid_ihdr(ord(bytes(<bitdepth>)), ord(bytes(<colortype>)))


# ------------------------------------------
# PLTE (optional)
# ------------------------------------------

<plte> ::= <len_plte> b'PLTE' <plte_data> <plte_crc>
where to_u32(<len_plte>) % 3 == 0
where <len_plte> == from_u32(len(bytes(<plte_data>)))
where <plte_crc> == crc(b'PLTE', bytes(<plte_data>))

<plte_data> ::= <byte>*
<len_plte> ::= <uint32>
<plte_crc> ::= <uint32>

# ------------------------------------------
# Custom IDAT generator
# ------------------------------------------

<idat> ::= <generated_idat>

<generated_idat> ::= <len_idat> b'IDAT' <idat_data> <idat_crc> := generate_idat(
        1, # to_u32(<width>),
        1, # to_u32(<height>),
        1, # <bitdepth>[0],
        0, # <colortype>[0]
    )

<len_idat> ::= <uint32>
<idat_crc> ::= <uint32>
<idat_data> ::= <byte>*

# where to_u32(<len_idat>) % 3 == 0
where <len_idat> == from_u32(len(bytes(<idat_data>)))
where <idat_crc> == crc(b'IDAT', bytes(<idat_data>))

# ------------------------------------------
# IEND
# ------------------------------------------

# <iend> ::= b'\x00\x00\x00\x00IEND\xaeB`\x82'
<iend> ::= <len_iend> b'IEND' <iend_crc>
where <len_iend> == from_u32(0)
where <iend_crc> == crc(b'IEND', b'')

<len_iend> ::= <uint32>
<iend_crc> ::= <uint32>


# ------------------------------------------
# Top-level PNG
# ------------------------------------------

<start> ::= (
    <signature>
    <ihdr>
    # <plte>?
    <idat>
    <iend>
)