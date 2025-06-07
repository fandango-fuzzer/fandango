
// Generated from language/FandangoLexer.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"




class  FandangoLexer : public FandangoLexerBase {
public:
  enum {
    INDENT = 1, DEDENT = 2, STRING = 3, NUMBER = 4, INTEGER = 5, PYTHON_START = 6, 
    PYTHON_END = 7, NONTERMINAL = 8, AND = 9, AS = 10, ASSERT = 11, ASYNC = 12, 
    AWAIT = 13, BREAK = 14, CASE = 15, CLASS = 16, CONTINUE = 17, DEF = 18, 
    DEL = 19, ELIF = 20, ELSE = 21, EXCEPT = 22, FALSE = 23, FINALLY = 24, 
    FOR = 25, FROM = 26, GLOBAL = 27, IF = 28, IMPORT = 29, IN = 30, IS = 31, 
    LAMBDA = 32, MATCH = 33, NONE = 34, NONLOCAL = 35, NOT = 36, OR = 37, 
    PASS = 38, RAISE = 39, RETURN = 40, TRUE = 41, TRY = 42, TYPE = 43, 
    UNDERSCORE = 44, WHILE = 45, WHERE = 46, WITH = 47, YIELD = 48, FORALL = 49, 
    EXISTS = 50, MAXIMIZING = 51, MINIMIZING = 52, NAME = 53, STRING_LITERAL = 54, 
    BYTES_LITERAL = 55, DECIMAL_INTEGER = 56, OCT_INTEGER = 57, HEX_INTEGER = 58, 
    BIN_INTEGER = 59, FLOAT_NUMBER = 60, IMAG_NUMBER = 61, GRAMMAR_ASSIGN = 62, 
    QUESTION = 63, BACKSLASH = 64, DOT = 65, DOTDOT = 66, ELLIPSIS = 67, 
    STAR = 68, OPEN_PAREN = 69, CLOSE_PAREN = 70, COMMA = 71, COLON = 72, 
    SEMI_COLON = 73, POWER = 74, ASSIGN = 75, OPEN_BRACK = 76, CLOSE_BRACK = 77, 
    OR_OP = 78, XOR = 79, AND_OP = 80, LEFT_SHIFT = 81, RIGHT_SHIFT = 82, 
    ADD = 83, MINUS = 84, DIV = 85, MOD = 86, IDIV = 87, NOT_OP = 88, OPEN_BRACE = 89, 
    CLOSE_BRACE = 90, LESS_THAN = 91, GREATER_THAN = 92, EQUALS = 93, GT_EQ = 94, 
    LT_EQ = 95, NOT_EQ_1 = 96, NOT_EQ_2 = 97, AT = 98, ARROW = 99, ADD_ASSIGN = 100, 
    SUB_ASSIGN = 101, MULT_ASSIGN = 102, AT_ASSIGN = 103, DIV_ASSIGN = 104, 
    MOD_ASSIGN = 105, AND_ASSIGN = 106, OR_ASSIGN = 107, XOR_ASSIGN = 108, 
    LEFT_SHIFT_ASSIGN = 109, RIGHT_SHIFT_ASSIGN = 110, POWER_ASSIGN = 111, 
    IDIV_ASSIGN = 112, EXPR_ASSIGN = 113, EXCL = 114, NEWLINE = 115, SKIP_ = 116, 
    UNKNOWN_CHAR = 117
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

