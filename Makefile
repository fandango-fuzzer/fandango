# Fandango Makefile. For development only.

MAKEFLAGS=--warn-undefined-variables
PYTHON = python
ANTLR = antlr
BLACK = black
PIP = pip

targets: requirements.txt parser install
.PHONY: parser install


## Requirements

requirements.txt:	pyproject.toml
	pip-compile $<


## Parser

PARSER_DIR = src/fandango/language/parser
LEXER_G4 = language/FandangoLexer.g4
PARSER_G4 = language/FandangoParser.g4

PARSERS = \
	$(PARSER_DIR)/FandangoLexer.py \
	$(PARSER_DIR)/FandangoParser.py \
	$(PARSER_DIR)/FandangoParserVisitor.py \
	$(PARSER_DIR)/FandangoParserListener.py

parser: $(PARSERS)

$(PARSERS) &: $(LEXER_G4) $(PARSER_G4)
	# $(PYTHON) scripts/update-grammar.py
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER_DIR) \
		-visitor -listener $(LEXER_G4) $(PARSER_G4)
	$(BLACK) src


## Installation

install:
	$(PIP) install -e .
