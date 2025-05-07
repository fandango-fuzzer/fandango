from fandango.evolution.havoc import havoc_mutate

# Start symbol
<start> ::= <actual_byte>* := havoc_mutate(<gif_file>) ;
<actual_byte> ::= <actual_bit>{8}
<actual_bit> ::= 0 | 1

# A complete GIF file: header, logical screen descriptor, data blocks, and trailer
<gif_file> ::= <header> <logical_screen_descriptor> <data_blocks> <trailer> ;

# Header: 6 bytes ("GIF" + version)
<header> ::= "GIF" <version> ;
<version> ::= "87a" | "89a"  # Literal 3-byte strings for version

# Logical Screen Descriptor: 7 bytes total
<logical_screen_descriptor> ::= <width> <height> <packed_fields> <background_color_index> <pixel_aspect_ratio> ;
<width> ::= <uint16>           # 2 bytes little-endian width
<height> ::= <uint16>          # 2 bytes little-endian height
<packed_fields> ::= "\\x00"     # 1 byte: no global color table
<background_color_index> ::= <byte>  # 1 byte (arbitrary since no global color table)
<pixel_aspect_ratio> ::= <byte>        # 1 byte

# Data Blocks: In this example, we produce one image block.
<data_blocks> ::= <image_block> ;

# Image Block
<image_block> ::= "\\x2C" <image_descriptor> <image_data> ;

# Image Descriptor: exactly 9 bytes (left, top, width, height, and a packed field)
<image_descriptor> ::= <left_position> <top_position> <width> <height> "\\x00" ;
<left_position> ::= <uint16>  # 2 bytes for left position
<top_position> ::= <uint16>   # 2 bytes for top position

# Image Data: LZW minimum code size (1 byte) + image sub-blocks
<image_data> ::= <lzw_minimum_code_size> <image_sub_blocks> ;
<lzw_minimum_code_size> ::= "\\x02"  # Valid LZW minimum code size for a 2-color image

# Image Sub-Blocks: one or more non-empty sub-blocks, ending with a terminating sub-block
<image_sub_blocks> ::= <non_empty_sub_block> <image_sub_blocks> | <terminating_sub_block> ;
<non_empty_sub_block> ::= <block_size_nonzero> <block_data> ;
<terminating_sub_block> ::= "\\x00"  # A sub-block of size 0 terminates the image data

# For simplicity, we generate a fixed sub-block of 8 bytes of LZW data.
<block_size_nonzero> ::= "\\x08"  # Indicates 8 bytes of data follow
<block_data> ::= <lzw_data_bytes> ;
<lzw_data_bytes> ::= <byte> <byte> <byte> <byte> <byte> <byte> <byte> <byte> ;

# Trailer: 1 byte terminator for the GIF file
<trailer> ::= "\\x3B" ;

# Data Types
<uint16> ::= <byte> <byte>  # 2-byte little-endian unsigned integer
<byte> ::= "\\x" <hex_digit> <hex_digit>  # A byte represented as \xHH
<hex_digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "A" | "B" | "C" | "D" | "E" | "F" ;
