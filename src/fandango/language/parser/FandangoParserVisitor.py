# Generated from FandangoParser.g4 by ANTLR 4.13.2
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

    # Visit a parse tree produced by FandangoParser#alternatives.
    def visitAlternatives(self, ctx: FandangoParser.AlternativesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#alternative.
    def visitAlternative(self, ctx: FandangoParser.AlternativeContext):
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

    # Visit a parse tree produced by FandangoParser#char_set.
    def visitChar_set(self, ctx: FandangoParser.Char_setContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#rule_name.
    def visitRule_name(self, ctx: FandangoParser.Rule_nameContext):
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

    # Visit a parse tree produced by FandangoParser#disjunction.
    def visitDisjunction(self, ctx: FandangoParser.DisjunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#conjunction.
    def visitConjunction(self, ctx: FandangoParser.ConjunctionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#formula_atom.
    def visitFormula_atom(self, ctx: FandangoParser.Formula_atomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#formula_comparison.
    def visitFormula_comparison(self, ctx: FandangoParser.Formula_comparisonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#expression.
    def visitExpression(self, ctx: FandangoParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#selector.
    def visitSelector(self, ctx: FandangoParser.SelectorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#selection.
    def visitSelection(self, ctx: FandangoParser.SelectionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#python.
    def visitPython(self, ctx: FandangoParser.PythonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#python_tag.
    def visitPython_tag(self, ctx: FandangoParser.Python_tagContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#decorator.
    def visitDecorator(self, ctx: FandangoParser.DecoratorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#decorators.
    def visitDecorators(self, ctx: FandangoParser.DecoratorsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#decorated.
    def visitDecorated(self, ctx: FandangoParser.DecoratedContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#async_funcdef.
    def visitAsync_funcdef(self, ctx: FandangoParser.Async_funcdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#funcdef.
    def visitFuncdef(self, ctx: FandangoParser.FuncdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#parameters.
    def visitParameters(self, ctx: FandangoParser.ParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#typedargslist.
    def visitTypedargslist(self, ctx: FandangoParser.TypedargslistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#tfpdef.
    def visitTfpdef(self, ctx: FandangoParser.TfpdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#varargslist.
    def visitVarargslist(self, ctx: FandangoParser.VarargslistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#vfpdef.
    def visitVfpdef(self, ctx: FandangoParser.VfpdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#stmt.
    def visitStmt(self, ctx: FandangoParser.StmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#simple_stmts.
    def visitSimple_stmts(self, ctx: FandangoParser.Simple_stmtsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#simple_stmt.
    def visitSimple_stmt(self, ctx: FandangoParser.Simple_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#expr_stmt.
    def visitExpr_stmt(self, ctx: FandangoParser.Expr_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#annassign.
    def visitAnnassign(self, ctx: FandangoParser.AnnassignContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#testlist_star_expr.
    def visitTestlist_star_expr(self, ctx: FandangoParser.Testlist_star_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#augassign.
    def visitAugassign(self, ctx: FandangoParser.AugassignContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#del_stmt.
    def visitDel_stmt(self, ctx: FandangoParser.Del_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#pass_stmt.
    def visitPass_stmt(self, ctx: FandangoParser.Pass_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#flow_stmt.
    def visitFlow_stmt(self, ctx: FandangoParser.Flow_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#break_stmt.
    def visitBreak_stmt(self, ctx: FandangoParser.Break_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#continue_stmt.
    def visitContinue_stmt(self, ctx: FandangoParser.Continue_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#return_stmt.
    def visitReturn_stmt(self, ctx: FandangoParser.Return_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#yield_stmt.
    def visitYield_stmt(self, ctx: FandangoParser.Yield_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#raise_stmt.
    def visitRaise_stmt(self, ctx: FandangoParser.Raise_stmtContext):
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

    # Visit a parse tree produced by FandangoParser#import_as_name.
    def visitImport_as_name(self, ctx: FandangoParser.Import_as_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dotted_as_name.
    def visitDotted_as_name(self, ctx: FandangoParser.Dotted_as_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#import_as_names.
    def visitImport_as_names(self, ctx: FandangoParser.Import_as_namesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dotted_as_names.
    def visitDotted_as_names(self, ctx: FandangoParser.Dotted_as_namesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dotted_name.
    def visitDotted_name(self, ctx: FandangoParser.Dotted_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#global_stmt.
    def visitGlobal_stmt(self, ctx: FandangoParser.Global_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#nonlocal_stmt.
    def visitNonlocal_stmt(self, ctx: FandangoParser.Nonlocal_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#assert_stmt.
    def visitAssert_stmt(self, ctx: FandangoParser.Assert_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#compound_stmt.
    def visitCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#async_stmt.
    def visitAsync_stmt(self, ctx: FandangoParser.Async_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#if_stmt.
    def visitIf_stmt(self, ctx: FandangoParser.If_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#while_stmt.
    def visitWhile_stmt(self, ctx: FandangoParser.While_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#for_stmt.
    def visitFor_stmt(self, ctx: FandangoParser.For_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#try_stmt.
    def visitTry_stmt(self, ctx: FandangoParser.Try_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#with_stmt.
    def visitWith_stmt(self, ctx: FandangoParser.With_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#with_item.
    def visitWith_item(self, ctx: FandangoParser.With_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#except_clause.
    def visitExcept_clause(self, ctx: FandangoParser.Except_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#block.
    def visitBlock(self, ctx: FandangoParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#match_stmt.
    def visitMatch_stmt(self, ctx: FandangoParser.Match_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#subject_expr.
    def visitSubject_expr(self, ctx: FandangoParser.Subject_exprContext):
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

    # Visit a parse tree produced by FandangoParser#test.
    def visitTest(self, ctx: FandangoParser.TestContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#test_nocond.
    def visitTest_nocond(self, ctx: FandangoParser.Test_nocondContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambdef.
    def visitLambdef(self, ctx: FandangoParser.LambdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#lambdef_nocond.
    def visitLambdef_nocond(self, ctx: FandangoParser.Lambdef_nocondContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#or_test.
    def visitOr_test(self, ctx: FandangoParser.Or_testContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#and_test.
    def visitAnd_test(self, ctx: FandangoParser.And_testContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#not_test.
    def visitNot_test(self, ctx: FandangoParser.Not_testContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#comparison.
    def visitComparison(self, ctx: FandangoParser.ComparisonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#comp_op.
    def visitComp_op(self, ctx: FandangoParser.Comp_opContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#star_expr.
    def visitStar_expr(self, ctx: FandangoParser.Star_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#expr.
    def visitExpr(self, ctx: FandangoParser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#atom_expr.
    def visitAtom_expr(self, ctx: FandangoParser.Atom_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#atom.
    def visitAtom(self, ctx: FandangoParser.AtomContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#name.
    def visitName(self, ctx: FandangoParser.NameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#testlist_comp.
    def visitTestlist_comp(self, ctx: FandangoParser.Testlist_compContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#trailer.
    def visitTrailer(self, ctx: FandangoParser.TrailerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#subscriptlist.
    def visitSubscriptlist(self, ctx: FandangoParser.SubscriptlistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#subscript_.
    def visitSubscript_(self, ctx: FandangoParser.Subscript_Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#sliceop.
    def visitSliceop(self, ctx: FandangoParser.SliceopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#exprlist.
    def visitExprlist(self, ctx: FandangoParser.ExprlistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#testlist.
    def visitTestlist(self, ctx: FandangoParser.TestlistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#dictorsetmaker.
    def visitDictorsetmaker(self, ctx: FandangoParser.DictorsetmakerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#classdef.
    def visitClassdef(self, ctx: FandangoParser.ClassdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#arglist.
    def visitArglist(self, ctx: FandangoParser.ArglistContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#argument.
    def visitArgument(self, ctx: FandangoParser.ArgumentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#comp_iter.
    def visitComp_iter(self, ctx: FandangoParser.Comp_iterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#comp_for.
    def visitComp_for(self, ctx: FandangoParser.Comp_forContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#comp_if.
    def visitComp_if(self, ctx: FandangoParser.Comp_ifContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#yield_expr.
    def visitYield_expr(self, ctx: FandangoParser.Yield_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#yield_arg.
    def visitYield_arg(self, ctx: FandangoParser.Yield_argContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by FandangoParser#strings.
    def visitStrings(self, ctx: FandangoParser.StringsContext):
        return self.visitChildren(ctx)


del FandangoParser
