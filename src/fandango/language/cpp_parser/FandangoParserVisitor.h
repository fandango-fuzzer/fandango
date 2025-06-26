
// Generated from language/FandangoParser.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "FandangoParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by FandangoParser.
 */
class  FandangoParserVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by FandangoParser.
   */
    virtual std::any visitFandango(FandangoParser::FandangoContext *context) = 0;

    virtual std::any visitProgram(FandangoParser::ProgramContext *context) = 0;

    virtual std::any visitStatement(FandangoParser::StatementContext *context) = 0;

    virtual std::any visitProduction(FandangoParser::ProductionContext *context) = 0;

    virtual std::any visitAlternative(FandangoParser::AlternativeContext *context) = 0;

    virtual std::any visitConcatenation(FandangoParser::ConcatenationContext *context) = 0;

    virtual std::any visitOperator(FandangoParser::OperatorContext *context) = 0;

    virtual std::any visitKleene(FandangoParser::KleeneContext *context) = 0;

    virtual std::any visitPlus(FandangoParser::PlusContext *context) = 0;

    virtual std::any visitOption(FandangoParser::OptionContext *context) = 0;

    virtual std::any visitRepeat(FandangoParser::RepeatContext *context) = 0;

    virtual std::any visitSymbol(FandangoParser::SymbolContext *context) = 0;

    virtual std::any visitNonterminal_right(FandangoParser::Nonterminal_rightContext *context) = 0;

    virtual std::any visitNonterminal(FandangoParser::NonterminalContext *context) = 0;

    virtual std::any visitGenerator_call(FandangoParser::Generator_callContext *context) = 0;

    virtual std::any visitChar_set(FandangoParser::Char_setContext *context) = 0;

    virtual std::any visitConstraint(FandangoParser::ConstraintContext *context) = 0;

    virtual std::any visitImplies(FandangoParser::ImpliesContext *context) = 0;

    virtual std::any visitQuantifier(FandangoParser::QuantifierContext *context) = 0;

    virtual std::any visitQuantifier_in_line(FandangoParser::Quantifier_in_lineContext *context) = 0;

    virtual std::any visitFormula_disjunction(FandangoParser::Formula_disjunctionContext *context) = 0;

    virtual std::any visitFormula_conjunction(FandangoParser::Formula_conjunctionContext *context) = 0;

    virtual std::any visitFormula_atom(FandangoParser::Formula_atomContext *context) = 0;

    virtual std::any visitFormula_comparison(FandangoParser::Formula_comparisonContext *context) = 0;

    virtual std::any visitExpr(FandangoParser::ExprContext *context) = 0;

    virtual std::any visitSelector_length(FandangoParser::Selector_lengthContext *context) = 0;

    virtual std::any visitStar_selection_or_dot_selection(FandangoParser::Star_selection_or_dot_selectionContext *context) = 0;

    virtual std::any visitStar_selection(FandangoParser::Star_selectionContext *context) = 0;

    virtual std::any visitDot_selection(FandangoParser::Dot_selectionContext *context) = 0;

    virtual std::any visitSelection(FandangoParser::SelectionContext *context) = 0;

    virtual std::any visitBase_selection(FandangoParser::Base_selectionContext *context) = 0;

    virtual std::any visitRs_pairs(FandangoParser::Rs_pairsContext *context) = 0;

    virtual std::any visitRs_pair(FandangoParser::Rs_pairContext *context) = 0;

    virtual std::any visitRs_slices(FandangoParser::Rs_slicesContext *context) = 0;

    virtual std::any visitRs_slice(FandangoParser::Rs_sliceContext *context) = 0;

    virtual std::any visitPython(FandangoParser::PythonContext *context) = 0;

    virtual std::any visitPython_tag(FandangoParser::Python_tagContext *context) = 0;

    virtual std::any visitPython_file(FandangoParser::Python_fileContext *context) = 0;

    virtual std::any visitInteractive(FandangoParser::InteractiveContext *context) = 0;

    virtual std::any visitEval(FandangoParser::EvalContext *context) = 0;

    virtual std::any visitFunc_type(FandangoParser::Func_typeContext *context) = 0;

    virtual std::any visitStatements(FandangoParser::StatementsContext *context) = 0;

    virtual std::any visitStmt(FandangoParser::StmtContext *context) = 0;

    virtual std::any visitStatement_newline(FandangoParser::Statement_newlineContext *context) = 0;

    virtual std::any visitSimple_stmts(FandangoParser::Simple_stmtsContext *context) = 0;

    virtual std::any visitSimple_stmt(FandangoParser::Simple_stmtContext *context) = 0;

    virtual std::any visitCompound_stmt(FandangoParser::Compound_stmtContext *context) = 0;

    virtual std::any visitAssignment(FandangoParser::AssignmentContext *context) = 0;

    virtual std::any visitAnnotated_rhs(FandangoParser::Annotated_rhsContext *context) = 0;

    virtual std::any visitAugassign(FandangoParser::AugassignContext *context) = 0;

    virtual std::any visitReturn_stmt(FandangoParser::Return_stmtContext *context) = 0;

    virtual std::any visitRaise_stmt(FandangoParser::Raise_stmtContext *context) = 0;

    virtual std::any visitGlobal_stmt(FandangoParser::Global_stmtContext *context) = 0;

    virtual std::any visitNonlocal_stmt(FandangoParser::Nonlocal_stmtContext *context) = 0;

    virtual std::any visitDel_stmt(FandangoParser::Del_stmtContext *context) = 0;

    virtual std::any visitYield_stmt(FandangoParser::Yield_stmtContext *context) = 0;

    virtual std::any visitAssert_stmt(FandangoParser::Assert_stmtContext *context) = 0;

    virtual std::any visitImport_stmt(FandangoParser::Import_stmtContext *context) = 0;

    virtual std::any visitImport_name(FandangoParser::Import_nameContext *context) = 0;

    virtual std::any visitImport_from(FandangoParser::Import_fromContext *context) = 0;

    virtual std::any visitImport_from_targets(FandangoParser::Import_from_targetsContext *context) = 0;

    virtual std::any visitImport_from_as_names(FandangoParser::Import_from_as_namesContext *context) = 0;

    virtual std::any visitImport_from_as_name(FandangoParser::Import_from_as_nameContext *context) = 0;

    virtual std::any visitDotted_as_names(FandangoParser::Dotted_as_namesContext *context) = 0;

    virtual std::any visitDotted_as_name(FandangoParser::Dotted_as_nameContext *context) = 0;

    virtual std::any visitDotted_name(FandangoParser::Dotted_nameContext *context) = 0;

    virtual std::any visitBlock(FandangoParser::BlockContext *context) = 0;

    virtual std::any visitDecorators(FandangoParser::DecoratorsContext *context) = 0;

    virtual std::any visitClass_def(FandangoParser::Class_defContext *context) = 0;

    virtual std::any visitClass_def_raw(FandangoParser::Class_def_rawContext *context) = 0;

    virtual std::any visitFunction_def(FandangoParser::Function_defContext *context) = 0;

    virtual std::any visitFunction_def_raw(FandangoParser::Function_def_rawContext *context) = 0;

    virtual std::any visitParams(FandangoParser::ParamsContext *context) = 0;

    virtual std::any visitParameters(FandangoParser::ParametersContext *context) = 0;

    virtual std::any visitSlash_no_default(FandangoParser::Slash_no_defaultContext *context) = 0;

    virtual std::any visitSlash_with_default(FandangoParser::Slash_with_defaultContext *context) = 0;

    virtual std::any visitStar_etc(FandangoParser::Star_etcContext *context) = 0;

    virtual std::any visitKwds(FandangoParser::KwdsContext *context) = 0;

    virtual std::any visitParam_no_default(FandangoParser::Param_no_defaultContext *context) = 0;

    virtual std::any visitParam_no_default_star_annotation(FandangoParser::Param_no_default_star_annotationContext *context) = 0;

    virtual std::any visitParam_with_default(FandangoParser::Param_with_defaultContext *context) = 0;

    virtual std::any visitParam_maybe_default(FandangoParser::Param_maybe_defaultContext *context) = 0;

    virtual std::any visitParam(FandangoParser::ParamContext *context) = 0;

    virtual std::any visitParam_star_annotation(FandangoParser::Param_star_annotationContext *context) = 0;

    virtual std::any visitAnnotation(FandangoParser::AnnotationContext *context) = 0;

    virtual std::any visitStar_annotation(FandangoParser::Star_annotationContext *context) = 0;

    virtual std::any visitDefault(FandangoParser::DefaultContext *context) = 0;

    virtual std::any visitIf_stmt(FandangoParser::If_stmtContext *context) = 0;

    virtual std::any visitElif_stmt(FandangoParser::Elif_stmtContext *context) = 0;

    virtual std::any visitElse_block(FandangoParser::Else_blockContext *context) = 0;

    virtual std::any visitWhile_stmt(FandangoParser::While_stmtContext *context) = 0;

    virtual std::any visitFor_stmt(FandangoParser::For_stmtContext *context) = 0;

    virtual std::any visitWith_stmt(FandangoParser::With_stmtContext *context) = 0;

    virtual std::any visitWith_item(FandangoParser::With_itemContext *context) = 0;

    virtual std::any visitTry_stmt(FandangoParser::Try_stmtContext *context) = 0;

    virtual std::any visitExcept_block(FandangoParser::Except_blockContext *context) = 0;

    virtual std::any visitExcept_star_block(FandangoParser::Except_star_blockContext *context) = 0;

    virtual std::any visitFinally_block(FandangoParser::Finally_blockContext *context) = 0;

    virtual std::any visitMatch_stmt(FandangoParser::Match_stmtContext *context) = 0;

    virtual std::any visitSubject_expr(FandangoParser::Subject_exprContext *context) = 0;

    virtual std::any visitCase_block(FandangoParser::Case_blockContext *context) = 0;

    virtual std::any visitGuard(FandangoParser::GuardContext *context) = 0;

    virtual std::any visitPatterns(FandangoParser::PatternsContext *context) = 0;

    virtual std::any visitPattern(FandangoParser::PatternContext *context) = 0;

    virtual std::any visitAs_pattern(FandangoParser::As_patternContext *context) = 0;

    virtual std::any visitOr_pattern(FandangoParser::Or_patternContext *context) = 0;

    virtual std::any visitClosed_pattern(FandangoParser::Closed_patternContext *context) = 0;

    virtual std::any visitLiteral_pattern(FandangoParser::Literal_patternContext *context) = 0;

    virtual std::any visitLiteral_expr(FandangoParser::Literal_exprContext *context) = 0;

    virtual std::any visitComplex_number(FandangoParser::Complex_numberContext *context) = 0;

    virtual std::any visitSigned_number(FandangoParser::Signed_numberContext *context) = 0;

    virtual std::any visitSigned_real_number(FandangoParser::Signed_real_numberContext *context) = 0;

    virtual std::any visitReal_number(FandangoParser::Real_numberContext *context) = 0;

    virtual std::any visitImaginary_number(FandangoParser::Imaginary_numberContext *context) = 0;

    virtual std::any visitCapture_pattern(FandangoParser::Capture_patternContext *context) = 0;

    virtual std::any visitPattern_capture_target(FandangoParser::Pattern_capture_targetContext *context) = 0;

    virtual std::any visitWildcard_pattern(FandangoParser::Wildcard_patternContext *context) = 0;

    virtual std::any visitValue_pattern(FandangoParser::Value_patternContext *context) = 0;

    virtual std::any visitAttr(FandangoParser::AttrContext *context) = 0;

    virtual std::any visitName_or_attr(FandangoParser::Name_or_attrContext *context) = 0;

    virtual std::any visitGroup_pattern(FandangoParser::Group_patternContext *context) = 0;

    virtual std::any visitSequence_pattern(FandangoParser::Sequence_patternContext *context) = 0;

    virtual std::any visitOpen_sequence_pattern(FandangoParser::Open_sequence_patternContext *context) = 0;

    virtual std::any visitMaybe_sequence_pattern(FandangoParser::Maybe_sequence_patternContext *context) = 0;

    virtual std::any visitMaybe_star_pattern(FandangoParser::Maybe_star_patternContext *context) = 0;

    virtual std::any visitStar_pattern(FandangoParser::Star_patternContext *context) = 0;

    virtual std::any visitMapping_pattern(FandangoParser::Mapping_patternContext *context) = 0;

    virtual std::any visitItems_pattern(FandangoParser::Items_patternContext *context) = 0;

    virtual std::any visitKey_value_pattern(FandangoParser::Key_value_patternContext *context) = 0;

    virtual std::any visitDouble_star_pattern(FandangoParser::Double_star_patternContext *context) = 0;

    virtual std::any visitClass_pattern(FandangoParser::Class_patternContext *context) = 0;

    virtual std::any visitPositional_patterns(FandangoParser::Positional_patternsContext *context) = 0;

    virtual std::any visitKeyword_patterns(FandangoParser::Keyword_patternsContext *context) = 0;

    virtual std::any visitKeyword_pattern(FandangoParser::Keyword_patternContext *context) = 0;

    virtual std::any visitType_alias(FandangoParser::Type_aliasContext *context) = 0;

    virtual std::any visitType_params(FandangoParser::Type_paramsContext *context) = 0;

    virtual std::any visitType_param_seq(FandangoParser::Type_param_seqContext *context) = 0;

    virtual std::any visitType_param(FandangoParser::Type_paramContext *context) = 0;

    virtual std::any visitType_param_bound(FandangoParser::Type_param_boundContext *context) = 0;

    virtual std::any visitExpressions(FandangoParser::ExpressionsContext *context) = 0;

    virtual std::any visitExpression(FandangoParser::ExpressionContext *context) = 0;

    virtual std::any visitYield_expr(FandangoParser::Yield_exprContext *context) = 0;

    virtual std::any visitStar_expressions(FandangoParser::Star_expressionsContext *context) = 0;

    virtual std::any visitStar_expression(FandangoParser::Star_expressionContext *context) = 0;

    virtual std::any visitStar_named_expressions(FandangoParser::Star_named_expressionsContext *context) = 0;

    virtual std::any visitStar_named_expression(FandangoParser::Star_named_expressionContext *context) = 0;

    virtual std::any visitAssignment_expression(FandangoParser::Assignment_expressionContext *context) = 0;

    virtual std::any visitNamed_expression(FandangoParser::Named_expressionContext *context) = 0;

    virtual std::any visitDisjunction(FandangoParser::DisjunctionContext *context) = 0;

    virtual std::any visitConjunction(FandangoParser::ConjunctionContext *context) = 0;

    virtual std::any visitInversion(FandangoParser::InversionContext *context) = 0;

    virtual std::any visitComparison(FandangoParser::ComparisonContext *context) = 0;

    virtual std::any visitCompare_op_bitwise_or_pair(FandangoParser::Compare_op_bitwise_or_pairContext *context) = 0;

    virtual std::any visitEq_bitwise_or(FandangoParser::Eq_bitwise_orContext *context) = 0;

    virtual std::any visitNoteq_bitwise_or(FandangoParser::Noteq_bitwise_orContext *context) = 0;

    virtual std::any visitLte_bitwise_or(FandangoParser::Lte_bitwise_orContext *context) = 0;

    virtual std::any visitLt_bitwise_or(FandangoParser::Lt_bitwise_orContext *context) = 0;

    virtual std::any visitGte_bitwise_or(FandangoParser::Gte_bitwise_orContext *context) = 0;

    virtual std::any visitGt_bitwise_or(FandangoParser::Gt_bitwise_orContext *context) = 0;

    virtual std::any visitNotin_bitwise_or(FandangoParser::Notin_bitwise_orContext *context) = 0;

    virtual std::any visitIn_bitwise_or(FandangoParser::In_bitwise_orContext *context) = 0;

    virtual std::any visitIsnot_bitwise_or(FandangoParser::Isnot_bitwise_orContext *context) = 0;

    virtual std::any visitIs_bitwise_or(FandangoParser::Is_bitwise_orContext *context) = 0;

    virtual std::any visitBitwise_or(FandangoParser::Bitwise_orContext *context) = 0;

    virtual std::any visitBitwise_xor(FandangoParser::Bitwise_xorContext *context) = 0;

    virtual std::any visitBitwise_and(FandangoParser::Bitwise_andContext *context) = 0;

    virtual std::any visitShift_expr(FandangoParser::Shift_exprContext *context) = 0;

    virtual std::any visitSum(FandangoParser::SumContext *context) = 0;

    virtual std::any visitTerm(FandangoParser::TermContext *context) = 0;

    virtual std::any visitFactor(FandangoParser::FactorContext *context) = 0;

    virtual std::any visitPower(FandangoParser::PowerContext *context) = 0;

    virtual std::any visitAwait_primary(FandangoParser::Await_primaryContext *context) = 0;

    virtual std::any visitPrimary(FandangoParser::PrimaryContext *context) = 0;

    virtual std::any visitSlices(FandangoParser::SlicesContext *context) = 0;

    virtual std::any visitSlice(FandangoParser::SliceContext *context) = 0;

    virtual std::any visitAtom(FandangoParser::AtomContext *context) = 0;

    virtual std::any visitGroup(FandangoParser::GroupContext *context) = 0;

    virtual std::any visitLambdef(FandangoParser::LambdefContext *context) = 0;

    virtual std::any visitLambda_params(FandangoParser::Lambda_paramsContext *context) = 0;

    virtual std::any visitLambda_parameters(FandangoParser::Lambda_parametersContext *context) = 0;

    virtual std::any visitLambda_slash_no_default(FandangoParser::Lambda_slash_no_defaultContext *context) = 0;

    virtual std::any visitLambda_slash_with_default(FandangoParser::Lambda_slash_with_defaultContext *context) = 0;

    virtual std::any visitLambda_star_etc(FandangoParser::Lambda_star_etcContext *context) = 0;

    virtual std::any visitLambda_kwds(FandangoParser::Lambda_kwdsContext *context) = 0;

    virtual std::any visitLambda_param_no_default(FandangoParser::Lambda_param_no_defaultContext *context) = 0;

    virtual std::any visitLambda_param_with_default(FandangoParser::Lambda_param_with_defaultContext *context) = 0;

    virtual std::any visitLambda_param_maybe_default(FandangoParser::Lambda_param_maybe_defaultContext *context) = 0;

    virtual std::any visitLambda_param(FandangoParser::Lambda_paramContext *context) = 0;

    virtual std::any visitFstring_middle_no_quote(FandangoParser::Fstring_middle_no_quoteContext *context) = 0;

    virtual std::any visitFstring_middle_no_single_quote(FandangoParser::Fstring_middle_no_single_quoteContext *context) = 0;

    virtual std::any visitFstring_middle_breaks_no_triple_quote(FandangoParser::Fstring_middle_breaks_no_triple_quoteContext *context) = 0;

    virtual std::any visitFstring_middle_breaks_no_triple_single_quote(FandangoParser::Fstring_middle_breaks_no_triple_single_quoteContext *context) = 0;

    virtual std::any visitFstring_any_no_quote(FandangoParser::Fstring_any_no_quoteContext *context) = 0;

    virtual std::any visitFstring_any_no_single_quote(FandangoParser::Fstring_any_no_single_quoteContext *context) = 0;

    virtual std::any visitFstring_middle(FandangoParser::Fstring_middleContext *context) = 0;

    virtual std::any visitFstring_any_breaks_no_triple_quote(FandangoParser::Fstring_any_breaks_no_triple_quoteContext *context) = 0;

    virtual std::any visitFstring_any_breaks_no_triple_single_quote(FandangoParser::Fstring_any_breaks_no_triple_single_quoteContext *context) = 0;

    virtual std::any visitFstring_any(FandangoParser::Fstring_anyContext *context) = 0;

    virtual std::any visitFstring_replacement_field(FandangoParser::Fstring_replacement_fieldContext *context) = 0;

    virtual std::any visitFstring_conversion(FandangoParser::Fstring_conversionContext *context) = 0;

    virtual std::any visitFstring_full_format_spec(FandangoParser::Fstring_full_format_specContext *context) = 0;

    virtual std::any visitFstring_format_spec(FandangoParser::Fstring_format_specContext *context) = 0;

    virtual std::any visitFstring(FandangoParser::FstringContext *context) = 0;

    virtual std::any visitString(FandangoParser::StringContext *context) = 0;

    virtual std::any visitStrings(FandangoParser::StringsContext *context) = 0;

    virtual std::any visitList(FandangoParser::ListContext *context) = 0;

    virtual std::any visitTuple(FandangoParser::TupleContext *context) = 0;

    virtual std::any visitSet(FandangoParser::SetContext *context) = 0;

    virtual std::any visitDict(FandangoParser::DictContext *context) = 0;

    virtual std::any visitDouble_starred_kvpairs(FandangoParser::Double_starred_kvpairsContext *context) = 0;

    virtual std::any visitDouble_starred_kvpair(FandangoParser::Double_starred_kvpairContext *context) = 0;

    virtual std::any visitKvpair(FandangoParser::KvpairContext *context) = 0;

    virtual std::any visitFor_if_clauses(FandangoParser::For_if_clausesContext *context) = 0;

    virtual std::any visitFor_if_clause(FandangoParser::For_if_clauseContext *context) = 0;

    virtual std::any visitListcomp(FandangoParser::ListcompContext *context) = 0;

    virtual std::any visitSetcomp(FandangoParser::SetcompContext *context) = 0;

    virtual std::any visitGenexp(FandangoParser::GenexpContext *context) = 0;

    virtual std::any visitDictcomp(FandangoParser::DictcompContext *context) = 0;

    virtual std::any visitArguments(FandangoParser::ArgumentsContext *context) = 0;

    virtual std::any visitArgs(FandangoParser::ArgsContext *context) = 0;

    virtual std::any visitArg(FandangoParser::ArgContext *context) = 0;

    virtual std::any visitKwargs(FandangoParser::KwargsContext *context) = 0;

    virtual std::any visitStarred_expression(FandangoParser::Starred_expressionContext *context) = 0;

    virtual std::any visitKwarg_or_starred(FandangoParser::Kwarg_or_starredContext *context) = 0;

    virtual std::any visitKwarg_or_double_starred(FandangoParser::Kwarg_or_double_starredContext *context) = 0;

    virtual std::any visitStar_targets(FandangoParser::Star_targetsContext *context) = 0;

    virtual std::any visitStar_targets_list_seq(FandangoParser::Star_targets_list_seqContext *context) = 0;

    virtual std::any visitStar_targets_tuple_seq(FandangoParser::Star_targets_tuple_seqContext *context) = 0;

    virtual std::any visitStar_target(FandangoParser::Star_targetContext *context) = 0;

    virtual std::any visitTarget_with_star_atom(FandangoParser::Target_with_star_atomContext *context) = 0;

    virtual std::any visitStar_atom(FandangoParser::Star_atomContext *context) = 0;

    virtual std::any visitSingle_target(FandangoParser::Single_targetContext *context) = 0;

    virtual std::any visitSingle_subscript_attribute_target(FandangoParser::Single_subscript_attribute_targetContext *context) = 0;

    virtual std::any visitT_primary(FandangoParser::T_primaryContext *context) = 0;

    virtual std::any visitDel_targets(FandangoParser::Del_targetsContext *context) = 0;

    virtual std::any visitDel_target(FandangoParser::Del_targetContext *context) = 0;

    virtual std::any visitDel_t_atom(FandangoParser::Del_t_atomContext *context) = 0;

    virtual std::any visitType_expressions(FandangoParser::Type_expressionsContext *context) = 0;

    virtual std::any visitFunc_type_comment(FandangoParser::Func_type_commentContext *context) = 0;

    virtual std::any visitIdentifier(FandangoParser::IdentifierContext *context) = 0;


};

