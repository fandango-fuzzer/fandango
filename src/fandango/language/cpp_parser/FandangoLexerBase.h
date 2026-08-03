
#pragma once

#include "antlr4-runtime.h"
#include "FandangoParser.h"
#include <regex>
#include <vector>
#include <deque>

class FandangoLexerBase: public antlr4::Lexer {
public:
    explicit FandangoLexerBase(antlr4::CharStream *input);

    void reset() override;
    std::unique_ptr<antlr4::Token> nextToken() override;
    void emitToken(std::unique_ptr<antlr4::Token> token);

    bool _at_start_of_input();
    void _open_brace();
    void _close_brace();
    void _python_start();
    void _python_end();
    void _on_newline();
    void _fstring_start();
    void _fstring_end();
    bool _is_not_fstring();
    void _permutation_start();
    void _permutation_end();
    bool _can_start_permutation();
    bool _is_in_permutation();
    static FandangoLexerBase *lexer;

private:
    std::deque<std::unique_ptr<antlr4::Token>> tokens;
    std::vector<int> indents;
    int opened = 0;
    int inPython = 0;
    bool isFstring = false;
    bool inPermutation = false;
    int skipLexer = 0;

    static const std::regex NEW_LINE_PATTERN;
    static const std::regex SPACES_PATTERN;

    std::unique_ptr<antlr4::Token> commonToken(const size_t type, const std::string &text);
    static int getIndentationCount(const std::string &whitespace);
};

#define at_start_of_input() FandangoLexerBase::lexer->_at_start_of_input();
#define open_brace() FandangoLexerBase::lexer->_open_brace();
#define close_brace() FandangoLexerBase::lexer->_close_brace();
#define python_start() FandangoLexerBase::lexer->_python_start();
#define python_end() FandangoLexerBase::lexer->_python_end();
#define on_newline() FandangoLexerBase::lexer->_on_newline();
#define fstring_start() FandangoLexerBase::lexer->_fstring_start();
#define fstring_end() FandangoLexerBase::lexer->_fstring_end();
#define is_not_fstring() FandangoLexerBase::lexer->_is_not_fstring();
#define permutation_start() FandangoLexerBase::lexer->_permutation_start();
#define permutation_end() FandangoLexerBase::lexer->_permutation_end();
#define can_start_permutation() FandangoLexerBase::lexer->_can_start_permutation()
#define is_in_permutation() FandangoLexerBase::lexer->_is_in_permutation()
