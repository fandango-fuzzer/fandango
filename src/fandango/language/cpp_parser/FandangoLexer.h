
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
    GLOBAL = 30, IF = 31, IMPORT = 32, IN = 33, INCLUDE = 34, IS = 35, LAMBDA = 36, 
    MATCH = 37, NONE = 38, NONLOCAL = 39, NOT = 40, OR = 41, PASS = 42, 
    RAISE = 43, RETURN = 44, TRUE = 45, TRY = 46, TYPE = 47, WHILE = 48, 
    WHERE = 49, WITH = 50, YIELD = 51, FORALL = 52, EXISTS = 53, MAXIMIZING = 54, 
    MINIMIZING = 55, ANY = 56, ALL = 57, LEN = 58, SETTING = 59, ALL_WITH_TYPE = 60, 
    NODE_TYPES = 61, NAME = 62, STRING_LITERAL = 63, FSTRING_END_TRIPLE_QUOTE = 64, 
    FSTRING_END_TRIPLE_SINGLE_QUOTE = 65, FSTRING_END_QUOTE = 66, FSTRING_END_SINGLE_QUOTE = 67, 
    BYTES_LITERAL = 68, DECIMAL_INTEGER = 69, OCT_INTEGER = 70, HEX_INTEGER = 71, 
    BIN_INTEGER = 72, FLOAT_NUMBER = 73, IMAG_NUMBER = 74, GRAMMAR_ASSIGN = 75, 
    QUESTION = 76, BACKSLASH = 77, ELLIPSIS = 78, DOTDOT = 79, DOT = 80, 
    STAR = 81, OPEN_PAREN = 82, CLOSE_PAREN = 83, COMMA = 84, COLON = 85, 
    SEMI_COLON = 86, POWER = 87, ASSIGN = 88, OPEN_BRACK = 89, CLOSE_BRACK = 90, 
    OR_OP = 91, XOR = 92, AND_OP = 93, LEFT_SHIFT = 94, RIGHT_SHIFT = 95, 
    ADD = 96, MINUS = 97, DIV = 98, MOD = 99, IDIV = 100, NOT_OP = 101, 
    OPEN_BRACE = 102, CLOSE_BRACE = 103, LESS_THAN = 104, GREATER_THAN = 105, 
    EQUALS = 106, GT_EQ = 107, LT_EQ = 108, NOT_EQ_1 = 109, NOT_EQ_2 = 110, 
    AT = 111, ARROW = 112, ADD_ASSIGN = 113, SUB_ASSIGN = 114, MULT_ASSIGN = 115, 
    AT_ASSIGN = 116, DIV_ASSIGN = 117, MOD_ASSIGN = 118, AND_ASSIGN = 119, 
    OR_ASSIGN = 120, XOR_ASSIGN = 121, LEFT_SHIFT_ASSIGN = 122, RIGHT_SHIFT_ASSIGN = 123, 
    POWER_ASSIGN = 124, IDIV_ASSIGN = 125, EXPR_ASSIGN = 126, EXCL = 127, 
    NEWLINE = 128, SKIP_ = 129, SPACES = 130, UNDERSCORE = 131, UNKNOWN_CHAR = 132
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

