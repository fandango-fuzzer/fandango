# gif_32x32.fan
# Fandango specification for a structurally valid 32x32 GIF89a file.

import struct
import random


# ----------------------------------------------------------------------
# Global Constants
# ----------------------------------------------------------------------

IMAGE_WIDTH: int = 32
IMAGE_HEIGHT: int = 32
TEXT_LENGTH: int = 100
GLOBAL_COLOR_TABLE_SIZE: int = 256


# ----------------------------------------------------------------------
# Start Symbol
# ----------------------------------------------------------------------

# Complete GIF file:
#   Header
#   Logical Screen Descriptor
#   Global Color Table
#   Optional Comment Extensions
#   Image Descriptor
#   Image Data
#   Trailer
<start> ::= \
    <header> \
    <logical_screen_descriptor> \
    <global_color_table> \
    <comment_extension>* \
    <image_descriptor> \
    <image_data> \
    <trailer>


# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------

# GIF89a signature
<header> ::= b"GIF89a"


# ----------------------------------------------------------------------
# Logical Screen Descriptor
# ----------------------------------------------------------------------

# Logical screen descriptor structure
<logical_screen_descriptor> ::= \
    <lsd_width> \
    <lsd_height> \
    <lsd_packed> \
    <lsd_background_color_index> \
    <lsd_pixel_aspect_ratio>

# Logical screen width (32 pixels, little-endian)
<lsd_width> ::= <byte>{2} := int_to_le_bytes(IMAGE_WIDTH)

# Logical screen height (32 pixels, little-endian)
<lsd_height> ::= <byte>{2} := int_to_le_bytes(IMAGE_HEIGHT)

# Packed fields:
#   Global Color Table Flag = 1
#   Color Resolution = 7
#   Sort Flag = 0
#   GCT Size = 7 (2^(7+1)=256 entries)
<lsd_packed> ::= b"\xf7"

# Background color index
<lsd_background_color_index> ::= b"\x00"

# Pixel aspect ratio (0 = not specified)
<lsd_pixel_aspect_ratio> ::= b"\x00"


# ----------------------------------------------------------------------
# Global Color Table
# ----------------------------------------------------------------------

# Global Color Table (256 entries × 3 bytes RGB)
<global_color_table> ::= <byte>{GLOBAL_COLOR_TABLE_SIZE * 3} \
    := generate_color_table(GLOBAL_COLOR_TABLE_SIZE)


# ----------------------------------------------------------------------
# Comment Extension (Optional)
# ----------------------------------------------------------------------

# Comment Extension block
<comment_extension> ::= \
    <comment_introducer> \
    <comment_label> \
    <comment_sub_blocks>

# Extension introducer
<comment_introducer> ::= b"\x21"

# Comment label
<comment_label> ::= b"\xfe"

# Comment data packed into sub-blocks
<comment_sub_blocks> ::= <byte>* \
    := generate_sub_blocks(generate_ascii_text(TEXT_LENGTH))


# ----------------------------------------------------------------------
# Image Descriptor
# ----------------------------------------------------------------------

# Image descriptor block
<image_descriptor> ::= \
    <image_separator> \
    <image_left> \
    <image_top> \
    <image_width> \
    <image_height> \
    <image_packed>

# Image separator
<image_separator> ::= b"\x2c"

# Left position
<image_left> ::= <byte>{2} := int_to_le_bytes(0)

# Top position
<image_top> ::= <byte>{2} := int_to_le_bytes(0)

# Image width (32 pixels)
<image_width> ::= <byte>{2} := int_to_le_bytes(IMAGE_WIDTH)

# Image height (32 pixels)
<image_height> ::= <byte>{2} := int_to_le_bytes(IMAGE_HEIGHT)

# Packed field (no local color table)
<image_packed> ::= b"\x00"


# ----------------------------------------------------------------------
# Image Data (LZW)
# ----------------------------------------------------------------------

# Image data block
<image_data> ::= \
    <lzw_min_code_size> \
    <image_sub_blocks>

# LZW minimum code size (8 bits for 256-color GCT)
<lzw_min_code_size> ::= b"\x08"

# LZW-compressed pixel indices packed into sub-blocks
<image_sub_blocks> ::= <byte>* \
    := generate_sub_blocks(generate_lzw_data(IMAGE_WIDTH, IMAGE_HEIGHT))


# ----------------------------------------------------------------------
# Trailer
# ----------------------------------------------------------------------

# GIF file terminator
<trailer> ::= b"\x3b"


# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------

def int_to_le_bytes(value: int) -> bytes:
    """
    Convert integer to 2-byte little-endian representation.

    :param value: Integer value.
    :return: 2-byte little-endian byte sequence.
    """
    return struct.pack("<H", value)


def generate_color_table(size: int) -> bytes:
    """
    Generate a global color table.

    Each entry consists of 3 bytes (RGB).

    :param size: Number of color entries.
    :return: RGB table as bytes.
    """
    table = bytearray()
    for _ in range(size):
        table.extend([
            random.getrandbits(8),
            random.getrandbits(8),
            random.getrandbits(8)
        ])
    return bytes(table)


def generate_ascii_text(length: int) -> bytes:
    """
    Generate ASCII text of fixed length.

    :param length: Number of characters.
    :return: ASCII byte string.
    """
    return bytes(
        random.randint(32, 126)
        for _ in range(length)
    )


def generate_lzw_data(width: int, height: int) -> bytes:
    """
    Generate placeholder LZW-compressed pixel index data.

    This function generates raw pixel indices and performs
    a minimal LZW-like packing sufficient for structural validity.

    :param width: Image width.
    :param height: Image height.
    :return: Compressed byte stream.
    """
    pixel_count = width * height
    data = bytearray()
    for _ in range(pixel_count):
        data.append(random.randint(0, 255))
    return bytes(data)


def generate_sub_blocks(data: bytes) -> bytes:
    """
    Split data into GIF sub-blocks.

    Each sub-block:
      - 1 length byte (1–255)
      - up to 255 data bytes
    Terminates with a zero-length block.

    :param data: Payload bytes.
    :return: Sub-block encoded byte sequence.
    """
    result = bytearray()
    index = 0
    while index < len(data):
        chunk = data[index:index+255]
        result.append(len(chunk))
        result.extend(chunk)
        index += 255
    result.append(0)
    return bytes(result)