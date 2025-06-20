#include "FandangoLexerBase.h"
#include <assert.h>

const std::regex FandangoLexerBase::NEW_LINE_PATTERN("[^\r\n\f]+");
const std::regex FandangoLexerBase::SPACES_PATTERN("[\r\n\f]+");

FandangoLexerBase *FandangoLexerBase::lexer = nullptr;

FandangoLexerBase::FandangoLexerBase(antlr4::CharStream *input)
    : Lexer(input) {
    tokens.clear();
    indents.clear();
    opened = 0;
    inPython = 0;
    isFstring = false;
    skipLexer = 0;

    lexer = this;
}

void FandangoLexerBase::reset() {
    tokens.clear();
    indents.clear();
    opened = 0;
    inPython = 0;
    isFstring = false;
    skipLexer = 0;

    Lexer::reset();
}

void FandangoLexerBase::emitToken(std::unique_ptr<antlr4::Token> token) {
    assert(token != nullptr);

    // std::clog << "FandangoLexerBase::emitToken: token = " << token->toString() << std::endl;
    tokens.push_back(std::move(token));
    // std::clog << "FandangoLexerBase::emitToken: done" << std::endl;
}

std::unique_ptr<antlr4::Token> FandangoLexerBase::nextToken() {
    // std::clog << "FandangoLexerBase::nextToken" << std::endl;

    // std::clog << "FandangoLexerBase::nextToken: tokens =";
    // for (auto&& t : tokens) {
    //     std::cerr << ' ' << t->toString();
    // }
    // std::clog << std::endl;

    // Check if the end-of-file is ahead and there are still some DEDENTS expected.
    if (_input->LA(1) == FandangoParser::EOF && !indents.empty()) {
        // std::clog << "FandangoLexerBase::nextToken: removing EOFs" << std::endl;

        // Remove any trailing EOF tokens from our buffer.
        #if 0
        tokens.erase(std::remove_if(tokens.begin(), tokens.end(),
             [](antlr4::Token *tok) {
            return tok->getType() == FandangoParser::EOF;
        }), tokens.end());
        #endif
        for (auto it = tokens.begin(); it != tokens.end();) {
            if ((*it)->getType() == FandangoParser::EOF) {
                it = tokens.erase(it);
            } else {
                ++it;
            }
        }

        // First emit an extra line break that serves as the end of the statement.
        emitToken(commonToken(FandangoParser::NEWLINE, "\n"));

        // Now emit as much DEDENT tokens as needed.
        while (!indents.empty()) {
            emitToken(commonToken(FandangoParser::DEDENT, "<DEDENT>"));
            indents.pop_back();
        }

        // Put the EOF back on the token stream.
        emitToken(commonToken(FandangoParser::EOF, "<EOF>"));
    }

    if (tokens.empty()) {
        // Get a new token from the lexer.
        // Note that Lexer::nextToken() may call on_newline() and other methods,
        // affecting the current state.
        std::unique_ptr<antlr4::Token> lexer_token = Lexer::nextToken();
        // std::clog << "FandangoLexerBase::nextToken: getting lexer token " << lexer_token->toString() << std::endl;

        if (skipLexer > 0) {
            // After emitting an INDENT or DEDENT, we may have to skip the lexer token
            // std::clog << "FandangoLexerBase::nextToken: skipping this lexer token" << std::endl;
            skipLexer--;
        } else {
            emitToken(std::move(lexer_token));
        }
    }

    // Now fetch the next token from the queue
    std::unique_ptr<antlr4::Token> token = std::move(tokens.front());
    tokens.pop_front();

    // std::clog << "FandangoLexerBase::nextToken: returning " << token->toString() << std::endl;

    return std::move(token);
}

// via https://github.com/antlr/grammars-v4/blob/bdf2e9a5e618f54e7a2ad95610e314a199f10f77/python/python/Cpp/PythonLexerBase.cpp
std::unique_ptr<antlr4::Token> FandangoLexerBase::commonToken(size_t type, const std::string &text) {
    // std::clog << "FandangoLexerBase::commonToken: type = " << type << ", text = '" << text << "'" << std::endl;

    std::unique_ptr<antlr4::Token> token(
		_factory->create({ this, _input },
				         type, text, antlr4::Token::DEFAULT_CHANNEL, getCharIndex() - text.size(), getCharIndex() - 1,
				         getLine(), getCharPositionInLine()));

    // std::clog << "FandangoLexerBase::commonToken: returning " << token->toString() << std::endl;
    assert(token != nullptr);

	return std::move(token);
}

int FandangoLexerBase::getIndentationCount(const std::string &whitespace) {
    int count = 0;
    for (char c : whitespace) {
        if (c == '\t')
            count += 8 - (count % 8);
        else
            count++;
    }
    return count;
}

bool FandangoLexerBase::_at_start_of_input() {
    return getCharIndex() == 0;
}

void FandangoLexerBase::_open_brace() {
    opened++;
}

void FandangoLexerBase::_close_brace() {
    opened--;
}

void FandangoLexerBase::_python_start() {
    inPython++;
}

void FandangoLexerBase::_python_end() {
    inPython = 0;
}

void FandangoLexerBase::_fstring_start() {
    isFstring = true;
}

void FandangoLexerBase::_fstring_end() {
    isFstring = false;
}

bool FandangoLexerBase::_is_not_fstring() {
    return !isFstring;
}

void FandangoLexerBase::_on_newline() {
    // std::clog << "FandangoLexerBase::on_newline" << std::endl;

    int next = _input->LA(1);
    int nextNext = _input->LA(2);

    if (opened > 0 || (nextNext != -1 && (next == '\n' || next == '\r' || next == '#'))) {
        // std::clog << "FandangoLexerBase::on_newline: Skipping " << next << std::endl;
        skip();
    } else {
        std::string newLine = std::regex_replace(getText(), NEW_LINE_PATTERN, "");
        std::string spaces = std::regex_replace(getText(), SPACES_PATTERN, "");
        // std::clog << "FandangoLexerBase::on_newline: newLine = '" << newLine << "', spaces = '" << spaces << "'" << std::endl;

        emitToken(commonToken(FandangoParser::NEWLINE, newLine));
        int indent = getIndentationCount(spaces);
        int previous = indents.empty() ? 0 : indents.back();
        // std::clog << "FandangoLexerBase::on_newline: indent = " << indent << ", previous = " << previous << std::endl;

        if (indent == previous) {
            // std::clog << "FandangoLexerBase::on_newline: Skipping identical indent " << next << std::endl;
            skip();
        } else if (indent > previous) {
            indents.push_back(indent);
            emitToken(commonToken(FandangoParser::INDENT, spaces));
            skipLexer++;
        } else {
            while (!indents.empty() && indents.back() > indent) {
                inPython--;
                emitToken(commonToken(FandangoParser::DEDENT, "<DEDENT>"));
                indents.pop_back();
            }
            skipLexer++;
        }
    }

    // std::clog << "FandangoLexerBase::on_newline: done" << std::endl;
}