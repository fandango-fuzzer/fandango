
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
    MINIMIZING = 50, ANY = 51, ALL = 52, LEN = 53, NAME = 54, STRING_LITERAL = 55, 
    BYTES_LITERAL = 56, DECIMAL_INTEGER = 57, OCT_INTEGER = 58, HEX_INTEGER = 59, 
    BIN_INTEGER = 60, FLOAT_NUMBER = 61, IMAG_NUMBER = 62, GRAMMAR_ASSIGN = 63, 
    QUESTION = 64, BACKSLASH = 65, DOT = 66, DOTDOT = 67, ELLIPSIS = 68, 
    STAR = 69, OPEN_PAREN = 70, CLOSE_PAREN = 71, COMMA = 72, COLON = 73, 
    SEMI_COLON = 74, POWER = 75, ASSIGN = 76, OPEN_BRACK = 77, CLOSE_BRACK = 78, 
    OR_OP = 79, XOR = 80, AND_OP = 81, LEFT_SHIFT = 82, RIGHT_SHIFT = 83, 
    ADD = 84, MINUS = 85, DIV = 86, MOD = 87, IDIV = 88, NOT_OP = 89, OPEN_BRACE = 90, 
    CLOSE_BRACE = 91, LESS_THAN = 92, GREATER_THAN = 93, EQUALS = 94, GT_EQ = 95, 
    LT_EQ = 96, NOT_EQ_1 = 97, NOT_EQ_2 = 98, AT = 99, ARROW = 100, ADD_ASSIGN = 101, 
    SUB_ASSIGN = 102, MULT_ASSIGN = 103, AT_ASSIGN = 104, DIV_ASSIGN = 105, 
    MOD_ASSIGN = 106, AND_ASSIGN = 107, OR_ASSIGN = 108, XOR_ASSIGN = 109, 
    LEFT_SHIFT_ASSIGN = 110, RIGHT_SHIFT_ASSIGN = 111, POWER_ASSIGN = 112, 
    IDIV_ASSIGN = 113, EXPR_ASSIGN = 114, EXCL = 115, NEWLINE = 116, SKIP_ = 117, 
    UNKNOWN_CHAR = 118
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

