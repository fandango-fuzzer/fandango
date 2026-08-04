# ============================================================
# Minimal Valid MP3 File (ID3v2 + MPEG1 Layer III + ID3v1)
# Produces exactly one second of silence.
# ============================================================

import struct
import random


# ============================================================
# Global Constants
# ============================================================

# MPEG-1 Layer III, 128 kbps, 44.1 kHz, no CRC, stereo
BITRATE_INDEX = 9              # 128 kbps
SAMPLING_INDEX = 0             # 44.1 kHz
PADDING_BIT = 0
CHANNEL_MODE = 0               # stereo
SAMPLES_PER_FRAME = 1152
SAMPLING_RATE = 44100
BITRATE = 128000
FRAME_LENGTH = 417             # floor(144*bitrate/sr)
FRAMES_PER_SECOND = 38         # ceil(44100/1152)
TEXT_DIMENSION = 100           # required preference


# ============================================================
# Helper Functions
# ============================================================

def synchsafe(n: int) -> bytes:
    """Convert integer to 4-byte synchsafe representation."""
    return bytes([
        (n >> 21) & 0x7F,
        (n >> 14) & 0x7F,
        (n >> 7) & 0x7F,
        n & 0x7F,
    ])


# ============================================================
# Grammar
# ============================================================

# ------------------------------------------------------------
# Start Symbol
# ------------------------------------------------------------

<start> ::= <mp3_file>


# ------------------------------------------------------------
# Complete MP3 File
# ------------------------------------------------------------

<mp3_file> ::= <id3v2> <mpeg_audio> <id3v1>

# ------------------------------------------------------------
# MPEG Audio
# ------------------------------------------------------------

<mpeg_audio> ::= <mpeg_audio_frame>{FRAMES_PER_SECOND}


# ------------------------------------------------------------
# MPEG Audio Frame
# ------------------------------------------------------------

# <mpeg_audio_frame> ::= <byte>* := build_frame()

<mpeg_audio_frame> ::= \
    <mpeg_audio_header> \
    <mpeg_audio_side_info> \
    <mpeg_audio_main_data>

# Frame Header (4 bytes, fully bit modeled)
<mpeg_audio_header> ::= \
    <mpeg_audio_sync_bits> \
    <mpeg_audio_version_id> \
    <mpeg_audio_layer_bits> \
    <mpeg_audio_protection_bit> \
    <mpeg_audio_bitrate_bits> \
    <mpeg_audio_sampling_bits> \
    <mpeg_audio_padding_bit> \
    <mpeg_audio_private_bit> \
    <mpeg_audio_channel_mode_bits> \
    <mpeg_audio_mode_extension_bits> \
    <mpeg_audio_copyright_bit> \
    <mpeg_audio_original_bit> \
    <mpeg_audio_emphasis_bits>


# 11 sync bits: 11111111111
<mpeg_audio_sync_bits> ::= 1 1 1 1 1 1 1 1 1 1 1

# MPEG Version 1: 11
<mpeg_audio_version_id> ::= 1 1

# Layer III: 01
<mpeg_audio_layer_bits> ::= 0 1

# No CRC
<mpeg_audio_protection_bit> ::= 1

# 128 kbps: 1001
<mpeg_audio_bitrate_bits> ::= 1 0 0 1

# 44.1 kHz: 00
<mpeg_audio_sampling_bits> ::= 0 0

# No padding
<mpeg_audio_padding_bit> ::= 0

<mpeg_audio_private_bit> ::= 0

# Stereo: 00
<mpeg_audio_channel_mode_bits> ::= 0 0

# Mode extension (unused in stereo)
<mpeg_audio_mode_extension_bits> ::= 0 0

<mpeg_audio_copyright_bit> ::= 0
<mpeg_audio_original_bit> ::= 0

# No emphasis: 00
<mpeg_audio_emphasis_bits> ::= 0 0

  
# Side information (32 bytes for stereo MPEG1)
<mpeg_audio_side_info> ::= b"\x00"{32}

# Main data (rest of frame) - all silence
MAIN_DATA_SIZE = FRAME_LENGTH - 4 - 32
<mpeg_audio_main_data> ::= b"\x00"{MAIN_DATA_SIZE}

# <mpeg_audio_main_data> ::= <byte>{MAIN_DATA_SIZE} := white_noise(MAIN_DATA_SIZE)
#
# def white_noise(size: int) -> bytes:
#     return bytes([random.randint(1, 255) for _ in range(size)])


# ------------------------------------------------------------
# ID3v2 Section
# ------------------------------------------------------------

# This is a minimal ID3v2.3 tag with one TIT2 frame

<id3v2> ::= <id3v2_header> <id3v2_frame>

# <id3v2> ::= <byte>* := build_id3v2()

<id3v2_header> ::= b"ID3" b"\x03\x00" b"\x00" <id3v2_len>

<id3v2_len> ::= <byte>{4} 
where <id3v2_len> == synchsafe(len(bytes(<id3v2_frame>)))

<id3v2_frame> ::= \
    <id3v2_frame_id> \
    <id3v2_frame_size> \
    <id3v2_flags> \
    <id3v2_encoding> \
    <id3v2_text>
    
<id3v2_frame_id> ::= b"TIT2"

<id3v2_frame_size> ::= <byte>{4}
where <id3v2_frame_size> == \
    struct.pack(">I", len(bytes(<id3v2_encoding>)) + 
                      len(bytes(<id3v2_text>)))

<id3v2_flags> ::= b"\x00\x00"

<id3v2_encoding> ::= b"\x00"

<id3v2_text> ::= <byte>* := \
    b"Silent MP3".ljust(TEXT_DIMENSION, b"\x00")


# ------------------------------------------------------------
# ID3v1 Section
# ------------------------------------------------------------

# <id3v1> ::= <byte>* := build_id3v1()

<id3v1> ::= \
    <id3v1_tag> \
    <id3v1_title> \
    <id3v1_artist> \
    <id3v1_album> \
    <id3v1_year> \
    <id3v1_comment> \
    <id3v1_genre>

<id3v1_tag> ::= b"TAG"

<id3v1_title> ::= <byte>{30} := b"Silent MP3".ljust(30, b"\x00")

<id3v1_artist> ::= <byte>{30} := b"ZZ Top".ljust(30, b"\x00")

<id3v1_album> ::= <byte>{30} := b"Fandango!".ljust(30, b"\x00")

<id3v1_year> ::= <byte>{4} := b"2026"

<id3v1_comment> ::= <byte>{30} := b"".ljust(30, b"\x00")

<id3v1_genre> ::= b"\x00"
