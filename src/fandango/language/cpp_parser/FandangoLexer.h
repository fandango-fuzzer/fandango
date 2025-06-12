
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
    RAISE = 38, RETURN = 39, TRUE = 40, TRY = 41, TYPE = 42, WHILE = 43, 
    WHERE = 44, WITH = 45, YIELD = 46, FORALL = 47, EXISTS = 48, MAXIMIZING = 49, 
    MINIMIZING = 50, NAME = 51, STRING_LITERAL = 52, BYTES_LITERAL = 53, 
    DECIMAL_INTEGER = 54, OCT_INTEGER = 55, HEX_INTEGER = 56, BIN_INTEGER = 57, 
    FLOAT_NUMBER = 58, IMAG_NUMBER = 59, GRAMMAR_ASSIGN = 60, QUESTION = 61, 
    BACKSLASH = 62, DOT = 63, DOTDOT = 64, ELLIPSIS = 65, STAR = 66, OPEN_PAREN = 67, 
    CLOSE_PAREN = 68, COMMA = 69, COLON = 70, SEMI_COLON = 71, POWER = 72, 
    ASSIGN = 73, OPEN_BRACK = 74, CLOSE_BRACK = 75, OR_OP = 76, XOR = 77, 
    AND_OP = 78, LEFT_SHIFT = 79, RIGHT_SHIFT = 80, ADD = 81, MINUS = 82, 
    DIV = 83, MOD = 84, IDIV = 85, NOT_OP = 86, OPEN_BRACE = 87, CLOSE_BRACE = 88, 
    LESS_THAN = 89, GREATER_THAN = 90, EQUALS = 91, GT_EQ = 92, LT_EQ = 93, 
    NOT_EQ_1 = 94, NOT_EQ_2 = 95, AT = 96, ARROW = 97, ADD_ASSIGN = 98, 
    SUB_ASSIGN = 99, MULT_ASSIGN = 100, AT_ASSIGN = 101, DIV_ASSIGN = 102, 
    MOD_ASSIGN = 103, AND_ASSIGN = 104, OR_ASSIGN = 105, XOR_ASSIGN = 106, 
    LEFT_SHIFT_ASSIGN = 107, RIGHT_SHIFT_ASSIGN = 108, POWER_ASSIGN = 109, 
    IDIV_ASSIGN = 110, EXPR_ASSIGN = 111, EXCL = 112, NEWLINE = 113, SKIP_ = 114, 
    UNKNOWN_CHAR = 115
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

