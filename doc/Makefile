# Makefile for automatic builds

BOOK_SOURCES=$(wildcard *.md *.ipynb *.yml *.bib Makefile)
JB=jupyter-book
BOOK=../doc

# Targets.
default: html
html: _build/html refresh
latex: _build/latex/fandangobook.pdf

.PHONY: default html latex refresh clean install
	
# Install the necessary tools
install:
	pip install -U jupyter-book pyppeteer ghp-import 

# Re-create the book in HTML
_build/html: $(BOOK_SOURCES)
	$(JB) build $(BOOK)

# Refresh Safari
refresh: _build/html
	osascript -e 'tell application "Safari" to set URL of document of window 1 to URL of document of window 1'
	

# Re-create the book in PDF
_build/latex: $(BOOK_SOURCES)
	$(JB) --builder latex $(BOOK)

_build/latex/fandangobook.pdf: _build/latex
	cd _build/latex && $(MAKE)

clean:
	$(JB) clean $(BOOK)
