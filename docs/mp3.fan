# ============================================================
# MP3 File Format – Grammar-Based Tags (Documented)
# ============================================================

import random
import struct

# ============================================================
# Global Configuration
# ============================================================

MIN_FRAMES = 1
MAX_FRAMES = 4
FRAME_PAYLOAD_SIZE = 100

# ============================================================
# Helper Functions
# ============================================================

def syncsafe(size: int) -> bytes:
    """
    Convert integer to 4-byte syncsafe representation
    (7 bits per byte, ID3v2 requirement).
    """
    b1 = (size >> 21) & 0x7F
    b2 = (size >> 14) & 0x7F
    b3 = (size >> 7) & 0x7F
    b4 = size & 0x7F
    return bytes([b1, b2, b3, b4])


def compute_id3v2_size(payload: bytes) -> bytes:
    """
    Compute syncsafe size for ID3v2 header.
    """
    return syncsafe(len(payload))


def pack_u32_be(value: int) -> bytes:
    """
    Pack 32-bit unsigned integer as big-endian.
    """
    return struct.pack(">I", value)


def build_frame(payload_size: int) -> bytes:
    """
    Construct a simple MPEG1 Layer III frame
    with fixed valid header.
    """
    header = b"\xFF\xFB\x90\x64"
    payload = random.randbytes(payload_size)
    return header + payload


# ============================================================
# Grammar
# ============================================================

# ------------------------------------------------------------
# Start Symbol
# ------------------------------------------------------------

# Root symbol of an MP3 document
<start> ::= <mp3_file>

# ------------------------------------------------------------
# Complete MP3 File
# ------------------------------------------------------------

# Full MP3 file:
#   Optional ID3v2 tag
#   One or more MPEG audio frames
#   Optional ID3v1 tag
<mp3_file> ::= <id3v2_tag>? <audio_frames> <id3v1_tag>?

# ============================================================
# ID3v2 Tag (Header + Frames)
# ============================================================

# ID3v2 tag structure:
#   "ID3" magic
#   version
#   flags
#   syncsafe size
#   frames
<id3v2_tag> ::= \
    "ID3" \
    <id3v2_version> \
    <id3v2_flags> \
    <id3v2_size> \
    <id3v2_frames>

# ID3v2 version 2.3.0
<id3v2_version> ::= b"\x03\x00"

# ID3v2 flags (no flags set)
<id3v2_flags> ::= b"\x00"

# 4-byte syncsafe size of the ID3v2 frame section
<id3v2_size> ::= <id3v2_size_raw>

# Construct syncsafe size from frame payload
<id3v2_size_raw> ::= <byte>* := compute_id3v2_size(bytes(<id3v2_frames>))

# ------------------------------------------------------------
# ID3v2 Frames
# ------------------------------------------------------------

# Zero or more ID3v2 frames
<id3v2_frames> ::= <id3v2_frame>*

# Single ID3v2 frame:
#   4-byte frame ID
#   4-byte size
#   2-byte flags
#   payload
<id3v2_frame> ::= \
    <id3v2_frame_id> \
    <id3v2_frame_size> \
    <id3v2_frame_flags> \
    <id3v2_frame_payload>

# Supported frame identifiers:
#   TIT2 – Title
#   TALB – Album
#   TPE1 – Artist
<id3v2_frame_id> ::= "TIT2" | "TALB" | "TPE1"

# 4-byte big-endian frame size
<id3v2_frame_size> ::= <id3v2_frame_size_raw>

# Construct frame size from payload length
<id3v2_frame_size_raw> ::= <byte>{4} := pack_u32_be(len(bytes(<id3v2_frame_payload>)))

# Frame flags (none set)
<id3v2_frame_flags> ::= b"\x00\x00"

# Text frame payload:
#   1 byte encoding
#   text bytes
<id3v2_frame_payload> ::= \
    <id3v2_text_encoding> \
    <id3v2_text_data>

# Text encoding 0 = ISO-8859-1
<id3v2_text_encoding> ::= b"\x00"

# 10 bytes of text data
<id3v2_text_data> ::= <byte>{10}

# ============================================================
# MPEG Audio Frames
# ============================================================

# One or more audio frames
<audio_frames> ::= <audio_frame>+

# Single audio frame constructed via helper
<audio_frame> ::= <audio_frame_raw>

# Construct MPEG frame with fixed header and random payload
<audio_frame_raw> ::= <byte>* := build_frame(FRAME_PAYLOAD_SIZE)

# ============================================================
# ID3v1 Tag (128-byte Footer)
# ============================================================

# ID3v1 tag structure:
#   "TAG"
#   30-byte title
#   30-byte artist
#   30-byte album
#   4-byte year
#   30-byte comment
#   1-byte genre
<id3v1_tag> ::= \
    "TAG" \
    <id3v1_title> \
    <id3v1_artist> \
    <id3v1_album> \
    <id3v1_year> \
    <id3v1_comment> \
    <id3v1_genre>

# 30-byte title field
<id3v1_title> ::= <byte>{30}

# 30-byte artist field
<id3v1_artist> ::= <byte>{30}

# 30-byte album field
<id3v1_album> ::= <byte>{30}

# 4 ASCII digits representing year
<id3v1_year> ::= <digit><digit><digit><digit>

# Single ASCII digit
<digit> ::= "0" | "1" | "2" | "3" | "4" | \
            "5" | "6" | "7" | "8" | "9"

# 30-byte comment field
<id3v1_comment> ::= <byte>{30}

# 1-byte genre index
<id3v1_genre> ::= <byte>