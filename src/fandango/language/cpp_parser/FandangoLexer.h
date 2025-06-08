
// Generated from language/FandangoLexer.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "FandangoLexerBase.h"




class  FandangoLexer : public FandangoLexerBase {
public:
  enum {
    INDENT = 1, DEDENT = 2, STRING = 3, NUMBER = 4, INTEGER = 5, PYTHON_START = 6, 
    PYTHON_END = 7, AND = 8, AS = 9, ASSERT = 10, ASYNC = 11, AWAIT = 12, 
    BREAK = 13, CASE = 14, CLASS = 15, CONTINUE = 16, DEF = 17, DEL = 18, 
    ELIF = 19, ELSE = 20, EXCEPT = 21, FALSE = 22, FINALLY = 23, FOR = 24, 
    FROM = 25, GLOBAL = 26, IF = 27, IMPORT = 28, IN = 29, IS = 30, LAMBDA = 31, 
    MATCH = 32, NONE = 33, NONLOCAL = 34, NOT = 35, OR = 36, PASS = 37, 
    RAISE = 38, RETURN = 39, TRUE = 40, TRY = 41, TYPE = 42, UNDERSCORE = 43, 
    WHILE = 44, WHERE = 45, WITH = 46, YIELD = 47, FORALL = 48, EXISTS = 49, 
    MAXIMIZING = 50, MINIMIZING = 51, NAME = 52, STRING_LITERAL = 53, BYTES_LITERAL = 54, 
    DECIMAL_INTEGER = 55, OCT_INTEGER = 56, HEX_INTEGER = 57, BIN_INTEGER = 58, 
    FLOAT_NUMBER = 59, IMAG_NUMBER = 60, GRAMMAR_ASSIGN = 61, QUESTION = 62, 
    BACKSLASH = 63, DOT = 64, DOTDOT = 65, ELLIPSIS = 66, STAR = 67, OPEN_PAREN = 68, 
    CLOSE_PAREN = 69, COMMA = 70, COLON = 71, SEMI_COLON = 72, POWER = 73, 
    ASSIGN = 74, OPEN_BRACK = 75, CLOSE_BRACK = 76, OR_OP = 77, XOR = 78, 
    AND_OP = 79, LEFT_SHIFT = 80, RIGHT_SHIFT = 81, ADD = 82, MINUS = 83, 
    DIV = 84, MOD = 85, IDIV = 86, NOT_OP = 87, OPEN_BRACE = 88, CLOSE_BRACE = 89, 
    LESS_THAN = 90, GREATER_THAN = 91, EQUALS = 92, GT_EQ = 93, LT_EQ = 94, 
    NOT_EQ_1 = 95, NOT_EQ_2 = 96, AT = 97, ARROW = 98, ADD_ASSIGN = 99, 
    SUB_ASSIGN = 100, MULT_ASSIGN = 101, AT_ASSIGN = 102, DIV_ASSIGN = 103, 
    MOD_ASSIGN = 104, AND_ASSIGN = 105, OR_ASSIGN = 106, XOR_ASSIGN = 107, 
    LEFT_SHIFT_ASSIGN = 108, RIGHT_SHIFT_ASSIGN = 109, POWER_ASSIGN = 110, 
    IDIV_ASSIGN = 111, EXPR_ASSIGN = 112, EXCL = 113, NEWLINE = 114, SKIP_ = 115, 
    UNKNOWN_CHAR = 116
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

