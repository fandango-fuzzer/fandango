
include('gif.fan')

where <GifHeader>..<Signature> == b"GIF"
where <GifHeader>..<Version> == b"89a"

<char> ::= <byte>
<unsigned_short> ::= <byte> <byte>
<unsigned_char> ::= <byte>

<rgb> ::= <RGB> <RGB>  # Have only two RGB entries

# Refine UNDEFINEDDATA
<UNDEFINEDDATA> ::= <ExtensionIntroducer_9> <Label> <DataSubBlocks_1>
<ExtensionIntroducer_9> ::= b'\x21'
<Label> ::= b'\f9'

# Ensure we have precisely these fields
<start> ::= <GifHeader> <LogicalScreenDescriptor> <GlobalColorTable> <Data_1> <Trailer>

# We want one pixel
<Width> ::= b"\x01" b"\x00"
<Height> ::= b"\x01" b"\x00"

<ImageWidth> ::= b"\x01" b"\x00"
<ImageHeight> ::= b"\x01" b"\x00"

<ImageLeftPosition> ::= b'\x00' b'\x00'
<ImageTopPosition> ::= b'\x00' b'\x00'

<DATA> ::= <GraphicControlExtension> <ImageDescriptor> <LocalColorTable> <ImageData>

<GRAPHICCONTROLEXTENSION_DATASUBBLOCK_PACKEDFIELDS> ::= 0 0 0 0 0 0 0 1
<PackedFields_1> ::= 0 0 0 0 0 0 0 0

<SizeOfLocalColorTable> ::= 0 0 0
<SizeOfGlobalColorTable> ::= 0 0 0

<GlobalColorTable> ::= <RGB> b'\x00' b'\x00' b'\x00'
<LocalColorTable> ::= b'\x02' b'\x02' b'L'

<PixelAspectRatio> ::= b'\x00'


<GlobalColorTableFlag> ::= 1
<ColorResolution> ::= 0 0 0

<BackgroundColorIndex> ::= b'\x01'

<BlockSize> ::= b'\x04'

<DelayTime> ::= b'\n' b'\x00'

<TransparentColorIndex> ::= b'\x01'
<BlockTerminator_2> ::= b'\x00'

<LZWMinimumCodeSize> ::= b'\x01'
<DataSubBlocks> ::= b'\x00'
