# Fandango Makefile. For development only.

MAKEFLAGS=--warn-undefined-variables
PYTHON = python
ANTLR = antlr
BLACK = black
PIP = pip


# Default targets
all: requirements.txt parser html
.PHONY: parser install dev-tools docs latex pdf


## Requirements

requirements.txt:	pyproject.toml
	pip-compile $<

# Install the necessary tools
dev-tools:
	brew install antlr
	pip install -U black
	pip install -U jupyter-book pyppeteer ghp-import

## Parser

PARSER = src/fandango/language/parser
LEXER_G4 = language/FandangoLexer.g4
PARSER_G4 = language/FandangoParser.g4

PARSERS = \
	$(PARSER)/FandangoLexer.py \
	$(PARSER)/FandangoParser.py \
	$(PARSER)/FandangoParserVisitor.py \
	$(PARSER)/FandangoParserListener.py

parser: $(PARSERS)

$(PARSERS) &: $(LEXER_G4) $(PARSER_G4)
	# $(PYTHON) scripts/update-grammar.py
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER) \
		-visitor -listener $(LEXER_G4) $(PARSER_G4)
	$(BLACK) src


## Documentation
DOCS = docs
DOCS_SOURCES = $(wildcard $(DOCS)/*.md $(DOCS)/*.ipynb $(DOCS)/*.yml $(DOCS)/*.bib Makefile)
JB = jupyter-book
HTML_MARKER = $(DOCS)/_build/html/marker.txt
LATEX_MARKER = $(DOCS)/_build/latex/marker.txt

# Command to refresh the Web view
REFRESH_HTML = osascript -e 'tell application "Safari" to set URL of document of window 1 to URL of document of window 1'

# Targets.
html: $(HTML_MARKER)
latex: $(LATEX_MARKER)
pdf: $(DOCS)/_build/latex/fandango.pdf
	

# Re-create the book in HTML
$(HTML_MARKER): $(DOCS_SOURCES)
	$(JB) build $(DOCS)
	echo 'Success' > $@
	$(REFRESH_HTML)

# view HTML
view: $(HTML_MARKER)
	open _build/html/index.html

# Refresh Safari
refresh: $(HTML_MARKER)
	$(REFRESH_HTML)
	

# Re-create the book in PDF
$(LATEX_MARKER): $(DOCS_SOURCES)
	$(JB) build --builder latex $(DOCS)
	echo 'Success' > $@

$(DOCS)/_build/latex/fandango.pdf: $(LATEX_MARKER)
	cd $(DOCS)/_build/latex && $(MAKE)

# clean:
# 	$(JB) clean $(BOOK)
#
# rebuild:
# 	$(JB) build --all $(BOOK)


## Installation

install:
	$(PIP) install -e .

