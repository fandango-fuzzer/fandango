
// Generated from language/FandangoParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "FandangoParserListener.h"


/**
 * This class provides an empty implementation of FandangoParserListener,
 * which can be extended to create a listener which only needs to handle a subset
 * of the available methods.
 */
class  FandangoParserBaseListener : public FandangoParserListener {
public:

  virtual void enterFandango(FandangoParser::FandangoContext * /*ctx*/) override { }
  virtual void exitFandango(FandangoParser::FandangoContext * /*ctx*/) override { }

  virtual void enterProgram(FandangoParser::ProgramContext * /*ctx*/) override { }
  virtual void exitProgram(FandangoParser::ProgramContext * /*ctx*/) override { }

  virtual void enterStatement(FandangoParser::StatementContext * /*ctx*/) override { }
  virtual void exitStatement(FandangoParser::StatementContext * /*ctx*/) override { }

  virtual void enterProduction(FandangoParser::ProductionContext * /*ctx*/) override { }
  virtual void exitProduction(FandangoParser::ProductionContext * /*ctx*/) override { }

  virtual void enterAlternative(FandangoParser::AlternativeContext * /*ctx*/) override { }
  virtual void exitAlternative(FandangoParser::AlternativeContext * /*ctx*/) override { }

  virtual void enterConcatenation(FandangoParser::ConcatenationContext * /*ctx*/) override { }
  virtual void exitConcatenation(FandangoParser::ConcatenationContext * /*ctx*/) override { }

  virtual void enterOperator(FandangoParser::OperatorContext * /*ctx*/) override { }
  virtual void exitOperator(FandangoParser::OperatorContext * /*ctx*/) override { }

  virtual void enterKleene(FandangoParser::KleeneContext * /*ctx*/) override { }
  virtual void exitKleene(FandangoParser::KleeneContext * /*ctx*/) override { }

  virtual void enterPlus(FandangoParser::PlusContext * /*ctx*/) override { }
  virtual void exitPlus(FandangoParser::PlusContext * /*ctx*/) override { }

  virtual void enterOption(FandangoParser::OptionContext * /*ctx*/) override { }
  virtual void exitOption(FandangoParser::OptionContext * /*ctx*/) override { }

  virtual void enterRepeat(FandangoParser::RepeatContext * /*ctx*/) override { }
  virtual void exitRepeat(FandangoParser::RepeatContext * /*ctx*/) override { }

  virtual void enterSymbol(FandangoParser::SymbolContext * /*ctx*/) override { }
  virtual void exitSymbol(FandangoParser::SymbolContext * /*ctx*/) override { }

  virtual void enterGenerator_call(FandangoParser::Generator_callContext * /*ctx*/) override { }
  virtual void exitGenerator_call(FandangoParser::Generator_callContext * /*ctx*/) override { }

  virtual void enterChar_set(FandangoParser::Char_setContext * /*ctx*/) override { }
  virtual void exitChar_set(FandangoParser::Char_setContext * /*ctx*/) override { }

  virtual void enterConstraint(FandangoParser::ConstraintContext * /*ctx*/) override { }
  virtual void exitConstraint(FandangoParser::ConstraintContext * /*ctx*/) override { }

  virtual void enterImplies(FandangoParser::ImpliesContext * /*ctx*/) override { }
  virtual void exitImplies(FandangoParser::ImpliesContext * /*ctx*/) override { }

  virtual void enterQuantifier(FandangoParser::QuantifierContext * /*ctx*/) override { }
  virtual void exitQuantifier(FandangoParser::QuantifierContext * /*ctx*/) override { }

  virtual void enterFormula_disjunction(FandangoParser::Formula_disjunctionContext * /*ctx*/) override { }
  virtual void exitFormula_disjunction(FandangoParser::Formula_disjunctionContext * /*ctx*/) override { }

  virtual void enterFormula_conjunction(FandangoParser::Formula_conjunctionContext * /*ctx*/) override { }
  virtual void exitFormula_conjunction(FandangoParser::Formula_conjunctionContext * /*ctx*/) override { }

  virtual void enterFormula_atom(FandangoParser::Formula_atomContext * /*ctx*/) override { }
  virtual void exitFormula_atom(FandangoParser::Formula_atomContext * /*ctx*/) override { }

  virtual void enterFormula_comparison(FandangoParser::Formula_comparisonContext * /*ctx*/) override { }
  virtual void exitFormula_comparison(FandangoParser::Formula_comparisonContext * /*ctx*/) override { }

  virtual void enterExpr(FandangoParser::ExprContext * /*ctx*/) override { }
  virtual void exitExpr(FandangoParser::ExprContext * /*ctx*/) override { }

  virtual void enterSelector_length(FandangoParser::Selector_lengthContext * /*ctx*/) override { }
  virtual void exitSelector_length(FandangoParser::Selector_lengthContext * /*ctx*/) override { }

  virtual void enterSelector(FandangoParser::SelectorContext * /*ctx*/) override { }
  virtual void exitSelector(FandangoParser::SelectorContext * /*ctx*/) override { }

  virtual void enterSelection(FandangoParser::SelectionContext * /*ctx*/) override { }
  virtual void exitSelection(FandangoParser::SelectionContext * /*ctx*/) override { }

  virtual void enterBase_selection(FandangoParser::Base_selectionContext * /*ctx*/) override { }
  virtual void exitBase_selection(FandangoParser::Base_selectionContext * /*ctx*/) override { }

  virtual void enterRs_pairs(FandangoParser::Rs_pairsContext * /*ctx*/) override { }
  virtual void exitRs_pairs(FandangoParser::Rs_pairsContext * /*ctx*/) override { }

  virtual void enterRs_pair(FandangoParser::Rs_pairContext * /*ctx*/) override { }
  virtual void exitRs_pair(FandangoParser::Rs_pairContext * /*ctx*/) override { }

  virtual void enterRs_slices(FandangoParser::Rs_slicesContext * /*ctx*/) override { }
  virtual void exitRs_slices(FandangoParser::Rs_slicesContext * /*ctx*/) override { }

  virtual void enterRs_slice(FandangoParser::Rs_sliceContext * /*ctx*/) override { }
  virtual void exitRs_slice(FandangoParser::Rs_sliceContext * /*ctx*/) override { }

  virtual void enterPython(FandangoParser::PythonContext * /*ctx*/) override { }
  virtual void exitPython(FandangoParser::PythonContext * /*ctx*/) override { }

  virtual void enterPython_tag(FandangoParser::Python_tagContext * /*ctx*/) override { }
  virtual void exitPython_tag(FandangoParser::Python_tagContext * /*ctx*/) override { }

  virtual void enterPython_file(FandangoParser::Python_fileContext * /*ctx*/) override { }
  virtual void exitPython_file(FandangoParser::Python_fileContext * /*ctx*/) override { }

  virtual void enterInteractive(FandangoParser::InteractiveContext * /*ctx*/) override { }
  virtual void exitInteractive(FandangoParser::InteractiveContext * /*ctx*/) override { }

  virtual void enterEval(FandangoParser::EvalContext * /*ctx*/) override { }
  virtual void exitEval(FandangoParser::EvalContext * /*ctx*/) override { }

  virtual void enterFunc_type(FandangoParser::Func_typeContext * /*ctx*/) override { }
  virtual void exitFunc_type(FandangoParser::Func_typeContext * /*ctx*/) override { }

  virtual void enterStatements(FandangoParser::StatementsContext * /*ctx*/) override { }
  virtual void exitStatements(FandangoParser::StatementsContext * /*ctx*/) override { }

  virtual void enterStmt(FandangoParser::StmtContext * /*ctx*/) override { }
  virtual void exitStmt(FandangoParser::StmtContext * /*ctx*/) override { }

  virtual void enterStatement_newline(FandangoParser::Statement_newlineContext * /*ctx*/) override { }
  virtual void exitStatement_newline(FandangoParser::Statement_newlineContext * /*ctx*/) override { }

  virtual void enterSimple_stmts(FandangoParser::Simple_stmtsContext * /*ctx*/) override { }
  virtual void exitSimple_stmts(FandangoParser::Simple_stmtsContext * /*ctx*/) override { }

  virtual void enterSimple_stmt(FandangoParser::Simple_stmtContext * /*ctx*/) override { }
  virtual void exitSimple_stmt(FandangoParser::Simple_stmtContext * /*ctx*/) override { }

  virtual void enterCompound_stmt(FandangoParser::Compound_stmtContext * /*ctx*/) override { }
  virtual void exitCompound_stmt(FandangoParser::Compound_stmtContext * /*ctx*/) override { }

  virtual void enterAssignment(FandangoParser::AssignmentContext * /*ctx*/) override { }
  virtual void exitAssignment(FandangoParser::AssignmentContext * /*ctx*/) override { }

  virtual void enterAnnotated_rhs(FandangoParser::Annotated_rhsContext * /*ctx*/) override { }
  virtual void exitAnnotated_rhs(FandangoParser::Annotated_rhsContext * /*ctx*/) override { }

  virtual void enterAugassign(FandangoParser::AugassignContext * /*ctx*/) override { }
  virtual void exitAugassign(FandangoParser::AugassignContext * /*ctx*/) override { }

  virtual void enterReturn_stmt(FandangoParser::Return_stmtContext * /*ctx*/) override { }
  virtual void exitReturn_stmt(FandangoParser::Return_stmtContext * /*ctx*/) override { }

  virtual void enterRaise_stmt(FandangoParser::Raise_stmtContext * /*ctx*/) override { }
  virtual void exitRaise_stmt(FandangoParser::Raise_stmtContext * /*ctx*/) override { }

  virtual void enterGlobal_stmt(FandangoParser::Global_stmtContext * /*ctx*/) override { }
  virtual void exitGlobal_stmt(FandangoParser::Global_stmtContext * /*ctx*/) override { }

  virtual void enterNonlocal_stmt(FandangoParser::Nonlocal_stmtContext * /*ctx*/) override { }
  virtual void exitNonlocal_stmt(FandangoParser::Nonlocal_stmtContext * /*ctx*/) override { }

  virtual void enterDel_stmt(FandangoParser::Del_stmtContext * /*ctx*/) override { }
  virtual void exitDel_stmt(FandangoParser::Del_stmtContext * /*ctx*/) override { }

  virtual void enterYield_stmt(FandangoParser::Yield_stmtContext * /*ctx*/) override { }
  virtual void exitYield_stmt(FandangoParser::Yield_stmtContext * /*ctx*/) override { }

  virtual void enterAssert_stmt(FandangoParser::Assert_stmtContext * /*ctx*/) override { }
  virtual void exitAssert_stmt(FandangoParser::Assert_stmtContext * /*ctx*/) override { }

  virtual void enterImport_stmt(FandangoParser::Import_stmtContext * /*ctx*/) override { }
  virtual void exitImport_stmt(FandangoParser::Import_stmtContext * /*ctx*/) override { }

  virtual void enterImport_name(FandangoParser::Import_nameContext * /*ctx*/) override { }
  virtual void exitImport_name(FandangoParser::Import_nameContext * /*ctx*/) override { }

  virtual void enterImport_from(FandangoParser::Import_fromContext * /*ctx*/) override { }
  virtual void exitImport_from(FandangoParser::Import_fromContext * /*ctx*/) override { }

  virtual void enterImport_from_targets(FandangoParser::Import_from_targetsContext * /*ctx*/) override { }
  virtual void exitImport_from_targets(FandangoParser::Import_from_targetsContext * /*ctx*/) override { }

  virtual void enterImport_from_as_names(FandangoParser::Import_from_as_namesContext * /*ctx*/) override { }
  virtual void exitImport_from_as_names(FandangoParser::Import_from_as_namesContext * /*ctx*/) override { }

  virtual void enterImport_from_as_name(FandangoParser::Import_from_as_nameContext * /*ctx*/) override { }
  virtual void exitImport_from_as_name(FandangoParser::Import_from_as_nameContext * /*ctx*/) override { }

  virtual void enterDotted_as_names(FandangoParser::Dotted_as_namesContext * /*ctx*/) override { }
  virtual void exitDotted_as_names(FandangoParser::Dotted_as_namesContext * /*ctx*/) override { }

  virtual void enterDotted_as_name(FandangoParser::Dotted_as_nameContext * /*ctx*/) override { }
  virtual void exitDotted_as_name(FandangoParser::Dotted_as_nameContext * /*ctx*/) override { }

  virtual void enterDotted_name(FandangoParser::Dotted_nameContext * /*ctx*/) override { }
  virtual void exitDotted_name(FandangoParser::Dotted_nameContext * /*ctx*/) override { }

  virtual void enterBlock(FandangoParser::BlockContext * /*ctx*/) override { }
  virtual void exitBlock(FandangoParser::BlockContext * /*ctx*/) override { }

  virtual void enterDecorators(FandangoParser::DecoratorsContext * /*ctx*/) override { }
  virtual void exitDecorators(FandangoParser::DecoratorsContext * /*ctx*/) override { }

  virtual void enterClass_def(FandangoParser::Class_defContext * /*ctx*/) override { }
  virtual void exitClass_def(FandangoParser::Class_defContext * /*ctx*/) override { }

  virtual void enterClass_def_raw(FandangoParser::Class_def_rawContext * /*ctx*/) override { }
  virtual void exitClass_def_raw(FandangoParser::Class_def_rawContext * /*ctx*/) override { }

  virtual void enterFunction_def(FandangoParser::Function_defContext * /*ctx*/) override { }
  virtual void exitFunction_def(FandangoParser::Function_defContext * /*ctx*/) override { }

  virtual void enterFunction_def_raw(FandangoParser::Function_def_rawContext * /*ctx*/) override { }
  virtual void exitFunction_def_raw(FandangoParser::Function_def_rawContext * /*ctx*/) override { }

  virtual void enterParams(FandangoParser::ParamsContext * /*ctx*/) override { }
  virtual void exitParams(FandangoParser::ParamsContext * /*ctx*/) override { }

  virtual void enterParameters(FandangoParser::ParametersContext * /*ctx*/) override { }
  virtual void exitParameters(FandangoParser::ParametersContext * /*ctx*/) override { }

  virtual void enterSlash_no_default(FandangoParser::Slash_no_defaultContext * /*ctx*/) override { }
  virtual void exitSlash_no_default(FandangoParser::Slash_no_defaultContext * /*ctx*/) override { }

  virtual void enterSlash_with_default(FandangoParser::Slash_with_defaultContext * /*ctx*/) override { }
  virtual void exitSlash_with_default(FandangoParser::Slash_with_defaultContext * /*ctx*/) override { }

  virtual void enterStar_etc(FandangoParser::Star_etcContext * /*ctx*/) override { }
  virtual void exitStar_etc(FandangoParser::Star_etcContext * /*ctx*/) override { }

  virtual void enterKwds(FandangoParser::KwdsContext * /*ctx*/) override { }
  virtual void exitKwds(FandangoParser::KwdsContext * /*ctx*/) override { }

  virtual void enterParam_no_default(FandangoParser::Param_no_defaultContext * /*ctx*/) override { }
  virtual void exitParam_no_default(FandangoParser::Param_no_defaultContext * /*ctx*/) override { }

  virtual void enterParam_no_default_star_annotation(FandangoParser::Param_no_default_star_annotationContext * /*ctx*/) override { }
  virtual void exitParam_no_default_star_annotation(FandangoParser::Param_no_default_star_annotationContext * /*ctx*/) override { }

  virtual void enterParam_with_default(FandangoParser::Param_with_defaultContext * /*ctx*/) override { }
  virtual void exitParam_with_default(FandangoParser::Param_with_defaultContext * /*ctx*/) override { }

  virtual void enterParam_maybe_default(FandangoParser::Param_maybe_defaultContext * /*ctx*/) override { }
  virtual void exitParam_maybe_default(FandangoParser::Param_maybe_defaultContext * /*ctx*/) override { }

  virtual void enterParam(FandangoParser::ParamContext * /*ctx*/) override { }
  virtual void exitParam(FandangoParser::ParamContext * /*ctx*/) override { }

  virtual void enterParam_star_annotation(FandangoParser::Param_star_annotationContext * /*ctx*/) override { }
  virtual void exitParam_star_annotation(FandangoParser::Param_star_annotationContext * /*ctx*/) override { }

  virtual void enterAnnotation(FandangoParser::AnnotationContext * /*ctx*/) override { }
  virtual void exitAnnotation(FandangoParser::AnnotationContext * /*ctx*/) override { }

  virtual void enterStar_annotation(FandangoParser::Star_annotationContext * /*ctx*/) override { }
  virtual void exitStar_annotation(FandangoParser::Star_annotationContext * /*ctx*/) override { }

  virtual void enterDefault(FandangoParser::DefaultContext * /*ctx*/) override { }
  virtual void exitDefault(FandangoParser::DefaultContext * /*ctx*/) override { }

  virtual void enterIf_stmt(FandangoParser::If_stmtContext * /*ctx*/) override { }
  virtual void exitIf_stmt(FandangoParser::If_stmtContext * /*ctx*/) override { }

  virtual void enterElif_stmt(FandangoParser::Elif_stmtContext * /*ctx*/) override { }
  virtual void exitElif_stmt(FandangoParser::Elif_stmtContext * /*ctx*/) override { }

  virtual void enterElse_block(FandangoParser::Else_blockContext * /*ctx*/) override { }
  virtual void exitElse_block(FandangoParser::Else_blockContext * /*ctx*/) override { }

  virtual void enterWhile_stmt(FandangoParser::While_stmtContext * /*ctx*/) override { }
  virtual void exitWhile_stmt(FandangoParser::While_stmtContext * /*ctx*/) override { }

  virtual void enterFor_stmt(FandangoParser::For_stmtContext * /*ctx*/) override { }
  virtual void exitFor_stmt(FandangoParser::For_stmtContext * /*ctx*/) override { }

  virtual void enterWith_stmt(FandangoParser::With_stmtContext * /*ctx*/) override { }
  virtual void exitWith_stmt(FandangoParser::With_stmtContext * /*ctx*/) override { }

  virtual void enterWith_item(FandangoParser::With_itemContext * /*ctx*/) override { }
  virtual void exitWith_item(FandangoParser::With_itemContext * /*ctx*/) override { }

  virtual void enterTry_stmt(FandangoParser::Try_stmtContext * /*ctx*/) override { }
  virtual void exitTry_stmt(FandangoParser::Try_stmtContext * /*ctx*/) override { }

  virtual void enterExcept_block(FandangoParser::Except_blockContext * /*ctx*/) override { }
  virtual void exitExcept_block(FandangoParser::Except_blockContext * /*ctx*/) override { }

  virtual void enterExcept_star_block(FandangoParser::Except_star_blockContext * /*ctx*/) override { }
  virtual void exitExcept_star_block(FandangoParser::Except_star_blockContext * /*ctx*/) override { }

  virtual void enterFinally_block(FandangoParser::Finally_blockContext * /*ctx*/) override { }
  virtual void exitFinally_block(FandangoParser::Finally_blockContext * /*ctx*/) override { }

  virtual void enterMatch_stmt(FandangoParser::Match_stmtContext * /*ctx*/) override { }
  virtual void exitMatch_stmt(FandangoParser::Match_stmtContext * /*ctx*/) override { }

  virtual void enterSubject_expr(FandangoParser::Subject_exprContext * /*ctx*/) override { }
  virtual void exitSubject_expr(FandangoParser::Subject_exprContext * /*ctx*/) override { }

  virtual void enterCase_block(FandangoParser::Case_blockContext * /*ctx*/) override { }
  virtual void exitCase_block(FandangoParser::Case_blockContext * /*ctx*/) override { }

  virtual void enterGuard(FandangoParser::GuardContext * /*ctx*/) override { }
  virtual void exitGuard(FandangoParser::GuardContext * /*ctx*/) override { }

  virtual void enterPatterns(FandangoParser::PatternsContext * /*ctx*/) override { }
  virtual void exitPatterns(FandangoParser::PatternsContext * /*ctx*/) override { }

  virtual void enterPattern(FandangoParser::PatternContext * /*ctx*/) override { }
  virtual void exitPattern(FandangoParser::PatternContext * /*ctx*/) override { }

  virtual void enterAs_pattern(FandangoParser::As_patternContext * /*ctx*/) override { }
  virtual void exitAs_pattern(FandangoParser::As_patternContext * /*ctx*/) override { }

  virtual void enterOr_pattern(FandangoParser::Or_patternContext * /*ctx*/) override { }
  virtual void exitOr_pattern(FandangoParser::Or_patternContext * /*ctx*/) override { }

  virtual void enterClosed_pattern(FandangoParser::Closed_patternContext * /*ctx*/) override { }
  virtual void exitClosed_pattern(FandangoParser::Closed_patternContext * /*ctx*/) override { }

  virtual void enterLiteral_pattern(FandangoParser::Literal_patternContext * /*ctx*/) override { }
  virtual void exitLiteral_pattern(FandangoParser::Literal_patternContext * /*ctx*/) override { }

  virtual void enterLiteral_expr(FandangoParser::Literal_exprContext * /*ctx*/) override { }
  virtual void exitLiteral_expr(FandangoParser::Literal_exprContext * /*ctx*/) override { }

  virtual void enterComplex_number(FandangoParser::Complex_numberContext * /*ctx*/) override { }
  virtual void exitComplex_number(FandangoParser::Complex_numberContext * /*ctx*/) override { }

  virtual void enterSigned_number(FandangoParser::Signed_numberContext * /*ctx*/) override { }
  virtual void exitSigned_number(FandangoParser::Signed_numberContext * /*ctx*/) override { }

  virtual void enterSigned_real_number(FandangoParser::Signed_real_numberContext * /*ctx*/) override { }
  virtual void exitSigned_real_number(FandangoParser::Signed_real_numberContext * /*ctx*/) override { }

  virtual void enterReal_number(FandangoParser::Real_numberContext * /*ctx*/) override { }
  virtual void exitReal_number(FandangoParser::Real_numberContext * /*ctx*/) override { }

  virtual void enterImaginary_number(FandangoParser::Imaginary_numberContext * /*ctx*/) override { }
  virtual void exitImaginary_number(FandangoParser::Imaginary_numberContext * /*ctx*/) override { }

  virtual void enterCapture_pattern(FandangoParser::Capture_patternContext * /*ctx*/) override { }
  virtual void exitCapture_pattern(FandangoParser::Capture_patternContext * /*ctx*/) override { }

  virtual void enterPattern_capture_target(FandangoParser::Pattern_capture_targetContext * /*ctx*/) override { }
  virtual void exitPattern_capture_target(FandangoParser::Pattern_capture_targetContext * /*ctx*/) override { }

  virtual void enterWildcard_pattern(FandangoParser::Wildcard_patternContext * /*ctx*/) override { }
  virtual void exitWildcard_pattern(FandangoParser::Wildcard_patternContext * /*ctx*/) override { }

  virtual void enterValue_pattern(FandangoParser::Value_patternContext * /*ctx*/) override { }
  virtual void exitValue_pattern(FandangoParser::Value_patternContext * /*ctx*/) override { }

  virtual void enterAttr(FandangoParser::AttrContext * /*ctx*/) override { }
  virtual void exitAttr(FandangoParser::AttrContext * /*ctx*/) override { }

  virtual void enterName_or_attr(FandangoParser::Name_or_attrContext * /*ctx*/) override { }
  virtual void exitName_or_attr(FandangoParser::Name_or_attrContext * /*ctx*/) override { }

  virtual void enterGroup_pattern(FandangoParser::Group_patternContext * /*ctx*/) override { }
  virtual void exitGroup_pattern(FandangoParser::Group_patternContext * /*ctx*/) override { }

  virtual void enterSequence_pattern(FandangoParser::Sequence_patternContext * /*ctx*/) override { }
  virtual void exitSequence_pattern(FandangoParser::Sequence_patternContext * /*ctx*/) override { }

  virtual void enterOpen_sequence_pattern(FandangoParser::Open_sequence_patternContext * /*ctx*/) override { }
  virtual void exitOpen_sequence_pattern(FandangoParser::Open_sequence_patternContext * /*ctx*/) override { }

  virtual void enterMaybe_sequence_pattern(FandangoParser::Maybe_sequence_patternContext * /*ctx*/) override { }
  virtual void exitMaybe_sequence_pattern(FandangoParser::Maybe_sequence_patternContext * /*ctx*/) override { }

  virtual void enterMaybe_star_pattern(FandangoParser::Maybe_star_patternContext * /*ctx*/) override { }
  virtual void exitMaybe_star_pattern(FandangoParser::Maybe_star_patternContext * /*ctx*/) override { }

  virtual void enterStar_pattern(FandangoParser::Star_patternContext * /*ctx*/) override { }
  virtual void exitStar_pattern(FandangoParser::Star_patternContext * /*ctx*/) override { }

  virtual void enterMapping_pattern(FandangoParser::Mapping_patternContext * /*ctx*/) override { }
  virtual void exitMapping_pattern(FandangoParser::Mapping_patternContext * /*ctx*/) override { }

  virtual void enterItems_pattern(FandangoParser::Items_patternContext * /*ctx*/) override { }
  virtual void exitItems_pattern(FandangoParser::Items_patternContext * /*ctx*/) override { }

  virtual void enterKey_value_pattern(FandangoParser::Key_value_patternContext * /*ctx*/) override { }
  virtual void exitKey_value_pattern(FandangoParser::Key_value_patternContext * /*ctx*/) override { }

  virtual void enterDouble_star_pattern(FandangoParser::Double_star_patternContext * /*ctx*/) override { }
  virtual void exitDouble_star_pattern(FandangoParser::Double_star_patternContext * /*ctx*/) override { }

  virtual void enterClass_pattern(FandangoParser::Class_patternContext * /*ctx*/) override { }
  virtual void exitClass_pattern(FandangoParser::Class_patternContext * /*ctx*/) override { }

  virtual void enterPositional_patterns(FandangoParser::Positional_patternsContext * /*ctx*/) override { }
  virtual void exitPositional_patterns(FandangoParser::Positional_patternsContext * /*ctx*/) override { }

  virtual void enterKeyword_patterns(FandangoParser::Keyword_patternsContext * /*ctx*/) override { }
  virtual void exitKeyword_patterns(FandangoParser::Keyword_patternsContext * /*ctx*/) override { }

  virtual void enterKeyword_pattern(FandangoParser::Keyword_patternContext * /*ctx*/) override { }
  virtual void exitKeyword_pattern(FandangoParser::Keyword_patternContext * /*ctx*/) override { }

  virtual void enterType_alias(FandangoParser::Type_aliasContext * /*ctx*/) override { }
  virtual void exitType_alias(FandangoParser::Type_aliasContext * /*ctx*/) override { }

  virtual void enterType_params(FandangoParser::Type_paramsContext * /*ctx*/) override { }
  virtual void exitType_params(FandangoParser::Type_paramsContext * /*ctx*/) override { }

  virtual void enterType_param_seq(FandangoParser::Type_param_seqContext * /*ctx*/) override { }
  virtual void exitType_param_seq(FandangoParser::Type_param_seqContext * /*ctx*/) override { }

  virtual void enterType_param(FandangoParser::Type_paramContext * /*ctx*/) override { }
  virtual void exitType_param(FandangoParser::Type_paramContext * /*ctx*/) override { }

  virtual void enterType_param_bound(FandangoParser::Type_param_boundContext * /*ctx*/) override { }
  virtual void exitType_param_bound(FandangoParser::Type_param_boundContext * /*ctx*/) override { }

  virtual void enterExpressions(FandangoParser::ExpressionsContext * /*ctx*/) override { }
  virtual void exitExpressions(FandangoParser::ExpressionsContext * /*ctx*/) override { }

  virtual void enterExpression(FandangoParser::ExpressionContext * /*ctx*/) override { }
  virtual void exitExpression(FandangoParser::ExpressionContext * /*ctx*/) override { }

  virtual void enterYield_expr(FandangoParser::Yield_exprContext * /*ctx*/) override { }
  virtual void exitYield_expr(FandangoParser::Yield_exprContext * /*ctx*/) override { }

  virtual void enterStar_expressions(FandangoParser::Star_expressionsContext * /*ctx*/) override { }
  virtual void exitStar_expressions(FandangoParser::Star_expressionsContext * /*ctx*/) override { }

  virtual void enterStar_expression(FandangoParser::Star_expressionContext * /*ctx*/) override { }
  virtual void exitStar_expression(FandangoParser::Star_expressionContext * /*ctx*/) override { }

  virtual void enterStar_named_expressions(FandangoParser::Star_named_expressionsContext * /*ctx*/) override { }
  virtual void exitStar_named_expressions(FandangoParser::Star_named_expressionsContext * /*ctx*/) override { }

  virtual void enterStar_named_expression(FandangoParser::Star_named_expressionContext * /*ctx*/) override { }
  virtual void exitStar_named_expression(FandangoParser::Star_named_expressionContext * /*ctx*/) override { }

  virtual void enterAssignment_expression(FandangoParser::Assignment_expressionContext * /*ctx*/) override { }
  virtual void exitAssignment_expression(FandangoParser::Assignment_expressionContext * /*ctx*/) override { }

  virtual void enterNamed_expression(FandangoParser::Named_expressionContext * /*ctx*/) override { }
  virtual void exitNamed_expression(FandangoParser::Named_expressionContext * /*ctx*/) override { }

  virtual void enterDisjunction(FandangoParser::DisjunctionContext * /*ctx*/) override { }
  virtual void exitDisjunction(FandangoParser::DisjunctionContext * /*ctx*/) override { }

  virtual void enterConjunction(FandangoParser::ConjunctionContext * /*ctx*/) override { }
  virtual void exitConjunction(FandangoParser::ConjunctionContext * /*ctx*/) override { }

  virtual void enterInversion(FandangoParser::InversionContext * /*ctx*/) override { }
  virtual void exitInversion(FandangoParser::InversionContext * /*ctx*/) override { }

  virtual void enterComparison(FandangoParser::ComparisonContext * /*ctx*/) override { }
  virtual void exitComparison(FandangoParser::ComparisonContext * /*ctx*/) override { }

  virtual void enterCompare_op_bitwise_or_pair(FandangoParser::Compare_op_bitwise_or_pairContext * /*ctx*/) override { }
  virtual void exitCompare_op_bitwise_or_pair(FandangoParser::Compare_op_bitwise_or_pairContext * /*ctx*/) override { }

  virtual void enterEq_bitwise_or(FandangoParser::Eq_bitwise_orContext * /*ctx*/) override { }
  virtual void exitEq_bitwise_or(FandangoParser::Eq_bitwise_orContext * /*ctx*/) override { }

  virtual void enterNoteq_bitwise_or(FandangoParser::Noteq_bitwise_orContext * /*ctx*/) override { }
  virtual void exitNoteq_bitwise_or(FandangoParser::Noteq_bitwise_orContext * /*ctx*/) override { }

  virtual void enterLte_bitwise_or(FandangoParser::Lte_bitwise_orContext * /*ctx*/) override { }
  virtual void exitLte_bitwise_or(FandangoParser::Lte_bitwise_orContext * /*ctx*/) override { }

  virtual void enterLt_bitwise_or(FandangoParser::Lt_bitwise_orContext * /*ctx*/) override { }
  virtual void exitLt_bitwise_or(FandangoParser::Lt_bitwise_orContext * /*ctx*/) override { }

  virtual void enterGte_bitwise_or(FandangoParser::Gte_bitwise_orContext * /*ctx*/) override { }
  virtual void exitGte_bitwise_or(FandangoParser::Gte_bitwise_orContext * /*ctx*/) override { }

  virtual void enterGt_bitwise_or(FandangoParser::Gt_bitwise_orContext * /*ctx*/) override { }
  virtual void exitGt_bitwise_or(FandangoParser::Gt_bitwise_orContext * /*ctx*/) override { }

  virtual void enterNotin_bitwise_or(FandangoParser::Notin_bitwise_orContext * /*ctx*/) override { }
  virtual void exitNotin_bitwise_or(FandangoParser::Notin_bitwise_orContext * /*ctx*/) override { }

  virtual void enterIn_bitwise_or(FandangoParser::In_bitwise_orContext * /*ctx*/) override { }
  virtual void exitIn_bitwise_or(FandangoParser::In_bitwise_orContext * /*ctx*/) override { }

  virtual void enterIsnot_bitwise_or(FandangoParser::Isnot_bitwise_orContext * /*ctx*/) override { }
  virtual void exitIsnot_bitwise_or(FandangoParser::Isnot_bitwise_orContext * /*ctx*/) override { }

  virtual void enterIs_bitwise_or(FandangoParser::Is_bitwise_orContext * /*ctx*/) override { }
  virtual void exitIs_bitwise_or(FandangoParser::Is_bitwise_orContext * /*ctx*/) override { }

  virtual void enterBitwise_or(FandangoParser::Bitwise_orContext * /*ctx*/) override { }
  virtual void exitBitwise_or(FandangoParser::Bitwise_orContext * /*ctx*/) override { }

  virtual void enterBitwise_xor(FandangoParser::Bitwise_xorContext * /*ctx*/) override { }
  virtual void exitBitwise_xor(FandangoParser::Bitwise_xorContext * /*ctx*/) override { }

  virtual void enterBitwise_and(FandangoParser::Bitwise_andContext * /*ctx*/) override { }
  virtual void exitBitwise_and(FandangoParser::Bitwise_andContext * /*ctx*/) override { }

  virtual void enterShift_expr(FandangoParser::Shift_exprContext * /*ctx*/) override { }
  virtual void exitShift_expr(FandangoParser::Shift_exprContext * /*ctx*/) override { }

  virtual void enterSum(FandangoParser::SumContext * /*ctx*/) override { }
  virtual void exitSum(FandangoParser::SumContext * /*ctx*/) override { }

  virtual void enterTerm(FandangoParser::TermContext * /*ctx*/) override { }
  virtual void exitTerm(FandangoParser::TermContext * /*ctx*/) override { }

  virtual void enterFactor(FandangoParser::FactorContext * /*ctx*/) override { }
  virtual void exitFactor(FandangoParser::FactorContext * /*ctx*/) override { }

  virtual void enterPower(FandangoParser::PowerContext * /*ctx*/) override { }
  virtual void exitPower(FandangoParser::PowerContext * /*ctx*/) override { }

  virtual void enterAwait_primary(FandangoParser::Await_primaryContext * /*ctx*/) override { }
  virtual void exitAwait_primary(FandangoParser::Await_primaryContext * /*ctx*/) override { }

  virtual void enterPrimary(FandangoParser::PrimaryContext * /*ctx*/) override { }
  virtual void exitPrimary(FandangoParser::PrimaryContext * /*ctx*/) override { }

  virtual void enterSlices(FandangoParser::SlicesContext * /*ctx*/) override { }
  virtual void exitSlices(FandangoParser::SlicesContext * /*ctx*/) override { }

  virtual void enterSlice(FandangoParser::SliceContext * /*ctx*/) override { }
  virtual void exitSlice(FandangoParser::SliceContext * /*ctx*/) override { }

  virtual void enterAtom(FandangoParser::AtomContext * /*ctx*/) override { }
  virtual void exitAtom(FandangoParser::AtomContext * /*ctx*/) override { }

  virtual void enterGroup(FandangoParser::GroupContext * /*ctx*/) override { }
  virtual void exitGroup(FandangoParser::GroupContext * /*ctx*/) override { }

  virtual void enterLambdef(FandangoParser::LambdefContext * /*ctx*/) override { }
  virtual void exitLambdef(FandangoParser::LambdefContext * /*ctx*/) override { }

  virtual void enterLambda_params(FandangoParser::Lambda_paramsContext * /*ctx*/) override { }
  virtual void exitLambda_params(FandangoParser::Lambda_paramsContext * /*ctx*/) override { }

  virtual void enterLambda_parameters(FandangoParser::Lambda_parametersContext * /*ctx*/) override { }
  virtual void exitLambda_parameters(FandangoParser::Lambda_parametersContext * /*ctx*/) override { }

  virtual void enterLambda_slash_no_default(FandangoParser::Lambda_slash_no_defaultContext * /*ctx*/) override { }
  virtual void exitLambda_slash_no_default(FandangoParser::Lambda_slash_no_defaultContext * /*ctx*/) override { }

  virtual void enterLambda_slash_with_default(FandangoParser::Lambda_slash_with_defaultContext * /*ctx*/) override { }
  virtual void exitLambda_slash_with_default(FandangoParser::Lambda_slash_with_defaultContext * /*ctx*/) override { }

  virtual void enterLambda_star_etc(FandangoParser::Lambda_star_etcContext * /*ctx*/) override { }
  virtual void exitLambda_star_etc(FandangoParser::Lambda_star_etcContext * /*ctx*/) override { }

  virtual void enterLambda_kwds(FandangoParser::Lambda_kwdsContext * /*ctx*/) override { }
  virtual void exitLambda_kwds(FandangoParser::Lambda_kwdsContext * /*ctx*/) override { }

  virtual void enterLambda_param_no_default(FandangoParser::Lambda_param_no_defaultContext * /*ctx*/) override { }
  virtual void exitLambda_param_no_default(FandangoParser::Lambda_param_no_defaultContext * /*ctx*/) override { }

  virtual void enterLambda_param_with_default(FandangoParser::Lambda_param_with_defaultContext * /*ctx*/) override { }
  virtual void exitLambda_param_with_default(FandangoParser::Lambda_param_with_defaultContext * /*ctx*/) override { }

  virtual void enterLambda_param_maybe_default(FandangoParser::Lambda_param_maybe_defaultContext * /*ctx*/) override { }
  virtual void exitLambda_param_maybe_default(FandangoParser::Lambda_param_maybe_defaultContext * /*ctx*/) override { }

  virtual void enterLambda_param(FandangoParser::Lambda_paramContext * /*ctx*/) override { }
  virtual void exitLambda_param(FandangoParser::Lambda_paramContext * /*ctx*/) override { }

  virtual void enterFstring_middle(FandangoParser::Fstring_middleContext * /*ctx*/) override { }
  virtual void exitFstring_middle(FandangoParser::Fstring_middleContext * /*ctx*/) override { }

  virtual void enterFstring_replacement_field(FandangoParser::Fstring_replacement_fieldContext * /*ctx*/) override { }
  virtual void exitFstring_replacement_field(FandangoParser::Fstring_replacement_fieldContext * /*ctx*/) override { }

  virtual void enterFstring_conversion(FandangoParser::Fstring_conversionContext * /*ctx*/) override { }
  virtual void exitFstring_conversion(FandangoParser::Fstring_conversionContext * /*ctx*/) override { }

  virtual void enterFstring_full_format_spec(FandangoParser::Fstring_full_format_specContext * /*ctx*/) override { }
  virtual void exitFstring_full_format_spec(FandangoParser::Fstring_full_format_specContext * /*ctx*/) override { }

  virtual void enterFstring_format_spec(FandangoParser::Fstring_format_specContext * /*ctx*/) override { }
  virtual void exitFstring_format_spec(FandangoParser::Fstring_format_specContext * /*ctx*/) override { }

  virtual void enterFstring(FandangoParser::FstringContext * /*ctx*/) override { }
  virtual void exitFstring(FandangoParser::FstringContext * /*ctx*/) override { }

  virtual void enterString(FandangoParser::StringContext * /*ctx*/) override { }
  virtual void exitString(FandangoParser::StringContext * /*ctx*/) override { }

  virtual void enterStrings(FandangoParser::StringsContext * /*ctx*/) override { }
  virtual void exitStrings(FandangoParser::StringsContext * /*ctx*/) override { }

  virtual void enterList(FandangoParser::ListContext * /*ctx*/) override { }
  virtual void exitList(FandangoParser::ListContext * /*ctx*/) override { }

  virtual void enterTuple(FandangoParser::TupleContext * /*ctx*/) override { }
  virtual void exitTuple(FandangoParser::TupleContext * /*ctx*/) override { }

  virtual void enterSet(FandangoParser::SetContext * /*ctx*/) override { }
  virtual void exitSet(FandangoParser::SetContext * /*ctx*/) override { }

  virtual void enterDict(FandangoParser::DictContext * /*ctx*/) override { }
  virtual void exitDict(FandangoParser::DictContext * /*ctx*/) override { }

  virtual void enterDouble_starred_kvpairs(FandangoParser::Double_starred_kvpairsContext * /*ctx*/) override { }
  virtual void exitDouble_starred_kvpairs(FandangoParser::Double_starred_kvpairsContext * /*ctx*/) override { }

  virtual void enterDouble_starred_kvpair(FandangoParser::Double_starred_kvpairContext * /*ctx*/) override { }
  virtual void exitDouble_starred_kvpair(FandangoParser::Double_starred_kvpairContext * /*ctx*/) override { }

  virtual void enterKvpair(FandangoParser::KvpairContext * /*ctx*/) override { }
  virtual void exitKvpair(FandangoParser::KvpairContext * /*ctx*/) override { }

  virtual void enterFor_if_clauses(FandangoParser::For_if_clausesContext * /*ctx*/) override { }
  virtual void exitFor_if_clauses(FandangoParser::For_if_clausesContext * /*ctx*/) override { }

  virtual void enterFor_if_clause(FandangoParser::For_if_clauseContext * /*ctx*/) override { }
  virtual void exitFor_if_clause(FandangoParser::For_if_clauseContext * /*ctx*/) override { }

  virtual void enterListcomp(FandangoParser::ListcompContext * /*ctx*/) override { }
  virtual void exitListcomp(FandangoParser::ListcompContext * /*ctx*/) override { }

  virtual void enterSetcomp(FandangoParser::SetcompContext * /*ctx*/) override { }
  virtual void exitSetcomp(FandangoParser::SetcompContext * /*ctx*/) override { }

  virtual void enterGenexp(FandangoParser::GenexpContext * /*ctx*/) override { }
  virtual void exitGenexp(FandangoParser::GenexpContext * /*ctx*/) override { }

  virtual void enterDictcomp(FandangoParser::DictcompContext * /*ctx*/) override { }
  virtual void exitDictcomp(FandangoParser::DictcompContext * /*ctx*/) override { }

  virtual void enterArguments(FandangoParser::ArgumentsContext * /*ctx*/) override { }
  virtual void exitArguments(FandangoParser::ArgumentsContext * /*ctx*/) override { }

  virtual void enterArgs(FandangoParser::ArgsContext * /*ctx*/) override { }
  virtual void exitArgs(FandangoParser::ArgsContext * /*ctx*/) override { }

  virtual void enterArg(FandangoParser::ArgContext * /*ctx*/) override { }
  virtual void exitArg(FandangoParser::ArgContext * /*ctx*/) override { }

  virtual void enterKwargs(FandangoParser::KwargsContext * /*ctx*/) override { }
  virtual void exitKwargs(FandangoParser::KwargsContext * /*ctx*/) override { }

  virtual void enterStarred_expression(FandangoParser::Starred_expressionContext * /*ctx*/) override { }
  virtual void exitStarred_expression(FandangoParser::Starred_expressionContext * /*ctx*/) override { }

  virtual void enterKwarg_or_starred(FandangoParser::Kwarg_or_starredContext * /*ctx*/) override { }
  virtual void exitKwarg_or_starred(FandangoParser::Kwarg_or_starredContext * /*ctx*/) override { }

  virtual void enterKwarg_or_double_starred(FandangoParser::Kwarg_or_double_starredContext * /*ctx*/) override { }
  virtual void exitKwarg_or_double_starred(FandangoParser::Kwarg_or_double_starredContext * /*ctx*/) override { }

  virtual void enterStar_targets(FandangoParser::Star_targetsContext * /*ctx*/) override { }
  virtual void exitStar_targets(FandangoParser::Star_targetsContext * /*ctx*/) override { }

  virtual void enterStar_targets_list_seq(FandangoParser::Star_targets_list_seqContext * /*ctx*/) override { }
  virtual void exitStar_targets_list_seq(FandangoParser::Star_targets_list_seqContext * /*ctx*/) override { }

  virtual void enterStar_targets_tuple_seq(FandangoParser::Star_targets_tuple_seqContext * /*ctx*/) override { }
  virtual void exitStar_targets_tuple_seq(FandangoParser::Star_targets_tuple_seqContext * /*ctx*/) override { }

  virtual void enterStar_target(FandangoParser::Star_targetContext * /*ctx*/) override { }
  virtual void exitStar_target(FandangoParser::Star_targetContext * /*ctx*/) override { }

  virtual void enterTarget_with_star_atom(FandangoParser::Target_with_star_atomContext * /*ctx*/) override { }
  virtual void exitTarget_with_star_atom(FandangoParser::Target_with_star_atomContext * /*ctx*/) override { }

  virtual void enterStar_atom(FandangoParser::Star_atomContext * /*ctx*/) override { }
  virtual void exitStar_atom(FandangoParser::Star_atomContext * /*ctx*/) override { }

  virtual void enterSingle_target(FandangoParser::Single_targetContext * /*ctx*/) override { }
  virtual void exitSingle_target(FandangoParser::Single_targetContext * /*ctx*/) override { }

  virtual void enterSingle_subscript_attribute_target(FandangoParser::Single_subscript_attribute_targetContext * /*ctx*/) override { }
  virtual void exitSingle_subscript_attribute_target(FandangoParser::Single_subscript_attribute_targetContext * /*ctx*/) override { }

  virtual void enterT_primary(FandangoParser::T_primaryContext * /*ctx*/) override { }
  virtual void exitT_primary(FandangoParser::T_primaryContext * /*ctx*/) override { }

  virtual void enterDel_targets(FandangoParser::Del_targetsContext * /*ctx*/) override { }
  virtual void exitDel_targets(FandangoParser::Del_targetsContext * /*ctx*/) override { }

  virtual void enterDel_target(FandangoParser::Del_targetContext * /*ctx*/) override { }
  virtual void exitDel_target(FandangoParser::Del_targetContext * /*ctx*/) override { }

  virtual void enterDel_t_atom(FandangoParser::Del_t_atomContext * /*ctx*/) override { }
  virtual void exitDel_t_atom(FandangoParser::Del_t_atomContext * /*ctx*/) override { }

  virtual void enterType_expressions(FandangoParser::Type_expressionsContext * /*ctx*/) override { }
  virtual void exitType_expressions(FandangoParser::Type_expressionsContext * /*ctx*/) override { }

  virtual void enterFunc_type_comment(FandangoParser::Func_type_commentContext * /*ctx*/) override { }
  virtual void exitFunc_type_comment(FandangoParser::Func_type_commentContext * /*ctx*/) override { }


  virtual void enterEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void exitEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void visitTerminal(antlr4::tree::TerminalNode * /*node*/) override { }
  virtual void visitErrorNode(antlr4::tree::ErrorNode * /*node*/) override { }

};

