
// Generated from language/FandangoLexer.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "FandangoLexerBase.h"




class  FandangoLexer : public FandangoLexerBase {
public:
  enum {
    INDENT = 1, DEDENT = 2, FSTRING_START_QUOTE = 3, FSTRING_START_SINGLE_QUOTE = 4, 
    FSTRING_START_TRIPLE_QUOTE = 5, FSTRING_START_TRIPLE_SINGLE_QUOTE = 6, 
    STRING = 7, NUMBER = 8, INTEGER = 9, PYTHON_START = 10, PYTHON_END = 11, 
    AND = 12, AS = 13, ASSERT = 14, ASYNC = 15, AWAIT = 16, BREAK = 17, 
    CASE = 18, CLASS = 19, CONTINUE = 20, DEF = 21, DEL = 22, ELIF = 23, 
    ELSE = 24, EXCEPT = 25, FALSE = 26, FINALLY = 27, FOR = 28, FROM = 29, 
    GLOBAL = 30, IF = 31, IMPORT = 32, IN = 33, IS = 34, LAMBDA = 35, MATCH = 36, 
    NONE = 37, NONLOCAL = 38, NOT = 39, OR = 40, PASS = 41, RAISE = 42, 
    RETURN = 43, TRUE = 44, TRY = 45, TYPE = 46, WHILE = 47, WHERE = 48, 
    WITH = 49, YIELD = 50, FORALL = 51, EXISTS = 52, MAXIMIZING = 53, MINIMIZING = 54, 
    ANY = 55, ALL = 56, LEN = 57, NAME = 58, STRING_LITERAL = 59, FSTRING_END_TRIPLE_QUOTE = 60, 
    FSTRING_END_TRIPLE_SINGLE_QUOTE = 61, FSTRING_END_QUOTE = 62, FSTRING_END_SINGLE_QUOTE = 63, 
    BYTES_LITERAL = 64, DECIMAL_INTEGER = 65, OCT_INTEGER = 66, HEX_INTEGER = 67, 
    BIN_INTEGER = 68, FLOAT_NUMBER = 69, IMAG_NUMBER = 70, GRAMMAR_ASSIGN = 71, 
    QUESTION = 72, BACKSLASH = 73, ELLIPSIS = 74, DOTDOT = 75, DOT = 76, 
    STAR = 77, OPEN_PAREN = 78, CLOSE_PAREN = 79, COMMA = 80, COLON = 81, 
    SEMI_COLON = 82, POWER = 83, ASSIGN = 84, OPEN_BRACK = 85, CLOSE_BRACK = 86, 
    OR_OP = 87, XOR = 88, AND_OP = 89, LEFT_SHIFT = 90, RIGHT_SHIFT = 91, 
    ADD = 92, MINUS = 93, DIV = 94, MOD = 95, IDIV = 96, NOT_OP = 97, OPEN_BRACE = 98, 
    CLOSE_BRACE = 99, LESS_THAN = 100, GREATER_THAN = 101, EQUALS = 102, 
    GT_EQ = 103, LT_EQ = 104, NOT_EQ_1 = 105, NOT_EQ_2 = 106, AT = 107, 
    ARROW = 108, ADD_ASSIGN = 109, SUB_ASSIGN = 110, MULT_ASSIGN = 111, 
    AT_ASSIGN = 112, DIV_ASSIGN = 113, MOD_ASSIGN = 114, AND_ASSIGN = 115, 
    OR_ASSIGN = 116, XOR_ASSIGN = 117, LEFT_SHIFT_ASSIGN = 118, RIGHT_SHIFT_ASSIGN = 119, 
    POWER_ASSIGN = 120, IDIV_ASSIGN = 121, EXPR_ASSIGN = 122, EXCL = 123, 
    NEWLINE = 124, SKIP_ = 125, UNKNOWN_CHAR = 126
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

  bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.
  void FSTRING_START_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
  void FSTRING_START_SINGLE_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
  void FSTRING_START_TRIPLE_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
  void FSTRING_START_TRIPLE_SINGLE_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
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
  void FSTRING_END_TRIPLE_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
  void FSTRING_END_TRIPLE_SINGLE_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
  void FSTRING_END_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
  void FSTRING_END_SINGLE_QUOTEAction(antlr4::RuleContext *context, size_t actionIndex);
  void OPEN_PARENAction(antlr4::RuleContext *context, size_t actionIndex);
  void CLOSE_PARENAction(antlr4::RuleContext *context, size_t actionIndex);
  void OPEN_BRACKAction(antlr4::RuleContext *context, size_t actionIndex);
  void CLOSE_BRACKAction(antlr4::RuleContext *context, size_t actionIndex);
  void OPEN_BRACEAction(antlr4::RuleContext *context, size_t actionIndex);
  void CLOSE_BRACEAction(antlr4::RuleContext *context, size_t actionIndex);
  void NEWLINEAction(antlr4::RuleContext *context, size_t actionIndex);

  // Individual semantic predicate functions triggered by sempred() above.
  bool STRING_LITERALSempred(antlr4::RuleContext *_localctx, size_t predicateIndex);

};

