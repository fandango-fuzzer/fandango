
// Generated from language/FandangoLexer.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "FandangoLexerBase.h"




class  FandangoLexer : public FandangoLexerBase {
public:
  enum {
    INDENT = 1, DEDENT = 2, FSTRING_START_QUOTE = 3, FSTRING_START_SINGLE_QUOTE = 4, 
    FSTRING_START_TRIPLE_QUOTE = 5, FSTRING_START_TRIPLE_SINGLE_QUOTE = 6, 
    FSTRING_DOUBLE_QUOTE = 7, FSTRING_DOUBLE_SINGLE_QUOTE = 8, STRING = 9, 
    NUMBER = 10, INTEGER = 11, PYTHON_START = 12, PYTHON_END = 13, AND = 14, 
    AS = 15, ASSERT = 16, ASYNC = 17, AWAIT = 18, BREAK = 19, CASE = 20, 
    CLASS = 21, CONTINUE = 22, DEF = 23, DEL = 24, ELIF = 25, ELSE = 26, 
    EXCEPT = 27, FALSE = 28, FINALLY = 29, FOR = 30, FROM = 31, GLOBAL = 32, 
    IF = 33, IMPORT = 34, IN = 35, IS = 36, LAMBDA = 37, MATCH = 38, NONE = 39, 
    NONLOCAL = 40, NOT = 41, OR = 42, PASS = 43, RAISE = 44, RETURN = 45, 
    TRUE = 46, TRY = 47, TYPE = 48, WHILE = 49, WHERE = 50, WITH = 51, YIELD = 52, 
    FORALL = 53, EXISTS = 54, MAXIMIZING = 55, MINIMIZING = 56, ANY = 57, 
    ALL = 58, LEN = 59, NAME = 60, STRING_LITERAL = 61, FSTRING_END_TRIPLE_QUOTE = 62, 
    FSTRING_END_TRIPLE_SINGLE_QUOTE = 63, FSTRING_END_QUOTE = 64, FSTRING_END_SINGLE_QUOTE = 65, 
    BYTES_LITERAL = 66, DECIMAL_INTEGER = 67, OCT_INTEGER = 68, HEX_INTEGER = 69, 
    BIN_INTEGER = 70, FLOAT_NUMBER = 71, IMAG_NUMBER = 72, GRAMMAR_ASSIGN = 73, 
    QUESTION = 74, BACKSLASH = 75, ELLIPSIS = 76, DOTDOT = 77, DOT = 78, 
    STAR = 79, OPEN_PAREN = 80, CLOSE_PAREN = 81, COMMA = 82, COLON = 83, 
    SEMI_COLON = 84, POWER = 85, ASSIGN = 86, OPEN_BRACK = 87, CLOSE_BRACK = 88, 
    OR_OP = 89, XOR = 90, AND_OP = 91, LEFT_SHIFT = 92, RIGHT_SHIFT = 93, 
    ADD = 94, MINUS = 95, DIV = 96, MOD = 97, IDIV = 98, NOT_OP = 99, OPEN_BRACE = 100, 
    CLOSE_BRACE = 101, LESS_THAN = 102, GREATER_THAN = 103, EQUALS = 104, 
    GT_EQ = 105, LT_EQ = 106, NOT_EQ_1 = 107, NOT_EQ_2 = 108, AT = 109, 
    ARROW = 110, ADD_ASSIGN = 111, SUB_ASSIGN = 112, MULT_ASSIGN = 113, 
    AT_ASSIGN = 114, DIV_ASSIGN = 115, MOD_ASSIGN = 116, AND_ASSIGN = 117, 
    OR_ASSIGN = 118, XOR_ASSIGN = 119, LEFT_SHIFT_ASSIGN = 120, RIGHT_SHIFT_ASSIGN = 121, 
    POWER_ASSIGN = 122, IDIV_ASSIGN = 123, EXPR_ASSIGN = 124, EXCL = 125, 
    NEWLINE = 126, SKIP_ = 127, UNKNOWN_CHAR = 128
  };

  explicit FandangoLexer(antlr4::CharStream *input);

  ~FandangoLexer() override;


  std::string getGrammarFileName() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const std::vector<std::string>& getChannelNames() const override;

  const std::vector<std::string>& getModeNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;

  const antlr4::atn::ATN& getATN() const override;

  void action(antlr4::RuleContext *context, size_t ruleIndex, size_t actionIndex) override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.
  void PYTHON_STARTAction(antlr4::RuleContext *context, size_t actionIndex);
  void PYTHON_ENDAction(antlr4::RuleContext *context, size_t actionIndex);
  void CASEAction(antlr4::RuleContext *context, size_t actionIndex);
  void CLASSAction(antlr4::RuleContext *context, size_t actionIndex);
  void DEFAction(antlr4::RuleContext *context, size_t actionIndex);
  void ELIFAction(antlr4::RuleContext *context, size_t actionIndex);
  void ELSEAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXCEPTAction(antlr4::RuleContext *context, size_t actionIndex);
  void FINALLYAction(antlr4::RuleContext *context, size_t actionIndex);
  void FORAction(antlr4::RuleContext *context, size_t actionIndex);
  void IFAction(antlr4::RuleContext *context, size_t actionIndex);
  void MATCHAction(antlr4::RuleContext *context, size_t actionIndex);
  void TRYAction(antlr4::RuleContext *context, size_t actionIndex);
  void WHILEAction(antlr4::RuleContext *context, size_t actionIndex);
  void WITHAction(antlr4::RuleContext *context, size_t actionIndex);
  void OPEN_PARENAction(antlr4::RuleContext *context, size_t actionIndex);
  void CLOSE_PARENAction(antlr4::RuleContext *context, size_t actionIndex);
  void OPEN_BRACKAction(antlr4::RuleContext *context, size_t actionIndex);
  void CLOSE_BRACKAction(antlr4::RuleContext *context, size_t actionIndex);
  void OPEN_BRACEAction(antlr4::RuleContext *context, size_t actionIndex);
  void CLOSE_BRACEAction(antlr4::RuleContext *context, size_t actionIndex);
  void NEWLINEAction(antlr4::RuleContext *context, size_t actionIndex);

  // Individual semantic predicate functions triggered by sempred() above.

};

