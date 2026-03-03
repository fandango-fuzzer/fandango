# ============================================================
# WAV (RIFF/WAVE) File Grammar for Fandango
# ============================================================

import struct
import random

# ============================================================
# Global Configuration
# ============================================================

# Audio configuration
NUM_CHANNELS = 1
SAMPLE_RATE  = 44100
BITS_PER_SAMPLE = 16
DURATION_SECONDS = 1

# Derived constants
BYTES_PER_SAMPLE = BITS_PER_SAMPLE // 8
BLOCK_ALIGN = NUM_CHANNELS * BYTES_PER_SAMPLE
BYTE_RATE = SAMPLE_RATE * BLOCK_ALIGN
NUM_SAMPLES = SAMPLE_RATE * DURATION_SECONDS
DATA_SIZE = NUM_SAMPLES * BLOCK_ALIGN
FMT_CHUNK_SIZE = 16
RIFF_CHUNK_SIZE = 4 + (8 + FMT_CHUNK_SIZE) + (8 + DATA_SIZE)

# ============================================================
# Helper Functions
# ============================================================

def le_u16(value: int) -> bytes:
    """Return value encoded as little-endian unsigned 16-bit."""
    return struct.pack("<H", value)

def le_u32(value: int) -> bytes:
    """Return value encoded as little-endian unsigned 32-bit."""
    return struct.pack("<I", value)

def generate_pcm_data(num_samples: int,
                      num_channels: int,
                      bits_per_sample: int) -> bytes:
    """
    Generate signed PCM sample data.

    Produces little-endian PCM samples.
    """
    max_amplitude = 2 ** (bits_per_sample - 1) - 1
    samples = []

    for _ in range(num_samples * num_channels):
        value = random.randint(-max_amplitude, max_amplitude)
        samples.append(struct.pack("<h", value))

    return b"".join(samples)

# ============================================================
# Grammar
# ============================================================

# ------------------------------------------------------------
# Start symbol
# ------------------------------------------------------------

<start> ::= <wav_file>

# ------------------------------------------------------------
# Complete WAV file
# ------------------------------------------------------------

<wav_file> ::= \
    <riff_header> \
    <fmt_chunk> \
    <data_chunk>

# ------------------------------------------------------------
# RIFF Header
# ------------------------------------------------------------

# RIFF chunk descriptor
<riff_header> ::= \
    b"RIFF" \
    <riff_chunk_size> \
    b"WAVE"

# Size of entire file minus 8 bytes
<riff_chunk_size> ::= <byte>{4} := le_u32(RIFF_CHUNK_SIZE)

# ------------------------------------------------------------
# Format Chunk ("fmt ")
# ------------------------------------------------------------

<fmt_chunk> ::= \
    b"fmt " \
    <fmt_chunk_size> \
    <audio_format> \
    <num_channels> \
    <sample_rate> \
    <byte_rate> \
    <block_align> \
    <bits_per_sample>

# PCM format chunk size (16 bytes)
<fmt_chunk_size> ::= <byte>{4} := le_u32(FMT_CHUNK_SIZE)

# Audio format (1 = PCM)
<audio_format> ::= <byte>{2} := le_u16(1)

# Number of channels
<num_channels> ::= <byte>{2} := le_u16(NUM_CHANNELS)

# Samples per second
<sample_rate> ::= <byte>{4} := le_u32(SAMPLE_RATE)

# Average bytes per second
<byte_rate> ::= <byte>{4} := le_u32(BYTE_RATE)

# Block alignment
<block_align> ::= <byte>{2} := le_u16(BLOCK_ALIGN)

# Bits per sample
<bits_per_sample> ::= <byte>{2} := le_u16(BITS_PER_SAMPLE)

# ------------------------------------------------------------
# Data Chunk
# ------------------------------------------------------------

<data_chunk> ::= \
    b"data" \
    <data_chunk_size> \
    <pcm_data>

# Size of PCM data in bytes
<data_chunk_size> ::= <byte>{4} := le_u32(DATA_SIZE)

# Raw PCM sample data
<pcm_data> ::= <byte>{DATA_SIZE} := \
    generate_pcm_data(NUM_SAMPLES, NUM_CHANNELS, BITS_PER_SAMPLE)

# ============================================================
# End of File
# ============================================================