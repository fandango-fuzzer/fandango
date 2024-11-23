PYTHON = python
ANTLR = antlr
BLACK = black
PIP = pip
PARSER_DIR = src/fandango/language/parser

targets: requirements.txt parser install


## Requirements

requirements.txt:	pyproject.toml
	pip-compile $<


## Parser
	
LEXER = language/FandangoLexer.g4
PARSER = language/FandangoParser.g4

PARSERS = \
	$(PARSER_DIR)/FandangoLexer.py \
	$(PARSER_DIR)/FandangoParser.py \
	$(PARSER_DIR)/FandangoParserVisitor.py \
	$(PARSER_DIR)/FandangoParserListener.py

parser: $(PARSERS)

$(PARSERS): $(PARSER_SOURCES)
	# $(PYTHON) scripts/update-grammar.py
	$(ANTLR) -Dlanguage=Python3 -o $(PARSER_DIR) \
		-visitor -listener $(LEXER) $(PARSER)
	$(BLACK) src


## Installation

install:
	$(PIP) install -e .
