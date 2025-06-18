PYTHON = python3
SED = sed
ANTLR = antlr

all: ANTLRv4Lexer.py ANTLRv4Parser.py

ANTLRv4Lexer.g4: ANTLRv4LexerOrig.g4
	echo '// Generated from $?. Do not edit.' > $@
	$(SED) 's/this\./self\./g' $? >> $@

ANTLRv4Lexer.py: ANTLRv4Lexer.g4
	$(ANTLR) -Dlanguage=Python3 -visitor $?

ANTLRv4Parser.py: ANTLRv4Parser.g4
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor $?

clean:
	$(RM) ANTLRv4Lexer.g4 \
	ANTLRv4Lexer.py ANTLRv4Lexer.interp ANTLRv4Lexer.tokens \
	ANTLRv4Parser.py ANTLRv4ParserVisitor.py ANTLRv4Parser.interp ANTLRv4Parser.tokens
