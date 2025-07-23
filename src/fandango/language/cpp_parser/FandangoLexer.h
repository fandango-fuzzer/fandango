
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
    ANY = 55, ALL = 56, LEN = 57, SETTING = 58, ALL_WITH_TYPE = 59, NODE_TYPES = 60, 
    NAME = 61, STRING_LITERAL = 62, FSTRING_END_TRIPLE_QUOTE = 63, FSTRING_END_TRIPLE_SINGLE_QUOTE = 64, 
    FSTRING_END_QUOTE = 65, FSTRING_END_SINGLE_QUOTE = 66, BYTES_LITERAL = 67, 
    DECIMAL_INTEGER = 68, OCT_INTEGER = 69, HEX_INTEGER = 70, BIN_INTEGER = 71, 
    FLOAT_NUMBER = 72, IMAG_NUMBER = 73, GRAMMAR_ASSIGN = 74, QUESTION = 75, 
    BACKSLASH = 76, ELLIPSIS = 77, DOTDOT = 78, DOT = 79, STAR = 80, OPEN_PAREN = 81, 
    CLOSE_PAREN = 82, COMMA = 83, COLON = 84, SEMI_COLON = 85, POWER = 86, 
    ASSIGN = 87, OPEN_BRACK = 88, CLOSE_BRACK = 89, OR_OP = 90, XOR = 91, 
    AND_OP = 92, LEFT_SHIFT = 93, RIGHT_SHIFT = 94, ADD = 95, MINUS = 96, 
    DIV = 97, MOD = 98, IDIV = 99, NOT_OP = 100, OPEN_BRACE = 101, CLOSE_BRACE = 102, 
    LESS_THAN = 103, GREATER_THAN = 104, EQUALS = 105, GT_EQ = 106, LT_EQ = 107, 
    NOT_EQ_1 = 108, NOT_EQ_2 = 109, AT = 110, ARROW = 111, ADD_ASSIGN = 112, 
    SUB_ASSIGN = 113, MULT_ASSIGN = 114, AT_ASSIGN = 115, DIV_ASSIGN = 116, 
    MOD_ASSIGN = 117, AND_ASSIGN = 118, OR_ASSIGN = 119, XOR_ASSIGN = 120, 
    LEFT_SHIFT_ASSIGN = 121, RIGHT_SHIFT_ASSIGN = 122, POWER_ASSIGN = 123, 
    IDIV_ASSIGN = 124, EXPR_ASSIGN = 125, EXCL = 126, NEWLINE = 127, SKIP_ = 128, 
    SPACES = 129, UNDERSCORE = 130, UNKNOWN_CHAR = 131
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

