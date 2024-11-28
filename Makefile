# Fandango Makefile. For development only.

MAKEFLAGS=--warn-undefined-variables
PYTHON = python
ANTLR = antlr
BLACK = black
PIP = pip
SED = sed


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
	pip install -U jupyter-book pyppeteer ghp-import pagelabels
	brew install pdftk 

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
DOCS_SOURCES = $(wildcard $(DOCS)/*.md $(DOCS)/*.fan $(DOCS)/*.ipynb $(DOCS)/*.yml $(DOCS)/*.bib Makefile)
JB = jupyter-book
HTML_MARKER = $(DOCS)/_build/html/marker.txt
LATEX_MARKER = $(DOCS)/_build/latex/marker.txt
PDF_RAW = $(DOCS)/_build/latex/fandango.pdf
PDF_TARGET = $(DOCS)/fandango.pdf

# Command to open and refresh the Web view (on a Mac)
VIEW_HTML = open $(DOCS)/_build/html/index.html
REFRESH_HTML = osascript -e 'tell application "Safari" to set URL of document of window 1 to URL of document of window 1'

# Command to open the PDF (on a Mac)
VIEW_PDF = open $(PDF_TARGET)


# Targets.
html: $(HTML_MARKER)
latex: $(LATEX_MARKER)
pdf: $(PDF_TARGET)

# Re-create the book in HTML
$(HTML_MARKER): $(DOCS_SOURCES)
	$(JB) build $(DOCS)
	echo 'Success' > $@
	$(REFRESH_HTML)

# view HTML
view: $(HTML_MARKER)
	$(VIEW_HTML)

# Refresh Safari
refresh: $(HTML_MARKER)
	$(REFRESH_HTML)
	

# Re-create the book in PDF
$(LATEX_MARKER): $(DOCS_SOURCES) $(DOCS)/_book_toc.yml
	cd $(DOCS); $(JB) build --builder latex --toc _book_toc.yml .
	echo 'Success' > $@
	
$(DOCS)/_book_toc.yml: $(DOCS)/_toc.yml
	echo '# Automatically generated from `$<`. Do not edit.' > $@
	$(SED) s/Intro/BookIntro/ $< >> $@

$(PDF_RAW): $(LATEX_MARKER)
	cd $(DOCS)/_build/latex && $(MAKE)

PDF_BODY = $(DOCS)/_build/latex/_body.pdf
$(PDF_BODY): $(DOCS)/Title.pdf $(PDF_RAW)
	pdftk $(PDF_RAW) cat 3-end output $@

PAGELABELS = python3 -m pagelabels
$(PDF_TARGET): $(PDF_BODY)
	pdftk $(DOCS)/Title.pdf $(PDF_BODY) cat output $@
	$(PAGELABELS) --load $(PDF_RAW) $@

view-pdf: $(PDF_TARGET)
	$(VIEW_PDF)

clean-docs:
	$(JB) clean $(DOCS)

rebuild-docs:
	$(JB) build --all $(DOCS)


## Installation

install:
	$(PIP) install -e .

