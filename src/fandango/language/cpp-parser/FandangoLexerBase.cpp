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

    lexer = this;
}

void FandangoLexerBase::reset() {
    tokens.clear();
    indents.clear();
    opened = 0;
    inPython = 0;

    Lexer::reset();
}

void FandangoLexerBase::emitToken(std::unique_ptr<antlr4::Token> token) {
    assert(token != nullptr);

    // std::cerr << "FandangoLexerBase::emitToken: token = " << token << std::endl;
    tokens.push_back(std::move(token));
    // std::cerr << "FandangoLexerBase::emitToken: done" << std::endl;
}

std::unique_ptr<antlr4::Token> FandangoLexerBase::nextToken() {
    // std::cerr << "FandangoLexerBase::nextToken..." << std::endl;

    // Check if the end-of-file is ahead and there are still some DEDENTS expected.
    if (_input->LA(1) == FandangoParser::EOF && !indents.empty()) {
        // std::cerr << "FandangoLexerBase::nextToken: removing EOFs" << std::endl;

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
            emitToken(createDedent());
            indents.pop_back();
        }

        // Put the EOF back on the token stream.
        emitToken(commonToken(FandangoParser::EOF, "<EOF>"));
    }

    std::unique_ptr<antlr4::Token> token = Lexer::nextToken();
    if (!tokens.empty()) {
        // std::cerr << "FandangoLexerBase::nextToken: taking token from tokens" << std::endl;
        token = std::move(tokens.front());
        tokens.pop_front();
    }

    // std::cerr << "FandangoLexerBase::nextToken: returning " << token << std::endl;

    assert(token != nullptr);

    return token;
}

std::unique_ptr<antlr4::Token> FandangoLexerBase::createDedent() {
    return commonToken(FandangoParser::DEDENT, "");
}

#if 0
// Close to original Python code, but the superclass has no _tokenFactorySourcePair member. -- AZ
std::unique_ptr<antlr4::Token> FandangoLexerBase::commonToken(size_t type, const std::string &text) {
    size_t stop = getCharIndex() - 1;
    size_t start = text.empty() ? stop : stop - text.length() + 1;

    return new antlr4::CommonToken(_tokenFactorySourcePair, type,
                                   antlr4::Token::DEFAULT_CHANNEL, start, stop);
}
#endif

#if 0
// This is a workaround replacing the commented-out code above. -- AZ
std::unique_ptr<antlr4::Token> FandangoLexerBase::commonToken(size_t type, const std::string &text) {
    return (std::unique_ptr<antlr4::Token>)new antlr4::CommonToken(type, text);
}
#endif

#if 1
// via https://github.com/antlr/grammars-v4/blob/bdf2e9a5e618f54e7a2ad95610e314a199f10f77/python/python/Cpp/PythonLexerBase.cpp
std::unique_ptr<antlr4::Token> FandangoLexerBase::commonToken(size_t type, const std::string &text) {
    // std::cerr << "FandangoLexerBase::commonToken: type = " << type << ", text = '" << text << "'..." << std::endl;

    std::unique_ptr<antlr4::Token> token(
		_factory->create({ this, _input },
				         type, text, antlr4::Token::DEFAULT_CHANNEL, getCharIndex() - text.size(), getCharIndex() - 1,
				         getLine(), getCharPositionInLine()));

    // std::cerr << "FandangoLexerBase::commonToken: returning " << token << std::endl;
    assert(token != nullptr);

	return std::move(token);
}
#endif

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

void FandangoLexerBase::_on_newline() {
    // std::cerr << "FandangoLexerBase::on_newline..." << std::endl;

    if (inPython > 0) {
        // std::cerr << "FandangoLexerBase::on_newline: handling Python" << std::endl;

        std::string newLine = std::regex_replace(getText(), NEW_LINE_PATTERN, "");
        std::string spaces = std::regex_replace(getText(), SPACES_PATTERN, "");

        int next = _input->LA(1);
        int nextNext = _input->LA(2);

        if (opened > 0 || (nextNext != -1 && (next == '\n' || next == '\r' || next == '#'))) {
            skip();
        } else {
            emitToken(commonToken(FandangoParser::NEWLINE, newLine));
            int indent = getIndentationCount(spaces);
            int previous = indents.empty() ? 0 : indents.back();

            if (indent == previous) {
                skip();
            } else if (indent > previous) {
                indents.push_back(indent);
                emitToken(commonToken(FandangoParser::INDENT, spaces));
            } else {
                while (!indents.empty() && indents.back() > indent) {
                    inPython--;
                    emitToken(createDedent());
                    indents.pop_back();
                }
            }
        }
    }

    // std::cerr << "FandangoLexerBase::on_newline: done" << std::endl;
}