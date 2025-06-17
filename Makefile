# Fandango Makefile. For development only.

# Settings
MAKEFLAGS=--warn-undefined-variables

# Programs
PYTHON = python
PYTEST = pytest
ANTLR = antlr
BLACK = black
PIP = pip
SED = sed
PAGELABELS = $(PYTHON) -m pagelabels

# Sources
SRC = src/fandango
PYTHON_SOURCES = $(wildcard $(SRC)/*.py $(SRC)/*/*.py $(SRC)/*/*/*.py)

# Default targets
web: package-info parser html
all: package-info parser html web pdf

.PHONY: web all parser install dev-tools docs html latex pdf


## Requirements (no longer used)

# requirements.txt:	pyproject.toml
# 	pip-compile $<


## Package info
EGG_INFO = src/fandango_fuzzer.egg-info

.PHONY: package-info
package-info: $(EGG_INFO)/PKG-INFO
$(EGG_INFO)/PKG-INFO: pyproject.toml
	$(PIP) install -e .

# Install tools for development
UNAME := $(shell uname)
ifeq ($(UNAME), Darwin)
# Mac
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz
SYSTEM_DEV_INSTALL = brew install
else
# Linux
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz
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
CPP_PARSER = src/fandango/language/cpp_parser
LEXER_G4 = language/FandangoLexer.g4
PARSER_G4 = language/FandangoParser.g4

parser: \
	$(PARSER)/FandangoLexer.py \
	$(PARSER)/FandangoParser.py \
	$(CPP_PARSER)/FandangoLexer.cpp \
	$(CPP_PARSER)/FandangoParser.cpp

$(PARSER)/FandangoLexer.py: $(LEXER_G4) Makefile
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER) \
		-visitor -listener $(LEXER_G4)
	sed 's/import FandangoLexerBase/import */' $@ > $@~ && mv $@~ $@

$(PARSER)/FandangoParser.py: $(LEXER_G4) $(PARSER_G4) Makefile
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER) \
		-visitor -listener $(PARSER_G4)
	$(BLACK) $(SRC)/language

$(CPP_PARSER)/FandangoLexer.cpp: $(LEXER_G4) Makefile
	$(ANTLR) -Dlanguage=Cpp -Xexact-output-dir -o $(CPP_PARSER) \
		$(LEXER_G4)
	sed -e '/^#include/a\'$$'\n''#include "FandangoLexerBase.h"' $(CPP_PARSER)/FandangoLexer.h > $(CPP_PARSER)/FandangoLexer.h~ && mv $(CPP_PARSER)/FandangoLexer.h~ $(CPP_PARSER)/FandangoLexer.h

$(CPP_PARSER)/FandangoParser.cpp: $(LEXER_G4) $(PARSER_G4) $(SRC)/language/generate-parser.py Makefile
	$(ANTLR) -Dlanguage=Cpp -Xexact-output-dir -o $(CPP_PARSER) \
		-visitor -no-listener $(PARSER_G4)
	cd $(SRC)/language; $(PYTHON) generate-parser.py
	$(BLACK) $(SRC)/language
	@echo 'Now run "pip install -e ." to compile C++ files'

.PHONY: format black
format black:
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
REFRESH_HTML = \
osascript -e 'tell application "Safari" to set URL of document of window 1 to URL of document of window 1'

# Command to open the PDF (on a Mac)
VIEW_PDF = open $(PDF_TARGET)

# Command to check docs for failed assertions
CHECK_DOCS = grep -l AssertionError $(DOCS)/_build/html/*.html; if [ $$? == 0 ]; then echo 'Check the above files for failed assertions'; false; else true; fi

# Command to patch HTML output
PATCH_HTML = cd $(DOCS); sh ./patch-html.sh

# Targets.
docs html: $(HTML_MARKER)
latex: $(LATEX_MARKER)
pdf: $(PDF_TARGET)

# Re-create the book in HTML
$(HTML_MARKER): $(DOCS_SOURCES) $(ALL_HTML_MARKER)
	$(JB) build $(DOCS)
	-$(PATCH_HTML)
	@$(CHECK_DOCS)
	echo 'Success' > $@
	@echo Output written to $(HTML_INDEX)

# If we change Python sources, _toc.yml, or _config.yml, all docs need to be rebuilt
$(ALL_HTML_MARKER): $(DOCS)/_toc.yml $(DOCS)/_config.yml $(PYTHON_SOURCES)
	$(JB) build --all $(DOCS)
	-$(PATCH_HTML)
	@$(CHECK_DOCS)
	echo 'Success' > $@


# Same as above, but also clear the cache
clear-cache:
	$(RM) -fr $(DOCS)/_build/

rebuild-docs: clear-cache $(ALL_HTML_MARKER)


# view HTML
view: $(HTML_MARKER)
	$(VIEW_HTML)

# Refresh Safari
refresh watch: $(HTML_MARKER)
	$(REFRESH_HTML)


# Re-create the book in PDF
$(LATEX_MARKER): $(DOCS_SOURCES) $(DOCS)/_book_toc.yml $(DOCS)/_book_config.yml
	cd $(DOCS); $(JB) build --builder latex --toc _book_toc.yml --config _book_config.yml .
	echo 'Success' > $@

$(DOCS)/_book_toc.yml: $(DOCS)/_toc.yml Makefile
	echo '# Automatically generated from `$<`. Do not edit.' > $@
	$(SED) s/Intro/BookIntro/ $< >> $@

$(DOCS)/_book_config.yml: $(DOCS)/_config.yml Makefile
	echo '# Automatically generated from `$<`. Do not edit.' > $@
	$(SED) s/BookIntro/Intro/ $< >> $@


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


## Tests
TESTS = tests
TEST_SOURCES = $(wildcard $(TESTS)/*.py $(TESTS)/resources/* $(TESTS)/docs/*.fan)
TEST_MARKER = $(TESTS)/test-marker.txt

.PHONY: test tests run-tests
test: $(PYTHON_SOURCES) $(TEST_SOURCES)
	$(PYTEST)
	echo 'Success' > $(TEST_MARKER)

# As above, but run tests in parallel
tests $(TEST_MARKER): $(PYTHON_SOURCES) $(TEST_SOURCES)
	$(PYTEST) -n auto
	echo 'Success' > $(TEST_MARKER)

run-tests: $(TEST_MARKER)

## Evaluation
EVALUATION = evaluation
EVALUATION_SOURCES = $(wildcard $(EVALUATION)/*.py $(EVALUATION)/*/*.py $(EVALUATION)/*/*/*.py $(EVALUATION)/*/*/*.fan $(EVALUATION)/*/*/*.txt)
EVALUATION_MARKER = $(EVALUATION)/test-evaluation.txt

# python -m evaluation.vs_isla.run_evaluation
.PHONY: evaluation evaluate
evaluation evaluate $(EVALUATION_MARKER): $(PYTHON_SOURCES) $(EVALUATION_SOURCES)
	$(PYTHON) -m evaluation.vs_isla.run_evaluation 1
	echo 'Success' > $(EVALUATION_MARKER)

run-evaluation: $(EVALUATION_MARKER)

## Experiments
EXPERIMENTS = $(EVALUATION)/experiments
EXPERIMENTS_SOURCES = $(wildcard $(EXPERIMENTS)/*/*.py $(EXPERIMENTS)/*/*.fan)
EXPERIMENTS_MARKER = $(EXPERIMENTS)/test-experiments.txt

.PHONY: experiment experiments
experiment experiments $(EXPERIMENTS_MARKER): $(PYTHON_SOURCES) $(EXPERIMENTS_SOURCES)
	$(PYTHON) -m evaluation.experiments.run_experiments
	echo 'Success' > $(EXPERIMENTS_MARKER)

run-experiments: $(EXPERIMENTS_MARKER)

## All
.PHONY: run-all
run-all: $(TEST_MARKER) $(EVALUATION_MARKER) $(EXPERIMENTS_MARKER)
	@echo 'All tests passed.'

## Installation
.PHONY: install install-test install-tests
install:
	$(PIP) install -e .

## Credit - from https://gist.github.com/Alpha59/4e9cd6c65f7aa2711b79
.PHONY: credit
credit:
	@echo "Lines contributed"
	@for pattern in .py .g4 .md .fan .toml .yml file; do \
		echo "*$$pattern files:"; \
		git ls-files | \
		grep "$$pattern"'$$' | \
		grep -v 'src/fandango/language/parser/' | \
		grep -v 'utils/dtd2fan/.*\.fan' | \
		xargs -n1 git blame -wfn | \
		sed 's/joszamama/José Antonio/g' | \
		sed 's/alex9849/Alexander Liggesmeyer/g' | \
		perl -n -e '/\((.*)\s[\d]{4}\-/ && print $$1."\n"' | \
		awk '{print $$1" "$$2}' | \
		sed 's/José Antonio$$/José Antonio Zamudio Amaya/g' | \
		sort -f | \
		uniq -c | \
		sort -nr; \
		echo; \
	done

# We separate _installing_ from _running_ tests
# so we can run 'make tests' quickly (see above)
# without having to reinstall things
install-test install-tests:
	$(PIP) install pytest mypy pytest-xdist
	$(PIP) install -e ".[test]"

uninstall:
	$(PIP) uninstall fandango-fuzzer -y

remove cache:
	rm -rf ~/Library/Caches/Fandango