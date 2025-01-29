
include('gif.fan')

where <GifHeader>..<Signature> == "GIF"
where <GifHeader>..<Version> == "89a"

<char> ::= <byte>
<unsigned_short> ::= <byte> <byte>
<unsigned_char> ::= <byte>

<rgb> ::= <RGB> <RGB>  # Have only two RGB entries

# Refine UNDEFINEDDATA
<UNDEFINEDDATA> ::= <ExtensionIntroducer_9> <Label> <DataSubBlocks_1>
<ExtensionIntroducer_9> ::= b'\x21'
<Label> ::= b'\f9'

# where len(<GLOBALCOLORTABLE>.<rgb>) == 2 ** ord(str(<SizeOfGlobalColorTable>))
# where len(<DATASUBBLOCK>.<Data>) == ord(str(<DATASUBBLOCK>.<Size_1>))
#
# # Make sure we have a global color table
# where <SizeOfGlobalColorTable> == chr(4)
#
# # Make sure we have an image
# <DATA> ::= <ImageDescriptor> <LocalColorTable>? <ImageData>
#
# # Make sure we have at least one data sub block
# <DATASUBBLOCKS> ::= (<DataSubBlock>)+ <BlockTerminator_1>
#
# # Force a particular size for the global color table; the above constraint does not cut it
# <rgb> ::= <RGB>{16}