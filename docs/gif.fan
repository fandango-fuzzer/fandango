# Automatically generated from 'gif.bt' by bt2fan. Do not edit.
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
                  <Size_1> ::= br'[^\x00]'
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
          <ExtensionIntroducer_9> ::= br'[^!]'
          <Label> ::= <UBYTE>
          <DataSubBlocks_1> ::= <DATASUBBLOCKS>
  <Trailer> ::= <TRAILER>
    <TRAILER> ::= <GIFTrailer_1>
      <GIFTrailer_1> ::= b';'

# where len(<Data>) == ord(str(<Size_1>))
# where not (<GifHeader>.<Signature> != "GIF")

# FIXME: ReadRGB()
# FIXME: ReadUByte()
# FIXME: size = 
# FIXME: ReadUByte()
# FIXME: size = 
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

