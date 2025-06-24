
// Generated from language/FandangoParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "FandangoParserVisitor.h"


/**
 * This class provides an empty implementation of FandangoParserVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  FandangoParserBaseVisitor : public FandangoParserVisitor {
public:

  virtual std::any visitFandango(FandangoParser::FandangoContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitProgram(FandangoParser::ProgramContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStatement(FandangoParser::StatementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitProduction(FandangoParser::ProductionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAlternative(FandangoParser::AlternativeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitConcatenation(FandangoParser::ConcatenationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOperator(FandangoParser::OperatorContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKleene(FandangoParser::KleeneContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPlus(FandangoParser::PlusContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOption(FandangoParser::OptionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRepeat(FandangoParser::RepeatContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSymbol(FandangoParser::SymbolContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNonterminal_right(FandangoParser::Nonterminal_rightContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNonterminal(FandangoParser::NonterminalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGenerator_call(FandangoParser::Generator_callContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitChar_set(FandangoParser::Char_setContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitConstraint(FandangoParser::ConstraintContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImplies(FandangoParser::ImpliesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitQuantifier(FandangoParser::QuantifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitQuantifier_in_line(FandangoParser::Quantifier_in_lineContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFormula_disjunction(FandangoParser::Formula_disjunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFormula_conjunction(FandangoParser::Formula_conjunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFormula_atom(FandangoParser::Formula_atomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFormula_comparison(FandangoParser::Formula_comparisonContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpr(FandangoParser::ExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelector_length(FandangoParser::Selector_lengthContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_selection_or_dot_selection(FandangoParser::Star_selection_or_dot_selectionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_selection(FandangoParser::Star_selectionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDot_selection(FandangoParser::Dot_selectionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSelection(FandangoParser::SelectionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBase_selection(FandangoParser::Base_selectionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRs_pairs(FandangoParser::Rs_pairsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRs_pair(FandangoParser::Rs_pairContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRs_slices(FandangoParser::Rs_slicesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRs_slice(FandangoParser::Rs_sliceContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPython(FandangoParser::PythonContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPython_tag(FandangoParser::Python_tagContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPython_file(FandangoParser::Python_fileContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitInteractive(FandangoParser::InteractiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEval(FandangoParser::EvalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFunc_type(FandangoParser::Func_typeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStatements(FandangoParser::StatementsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStmt(FandangoParser::StmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStatement_newline(FandangoParser::Statement_newlineContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSimple_stmts(FandangoParser::Simple_stmtsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSimple_stmt(FandangoParser::Simple_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCompound_stmt(FandangoParser::Compound_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAssignment(FandangoParser::AssignmentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAnnotated_rhs(FandangoParser::Annotated_rhsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAugassign(FandangoParser::AugassignContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitReturn_stmt(FandangoParser::Return_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRaise_stmt(FandangoParser::Raise_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGlobal_stmt(FandangoParser::Global_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNonlocal_stmt(FandangoParser::Nonlocal_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDel_stmt(FandangoParser::Del_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitYield_stmt(FandangoParser::Yield_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAssert_stmt(FandangoParser::Assert_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImport_stmt(FandangoParser::Import_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImport_name(FandangoParser::Import_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImport_from(FandangoParser::Import_fromContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImport_from_targets(FandangoParser::Import_from_targetsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImport_from_as_names(FandangoParser::Import_from_as_namesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImport_from_as_name(FandangoParser::Import_from_as_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDotted_as_names(FandangoParser::Dotted_as_namesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDotted_as_name(FandangoParser::Dotted_as_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDotted_name(FandangoParser::Dotted_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBlock(FandangoParser::BlockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDecorators(FandangoParser::DecoratorsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitClass_def(FandangoParser::Class_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitClass_def_raw(FandangoParser::Class_def_rawContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFunction_def(FandangoParser::Function_defContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFunction_def_raw(FandangoParser::Function_def_rawContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParams(FandangoParser::ParamsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParameters(FandangoParser::ParametersContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSlash_no_default(FandangoParser::Slash_no_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSlash_with_default(FandangoParser::Slash_with_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_etc(FandangoParser::Star_etcContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKwds(FandangoParser::KwdsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParam_no_default(FandangoParser::Param_no_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParam_no_default_star_annotation(FandangoParser::Param_no_default_star_annotationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParam_with_default(FandangoParser::Param_with_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParam_maybe_default(FandangoParser::Param_maybe_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParam(FandangoParser::ParamContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParam_star_annotation(FandangoParser::Param_star_annotationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAnnotation(FandangoParser::AnnotationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_annotation(FandangoParser::Star_annotationContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDefault(FandangoParser::DefaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIf_stmt(FandangoParser::If_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitElif_stmt(FandangoParser::Elif_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitElse_block(FandangoParser::Else_blockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWhile_stmt(FandangoParser::While_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFor_stmt(FandangoParser::For_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWith_stmt(FandangoParser::With_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWith_item(FandangoParser::With_itemContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTry_stmt(FandangoParser::Try_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExcept_block(FandangoParser::Except_blockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExcept_star_block(FandangoParser::Except_star_blockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFinally_block(FandangoParser::Finally_blockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMatch_stmt(FandangoParser::Match_stmtContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSubject_expr(FandangoParser::Subject_exprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCase_block(FandangoParser::Case_blockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGuard(FandangoParser::GuardContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPatterns(FandangoParser::PatternsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPattern(FandangoParser::PatternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAs_pattern(FandangoParser::As_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOr_pattern(FandangoParser::Or_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitClosed_pattern(FandangoParser::Closed_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLiteral_pattern(FandangoParser::Literal_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLiteral_expr(FandangoParser::Literal_exprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitComplex_number(FandangoParser::Complex_numberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSigned_number(FandangoParser::Signed_numberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSigned_real_number(FandangoParser::Signed_real_numberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitReal_number(FandangoParser::Real_numberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitImaginary_number(FandangoParser::Imaginary_numberContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCapture_pattern(FandangoParser::Capture_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPattern_capture_target(FandangoParser::Pattern_capture_targetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitWildcard_pattern(FandangoParser::Wildcard_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitValue_pattern(FandangoParser::Value_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAttr(FandangoParser::AttrContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitName_or_attr(FandangoParser::Name_or_attrContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGroup_pattern(FandangoParser::Group_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSequence_pattern(FandangoParser::Sequence_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitOpen_sequence_pattern(FandangoParser::Open_sequence_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMaybe_sequence_pattern(FandangoParser::Maybe_sequence_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMaybe_star_pattern(FandangoParser::Maybe_star_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_pattern(FandangoParser::Star_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMapping_pattern(FandangoParser::Mapping_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitItems_pattern(FandangoParser::Items_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKey_value_pattern(FandangoParser::Key_value_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDouble_star_pattern(FandangoParser::Double_star_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitClass_pattern(FandangoParser::Class_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPositional_patterns(FandangoParser::Positional_patternsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKeyword_patterns(FandangoParser::Keyword_patternsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKeyword_pattern(FandangoParser::Keyword_patternContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_alias(FandangoParser::Type_aliasContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_params(FandangoParser::Type_paramsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_param_seq(FandangoParser::Type_param_seqContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_param(FandangoParser::Type_paramContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_param_bound(FandangoParser::Type_param_boundContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpressions(FandangoParser::ExpressionsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpression(FandangoParser::ExpressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitYield_expr(FandangoParser::Yield_exprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_expressions(FandangoParser::Star_expressionsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_expression(FandangoParser::Star_expressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_named_expressions(FandangoParser::Star_named_expressionsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_named_expression(FandangoParser::Star_named_expressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAssignment_expression(FandangoParser::Assignment_expressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNamed_expression(FandangoParser::Named_expressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDisjunction(FandangoParser::DisjunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitConjunction(FandangoParser::ConjunctionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitInversion(FandangoParser::InversionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitComparison(FandangoParser::ComparisonContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCompare_op_bitwise_or_pair(FandangoParser::Compare_op_bitwise_or_pairContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitEq_bitwise_or(FandangoParser::Eq_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNoteq_bitwise_or(FandangoParser::Noteq_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLte_bitwise_or(FandangoParser::Lte_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLt_bitwise_or(FandangoParser::Lt_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGte_bitwise_or(FandangoParser::Gte_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGt_bitwise_or(FandangoParser::Gt_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNotin_bitwise_or(FandangoParser::Notin_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIn_bitwise_or(FandangoParser::In_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIsnot_bitwise_or(FandangoParser::Isnot_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIs_bitwise_or(FandangoParser::Is_bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBitwise_or(FandangoParser::Bitwise_orContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBitwise_xor(FandangoParser::Bitwise_xorContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitBitwise_and(FandangoParser::Bitwise_andContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitShift_expr(FandangoParser::Shift_exprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSum(FandangoParser::SumContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTerm(FandangoParser::TermContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFactor(FandangoParser::FactorContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPower(FandangoParser::PowerContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAwait_primary(FandangoParser::Await_primaryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPrimary(FandangoParser::PrimaryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSlices(FandangoParser::SlicesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSlice(FandangoParser::SliceContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAtom(FandangoParser::AtomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGroup(FandangoParser::GroupContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambdef(FandangoParser::LambdefContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_params(FandangoParser::Lambda_paramsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_parameters(FandangoParser::Lambda_parametersContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_slash_no_default(FandangoParser::Lambda_slash_no_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_slash_with_default(FandangoParser::Lambda_slash_with_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_star_etc(FandangoParser::Lambda_star_etcContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_kwds(FandangoParser::Lambda_kwdsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_param_no_default(FandangoParser::Lambda_param_no_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_param_with_default(FandangoParser::Lambda_param_with_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_param_maybe_default(FandangoParser::Lambda_param_maybe_defaultContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLambda_param(FandangoParser::Lambda_paramContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_middle_no_quote(FandangoParser::Fstring_middle_no_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_middle_no_single_quote(FandangoParser::Fstring_middle_no_single_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_middle_breaks_no_triple_quote(FandangoParser::Fstring_middle_breaks_no_triple_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_middle_breaks_no_triple_single_quote(FandangoParser::Fstring_middle_breaks_no_triple_single_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_any_no_quote(FandangoParser::Fstring_any_no_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_any_no_single_quote(FandangoParser::Fstring_any_no_single_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_middle(FandangoParser::Fstring_middleContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_any_breaks_no_triple_quote(FandangoParser::Fstring_any_breaks_no_triple_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_any_breaks_no_triple_single_quote(FandangoParser::Fstring_any_breaks_no_triple_single_quoteContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_any(FandangoParser::Fstring_anyContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_replacement_field(FandangoParser::Fstring_replacement_fieldContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_conversion(FandangoParser::Fstring_conversionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_full_format_spec(FandangoParser::Fstring_full_format_specContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring_format_spec(FandangoParser::Fstring_format_specContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFstring(FandangoParser::FstringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitString(FandangoParser::StringContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStrings(FandangoParser::StringsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitList(FandangoParser::ListContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTuple(FandangoParser::TupleContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSet(FandangoParser::SetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDict(FandangoParser::DictContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDouble_starred_kvpairs(FandangoParser::Double_starred_kvpairsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDouble_starred_kvpair(FandangoParser::Double_starred_kvpairContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKvpair(FandangoParser::KvpairContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFor_if_clauses(FandangoParser::For_if_clausesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFor_if_clause(FandangoParser::For_if_clauseContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitListcomp(FandangoParser::ListcompContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSetcomp(FandangoParser::SetcompContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitGenexp(FandangoParser::GenexpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDictcomp(FandangoParser::DictcompContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArguments(FandangoParser::ArgumentsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArgs(FandangoParser::ArgsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArg(FandangoParser::ArgContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKwargs(FandangoParser::KwargsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStarred_expression(FandangoParser::Starred_expressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKwarg_or_starred(FandangoParser::Kwarg_or_starredContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitKwarg_or_double_starred(FandangoParser::Kwarg_or_double_starredContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_targets(FandangoParser::Star_targetsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_targets_list_seq(FandangoParser::Star_targets_list_seqContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_targets_tuple_seq(FandangoParser::Star_targets_tuple_seqContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_target(FandangoParser::Star_targetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitTarget_with_star_atom(FandangoParser::Target_with_star_atomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStar_atom(FandangoParser::Star_atomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSingle_target(FandangoParser::Single_targetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitSingle_subscript_attribute_target(FandangoParser::Single_subscript_attribute_targetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitT_primary(FandangoParser::T_primaryContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDel_targets(FandangoParser::Del_targetsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDel_target(FandangoParser::Del_targetContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDel_t_atom(FandangoParser::Del_t_atomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitType_expressions(FandangoParser::Type_expressionsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitFunc_type_comment(FandangoParser::Func_type_commentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIdentifier(FandangoParser::IdentifierContext *ctx) override {
    return visitChildren(ctx);
  }


};

