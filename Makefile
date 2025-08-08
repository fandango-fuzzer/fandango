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
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz mermaid-cli
TEST_TOOLS =  # clang is installed by default on Mac
SYSTEM_DEV_INSTALL = brew install
else ifeq ($(UNAME), Linux)
# Linux
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz mermaid-cli
TEST_TOOLS = clang
SYSTEM_DEV_INSTALL = apt-get install
else ifneq (,$(findstring NT,$(UNAME)))
# Windows (all variants): Windows_NT, MINGW64_NT-10.0-20348, MSYS_NT-10.0-20348
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz mermaid-cli
TEST_TOOLS = llvm # this is the easiest way to install clang on windows
SYSTEM_DEV_INSTALL = choco install
else
$(error Unsupported OS: $(UNAME))
endif


dev-tools: system-dev-tools
	$(PIP) install -e ".[development]"

system-dev-tools:
	$(SYSTEM_DEV_INSTALL) $(SYSTEM_DEV_TOOLS) $(TEST_TOOLS)

test-tools:
ifneq ($(TEST_TOOLS),)
	$(SYSTEM_DEV_INSTALL) $(TEST_TOOLS)
endif

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
		-visitor -no-listener $(LEXER_G4)
	sed 's/import FandangoLexerBase/import */' $@ > $@~ && mv $@~ $@

$(PARSER)/FandangoParser.py: $(LEXER_G4) $(PARSER_G4) Makefile
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER) \
		-visitor -no-listener $(PARSER_G4)
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
JB = JUPYTER_BOOK=1 jupyter-book
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
CHECK_DOCS = grep -l AssertionError $(DOCS)/_build/html/*.html; if [ $$? == 0 ]; then echo '*** Check the above files for failed assertions'; false; else true; fi

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

.PHONY: test tests
# As above, but run tests in parallel
tests $(TEST_MARKER): $(PYTHON_SOURCES) $(TEST_SOURCES)
	$(PYTEST)

COVERAGE = coverage.xml
COVERAGERC = .coveragerc
REPORT = report.html
COVERAGE_REPORT = htmlcov/index.html

# Run tests and generate coverage report
.PHONY: coverage
coverage $(COVERAGE_REPORT): $(PYTHON_SOURCES) $(TEST_SOURCES)
	$(PYTEST) --html=$(REPORT) --self-contained-html --cov-report xml:$(COVERAGE) --cov-report term --cov-config=$(COVERAGERC) --cov=fandango
	@echo 'Coverage report generated in $(COVERAGE_REPORT)'

run-tests: $(TEST_MARKER)

## Evaluation
EVALUATION = evaluation
EVALUATION_SOURCES = $(wildcard $(EVALUATION)/*.py $(EVALUATION)/*/*.py $(EVALUATION)/*/*/*.py $(EVALUATION)/*/*/*.fan $(EVALUATION)/*/*/*.txt)

# python -m evaluation.vs_isla.run_evaluation
.PHONY: evaluation
evaluation $(EVALUATION_MARKER): $(PYTHON_SOURCES) $(EVALUATION_SOURCES)
	$(PYTHON) -m evaluation.run_evaluation 1

## All
.PHONY: run-all
run-all: $(TEST_MARKER) $(EVALUATION_MARKER)

## Installation
.PHONY: install
install:
	$(PIP) install -e .

uninstall:
	$(PIP) uninstall fandango-fuzzer -y

remove cache:
	rm -rf ~/Library/Caches/Fandango

GIT_LS_FILES = git ls-files --exclude-standard | \
	grep ".*$$pattern"'$$' | \
	grep -v 'src/fandango/language/parser/' | \
	grep -v 'src/fandango/language/cpp_parser/' | \
	grep -v 'src/fandango/converters/dtd/[^.]*\.fan' | \
	grep -v 'src/fandango/converters/antlr/ANTLRv4[^.]*\.py' | \
	grep -v 'src/fandango/converters/antlr/LexerAdaptor[^.]*\.py'

.PHONY: ls-files
ls-files:
	@echo 'Listing files in the repository...'
	@$(GIT_LS_FILES) | sort

## Statistics
.PHONY: stats statistics
stats statistics:
	@for pattern in .py .g4 .md .fan .yml file; do \
		printf "%12s" "*$$pattern lines:"; \
		$(GIT_LS_FILES) | \
		xargs wc -l | grep ' total$$'; \
	done
	@printf '  All lines:'
	@$(GIT_LS_FILES) | \
	grep -E '(\.py|\.g4|\.md|\.fan|\.yml|file)$$' | xargs wc -l | grep ' total$$'

## Credit - from https://gist.github.com/Alpha59/4e9cd6c65f7aa2711b79
.PHONY: credits
credits:
	@echo "Lines contributed"
	@for pattern in .py .g4 .md .fan .toml .yml file; do \
		echo "*$$pattern files:"; \
		$(GIT_LS_FILES) | \
		xargs -n1 git blame -wfn | \
		sed 's/joszamama/José Antonio/g' | \
		sed 's/Leon/Leon Bettscheider/g' | \
		sed 's/alex9849/Alexander Liggesmeyer/g' | \
		perl -n -e '/\((.*)\s[\d]{4}\-/ && print $$1."\n"' | \
		awk '{print $$1" "$$2}' | \
		sed 's/José Antonio$$/José Antonio Zamudio Amaya/g' | \
		sort -f | \
		uniq -c | \
		sort -nr; \
		echo; \
	done
