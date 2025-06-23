# Generated from language/FandangoParser.g4 by ANTLR 4.13.2
from antlr4 import *

if "." in __name__:
    from .FandangoParser import FandangoParser
else:
    from FandangoParser import FandangoParser

# This class defines a complete generic visitor for a parse tree produced by FandangoParser.


class FandangoParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FandangoParser#fandango.
    def visitFandango(self, ctx: FandangoParser.FandangoContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#program.
    def visitProgram(self, ctx: FandangoParser.ProgramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#statement.
    def visitStatement(self, ctx: FandangoParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#production.
    def visitProduction(self, ctx: FandangoParser.ProductionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#alternative.
    def visitAlternative(self, ctx: FandangoParser.AlternativeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#concatenation.
    def visitConcatenation(self, ctx: FandangoParser.ConcatenationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#operator.
    def visitOperator(self, ctx: FandangoParser.OperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#kleene.
    def visitKleene(self, ctx: FandangoParser.KleeneContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#plus.
    def visitPlus(self, ctx: FandangoParser.PlusContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#option.
    def visitOption(self, ctx: FandangoParser.OptionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#repeat.
    def visitRepeat(self, ctx: FandangoParser.RepeatContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#symbol.
    def visitSymbol(self, ctx: FandangoParser.SymbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#nonterminal_right.
    def visitNonterminal_right(self, ctx: FandangoParser.Nonterminal_rightContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#nonterminal.
    def visitNonterminal(self, ctx: FandangoParser.NonterminalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#generator_call.
    def visitGenerator_call(self, ctx: FandangoParser.Generator_callContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#char_set.
    def visitChar_set(self, ctx: FandangoParser.Char_setContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#constraint.
    def visitConstraint(self, ctx: FandangoParser.ConstraintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#implies.
    def visitImplies(self, ctx: FandangoParser.ImpliesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#quantifier.
    def visitQuantifier(self, ctx: FandangoParser.QuantifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#quantifier_in_line.
    def visitQuantifier_in_line(self, ctx: FandangoParser.Quantifier_in_lineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#formula_disjunction.
    def visitFormula_disjunction(self, ctx: FandangoParser.Formula_disjunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#formula_conjunction.
    def visitFormula_conjunction(self, ctx: FandangoParser.Formula_conjunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#formula_atom.
    def visitFormula_atom(self, ctx: FandangoParser.Formula_atomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#formula_comparison.
    def visitFormula_comparison(self, ctx: FandangoParser.Formula_comparisonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#expr.
    def visitExpr(self, ctx: FandangoParser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#selector_length.
    def visitSelector_length(self, ctx: FandangoParser.Selector_lengthContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_selection_or_dot_selection.
    def visitStar_selection_or_dot_selection(
        self, ctx: FandangoParser.Star_selection_or_dot_selectionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_selection.
    def visitStar_selection(self, ctx: FandangoParser.Star_selectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dot_selection.
    def visitDot_selection(self, ctx: FandangoParser.Dot_selectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#selection.
    def visitSelection(self, ctx: FandangoParser.SelectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#base_selection.
    def visitBase_selection(self, ctx: FandangoParser.Base_selectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#rs_pairs.
    def visitRs_pairs(self, ctx: FandangoParser.Rs_pairsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#rs_pair.
    def visitRs_pair(self, ctx: FandangoParser.Rs_pairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#rs_slices.
    def visitRs_slices(self, ctx: FandangoParser.Rs_slicesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#rs_slice.
    def visitRs_slice(self, ctx: FandangoParser.Rs_sliceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#python.
    def visitPython(self, ctx: FandangoParser.PythonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#python_tag.
    def visitPython_tag(self, ctx: FandangoParser.Python_tagContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#python_file.
    def visitPython_file(self, ctx: FandangoParser.Python_fileContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#interactive.
    def visitInteractive(self, ctx: FandangoParser.InteractiveContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#eval.
    def visitEval(self, ctx: FandangoParser.EvalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#func_type.
    def visitFunc_type(self, ctx: FandangoParser.Func_typeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#statements.
    def visitStatements(self, ctx: FandangoParser.StatementsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#stmt.
    def visitStmt(self, ctx: FandangoParser.StmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#statement_newline.
    def visitStatement_newline(self, ctx: FandangoParser.Statement_newlineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#simple_stmts.
    def visitSimple_stmts(self, ctx: FandangoParser.Simple_stmtsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#simple_stmt.
    def visitSimple_stmt(self, ctx: FandangoParser.Simple_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#compound_stmt.
    def visitCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#assignment.
    def visitAssignment(self, ctx: FandangoParser.AssignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#annotated_rhs.
    def visitAnnotated_rhs(self, ctx: FandangoParser.Annotated_rhsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#augassign.
    def visitAugassign(self, ctx: FandangoParser.AugassignContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#return_stmt.
    def visitReturn_stmt(self, ctx: FandangoParser.Return_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#raise_stmt.
    def visitRaise_stmt(self, ctx: FandangoParser.Raise_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#global_stmt.
    def visitGlobal_stmt(self, ctx: FandangoParser.Global_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#nonlocal_stmt.
    def visitNonlocal_stmt(self, ctx: FandangoParser.Nonlocal_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#del_stmt.
    def visitDel_stmt(self, ctx: FandangoParser.Del_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#yield_stmt.
    def visitYield_stmt(self, ctx: FandangoParser.Yield_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#assert_stmt.
    def visitAssert_stmt(self, ctx: FandangoParser.Assert_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#import_stmt.
    def visitImport_stmt(self, ctx: FandangoParser.Import_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#import_name.
    def visitImport_name(self, ctx: FandangoParser.Import_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#import_from.
    def visitImport_from(self, ctx: FandangoParser.Import_fromContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#import_from_targets.
    def visitImport_from_targets(self, ctx: FandangoParser.Import_from_targetsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#import_from_as_names.
    def visitImport_from_as_names(
        self, ctx: FandangoParser.Import_from_as_namesContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#import_from_as_name.
    def visitImport_from_as_name(self, ctx: FandangoParser.Import_from_as_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dotted_as_names.
    def visitDotted_as_names(self, ctx: FandangoParser.Dotted_as_namesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dotted_as_name.
    def visitDotted_as_name(self, ctx: FandangoParser.Dotted_as_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dotted_name.
    def visitDotted_name(self, ctx: FandangoParser.Dotted_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#block.
    def visitBlock(self, ctx: FandangoParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#decorators.
    def visitDecorators(self, ctx: FandangoParser.DecoratorsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#class_def.
    def visitClass_def(self, ctx: FandangoParser.Class_defContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#class_def_raw.
    def visitClass_def_raw(self, ctx: FandangoParser.Class_def_rawContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#function_def.
    def visitFunction_def(self, ctx: FandangoParser.Function_defContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#function_def_raw.
    def visitFunction_def_raw(self, ctx: FandangoParser.Function_def_rawContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#params.
    def visitParams(self, ctx: FandangoParser.ParamsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#parameters.
    def visitParameters(self, ctx: FandangoParser.ParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#slash_no_default.
    def visitSlash_no_default(self, ctx: FandangoParser.Slash_no_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#slash_with_default.
    def visitSlash_with_default(self, ctx: FandangoParser.Slash_with_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_etc.
    def visitStar_etc(self, ctx: FandangoParser.Star_etcContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#kwds.
    def visitKwds(self, ctx: FandangoParser.KwdsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#param_no_default.
    def visitParam_no_default(self, ctx: FandangoParser.Param_no_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#param_no_default_star_annotation.
    def visitParam_no_default_star_annotation(
        self, ctx: FandangoParser.Param_no_default_star_annotationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#param_with_default.
    def visitParam_with_default(self, ctx: FandangoParser.Param_with_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#param_maybe_default.
    def visitParam_maybe_default(self, ctx: FandangoParser.Param_maybe_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#param.
    def visitParam(self, ctx: FandangoParser.ParamContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#param_star_annotation.
    def visitParam_star_annotation(
        self, ctx: FandangoParser.Param_star_annotationContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#annotation.
    def visitAnnotation(self, ctx: FandangoParser.AnnotationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_annotation.
    def visitStar_annotation(self, ctx: FandangoParser.Star_annotationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#default.
    def visitDefault(self, ctx: FandangoParser.DefaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#if_stmt.
    def visitIf_stmt(self, ctx: FandangoParser.If_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#elif_stmt.
    def visitElif_stmt(self, ctx: FandangoParser.Elif_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#else_block.
    def visitElse_block(self, ctx: FandangoParser.Else_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#while_stmt.
    def visitWhile_stmt(self, ctx: FandangoParser.While_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#for_stmt.
    def visitFor_stmt(self, ctx: FandangoParser.For_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#with_stmt.
    def visitWith_stmt(self, ctx: FandangoParser.With_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#with_item.
    def visitWith_item(self, ctx: FandangoParser.With_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#try_stmt.
    def visitTry_stmt(self, ctx: FandangoParser.Try_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#except_block.
    def visitExcept_block(self, ctx: FandangoParser.Except_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#except_star_block.
    def visitExcept_star_block(self, ctx: FandangoParser.Except_star_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#finally_block.
    def visitFinally_block(self, ctx: FandangoParser.Finally_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#match_stmt.
    def visitMatch_stmt(self, ctx: FandangoParser.Match_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#subject_expr.
    def visitSubject_expr(self, ctx: FandangoParser.Subject_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#case_block.
    def visitCase_block(self, ctx: FandangoParser.Case_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#guard.
    def visitGuard(self, ctx: FandangoParser.GuardContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#patterns.
    def visitPatterns(self, ctx: FandangoParser.PatternsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#pattern.
    def visitPattern(self, ctx: FandangoParser.PatternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#as_pattern.
    def visitAs_pattern(self, ctx: FandangoParser.As_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#or_pattern.
    def visitOr_pattern(self, ctx: FandangoParser.Or_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#closed_pattern.
    def visitClosed_pattern(self, ctx: FandangoParser.Closed_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#literal_pattern.
    def visitLiteral_pattern(self, ctx: FandangoParser.Literal_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#literal_expr.
    def visitLiteral_expr(self, ctx: FandangoParser.Literal_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#complex_number.
    def visitComplex_number(self, ctx: FandangoParser.Complex_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#signed_number.
    def visitSigned_number(self, ctx: FandangoParser.Signed_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#signed_real_number.
    def visitSigned_real_number(self, ctx: FandangoParser.Signed_real_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#real_number.
    def visitReal_number(self, ctx: FandangoParser.Real_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#imaginary_number.
    def visitImaginary_number(self, ctx: FandangoParser.Imaginary_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#capture_pattern.
    def visitCapture_pattern(self, ctx: FandangoParser.Capture_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#pattern_capture_target.
    def visitPattern_capture_target(
        self, ctx: FandangoParser.Pattern_capture_targetContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#wildcard_pattern.
    def visitWildcard_pattern(self, ctx: FandangoParser.Wildcard_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#value_pattern.
    def visitValue_pattern(self, ctx: FandangoParser.Value_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#attr.
    def visitAttr(self, ctx: FandangoParser.AttrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#name_or_attr.
    def visitName_or_attr(self, ctx: FandangoParser.Name_or_attrContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#group_pattern.
    def visitGroup_pattern(self, ctx: FandangoParser.Group_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#sequence_pattern.
    def visitSequence_pattern(self, ctx: FandangoParser.Sequence_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#open_sequence_pattern.
    def visitOpen_sequence_pattern(
        self, ctx: FandangoParser.Open_sequence_patternContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#maybe_sequence_pattern.
    def visitMaybe_sequence_pattern(
        self, ctx: FandangoParser.Maybe_sequence_patternContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#maybe_star_pattern.
    def visitMaybe_star_pattern(self, ctx: FandangoParser.Maybe_star_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_pattern.
    def visitStar_pattern(self, ctx: FandangoParser.Star_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#mapping_pattern.
    def visitMapping_pattern(self, ctx: FandangoParser.Mapping_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#items_pattern.
    def visitItems_pattern(self, ctx: FandangoParser.Items_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#key_value_pattern.
    def visitKey_value_pattern(self, ctx: FandangoParser.Key_value_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#double_star_pattern.
    def visitDouble_star_pattern(self, ctx: FandangoParser.Double_star_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#class_pattern.
    def visitClass_pattern(self, ctx: FandangoParser.Class_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#positional_patterns.
    def visitPositional_patterns(self, ctx: FandangoParser.Positional_patternsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#keyword_patterns.
    def visitKeyword_patterns(self, ctx: FandangoParser.Keyword_patternsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#keyword_pattern.
    def visitKeyword_pattern(self, ctx: FandangoParser.Keyword_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#type_alias.
    def visitType_alias(self, ctx: FandangoParser.Type_aliasContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#type_params.
    def visitType_params(self, ctx: FandangoParser.Type_paramsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#type_param_seq.
    def visitType_param_seq(self, ctx: FandangoParser.Type_param_seqContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#type_param.
    def visitType_param(self, ctx: FandangoParser.Type_paramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#type_param_bound.
    def visitType_param_bound(self, ctx: FandangoParser.Type_param_boundContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#expressions.
    def visitExpressions(self, ctx: FandangoParser.ExpressionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#expression.
    def visitExpression(self, ctx: FandangoParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#yield_expr.
    def visitYield_expr(self, ctx: FandangoParser.Yield_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_expressions.
    def visitStar_expressions(self, ctx: FandangoParser.Star_expressionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_expression.
    def visitStar_expression(self, ctx: FandangoParser.Star_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_named_expressions.
    def visitStar_named_expressions(
        self, ctx: FandangoParser.Star_named_expressionsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_named_expression.
    def visitStar_named_expression(
        self, ctx: FandangoParser.Star_named_expressionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#assignment_expression.
    def visitAssignment_expression(
        self, ctx: FandangoParser.Assignment_expressionContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#named_expression.
    def visitNamed_expression(self, ctx: FandangoParser.Named_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#disjunction.
    def visitDisjunction(self, ctx: FandangoParser.DisjunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#conjunction.
    def visitConjunction(self, ctx: FandangoParser.ConjunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#inversion.
    def visitInversion(self, ctx: FandangoParser.InversionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#comparison.
    def visitComparison(self, ctx: FandangoParser.ComparisonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#compare_op_bitwise_or_pair.
    def visitCompare_op_bitwise_or_pair(
        self, ctx: FandangoParser.Compare_op_bitwise_or_pairContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#eq_bitwise_or.
    def visitEq_bitwise_or(self, ctx: FandangoParser.Eq_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#noteq_bitwise_or.
    def visitNoteq_bitwise_or(self, ctx: FandangoParser.Noteq_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lte_bitwise_or.
    def visitLte_bitwise_or(self, ctx: FandangoParser.Lte_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lt_bitwise_or.
    def visitLt_bitwise_or(self, ctx: FandangoParser.Lt_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#gte_bitwise_or.
    def visitGte_bitwise_or(self, ctx: FandangoParser.Gte_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#gt_bitwise_or.
    def visitGt_bitwise_or(self, ctx: FandangoParser.Gt_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#notin_bitwise_or.
    def visitNotin_bitwise_or(self, ctx: FandangoParser.Notin_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#in_bitwise_or.
    def visitIn_bitwise_or(self, ctx: FandangoParser.In_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#isnot_bitwise_or.
    def visitIsnot_bitwise_or(self, ctx: FandangoParser.Isnot_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#is_bitwise_or.
    def visitIs_bitwise_or(self, ctx: FandangoParser.Is_bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#bitwise_or.
    def visitBitwise_or(self, ctx: FandangoParser.Bitwise_orContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#bitwise_xor.
    def visitBitwise_xor(self, ctx: FandangoParser.Bitwise_xorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#bitwise_and.
    def visitBitwise_and(self, ctx: FandangoParser.Bitwise_andContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#shift_expr.
    def visitShift_expr(self, ctx: FandangoParser.Shift_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#sum.
    def visitSum(self, ctx: FandangoParser.SumContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#term.
    def visitTerm(self, ctx: FandangoParser.TermContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#factor.
    def visitFactor(self, ctx: FandangoParser.FactorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#power.
    def visitPower(self, ctx: FandangoParser.PowerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#await_primary.
    def visitAwait_primary(self, ctx: FandangoParser.Await_primaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#primary.
    def visitPrimary(self, ctx: FandangoParser.PrimaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#slices.
    def visitSlices(self, ctx: FandangoParser.SlicesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#slice.
    def visitSlice(self, ctx: FandangoParser.SliceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#atom.
    def visitAtom(self, ctx: FandangoParser.AtomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#group.
    def visitGroup(self, ctx: FandangoParser.GroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambdef.
    def visitLambdef(self, ctx: FandangoParser.LambdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_params.
    def visitLambda_params(self, ctx: FandangoParser.Lambda_paramsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_parameters.
    def visitLambda_parameters(self, ctx: FandangoParser.Lambda_parametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_slash_no_default.
    def visitLambda_slash_no_default(
        self, ctx: FandangoParser.Lambda_slash_no_defaultContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_slash_with_default.
    def visitLambda_slash_with_default(
        self, ctx: FandangoParser.Lambda_slash_with_defaultContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_star_etc.
    def visitLambda_star_etc(self, ctx: FandangoParser.Lambda_star_etcContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_kwds.
    def visitLambda_kwds(self, ctx: FandangoParser.Lambda_kwdsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_param_no_default.
    def visitLambda_param_no_default(
        self, ctx: FandangoParser.Lambda_param_no_defaultContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_param_with_default.
    def visitLambda_param_with_default(
        self, ctx: FandangoParser.Lambda_param_with_defaultContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_param_maybe_default.
    def visitLambda_param_maybe_default(
        self, ctx: FandangoParser.Lambda_param_maybe_defaultContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambda_param.
    def visitLambda_param(self, ctx: FandangoParser.Lambda_paramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_middle_no_quote.
    def visitFstring_middle_no_quote(
        self, ctx: FandangoParser.Fstring_middle_no_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_middle_no_single_quote.
    def visitFstring_middle_no_single_quote(
        self, ctx: FandangoParser.Fstring_middle_no_single_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_middle_breaks_no_triple_quote.
    def visitFstring_middle_breaks_no_triple_quote(
        self, ctx: FandangoParser.Fstring_middle_breaks_no_triple_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_middle_breaks_no_triple_single_quote.
    def visitFstring_middle_breaks_no_triple_single_quote(
        self, ctx: FandangoParser.Fstring_middle_breaks_no_triple_single_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_any_no_quote.
    def visitFstring_any_no_quote(
        self, ctx: FandangoParser.Fstring_any_no_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_any_no_single_quote.
    def visitFstring_any_no_single_quote(
        self, ctx: FandangoParser.Fstring_any_no_single_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_middle.
    def visitFstring_middle(self, ctx: FandangoParser.Fstring_middleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_any_breaks_no_triple_quote.
    def visitFstring_any_breaks_no_triple_quote(
        self, ctx: FandangoParser.Fstring_any_breaks_no_triple_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_any_breaks_no_triple_single_quote.
    def visitFstring_any_breaks_no_triple_single_quote(
        self, ctx: FandangoParser.Fstring_any_breaks_no_triple_single_quoteContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_any.
    def visitFstring_any(self, ctx: FandangoParser.Fstring_anyContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_replacement_field.
    def visitFstring_replacement_field(
        self, ctx: FandangoParser.Fstring_replacement_fieldContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_conversion.
    def visitFstring_conversion(self, ctx: FandangoParser.Fstring_conversionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_full_format_spec.
    def visitFstring_full_format_spec(
        self, ctx: FandangoParser.Fstring_full_format_specContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring_format_spec.
    def visitFstring_format_spec(self, ctx: FandangoParser.Fstring_format_specContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#fstring.
    def visitFstring(self, ctx: FandangoParser.FstringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#string.
    def visitString(self, ctx: FandangoParser.StringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#strings.
    def visitStrings(self, ctx: FandangoParser.StringsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#list.
    def visitList(self, ctx: FandangoParser.ListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#tuple.
    def visitTuple(self, ctx: FandangoParser.TupleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#set.
    def visitSet(self, ctx: FandangoParser.SetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dict.
    def visitDict(self, ctx: FandangoParser.DictContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#double_starred_kvpairs.
    def visitDouble_starred_kvpairs(
        self, ctx: FandangoParser.Double_starred_kvpairsContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#double_starred_kvpair.
    def visitDouble_starred_kvpair(
        self, ctx: FandangoParser.Double_starred_kvpairContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#kvpair.
    def visitKvpair(self, ctx: FandangoParser.KvpairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#for_if_clauses.
    def visitFor_if_clauses(self, ctx: FandangoParser.For_if_clausesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#for_if_clause.
    def visitFor_if_clause(self, ctx: FandangoParser.For_if_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#listcomp.
    def visitListcomp(self, ctx: FandangoParser.ListcompContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#setcomp.
    def visitSetcomp(self, ctx: FandangoParser.SetcompContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#genexp.
    def visitGenexp(self, ctx: FandangoParser.GenexpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dictcomp.
    def visitDictcomp(self, ctx: FandangoParser.DictcompContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#arguments.
    def visitArguments(self, ctx: FandangoParser.ArgumentsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#args.
    def visitArgs(self, ctx: FandangoParser.ArgsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#arg.
    def visitArg(self, ctx: FandangoParser.ArgContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#kwargs.
    def visitKwargs(self, ctx: FandangoParser.KwargsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#starred_expression.
    def visitStarred_expression(self, ctx: FandangoParser.Starred_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#kwarg_or_starred.
    def visitKwarg_or_starred(self, ctx: FandangoParser.Kwarg_or_starredContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#kwarg_or_double_starred.
    def visitKwarg_or_double_starred(
        self, ctx: FandangoParser.Kwarg_or_double_starredContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_targets.
    def visitStar_targets(self, ctx: FandangoParser.Star_targetsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_targets_list_seq.
    def visitStar_targets_list_seq(
        self, ctx: FandangoParser.Star_targets_list_seqContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_targets_tuple_seq.
    def visitStar_targets_tuple_seq(
        self, ctx: FandangoParser.Star_targets_tuple_seqContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_target.
    def visitStar_target(self, ctx: FandangoParser.Star_targetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#target_with_star_atom.
    def visitTarget_with_star_atom(
        self, ctx: FandangoParser.Target_with_star_atomContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_atom.
    def visitStar_atom(self, ctx: FandangoParser.Star_atomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#single_target.
    def visitSingle_target(self, ctx: FandangoParser.Single_targetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#single_subscript_attribute_target.
    def visitSingle_subscript_attribute_target(
        self, ctx: FandangoParser.Single_subscript_attribute_targetContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#t_primary.
    def visitT_primary(self, ctx: FandangoParser.T_primaryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#del_targets.
    def visitDel_targets(self, ctx: FandangoParser.Del_targetsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#del_target.
    def visitDel_target(self, ctx: FandangoParser.Del_targetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#del_t_atom.
    def visitDel_t_atom(self, ctx: FandangoParser.Del_t_atomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#type_expressions.
    def visitType_expressions(self, ctx: FandangoParser.Type_expressionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#func_type_comment.
    def visitFunc_type_comment(self, ctx: FandangoParser.Func_type_commentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#identifier.
    def visitIdentifier(self, ctx: FandangoParser.IdentifierContext):
        return self.visitChildren(ctx)


del FandangoParser
