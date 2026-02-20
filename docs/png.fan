# png.fan
# Constructive PNG grammar for Fandango


import struct
import zlib
import binascii
import random


###############################################################################
# Constructive Helper Functions
###############################################################################

def png_signature():
    """
    Return the fixed 8-byte PNG file signature.
    """
    return bytes([137,80,78,71,13,10,26,10])


def be32(n):
    """
    Encode integer n as 4-byte big-endian.
    """
    return struct.pack(">I", n)


def crc32_chunk(chunk_type, data):
    """
    Construct PNG CRC over chunk_type + data.
    Returns 4-byte big-endian encoded CRC.
    """
    return be32(binascii.crc32(chunk_type + data) & 0xffffffff)


def ihdr_payload(width, height):
    """
    Construct a valid IHDR payload:
      - bit depth 8
      - color type 2 (truecolor)
      - compression 0
      - filter 0
      - interlace 0
    """
    return \
        be32(width) + \
        be32(height) + \
        bytes([8,2,0,0,0])


def raw_scanlines(width, height):
    """
    Construct raw scanlines using filter type 0.
    Produces random RGB pixels.
    """
    rows = []
    for _ in range(height):
        pixels = bytes(random.randint(0,255) for _ in range(width * 3))
        rows.append(bytes([0]) + pixels)
    return b"".join(rows)


def idat_payload(width, height):
    """
    Construct compressed IDAT payload.
    """
    raw = raw_scanlines(width, height)
    return zlib.compress(raw)


###############################################################################
# Grammar
###############################################################################

<start> ::= <png>

<png> ::= \
( \
    <signature> \
    <ihdr_chunk> \
    <idat_chunk> \
    <iend_chunk> \
)


###############################################################################
# PNG Signature
###############################################################################

<signature> ::= <signature_bytes>

<signature_bytes> ::= <byte>* := png_signature()


###############################################################################
# IHDR Chunk
###############################################################################

<ihdr_chunk> ::= \
( \
    <IHDR_length> \
    <IHDR_type> \
    <IHDR_data> \
    <IHDR_crc> \
)

<IHDR_type> ::= b"IHDR"

<IHDR_length> ::= <IHDR_length_bytes>

<IHDR_length_bytes> ::= <byte>* := be32(13)


<IHDR_data> ::= \
( \
    <IHDR_width> \
    <IHDR_height> \
    <IHDR_bit_depth> \
    <IHDR_color_type> \
    <IHDR_compression> \
    <IHDR_filter> \
    <IHDR_interlace> \
)

<IHDR_width> ::= <IHDR_width_bytes>

<IHDR_width_bytes> ::= <byte>* := be32(32)


<IHDR_height> ::= <IHDR_height_bytes>

<IHDR_height_bytes> ::= <byte>* := be32(32)


<IHDR_bit_depth> ::= b"\x08"

<IHDR_color_type> ::= b"\x02"

<IHDR_compression> ::= b"\x00"

<IHDR_filter> ::= b"\x00"

<IHDR_interlace> ::= b"\x00"


<IHDR_crc> ::= <IHDR_crc_bytes>

<IHDR_crc_bytes> ::= <byte>* := \
    crc32_chunk( \
        b"IHDR", \
        ihdr_payload(32,32) \
    )


###############################################################################
# IDAT Chunk
###############################################################################

<idat_chunk> ::= \
( \
    <IDAT_length> \
    <IDAT_type> \
    <IDAT_data> \
    <IDAT_crc> \
)

<IDAT_type> ::= b"IDAT"

<IDAT_data> ::= <IDAT_data_bytes>

<IDAT_data_bytes> ::= <byte>* := idat_payload(32,32)


<IDAT_length> ::= <IDAT_length_bytes>

<IDAT_length_bytes> ::= <byte>* := \
    be32(len(idat_payload(32,32)))


<IDAT_crc> ::= <IDAT_crc_bytes>

<IDAT_crc_bytes> ::= <byte>* := \
    crc32_chunk( \
        b"IDAT", \
        idat_payload(32,32) \
    )


###############################################################################
# IEND Chunk
###############################################################################

<iend_chunk> ::= \
( \
    <IEND_length> \
    <IEND_type> \
    <IEND_crc> \
)

<IEND_type> ::= b"IEND"

<IEND_length> ::= <IEND_length_bytes>

<IEND_length_bytes> ::= <byte>* := be32(0)


<IEND_crc> ::= <IEND_crc_bytes>

<IEND_crc_bytes> ::= <byte>* := \
    crc32_chunk(b"IEND", b"")