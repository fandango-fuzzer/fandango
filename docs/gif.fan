# gif_minimal.fan
# Minimal structurally valid GIF89a grammar for Fandango

import struct


###############################################################################
# Helper Functions (Constructive Only)
###############################################################################

def u16le(n):
    """
    Construct 2-byte little-endian encoding of integer n.
    """
    return struct.pack("<H", n & 0xffff)


def make_lsd_packed():
    """
    Construct Logical Screen Descriptor packed field
    with:
      - Global Color Table flag = 1
      - Color resolution = 0
      - Sort flag = 0
      - GCT size = 0  (table size = 2 entries)
    """
    return b"\x80"


def make_global_color_table():
    """
    Construct a minimal 2-entry global color table.
    Two RGB triples.
    """
    return b"\x00\x00\x00" + b"\xff\xff\xff"


def make_image_descriptor():
    """
    Construct a minimal Image Descriptor:
      - Image separator (0x2C)
      - Left, Top = 0
      - Width, Height = 1
      - No local color table
    """
    return b"\x2C" + \
           u16le(0) + \
           u16le(0) + \
           u16le(1) + \
           u16le(1) + \
           b"\x00"


def make_image_data():
    """
    Construct minimal LZW image data for 1x1 pixel image.

    Structure:
      - LZW minimum code size = 2
      - One data sub-block of size 2
      - Block terminator (0)
    """
    return b"\x02" + \
           b"\x02" + \
           b"\x4C\x01" + \
           b"\x00"


###############################################################################
# Grammar
###############################################################################

<start> ::= <gif_file>


###############################################################################
# GIF File
###############################################################################

<gif_file> ::= <gif_header> \
               <logical_screen_descriptor> \
               <global_color_table> \
               <image_block> \
               <gif_trailer>


###############################################################################
# Header
###############################################################################

<gif_header> ::= <gif_signature> <gif_version>

<gif_signature> ::= <byte>* := b"GIF"

<gif_version> ::= <byte>* := b"89a"


###############################################################################
# Logical Screen Descriptor
###############################################################################

<logical_screen_descriptor> ::= <lsd_width> \
                                <lsd_height> \
                                <lsd_packed> \
                                <lsd_bgcolor> \
                                <lsd_aspect>

<lsd_width> ::= <byte>* := u16le(1)

<lsd_height> ::= <byte>* := u16le(1)

<lsd_packed> ::= <byte>* := make_lsd_packed()

<lsd_bgcolor> ::= <byte>* := b"\x00"

<lsd_aspect> ::= <byte>* := b"\x00"


###############################################################################
# Global Color Table
###############################################################################

<global_color_table> ::= <gct_bytes>

<gct_bytes> ::= <byte>* := make_global_color_table()


###############################################################################
# Image Block
###############################################################################

<image_block> ::= <image_descriptor> <image_data>

<image_descriptor> ::= <byte>* := make_image_descriptor()

<image_data> ::= <byte>* := make_image_data()


###############################################################################
# Trailer
###############################################################################

<gif_trailer> ::= <byte>* := b"\x3B"