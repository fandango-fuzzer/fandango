
// Generated from language/FandangoParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"




class  FandangoParser : public antlr4::Parser {
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
    NEWLINE = 124, SKIP_ = 125, UNKNOWN_CHAR = 126, UNDERSCORE = 127
  };

  enum {
    RuleFandango = 0, RuleProgram = 1, RuleStatement = 2, RuleProduction = 3, 
    RuleAlternative = 4, RuleConcatenation = 5, RuleOperator = 6, RuleKleene = 7, 
    RulePlus = 8, RuleOption = 9, RuleRepeat = 10, RuleSymbol = 11, RuleNonterminal_right = 12, 
    RuleNonterminal = 13, RuleGenerator_call = 14, RuleChar_set = 15, RuleConstraint = 16, 
    RuleImplies = 17, RuleQuantifier = 18, RuleQuantifier_in_line = 19, 
    RuleFormula_disjunction = 20, RuleFormula_conjunction = 21, RuleFormula_atom = 22, 
    RuleFormula_comparison = 23, RuleExpr = 24, RuleSelector_length = 25, 
    RuleStar_selection_or_dot_selection = 26, RuleStar_selection = 27, RuleDot_selection = 28, 
    RuleSelection = 29, RuleBase_selection = 30, RuleRs_pairs = 31, RuleRs_pair = 32, 
    RuleRs_slices = 33, RuleRs_slice = 34, RulePython = 35, RulePython_tag = 36, 
    RulePython_file = 37, RuleInteractive = 38, RuleEval = 39, RuleFunc_type = 40, 
    RuleStatements = 41, RuleStmt = 42, RuleStatement_newline = 43, RuleSimple_stmts = 44, 
    RuleSimple_stmt = 45, RuleCompound_stmt = 46, RuleAssignment = 47, RuleAnnotated_rhs = 48, 
    RuleAugassign = 49, RuleReturn_stmt = 50, RuleRaise_stmt = 51, RuleGlobal_stmt = 52, 
    RuleNonlocal_stmt = 53, RuleDel_stmt = 54, RuleYield_stmt = 55, RuleAssert_stmt = 56, 
    RuleImport_stmt = 57, RuleImport_name = 58, RuleImport_from = 59, RuleImport_from_targets = 60, 
    RuleImport_from_as_names = 61, RuleImport_from_as_name = 62, RuleDotted_as_names = 63, 
    RuleDotted_as_name = 64, RuleDotted_name = 65, RuleBlock = 66, RuleDecorators = 67, 
    RuleClass_def = 68, RuleClass_def_raw = 69, RuleFunction_def = 70, RuleFunction_def_raw = 71, 
    RuleParams = 72, RuleParameters = 73, RuleSlash_no_default = 74, RuleSlash_with_default = 75, 
    RuleStar_etc = 76, RuleKwds = 77, RuleParam_no_default = 78, RuleParam_no_default_star_annotation = 79, 
    RuleParam_with_default = 80, RuleParam_maybe_default = 81, RuleParam = 82, 
    RuleParam_star_annotation = 83, RuleAnnotation = 84, RuleStar_annotation = 85, 
    RuleDefault = 86, RuleIf_stmt = 87, RuleElif_stmt = 88, RuleElse_block = 89, 
    RuleWhile_stmt = 90, RuleFor_stmt = 91, RuleWith_stmt = 92, RuleWith_item = 93, 
    RuleTry_stmt = 94, RuleExcept_block = 95, RuleExcept_star_block = 96, 
    RuleFinally_block = 97, RuleMatch_stmt = 98, RuleSubject_expr = 99, 
    RuleCase_block = 100, RuleGuard = 101, RulePatterns = 102, RulePattern = 103, 
    RuleAs_pattern = 104, RuleOr_pattern = 105, RuleClosed_pattern = 106, 
    RuleLiteral_pattern = 107, RuleLiteral_expr = 108, RuleComplex_number = 109, 
    RuleSigned_number = 110, RuleSigned_real_number = 111, RuleReal_number = 112, 
    RuleImaginary_number = 113, RuleCapture_pattern = 114, RulePattern_capture_target = 115, 
    RuleWildcard_pattern = 116, RuleValue_pattern = 117, RuleAttr = 118, 
    RuleName_or_attr = 119, RuleGroup_pattern = 120, RuleSequence_pattern = 121, 
    RuleOpen_sequence_pattern = 122, RuleMaybe_sequence_pattern = 123, RuleMaybe_star_pattern = 124, 
    RuleStar_pattern = 125, RuleMapping_pattern = 126, RuleItems_pattern = 127, 
    RuleKey_value_pattern = 128, RuleDouble_star_pattern = 129, RuleClass_pattern = 130, 
    RulePositional_patterns = 131, RuleKeyword_patterns = 132, RuleKeyword_pattern = 133, 
    RuleType_alias = 134, RuleType_params = 135, RuleType_param_seq = 136, 
    RuleType_param = 137, RuleType_param_bound = 138, RuleExpressions = 139, 
    RuleExpression = 140, RuleYield_expr = 141, RuleStar_expressions = 142, 
    RuleStar_expression = 143, RuleStar_named_expressions = 144, RuleStar_named_expression = 145, 
    RuleAssignment_expression = 146, RuleNamed_expression = 147, RuleDisjunction = 148, 
    RuleConjunction = 149, RuleInversion = 150, RuleComparison = 151, RuleCompare_op_bitwise_or_pair = 152, 
    RuleEq_bitwise_or = 153, RuleNoteq_bitwise_or = 154, RuleLte_bitwise_or = 155, 
    RuleLt_bitwise_or = 156, RuleGte_bitwise_or = 157, RuleGt_bitwise_or = 158, 
    RuleNotin_bitwise_or = 159, RuleIn_bitwise_or = 160, RuleIsnot_bitwise_or = 161, 
    RuleIs_bitwise_or = 162, RuleBitwise_or = 163, RuleBitwise_xor = 164, 
    RuleBitwise_and = 165, RuleShift_expr = 166, RuleSum = 167, RuleTerm = 168, 
    RuleFactor = 169, RulePower = 170, RuleAwait_primary = 171, RulePrimary = 172, 
    RuleSlices = 173, RuleSlice = 174, RuleAtom = 175, RuleGroup = 176, 
    RuleLambdef = 177, RuleLambda_params = 178, RuleLambda_parameters = 179, 
    RuleLambda_slash_no_default = 180, RuleLambda_slash_with_default = 181, 
    RuleLambda_star_etc = 182, RuleLambda_kwds = 183, RuleLambda_param_no_default = 184, 
    RuleLambda_param_with_default = 185, RuleLambda_param_maybe_default = 186, 
    RuleLambda_param = 187, RuleFstring_middle_no_quote = 188, RuleFstring_middle_no_single_quote = 189, 
    RuleFstring_middle_breaks_no_triple_quote = 190, RuleFstring_middle_breaks_no_triple_single_quote = 191, 
    RuleFstring_any_no_quote = 192, RuleFstring_any_no_single_quote = 193, 
    RuleFstring_middle = 194, RuleFstring_any_breaks_no_triple_quote = 195, 
    RuleFstring_any_breaks_no_triple_single_quote = 196, RuleFstring_any = 197, 
    RuleFstring_replacement_field = 198, RuleFstring_conversion = 199, RuleFstring_full_format_spec = 200, 
    RuleFstring_format_spec = 201, RuleFstring = 202, RuleString = 203, 
    RuleStrings = 204, RuleList = 205, RuleTuple = 206, RuleSet = 207, RuleDict = 208, 
    RuleDouble_starred_kvpairs = 209, RuleDouble_starred_kvpair = 210, RuleKvpair = 211, 
    RuleFor_if_clauses = 212, RuleFor_if_clause = 213, RuleListcomp = 214, 
    RuleSetcomp = 215, RuleGenexp = 216, RuleDictcomp = 217, RuleArguments = 218, 
    RuleArgs = 219, RuleArg = 220, RuleKwargs = 221, RuleStarred_expression = 222, 
    RuleKwarg_or_starred = 223, RuleKwarg_or_double_starred = 224, RuleStar_targets = 225, 
    RuleStar_targets_list_seq = 226, RuleStar_targets_tuple_seq = 227, RuleStar_target = 228, 
    RuleTarget_with_star_atom = 229, RuleStar_atom = 230, RuleSingle_target = 231, 
    RuleSingle_subscript_attribute_target = 232, RuleT_primary = 233, RuleDel_targets = 234, 
    RuleDel_target = 235, RuleDel_t_atom = 236, RuleType_expressions = 237, 
    RuleFunc_type_comment = 238, RuleIdentifier = 239
  };

  explicit FandangoParser(antlr4::TokenStream *input);

  FandangoParser(antlr4::TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options);

  ~FandangoParser() override;

  std::string getGrammarFileName() const override;

  const antlr4::atn::ATN& getATN() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;


  class FandangoContext;
  class ProgramContext;
  class StatementContext;
  class ProductionContext;
  class AlternativeContext;
  class ConcatenationContext;
  class OperatorContext;
  class KleeneContext;
  class PlusContext;
  class OptionContext;
  class RepeatContext;
  class SymbolContext;
  class Nonterminal_rightContext;
  class NonterminalContext;
  class Generator_callContext;
  class Char_setContext;
  class ConstraintContext;
  class ImpliesContext;
  class QuantifierContext;
  class Quantifier_in_lineContext;
  class Formula_disjunctionContext;
  class Formula_conjunctionContext;
  class Formula_atomContext;
  class Formula_comparisonContext;
  class ExprContext;
  class Selector_lengthContext;
  class Star_selection_or_dot_selectionContext;
  class Star_selectionContext;
  class Dot_selectionContext;
  class SelectionContext;
  class Base_selectionContext;
  class Rs_pairsContext;
  class Rs_pairContext;
  class Rs_slicesContext;
  class Rs_sliceContext;
  class PythonContext;
  class Python_tagContext;
  class Python_fileContext;
  class InteractiveContext;
  class EvalContext;
  class Func_typeContext;
  class StatementsContext;
  class StmtContext;
  class Statement_newlineContext;
  class Simple_stmtsContext;
  class Simple_stmtContext;
  class Compound_stmtContext;
  class AssignmentContext;
  class Annotated_rhsContext;
  class AugassignContext;
  class Return_stmtContext;
  class Raise_stmtContext;
  class Global_stmtContext;
  class Nonlocal_stmtContext;
  class Del_stmtContext;
  class Yield_stmtContext;
  class Assert_stmtContext;
  class Import_stmtContext;
  class Import_nameContext;
  class Import_fromContext;
  class Import_from_targetsContext;
  class Import_from_as_namesContext;
  class Import_from_as_nameContext;
  class Dotted_as_namesContext;
  class Dotted_as_nameContext;
  class Dotted_nameContext;
  class BlockContext;
  class DecoratorsContext;
  class Class_defContext;
  class Class_def_rawContext;
  class Function_defContext;
  class Function_def_rawContext;
  class ParamsContext;
  class ParametersContext;
  class Slash_no_defaultContext;
  class Slash_with_defaultContext;
  class Star_etcContext;
  class KwdsContext;
  class Param_no_defaultContext;
  class Param_no_default_star_annotationContext;
  class Param_with_defaultContext;
  class Param_maybe_defaultContext;
  class ParamContext;
  class Param_star_annotationContext;
  class AnnotationContext;
  class Star_annotationContext;
  class DefaultContext;
  class If_stmtContext;
  class Elif_stmtContext;
  class Else_blockContext;
  class While_stmtContext;
  class For_stmtContext;
  class With_stmtContext;
  class With_itemContext;
  class Try_stmtContext;
  class Except_blockContext;
  class Except_star_blockContext;
  class Finally_blockContext;
  class Match_stmtContext;
  class Subject_exprContext;
  class Case_blockContext;
  class GuardContext;
  class PatternsContext;
  class PatternContext;
  class As_patternContext;
  class Or_patternContext;
  class Closed_patternContext;
  class Literal_patternContext;
  class Literal_exprContext;
  class Complex_numberContext;
  class Signed_numberContext;
  class Signed_real_numberContext;
  class Real_numberContext;
  class Imaginary_numberContext;
  class Capture_patternContext;
  class Pattern_capture_targetContext;
  class Wildcard_patternContext;
  class Value_patternContext;
  class AttrContext;
  class Name_or_attrContext;
  class Group_patternContext;
  class Sequence_patternContext;
  class Open_sequence_patternContext;
  class Maybe_sequence_patternContext;
  class Maybe_star_patternContext;
  class Star_patternContext;
  class Mapping_patternContext;
  class Items_patternContext;
  class Key_value_patternContext;
  class Double_star_patternContext;
  class Class_patternContext;
  class Positional_patternsContext;
  class Keyword_patternsContext;
  class Keyword_patternContext;
  class Type_aliasContext;
  class Type_paramsContext;
  class Type_param_seqContext;
  class Type_paramContext;
  class Type_param_boundContext;
  class ExpressionsContext;
  class ExpressionContext;
  class Yield_exprContext;
  class Star_expressionsContext;
  class Star_expressionContext;
  class Star_named_expressionsContext;
  class Star_named_expressionContext;
  class Assignment_expressionContext;
  class Named_expressionContext;
  class DisjunctionContext;
  class ConjunctionContext;
  class InversionContext;
  class ComparisonContext;
  class Compare_op_bitwise_or_pairContext;
  class Eq_bitwise_orContext;
  class Noteq_bitwise_orContext;
  class Lte_bitwise_orContext;
  class Lt_bitwise_orContext;
  class Gte_bitwise_orContext;
  class Gt_bitwise_orContext;
  class Notin_bitwise_orContext;
  class In_bitwise_orContext;
  class Isnot_bitwise_orContext;
  class Is_bitwise_orContext;
  class Bitwise_orContext;
  class Bitwise_xorContext;
  class Bitwise_andContext;
  class Shift_exprContext;
  class SumContext;
  class TermContext;
  class FactorContext;
  class PowerContext;
  class Await_primaryContext;
  class PrimaryContext;
  class SlicesContext;
  class SliceContext;
  class AtomContext;
  class GroupContext;
  class LambdefContext;
  class Lambda_paramsContext;
  class Lambda_parametersContext;
  class Lambda_slash_no_defaultContext;
  class Lambda_slash_with_defaultContext;
  class Lambda_star_etcContext;
  class Lambda_kwdsContext;
  class Lambda_param_no_defaultContext;
  class Lambda_param_with_defaultContext;
  class Lambda_param_maybe_defaultContext;
  class Lambda_paramContext;
  class Fstring_middle_no_quoteContext;
  class Fstring_middle_no_single_quoteContext;
  class Fstring_middle_breaks_no_triple_quoteContext;
  class Fstring_middle_breaks_no_triple_single_quoteContext;
  class Fstring_any_no_quoteContext;
  class Fstring_any_no_single_quoteContext;
  class Fstring_middleContext;
  class Fstring_any_breaks_no_triple_quoteContext;
  class Fstring_any_breaks_no_triple_single_quoteContext;
  class Fstring_anyContext;
  class Fstring_replacement_fieldContext;
  class Fstring_conversionContext;
  class Fstring_full_format_specContext;
  class Fstring_format_specContext;
  class FstringContext;
  class StringContext;
  class StringsContext;
  class ListContext;
  class TupleContext;
  class SetContext;
  class DictContext;
  class Double_starred_kvpairsContext;
  class Double_starred_kvpairContext;
  class KvpairContext;
  class For_if_clausesContext;
  class For_if_clauseContext;
  class ListcompContext;
  class SetcompContext;
  class GenexpContext;
  class DictcompContext;
  class ArgumentsContext;
  class ArgsContext;
  class ArgContext;
  class KwargsContext;
  class Starred_expressionContext;
  class Kwarg_or_starredContext;
  class Kwarg_or_double_starredContext;
  class Star_targetsContext;
  class Star_targets_list_seqContext;
  class Star_targets_tuple_seqContext;
  class Star_targetContext;
  class Target_with_star_atomContext;
  class Star_atomContext;
  class Single_targetContext;
  class Single_subscript_attribute_targetContext;
  class T_primaryContext;
  class Del_targetsContext;
  class Del_targetContext;
  class Del_t_atomContext;
  class Type_expressionsContext;
  class Func_type_commentContext;
  class IdentifierContext; 

  class  FandangoContext : public antlr4::ParserRuleContext {
  public:
    FandangoContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ProgramContext *program();
    antlr4::tree::TerminalNode *EOF();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FandangoContext* fandango();

  class  ProgramContext : public antlr4::ParserRuleContext {
  public:
    ProgramContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);
    std::vector<StatementContext *> statement();
    StatementContext* statement(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ProgramContext* program();

  class  StatementContext : public antlr4::ParserRuleContext {
  public:
    StatementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ProductionContext *production();
    ConstraintContext *constraint();
    PythonContext *python();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StatementContext* statement();

  class  ProductionContext : public antlr4::ParserRuleContext {
  public:
    ProductionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    NonterminalContext *nonterminal();
    antlr4::tree::TerminalNode *GRAMMAR_ASSIGN();
    AlternativeContext *alternative();
    antlr4::tree::TerminalNode *SEMI_COLON();
    antlr4::tree::TerminalNode *EOF();
    std::vector<antlr4::tree::TerminalNode *> INDENT();
    antlr4::tree::TerminalNode* INDENT(size_t i);
    antlr4::tree::TerminalNode *EXPR_ASSIGN();
    ExpressionContext *expression();
    std::vector<antlr4::tree::TerminalNode *> DEDENT();
    antlr4::tree::TerminalNode* DEDENT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);
    antlr4::tree::TerminalNode *ASSIGN();
    std::vector<antlr4::tree::TerminalNode *> COLON();
    antlr4::tree::TerminalNode* COLON(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ProductionContext* production();

  class  AlternativeContext : public antlr4::ParserRuleContext {
  public:
    AlternativeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ConcatenationContext *> concatenation();
    ConcatenationContext* concatenation(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR_OP();
    antlr4::tree::TerminalNode* OR_OP(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AlternativeContext* alternative();

  class  ConcatenationContext : public antlr4::ParserRuleContext {
  public:
    ConcatenationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<OperatorContext *> operator_();
    OperatorContext* operator_(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConcatenationContext* concatenation();

  class  OperatorContext : public antlr4::ParserRuleContext {
  public:
    OperatorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SymbolContext *symbol();
    KleeneContext *kleene();
    PlusContext *plus();
    OptionContext *option();
    RepeatContext *repeat();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  OperatorContext* operator_();

  class  KleeneContext : public antlr4::ParserRuleContext {
  public:
    KleeneContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SymbolContext *symbol();
    antlr4::tree::TerminalNode *STAR();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  KleeneContext* kleene();

  class  PlusContext : public antlr4::ParserRuleContext {
  public:
    PlusContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SymbolContext *symbol();
    antlr4::tree::TerminalNode *ADD();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PlusContext* plus();

  class  OptionContext : public antlr4::ParserRuleContext {
  public:
    OptionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SymbolContext *symbol();
    antlr4::tree::TerminalNode *QUESTION();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  OptionContext* option();

  class  RepeatContext : public antlr4::ParserRuleContext {
  public:
    RepeatContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SymbolContext *symbol();
    antlr4::tree::TerminalNode *OPEN_BRACE();
    antlr4::tree::TerminalNode *CLOSE_BRACE();
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  RepeatContext* repeat();

  class  SymbolContext : public antlr4::ParserRuleContext {
  public:
    SymbolContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Nonterminal_rightContext *nonterminal_right();
    StringContext *string();
    antlr4::tree::TerminalNode *NUMBER();
    Generator_callContext *generator_call();
    Char_setContext *char_set();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    AlternativeContext *alternative();
    antlr4::tree::TerminalNode *CLOSE_PAREN();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SymbolContext* symbol();

  class  Nonterminal_rightContext : public antlr4::ParserRuleContext {
  public:
    Nonterminal_rightContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LESS_THAN();
    std::vector<IdentifierContext *> identifier();
    IdentifierContext* identifier(size_t i);
    antlr4::tree::TerminalNode *GREATER_THAN();
    std::vector<antlr4::tree::TerminalNode *> COLON();
    antlr4::tree::TerminalNode* COLON(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Nonterminal_rightContext* nonterminal_right();

  class  NonterminalContext : public antlr4::ParserRuleContext {
  public:
    NonterminalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LESS_THAN();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *GREATER_THAN();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  NonterminalContext* nonterminal();

  class  Generator_callContext : public antlr4::ParserRuleContext {
  public:
    Generator_callContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    Generator_callContext *generator_call();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    SlicesContext *slices();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    GenexpContext *genexp();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    ArgumentsContext *arguments();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Generator_callContext* generator_call();
  Generator_callContext* generator_call(int precedence);
  class  Char_setContext : public antlr4::ParserRuleContext {
  public:
    Char_setContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACK();
    StringContext *string();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    antlr4::tree::TerminalNode *XOR();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Char_setContext* char_set();

  class  ConstraintContext : public antlr4::ParserRuleContext {
  public:
    ConstraintContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *WHERE();
    ImpliesContext *implies();
    std::vector<antlr4::tree::TerminalNode *> INDENT();
    antlr4::tree::TerminalNode* INDENT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DEDENT();
    antlr4::tree::TerminalNode* DEDENT(size_t i);
    antlr4::tree::TerminalNode *MINIMIZING();
    ExprContext *expr();
    antlr4::tree::TerminalNode *SEMI_COLON();
    antlr4::tree::TerminalNode *EOF();
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);
    antlr4::tree::TerminalNode *MAXIMIZING();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConstraintContext* constraint();

  class  ImpliesContext : public antlr4::ParserRuleContext {
  public:
    ImpliesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Formula_disjunctionContext *> formula_disjunction();
    Formula_disjunctionContext* formula_disjunction(size_t i);
    antlr4::tree::TerminalNode *ARROW();
    antlr4::tree::TerminalNode *SEMI_COLON();
    antlr4::tree::TerminalNode *NEWLINE();
    antlr4::tree::TerminalNode *EOF();
    QuantifierContext *quantifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ImpliesContext* implies();

  class  QuantifierContext : public antlr4::ParserRuleContext {
  public:
    QuantifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FORALL();
    NonterminalContext *nonterminal();
    antlr4::tree::TerminalNode *IN();
    Dot_selectionContext *dot_selection();
    antlr4::tree::TerminalNode *COLON();
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);
    antlr4::tree::TerminalNode *INDENT();
    QuantifierContext *quantifier();
    antlr4::tree::TerminalNode *DEDENT();
    antlr4::tree::TerminalNode *EXISTS();
    antlr4::tree::TerminalNode *ANY();
    std::vector<antlr4::tree::TerminalNode *> OPEN_PAREN();
    antlr4::tree::TerminalNode* OPEN_PAREN(size_t i);
    Quantifier_in_lineContext *quantifier_in_line();
    antlr4::tree::TerminalNode *FOR();
    Star_selectionContext *star_selection();
    std::vector<antlr4::tree::TerminalNode *> CLOSE_PAREN();
    antlr4::tree::TerminalNode* CLOSE_PAREN(size_t i);
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *SEMI_COLON();
    antlr4::tree::TerminalNode *EOF();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    antlr4::tree::TerminalNode *OPEN_BRACE();
    antlr4::tree::TerminalNode *CLOSE_BRACE();
    antlr4::tree::TerminalNode *ALL();
    Formula_disjunctionContext *formula_disjunction();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  QuantifierContext* quantifier();

  class  Quantifier_in_lineContext : public antlr4::ParserRuleContext {
  public:
    Quantifier_in_lineContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ANY();
    std::vector<antlr4::tree::TerminalNode *> OPEN_PAREN();
    antlr4::tree::TerminalNode* OPEN_PAREN(size_t i);
    Quantifier_in_lineContext *quantifier_in_line();
    antlr4::tree::TerminalNode *FOR();
    antlr4::tree::TerminalNode *IN();
    Star_selectionContext *star_selection();
    std::vector<antlr4::tree::TerminalNode *> CLOSE_PAREN();
    antlr4::tree::TerminalNode* CLOSE_PAREN(size_t i);
    NonterminalContext *nonterminal();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    antlr4::tree::TerminalNode *OPEN_BRACE();
    antlr4::tree::TerminalNode *CLOSE_BRACE();
    antlr4::tree::TerminalNode *ALL();
    Formula_disjunctionContext *formula_disjunction();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Quantifier_in_lineContext* quantifier_in_line();

  class  Formula_disjunctionContext : public antlr4::ParserRuleContext {
  public:
    Formula_disjunctionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Formula_conjunctionContext *> formula_conjunction();
    Formula_conjunctionContext* formula_conjunction(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR();
    antlr4::tree::TerminalNode* OR(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Formula_disjunctionContext* formula_disjunction();

  class  Formula_conjunctionContext : public antlr4::ParserRuleContext {
  public:
    Formula_conjunctionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Formula_atomContext *> formula_atom();
    Formula_atomContext* formula_atom(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AND();
    antlr4::tree::TerminalNode* AND(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Formula_conjunctionContext* formula_conjunction();

  class  Formula_atomContext : public antlr4::ParserRuleContext {
  public:
    Formula_atomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Formula_comparisonContext *formula_comparison();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    ImpliesContext *implies();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    ExprContext *expr();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Formula_atomContext* formula_atom();

  class  Formula_comparisonContext : public antlr4::ParserRuleContext {
  public:
    Formula_comparisonContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExprContext *> expr();
    ExprContext* expr(size_t i);
    antlr4::tree::TerminalNode *LESS_THAN();
    antlr4::tree::TerminalNode *GREATER_THAN();
    antlr4::tree::TerminalNode *EQUALS();
    antlr4::tree::TerminalNode *GT_EQ();
    antlr4::tree::TerminalNode *LT_EQ();
    antlr4::tree::TerminalNode *NOT_EQ_1();
    antlr4::tree::TerminalNode *NOT_EQ_2();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Formula_comparisonContext* formula_comparison();

  class  ExprContext : public antlr4::ParserRuleContext {
  public:
    ExprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Selector_lengthContext *selector_length();
    std::vector<InversionContext *> inversion();
    InversionContext* inversion(size_t i);
    antlr4::tree::TerminalNode *IF();
    antlr4::tree::TerminalNode *ELSE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExprContext* expr();

  class  Selector_lengthContext : public antlr4::ParserRuleContext {
  public:
    Selector_lengthContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> OR_OP();
    antlr4::tree::TerminalNode* OR_OP(size_t i);
    Dot_selectionContext *dot_selection();
    antlr4::tree::TerminalNode *LEN();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    Star_selectionContext *star_selection();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Star_selection_or_dot_selectionContext *star_selection_or_dot_selection();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Selector_lengthContext* selector_length();

  class  Star_selection_or_dot_selectionContext : public antlr4::ParserRuleContext {
  public:
    Star_selection_or_dot_selectionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Star_selectionContext *star_selection();
    Dot_selectionContext *dot_selection();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_selection_or_dot_selectionContext* star_selection_or_dot_selection();

  class  Star_selectionContext : public antlr4::ParserRuleContext {
  public:
    Star_selectionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    Dot_selectionContext *dot_selection();
    antlr4::tree::TerminalNode *POWER();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_selectionContext* star_selection();

  class  Dot_selectionContext : public antlr4::ParserRuleContext {
  public:
    Dot_selectionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SelectionContext *selection();
    Dot_selectionContext *dot_selection();
    antlr4::tree::TerminalNode *DOT();
    antlr4::tree::TerminalNode *DOTDOT();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Dot_selectionContext* dot_selection();
  Dot_selectionContext* dot_selection(int precedence);
  class  SelectionContext : public antlr4::ParserRuleContext {
  public:
    SelectionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Base_selectionContext *base_selection();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    Rs_slicesContext *rs_slices();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    antlr4::tree::TerminalNode *OPEN_BRACE();
    Rs_pairsContext *rs_pairs();
    antlr4::tree::TerminalNode *CLOSE_BRACE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SelectionContext* selection();

  class  Base_selectionContext : public antlr4::ParserRuleContext {
  public:
    Base_selectionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    NonterminalContext *nonterminal();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    Dot_selectionContext *dot_selection();
    antlr4::tree::TerminalNode *CLOSE_PAREN();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Base_selectionContext* base_selection();

  class  Rs_pairsContext : public antlr4::ParserRuleContext {
  public:
    Rs_pairsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Rs_pairContext *> rs_pair();
    Rs_pairContext* rs_pair(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Rs_pairsContext* rs_pairs();

  class  Rs_pairContext : public antlr4::ParserRuleContext {
  public:
    Rs_pairContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    NonterminalContext *nonterminal();
    antlr4::tree::TerminalNode *COLON();
    Rs_sliceContext *rs_slice();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Rs_pairContext* rs_pair();

  class  Rs_slicesContext : public antlr4::ParserRuleContext {
  public:
    Rs_slicesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Rs_sliceContext *> rs_slice();
    Rs_sliceContext* rs_slice(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Rs_slicesContext* rs_slices();

  class  Rs_sliceContext : public antlr4::ParserRuleContext {
  public:
    Rs_sliceContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> NUMBER();
    antlr4::tree::TerminalNode* NUMBER(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COLON();
    antlr4::tree::TerminalNode* COLON(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Rs_sliceContext* rs_slice();

  class  PythonContext : public antlr4::ParserRuleContext {
  public:
    PythonContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Compound_stmtContext *compound_stmt();
    Simple_stmtContext *simple_stmt();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PythonContext* python();

  class  Python_tagContext : public antlr4::ParserRuleContext {
  public:
    Python_tagContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    StmtContext *stmt();
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Python_tagContext* python_tag();

  class  Python_fileContext : public antlr4::ParserRuleContext {
  public:
    Python_fileContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    StatementsContext *statements();
    antlr4::tree::TerminalNode *EOF();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Python_fileContext* python_file();

  class  InteractiveContext : public antlr4::ParserRuleContext {
  public:
    InteractiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Statement_newlineContext *statement_newline();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InteractiveContext* interactive();

  class  EvalContext : public antlr4::ParserRuleContext {
  public:
    EvalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExpressionsContext *expressions();
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);
    antlr4::tree::TerminalNode *EOF();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EvalContext* eval();

  class  Func_typeContext : public antlr4::ParserRuleContext {
  public:
    Func_typeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    antlr4::tree::TerminalNode *ARROW();
    ExpressionContext *expression();
    Type_expressionsContext *type_expressions();
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);
    antlr4::tree::TerminalNode *EOF();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Func_typeContext* func_type();

  class  StatementsContext : public antlr4::ParserRuleContext {
  public:
    StatementsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<StmtContext *> stmt();
    StmtContext* stmt(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StatementsContext* statements();

  class  StmtContext : public antlr4::ParserRuleContext {
  public:
    StmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Compound_stmtContext *compound_stmt();
    Simple_stmtsContext *simple_stmts();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StmtContext* stmt();

  class  Statement_newlineContext : public antlr4::ParserRuleContext {
  public:
    Statement_newlineContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Compound_stmtContext *compound_stmt();
    antlr4::tree::TerminalNode *NEWLINE();
    Simple_stmtsContext *simple_stmts();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Statement_newlineContext* statement_newline();

  class  Simple_stmtsContext : public antlr4::ParserRuleContext {
  public:
    Simple_stmtsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Simple_stmtContext *> simple_stmt();
    Simple_stmtContext* simple_stmt(size_t i);
    antlr4::tree::TerminalNode *EOF();
    std::vector<antlr4::tree::TerminalNode *> SEMI_COLON();
    antlr4::tree::TerminalNode* SEMI_COLON(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Simple_stmtsContext* simple_stmts();

  class  Simple_stmtContext : public antlr4::ParserRuleContext {
  public:
    Simple_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AssignmentContext *assignment();
    Type_aliasContext *type_alias();
    Star_expressionsContext *star_expressions();
    Return_stmtContext *return_stmt();
    Import_stmtContext *import_stmt();
    Raise_stmtContext *raise_stmt();
    antlr4::tree::TerminalNode *PASS();
    Del_stmtContext *del_stmt();
    Yield_stmtContext *yield_stmt();
    Assert_stmtContext *assert_stmt();
    antlr4::tree::TerminalNode *BREAK();
    antlr4::tree::TerminalNode *CONTINUE();
    Global_stmtContext *global_stmt();
    Nonlocal_stmtContext *nonlocal_stmt();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Simple_stmtContext* simple_stmt();

  class  Compound_stmtContext : public antlr4::ParserRuleContext {
  public:
    Compound_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Function_defContext *function_def();
    If_stmtContext *if_stmt();
    Class_defContext *class_def();
    With_stmtContext *with_stmt();
    For_stmtContext *for_stmt();
    Try_stmtContext *try_stmt();
    While_stmtContext *while_stmt();
    Match_stmtContext *match_stmt();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Compound_stmtContext* compound_stmt();

  class  AssignmentContext : public antlr4::ParserRuleContext {
  public:
    AssignmentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();
    std::vector<antlr4::tree::TerminalNode *> ASSIGN();
    antlr4::tree::TerminalNode* ASSIGN(size_t i);
    Annotated_rhsContext *annotated_rhs();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    Single_targetContext *single_target();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Single_subscript_attribute_targetContext *single_subscript_attribute_target();
    Yield_exprContext *yield_expr();
    Star_expressionsContext *star_expressions();
    std::vector<Star_targetsContext *> star_targets();
    Star_targetsContext* star_targets(size_t i);
    AugassignContext *augassign();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AssignmentContext* assignment();

  class  Annotated_rhsContext : public antlr4::ParserRuleContext {
  public:
    Annotated_rhsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Yield_exprContext *yield_expr();
    Star_expressionsContext *star_expressions();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Annotated_rhsContext* annotated_rhs();

  class  AugassignContext : public antlr4::ParserRuleContext {
  public:
    AugassignContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ADD_ASSIGN();
    antlr4::tree::TerminalNode *SUB_ASSIGN();
    antlr4::tree::TerminalNode *MULT_ASSIGN();
    antlr4::tree::TerminalNode *AT_ASSIGN();
    antlr4::tree::TerminalNode *DIV_ASSIGN();
    antlr4::tree::TerminalNode *MOD_ASSIGN();
    antlr4::tree::TerminalNode *AND_ASSIGN();
    antlr4::tree::TerminalNode *OR_ASSIGN();
    antlr4::tree::TerminalNode *XOR_ASSIGN();
    antlr4::tree::TerminalNode *LEFT_SHIFT_ASSIGN();
    antlr4::tree::TerminalNode *RIGHT_SHIFT_ASSIGN();
    antlr4::tree::TerminalNode *POWER_ASSIGN();
    antlr4::tree::TerminalNode *IDIV_ASSIGN();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AugassignContext* augassign();

  class  Return_stmtContext : public antlr4::ParserRuleContext {
  public:
    Return_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *RETURN();
    Star_expressionsContext *star_expressions();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Return_stmtContext* return_stmt();

  class  Raise_stmtContext : public antlr4::ParserRuleContext {
  public:
    Raise_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *RAISE();
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *FROM();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Raise_stmtContext* raise_stmt();

  class  Global_stmtContext : public antlr4::ParserRuleContext {
  public:
    Global_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *GLOBAL();
    std::vector<IdentifierContext *> identifier();
    IdentifierContext* identifier(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Global_stmtContext* global_stmt();

  class  Nonlocal_stmtContext : public antlr4::ParserRuleContext {
  public:
    Nonlocal_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NONLOCAL();
    std::vector<IdentifierContext *> identifier();
    IdentifierContext* identifier(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Nonlocal_stmtContext* nonlocal_stmt();

  class  Del_stmtContext : public antlr4::ParserRuleContext {
  public:
    Del_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEL();
    Del_targetsContext *del_targets();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Del_stmtContext* del_stmt();

  class  Yield_stmtContext : public antlr4::ParserRuleContext {
  public:
    Yield_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Yield_exprContext *yield_expr();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Yield_stmtContext* yield_stmt();

  class  Assert_stmtContext : public antlr4::ParserRuleContext {
  public:
    Assert_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ASSERT();
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Assert_stmtContext* assert_stmt();

  class  Import_stmtContext : public antlr4::ParserRuleContext {
  public:
    Import_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Import_nameContext *import_name();
    Import_fromContext *import_from();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Import_stmtContext* import_stmt();

  class  Import_nameContext : public antlr4::ParserRuleContext {
  public:
    Import_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IMPORT();
    Dotted_as_namesContext *dotted_as_names();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Import_nameContext* import_name();

  class  Import_fromContext : public antlr4::ParserRuleContext {
  public:
    Import_fromContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FROM();
    Dotted_nameContext *dotted_name();
    antlr4::tree::TerminalNode *IMPORT();
    Import_from_targetsContext *import_from_targets();
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ELLIPSIS();
    antlr4::tree::TerminalNode* ELLIPSIS(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Import_fromContext* import_from();

  class  Import_from_targetsContext : public antlr4::ParserRuleContext {
  public:
    Import_from_targetsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_PAREN();
    Import_from_as_namesContext *import_from_as_names();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    antlr4::tree::TerminalNode *COMMA();
    antlr4::tree::TerminalNode *STAR();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Import_from_targetsContext* import_from_targets();

  class  Import_from_as_namesContext : public antlr4::ParserRuleContext {
  public:
    Import_from_as_namesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Import_from_as_nameContext *> import_from_as_name();
    Import_from_as_nameContext* import_from_as_name(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Import_from_as_namesContext* import_from_as_names();

  class  Import_from_as_nameContext : public antlr4::ParserRuleContext {
  public:
    Import_from_as_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<IdentifierContext *> identifier();
    IdentifierContext* identifier(size_t i);
    antlr4::tree::TerminalNode *AS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Import_from_as_nameContext* import_from_as_name();

  class  Dotted_as_namesContext : public antlr4::ParserRuleContext {
  public:
    Dotted_as_namesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Dotted_as_nameContext *> dotted_as_name();
    Dotted_as_nameContext* dotted_as_name(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Dotted_as_namesContext* dotted_as_names();

  class  Dotted_as_nameContext : public antlr4::ParserRuleContext {
  public:
    Dotted_as_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Dotted_nameContext *dotted_name();
    antlr4::tree::TerminalNode *AS();
    IdentifierContext *identifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Dotted_as_nameContext* dotted_as_name();

  class  Dotted_nameContext : public antlr4::ParserRuleContext {
  public:
    Dotted_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    Dotted_nameContext *dotted_name();
    antlr4::tree::TerminalNode *DOT();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Dotted_nameContext* dotted_name();
  Dotted_nameContext* dotted_name(int precedence);
  class  BlockContext : public antlr4::ParserRuleContext {
  public:
    BlockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NEWLINE();
    antlr4::tree::TerminalNode *INDENT();
    StatementsContext *statements();
    antlr4::tree::TerminalNode *DEDENT();
    Simple_stmtsContext *simple_stmts();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  BlockContext* block();

  class  DecoratorsContext : public antlr4::ParserRuleContext {
  public:
    DecoratorsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> AT();
    antlr4::tree::TerminalNode* AT(size_t i);
    std::vector<Named_expressionContext *> named_expression();
    Named_expressionContext* named_expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NEWLINE();
    antlr4::tree::TerminalNode* NEWLINE(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DecoratorsContext* decorators();

  class  Class_defContext : public antlr4::ParserRuleContext {
  public:
    Class_defContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Class_def_rawContext *class_def_raw();
    DecoratorsContext *decorators();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Class_defContext* class_def();

  class  Class_def_rawContext : public antlr4::ParserRuleContext {
  public:
    Class_def_rawContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CLASS();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    Type_paramsContext *type_params();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    ArgumentsContext *arguments();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Class_def_rawContext* class_def_raw();

  class  Function_defContext : public antlr4::ParserRuleContext {
  public:
    Function_defContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Function_def_rawContext *function_def_raw();
    DecoratorsContext *decorators();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Function_defContext* function_def();

  class  Function_def_rawContext : public antlr4::ParserRuleContext {
  public:
    Function_def_rawContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEF();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    antlr4::tree::TerminalNode *ASYNC();
    Type_paramsContext *type_params();
    ParamsContext *params();
    antlr4::tree::TerminalNode *ARROW();
    ExpressionContext *expression();
    Func_type_commentContext *func_type_comment();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Function_def_rawContext* function_def_raw();

  class  ParamsContext : public antlr4::ParserRuleContext {
  public:
    ParamsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ParametersContext *parameters();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ParamsContext* params();

  class  ParametersContext : public antlr4::ParserRuleContext {
  public:
    ParametersContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Slash_no_defaultContext *slash_no_default();
    std::vector<Param_no_defaultContext *> param_no_default();
    Param_no_defaultContext* param_no_default(size_t i);
    std::vector<Param_with_defaultContext *> param_with_default();
    Param_with_defaultContext* param_with_default(size_t i);
    Star_etcContext *star_etc();
    Slash_with_defaultContext *slash_with_default();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ParametersContext* parameters();

  class  Slash_no_defaultContext : public antlr4::ParserRuleContext {
  public:
    Slash_no_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DIV();
    std::vector<Param_no_defaultContext *> param_no_default();
    Param_no_defaultContext* param_no_default(size_t i);
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Slash_no_defaultContext* slash_no_default();

  class  Slash_with_defaultContext : public antlr4::ParserRuleContext {
  public:
    Slash_with_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DIV();
    std::vector<Param_no_defaultContext *> param_no_default();
    Param_no_defaultContext* param_no_default(size_t i);
    std::vector<Param_with_defaultContext *> param_with_default();
    Param_with_defaultContext* param_with_default(size_t i);
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Slash_with_defaultContext* slash_with_default();

  class  Star_etcContext : public antlr4::ParserRuleContext {
  public:
    Star_etcContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    Param_no_defaultContext *param_no_default();
    std::vector<Param_maybe_defaultContext *> param_maybe_default();
    Param_maybe_defaultContext* param_maybe_default(size_t i);
    KwdsContext *kwds();
    Param_no_default_star_annotationContext *param_no_default_star_annotation();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_etcContext* star_etc();

  class  KwdsContext : public antlr4::ParserRuleContext {
  public:
    KwdsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *POWER();
    Param_no_defaultContext *param_no_default();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  KwdsContext* kwds();

  class  Param_no_defaultContext : public antlr4::ParserRuleContext {
  public:
    Param_no_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ParamContext *param();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Param_no_defaultContext* param_no_default();

  class  Param_no_default_star_annotationContext : public antlr4::ParserRuleContext {
  public:
    Param_no_default_star_annotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Param_star_annotationContext *param_star_annotation();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Param_no_default_star_annotationContext* param_no_default_star_annotation();

  class  Param_with_defaultContext : public antlr4::ParserRuleContext {
  public:
    Param_with_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ParamContext *param();
    DefaultContext *default_();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Param_with_defaultContext* param_with_default();

  class  Param_maybe_defaultContext : public antlr4::ParserRuleContext {
  public:
    Param_maybe_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ParamContext *param();
    antlr4::tree::TerminalNode *COMMA();
    DefaultContext *default_();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Param_maybe_defaultContext* param_maybe_default();

  class  ParamContext : public antlr4::ParserRuleContext {
  public:
    ParamContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    AnnotationContext *annotation();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ParamContext* param();

  class  Param_star_annotationContext : public antlr4::ParserRuleContext {
  public:
    Param_star_annotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    Star_annotationContext *star_annotation();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Param_star_annotationContext* param_star_annotation();

  class  AnnotationContext : public antlr4::ParserRuleContext {
  public:
    AnnotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AnnotationContext* annotation();

  class  Star_annotationContext : public antlr4::ParserRuleContext {
  public:
    Star_annotationContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *COLON();
    Star_expressionContext *star_expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_annotationContext* star_annotation();

  class  DefaultContext : public antlr4::ParserRuleContext {
  public:
    DefaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ASSIGN();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DefaultContext* default_();

  class  If_stmtContext : public antlr4::ParserRuleContext {
  public:
    If_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IF();
    Named_expressionContext *named_expression();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    Elif_stmtContext *elif_stmt();
    Else_blockContext *else_block();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  If_stmtContext* if_stmt();

  class  Elif_stmtContext : public antlr4::ParserRuleContext {
  public:
    Elif_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ELIF();
    Named_expressionContext *named_expression();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    Elif_stmtContext *elif_stmt();
    Else_blockContext *else_block();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Elif_stmtContext* elif_stmt();

  class  Else_blockContext : public antlr4::ParserRuleContext {
  public:
    Else_blockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ELSE();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Else_blockContext* else_block();

  class  While_stmtContext : public antlr4::ParserRuleContext {
  public:
    While_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *WHILE();
    Named_expressionContext *named_expression();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    Else_blockContext *else_block();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  While_stmtContext* while_stmt();

  class  For_stmtContext : public antlr4::ParserRuleContext {
  public:
    For_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FOR();
    Star_targetsContext *star_targets();
    antlr4::tree::TerminalNode *IN();
    Star_expressionsContext *star_expressions();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    Else_blockContext *else_block();
    antlr4::tree::TerminalNode *ASYNC();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  For_stmtContext* for_stmt();

  class  With_stmtContext : public antlr4::ParserRuleContext {
  public:
    With_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *WITH();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    std::vector<With_itemContext *> with_item();
    With_itemContext* with_item(size_t i);
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    antlr4::tree::TerminalNode *ASYNC();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  With_stmtContext* with_stmt();

  class  With_itemContext : public antlr4::ParserRuleContext {
  public:
    With_itemContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *AS();
    Star_targetContext *star_target();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  With_itemContext* with_item();

  class  Try_stmtContext : public antlr4::ParserRuleContext {
  public:
    Try_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *TRY();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    Finally_blockContext *finally_block();
    std::vector<Except_blockContext *> except_block();
    Except_blockContext* except_block(size_t i);
    Else_blockContext *else_block();
    std::vector<Except_star_blockContext *> except_star_block();
    Except_star_blockContext* except_star_block(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Try_stmtContext* try_stmt();

  class  Except_blockContext : public antlr4::ParserRuleContext {
  public:
    Except_blockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EXCEPT();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    antlr4::tree::TerminalNode *AS();
    IdentifierContext *identifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Except_blockContext* except_block();

  class  Except_star_blockContext : public antlr4::ParserRuleContext {
  public:
    Except_star_blockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EXCEPT();
    antlr4::tree::TerminalNode *STAR();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    antlr4::tree::TerminalNode *AS();
    IdentifierContext *identifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Except_star_blockContext* except_star_block();

  class  Finally_blockContext : public antlr4::ParserRuleContext {
  public:
    Finally_blockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FINALLY();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Finally_blockContext* finally_block();

  class  Match_stmtContext : public antlr4::ParserRuleContext {
  public:
    Match_stmtContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *MATCH();
    Subject_exprContext *subject_expr();
    antlr4::tree::TerminalNode *COLON();
    antlr4::tree::TerminalNode *NEWLINE();
    antlr4::tree::TerminalNode *INDENT();
    antlr4::tree::TerminalNode *DEDENT();
    std::vector<Case_blockContext *> case_block();
    Case_blockContext* case_block(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Match_stmtContext* match_stmt();

  class  Subject_exprContext : public antlr4::ParserRuleContext {
  public:
    Subject_exprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Star_named_expressionContext *star_named_expression();
    antlr4::tree::TerminalNode *COMMA();
    Star_named_expressionsContext *star_named_expressions();
    Named_expressionContext *named_expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Subject_exprContext* subject_expr();

  class  Case_blockContext : public antlr4::ParserRuleContext {
  public:
    Case_blockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CASE();
    PatternsContext *patterns();
    antlr4::tree::TerminalNode *COLON();
    BlockContext *block();
    GuardContext *guard();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Case_blockContext* case_block();

  class  GuardContext : public antlr4::ParserRuleContext {
  public:
    GuardContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IF();
    Named_expressionContext *named_expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  GuardContext* guard();

  class  PatternsContext : public antlr4::ParserRuleContext {
  public:
    PatternsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Open_sequence_patternContext *open_sequence_pattern();
    PatternContext *pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PatternsContext* patterns();

  class  PatternContext : public antlr4::ParserRuleContext {
  public:
    PatternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    As_patternContext *as_pattern();
    Or_patternContext *or_pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PatternContext* pattern();

  class  As_patternContext : public antlr4::ParserRuleContext {
  public:
    As_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Or_patternContext *or_pattern();
    antlr4::tree::TerminalNode *AS();
    Pattern_capture_targetContext *pattern_capture_target();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  As_patternContext* as_pattern();

  class  Or_patternContext : public antlr4::ParserRuleContext {
  public:
    Or_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Closed_patternContext *> closed_pattern();
    Closed_patternContext* closed_pattern(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR_OP();
    antlr4::tree::TerminalNode* OR_OP(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Or_patternContext* or_pattern();

  class  Closed_patternContext : public antlr4::ParserRuleContext {
  public:
    Closed_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Literal_patternContext *literal_pattern();
    Capture_patternContext *capture_pattern();
    Wildcard_patternContext *wildcard_pattern();
    Value_patternContext *value_pattern();
    Group_patternContext *group_pattern();
    Sequence_patternContext *sequence_pattern();
    Mapping_patternContext *mapping_pattern();
    Class_patternContext *class_pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Closed_patternContext* closed_pattern();

  class  Literal_patternContext : public antlr4::ParserRuleContext {
  public:
    Literal_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Signed_numberContext *signed_number();
    Complex_numberContext *complex_number();
    StringsContext *strings();
    antlr4::tree::TerminalNode *NONE();
    antlr4::tree::TerminalNode *TRUE();
    antlr4::tree::TerminalNode *FALSE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Literal_patternContext* literal_pattern();

  class  Literal_exprContext : public antlr4::ParserRuleContext {
  public:
    Literal_exprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Signed_numberContext *signed_number();
    Complex_numberContext *complex_number();
    StringsContext *strings();
    antlr4::tree::TerminalNode *NONE();
    antlr4::tree::TerminalNode *TRUE();
    antlr4::tree::TerminalNode *FALSE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Literal_exprContext* literal_expr();

  class  Complex_numberContext : public antlr4::ParserRuleContext {
  public:
    Complex_numberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Signed_real_numberContext *signed_real_number();
    antlr4::tree::TerminalNode *ADD();
    Imaginary_numberContext *imaginary_number();
    antlr4::tree::TerminalNode *MINUS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Complex_numberContext* complex_number();

  class  Signed_numberContext : public antlr4::ParserRuleContext {
  public:
    Signed_numberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NUMBER();
    antlr4::tree::TerminalNode *MINUS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Signed_numberContext* signed_number();

  class  Signed_real_numberContext : public antlr4::ParserRuleContext {
  public:
    Signed_real_numberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Real_numberContext *real_number();
    antlr4::tree::TerminalNode *MINUS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Signed_real_numberContext* signed_real_number();

  class  Real_numberContext : public antlr4::ParserRuleContext {
  public:
    Real_numberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NUMBER();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Real_numberContext* real_number();

  class  Imaginary_numberContext : public antlr4::ParserRuleContext {
  public:
    Imaginary_numberContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NUMBER();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Imaginary_numberContext* imaginary_number();

  class  Capture_patternContext : public antlr4::ParserRuleContext {
  public:
    Capture_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Pattern_capture_targetContext *pattern_capture_target();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Capture_patternContext* capture_pattern();

  class  Pattern_capture_targetContext : public antlr4::ParserRuleContext {
  public:
    Pattern_capture_targetContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Pattern_capture_targetContext* pattern_capture_target();

  class  Wildcard_patternContext : public antlr4::ParserRuleContext {
  public:
    Wildcard_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNDERSCORE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Wildcard_patternContext* wildcard_pattern();

  class  Value_patternContext : public antlr4::ParserRuleContext {
  public:
    Value_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AttrContext *attr();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Value_patternContext* value_pattern();

  class  AttrContext : public antlr4::ParserRuleContext {
  public:
    AttrContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Name_or_attrContext *name_or_attr();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AttrContext* attr();

  class  Name_or_attrContext : public antlr4::ParserRuleContext {
  public:
    Name_or_attrContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    Name_or_attrContext *name_or_attr();
    antlr4::tree::TerminalNode *DOT();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Name_or_attrContext* name_or_attr();
  Name_or_attrContext* name_or_attr(int precedence);
  class  Group_patternContext : public antlr4::ParserRuleContext {
  public:
    Group_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_PAREN();
    PatternContext *pattern();
    antlr4::tree::TerminalNode *CLOSE_PAREN();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Group_patternContext* group_pattern();

  class  Sequence_patternContext : public antlr4::ParserRuleContext {
  public:
    Sequence_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACK();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    Maybe_sequence_patternContext *maybe_sequence_pattern();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Open_sequence_patternContext *open_sequence_pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Sequence_patternContext* sequence_pattern();

  class  Open_sequence_patternContext : public antlr4::ParserRuleContext {
  public:
    Open_sequence_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Maybe_star_patternContext *maybe_star_pattern();
    antlr4::tree::TerminalNode *COMMA();
    Maybe_sequence_patternContext *maybe_sequence_pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Open_sequence_patternContext* open_sequence_pattern();

  class  Maybe_sequence_patternContext : public antlr4::ParserRuleContext {
  public:
    Maybe_sequence_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Maybe_star_patternContext *> maybe_star_pattern();
    Maybe_star_patternContext* maybe_star_pattern(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Maybe_sequence_patternContext* maybe_sequence_pattern();

  class  Maybe_star_patternContext : public antlr4::ParserRuleContext {
  public:
    Maybe_star_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Star_patternContext *star_pattern();
    PatternContext *pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Maybe_star_patternContext* maybe_star_pattern();

  class  Star_patternContext : public antlr4::ParserRuleContext {
  public:
    Star_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    Pattern_capture_targetContext *pattern_capture_target();
    Wildcard_patternContext *wildcard_pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_patternContext* star_pattern();

  class  Mapping_patternContext : public antlr4::ParserRuleContext {
  public:
    Mapping_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACE();
    antlr4::tree::TerminalNode *CLOSE_BRACE();
    Double_star_patternContext *double_star_pattern();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    Items_patternContext *items_pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Mapping_patternContext* mapping_pattern();

  class  Items_patternContext : public antlr4::ParserRuleContext {
  public:
    Items_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Key_value_patternContext *> key_value_pattern();
    Key_value_patternContext* key_value_pattern(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Items_patternContext* items_pattern();

  class  Key_value_patternContext : public antlr4::ParserRuleContext {
  public:
    Key_value_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *COLON();
    PatternContext *pattern();
    Literal_exprContext *literal_expr();
    AttrContext *attr();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Key_value_patternContext* key_value_pattern();

  class  Double_star_patternContext : public antlr4::ParserRuleContext {
  public:
    Double_star_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *POWER();
    Pattern_capture_targetContext *pattern_capture_target();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Double_star_patternContext* double_star_pattern();

  class  Class_patternContext : public antlr4::ParserRuleContext {
  public:
    Class_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Name_or_attrContext *name_or_attr();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Positional_patternsContext *positional_patterns();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    Keyword_patternsContext *keyword_patterns();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Class_patternContext* class_pattern();

  class  Positional_patternsContext : public antlr4::ParserRuleContext {
  public:
    Positional_patternsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<PatternContext *> pattern();
    PatternContext* pattern(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Positional_patternsContext* positional_patterns();

  class  Keyword_patternsContext : public antlr4::ParserRuleContext {
  public:
    Keyword_patternsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Keyword_patternContext *> keyword_pattern();
    Keyword_patternContext* keyword_pattern(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Keyword_patternsContext* keyword_patterns();

  class  Keyword_patternContext : public antlr4::ParserRuleContext {
  public:
    Keyword_patternContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *ASSIGN();
    PatternContext *pattern();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Keyword_patternContext* keyword_pattern();

  class  Type_aliasContext : public antlr4::ParserRuleContext {
  public:
    Type_aliasContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *TYPE();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *ASSIGN();
    ExpressionContext *expression();
    Type_paramsContext *type_params();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_aliasContext* type_alias();

  class  Type_paramsContext : public antlr4::ParserRuleContext {
  public:
    Type_paramsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACK();
    Type_param_seqContext *type_param_seq();
    antlr4::tree::TerminalNode *CLOSE_BRACK();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_paramsContext* type_params();

  class  Type_param_seqContext : public antlr4::ParserRuleContext {
  public:
    Type_param_seqContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Type_paramContext *> type_param();
    Type_paramContext* type_param(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_param_seqContext* type_param_seq();

  class  Type_paramContext : public antlr4::ParserRuleContext {
  public:
    Type_paramContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    Type_param_boundContext *type_param_bound();
    antlr4::tree::TerminalNode *STAR();
    antlr4::tree::TerminalNode *POWER();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_paramContext* type_param();

  class  Type_param_boundContext : public antlr4::ParserRuleContext {
  public:
    Type_param_boundContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_param_boundContext* type_param_bound();

  class  ExpressionsContext : public antlr4::ParserRuleContext {
  public:
    ExpressionsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExpressionsContext* expressions();

  class  ExpressionContext : public antlr4::ParserRuleContext {
  public:
    ExpressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<DisjunctionContext *> disjunction();
    DisjunctionContext* disjunction(size_t i);
    antlr4::tree::TerminalNode *IF();
    antlr4::tree::TerminalNode *ELSE();
    ExpressionContext *expression();
    LambdefContext *lambdef();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExpressionContext* expression();

  class  Yield_exprContext : public antlr4::ParserRuleContext {
  public:
    Yield_exprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *YIELD();
    antlr4::tree::TerminalNode *FROM();
    ExpressionContext *expression();
    Star_expressionsContext *star_expressions();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Yield_exprContext* yield_expr();

  class  Star_expressionsContext : public antlr4::ParserRuleContext {
  public:
    Star_expressionsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Star_expressionContext *> star_expression();
    Star_expressionContext* star_expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_expressionsContext* star_expressions();

  class  Star_expressionContext : public antlr4::ParserRuleContext {
  public:
    Star_expressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Star_selectionContext *star_selection();
    antlr4::tree::TerminalNode *STAR();
    Bitwise_orContext *bitwise_or();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_expressionContext* star_expression();

  class  Star_named_expressionsContext : public antlr4::ParserRuleContext {
  public:
    Star_named_expressionsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Star_named_expressionContext *> star_named_expression();
    Star_named_expressionContext* star_named_expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_named_expressionsContext* star_named_expressions();

  class  Star_named_expressionContext : public antlr4::ParserRuleContext {
  public:
    Star_named_expressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    Bitwise_orContext *bitwise_or();
    Named_expressionContext *named_expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_named_expressionContext* star_named_expression();

  class  Assignment_expressionContext : public antlr4::ParserRuleContext {
  public:
    Assignment_expressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *EXPR_ASSIGN();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Assignment_expressionContext* assignment_expression();

  class  Named_expressionContext : public antlr4::ParserRuleContext {
  public:
    Named_expressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Assignment_expressionContext *assignment_expression();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Named_expressionContext* named_expression();

  class  DisjunctionContext : public antlr4::ParserRuleContext {
  public:
    DisjunctionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ConjunctionContext *> conjunction();
    ConjunctionContext* conjunction(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR();
    antlr4::tree::TerminalNode* OR(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DisjunctionContext* disjunction();

  class  ConjunctionContext : public antlr4::ParserRuleContext {
  public:
    ConjunctionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<InversionContext *> inversion();
    InversionContext* inversion(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AND();
    antlr4::tree::TerminalNode* AND(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConjunctionContext* conjunction();

  class  InversionContext : public antlr4::ParserRuleContext {
  public:
    InversionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NOT();
    InversionContext *inversion();
    ComparisonContext *comparison();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  InversionContext* inversion();

  class  ComparisonContext : public antlr4::ParserRuleContext {
  public:
    ComparisonContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Bitwise_orContext *bitwise_or();
    std::vector<Compare_op_bitwise_or_pairContext *> compare_op_bitwise_or_pair();
    Compare_op_bitwise_or_pairContext* compare_op_bitwise_or_pair(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ComparisonContext* comparison();

  class  Compare_op_bitwise_or_pairContext : public antlr4::ParserRuleContext {
  public:
    Compare_op_bitwise_or_pairContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Eq_bitwise_orContext *eq_bitwise_or();
    Noteq_bitwise_orContext *noteq_bitwise_or();
    Lte_bitwise_orContext *lte_bitwise_or();
    Lt_bitwise_orContext *lt_bitwise_or();
    Gte_bitwise_orContext *gte_bitwise_or();
    Gt_bitwise_orContext *gt_bitwise_or();
    Notin_bitwise_orContext *notin_bitwise_or();
    In_bitwise_orContext *in_bitwise_or();
    Isnot_bitwise_orContext *isnot_bitwise_or();
    Is_bitwise_orContext *is_bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Compare_op_bitwise_or_pairContext* compare_op_bitwise_or_pair();

  class  Eq_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Eq_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EQUALS();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Eq_bitwise_orContext* eq_bitwise_or();

  class  Noteq_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Noteq_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NOT_EQ_2();
    Bitwise_orContext *bitwise_or();
    antlr4::tree::TerminalNode *NOT_EQ_1();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Noteq_bitwise_orContext* noteq_bitwise_or();

  class  Lte_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Lte_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LT_EQ();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lte_bitwise_orContext* lte_bitwise_or();

  class  Lt_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Lt_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LESS_THAN();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lt_bitwise_orContext* lt_bitwise_or();

  class  Gte_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Gte_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *GT_EQ();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Gte_bitwise_orContext* gte_bitwise_or();

  class  Gt_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Gt_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *GREATER_THAN();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Gt_bitwise_orContext* gt_bitwise_or();

  class  Notin_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Notin_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NOT();
    antlr4::tree::TerminalNode *IN();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Notin_bitwise_orContext* notin_bitwise_or();

  class  In_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    In_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IN();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  In_bitwise_orContext* in_bitwise_or();

  class  Isnot_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Isnot_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IS();
    antlr4::tree::TerminalNode *NOT();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Isnot_bitwise_orContext* isnot_bitwise_or();

  class  Is_bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Is_bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IS();
    Bitwise_orContext *bitwise_or();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Is_bitwise_orContext* is_bitwise_or();

  class  Bitwise_orContext : public antlr4::ParserRuleContext {
  public:
    Bitwise_orContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Bitwise_xorContext *bitwise_xor();
    Bitwise_orContext *bitwise_or();
    antlr4::tree::TerminalNode *OR_OP();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Bitwise_orContext* bitwise_or();
  Bitwise_orContext* bitwise_or(int precedence);
  class  Bitwise_xorContext : public antlr4::ParserRuleContext {
  public:
    Bitwise_xorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Bitwise_andContext *bitwise_and();
    Bitwise_xorContext *bitwise_xor();
    antlr4::tree::TerminalNode *XOR();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Bitwise_xorContext* bitwise_xor();
  Bitwise_xorContext* bitwise_xor(int precedence);
  class  Bitwise_andContext : public antlr4::ParserRuleContext {
  public:
    Bitwise_andContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Shift_exprContext *shift_expr();
    Bitwise_andContext *bitwise_and();
    antlr4::tree::TerminalNode *AND_OP();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Bitwise_andContext* bitwise_and();
  Bitwise_andContext* bitwise_and(int precedence);
  class  Shift_exprContext : public antlr4::ParserRuleContext {
  public:
    Shift_exprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    SumContext *sum();
    Shift_exprContext *shift_expr();
    antlr4::tree::TerminalNode *LEFT_SHIFT();
    antlr4::tree::TerminalNode *RIGHT_SHIFT();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Shift_exprContext* shift_expr();
  Shift_exprContext* shift_expr(int precedence);
  class  SumContext : public antlr4::ParserRuleContext {
  public:
    SumContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    TermContext *term();
    SumContext *sum();
    antlr4::tree::TerminalNode *ADD();
    antlr4::tree::TerminalNode *MINUS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SumContext* sum();
  SumContext* sum(int precedence);
  class  TermContext : public antlr4::ParserRuleContext {
  public:
    TermContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    FactorContext *factor();
    TermContext *term();
    antlr4::tree::TerminalNode *STAR();
    antlr4::tree::TerminalNode *DIV();
    antlr4::tree::TerminalNode *IDIV();
    antlr4::tree::TerminalNode *MOD();
    antlr4::tree::TerminalNode *AT();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TermContext* term();
  TermContext* term(int precedence);
  class  FactorContext : public antlr4::ParserRuleContext {
  public:
    FactorContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ADD();
    FactorContext *factor();
    antlr4::tree::TerminalNode *MINUS();
    antlr4::tree::TerminalNode *NOT_OP();
    PowerContext *power();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FactorContext* factor();

  class  PowerContext : public antlr4::ParserRuleContext {
  public:
    PowerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Await_primaryContext *await_primary();
    antlr4::tree::TerminalNode *POWER();
    FactorContext *factor();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PowerContext* power();

  class  Await_primaryContext : public antlr4::ParserRuleContext {
  public:
    Await_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *AWAIT();
    PrimaryContext *primary();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Await_primaryContext* await_primary();

  class  PrimaryContext : public antlr4::ParserRuleContext {
  public:
    PrimaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AtomContext *atom();
    PrimaryContext *primary();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    GenexpContext *genexp();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    ArgumentsContext *arguments();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    SlicesContext *slices();
    antlr4::tree::TerminalNode *CLOSE_BRACK();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PrimaryContext* primary();
  PrimaryContext* primary(int precedence);
  class  SlicesContext : public antlr4::ParserRuleContext {
  public:
    SlicesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<SliceContext *> slice();
    SliceContext* slice(size_t i);
    std::vector<Starred_expressionContext *> starred_expression();
    Starred_expressionContext* starred_expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SlicesContext* slices();

  class  SliceContext : public antlr4::ParserRuleContext {
  public:
    SliceContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> COLON();
    antlr4::tree::TerminalNode* COLON(size_t i);
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    Named_expressionContext *named_expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SliceContext* slice();

  class  AtomContext : public antlr4::ParserRuleContext {
  public:
    AtomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Selector_lengthContext *selector_length();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *TRUE();
    antlr4::tree::TerminalNode *FALSE();
    antlr4::tree::TerminalNode *NONE();
    StringsContext *strings();
    antlr4::tree::TerminalNode *NUMBER();
    TupleContext *tuple();
    GroupContext *group();
    GenexpContext *genexp();
    ListContext *list();
    ListcompContext *listcomp();
    DictContext *dict();
    SetContext *set();
    DictcompContext *dictcomp();
    SetcompContext *setcomp();
    antlr4::tree::TerminalNode *ELLIPSIS();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AtomContext* atom();

  class  GroupContext : public antlr4::ParserRuleContext {
  public:
    GroupContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Yield_exprContext *yield_expr();
    Named_expressionContext *named_expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  GroupContext* group();

  class  LambdefContext : public antlr4::ParserRuleContext {
  public:
    LambdefContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LAMBDA();
    antlr4::tree::TerminalNode *COLON();
    ExpressionContext *expression();
    Lambda_paramsContext *lambda_params();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LambdefContext* lambdef();

  class  Lambda_paramsContext : public antlr4::ParserRuleContext {
  public:
    Lambda_paramsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Lambda_parametersContext *lambda_parameters();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_paramsContext* lambda_params();

  class  Lambda_parametersContext : public antlr4::ParserRuleContext {
  public:
    Lambda_parametersContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Lambda_slash_no_defaultContext *lambda_slash_no_default();
    std::vector<Lambda_param_no_defaultContext *> lambda_param_no_default();
    Lambda_param_no_defaultContext* lambda_param_no_default(size_t i);
    std::vector<Lambda_param_with_defaultContext *> lambda_param_with_default();
    Lambda_param_with_defaultContext* lambda_param_with_default(size_t i);
    Lambda_star_etcContext *lambda_star_etc();
    Lambda_slash_with_defaultContext *lambda_slash_with_default();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_parametersContext* lambda_parameters();

  class  Lambda_slash_no_defaultContext : public antlr4::ParserRuleContext {
  public:
    Lambda_slash_no_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DIV();
    std::vector<Lambda_param_no_defaultContext *> lambda_param_no_default();
    Lambda_param_no_defaultContext* lambda_param_no_default(size_t i);
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_slash_no_defaultContext* lambda_slash_no_default();

  class  Lambda_slash_with_defaultContext : public antlr4::ParserRuleContext {
  public:
    Lambda_slash_with_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DIV();
    std::vector<Lambda_param_no_defaultContext *> lambda_param_no_default();
    Lambda_param_no_defaultContext* lambda_param_no_default(size_t i);
    std::vector<Lambda_param_with_defaultContext *> lambda_param_with_default();
    Lambda_param_with_defaultContext* lambda_param_with_default(size_t i);
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_slash_with_defaultContext* lambda_slash_with_default();

  class  Lambda_star_etcContext : public antlr4::ParserRuleContext {
  public:
    Lambda_star_etcContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    Lambda_param_no_defaultContext *lambda_param_no_default();
    std::vector<Lambda_param_maybe_defaultContext *> lambda_param_maybe_default();
    Lambda_param_maybe_defaultContext* lambda_param_maybe_default(size_t i);
    Lambda_kwdsContext *lambda_kwds();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_star_etcContext* lambda_star_etc();

  class  Lambda_kwdsContext : public antlr4::ParserRuleContext {
  public:
    Lambda_kwdsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *POWER();
    Lambda_param_no_defaultContext *lambda_param_no_default();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_kwdsContext* lambda_kwds();

  class  Lambda_param_no_defaultContext : public antlr4::ParserRuleContext {
  public:
    Lambda_param_no_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Lambda_paramContext *lambda_param();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_param_no_defaultContext* lambda_param_no_default();

  class  Lambda_param_with_defaultContext : public antlr4::ParserRuleContext {
  public:
    Lambda_param_with_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Lambda_paramContext *lambda_param();
    DefaultContext *default_();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_param_with_defaultContext* lambda_param_with_default();

  class  Lambda_param_maybe_defaultContext : public antlr4::ParserRuleContext {
  public:
    Lambda_param_maybe_defaultContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Lambda_paramContext *lambda_param();
    DefaultContext *default_();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_param_maybe_defaultContext* lambda_param_maybe_default();

  class  Lambda_paramContext : public antlr4::ParserRuleContext {
  public:
    Lambda_paramContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Lambda_paramContext* lambda_param();

  class  Fstring_middle_no_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_middle_no_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_replacement_fieldContext *fstring_replacement_field();
    Fstring_any_no_quoteContext *fstring_any_no_quote();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_middle_no_quoteContext* fstring_middle_no_quote();

  class  Fstring_middle_no_single_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_middle_no_single_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_replacement_fieldContext *fstring_replacement_field();
    Fstring_any_no_single_quoteContext *fstring_any_no_single_quote();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_middle_no_single_quoteContext* fstring_middle_no_single_quote();

  class  Fstring_middle_breaks_no_triple_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_middle_breaks_no_triple_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_replacement_fieldContext *fstring_replacement_field();
    Fstring_any_breaks_no_triple_quoteContext *fstring_any_breaks_no_triple_quote();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_middle_breaks_no_triple_quoteContext* fstring_middle_breaks_no_triple_quote();

  class  Fstring_middle_breaks_no_triple_single_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_middle_breaks_no_triple_single_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_replacement_fieldContext *fstring_replacement_field();
    Fstring_any_breaks_no_triple_single_quoteContext *fstring_any_breaks_no_triple_single_quote();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_middle_breaks_no_triple_single_quoteContext* fstring_middle_breaks_no_triple_single_quote();

  class  Fstring_any_no_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_any_no_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_anyContext *fstring_any();
    antlr4::tree::TerminalNode *FSTRING_END_SINGLE_QUOTE();
    antlr4::tree::TerminalNode *FSTRING_END_TRIPLE_SINGLE_QUOTE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_any_no_quoteContext* fstring_any_no_quote();

  class  Fstring_any_no_single_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_any_no_single_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_anyContext *fstring_any();
    antlr4::tree::TerminalNode *FSTRING_END_QUOTE();
    antlr4::tree::TerminalNode *FSTRING_END_TRIPLE_QUOTE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_any_no_single_quoteContext* fstring_any_no_single_quote();

  class  Fstring_middleContext : public antlr4::ParserRuleContext {
  public:
    Fstring_middleContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_anyContext *fstring_any();
    antlr4::tree::TerminalNode *FSTRING_END_SINGLE_QUOTE();
    antlr4::tree::TerminalNode *FSTRING_END_QUOTE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_middleContext* fstring_middle();

  class  Fstring_any_breaks_no_triple_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_any_breaks_no_triple_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_anyContext *fstring_any();
    antlr4::tree::TerminalNode *NEWLINE();
    antlr4::tree::TerminalNode *FSTRING_END_SINGLE_QUOTE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_any_breaks_no_triple_quoteContext* fstring_any_breaks_no_triple_quote();

  class  Fstring_any_breaks_no_triple_single_quoteContext : public antlr4::ParserRuleContext {
  public:
    Fstring_any_breaks_no_triple_single_quoteContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_anyContext *fstring_any();
    antlr4::tree::TerminalNode *NEWLINE();
    antlr4::tree::TerminalNode *FSTRING_END_QUOTE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_any_breaks_no_triple_single_quoteContext* fstring_any_breaks_no_triple_single_quote();

  class  Fstring_anyContext : public antlr4::ParserRuleContext {
  public:
    Fstring_anyContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> NUMBER();
    antlr4::tree::TerminalNode* NUMBER(size_t i);
    std::vector<antlr4::tree::TerminalNode *> PYTHON_START();
    antlr4::tree::TerminalNode* PYTHON_START(size_t i);
    std::vector<antlr4::tree::TerminalNode *> PYTHON_END();
    antlr4::tree::TerminalNode* PYTHON_END(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AND();
    antlr4::tree::TerminalNode* AND(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AS();
    antlr4::tree::TerminalNode* AS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ASSERT();
    antlr4::tree::TerminalNode* ASSERT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ASYNC();
    antlr4::tree::TerminalNode* ASYNC(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AWAIT();
    antlr4::tree::TerminalNode* AWAIT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> BREAK();
    antlr4::tree::TerminalNode* BREAK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> CASE();
    antlr4::tree::TerminalNode* CASE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> CLASS();
    antlr4::tree::TerminalNode* CLASS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> CONTINUE();
    antlr4::tree::TerminalNode* CONTINUE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DEF();
    antlr4::tree::TerminalNode* DEF(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DEL();
    antlr4::tree::TerminalNode* DEL(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ELIF();
    antlr4::tree::TerminalNode* ELIF(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ELSE();
    antlr4::tree::TerminalNode* ELSE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> EXCEPT();
    antlr4::tree::TerminalNode* EXCEPT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> FALSE();
    antlr4::tree::TerminalNode* FALSE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> FINALLY();
    antlr4::tree::TerminalNode* FINALLY(size_t i);
    std::vector<antlr4::tree::TerminalNode *> FOR();
    antlr4::tree::TerminalNode* FOR(size_t i);
    std::vector<antlr4::tree::TerminalNode *> FROM();
    antlr4::tree::TerminalNode* FROM(size_t i);
    std::vector<antlr4::tree::TerminalNode *> GLOBAL();
    antlr4::tree::TerminalNode* GLOBAL(size_t i);
    std::vector<antlr4::tree::TerminalNode *> IF();
    antlr4::tree::TerminalNode* IF(size_t i);
    std::vector<antlr4::tree::TerminalNode *> IMPORT();
    antlr4::tree::TerminalNode* IMPORT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> IN();
    antlr4::tree::TerminalNode* IN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> IS();
    antlr4::tree::TerminalNode* IS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LAMBDA();
    antlr4::tree::TerminalNode* LAMBDA(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MATCH();
    antlr4::tree::TerminalNode* MATCH(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NONE();
    antlr4::tree::TerminalNode* NONE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NONLOCAL();
    antlr4::tree::TerminalNode* NONLOCAL(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NOT();
    antlr4::tree::TerminalNode* NOT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR();
    antlr4::tree::TerminalNode* OR(size_t i);
    std::vector<antlr4::tree::TerminalNode *> PASS();
    antlr4::tree::TerminalNode* PASS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RAISE();
    antlr4::tree::TerminalNode* RAISE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RETURN();
    antlr4::tree::TerminalNode* RETURN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> TRUE();
    antlr4::tree::TerminalNode* TRUE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> TRY();
    antlr4::tree::TerminalNode* TRY(size_t i);
    std::vector<antlr4::tree::TerminalNode *> TYPE();
    antlr4::tree::TerminalNode* TYPE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> WHILE();
    antlr4::tree::TerminalNode* WHILE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> WHERE();
    antlr4::tree::TerminalNode* WHERE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> WITH();
    antlr4::tree::TerminalNode* WITH(size_t i);
    std::vector<antlr4::tree::TerminalNode *> YIELD();
    antlr4::tree::TerminalNode* YIELD(size_t i);
    std::vector<antlr4::tree::TerminalNode *> FORALL();
    antlr4::tree::TerminalNode* FORALL(size_t i);
    std::vector<antlr4::tree::TerminalNode *> EXISTS();
    antlr4::tree::TerminalNode* EXISTS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MAXIMIZING();
    antlr4::tree::TerminalNode* MAXIMIZING(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MINIMIZING();
    antlr4::tree::TerminalNode* MINIMIZING(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ANY();
    antlr4::tree::TerminalNode* ANY(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ALL();
    antlr4::tree::TerminalNode* ALL(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LEN();
    antlr4::tree::TerminalNode* LEN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NAME();
    antlr4::tree::TerminalNode* NAME(size_t i);
    std::vector<antlr4::tree::TerminalNode *> GRAMMAR_ASSIGN();
    antlr4::tree::TerminalNode* GRAMMAR_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> QUESTION();
    antlr4::tree::TerminalNode* QUESTION(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOT();
    antlr4::tree::TerminalNode* DOT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DOTDOT();
    antlr4::tree::TerminalNode* DOTDOT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ELLIPSIS();
    antlr4::tree::TerminalNode* ELLIPSIS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> STAR();
    antlr4::tree::TerminalNode* STAR(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OPEN_PAREN();
    antlr4::tree::TerminalNode* OPEN_PAREN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> CLOSE_PAREN();
    antlr4::tree::TerminalNode* CLOSE_PAREN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COLON();
    antlr4::tree::TerminalNode* COLON(size_t i);
    std::vector<antlr4::tree::TerminalNode *> SEMI_COLON();
    antlr4::tree::TerminalNode* SEMI_COLON(size_t i);
    std::vector<antlr4::tree::TerminalNode *> POWER();
    antlr4::tree::TerminalNode* POWER(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ASSIGN();
    antlr4::tree::TerminalNode* ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OPEN_BRACK();
    antlr4::tree::TerminalNode* OPEN_BRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> CLOSE_BRACK();
    antlr4::tree::TerminalNode* CLOSE_BRACK(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR_OP();
    antlr4::tree::TerminalNode* OR_OP(size_t i);
    std::vector<antlr4::tree::TerminalNode *> XOR();
    antlr4::tree::TerminalNode* XOR(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AND_OP();
    antlr4::tree::TerminalNode* AND_OP(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LEFT_SHIFT();
    antlr4::tree::TerminalNode* LEFT_SHIFT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RIGHT_SHIFT();
    antlr4::tree::TerminalNode* RIGHT_SHIFT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ADD();
    antlr4::tree::TerminalNode* ADD(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MINUS();
    antlr4::tree::TerminalNode* MINUS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DIV();
    antlr4::tree::TerminalNode* DIV(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MOD();
    antlr4::tree::TerminalNode* MOD(size_t i);
    std::vector<antlr4::tree::TerminalNode *> IDIV();
    antlr4::tree::TerminalNode* IDIV(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NOT_OP();
    antlr4::tree::TerminalNode* NOT_OP(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OPEN_BRACE();
    antlr4::tree::TerminalNode* OPEN_BRACE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> CLOSE_BRACE();
    antlr4::tree::TerminalNode* CLOSE_BRACE(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LESS_THAN();
    antlr4::tree::TerminalNode* LESS_THAN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> GREATER_THAN();
    antlr4::tree::TerminalNode* GREATER_THAN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> EQUALS();
    antlr4::tree::TerminalNode* EQUALS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> GT_EQ();
    antlr4::tree::TerminalNode* GT_EQ(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LT_EQ();
    antlr4::tree::TerminalNode* LT_EQ(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NOT_EQ_1();
    antlr4::tree::TerminalNode* NOT_EQ_1(size_t i);
    std::vector<antlr4::tree::TerminalNode *> NOT_EQ_2();
    antlr4::tree::TerminalNode* NOT_EQ_2(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AT();
    antlr4::tree::TerminalNode* AT(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ARROW();
    antlr4::tree::TerminalNode* ARROW(size_t i);
    std::vector<antlr4::tree::TerminalNode *> ADD_ASSIGN();
    antlr4::tree::TerminalNode* ADD_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> SUB_ASSIGN();
    antlr4::tree::TerminalNode* SUB_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MULT_ASSIGN();
    antlr4::tree::TerminalNode* MULT_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AT_ASSIGN();
    antlr4::tree::TerminalNode* AT_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> DIV_ASSIGN();
    antlr4::tree::TerminalNode* DIV_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MOD_ASSIGN();
    antlr4::tree::TerminalNode* MOD_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AND_ASSIGN();
    antlr4::tree::TerminalNode* AND_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR_ASSIGN();
    antlr4::tree::TerminalNode* OR_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> XOR_ASSIGN();
    antlr4::tree::TerminalNode* XOR_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> LEFT_SHIFT_ASSIGN();
    antlr4::tree::TerminalNode* LEFT_SHIFT_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> RIGHT_SHIFT_ASSIGN();
    antlr4::tree::TerminalNode* RIGHT_SHIFT_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> POWER_ASSIGN();
    antlr4::tree::TerminalNode* POWER_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> IDIV_ASSIGN();
    antlr4::tree::TerminalNode* IDIV_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> EXPR_ASSIGN();
    antlr4::tree::TerminalNode* EXPR_ASSIGN(size_t i);
    std::vector<antlr4::tree::TerminalNode *> EXCL();
    antlr4::tree::TerminalNode* EXCL(size_t i);
    std::vector<antlr4::tree::TerminalNode *> SKIP_();
    antlr4::tree::TerminalNode* SKIP_(size_t i);
    std::vector<antlr4::tree::TerminalNode *> UNKNOWN_CHAR();
    antlr4::tree::TerminalNode* UNKNOWN_CHAR(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_anyContext* fstring_any();

  class  Fstring_replacement_fieldContext : public antlr4::ParserRuleContext {
  public:
    Fstring_replacement_fieldContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACE();
    antlr4::tree::TerminalNode *CLOSE_BRACE();
    Yield_exprContext *yield_expr();
    Star_expressionsContext *star_expressions();
    antlr4::tree::TerminalNode *ASSIGN();
    Fstring_conversionContext *fstring_conversion();
    Fstring_full_format_specContext *fstring_full_format_spec();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_replacement_fieldContext* fstring_replacement_field();

  class  Fstring_conversionContext : public antlr4::ParserRuleContext {
  public:
    Fstring_conversionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EXCL();
    IdentifierContext *identifier();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_conversionContext* fstring_conversion();

  class  Fstring_full_format_specContext : public antlr4::ParserRuleContext {
  public:
    Fstring_full_format_specContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *COLON();
    std::vector<Fstring_format_specContext *> fstring_format_spec();
    Fstring_format_specContext* fstring_format_spec(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_full_format_specContext* fstring_full_format_spec();

  class  Fstring_format_specContext : public antlr4::ParserRuleContext {
  public:
    Fstring_format_specContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Fstring_replacement_fieldContext *fstring_replacement_field();
    Fstring_middleContext *fstring_middle();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Fstring_format_specContext* fstring_format_spec();

  class  FstringContext : public antlr4::ParserRuleContext {
  public:
    FstringContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FSTRING_START_QUOTE();
    antlr4::tree::TerminalNode *FSTRING_END_QUOTE();
    std::vector<Fstring_middle_no_quoteContext *> fstring_middle_no_quote();
    Fstring_middle_no_quoteContext* fstring_middle_no_quote(size_t i);
    antlr4::tree::TerminalNode *FSTRING_START_SINGLE_QUOTE();
    antlr4::tree::TerminalNode *FSTRING_END_SINGLE_QUOTE();
    std::vector<Fstring_middle_no_single_quoteContext *> fstring_middle_no_single_quote();
    Fstring_middle_no_single_quoteContext* fstring_middle_no_single_quote(size_t i);
    antlr4::tree::TerminalNode *FSTRING_START_TRIPLE_QUOTE();
    antlr4::tree::TerminalNode *FSTRING_END_TRIPLE_QUOTE();
    std::vector<Fstring_middle_breaks_no_triple_quoteContext *> fstring_middle_breaks_no_triple_quote();
    Fstring_middle_breaks_no_triple_quoteContext* fstring_middle_breaks_no_triple_quote(size_t i);
    antlr4::tree::TerminalNode *FSTRING_START_TRIPLE_SINGLE_QUOTE();
    antlr4::tree::TerminalNode *FSTRING_END_TRIPLE_SINGLE_QUOTE();
    std::vector<Fstring_middle_breaks_no_triple_single_quoteContext *> fstring_middle_breaks_no_triple_single_quote();
    Fstring_middle_breaks_no_triple_single_quoteContext* fstring_middle_breaks_no_triple_single_quote(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FstringContext* fstring();

  class  StringContext : public antlr4::ParserRuleContext {
  public:
    StringContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STRING();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StringContext* string();

  class  StringsContext : public antlr4::ParserRuleContext {
  public:
    StringsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<FstringContext *> fstring();
    FstringContext* fstring(size_t i);
    std::vector<StringContext *> string();
    StringContext* string(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StringsContext* strings();

  class  ListContext : public antlr4::ParserRuleContext {
  public:
    ListContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACK();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    Star_named_expressionsContext *star_named_expressions();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ListContext* list();

  class  TupleContext : public antlr4::ParserRuleContext {
  public:
    TupleContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Star_named_expressionContext *star_named_expression();
    antlr4::tree::TerminalNode *COMMA();
    Star_named_expressionsContext *star_named_expressions();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TupleContext* tuple();

  class  SetContext : public antlr4::ParserRuleContext {
  public:
    SetContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACE();
    Star_named_expressionsContext *star_named_expressions();
    antlr4::tree::TerminalNode *CLOSE_BRACE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SetContext* set();

  class  DictContext : public antlr4::ParserRuleContext {
  public:
    DictContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACE();
    antlr4::tree::TerminalNode *CLOSE_BRACE();
    Double_starred_kvpairsContext *double_starred_kvpairs();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DictContext* dict();

  class  Double_starred_kvpairsContext : public antlr4::ParserRuleContext {
  public:
    Double_starred_kvpairsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Double_starred_kvpairContext *> double_starred_kvpair();
    Double_starred_kvpairContext* double_starred_kvpair(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Double_starred_kvpairsContext* double_starred_kvpairs();

  class  Double_starred_kvpairContext : public antlr4::ParserRuleContext {
  public:
    Double_starred_kvpairContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *POWER();
    Bitwise_orContext *bitwise_or();
    KvpairContext *kvpair();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Double_starred_kvpairContext* double_starred_kvpair();

  class  KvpairContext : public antlr4::ParserRuleContext {
  public:
    KvpairContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    antlr4::tree::TerminalNode *COLON();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  KvpairContext* kvpair();

  class  For_if_clausesContext : public antlr4::ParserRuleContext {
  public:
    For_if_clausesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<For_if_clauseContext *> for_if_clause();
    For_if_clauseContext* for_if_clause(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  For_if_clausesContext* for_if_clauses();

  class  For_if_clauseContext : public antlr4::ParserRuleContext {
  public:
    For_if_clauseContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *FOR();
    Star_targetsContext *star_targets();
    antlr4::tree::TerminalNode *IN();
    std::vector<DisjunctionContext *> disjunction();
    DisjunctionContext* disjunction(size_t i);
    antlr4::tree::TerminalNode *ASYNC();
    std::vector<antlr4::tree::TerminalNode *> IF();
    antlr4::tree::TerminalNode* IF(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  For_if_clauseContext* for_if_clause();

  class  ListcompContext : public antlr4::ParserRuleContext {
  public:
    ListcompContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACK();
    Named_expressionContext *named_expression();
    For_if_clausesContext *for_if_clauses();
    antlr4::tree::TerminalNode *CLOSE_BRACK();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ListcompContext* listcomp();

  class  SetcompContext : public antlr4::ParserRuleContext {
  public:
    SetcompContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACE();
    Named_expressionContext *named_expression();
    For_if_clausesContext *for_if_clauses();
    antlr4::tree::TerminalNode *CLOSE_BRACE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  SetcompContext* setcomp();

  class  GenexpContext : public antlr4::ParserRuleContext {
  public:
    GenexpContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_PAREN();
    For_if_clausesContext *for_if_clauses();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Assignment_expressionContext *assignment_expression();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  GenexpContext* genexp();

  class  DictcompContext : public antlr4::ParserRuleContext {
  public:
    DictcompContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OPEN_BRACE();
    KvpairContext *kvpair();
    For_if_clausesContext *for_if_clauses();
    antlr4::tree::TerminalNode *CLOSE_BRACE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DictcompContext* dictcomp();

  class  ArgumentsContext : public antlr4::ParserRuleContext {
  public:
    ArgumentsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ArgsContext *args();
    antlr4::tree::TerminalNode *COMMA();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArgumentsContext* arguments();

  class  ArgsContext : public antlr4::ParserRuleContext {
  public:
    ArgsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ArgContext *> arg();
    ArgContext* arg(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    KwargsContext *kwargs();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArgsContext* args();

  class  ArgContext : public antlr4::ParserRuleContext {
  public:
    ArgContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Star_selectionContext *star_selection();
    Starred_expressionContext *starred_expression();
    Assignment_expressionContext *assignment_expression();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArgContext* arg();

  class  KwargsContext : public antlr4::ParserRuleContext {
  public:
    KwargsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Kwarg_or_starredContext *> kwarg_or_starred();
    Kwarg_or_starredContext* kwarg_or_starred(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    std::vector<Kwarg_or_double_starredContext *> kwarg_or_double_starred();
    Kwarg_or_double_starredContext* kwarg_or_double_starred(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  KwargsContext* kwargs();

  class  Starred_expressionContext : public antlr4::ParserRuleContext {
  public:
    Starred_expressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    ExpressionContext *expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Starred_expressionContext* starred_expression();

  class  Kwarg_or_starredContext : public antlr4::ParserRuleContext {
  public:
    Kwarg_or_starredContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *ASSIGN();
    ExpressionContext *expression();
    Starred_expressionContext *starred_expression();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Kwarg_or_starredContext* kwarg_or_starred();

  class  Kwarg_or_double_starredContext : public antlr4::ParserRuleContext {
  public:
    Kwarg_or_double_starredContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *ASSIGN();
    ExpressionContext *expression();
    antlr4::tree::TerminalNode *POWER();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Kwarg_or_double_starredContext* kwarg_or_double_starred();

  class  Star_targetsContext : public antlr4::ParserRuleContext {
  public:
    Star_targetsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Star_targetContext *> star_target();
    Star_targetContext* star_target(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_targetsContext* star_targets();

  class  Star_targets_list_seqContext : public antlr4::ParserRuleContext {
  public:
    Star_targets_list_seqContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Star_targetContext *> star_target();
    Star_targetContext* star_target(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_targets_list_seqContext* star_targets_list_seq();

  class  Star_targets_tuple_seqContext : public antlr4::ParserRuleContext {
  public:
    Star_targets_tuple_seqContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Star_targetContext *> star_target();
    Star_targetContext* star_target(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_targets_tuple_seqContext* star_targets_tuple_seq();

  class  Star_targetContext : public antlr4::ParserRuleContext {
  public:
    Star_targetContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STAR();
    Star_targetContext *star_target();
    Target_with_star_atomContext *target_with_star_atom();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_targetContext* star_target();

  class  Target_with_star_atomContext : public antlr4::ParserRuleContext {
  public:
    Target_with_star_atomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    T_primaryContext *t_primary();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    SlicesContext *slices();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    Star_atomContext *star_atom();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Target_with_star_atomContext* target_with_star_atom();

  class  Star_atomContext : public antlr4::ParserRuleContext {
  public:
    Star_atomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    Target_with_star_atomContext *target_with_star_atom();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Star_targets_tuple_seqContext *star_targets_tuple_seq();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    Star_targets_list_seqContext *star_targets_list_seq();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Star_atomContext* star_atom();

  class  Single_targetContext : public antlr4::ParserRuleContext {
  public:
    Single_targetContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Single_subscript_attribute_targetContext *single_subscript_attribute_target();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    Single_targetContext *single_target();
    antlr4::tree::TerminalNode *CLOSE_PAREN();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Single_targetContext* single_target();

  class  Single_subscript_attribute_targetContext : public antlr4::ParserRuleContext {
  public:
    Single_subscript_attribute_targetContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    T_primaryContext *t_primary();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    SlicesContext *slices();
    antlr4::tree::TerminalNode *CLOSE_BRACK();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Single_subscript_attribute_targetContext* single_subscript_attribute_target();

  class  T_primaryContext : public antlr4::ParserRuleContext {
  public:
    T_primaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AtomContext *atom();
    T_primaryContext *t_primary();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    SlicesContext *slices();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    GenexpContext *genexp();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    ArgumentsContext *arguments();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  T_primaryContext* t_primary();
  T_primaryContext* t_primary(int precedence);
  class  Del_targetsContext : public antlr4::ParserRuleContext {
  public:
    Del_targetsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Del_targetContext *> del_target();
    Del_targetContext* del_target(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Del_targetsContext* del_targets();

  class  Del_targetContext : public antlr4::ParserRuleContext {
  public:
    Del_targetContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    T_primaryContext *t_primary();
    antlr4::tree::TerminalNode *DOT();
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    SlicesContext *slices();
    antlr4::tree::TerminalNode *CLOSE_BRACK();
    Del_t_atomContext *del_t_atom();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Del_targetContext* del_target();

  class  Del_t_atomContext : public antlr4::ParserRuleContext {
  public:
    Del_t_atomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    IdentifierContext *identifier();
    antlr4::tree::TerminalNode *OPEN_PAREN();
    antlr4::tree::TerminalNode *CLOSE_PAREN();
    Del_targetsContext *del_targets();
    antlr4::tree::TerminalNode *OPEN_BRACK();
    antlr4::tree::TerminalNode *CLOSE_BRACK();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Del_t_atomContext* del_t_atom();

  class  Type_expressionsContext : public antlr4::ParserRuleContext {
  public:
    Type_expressionsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExpressionContext *> expression();
    ExpressionContext* expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    antlr4::tree::TerminalNode *STAR();
    antlr4::tree::TerminalNode *POWER();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Type_expressionsContext* type_expressions();

  class  Func_type_commentContext : public antlr4::ParserRuleContext {
  public:
    Func_type_commentContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NEWLINE();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Func_type_commentContext* func_type_comment();

  class  IdentifierContext : public antlr4::ParserRuleContext {
  public:
    IdentifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NAME();
    antlr4::tree::TerminalNode *ANY();
    antlr4::tree::TerminalNode *ALL();
    antlr4::tree::TerminalNode *LEN();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IdentifierContext* identifier();


  bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;

  bool generator_callSempred(Generator_callContext *_localctx, size_t predicateIndex);
  bool dot_selectionSempred(Dot_selectionContext *_localctx, size_t predicateIndex);
  bool dotted_nameSempred(Dotted_nameContext *_localctx, size_t predicateIndex);
  bool name_or_attrSempred(Name_or_attrContext *_localctx, size_t predicateIndex);
  bool bitwise_orSempred(Bitwise_orContext *_localctx, size_t predicateIndex);
  bool bitwise_xorSempred(Bitwise_xorContext *_localctx, size_t predicateIndex);
  bool bitwise_andSempred(Bitwise_andContext *_localctx, size_t predicateIndex);
  bool shift_exprSempred(Shift_exprContext *_localctx, size_t predicateIndex);
  bool sumSempred(SumContext *_localctx, size_t predicateIndex);
  bool termSempred(TermContext *_localctx, size_t predicateIndex);
  bool primarySempred(PrimaryContext *_localctx, size_t predicateIndex);
  bool t_primarySempred(T_primaryContext *_localctx, size_t predicateIndex);

  // By default the static state used to implement the parser is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:
};

