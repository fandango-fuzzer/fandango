# Generated from FandangoParser.g4 by ANTLR 4.9.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .FandangoParser import FandangoParser
else:
    from FandangoParser import FandangoParser


# This class defines a complete listener for a parse tree produced by FandangoParser.
class FandangoParserListener(ParseTreeListener):
    # Enter a parse tree produced by FandangoParser#fandango.
    def enterFandango(self, ctx: FandangoParser.FandangoContext):
        pass

    # Exit a parse tree produced by FandangoParser#fandango.
    def exitFandango(self, ctx: FandangoParser.FandangoContext):
        pass

    # Enter a parse tree produced by FandangoParser#program.
    def enterProgram(self, ctx: FandangoParser.ProgramContext):
        pass

    # Exit a parse tree produced by FandangoParser#program.
    def exitProgram(self, ctx: FandangoParser.ProgramContext):
        pass

    # Enter a parse tree produced by FandangoParser#statement.
    def enterStatement(self, ctx: FandangoParser.StatementContext):
        pass

    # Exit a parse tree produced by FandangoParser#statement.
    def exitStatement(self, ctx: FandangoParser.StatementContext):
        pass

    # Enter a parse tree produced by FandangoParser#production.
    def enterProduction(self, ctx: FandangoParser.ProductionContext):
        pass

    # Exit a parse tree produced by FandangoParser#production.
    def exitProduction(self, ctx: FandangoParser.ProductionContext):
        pass

    # Enter a parse tree produced by FandangoParser#alternatives.
    def enterAlternatives(self, ctx: FandangoParser.AlternativesContext):
        pass

    # Exit a parse tree produced by FandangoParser#alternatives.
    def exitAlternatives(self, ctx: FandangoParser.AlternativesContext):
        pass

    # Enter a parse tree produced by FandangoParser#alternative.
    def enterAlternative(self, ctx: FandangoParser.AlternativeContext):
        pass

    # Exit a parse tree produced by FandangoParser#alternative.
    def exitAlternative(self, ctx: FandangoParser.AlternativeContext):
        pass

    # Enter a parse tree produced by FandangoParser#operator.
    def enterOperator(self, ctx: FandangoParser.OperatorContext):
        pass

    # Exit a parse tree produced by FandangoParser#operator.
    def exitOperator(self, ctx: FandangoParser.OperatorContext):
        pass

    # Enter a parse tree produced by FandangoParser#kleene.
    def enterKleene(self, ctx: FandangoParser.KleeneContext):
        pass

    # Exit a parse tree produced by FandangoParser#kleene.
    def exitKleene(self, ctx: FandangoParser.KleeneContext):
        pass

    # Enter a parse tree produced by FandangoParser#plus.
    def enterPlus(self, ctx: FandangoParser.PlusContext):
        pass

    # Exit a parse tree produced by FandangoParser#plus.
    def exitPlus(self, ctx: FandangoParser.PlusContext):
        pass

    # Enter a parse tree produced by FandangoParser#option.
    def enterOption(self, ctx: FandangoParser.OptionContext):
        pass

    # Exit a parse tree produced by FandangoParser#option.
    def exitOption(self, ctx: FandangoParser.OptionContext):
        pass

    # Enter a parse tree produced by FandangoParser#repeat.
    def enterRepeat(self, ctx: FandangoParser.RepeatContext):
        pass

    # Exit a parse tree produced by FandangoParser#repeat.
    def exitRepeat(self, ctx: FandangoParser.RepeatContext):
        pass

    # Enter a parse tree produced by FandangoParser#symbol.
    def enterSymbol(self, ctx: FandangoParser.SymbolContext):
        pass

    # Exit a parse tree produced by FandangoParser#symbol.
    def exitSymbol(self, ctx: FandangoParser.SymbolContext):
        pass

    # Enter a parse tree produced by FandangoParser#char_set.
    def enterChar_set(self, ctx: FandangoParser.Char_setContext):
        pass

    # Exit a parse tree produced by FandangoParser#char_set.
    def exitChar_set(self, ctx: FandangoParser.Char_setContext):
        pass

    # Enter a parse tree produced by FandangoParser#rule_name.
    def enterRule_name(self, ctx: FandangoParser.Rule_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#rule_name.
    def exitRule_name(self, ctx: FandangoParser.Rule_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#constraint.
    def enterConstraint(self, ctx: FandangoParser.ConstraintContext):
        pass

    # Exit a parse tree produced by FandangoParser#constraint.
    def exitConstraint(self, ctx: FandangoParser.ConstraintContext):
        pass

    # Enter a parse tree produced by FandangoParser#implies.
    def enterImplies(self, ctx: FandangoParser.ImpliesContext):
        pass

    # Exit a parse tree produced by FandangoParser#implies.
    def exitImplies(self, ctx: FandangoParser.ImpliesContext):
        pass

    # Enter a parse tree produced by FandangoParser#quantifier.
    def enterQuantifier(self, ctx: FandangoParser.QuantifierContext):
        pass

    # Exit a parse tree produced by FandangoParser#quantifier.
    def exitQuantifier(self, ctx: FandangoParser.QuantifierContext):
        pass

    # Enter a parse tree produced by FandangoParser#disjunction.
    def enterDisjunction(self, ctx: FandangoParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by FandangoParser#disjunction.
    def exitDisjunction(self, ctx: FandangoParser.DisjunctionContext):
        pass

    # Enter a parse tree produced by FandangoParser#conjunction.
    def enterConjunction(self, ctx: FandangoParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by FandangoParser#conjunction.
    def exitConjunction(self, ctx: FandangoParser.ConjunctionContext):
        pass

    # Enter a parse tree produced by FandangoParser#formula_atom.
    def enterFormula_atom(self, ctx: FandangoParser.Formula_atomContext):
        pass

    # Exit a parse tree produced by FandangoParser#formula_atom.
    def exitFormula_atom(self, ctx: FandangoParser.Formula_atomContext):
        pass

    # Enter a parse tree produced by FandangoParser#formula_comparison.
    def enterFormula_comparison(self, ctx: FandangoParser.Formula_comparisonContext):
        pass

    # Exit a parse tree produced by FandangoParser#formula_comparison.
    def exitFormula_comparison(self, ctx: FandangoParser.Formula_comparisonContext):
        pass

    # Enter a parse tree produced by FandangoParser#expression.
    def enterExpression(self, ctx: FandangoParser.ExpressionContext):
        pass

    # Exit a parse tree produced by FandangoParser#expression.
    def exitExpression(self, ctx: FandangoParser.ExpressionContext):
        pass

    # Enter a parse tree produced by FandangoParser#selector.
    def enterSelector(self, ctx: FandangoParser.SelectorContext):
        pass

    # Exit a parse tree produced by FandangoParser#selector.
    def exitSelector(self, ctx: FandangoParser.SelectorContext):
        pass

    # Enter a parse tree produced by FandangoParser#selection.
    def enterSelection(self, ctx: FandangoParser.SelectionContext):
        pass

    # Exit a parse tree produced by FandangoParser#selection.
    def exitSelection(self, ctx: FandangoParser.SelectionContext):
        pass

    # Enter a parse tree produced by FandangoParser#python.
    def enterPython(self, ctx: FandangoParser.PythonContext):
        pass

    # Exit a parse tree produced by FandangoParser#python.
    def exitPython(self, ctx: FandangoParser.PythonContext):
        pass

    # Enter a parse tree produced by FandangoParser#python_tag.
    def enterPython_tag(self, ctx: FandangoParser.Python_tagContext):
        pass

    # Exit a parse tree produced by FandangoParser#python_tag.
    def exitPython_tag(self, ctx: FandangoParser.Python_tagContext):
        pass

    # Enter a parse tree produced by FandangoParser#decorator.
    def enterDecorator(self, ctx: FandangoParser.DecoratorContext):
        pass

    # Exit a parse tree produced by FandangoParser#decorator.
    def exitDecorator(self, ctx: FandangoParser.DecoratorContext):
        pass

    # Enter a parse tree produced by FandangoParser#decorators.
    def enterDecorators(self, ctx: FandangoParser.DecoratorsContext):
        pass

    # Exit a parse tree produced by FandangoParser#decorators.
    def exitDecorators(self, ctx: FandangoParser.DecoratorsContext):
        pass

    # Enter a parse tree produced by FandangoParser#decorated.
    def enterDecorated(self, ctx: FandangoParser.DecoratedContext):
        pass

    # Exit a parse tree produced by FandangoParser#decorated.
    def exitDecorated(self, ctx: FandangoParser.DecoratedContext):
        pass

    # Enter a parse tree produced by FandangoParser#async_funcdef.
    def enterAsync_funcdef(self, ctx: FandangoParser.Async_funcdefContext):
        pass

    # Exit a parse tree produced by FandangoParser#async_funcdef.
    def exitAsync_funcdef(self, ctx: FandangoParser.Async_funcdefContext):
        pass

    # Enter a parse tree produced by FandangoParser#funcdef.
    def enterFuncdef(self, ctx: FandangoParser.FuncdefContext):
        pass

    # Exit a parse tree produced by FandangoParser#funcdef.
    def exitFuncdef(self, ctx: FandangoParser.FuncdefContext):
        pass

    # Enter a parse tree produced by FandangoParser#parameters.
    def enterParameters(self, ctx: FandangoParser.ParametersContext):
        pass

    # Exit a parse tree produced by FandangoParser#parameters.
    def exitParameters(self, ctx: FandangoParser.ParametersContext):
        pass

    # Enter a parse tree produced by FandangoParser#typedargslist.
    def enterTypedargslist(self, ctx: FandangoParser.TypedargslistContext):
        pass

    # Exit a parse tree produced by FandangoParser#typedargslist.
    def exitTypedargslist(self, ctx: FandangoParser.TypedargslistContext):
        pass

    # Enter a parse tree produced by FandangoParser#tfpdef.
    def enterTfpdef(self, ctx: FandangoParser.TfpdefContext):
        pass

    # Exit a parse tree produced by FandangoParser#tfpdef.
    def exitTfpdef(self, ctx: FandangoParser.TfpdefContext):
        pass

    # Enter a parse tree produced by FandangoParser#varargslist.
    def enterVarargslist(self, ctx: FandangoParser.VarargslistContext):
        pass

    # Exit a parse tree produced by FandangoParser#varargslist.
    def exitVarargslist(self, ctx: FandangoParser.VarargslistContext):
        pass

    # Enter a parse tree produced by FandangoParser#vfpdef.
    def enterVfpdef(self, ctx: FandangoParser.VfpdefContext):
        pass

    # Exit a parse tree produced by FandangoParser#vfpdef.
    def exitVfpdef(self, ctx: FandangoParser.VfpdefContext):
        pass

    # Enter a parse tree produced by FandangoParser#stmt.
    def enterStmt(self, ctx: FandangoParser.StmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#stmt.
    def exitStmt(self, ctx: FandangoParser.StmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#simple_stmts.
    def enterSimple_stmts(self, ctx: FandangoParser.Simple_stmtsContext):
        pass

    # Exit a parse tree produced by FandangoParser#simple_stmts.
    def exitSimple_stmts(self, ctx: FandangoParser.Simple_stmtsContext):
        pass

    # Enter a parse tree produced by FandangoParser#simple_stmt.
    def enterSimple_stmt(self, ctx: FandangoParser.Simple_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#simple_stmt.
    def exitSimple_stmt(self, ctx: FandangoParser.Simple_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#expr_stmt.
    def enterExpr_stmt(self, ctx: FandangoParser.Expr_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#expr_stmt.
    def exitExpr_stmt(self, ctx: FandangoParser.Expr_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#annassign.
    def enterAnnassign(self, ctx: FandangoParser.AnnassignContext):
        pass

    # Exit a parse tree produced by FandangoParser#annassign.
    def exitAnnassign(self, ctx: FandangoParser.AnnassignContext):
        pass

    # Enter a parse tree produced by FandangoParser#testlist_star_expr.
    def enterTestlist_star_expr(self, ctx: FandangoParser.Testlist_star_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#testlist_star_expr.
    def exitTestlist_star_expr(self, ctx: FandangoParser.Testlist_star_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#augassign.
    def enterAugassign(self, ctx: FandangoParser.AugassignContext):
        pass

    # Exit a parse tree produced by FandangoParser#augassign.
    def exitAugassign(self, ctx: FandangoParser.AugassignContext):
        pass

    # Enter a parse tree produced by FandangoParser#del_stmt.
    def enterDel_stmt(self, ctx: FandangoParser.Del_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#del_stmt.
    def exitDel_stmt(self, ctx: FandangoParser.Del_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#pass_stmt.
    def enterPass_stmt(self, ctx: FandangoParser.Pass_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#pass_stmt.
    def exitPass_stmt(self, ctx: FandangoParser.Pass_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#flow_stmt.
    def enterFlow_stmt(self, ctx: FandangoParser.Flow_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#flow_stmt.
    def exitFlow_stmt(self, ctx: FandangoParser.Flow_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#break_stmt.
    def enterBreak_stmt(self, ctx: FandangoParser.Break_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#break_stmt.
    def exitBreak_stmt(self, ctx: FandangoParser.Break_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#continue_stmt.
    def enterContinue_stmt(self, ctx: FandangoParser.Continue_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#continue_stmt.
    def exitContinue_stmt(self, ctx: FandangoParser.Continue_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#return_stmt.
    def enterReturn_stmt(self, ctx: FandangoParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#return_stmt.
    def exitReturn_stmt(self, ctx: FandangoParser.Return_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#yield_stmt.
    def enterYield_stmt(self, ctx: FandangoParser.Yield_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#yield_stmt.
    def exitYield_stmt(self, ctx: FandangoParser.Yield_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#raise_stmt.
    def enterRaise_stmt(self, ctx: FandangoParser.Raise_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#raise_stmt.
    def exitRaise_stmt(self, ctx: FandangoParser.Raise_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#import_stmt.
    def enterImport_stmt(self, ctx: FandangoParser.Import_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#import_stmt.
    def exitImport_stmt(self, ctx: FandangoParser.Import_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#import_name.
    def enterImport_name(self, ctx: FandangoParser.Import_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#import_name.
    def exitImport_name(self, ctx: FandangoParser.Import_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#import_from.
    def enterImport_from(self, ctx: FandangoParser.Import_fromContext):
        pass

    # Exit a parse tree produced by FandangoParser#import_from.
    def exitImport_from(self, ctx: FandangoParser.Import_fromContext):
        pass

    # Enter a parse tree produced by FandangoParser#import_as_name.
    def enterImport_as_name(self, ctx: FandangoParser.Import_as_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#import_as_name.
    def exitImport_as_name(self, ctx: FandangoParser.Import_as_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#dotted_as_name.
    def enterDotted_as_name(self, ctx: FandangoParser.Dotted_as_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#dotted_as_name.
    def exitDotted_as_name(self, ctx: FandangoParser.Dotted_as_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#import_as_names.
    def enterImport_as_names(self, ctx: FandangoParser.Import_as_namesContext):
        pass

    # Exit a parse tree produced by FandangoParser#import_as_names.
    def exitImport_as_names(self, ctx: FandangoParser.Import_as_namesContext):
        pass

    # Enter a parse tree produced by FandangoParser#dotted_as_names.
    def enterDotted_as_names(self, ctx: FandangoParser.Dotted_as_namesContext):
        pass

    # Exit a parse tree produced by FandangoParser#dotted_as_names.
    def exitDotted_as_names(self, ctx: FandangoParser.Dotted_as_namesContext):
        pass

    # Enter a parse tree produced by FandangoParser#dotted_name.
    def enterDotted_name(self, ctx: FandangoParser.Dotted_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#dotted_name.
    def exitDotted_name(self, ctx: FandangoParser.Dotted_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#global_stmt.
    def enterGlobal_stmt(self, ctx: FandangoParser.Global_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#global_stmt.
    def exitGlobal_stmt(self, ctx: FandangoParser.Global_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#nonlocal_stmt.
    def enterNonlocal_stmt(self, ctx: FandangoParser.Nonlocal_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#nonlocal_stmt.
    def exitNonlocal_stmt(self, ctx: FandangoParser.Nonlocal_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#assert_stmt.
    def enterAssert_stmt(self, ctx: FandangoParser.Assert_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#assert_stmt.
    def exitAssert_stmt(self, ctx: FandangoParser.Assert_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#compound_stmt.
    def enterCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#compound_stmt.
    def exitCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#async_stmt.
    def enterAsync_stmt(self, ctx: FandangoParser.Async_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#async_stmt.
    def exitAsync_stmt(self, ctx: FandangoParser.Async_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#if_stmt.
    def enterIf_stmt(self, ctx: FandangoParser.If_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#if_stmt.
    def exitIf_stmt(self, ctx: FandangoParser.If_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#while_stmt.
    def enterWhile_stmt(self, ctx: FandangoParser.While_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#while_stmt.
    def exitWhile_stmt(self, ctx: FandangoParser.While_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#for_stmt.
    def enterFor_stmt(self, ctx: FandangoParser.For_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#for_stmt.
    def exitFor_stmt(self, ctx: FandangoParser.For_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#try_stmt.
    def enterTry_stmt(self, ctx: FandangoParser.Try_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#try_stmt.
    def exitTry_stmt(self, ctx: FandangoParser.Try_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#with_stmt.
    def enterWith_stmt(self, ctx: FandangoParser.With_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#with_stmt.
    def exitWith_stmt(self, ctx: FandangoParser.With_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#with_item.
    def enterWith_item(self, ctx: FandangoParser.With_itemContext):
        pass

    # Exit a parse tree produced by FandangoParser#with_item.
    def exitWith_item(self, ctx: FandangoParser.With_itemContext):
        pass

    # Enter a parse tree produced by FandangoParser#except_clause.
    def enterExcept_clause(self, ctx: FandangoParser.Except_clauseContext):
        pass

    # Exit a parse tree produced by FandangoParser#except_clause.
    def exitExcept_clause(self, ctx: FandangoParser.Except_clauseContext):
        pass

    # Enter a parse tree produced by FandangoParser#block.
    def enterBlock(self, ctx: FandangoParser.BlockContext):
        pass

    # Exit a parse tree produced by FandangoParser#block.
    def exitBlock(self, ctx: FandangoParser.BlockContext):
        pass

    # Enter a parse tree produced by FandangoParser#match_stmt.
    def enterMatch_stmt(self, ctx: FandangoParser.Match_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#match_stmt.
    def exitMatch_stmt(self, ctx: FandangoParser.Match_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#subject_expr.
    def enterSubject_expr(self, ctx: FandangoParser.Subject_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#subject_expr.
    def exitSubject_expr(self, ctx: FandangoParser.Subject_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_named_expressions.
    def enterStar_named_expressions(
        self, ctx: FandangoParser.Star_named_expressionsContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#star_named_expressions.
    def exitStar_named_expressions(
        self, ctx: FandangoParser.Star_named_expressionsContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#star_named_expression.
    def enterStar_named_expression(
        self, ctx: FandangoParser.Star_named_expressionContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#star_named_expression.
    def exitStar_named_expression(
        self, ctx: FandangoParser.Star_named_expressionContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#case_block.
    def enterCase_block(self, ctx: FandangoParser.Case_blockContext):
        pass

    # Exit a parse tree produced by FandangoParser#case_block.
    def exitCase_block(self, ctx: FandangoParser.Case_blockContext):
        pass

    # Enter a parse tree produced by FandangoParser#guard.
    def enterGuard(self, ctx: FandangoParser.GuardContext):
        pass

    # Exit a parse tree produced by FandangoParser#guard.
    def exitGuard(self, ctx: FandangoParser.GuardContext):
        pass

    # Enter a parse tree produced by FandangoParser#patterns.
    def enterPatterns(self, ctx: FandangoParser.PatternsContext):
        pass

    # Exit a parse tree produced by FandangoParser#patterns.
    def exitPatterns(self, ctx: FandangoParser.PatternsContext):
        pass

    # Enter a parse tree produced by FandangoParser#pattern.
    def enterPattern(self, ctx: FandangoParser.PatternContext):
        pass

    # Exit a parse tree produced by FandangoParser#pattern.
    def exitPattern(self, ctx: FandangoParser.PatternContext):
        pass

    # Enter a parse tree produced by FandangoParser#as_pattern.
    def enterAs_pattern(self, ctx: FandangoParser.As_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#as_pattern.
    def exitAs_pattern(self, ctx: FandangoParser.As_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#or_pattern.
    def enterOr_pattern(self, ctx: FandangoParser.Or_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#or_pattern.
    def exitOr_pattern(self, ctx: FandangoParser.Or_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#closed_pattern.
    def enterClosed_pattern(self, ctx: FandangoParser.Closed_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#closed_pattern.
    def exitClosed_pattern(self, ctx: FandangoParser.Closed_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#literal_pattern.
    def enterLiteral_pattern(self, ctx: FandangoParser.Literal_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#literal_pattern.
    def exitLiteral_pattern(self, ctx: FandangoParser.Literal_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#literal_expr.
    def enterLiteral_expr(self, ctx: FandangoParser.Literal_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#literal_expr.
    def exitLiteral_expr(self, ctx: FandangoParser.Literal_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#complex_number.
    def enterComplex_number(self, ctx: FandangoParser.Complex_numberContext):
        pass

    # Exit a parse tree produced by FandangoParser#complex_number.
    def exitComplex_number(self, ctx: FandangoParser.Complex_numberContext):
        pass

    # Enter a parse tree produced by FandangoParser#signed_number.
    def enterSigned_number(self, ctx: FandangoParser.Signed_numberContext):
        pass

    # Exit a parse tree produced by FandangoParser#signed_number.
    def exitSigned_number(self, ctx: FandangoParser.Signed_numberContext):
        pass

    # Enter a parse tree produced by FandangoParser#signed_real_number.
    def enterSigned_real_number(self, ctx: FandangoParser.Signed_real_numberContext):
        pass

    # Exit a parse tree produced by FandangoParser#signed_real_number.
    def exitSigned_real_number(self, ctx: FandangoParser.Signed_real_numberContext):
        pass

    # Enter a parse tree produced by FandangoParser#real_number.
    def enterReal_number(self, ctx: FandangoParser.Real_numberContext):
        pass

    # Exit a parse tree produced by FandangoParser#real_number.
    def exitReal_number(self, ctx: FandangoParser.Real_numberContext):
        pass

    # Enter a parse tree produced by FandangoParser#imaginary_number.
    def enterImaginary_number(self, ctx: FandangoParser.Imaginary_numberContext):
        pass

    # Exit a parse tree produced by FandangoParser#imaginary_number.
    def exitImaginary_number(self, ctx: FandangoParser.Imaginary_numberContext):
        pass

    # Enter a parse tree produced by FandangoParser#capture_pattern.
    def enterCapture_pattern(self, ctx: FandangoParser.Capture_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#capture_pattern.
    def exitCapture_pattern(self, ctx: FandangoParser.Capture_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#pattern_capture_target.
    def enterPattern_capture_target(
        self, ctx: FandangoParser.Pattern_capture_targetContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#pattern_capture_target.
    def exitPattern_capture_target(
        self, ctx: FandangoParser.Pattern_capture_targetContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#wildcard_pattern.
    def enterWildcard_pattern(self, ctx: FandangoParser.Wildcard_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#wildcard_pattern.
    def exitWildcard_pattern(self, ctx: FandangoParser.Wildcard_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#value_pattern.
    def enterValue_pattern(self, ctx: FandangoParser.Value_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#value_pattern.
    def exitValue_pattern(self, ctx: FandangoParser.Value_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#attr.
    def enterAttr(self, ctx: FandangoParser.AttrContext):
        pass

    # Exit a parse tree produced by FandangoParser#attr.
    def exitAttr(self, ctx: FandangoParser.AttrContext):
        pass

    # Enter a parse tree produced by FandangoParser#name_or_attr.
    def enterName_or_attr(self, ctx: FandangoParser.Name_or_attrContext):
        pass

    # Exit a parse tree produced by FandangoParser#name_or_attr.
    def exitName_or_attr(self, ctx: FandangoParser.Name_or_attrContext):
        pass

    # Enter a parse tree produced by FandangoParser#group_pattern.
    def enterGroup_pattern(self, ctx: FandangoParser.Group_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#group_pattern.
    def exitGroup_pattern(self, ctx: FandangoParser.Group_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#sequence_pattern.
    def enterSequence_pattern(self, ctx: FandangoParser.Sequence_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#sequence_pattern.
    def exitSequence_pattern(self, ctx: FandangoParser.Sequence_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#open_sequence_pattern.
    def enterOpen_sequence_pattern(
        self, ctx: FandangoParser.Open_sequence_patternContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#open_sequence_pattern.
    def exitOpen_sequence_pattern(
        self, ctx: FandangoParser.Open_sequence_patternContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#maybe_sequence_pattern.
    def enterMaybe_sequence_pattern(
        self, ctx: FandangoParser.Maybe_sequence_patternContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#maybe_sequence_pattern.
    def exitMaybe_sequence_pattern(
        self, ctx: FandangoParser.Maybe_sequence_patternContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#maybe_star_pattern.
    def enterMaybe_star_pattern(self, ctx: FandangoParser.Maybe_star_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#maybe_star_pattern.
    def exitMaybe_star_pattern(self, ctx: FandangoParser.Maybe_star_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_pattern.
    def enterStar_pattern(self, ctx: FandangoParser.Star_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_pattern.
    def exitStar_pattern(self, ctx: FandangoParser.Star_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#mapping_pattern.
    def enterMapping_pattern(self, ctx: FandangoParser.Mapping_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#mapping_pattern.
    def exitMapping_pattern(self, ctx: FandangoParser.Mapping_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#items_pattern.
    def enterItems_pattern(self, ctx: FandangoParser.Items_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#items_pattern.
    def exitItems_pattern(self, ctx: FandangoParser.Items_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#key_value_pattern.
    def enterKey_value_pattern(self, ctx: FandangoParser.Key_value_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#key_value_pattern.
    def exitKey_value_pattern(self, ctx: FandangoParser.Key_value_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#double_star_pattern.
    def enterDouble_star_pattern(self, ctx: FandangoParser.Double_star_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#double_star_pattern.
    def exitDouble_star_pattern(self, ctx: FandangoParser.Double_star_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#class_pattern.
    def enterClass_pattern(self, ctx: FandangoParser.Class_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#class_pattern.
    def exitClass_pattern(self, ctx: FandangoParser.Class_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#positional_patterns.
    def enterPositional_patterns(self, ctx: FandangoParser.Positional_patternsContext):
        pass

    # Exit a parse tree produced by FandangoParser#positional_patterns.
    def exitPositional_patterns(self, ctx: FandangoParser.Positional_patternsContext):
        pass

    # Enter a parse tree produced by FandangoParser#keyword_patterns.
    def enterKeyword_patterns(self, ctx: FandangoParser.Keyword_patternsContext):
        pass

    # Exit a parse tree produced by FandangoParser#keyword_patterns.
    def exitKeyword_patterns(self, ctx: FandangoParser.Keyword_patternsContext):
        pass

    # Enter a parse tree produced by FandangoParser#keyword_pattern.
    def enterKeyword_pattern(self, ctx: FandangoParser.Keyword_patternContext):
        pass

    # Exit a parse tree produced by FandangoParser#keyword_pattern.
    def exitKeyword_pattern(self, ctx: FandangoParser.Keyword_patternContext):
        pass

    # Enter a parse tree produced by FandangoParser#test.
    def enterTest(self, ctx: FandangoParser.TestContext):
        pass

    # Exit a parse tree produced by FandangoParser#test.
    def exitTest(self, ctx: FandangoParser.TestContext):
        pass

    # Enter a parse tree produced by FandangoParser#test_nocond.
    def enterTest_nocond(self, ctx: FandangoParser.Test_nocondContext):
        pass

    # Exit a parse tree produced by FandangoParser#test_nocond.
    def exitTest_nocond(self, ctx: FandangoParser.Test_nocondContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambdef.
    def enterLambdef(self, ctx: FandangoParser.LambdefContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambdef.
    def exitLambdef(self, ctx: FandangoParser.LambdefContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambdef_nocond.
    def enterLambdef_nocond(self, ctx: FandangoParser.Lambdef_nocondContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambdef_nocond.
    def exitLambdef_nocond(self, ctx: FandangoParser.Lambdef_nocondContext):
        pass

    # Enter a parse tree produced by FandangoParser#or_test.
    def enterOr_test(self, ctx: FandangoParser.Or_testContext):
        pass

    # Exit a parse tree produced by FandangoParser#or_test.
    def exitOr_test(self, ctx: FandangoParser.Or_testContext):
        pass

    # Enter a parse tree produced by FandangoParser#and_test.
    def enterAnd_test(self, ctx: FandangoParser.And_testContext):
        pass

    # Exit a parse tree produced by FandangoParser#and_test.
    def exitAnd_test(self, ctx: FandangoParser.And_testContext):
        pass

    # Enter a parse tree produced by FandangoParser#not_test.
    def enterNot_test(self, ctx: FandangoParser.Not_testContext):
        pass

    # Exit a parse tree produced by FandangoParser#not_test.
    def exitNot_test(self, ctx: FandangoParser.Not_testContext):
        pass

    # Enter a parse tree produced by FandangoParser#comparison.
    def enterComparison(self, ctx: FandangoParser.ComparisonContext):
        pass

    # Exit a parse tree produced by FandangoParser#comparison.
    def exitComparison(self, ctx: FandangoParser.ComparisonContext):
        pass

    # Enter a parse tree produced by FandangoParser#comp_op.
    def enterComp_op(self, ctx: FandangoParser.Comp_opContext):
        pass

    # Exit a parse tree produced by FandangoParser#comp_op.
    def exitComp_op(self, ctx: FandangoParser.Comp_opContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_expr.
    def enterStar_expr(self, ctx: FandangoParser.Star_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_expr.
    def exitStar_expr(self, ctx: FandangoParser.Star_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#expr.
    def enterExpr(self, ctx: FandangoParser.ExprContext):
        pass

    # Exit a parse tree produced by FandangoParser#expr.
    def exitExpr(self, ctx: FandangoParser.ExprContext):
        pass

    # Enter a parse tree produced by FandangoParser#atom_expr.
    def enterAtom_expr(self, ctx: FandangoParser.Atom_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#atom_expr.
    def exitAtom_expr(self, ctx: FandangoParser.Atom_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#atom.
    def enterAtom(self, ctx: FandangoParser.AtomContext):
        pass

    # Exit a parse tree produced by FandangoParser#atom.
    def exitAtom(self, ctx: FandangoParser.AtomContext):
        pass

    # Enter a parse tree produced by FandangoParser#name.
    def enterName(self, ctx: FandangoParser.NameContext):
        pass

    # Exit a parse tree produced by FandangoParser#name.
    def exitName(self, ctx: FandangoParser.NameContext):
        pass

    # Enter a parse tree produced by FandangoParser#testlist_comp.
    def enterTestlist_comp(self, ctx: FandangoParser.Testlist_compContext):
        pass

    # Exit a parse tree produced by FandangoParser#testlist_comp.
    def exitTestlist_comp(self, ctx: FandangoParser.Testlist_compContext):
        pass

    # Enter a parse tree produced by FandangoParser#trailer.
    def enterTrailer(self, ctx: FandangoParser.TrailerContext):
        pass

    # Exit a parse tree produced by FandangoParser#trailer.
    def exitTrailer(self, ctx: FandangoParser.TrailerContext):
        pass

    # Enter a parse tree produced by FandangoParser#subscriptlist.
    def enterSubscriptlist(self, ctx: FandangoParser.SubscriptlistContext):
        pass

    # Exit a parse tree produced by FandangoParser#subscriptlist.
    def exitSubscriptlist(self, ctx: FandangoParser.SubscriptlistContext):
        pass

    # Enter a parse tree produced by FandangoParser#subscript_.
    def enterSubscript_(self, ctx: FandangoParser.Subscript_Context):
        pass

    # Exit a parse tree produced by FandangoParser#subscript_.
    def exitSubscript_(self, ctx: FandangoParser.Subscript_Context):
        pass

    # Enter a parse tree produced by FandangoParser#sliceop.
    def enterSliceop(self, ctx: FandangoParser.SliceopContext):
        pass

    # Exit a parse tree produced by FandangoParser#sliceop.
    def exitSliceop(self, ctx: FandangoParser.SliceopContext):
        pass

    # Enter a parse tree produced by FandangoParser#exprlist.
    def enterExprlist(self, ctx: FandangoParser.ExprlistContext):
        pass

    # Exit a parse tree produced by FandangoParser#exprlist.
    def exitExprlist(self, ctx: FandangoParser.ExprlistContext):
        pass

    # Enter a parse tree produced by FandangoParser#testlist.
    def enterTestlist(self, ctx: FandangoParser.TestlistContext):
        pass

    # Exit a parse tree produced by FandangoParser#testlist.
    def exitTestlist(self, ctx: FandangoParser.TestlistContext):
        pass

    # Enter a parse tree produced by FandangoParser#dictorsetmaker.
    def enterDictorsetmaker(self, ctx: FandangoParser.DictorsetmakerContext):
        pass

    # Exit a parse tree produced by FandangoParser#dictorsetmaker.
    def exitDictorsetmaker(self, ctx: FandangoParser.DictorsetmakerContext):
        pass

    # Enter a parse tree produced by FandangoParser#classdef.
    def enterClassdef(self, ctx: FandangoParser.ClassdefContext):
        pass

    # Exit a parse tree produced by FandangoParser#classdef.
    def exitClassdef(self, ctx: FandangoParser.ClassdefContext):
        pass

    # Enter a parse tree produced by FandangoParser#arglist.
    def enterArglist(self, ctx: FandangoParser.ArglistContext):
        pass

    # Exit a parse tree produced by FandangoParser#arglist.
    def exitArglist(self, ctx: FandangoParser.ArglistContext):
        pass

    # Enter a parse tree produced by FandangoParser#argument.
    def enterArgument(self, ctx: FandangoParser.ArgumentContext):
        pass

    # Exit a parse tree produced by FandangoParser#argument.
    def exitArgument(self, ctx: FandangoParser.ArgumentContext):
        pass

    # Enter a parse tree produced by FandangoParser#comp_iter.
    def enterComp_iter(self, ctx: FandangoParser.Comp_iterContext):
        pass

    # Exit a parse tree produced by FandangoParser#comp_iter.
    def exitComp_iter(self, ctx: FandangoParser.Comp_iterContext):
        pass

    # Enter a parse tree produced by FandangoParser#comp_for.
    def enterComp_for(self, ctx: FandangoParser.Comp_forContext):
        pass

    # Exit a parse tree produced by FandangoParser#comp_for.
    def exitComp_for(self, ctx: FandangoParser.Comp_forContext):
        pass

    # Enter a parse tree produced by FandangoParser#comp_if.
    def enterComp_if(self, ctx: FandangoParser.Comp_ifContext):
        pass

    # Exit a parse tree produced by FandangoParser#comp_if.
    def exitComp_if(self, ctx: FandangoParser.Comp_ifContext):
        pass

    # Enter a parse tree produced by FandangoParser#yield_expr.
    def enterYield_expr(self, ctx: FandangoParser.Yield_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#yield_expr.
    def exitYield_expr(self, ctx: FandangoParser.Yield_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#yield_arg.
    def enterYield_arg(self, ctx: FandangoParser.Yield_argContext):
        pass

    # Exit a parse tree produced by FandangoParser#yield_arg.
    def exitYield_arg(self, ctx: FandangoParser.Yield_argContext):
        pass

    # Enter a parse tree produced by FandangoParser#strings.
    def enterStrings(self, ctx: FandangoParser.StringsContext):
        pass

    # Exit a parse tree produced by FandangoParser#strings.
    def exitStrings(self, ctx: FandangoParser.StringsContext):
        pass


del FandangoParser
