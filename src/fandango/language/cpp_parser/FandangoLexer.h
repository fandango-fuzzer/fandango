
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
    ANY = 55, ALL = 56, LEN = 57, SETTING = 58, NAME = 59, STRING_LITERAL = 60, 
    FSTRING_END_TRIPLE_QUOTE = 61, FSTRING_END_TRIPLE_SINGLE_QUOTE = 62, 
    FSTRING_END_QUOTE = 63, FSTRING_END_SINGLE_QUOTE = 64, BYTES_LITERAL = 65, 
    DECIMAL_INTEGER = 66, OCT_INTEGER = 67, HEX_INTEGER = 68, BIN_INTEGER = 69, 
    FLOAT_NUMBER = 70, IMAG_NUMBER = 71, GRAMMAR_ASSIGN = 72, QUESTION = 73, 
    BACKSLASH = 74, ELLIPSIS = 75, DOTDOT = 76, DOT = 77, STAR = 78, OPEN_PAREN = 79, 
    CLOSE_PAREN = 80, COMMA = 81, COLON = 82, SEMI_COLON = 83, POWER = 84, 
    ASSIGN = 85, OPEN_BRACK = 86, CLOSE_BRACK = 87, OR_OP = 88, XOR = 89, 
    AND_OP = 90, LEFT_SHIFT = 91, RIGHT_SHIFT = 92, ADD = 93, MINUS = 94, 
    DIV = 95, MOD = 96, IDIV = 97, NOT_OP = 98, OPEN_BRACE = 99, CLOSE_BRACE = 100, 
    LESS_THAN = 101, GREATER_THAN = 102, EQUALS = 103, GT_EQ = 104, LT_EQ = 105, 
    NOT_EQ_1 = 106, NOT_EQ_2 = 107, AT = 108, ARROW = 109, ADD_ASSIGN = 110, 
    SUB_ASSIGN = 111, MULT_ASSIGN = 112, AT_ASSIGN = 113, DIV_ASSIGN = 114, 
    MOD_ASSIGN = 115, AND_ASSIGN = 116, OR_ASSIGN = 117, XOR_ASSIGN = 118, 
    LEFT_SHIFT_ASSIGN = 119, RIGHT_SHIFT_ASSIGN = 120, POWER_ASSIGN = 121, 
    IDIV_ASSIGN = 122, EXPR_ASSIGN = 123, EXCL = 124, NEWLINE = 125, SKIP_ = 126, 
    SPACES = 127, UNDERSCORE = 128, UNKNOWN_CHAR = 129
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

