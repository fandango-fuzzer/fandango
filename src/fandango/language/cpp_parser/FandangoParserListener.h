
// Generated from language/FandangoParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "FandangoParser.h"


/**
 * This interface defines an abstract listener for a parse tree produced by FandangoParser.
 */
class  FandangoParserListener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterFandango(FandangoParser::FandangoContext *ctx) = 0;
  virtual void exitFandango(FandangoParser::FandangoContext *ctx) = 0;

  virtual void enterProgram(FandangoParser::ProgramContext *ctx) = 0;
  virtual void exitProgram(FandangoParser::ProgramContext *ctx) = 0;

  virtual void enterStatement(FandangoParser::StatementContext *ctx) = 0;
  virtual void exitStatement(FandangoParser::StatementContext *ctx) = 0;

  virtual void enterProduction(FandangoParser::ProductionContext *ctx) = 0;
  virtual void exitProduction(FandangoParser::ProductionContext *ctx) = 0;

  virtual void enterAlternative(FandangoParser::AlternativeContext *ctx) = 0;
  virtual void exitAlternative(FandangoParser::AlternativeContext *ctx) = 0;

  virtual void enterConcatenation(FandangoParser::ConcatenationContext *ctx) = 0;
  virtual void exitConcatenation(FandangoParser::ConcatenationContext *ctx) = 0;

  virtual void enterOperator(FandangoParser::OperatorContext *ctx) = 0;
  virtual void exitOperator(FandangoParser::OperatorContext *ctx) = 0;

  virtual void enterKleene(FandangoParser::KleeneContext *ctx) = 0;
  virtual void exitKleene(FandangoParser::KleeneContext *ctx) = 0;

  virtual void enterPlus(FandangoParser::PlusContext *ctx) = 0;
  virtual void exitPlus(FandangoParser::PlusContext *ctx) = 0;

  virtual void enterOption(FandangoParser::OptionContext *ctx) = 0;
  virtual void exitOption(FandangoParser::OptionContext *ctx) = 0;

  virtual void enterRepeat(FandangoParser::RepeatContext *ctx) = 0;
  virtual void exitRepeat(FandangoParser::RepeatContext *ctx) = 0;

  virtual void enterSymbol(FandangoParser::SymbolContext *ctx) = 0;
  virtual void exitSymbol(FandangoParser::SymbolContext *ctx) = 0;

  virtual void enterGenerator_call(FandangoParser::Generator_callContext *ctx) = 0;
  virtual void exitGenerator_call(FandangoParser::Generator_callContext *ctx) = 0;

  virtual void enterChar_set(FandangoParser::Char_setContext *ctx) = 0;
  virtual void exitChar_set(FandangoParser::Char_setContext *ctx) = 0;

  virtual void enterConstraint(FandangoParser::ConstraintContext *ctx) = 0;
  virtual void exitConstraint(FandangoParser::ConstraintContext *ctx) = 0;

  virtual void enterImplies(FandangoParser::ImpliesContext *ctx) = 0;
  virtual void exitImplies(FandangoParser::ImpliesContext *ctx) = 0;

  virtual void enterQuantifier(FandangoParser::QuantifierContext *ctx) = 0;
  virtual void exitQuantifier(FandangoParser::QuantifierContext *ctx) = 0;

  virtual void enterFormula_disjunction(FandangoParser::Formula_disjunctionContext *ctx) = 0;
  virtual void exitFormula_disjunction(FandangoParser::Formula_disjunctionContext *ctx) = 0;

  virtual void enterFormula_conjunction(FandangoParser::Formula_conjunctionContext *ctx) = 0;
  virtual void exitFormula_conjunction(FandangoParser::Formula_conjunctionContext *ctx) = 0;

  virtual void enterFormula_atom(FandangoParser::Formula_atomContext *ctx) = 0;
  virtual void exitFormula_atom(FandangoParser::Formula_atomContext *ctx) = 0;

  virtual void enterFormula_comparison(FandangoParser::Formula_comparisonContext *ctx) = 0;
  virtual void exitFormula_comparison(FandangoParser::Formula_comparisonContext *ctx) = 0;

  virtual void enterExpr(FandangoParser::ExprContext *ctx) = 0;
  virtual void exitExpr(FandangoParser::ExprContext *ctx) = 0;

  virtual void enterSelector_length(FandangoParser::Selector_lengthContext *ctx) = 0;
  virtual void exitSelector_length(FandangoParser::Selector_lengthContext *ctx) = 0;

  virtual void enterSelector(FandangoParser::SelectorContext *ctx) = 0;
  virtual void exitSelector(FandangoParser::SelectorContext *ctx) = 0;

  virtual void enterSelection(FandangoParser::SelectionContext *ctx) = 0;
  virtual void exitSelection(FandangoParser::SelectionContext *ctx) = 0;

  virtual void enterBase_selection(FandangoParser::Base_selectionContext *ctx) = 0;
  virtual void exitBase_selection(FandangoParser::Base_selectionContext *ctx) = 0;

  virtual void enterRs_pairs(FandangoParser::Rs_pairsContext *ctx) = 0;
  virtual void exitRs_pairs(FandangoParser::Rs_pairsContext *ctx) = 0;

  virtual void enterRs_pair(FandangoParser::Rs_pairContext *ctx) = 0;
  virtual void exitRs_pair(FandangoParser::Rs_pairContext *ctx) = 0;

  virtual void enterRs_slices(FandangoParser::Rs_slicesContext *ctx) = 0;
  virtual void exitRs_slices(FandangoParser::Rs_slicesContext *ctx) = 0;

  virtual void enterRs_slice(FandangoParser::Rs_sliceContext *ctx) = 0;
  virtual void exitRs_slice(FandangoParser::Rs_sliceContext *ctx) = 0;

  virtual void enterPython(FandangoParser::PythonContext *ctx) = 0;
  virtual void exitPython(FandangoParser::PythonContext *ctx) = 0;

  virtual void enterPython_tag(FandangoParser::Python_tagContext *ctx) = 0;
  virtual void exitPython_tag(FandangoParser::Python_tagContext *ctx) = 0;

  virtual void enterPython_file(FandangoParser::Python_fileContext *ctx) = 0;
  virtual void exitPython_file(FandangoParser::Python_fileContext *ctx) = 0;

  virtual void enterInteractive(FandangoParser::InteractiveContext *ctx) = 0;
  virtual void exitInteractive(FandangoParser::InteractiveContext *ctx) = 0;

  virtual void enterEval(FandangoParser::EvalContext *ctx) = 0;
  virtual void exitEval(FandangoParser::EvalContext *ctx) = 0;

  virtual void enterFunc_type(FandangoParser::Func_typeContext *ctx) = 0;
  virtual void exitFunc_type(FandangoParser::Func_typeContext *ctx) = 0;

  virtual void enterStatements(FandangoParser::StatementsContext *ctx) = 0;
  virtual void exitStatements(FandangoParser::StatementsContext *ctx) = 0;

  virtual void enterStmt(FandangoParser::StmtContext *ctx) = 0;
  virtual void exitStmt(FandangoParser::StmtContext *ctx) = 0;

  virtual void enterStatement_newline(FandangoParser::Statement_newlineContext *ctx) = 0;
  virtual void exitStatement_newline(FandangoParser::Statement_newlineContext *ctx) = 0;

  virtual void enterSimple_stmts(FandangoParser::Simple_stmtsContext *ctx) = 0;
  virtual void exitSimple_stmts(FandangoParser::Simple_stmtsContext *ctx) = 0;

  virtual void enterSimple_stmt(FandangoParser::Simple_stmtContext *ctx) = 0;
  virtual void exitSimple_stmt(FandangoParser::Simple_stmtContext *ctx) = 0;

  virtual void enterCompound_stmt(FandangoParser::Compound_stmtContext *ctx) = 0;
  virtual void exitCompound_stmt(FandangoParser::Compound_stmtContext *ctx) = 0;

  virtual void enterAssignment(FandangoParser::AssignmentContext *ctx) = 0;
  virtual void exitAssignment(FandangoParser::AssignmentContext *ctx) = 0;

  virtual void enterAnnotated_rhs(FandangoParser::Annotated_rhsContext *ctx) = 0;
  virtual void exitAnnotated_rhs(FandangoParser::Annotated_rhsContext *ctx) = 0;

  virtual void enterAugassign(FandangoParser::AugassignContext *ctx) = 0;
  virtual void exitAugassign(FandangoParser::AugassignContext *ctx) = 0;

  virtual void enterReturn_stmt(FandangoParser::Return_stmtContext *ctx) = 0;
  virtual void exitReturn_stmt(FandangoParser::Return_stmtContext *ctx) = 0;

  virtual void enterRaise_stmt(FandangoParser::Raise_stmtContext *ctx) = 0;
  virtual void exitRaise_stmt(FandangoParser::Raise_stmtContext *ctx) = 0;

  virtual void enterGlobal_stmt(FandangoParser::Global_stmtContext *ctx) = 0;
  virtual void exitGlobal_stmt(FandangoParser::Global_stmtContext *ctx) = 0;

  virtual void enterNonlocal_stmt(FandangoParser::Nonlocal_stmtContext *ctx) = 0;
  virtual void exitNonlocal_stmt(FandangoParser::Nonlocal_stmtContext *ctx) = 0;

  virtual void enterDel_stmt(FandangoParser::Del_stmtContext *ctx) = 0;
  virtual void exitDel_stmt(FandangoParser::Del_stmtContext *ctx) = 0;

  virtual void enterYield_stmt(FandangoParser::Yield_stmtContext *ctx) = 0;
  virtual void exitYield_stmt(FandangoParser::Yield_stmtContext *ctx) = 0;

  virtual void enterAssert_stmt(FandangoParser::Assert_stmtContext *ctx) = 0;
  virtual void exitAssert_stmt(FandangoParser::Assert_stmtContext *ctx) = 0;

  virtual void enterImport_stmt(FandangoParser::Import_stmtContext *ctx) = 0;
  virtual void exitImport_stmt(FandangoParser::Import_stmtContext *ctx) = 0;

  virtual void enterImport_name(FandangoParser::Import_nameContext *ctx) = 0;
  virtual void exitImport_name(FandangoParser::Import_nameContext *ctx) = 0;

  virtual void enterImport_from(FandangoParser::Import_fromContext *ctx) = 0;
  virtual void exitImport_from(FandangoParser::Import_fromContext *ctx) = 0;

  virtual void enterImport_from_targets(FandangoParser::Import_from_targetsContext *ctx) = 0;
  virtual void exitImport_from_targets(FandangoParser::Import_from_targetsContext *ctx) = 0;

  virtual void enterImport_from_as_names(FandangoParser::Import_from_as_namesContext *ctx) = 0;
  virtual void exitImport_from_as_names(FandangoParser::Import_from_as_namesContext *ctx) = 0;

  virtual void enterImport_from_as_name(FandangoParser::Import_from_as_nameContext *ctx) = 0;
  virtual void exitImport_from_as_name(FandangoParser::Import_from_as_nameContext *ctx) = 0;

  virtual void enterDotted_as_names(FandangoParser::Dotted_as_namesContext *ctx) = 0;
  virtual void exitDotted_as_names(FandangoParser::Dotted_as_namesContext *ctx) = 0;

  virtual void enterDotted_as_name(FandangoParser::Dotted_as_nameContext *ctx) = 0;
  virtual void exitDotted_as_name(FandangoParser::Dotted_as_nameContext *ctx) = 0;

  virtual void enterDotted_name(FandangoParser::Dotted_nameContext *ctx) = 0;
  virtual void exitDotted_name(FandangoParser::Dotted_nameContext *ctx) = 0;

  virtual void enterBlock(FandangoParser::BlockContext *ctx) = 0;
  virtual void exitBlock(FandangoParser::BlockContext *ctx) = 0;

  virtual void enterDecorators(FandangoParser::DecoratorsContext *ctx) = 0;
  virtual void exitDecorators(FandangoParser::DecoratorsContext *ctx) = 0;

  virtual void enterClass_def(FandangoParser::Class_defContext *ctx) = 0;
  virtual void exitClass_def(FandangoParser::Class_defContext *ctx) = 0;

  virtual void enterClass_def_raw(FandangoParser::Class_def_rawContext *ctx) = 0;
  virtual void exitClass_def_raw(FandangoParser::Class_def_rawContext *ctx) = 0;

  virtual void enterFunction_def(FandangoParser::Function_defContext *ctx) = 0;
  virtual void exitFunction_def(FandangoParser::Function_defContext *ctx) = 0;

  virtual void enterFunction_def_raw(FandangoParser::Function_def_rawContext *ctx) = 0;
  virtual void exitFunction_def_raw(FandangoParser::Function_def_rawContext *ctx) = 0;

  virtual void enterParams(FandangoParser::ParamsContext *ctx) = 0;
  virtual void exitParams(FandangoParser::ParamsContext *ctx) = 0;

  virtual void enterParameters(FandangoParser::ParametersContext *ctx) = 0;
  virtual void exitParameters(FandangoParser::ParametersContext *ctx) = 0;

  virtual void enterSlash_no_default(FandangoParser::Slash_no_defaultContext *ctx) = 0;
  virtual void exitSlash_no_default(FandangoParser::Slash_no_defaultContext *ctx) = 0;

  virtual void enterSlash_with_default(FandangoParser::Slash_with_defaultContext *ctx) = 0;
  virtual void exitSlash_with_default(FandangoParser::Slash_with_defaultContext *ctx) = 0;

  virtual void enterStar_etc(FandangoParser::Star_etcContext *ctx) = 0;
  virtual void exitStar_etc(FandangoParser::Star_etcContext *ctx) = 0;

  virtual void enterKwds(FandangoParser::KwdsContext *ctx) = 0;
  virtual void exitKwds(FandangoParser::KwdsContext *ctx) = 0;

  virtual void enterParam_no_default(FandangoParser::Param_no_defaultContext *ctx) = 0;
  virtual void exitParam_no_default(FandangoParser::Param_no_defaultContext *ctx) = 0;

  virtual void enterParam_no_default_star_annotation(FandangoParser::Param_no_default_star_annotationContext *ctx) = 0;
  virtual void exitParam_no_default_star_annotation(FandangoParser::Param_no_default_star_annotationContext *ctx) = 0;

  virtual void enterParam_with_default(FandangoParser::Param_with_defaultContext *ctx) = 0;
  virtual void exitParam_with_default(FandangoParser::Param_with_defaultContext *ctx) = 0;

  virtual void enterParam_maybe_default(FandangoParser::Param_maybe_defaultContext *ctx) = 0;
  virtual void exitParam_maybe_default(FandangoParser::Param_maybe_defaultContext *ctx) = 0;

  virtual void enterParam(FandangoParser::ParamContext *ctx) = 0;
  virtual void exitParam(FandangoParser::ParamContext *ctx) = 0;

  virtual void enterParam_star_annotation(FandangoParser::Param_star_annotationContext *ctx) = 0;
  virtual void exitParam_star_annotation(FandangoParser::Param_star_annotationContext *ctx) = 0;

  virtual void enterAnnotation(FandangoParser::AnnotationContext *ctx) = 0;
  virtual void exitAnnotation(FandangoParser::AnnotationContext *ctx) = 0;

  virtual void enterStar_annotation(FandangoParser::Star_annotationContext *ctx) = 0;
  virtual void exitStar_annotation(FandangoParser::Star_annotationContext *ctx) = 0;

  virtual void enterDefault(FandangoParser::DefaultContext *ctx) = 0;
  virtual void exitDefault(FandangoParser::DefaultContext *ctx) = 0;

  virtual void enterIf_stmt(FandangoParser::If_stmtContext *ctx) = 0;
  virtual void exitIf_stmt(FandangoParser::If_stmtContext *ctx) = 0;

  virtual void enterElif_stmt(FandangoParser::Elif_stmtContext *ctx) = 0;
  virtual void exitElif_stmt(FandangoParser::Elif_stmtContext *ctx) = 0;

  virtual void enterElse_block(FandangoParser::Else_blockContext *ctx) = 0;
  virtual void exitElse_block(FandangoParser::Else_blockContext *ctx) = 0;

  virtual void enterWhile_stmt(FandangoParser::While_stmtContext *ctx) = 0;
  virtual void exitWhile_stmt(FandangoParser::While_stmtContext *ctx) = 0;

  virtual void enterFor_stmt(FandangoParser::For_stmtContext *ctx) = 0;
  virtual void exitFor_stmt(FandangoParser::For_stmtContext *ctx) = 0;

  virtual void enterWith_stmt(FandangoParser::With_stmtContext *ctx) = 0;
  virtual void exitWith_stmt(FandangoParser::With_stmtContext *ctx) = 0;

  virtual void enterWith_item(FandangoParser::With_itemContext *ctx) = 0;
  virtual void exitWith_item(FandangoParser::With_itemContext *ctx) = 0;

  virtual void enterTry_stmt(FandangoParser::Try_stmtContext *ctx) = 0;
  virtual void exitTry_stmt(FandangoParser::Try_stmtContext *ctx) = 0;

  virtual void enterExcept_block(FandangoParser::Except_blockContext *ctx) = 0;
  virtual void exitExcept_block(FandangoParser::Except_blockContext *ctx) = 0;

  virtual void enterExcept_star_block(FandangoParser::Except_star_blockContext *ctx) = 0;
  virtual void exitExcept_star_block(FandangoParser::Except_star_blockContext *ctx) = 0;

  virtual void enterFinally_block(FandangoParser::Finally_blockContext *ctx) = 0;
  virtual void exitFinally_block(FandangoParser::Finally_blockContext *ctx) = 0;

  virtual void enterMatch_stmt(FandangoParser::Match_stmtContext *ctx) = 0;
  virtual void exitMatch_stmt(FandangoParser::Match_stmtContext *ctx) = 0;

  virtual void enterSubject_expr(FandangoParser::Subject_exprContext *ctx) = 0;
  virtual void exitSubject_expr(FandangoParser::Subject_exprContext *ctx) = 0;

  virtual void enterCase_block(FandangoParser::Case_blockContext *ctx) = 0;
  virtual void exitCase_block(FandangoParser::Case_blockContext *ctx) = 0;

  virtual void enterGuard(FandangoParser::GuardContext *ctx) = 0;
  virtual void exitGuard(FandangoParser::GuardContext *ctx) = 0;

  virtual void enterPatterns(FandangoParser::PatternsContext *ctx) = 0;
  virtual void exitPatterns(FandangoParser::PatternsContext *ctx) = 0;

  virtual void enterPattern(FandangoParser::PatternContext *ctx) = 0;
  virtual void exitPattern(FandangoParser::PatternContext *ctx) = 0;

  virtual void enterAs_pattern(FandangoParser::As_patternContext *ctx) = 0;
  virtual void exitAs_pattern(FandangoParser::As_patternContext *ctx) = 0;

  virtual void enterOr_pattern(FandangoParser::Or_patternContext *ctx) = 0;
  virtual void exitOr_pattern(FandangoParser::Or_patternContext *ctx) = 0;

  virtual void enterClosed_pattern(FandangoParser::Closed_patternContext *ctx) = 0;
  virtual void exitClosed_pattern(FandangoParser::Closed_patternContext *ctx) = 0;

  virtual void enterLiteral_pattern(FandangoParser::Literal_patternContext *ctx) = 0;
  virtual void exitLiteral_pattern(FandangoParser::Literal_patternContext *ctx) = 0;

  virtual void enterLiteral_expr(FandangoParser::Literal_exprContext *ctx) = 0;
  virtual void exitLiteral_expr(FandangoParser::Literal_exprContext *ctx) = 0;

  virtual void enterComplex_number(FandangoParser::Complex_numberContext *ctx) = 0;
  virtual void exitComplex_number(FandangoParser::Complex_numberContext *ctx) = 0;

  virtual void enterSigned_number(FandangoParser::Signed_numberContext *ctx) = 0;
  virtual void exitSigned_number(FandangoParser::Signed_numberContext *ctx) = 0;

  virtual void enterSigned_real_number(FandangoParser::Signed_real_numberContext *ctx) = 0;
  virtual void exitSigned_real_number(FandangoParser::Signed_real_numberContext *ctx) = 0;

  virtual void enterReal_number(FandangoParser::Real_numberContext *ctx) = 0;
  virtual void exitReal_number(FandangoParser::Real_numberContext *ctx) = 0;

  virtual void enterImaginary_number(FandangoParser::Imaginary_numberContext *ctx) = 0;
  virtual void exitImaginary_number(FandangoParser::Imaginary_numberContext *ctx) = 0;

  virtual void enterCapture_pattern(FandangoParser::Capture_patternContext *ctx) = 0;
  virtual void exitCapture_pattern(FandangoParser::Capture_patternContext *ctx) = 0;

  virtual void enterPattern_capture_target(FandangoParser::Pattern_capture_targetContext *ctx) = 0;
  virtual void exitPattern_capture_target(FandangoParser::Pattern_capture_targetContext *ctx) = 0;

  virtual void enterWildcard_pattern(FandangoParser::Wildcard_patternContext *ctx) = 0;
  virtual void exitWildcard_pattern(FandangoParser::Wildcard_patternContext *ctx) = 0;

  virtual void enterValue_pattern(FandangoParser::Value_patternContext *ctx) = 0;
  virtual void exitValue_pattern(FandangoParser::Value_patternContext *ctx) = 0;

  virtual void enterAttr(FandangoParser::AttrContext *ctx) = 0;
  virtual void exitAttr(FandangoParser::AttrContext *ctx) = 0;

  virtual void enterName_or_attr(FandangoParser::Name_or_attrContext *ctx) = 0;
  virtual void exitName_or_attr(FandangoParser::Name_or_attrContext *ctx) = 0;

  virtual void enterGroup_pattern(FandangoParser::Group_patternContext *ctx) = 0;
  virtual void exitGroup_pattern(FandangoParser::Group_patternContext *ctx) = 0;

  virtual void enterSequence_pattern(FandangoParser::Sequence_patternContext *ctx) = 0;
  virtual void exitSequence_pattern(FandangoParser::Sequence_patternContext *ctx) = 0;

  virtual void enterOpen_sequence_pattern(FandangoParser::Open_sequence_patternContext *ctx) = 0;
  virtual void exitOpen_sequence_pattern(FandangoParser::Open_sequence_patternContext *ctx) = 0;

  virtual void enterMaybe_sequence_pattern(FandangoParser::Maybe_sequence_patternContext *ctx) = 0;
  virtual void exitMaybe_sequence_pattern(FandangoParser::Maybe_sequence_patternContext *ctx) = 0;

  virtual void enterMaybe_star_pattern(FandangoParser::Maybe_star_patternContext *ctx) = 0;
  virtual void exitMaybe_star_pattern(FandangoParser::Maybe_star_patternContext *ctx) = 0;

  virtual void enterStar_pattern(FandangoParser::Star_patternContext *ctx) = 0;
  virtual void exitStar_pattern(FandangoParser::Star_patternContext *ctx) = 0;

  virtual void enterMapping_pattern(FandangoParser::Mapping_patternContext *ctx) = 0;
  virtual void exitMapping_pattern(FandangoParser::Mapping_patternContext *ctx) = 0;

  virtual void enterItems_pattern(FandangoParser::Items_patternContext *ctx) = 0;
  virtual void exitItems_pattern(FandangoParser::Items_patternContext *ctx) = 0;

  virtual void enterKey_value_pattern(FandangoParser::Key_value_patternContext *ctx) = 0;
  virtual void exitKey_value_pattern(FandangoParser::Key_value_patternContext *ctx) = 0;

  virtual void enterDouble_star_pattern(FandangoParser::Double_star_patternContext *ctx) = 0;
  virtual void exitDouble_star_pattern(FandangoParser::Double_star_patternContext *ctx) = 0;

  virtual void enterClass_pattern(FandangoParser::Class_patternContext *ctx) = 0;
  virtual void exitClass_pattern(FandangoParser::Class_patternContext *ctx) = 0;

  virtual void enterPositional_patterns(FandangoParser::Positional_patternsContext *ctx) = 0;
  virtual void exitPositional_patterns(FandangoParser::Positional_patternsContext *ctx) = 0;

  virtual void enterKeyword_patterns(FandangoParser::Keyword_patternsContext *ctx) = 0;
  virtual void exitKeyword_patterns(FandangoParser::Keyword_patternsContext *ctx) = 0;

  virtual void enterKeyword_pattern(FandangoParser::Keyword_patternContext *ctx) = 0;
  virtual void exitKeyword_pattern(FandangoParser::Keyword_patternContext *ctx) = 0;

  virtual void enterType_alias(FandangoParser::Type_aliasContext *ctx) = 0;
  virtual void exitType_alias(FandangoParser::Type_aliasContext *ctx) = 0;

  virtual void enterType_params(FandangoParser::Type_paramsContext *ctx) = 0;
  virtual void exitType_params(FandangoParser::Type_paramsContext *ctx) = 0;

  virtual void enterType_param_seq(FandangoParser::Type_param_seqContext *ctx) = 0;
  virtual void exitType_param_seq(FandangoParser::Type_param_seqContext *ctx) = 0;

  virtual void enterType_param(FandangoParser::Type_paramContext *ctx) = 0;
  virtual void exitType_param(FandangoParser::Type_paramContext *ctx) = 0;

  virtual void enterType_param_bound(FandangoParser::Type_param_boundContext *ctx) = 0;
  virtual void exitType_param_bound(FandangoParser::Type_param_boundContext *ctx) = 0;

  virtual void enterExpressions(FandangoParser::ExpressionsContext *ctx) = 0;
  virtual void exitExpressions(FandangoParser::ExpressionsContext *ctx) = 0;

  virtual void enterExpression(FandangoParser::ExpressionContext *ctx) = 0;
  virtual void exitExpression(FandangoParser::ExpressionContext *ctx) = 0;

  virtual void enterYield_expr(FandangoParser::Yield_exprContext *ctx) = 0;
  virtual void exitYield_expr(FandangoParser::Yield_exprContext *ctx) = 0;

  virtual void enterStar_expressions(FandangoParser::Star_expressionsContext *ctx) = 0;
  virtual void exitStar_expressions(FandangoParser::Star_expressionsContext *ctx) = 0;

  virtual void enterStar_expression(FandangoParser::Star_expressionContext *ctx) = 0;
  virtual void exitStar_expression(FandangoParser::Star_expressionContext *ctx) = 0;

  virtual void enterStar_named_expressions(FandangoParser::Star_named_expressionsContext *ctx) = 0;
  virtual void exitStar_named_expressions(FandangoParser::Star_named_expressionsContext *ctx) = 0;

  virtual void enterStar_named_expression(FandangoParser::Star_named_expressionContext *ctx) = 0;
  virtual void exitStar_named_expression(FandangoParser::Star_named_expressionContext *ctx) = 0;

  virtual void enterAssignment_expression(FandangoParser::Assignment_expressionContext *ctx) = 0;
  virtual void exitAssignment_expression(FandangoParser::Assignment_expressionContext *ctx) = 0;

  virtual void enterNamed_expression(FandangoParser::Named_expressionContext *ctx) = 0;
  virtual void exitNamed_expression(FandangoParser::Named_expressionContext *ctx) = 0;

  virtual void enterDisjunction(FandangoParser::DisjunctionContext *ctx) = 0;
  virtual void exitDisjunction(FandangoParser::DisjunctionContext *ctx) = 0;

  virtual void enterConjunction(FandangoParser::ConjunctionContext *ctx) = 0;
  virtual void exitConjunction(FandangoParser::ConjunctionContext *ctx) = 0;

  virtual void enterInversion(FandangoParser::InversionContext *ctx) = 0;
  virtual void exitInversion(FandangoParser::InversionContext *ctx) = 0;

  virtual void enterComparison(FandangoParser::ComparisonContext *ctx) = 0;
  virtual void exitComparison(FandangoParser::ComparisonContext *ctx) = 0;

  virtual void enterCompare_op_bitwise_or_pair(FandangoParser::Compare_op_bitwise_or_pairContext *ctx) = 0;
  virtual void exitCompare_op_bitwise_or_pair(FandangoParser::Compare_op_bitwise_or_pairContext *ctx) = 0;

  virtual void enterEq_bitwise_or(FandangoParser::Eq_bitwise_orContext *ctx) = 0;
  virtual void exitEq_bitwise_or(FandangoParser::Eq_bitwise_orContext *ctx) = 0;

  virtual void enterNoteq_bitwise_or(FandangoParser::Noteq_bitwise_orContext *ctx) = 0;
  virtual void exitNoteq_bitwise_or(FandangoParser::Noteq_bitwise_orContext *ctx) = 0;

  virtual void enterLte_bitwise_or(FandangoParser::Lte_bitwise_orContext *ctx) = 0;
  virtual void exitLte_bitwise_or(FandangoParser::Lte_bitwise_orContext *ctx) = 0;

  virtual void enterLt_bitwise_or(FandangoParser::Lt_bitwise_orContext *ctx) = 0;
  virtual void exitLt_bitwise_or(FandangoParser::Lt_bitwise_orContext *ctx) = 0;

  virtual void enterGte_bitwise_or(FandangoParser::Gte_bitwise_orContext *ctx) = 0;
  virtual void exitGte_bitwise_or(FandangoParser::Gte_bitwise_orContext *ctx) = 0;

  virtual void enterGt_bitwise_or(FandangoParser::Gt_bitwise_orContext *ctx) = 0;
  virtual void exitGt_bitwise_or(FandangoParser::Gt_bitwise_orContext *ctx) = 0;

  virtual void enterNotin_bitwise_or(FandangoParser::Notin_bitwise_orContext *ctx) = 0;
  virtual void exitNotin_bitwise_or(FandangoParser::Notin_bitwise_orContext *ctx) = 0;

  virtual void enterIn_bitwise_or(FandangoParser::In_bitwise_orContext *ctx) = 0;
  virtual void exitIn_bitwise_or(FandangoParser::In_bitwise_orContext *ctx) = 0;

  virtual void enterIsnot_bitwise_or(FandangoParser::Isnot_bitwise_orContext *ctx) = 0;
  virtual void exitIsnot_bitwise_or(FandangoParser::Isnot_bitwise_orContext *ctx) = 0;

  virtual void enterIs_bitwise_or(FandangoParser::Is_bitwise_orContext *ctx) = 0;
  virtual void exitIs_bitwise_or(FandangoParser::Is_bitwise_orContext *ctx) = 0;

  virtual void enterBitwise_or(FandangoParser::Bitwise_orContext *ctx) = 0;
  virtual void exitBitwise_or(FandangoParser::Bitwise_orContext *ctx) = 0;

  virtual void enterBitwise_xor(FandangoParser::Bitwise_xorContext *ctx) = 0;
  virtual void exitBitwise_xor(FandangoParser::Bitwise_xorContext *ctx) = 0;

  virtual void enterBitwise_and(FandangoParser::Bitwise_andContext *ctx) = 0;
  virtual void exitBitwise_and(FandangoParser::Bitwise_andContext *ctx) = 0;

  virtual void enterShift_expr(FandangoParser::Shift_exprContext *ctx) = 0;
  virtual void exitShift_expr(FandangoParser::Shift_exprContext *ctx) = 0;

  virtual void enterSum(FandangoParser::SumContext *ctx) = 0;
  virtual void exitSum(FandangoParser::SumContext *ctx) = 0;

  virtual void enterTerm(FandangoParser::TermContext *ctx) = 0;
  virtual void exitTerm(FandangoParser::TermContext *ctx) = 0;

  virtual void enterFactor(FandangoParser::FactorContext *ctx) = 0;
  virtual void exitFactor(FandangoParser::FactorContext *ctx) = 0;

  virtual void enterPower(FandangoParser::PowerContext *ctx) = 0;
  virtual void exitPower(FandangoParser::PowerContext *ctx) = 0;

  virtual void enterAwait_primary(FandangoParser::Await_primaryContext *ctx) = 0;
  virtual void exitAwait_primary(FandangoParser::Await_primaryContext *ctx) = 0;

  virtual void enterPrimary(FandangoParser::PrimaryContext *ctx) = 0;
  virtual void exitPrimary(FandangoParser::PrimaryContext *ctx) = 0;

  virtual void enterSlices(FandangoParser::SlicesContext *ctx) = 0;
  virtual void exitSlices(FandangoParser::SlicesContext *ctx) = 0;

  virtual void enterSlice(FandangoParser::SliceContext *ctx) = 0;
  virtual void exitSlice(FandangoParser::SliceContext *ctx) = 0;

  virtual void enterAtom(FandangoParser::AtomContext *ctx) = 0;
  virtual void exitAtom(FandangoParser::AtomContext *ctx) = 0;

  virtual void enterGroup(FandangoParser::GroupContext *ctx) = 0;
  virtual void exitGroup(FandangoParser::GroupContext *ctx) = 0;

  virtual void enterLambdef(FandangoParser::LambdefContext *ctx) = 0;
  virtual void exitLambdef(FandangoParser::LambdefContext *ctx) = 0;

  virtual void enterLambda_params(FandangoParser::Lambda_paramsContext *ctx) = 0;
  virtual void exitLambda_params(FandangoParser::Lambda_paramsContext *ctx) = 0;

  virtual void enterLambda_parameters(FandangoParser::Lambda_parametersContext *ctx) = 0;
  virtual void exitLambda_parameters(FandangoParser::Lambda_parametersContext *ctx) = 0;

  virtual void enterLambda_slash_no_default(FandangoParser::Lambda_slash_no_defaultContext *ctx) = 0;
  virtual void exitLambda_slash_no_default(FandangoParser::Lambda_slash_no_defaultContext *ctx) = 0;

  virtual void enterLambda_slash_with_default(FandangoParser::Lambda_slash_with_defaultContext *ctx) = 0;
  virtual void exitLambda_slash_with_default(FandangoParser::Lambda_slash_with_defaultContext *ctx) = 0;

  virtual void enterLambda_star_etc(FandangoParser::Lambda_star_etcContext *ctx) = 0;
  virtual void exitLambda_star_etc(FandangoParser::Lambda_star_etcContext *ctx) = 0;

  virtual void enterLambda_kwds(FandangoParser::Lambda_kwdsContext *ctx) = 0;
  virtual void exitLambda_kwds(FandangoParser::Lambda_kwdsContext *ctx) = 0;

  virtual void enterLambda_param_no_default(FandangoParser::Lambda_param_no_defaultContext *ctx) = 0;
  virtual void exitLambda_param_no_default(FandangoParser::Lambda_param_no_defaultContext *ctx) = 0;

  virtual void enterLambda_param_with_default(FandangoParser::Lambda_param_with_defaultContext *ctx) = 0;
  virtual void exitLambda_param_with_default(FandangoParser::Lambda_param_with_defaultContext *ctx) = 0;

  virtual void enterLambda_param_maybe_default(FandangoParser::Lambda_param_maybe_defaultContext *ctx) = 0;
  virtual void exitLambda_param_maybe_default(FandangoParser::Lambda_param_maybe_defaultContext *ctx) = 0;

  virtual void enterLambda_param(FandangoParser::Lambda_paramContext *ctx) = 0;
  virtual void exitLambda_param(FandangoParser::Lambda_paramContext *ctx) = 0;

  virtual void enterFstring_middle(FandangoParser::Fstring_middleContext *ctx) = 0;
  virtual void exitFstring_middle(FandangoParser::Fstring_middleContext *ctx) = 0;

  virtual void enterFstring_replacement_field(FandangoParser::Fstring_replacement_fieldContext *ctx) = 0;
  virtual void exitFstring_replacement_field(FandangoParser::Fstring_replacement_fieldContext *ctx) = 0;

  virtual void enterFstring_conversion(FandangoParser::Fstring_conversionContext *ctx) = 0;
  virtual void exitFstring_conversion(FandangoParser::Fstring_conversionContext *ctx) = 0;

  virtual void enterFstring_full_format_spec(FandangoParser::Fstring_full_format_specContext *ctx) = 0;
  virtual void exitFstring_full_format_spec(FandangoParser::Fstring_full_format_specContext *ctx) = 0;

  virtual void enterFstring_format_spec(FandangoParser::Fstring_format_specContext *ctx) = 0;
  virtual void exitFstring_format_spec(FandangoParser::Fstring_format_specContext *ctx) = 0;

  virtual void enterFstring(FandangoParser::FstringContext *ctx) = 0;
  virtual void exitFstring(FandangoParser::FstringContext *ctx) = 0;

  virtual void enterString(FandangoParser::StringContext *ctx) = 0;
  virtual void exitString(FandangoParser::StringContext *ctx) = 0;

  virtual void enterStrings(FandangoParser::StringsContext *ctx) = 0;
  virtual void exitStrings(FandangoParser::StringsContext *ctx) = 0;

  virtual void enterList(FandangoParser::ListContext *ctx) = 0;
  virtual void exitList(FandangoParser::ListContext *ctx) = 0;

  virtual void enterTuple(FandangoParser::TupleContext *ctx) = 0;
  virtual void exitTuple(FandangoParser::TupleContext *ctx) = 0;

  virtual void enterSet(FandangoParser::SetContext *ctx) = 0;
  virtual void exitSet(FandangoParser::SetContext *ctx) = 0;

  virtual void enterDict(FandangoParser::DictContext *ctx) = 0;
  virtual void exitDict(FandangoParser::DictContext *ctx) = 0;

  virtual void enterDouble_starred_kvpairs(FandangoParser::Double_starred_kvpairsContext *ctx) = 0;
  virtual void exitDouble_starred_kvpairs(FandangoParser::Double_starred_kvpairsContext *ctx) = 0;

  virtual void enterDouble_starred_kvpair(FandangoParser::Double_starred_kvpairContext *ctx) = 0;
  virtual void exitDouble_starred_kvpair(FandangoParser::Double_starred_kvpairContext *ctx) = 0;

  virtual void enterKvpair(FandangoParser::KvpairContext *ctx) = 0;
  virtual void exitKvpair(FandangoParser::KvpairContext *ctx) = 0;

  virtual void enterFor_if_clauses(FandangoParser::For_if_clausesContext *ctx) = 0;
  virtual void exitFor_if_clauses(FandangoParser::For_if_clausesContext *ctx) = 0;

  virtual void enterFor_if_clause(FandangoParser::For_if_clauseContext *ctx) = 0;
  virtual void exitFor_if_clause(FandangoParser::For_if_clauseContext *ctx) = 0;

  virtual void enterListcomp(FandangoParser::ListcompContext *ctx) = 0;
  virtual void exitListcomp(FandangoParser::ListcompContext *ctx) = 0;

  virtual void enterSetcomp(FandangoParser::SetcompContext *ctx) = 0;
  virtual void exitSetcomp(FandangoParser::SetcompContext *ctx) = 0;

  virtual void enterGenexp(FandangoParser::GenexpContext *ctx) = 0;
  virtual void exitGenexp(FandangoParser::GenexpContext *ctx) = 0;

  virtual void enterDictcomp(FandangoParser::DictcompContext *ctx) = 0;
  virtual void exitDictcomp(FandangoParser::DictcompContext *ctx) = 0;

  virtual void enterArguments(FandangoParser::ArgumentsContext *ctx) = 0;
  virtual void exitArguments(FandangoParser::ArgumentsContext *ctx) = 0;

  virtual void enterArgs(FandangoParser::ArgsContext *ctx) = 0;
  virtual void exitArgs(FandangoParser::ArgsContext *ctx) = 0;

  virtual void enterArg(FandangoParser::ArgContext *ctx) = 0;
  virtual void exitArg(FandangoParser::ArgContext *ctx) = 0;

  virtual void enterKwargs(FandangoParser::KwargsContext *ctx) = 0;
  virtual void exitKwargs(FandangoParser::KwargsContext *ctx) = 0;

  virtual void enterStarred_expression(FandangoParser::Starred_expressionContext *ctx) = 0;
  virtual void exitStarred_expression(FandangoParser::Starred_expressionContext *ctx) = 0;

  virtual void enterKwarg_or_starred(FandangoParser::Kwarg_or_starredContext *ctx) = 0;
  virtual void exitKwarg_or_starred(FandangoParser::Kwarg_or_starredContext *ctx) = 0;

  virtual void enterKwarg_or_double_starred(FandangoParser::Kwarg_or_double_starredContext *ctx) = 0;
  virtual void exitKwarg_or_double_starred(FandangoParser::Kwarg_or_double_starredContext *ctx) = 0;

  virtual void enterStar_targets(FandangoParser::Star_targetsContext *ctx) = 0;
  virtual void exitStar_targets(FandangoParser::Star_targetsContext *ctx) = 0;

  virtual void enterStar_targets_list_seq(FandangoParser::Star_targets_list_seqContext *ctx) = 0;
  virtual void exitStar_targets_list_seq(FandangoParser::Star_targets_list_seqContext *ctx) = 0;

  virtual void enterStar_targets_tuple_seq(FandangoParser::Star_targets_tuple_seqContext *ctx) = 0;
  virtual void exitStar_targets_tuple_seq(FandangoParser::Star_targets_tuple_seqContext *ctx) = 0;

  virtual void enterStar_target(FandangoParser::Star_targetContext *ctx) = 0;
  virtual void exitStar_target(FandangoParser::Star_targetContext *ctx) = 0;

  virtual void enterTarget_with_star_atom(FandangoParser::Target_with_star_atomContext *ctx) = 0;
  virtual void exitTarget_with_star_atom(FandangoParser::Target_with_star_atomContext *ctx) = 0;

  virtual void enterStar_atom(FandangoParser::Star_atomContext *ctx) = 0;
  virtual void exitStar_atom(FandangoParser::Star_atomContext *ctx) = 0;

  virtual void enterSingle_target(FandangoParser::Single_targetContext *ctx) = 0;
  virtual void exitSingle_target(FandangoParser::Single_targetContext *ctx) = 0;

  virtual void enterSingle_subscript_attribute_target(FandangoParser::Single_subscript_attribute_targetContext *ctx) = 0;
  virtual void exitSingle_subscript_attribute_target(FandangoParser::Single_subscript_attribute_targetContext *ctx) = 0;

  virtual void enterT_primary(FandangoParser::T_primaryContext *ctx) = 0;
  virtual void exitT_primary(FandangoParser::T_primaryContext *ctx) = 0;

  virtual void enterDel_targets(FandangoParser::Del_targetsContext *ctx) = 0;
  virtual void exitDel_targets(FandangoParser::Del_targetsContext *ctx) = 0;

  virtual void enterDel_target(FandangoParser::Del_targetContext *ctx) = 0;
  virtual void exitDel_target(FandangoParser::Del_targetContext *ctx) = 0;

  virtual void enterDel_t_atom(FandangoParser::Del_t_atomContext *ctx) = 0;
  virtual void exitDel_t_atom(FandangoParser::Del_t_atomContext *ctx) = 0;

  virtual void enterType_expressions(FandangoParser::Type_expressionsContext *ctx) = 0;
  virtual void exitType_expressions(FandangoParser::Type_expressionsContext *ctx) = 0;

  virtual void enterFunc_type_comment(FandangoParser::Func_type_commentContext *ctx) = 0;
  virtual void exitFunc_type_comment(FandangoParser::Func_type_commentContext *ctx) = 0;


};

