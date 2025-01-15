<start> ::= <GifHeader> <LogicalScreenDescriptor> <GlobalColorTable>? <Data_1> <Trailer>
  <GifHeader> ::= <GIFHEADER>
    <GIFHEADER> ::= <Signature> <Version>
      <Signature> ::= <char>{3}
      <Version> ::= <char>{3}
  <LogicalScreenDescriptor> ::= <LOGICALSCREENDESCRIPTOR>
    <LOGICALSCREENDESCRIPTOR> ::= <Width> <Height> <PackedFields> <BackgroundColorIndex> <PixelAspectRatio>
      <Width> ::= <ushort>
        <ushort> ::= <unsigned_short>
      <Height> ::= <ushort>
      <PackedFields> ::= <LOGICALSCREENDESCRIPTOR_PACKEDFIELDS>
        <LOGICALSCREENDESCRIPTOR_PACKEDFIELDS> ::= <GlobalColorTableFlag> <ColorResolution> <SortFlag> <SizeOfGlobalColorTable>
          <GlobalColorTableFlag> ::= <bit>
          <ColorResolution> ::= <bit>{3}
          <SortFlag> ::= <bit>
          <SizeOfGlobalColorTable> ::= <bit>{3}
      <BackgroundColorIndex> ::= <UBYTE>
        <UBYTE> ::= <ubyte>
          <ubyte> ::= <uchar>
            <uchar> ::= <unsigned_char>
      <PixelAspectRatio> ::= <UBYTE>
  <GlobalColorTable> ::= <GLOBALCOLORTABLE>
    <GLOBALCOLORTABLE> ::= <rgb>
      <rgb> ::= <RGB>*  # FIXME: must be {size}
        <RGB> ::= <R> <G> <B>
          <R> ::= <UBYTE>
          <G> ::= <UBYTE>
          <B> ::= <UBYTE>
  <Data_1> ::= <DATA>
    <DATA> ::= (<ImageDescriptor> <LocalColorTable>? <ImageData> | <GraphicControlExtension> | <CommentExtension> | <PlainTextExtension> | <ApplicationExtension> | <UndefinedData>)*
      <ImageDescriptor> ::= <IMAGEDESCRIPTOR>
        <IMAGEDESCRIPTOR> ::= <ImageSeperator_1> <ImageLeftPosition> <ImageTopPosition> <ImageWidth> <ImageHeight> <PackedFields_1>
          <ImageSeperator_1> ::= b','
          <ImageLeftPosition> ::= <ushort>
          <ImageTopPosition> ::= <ushort>
          <ImageWidth> ::= <ushort>
          <ImageHeight> ::= <ushort>
          <PackedFields_1> ::= <IMAGEDESCRIPTOR_PACKEDFIELDS>
            <IMAGEDESCRIPTOR_PACKEDFIELDS> ::= <LocalColorTableFlag> <InterlaceFlag> <SortFlag_1> <Reserved> <SizeOfLocalColorTable>
              <LocalColorTableFlag> ::= <bit>
              <InterlaceFlag> ::= <bit>
              <SortFlag_1> ::= <bit>
              <Reserved> ::= <bit>{2}
              <SizeOfLocalColorTable> ::= <bit>{3}
      <LocalColorTable> ::= <LOCALCOLORTABLE>
        <LOCALCOLORTABLE> ::= <rgb_1>
          <rgb_1> ::= <RGB>*  # FIXME: must be {size}
      <ImageData> ::= <IMAGEDATA>
        <IMAGEDATA> ::= <LZWMinimumCodeSize> <DataSubBlocks>
          <LZWMinimumCodeSize> ::= <UBYTE>
          <DataSubBlocks> ::= <DATASUBBLOCKS>
            <DATASUBBLOCKS> ::= (<DataSubBlock>)* <BlockTerminator_1>
              <DataSubBlock> ::= <DATASUBBLOCK>
                <DATASUBBLOCK> ::= <Size_1> <Data>
                  <Size_1> ::= (b'\x01' | b'\x02' | b'\x03' | b'\x04' | b'\x05' | b'\x06' | b'\x07' | b'\x08' | b'\t' | b'\n' | b'\x0b' | b'\x0c' | b'\r' | b'\x0e' | b'\x0f' | b'\x10' | b'\x11' | b'\x12' | b'\x13' | b'\x14' | b'\x15' | b'\x16' | b'\x17' | b'\x18' | b'\x19' | b'\x1a' | b'\x1b' | b'\x1c' | b'\x1d' | b'\x1e' | b'\x1f' | b' ' | b'!' | b'"' | b'#' | b'$' | b'%' | b'&' | b"'" | b'(' | b')' | b'*' | b'+' | b',' | b'-' | b'.' | b'/' | b'0' | b'1' | b'2' | b'3' | b'4' | b'5' | b'6' | b'7' | b'8' | b'9' | b':' | b';' | b'<' | b'=' | b'>' | b'?' | b'@' | b'A' | b'B' | b'C' | b'D' | b'E' | b'F' | b'G' | b'H' | b'I' | b'J' | b'K' | b'L' | b'M' | b'N' | b'O' | b'P' | b'Q' | b'R' | b'S' | b'T' | b'U' | b'V' | b'W' | b'X' | b'Y' | b'Z' | b'[' | b'\\' | b']' | b'^' | b'_' | b'`' | b'a' | b'b' | b'c' | b'd' | b'e' | b'f' | b'g' | b'h' | b'i' | b'j' | b'k' | b'l' | b'm' | b'n' | b'o' | b'p' | b'q' | b'r' | b's' | b't' | b'u' | b'v' | b'w' | b'x' | b'y' | b'z' | b'{' | b'|' | b'}' | b'~' | b'\x7f' | b'\x80' | b'\x81' | b'\x82' | b'\x83' | b'\x84' | b'\x85' | b'\x86' | b'\x87' | b'\x88' | b'\x89' | b'\x8a' | b'\x8b' | b'\x8c' | b'\x8d' | b'\x8e' | b'\x8f' | b'\x90' | b'\x91' | b'\x92' | b'\x93' | b'\x94' | b'\x95' | b'\x96' | b'\x97' | b'\x98' | b'\x99' | b'\x9a' | b'\x9b' | b'\x9c' | b'\x9d' | b'\x9e' | b'\x9f' | b'\xa0' | b'\xa1' | b'\xa2' | b'\xa3' | b'\xa4' | b'\xa5' | b'\xa6' | b'\xa7' | b'\xa8' | b'\xa9' | b'\xaa' | b'\xab' | b'\xac' | b'\xad' | b'\xae' | b'\xaf' | b'\xb0' | b'\xb1' | b'\xb2' | b'\xb3' | b'\xb4' | b'\xb5' | b'\xb6' | b'\xb7' | b'\xb8' | b'\xb9' | b'\xba' | b'\xbb' | b'\xbc' | b'\xbd' | b'\xbe' | b'\xbf' | b'\xc0' | b'\xc1' | b'\xc2' | b'\xc3' | b'\xc4' | b'\xc5' | b'\xc6' | b'\xc7' | b'\xc8' | b'\xc9' | b'\xca' | b'\xcb' | b'\xcc' | b'\xcd' | b'\xce' | b'\xcf' | b'\xd0' | b'\xd1' | b'\xd2' | b'\xd3' | b'\xd4' | b'\xd5' | b'\xd6' | b'\xd7' | b'\xd8' | b'\xd9' | b'\xda' | b'\xdb' | b'\xdc' | b'\xdd' | b'\xde' | b'\xdf' | b'\xe0' | b'\xe1' | b'\xe2' | b'\xe3' | b'\xe4' | b'\xe5' | b'\xe6' | b'\xe7' | b'\xe8' | b'\xe9' | b'\xea' | b'\xeb' | b'\xec' | b'\xed' | b'\xee' | b'\xef' | b'\xf0' | b'\xf1' | b'\xf2' | b'\xf3' | b'\xf4' | b'\xf5' | b'\xf6' | b'\xf7' | b'\xf8' | b'\xf9' | b'\xfa' | b'\xfb' | b'\xfc' | b'\xfd' | b'\xfe' | b'\xff')  # not b'\x00'
                  <Data> ::= <char>*  # len(<Data>) == ord(str(<Size_1>)); see below
              <BlockTerminator_1> ::= b'\x00'
      <GraphicControlExtension> ::= <GRAPHICCONTROLEXTENSION>
        <GRAPHICCONTROLEXTENSION> ::= <ExtensionIntroducer_1> <GraphicControlLabel_1> <GraphicControlSubBlock> <BlockTerminator_2>
          <ExtensionIntroducer_1> ::= b'!'
          <GraphicControlLabel_1> ::= b'\xf9'
          <GraphicControlSubBlock> ::= <GRAPHICCONTROLSUBBLOCK>
            <GRAPHICCONTROLSUBBLOCK> ::= <BlockSize> <PackedFields_2> <DelayTime> <TransparentColorIndex>
              <BlockSize> ::= <UBYTE>
              <PackedFields_2> ::= <GRAPHICCONTROLEXTENSION_DATASUBBLOCK_PACKEDFIELDS>
                <GRAPHICCONTROLEXTENSION_DATASUBBLOCK_PACKEDFIELDS> ::= <Reserved_1> <DisposalMethod> <UserInputFlag> <TransparentColorFlag>
                  <Reserved_1> ::= <bit>{3}
                  <DisposalMethod> ::= <bit>{3}
                  <UserInputFlag> ::= <bit>
                  <TransparentColorFlag> ::= <bit>
              <DelayTime> ::= <ushort>
              <TransparentColorIndex> ::= <UBYTE>
          <BlockTerminator_2> ::= <UBYTE>
      <CommentExtension> ::= <COMMENTEXTENSION>
        <COMMENTEXTENSION> ::= <ExtensionIntroducer_3> <CommentLabel_1> <CommentData>
          <ExtensionIntroducer_3> ::= b'!'
          <CommentLabel_1> ::= b'\xfe'
          <CommentData> ::= <DATASUBBLOCKS>
      <PlainTextExtension> ::= <PLAINTEXTEXTENTION>
        <PLAINTEXTEXTENTION> ::= <ExtensionIntroducer_5> <PlainTextLabel_1> <PlainTextSubBlock> <PlainTextData>
          <ExtensionIntroducer_5> ::= b'!'
          <PlainTextLabel_1> ::= b'\x01'
          <PlainTextSubBlock> ::= <PLAINTEXTSUBBLOCK>
            <PLAINTEXTSUBBLOCK> ::= <BlockSize_1> <TextGridLeftPosition> <TextGridTopPosition> <TextGridWidth> <TextGridHeight> <CharacterCellWidth> <CharacterCellHeight> <TextForegroundColorIndex> <TextBackgroundColorIndex>
              <BlockSize_1> ::= <UBYTE>
              <TextGridLeftPosition> ::= <ushort>
              <TextGridTopPosition> ::= <ushort>
              <TextGridWidth> ::= <ushort>
              <TextGridHeight> ::= <ushort>
              <CharacterCellWidth> ::= <UBYTE>
              <CharacterCellHeight> ::= <UBYTE>
              <TextForegroundColorIndex> ::= <UBYTE>
              <TextBackgroundColorIndex> ::= <UBYTE>
          <PlainTextData> ::= <DATASUBBLOCKS>
      <ApplicationExtension> ::= <APPLICATIONEXTENTION>
        <APPLICATIONEXTENTION> ::= <ExtensionIntroducer_7> <ApplicationLabel_1> <ApplicationSubBlock> <ApplicationData>
          <ExtensionIntroducer_7> ::= b'!'
          <ApplicationLabel_1> ::= b'\xff'
          <ApplicationSubBlock> ::= <APPLICATIONSUBBLOCK>
            <APPLICATIONSUBBLOCK> ::= <BlockSize_2> <ApplicationIdentifier> <ApplicationAuthenticationCode>
              <BlockSize_2> ::= <UBYTE>
              <ApplicationIdentifier> ::= <char>{8}
              <ApplicationAuthenticationCode> ::= <char>{3}
          <ApplicationData> ::= <DATASUBBLOCKS>
      <UndefinedData> ::= <UNDEFINEDDATA>
        <UNDEFINEDDATA> ::= <ExtensionIntroducer_9> <Label> <DataSubBlocks_1>
          <ExtensionIntroducer_9> ::= (b'\x00' | b'\x01' | b'\x02' | b'\x03' | b'\x04' | b'\x05' | b'\x06' | b'\x07' | b'\x08' | b'\t' | b'\n' | b'\x0b' | b'\x0c' | b'\r' | b'\x0e' | b'\x0f' | b'\x10' | b'\x11' | b'\x12' | b'\x13' | b'\x14' | b'\x15' | b'\x16' | b'\x17' | b'\x18' | b'\x19' | b'\x1a' | b'\x1b' | b'\x1c' | b'\x1d' | b'\x1e' | b'\x1f' | b' ' | b'"' | b'#' | b'$' | b'%' | b'&' | b"'" | b'(' | b')' | b'*' | b'+' | b',' | b'-' | b'.' | b'/' | b'0' | b'1' | b'2' | b'3' | b'4' | b'5' | b'6' | b'7' | b'8' | b'9' | b':' | b';' | b'<' | b'=' | b'>' | b'?' | b'@' | b'A' | b'B' | b'C' | b'D' | b'E' | b'F' | b'G' | b'H' | b'I' | b'J' | b'K' | b'L' | b'M' | b'N' | b'O' | b'P' | b'Q' | b'R' | b'S' | b'T' | b'U' | b'V' | b'W' | b'X' | b'Y' | b'Z' | b'[' | b'\\' | b']' | b'^' | b'_' | b'`' | b'a' | b'b' | b'c' | b'd' | b'e' | b'f' | b'g' | b'h' | b'i' | b'j' | b'k' | b'l' | b'm' | b'n' | b'o' | b'p' | b'q' | b'r' | b's' | b't' | b'u' | b'v' | b'w' | b'x' | b'y' | b'z' | b'{' | b'|' | b'}' | b'~' | b'\x7f' | b'\x80' | b'\x81' | b'\x82' | b'\x83' | b'\x84' | b'\x85' | b'\x86' | b'\x87' | b'\x88' | b'\x89' | b'\x8a' | b'\x8b' | b'\x8c' | b'\x8d' | b'\x8e' | b'\x8f' | b'\x90' | b'\x91' | b'\x92' | b'\x93' | b'\x94' | b'\x95' | b'\x96' | b'\x97' | b'\x98' | b'\x99' | b'\x9a' | b'\x9b' | b'\x9c' | b'\x9d' | b'\x9e' | b'\x9f' | b'\xa0' | b'\xa1' | b'\xa2' | b'\xa3' | b'\xa4' | b'\xa5' | b'\xa6' | b'\xa7' | b'\xa8' | b'\xa9' | b'\xaa' | b'\xab' | b'\xac' | b'\xad' | b'\xae' | b'\xaf' | b'\xb0' | b'\xb1' | b'\xb2' | b'\xb3' | b'\xb4' | b'\xb5' | b'\xb6' | b'\xb7' | b'\xb8' | b'\xb9' | b'\xba' | b'\xbb' | b'\xbc' | b'\xbd' | b'\xbe' | b'\xbf' | b'\xc0' | b'\xc1' | b'\xc2' | b'\xc3' | b'\xc4' | b'\xc5' | b'\xc6' | b'\xc7' | b'\xc8' | b'\xc9' | b'\xca' | b'\xcb' | b'\xcc' | b'\xcd' | b'\xce' | b'\xcf' | b'\xd0' | b'\xd1' | b'\xd2' | b'\xd3' | b'\xd4' | b'\xd5' | b'\xd6' | b'\xd7' | b'\xd8' | b'\xd9' | b'\xda' | b'\xdb' | b'\xdc' | b'\xdd' | b'\xde' | b'\xdf' | b'\xe0' | b'\xe1' | b'\xe2' | b'\xe3' | b'\xe4' | b'\xe5' | b'\xe6' | b'\xe7' | b'\xe8' | b'\xe9' | b'\xea' | b'\xeb' | b'\xec' | b'\xed' | b'\xee' | b'\xef' | b'\xf0' | b'\xf1' | b'\xf2' | b'\xf3' | b'\xf4' | b'\xf5' | b'\xf6' | b'\xf7' | b'\xf8' | b'\xf9' | b'\xfa' | b'\xfb' | b'\xfc' | b'\xfd' | b'\xfe' | b'\xff')  # not b'!'
          <Label> ::= <UBYTE>
          <DataSubBlocks_1> ::= <DATASUBBLOCKS>
  <Trailer> ::= <TRAILER>
    <TRAILER> ::= <GIFTrailer_1>
      <GIFTrailer_1> ::= b';'

# where len(<Data>) == ord(str(<Size_1>))
# where <GifHeader>..<Signature> == "GIF"

# FIXME: ReadRGB()
# FIXME: ReadUByte()
# FIXME: size = 
# FIXME: ReadUByte()
# FIXME: size = 
# FIXME: Warning()
# FIXME: size = 1
# FIXME: size = 2
# FIXME: ReadUByte()
# FIXME: ReadUByte()
# FIXME: size = 1
# FIXME: size = 2
# FIXME: ReadUShort()
# FIXME: ReadUShort()
# FIXME: ReadUShort()
# FIXME: ReadUShort()

