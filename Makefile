# Fandango Makefile. For development only.

# Settings
MAKEFLAGS=--warn-undefined-variables

# Programs
PYTHON = python
PYTEST = pytest
BLACK = black
PIP = $(PYTHON) -m pip
SED = sed
PAGELABELS = $(PYTHON) -m pagelabels
ANTLR = antlr

# Sources
SRC = src/fandango
PYTHON_SOURCES = $(wildcard $(SRC)/*.py $(SRC)/*/*.py $(SRC)/*/*/*.py)

# Default targets
web: package-info html
all: package-info parser html web pdf

.PHONY: web all parser install dev-tools docs html latex pdf

## Package info
EGG_INFO = src/fandango_fuzzer.egg-info

.PHONY: package-info
package-info: $(EGG_INFO)/PKG-INFO
$(EGG_INFO)/PKG-INFO: pyproject.toml
	$(PIP) install -e .

# Install tools for development
UNAME_DETECTED := $(OS)
ifdef UNAME_DETECTED
UNAME := $(UNAME_DETECTED)
else
UNAME := $(shell uname)
endif

ifeq ($(UNAME), Darwin)
# Mac
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz uv telnet
TEST_TOOLS = llvm@20 # clang is installed by default on Mac
SYSTEM_DEV_INSTALL = brew install
else ifeq ($(UNAME), Linux)
# Linux
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz
TEST_TOOLS = clang llvm
SYSTEM_DEV_INSTALL = apt-get install -y
ANTLR = antlr4
else ifneq (,$(findstring NT,$(UNAME)))
# Windows (all variants): Windows_NT, MINGW64_NT-10.0-20348, MSYS_NT-10.0-20348
SYSTEM_DEV_TOOLS = antlr pdftk-java graphviz uv
TEST_TOOLS = llvm # this is the easiest way to install clang on windows
SYSTEM_DEV_INSTALL = choco install
ANTLR = java -jar .\dev-dependencies\antlr-4.13.2-complete.jar
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
	$(MAKE) fcc-local

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
ifeq ($(UNAME), Windows_NT)
	powershell -Command "(Get-Content '$@') -replace 'import FandangoLexerBase', 'import *' | Set-Content '$@'"
else
	sed 's/import FandangoLexerBase/import */' $@ > $@~ && mv $@~ $@
endif

$(PARSER)/FandangoParser.py: $(LEXER_G4) $(PARSER_G4) Makefile
	$(ANTLR) -Dlanguage=Python3 -Xexact-output-dir -o $(PARSER) \
		-visitor -no-listener $(PARSER_G4)
	$(BLACK) $(SRC)/language

$(CPP_PARSER)/FandangoLexer.cpp: $(LEXER_G4) Makefile
	$(ANTLR) -Dlanguage=Cpp -Xexact-output-dir -o $(CPP_PARSER) \
		$(LEXER_G4)
ifeq ($(UNAME), Windows_NT)
	powershell -Command "$$content = Get-Content '$(CPP_PARSER)/FandangoLexer.h' -Raw; $$content = $$content -replace '(#include\s+\"antlr4-runtime\.h\")', ('$$1' + [Environment]::NewLine + '#include \"FandangoLexerBase.h\"'); $$content | Set-Content '$(CPP_PARSER)/FandangoLexer.h' -NoNewline"
else
	sed -e '/^#include/a\'$$'\n''#include "FandangoLexerBase.h"' $(CPP_PARSER)/FandangoLexer.h > $(CPP_PARSER)/FandangoLexer.h~ && mv $(CPP_PARSER)/FandangoLexer.h~ $(CPP_PARSER)/FandangoLexer.h
endif


$(CPP_PARSER)/FandangoParser.cpp: $(LEXER_G4) $(PARSER_G4) $(SRC)/language/generate-parser.py Makefile
	$(ANTLR) -Dlanguage=Cpp -Xexact-output-dir -o $(CPP_PARSER) \
		-visitor -no-listener $(PARSER_G4)
	cd $(SRC)/language && $(PYTHON) generate-parser.py
	$(BLACK) $(SRC)/language
	@echo 'Now run "pip install -e ." to compile C++ files'

.PHONY: format black
format black:
	$(BLACK) src

## Documentation
DOCS = docs
DOCS_SOURCES = $(wildcard $(DOCS)/*.md $(DOCS)/*.fan $(DOCS)/*.ipynb $(DOCS)/*.yml $(DOCS)/*.bib)
JB = JUPYTER_BOOK=1 FANDANGO_RAISE_ALL_EXCEPTIONS=1 FANDANGO_RUN_BEARTYPE=1 jupyter-book
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
CHECK_DOCS = \
	[ -f docs/_build/html/reports/*.err.log ] && \
	grep -R -n -C 20 "AssertionError" docs/_build/html/reports/*.err.log; \
	[ $$? -eq 1 ]

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

LLVM_MIN_VERSION := 18
LLVM_MAX_VERSION := 20
# This is an ugly ugly hack to access the correct llvm version.
# If you need to adjust this, you probably also need to touch tests/test_execution_feedback.py.
# If you read this and know how to: please make this nicer!
# The trouble is that macOS has an incompatible default llvm version installed.
LLVM_CONFIG_SEARCH_PATH := /opt/homebrew/opt/llvm@20/bin:/opt/homebrew/opt/llvm@19/bin:/opt/homebrew/opt/llvm@18/bin:/usr/local/opt/llvm@20/bin:/usr/local/opt/llvm@19/bin:/usr/local/opt/llvm@18/bin
LLVM_CONFIG := $(shell PATH="$(LLVM_CONFIG_SEARCH_PATH):$$PATH" command -v llvm-config 2>/dev/null || true)
LLVM_BIN_DIR := $(dir $(LLVM_CONFIG))

.PHONY: fcc
# Build fcc, but don't install it globally to not pollute the system
fcc-local:
ifneq (,$(findstring NT,$(UNAME)))
	@echo "Skipping fcc install on Windows"
else
	@LLVM_VERSION="$$( "$(LLVM_CONFIG)" --version 2>/dev/null )"; \
	LLVM_MAJOR="$${LLVM_VERSION%%.*}"; \
	echo "Required LLVM version: $(LLVM_MIN_VERSION)-$(LLVM_MAX_VERSION)"; \
	echo "Using llvm-config: $(LLVM_CONFIG)"; \
	echo "Detected LLVM version: $$LLVM_VERSION"; \
	if [ -z "$$LLVM_VERSION" ]; then \
		echo "Error: llvm-config not found (or not executable)"; \
		exit 1; \
	fi; \
	if [ "$$LLVM_MAJOR" -lt "$(LLVM_MIN_VERSION)" ] || [ "$$LLVM_MAJOR" -gt "$(LLVM_MAX_VERSION)" ]; then \
		echo "Error: unsupported LLVM version $$LLVM_VERSION (need $(LLVM_MIN_VERSION)-$(LLVM_MAX_VERSION))"; \
		exit 1; \
	fi; \
	if [ ! -d fcc ]; then \
		git clone https://github.com/fandango-fuzzer/fcc.git; \
	else \
		cd fcc && git pull && cd ..; \
	fi; \
	PATH="$(LLVM_BIN_DIR):$$PATH" LLVM_CONFIG_PATH="$(LLVM_CONFIG)" make -C fcc install-local
endif

# Build and install fcc globally
fcc: fcc-local
	PATH="$(LLVM_BIN_DIR):$$PATH" LLVM_CONFIG_PATH="$(LLVM_CONFIG)" make -C fcc install
	
## All
.PHONY: run-all
run-all: $(TEST_MARKER) $(EVALUATION_MARKER)

## Installation
.PHONY: install
install:
	rm -f src/fandango/language/parser/sa_fandango_cpp_parser*.so
	rm -f src/fandango/language/parser/sa_fandango_cpp_parser*.pdy
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
