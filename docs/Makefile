# Makefile for automatic builds

BOOK_SOURCES=$(wildcard *.md *.ipynb *.yml *.bib Makefile)
JB=jupyter-book
BOOK=../docs
HTML_MARKER=_build/html/marker.txt
LATEX_MARKER=_build/latex/marker.txt

# Targets.
default: html
html: $(HTML_MARKER) refresh
latex: $(LATEX_MARKER)
pdf: _build/latex/fandango.pdf

.PHONY: default html latex pdf refresh clean rebuild install
	
# Install the necessary tools
install:
	pip install -U jupyter-book pyppeteer ghp-import 

# Re-create the book in HTML
$(HTML_MARKER): $(BOOK_SOURCES)
	$(JB) build $(BOOK)
	echo 'Success' > $@

# view HTML
view: $(HTML_MARKER)
	open _build/html/index.html

# Refresh Safari
refresh: $(HTML_MARKER)
	osascript -e 'tell application "Safari" to set URL of document of window 1 to URL of document of window 1'
	

# Re-create the book in PDF
$(LATEX_MARKER): $(BOOK_SOURCES)
	$(JB) build --builder latex $(BOOK)
	echo 'Success' > $@

_build/latex/fandango.pdf: $(LATEX_MARKER)
	cd _build/latex && $(MAKE)

clean:
	$(JB) clean $(BOOK)

rebuild:
	$(JB) build --all $(BOOK)
