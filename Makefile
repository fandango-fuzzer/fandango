# Fandango Makefile. For development only.

# Settings
MAKEFLAGS=--warn-undefined-variables

# Programs
PYTHON = python
ANTLR = antlr
BLACK = black
PIP = pip
SED = sed
PAGELABELS = $(PYTHON) -m pagelabels


# Default targets
web: requirements.txt parser html
all: web pdf

.PHONY: web all parser install dev-tools docs html latex pdf


## Requirements

requirements.txt:	pyproject.toml
	pip-compile $<

# Install tools for development
UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
# Mac
SYSTEM_DEV_TOOLS = antlr pdftk graphviz
SYSTEM_DEV_INSTALL = brew install
else
# Linux
SYSTEM_DEV_TOOLS = antlr pdftk graphviz
SYSTEM_DEV_INSTALL = apt-get install
endif


dev-tools: system-dev-tools
	pip install -U black
	pip install -U jupyter-book pyppeteer ghp-import pagelabels 
	pip install -U graphviz

system-dev-tools:
	$(SYSTEM_DEV_INSTALL) $(SYSTEM_DEV_TOOLS)


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
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER) \
		-visitor -listener $(LEXER_G4) $(PARSER_G4)
	$(BLACK) src


## Documentation
DOCS = docs
DOCS_SOURCES = $(wildcard $(DOCS)/*.md $(DOCS)/*.fan $(DOCS)/*.ipynb $(DOCS)/*.yml $(DOCS)/*.bib)
JB = jupyter-book
HTML_MARKER = $(DOCS)/_build/html/marker.txt
ALL_HTML_MARKER = $(DOCS)/_build/html/all-marker.txt
LATEX_MARKER = $(DOCS)/_build/latex/marker.txt
PDF_RAW = $(DOCS)/_build/latex/fandango.pdf
PDF_TARGET = $(DOCS)/fandango.pdf

# Command to open and refresh the Web view (on a Mac)
HTML_INDEX = $(DOCS)/_build/html/index.html
VIEW_HTML = open $(HTML_INDEX)
REFRESH_HTML = osascript -e 'tell application "Safari" to set URL of document of window 1 to URL of document of window 1'

# Command to open the PDF (on a Mac)
VIEW_PDF = open $(PDF_TARGET)


# Targets.
html: $(HTML_MARKER)
latex: $(LATEX_MARKER)
pdf: $(PDF_TARGET)

# Re-create the book in HTML
$(HTML_MARKER): $(DOCS_SOURCES) $(ALL_HTML_MARKER)
	$(JB) build $(DOCS)
	echo 'Success' > $@
	-$(REFRESH_HTML)
	@echo Output written to $(HTML_INDEX)

# If we change _toc.yml, all tocs need to be rebuilt
$(ALL_HTML_MARKER): $(DOCS)/_toc.yml
	$(JB) build --all $(DOCS)
	echo 'Success' > $@

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
	
$(DOCS)/_book_toc.yml: $(DOCS)/_toc.yml Makefile
	echo '# Automatically generated from `$<`. Do not edit.' > $@
	$(SED) s/Intro/BookIntro/ $< >> $@

$(DOCS)/_book_toc.yml: $(DOCS)/_toc.yml
	echo '# Automatically generated from `$<`. Do not edit.' > $@
	$(SED) s/Intro/BookIntro/ $< >> $@

$(PDF_RAW): $(LATEX_MARKER)
	cd $(DOCS)/_build/latex && $(MAKE) && cd ../../.. && touch $@

PDF_BODY = $(DOCS)/_build/latex/_body.pdf
$(PDF_BODY): $(DOCS)/Title.pdf $(PDF_RAW)
	pdftk $(PDF_RAW) cat 3-end output $@

$(PDF_TARGET): $(PDF_BODY)
	pdftk $(DOCS)/Title.pdf $(PDF_BODY) cat output $@
	$(PAGELABELS) --load $(PDF_RAW) $@
	@echo Output written to $@

view-pdf: $(PDF_TARGET)
	$(VIEW_PDF)

clean-docs:
	$(JB) clean $(DOCS)



## Installation

install:
	$(PIP) install -e .

