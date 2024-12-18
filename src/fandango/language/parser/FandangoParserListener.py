# Generated from language/FandangoParser.g4 by ANTLR 4.13.2
from antlr4 import *

if "." in __name__:
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

    # Enter a parse tree produced by FandangoParser#alternative.
    def enterAlternative(self, ctx: FandangoParser.AlternativeContext):
        pass

    # Exit a parse tree produced by FandangoParser#alternative.
    def exitAlternative(self, ctx: FandangoParser.AlternativeContext):
        pass

    # Enter a parse tree produced by FandangoParser#concatenation.
    def enterConcatenation(self, ctx: FandangoParser.ConcatenationContext):
        pass

    # Exit a parse tree produced by FandangoParser#concatenation.
    def exitConcatenation(self, ctx: FandangoParser.ConcatenationContext):
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

    # Enter a parse tree produced by FandangoParser#formula_disjunction.
    def enterFormula_disjunction(self, ctx: FandangoParser.Formula_disjunctionContext):
        pass

    # Exit a parse tree produced by FandangoParser#formula_disjunction.
    def exitFormula_disjunction(self, ctx: FandangoParser.Formula_disjunctionContext):
        pass

    # Enter a parse tree produced by FandangoParser#formula_conjunction.
    def enterFormula_conjunction(self, ctx: FandangoParser.Formula_conjunctionContext):
        pass

    # Exit a parse tree produced by FandangoParser#formula_conjunction.
    def exitFormula_conjunction(self, ctx: FandangoParser.Formula_conjunctionContext):
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

    # Enter a parse tree produced by FandangoParser#expr.
    def enterExpr(self, ctx: FandangoParser.ExprContext):
        pass

    # Exit a parse tree produced by FandangoParser#expr.
    def exitExpr(self, ctx: FandangoParser.ExprContext):
        pass

    # Enter a parse tree produced by FandangoParser#selector_length.
    def enterSelector_length(self, ctx: FandangoParser.Selector_lengthContext):
        pass

    # Exit a parse tree produced by FandangoParser#selector_length.
    def exitSelector_length(self, ctx: FandangoParser.Selector_lengthContext):
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

    # Enter a parse tree produced by FandangoParser#base_selection.
    def enterBase_selection(self, ctx: FandangoParser.Base_selectionContext):
        pass

    # Exit a parse tree produced by FandangoParser#base_selection.
    def exitBase_selection(self, ctx: FandangoParser.Base_selectionContext):
        pass

    # Enter a parse tree produced by FandangoParser#rs_pairs.
    def enterRs_pairs(self, ctx: FandangoParser.Rs_pairsContext):
        pass

    # Exit a parse tree produced by FandangoParser#rs_pairs.
    def exitRs_pairs(self, ctx: FandangoParser.Rs_pairsContext):
        pass

    # Enter a parse tree produced by FandangoParser#rs_pair.
    def enterRs_pair(self, ctx: FandangoParser.Rs_pairContext):
        pass

    # Exit a parse tree produced by FandangoParser#rs_pair.
    def exitRs_pair(self, ctx: FandangoParser.Rs_pairContext):
        pass

    # Enter a parse tree produced by FandangoParser#rs_slices.
    def enterRs_slices(self, ctx: FandangoParser.Rs_slicesContext):
        pass

    # Exit a parse tree produced by FandangoParser#rs_slices.
    def exitRs_slices(self, ctx: FandangoParser.Rs_slicesContext):
        pass

    # Enter a parse tree produced by FandangoParser#rs_slice.
    def enterRs_slice(self, ctx: FandangoParser.Rs_sliceContext):
        pass

    # Exit a parse tree produced by FandangoParser#rs_slice.
    def exitRs_slice(self, ctx: FandangoParser.Rs_sliceContext):
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

    # Enter a parse tree produced by FandangoParser#python_file.
    def enterPython_file(self, ctx: FandangoParser.Python_fileContext):
        pass

    # Exit a parse tree produced by FandangoParser#python_file.
    def exitPython_file(self, ctx: FandangoParser.Python_fileContext):
        pass

    # Enter a parse tree produced by FandangoParser#interactive.
    def enterInteractive(self, ctx: FandangoParser.InteractiveContext):
        pass

    # Exit a parse tree produced by FandangoParser#interactive.
    def exitInteractive(self, ctx: FandangoParser.InteractiveContext):
        pass

    # Enter a parse tree produced by FandangoParser#eval.
    def enterEval(self, ctx: FandangoParser.EvalContext):
        pass

    # Exit a parse tree produced by FandangoParser#eval.
    def exitEval(self, ctx: FandangoParser.EvalContext):
        pass

    # Enter a parse tree produced by FandangoParser#func_type.
    def enterFunc_type(self, ctx: FandangoParser.Func_typeContext):
        pass

    # Exit a parse tree produced by FandangoParser#func_type.
    def exitFunc_type(self, ctx: FandangoParser.Func_typeContext):
        pass

    # Enter a parse tree produced by FandangoParser#statements.
    def enterStatements(self, ctx: FandangoParser.StatementsContext):
        pass

    # Exit a parse tree produced by FandangoParser#statements.
    def exitStatements(self, ctx: FandangoParser.StatementsContext):
        pass

    # Enter a parse tree produced by FandangoParser#stmt.
    def enterStmt(self, ctx: FandangoParser.StmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#stmt.
    def exitStmt(self, ctx: FandangoParser.StmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#statement_newline.
    def enterStatement_newline(self, ctx: FandangoParser.Statement_newlineContext):
        pass

    # Exit a parse tree produced by FandangoParser#statement_newline.
    def exitStatement_newline(self, ctx: FandangoParser.Statement_newlineContext):
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

    # Enter a parse tree produced by FandangoParser#compound_stmt.
    def enterCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#compound_stmt.
    def exitCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#assignment.
    def enterAssignment(self, ctx: FandangoParser.AssignmentContext):
        pass

    # Exit a parse tree produced by FandangoParser#assignment.
    def exitAssignment(self, ctx: FandangoParser.AssignmentContext):
        pass

    # Enter a parse tree produced by FandangoParser#annotated_rhs.
    def enterAnnotated_rhs(self, ctx: FandangoParser.Annotated_rhsContext):
        pass

    # Exit a parse tree produced by FandangoParser#annotated_rhs.
    def exitAnnotated_rhs(self, ctx: FandangoParser.Annotated_rhsContext):
        pass

    # Enter a parse tree produced by FandangoParser#augassign.
    def enterAugassign(self, ctx: FandangoParser.AugassignContext):
        pass

    # Exit a parse tree produced by FandangoParser#augassign.
    def exitAugassign(self, ctx: FandangoParser.AugassignContext):
        pass

    # Enter a parse tree produced by FandangoParser#return_stmt.
    def enterReturn_stmt(self, ctx: FandangoParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#return_stmt.
    def exitReturn_stmt(self, ctx: FandangoParser.Return_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#raise_stmt.
    def enterRaise_stmt(self, ctx: FandangoParser.Raise_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#raise_stmt.
    def exitRaise_stmt(self, ctx: FandangoParser.Raise_stmtContext):
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

    # Enter a parse tree produced by FandangoParser#del_stmt.
    def enterDel_stmt(self, ctx: FandangoParser.Del_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#del_stmt.
    def exitDel_stmt(self, ctx: FandangoParser.Del_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#yield_stmt.
    def enterYield_stmt(self, ctx: FandangoParser.Yield_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#yield_stmt.
    def exitYield_stmt(self, ctx: FandangoParser.Yield_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#assert_stmt.
    def enterAssert_stmt(self, ctx: FandangoParser.Assert_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#assert_stmt.
    def exitAssert_stmt(self, ctx: FandangoParser.Assert_stmtContext):
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

    # Enter a parse tree produced by FandangoParser#import_from_targets.
    def enterImport_from_targets(self, ctx: FandangoParser.Import_from_targetsContext):
        pass

    # Exit a parse tree produced by FandangoParser#import_from_targets.
    def exitImport_from_targets(self, ctx: FandangoParser.Import_from_targetsContext):
        pass

    # Enter a parse tree produced by FandangoParser#import_from_as_names.
    def enterImport_from_as_names(
        self, ctx: FandangoParser.Import_from_as_namesContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#import_from_as_names.
    def exitImport_from_as_names(self, ctx: FandangoParser.Import_from_as_namesContext):
        pass

    # Enter a parse tree produced by FandangoParser#import_from_as_name.
    def enterImport_from_as_name(self, ctx: FandangoParser.Import_from_as_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#import_from_as_name.
    def exitImport_from_as_name(self, ctx: FandangoParser.Import_from_as_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#dotted_as_names.
    def enterDotted_as_names(self, ctx: FandangoParser.Dotted_as_namesContext):
        pass

    # Exit a parse tree produced by FandangoParser#dotted_as_names.
    def exitDotted_as_names(self, ctx: FandangoParser.Dotted_as_namesContext):
        pass

    # Enter a parse tree produced by FandangoParser#dotted_as_name.
    def enterDotted_as_name(self, ctx: FandangoParser.Dotted_as_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#dotted_as_name.
    def exitDotted_as_name(self, ctx: FandangoParser.Dotted_as_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#dotted_name.
    def enterDotted_name(self, ctx: FandangoParser.Dotted_nameContext):
        pass

    # Exit a parse tree produced by FandangoParser#dotted_name.
    def exitDotted_name(self, ctx: FandangoParser.Dotted_nameContext):
        pass

    # Enter a parse tree produced by FandangoParser#block.
    def enterBlock(self, ctx: FandangoParser.BlockContext):
        pass

    # Exit a parse tree produced by FandangoParser#block.
    def exitBlock(self, ctx: FandangoParser.BlockContext):
        pass

    # Enter a parse tree produced by FandangoParser#decorators.
    def enterDecorators(self, ctx: FandangoParser.DecoratorsContext):
        pass

    # Exit a parse tree produced by FandangoParser#decorators.
    def exitDecorators(self, ctx: FandangoParser.DecoratorsContext):
        pass

    # Enter a parse tree produced by FandangoParser#class_def.
    def enterClass_def(self, ctx: FandangoParser.Class_defContext):
        pass

    # Exit a parse tree produced by FandangoParser#class_def.
    def exitClass_def(self, ctx: FandangoParser.Class_defContext):
        pass

    # Enter a parse tree produced by FandangoParser#class_def_raw.
    def enterClass_def_raw(self, ctx: FandangoParser.Class_def_rawContext):
        pass

    # Exit a parse tree produced by FandangoParser#class_def_raw.
    def exitClass_def_raw(self, ctx: FandangoParser.Class_def_rawContext):
        pass

    # Enter a parse tree produced by FandangoParser#function_def.
    def enterFunction_def(self, ctx: FandangoParser.Function_defContext):
        pass

    # Exit a parse tree produced by FandangoParser#function_def.
    def exitFunction_def(self, ctx: FandangoParser.Function_defContext):
        pass

    # Enter a parse tree produced by FandangoParser#function_def_raw.
    def enterFunction_def_raw(self, ctx: FandangoParser.Function_def_rawContext):
        pass

    # Exit a parse tree produced by FandangoParser#function_def_raw.
    def exitFunction_def_raw(self, ctx: FandangoParser.Function_def_rawContext):
        pass

    # Enter a parse tree produced by FandangoParser#params.
    def enterParams(self, ctx: FandangoParser.ParamsContext):
        pass

    # Exit a parse tree produced by FandangoParser#params.
    def exitParams(self, ctx: FandangoParser.ParamsContext):
        pass

    # Enter a parse tree produced by FandangoParser#parameters.
    def enterParameters(self, ctx: FandangoParser.ParametersContext):
        pass

    # Exit a parse tree produced by FandangoParser#parameters.
    def exitParameters(self, ctx: FandangoParser.ParametersContext):
        pass

    # Enter a parse tree produced by FandangoParser#slash_no_default.
    def enterSlash_no_default(self, ctx: FandangoParser.Slash_no_defaultContext):
        pass

    # Exit a parse tree produced by FandangoParser#slash_no_default.
    def exitSlash_no_default(self, ctx: FandangoParser.Slash_no_defaultContext):
        pass

    # Enter a parse tree produced by FandangoParser#slash_with_default.
    def enterSlash_with_default(self, ctx: FandangoParser.Slash_with_defaultContext):
        pass

    # Exit a parse tree produced by FandangoParser#slash_with_default.
    def exitSlash_with_default(self, ctx: FandangoParser.Slash_with_defaultContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_etc.
    def enterStar_etc(self, ctx: FandangoParser.Star_etcContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_etc.
    def exitStar_etc(self, ctx: FandangoParser.Star_etcContext):
        pass

    # Enter a parse tree produced by FandangoParser#kwds.
    def enterKwds(self, ctx: FandangoParser.KwdsContext):
        pass

    # Exit a parse tree produced by FandangoParser#kwds.
    def exitKwds(self, ctx: FandangoParser.KwdsContext):
        pass

    # Enter a parse tree produced by FandangoParser#param_no_default.
    def enterParam_no_default(self, ctx: FandangoParser.Param_no_defaultContext):
        pass

    # Exit a parse tree produced by FandangoParser#param_no_default.
    def exitParam_no_default(self, ctx: FandangoParser.Param_no_defaultContext):
        pass

    # Enter a parse tree produced by FandangoParser#param_no_default_star_annotation.
    def enterParam_no_default_star_annotation(
        self, ctx: FandangoParser.Param_no_default_star_annotationContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#param_no_default_star_annotation.
    def exitParam_no_default_star_annotation(
        self, ctx: FandangoParser.Param_no_default_star_annotationContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#param_with_default.
    def enterParam_with_default(self, ctx: FandangoParser.Param_with_defaultContext):
        pass

    # Exit a parse tree produced by FandangoParser#param_with_default.
    def exitParam_with_default(self, ctx: FandangoParser.Param_with_defaultContext):
        pass

    # Enter a parse tree produced by FandangoParser#param_maybe_default.
    def enterParam_maybe_default(self, ctx: FandangoParser.Param_maybe_defaultContext):
        pass

    # Exit a parse tree produced by FandangoParser#param_maybe_default.
    def exitParam_maybe_default(self, ctx: FandangoParser.Param_maybe_defaultContext):
        pass

    # Enter a parse tree produced by FandangoParser#param.
    def enterParam(self, ctx: FandangoParser.ParamContext):
        pass

    # Exit a parse tree produced by FandangoParser#param.
    def exitParam(self, ctx: FandangoParser.ParamContext):
        pass

    # Enter a parse tree produced by FandangoParser#param_star_annotation.
    def enterParam_star_annotation(
        self, ctx: FandangoParser.Param_star_annotationContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#param_star_annotation.
    def exitParam_star_annotation(
        self, ctx: FandangoParser.Param_star_annotationContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#annotation.
    def enterAnnotation(self, ctx: FandangoParser.AnnotationContext):
        pass

    # Exit a parse tree produced by FandangoParser#annotation.
    def exitAnnotation(self, ctx: FandangoParser.AnnotationContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_annotation.
    def enterStar_annotation(self, ctx: FandangoParser.Star_annotationContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_annotation.
    def exitStar_annotation(self, ctx: FandangoParser.Star_annotationContext):
        pass

    # Enter a parse tree produced by FandangoParser#default.
    def enterDefault(self, ctx: FandangoParser.DefaultContext):
        pass

    # Exit a parse tree produced by FandangoParser#default.
    def exitDefault(self, ctx: FandangoParser.DefaultContext):
        pass

    # Enter a parse tree produced by FandangoParser#if_stmt.
    def enterIf_stmt(self, ctx: FandangoParser.If_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#if_stmt.
    def exitIf_stmt(self, ctx: FandangoParser.If_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#elif_stmt.
    def enterElif_stmt(self, ctx: FandangoParser.Elif_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#elif_stmt.
    def exitElif_stmt(self, ctx: FandangoParser.Elif_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#else_block.
    def enterElse_block(self, ctx: FandangoParser.Else_blockContext):
        pass

    # Exit a parse tree produced by FandangoParser#else_block.
    def exitElse_block(self, ctx: FandangoParser.Else_blockContext):
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

    # Enter a parse tree produced by FandangoParser#try_stmt.
    def enterTry_stmt(self, ctx: FandangoParser.Try_stmtContext):
        pass

    # Exit a parse tree produced by FandangoParser#try_stmt.
    def exitTry_stmt(self, ctx: FandangoParser.Try_stmtContext):
        pass

    # Enter a parse tree produced by FandangoParser#except_block.
    def enterExcept_block(self, ctx: FandangoParser.Except_blockContext):
        pass

    # Exit a parse tree produced by FandangoParser#except_block.
    def exitExcept_block(self, ctx: FandangoParser.Except_blockContext):
        pass

    # Enter a parse tree produced by FandangoParser#except_star_block.
    def enterExcept_star_block(self, ctx: FandangoParser.Except_star_blockContext):
        pass

    # Exit a parse tree produced by FandangoParser#except_star_block.
    def exitExcept_star_block(self, ctx: FandangoParser.Except_star_blockContext):
        pass

    # Enter a parse tree produced by FandangoParser#finally_block.
    def enterFinally_block(self, ctx: FandangoParser.Finally_blockContext):
        pass

    # Exit a parse tree produced by FandangoParser#finally_block.
    def exitFinally_block(self, ctx: FandangoParser.Finally_blockContext):
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

    # Enter a parse tree produced by FandangoParser#type_alias.
    def enterType_alias(self, ctx: FandangoParser.Type_aliasContext):
        pass

    # Exit a parse tree produced by FandangoParser#type_alias.
    def exitType_alias(self, ctx: FandangoParser.Type_aliasContext):
        pass

    # Enter a parse tree produced by FandangoParser#type_params.
    def enterType_params(self, ctx: FandangoParser.Type_paramsContext):
        pass

    # Exit a parse tree produced by FandangoParser#type_params.
    def exitType_params(self, ctx: FandangoParser.Type_paramsContext):
        pass

    # Enter a parse tree produced by FandangoParser#type_param_seq.
    def enterType_param_seq(self, ctx: FandangoParser.Type_param_seqContext):
        pass

    # Exit a parse tree produced by FandangoParser#type_param_seq.
    def exitType_param_seq(self, ctx: FandangoParser.Type_param_seqContext):
        pass

    # Enter a parse tree produced by FandangoParser#type_param.
    def enterType_param(self, ctx: FandangoParser.Type_paramContext):
        pass

    # Exit a parse tree produced by FandangoParser#type_param.
    def exitType_param(self, ctx: FandangoParser.Type_paramContext):
        pass

    # Enter a parse tree produced by FandangoParser#type_param_bound.
    def enterType_param_bound(self, ctx: FandangoParser.Type_param_boundContext):
        pass

    # Exit a parse tree produced by FandangoParser#type_param_bound.
    def exitType_param_bound(self, ctx: FandangoParser.Type_param_boundContext):
        pass

    # Enter a parse tree produced by FandangoParser#expressions.
    def enterExpressions(self, ctx: FandangoParser.ExpressionsContext):
        pass

    # Exit a parse tree produced by FandangoParser#expressions.
    def exitExpressions(self, ctx: FandangoParser.ExpressionsContext):
        pass

    # Enter a parse tree produced by FandangoParser#expression.
    def enterExpression(self, ctx: FandangoParser.ExpressionContext):
        pass

    # Exit a parse tree produced by FandangoParser#expression.
    def exitExpression(self, ctx: FandangoParser.ExpressionContext):
        pass

    # Enter a parse tree produced by FandangoParser#yield_expr.
    def enterYield_expr(self, ctx: FandangoParser.Yield_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#yield_expr.
    def exitYield_expr(self, ctx: FandangoParser.Yield_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_expressions.
    def enterStar_expressions(self, ctx: FandangoParser.Star_expressionsContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_expressions.
    def exitStar_expressions(self, ctx: FandangoParser.Star_expressionsContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_expression.
    def enterStar_expression(self, ctx: FandangoParser.Star_expressionContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_expression.
    def exitStar_expression(self, ctx: FandangoParser.Star_expressionContext):
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

    # Enter a parse tree produced by FandangoParser#assignment_expression.
    def enterAssignment_expression(
        self, ctx: FandangoParser.Assignment_expressionContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#assignment_expression.
    def exitAssignment_expression(
        self, ctx: FandangoParser.Assignment_expressionContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#named_expression.
    def enterNamed_expression(self, ctx: FandangoParser.Named_expressionContext):
        pass

    # Exit a parse tree produced by FandangoParser#named_expression.
    def exitNamed_expression(self, ctx: FandangoParser.Named_expressionContext):
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

    # Enter a parse tree produced by FandangoParser#inversion.
    def enterInversion(self, ctx: FandangoParser.InversionContext):
        pass

    # Exit a parse tree produced by FandangoParser#inversion.
    def exitInversion(self, ctx: FandangoParser.InversionContext):
        pass

    # Enter a parse tree produced by FandangoParser#comparison.
    def enterComparison(self, ctx: FandangoParser.ComparisonContext):
        pass

    # Exit a parse tree produced by FandangoParser#comparison.
    def exitComparison(self, ctx: FandangoParser.ComparisonContext):
        pass

    # Enter a parse tree produced by FandangoParser#compare_op_bitwise_or_pair.
    def enterCompare_op_bitwise_or_pair(
        self, ctx: FandangoParser.Compare_op_bitwise_or_pairContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#compare_op_bitwise_or_pair.
    def exitCompare_op_bitwise_or_pair(
        self, ctx: FandangoParser.Compare_op_bitwise_or_pairContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#eq_bitwise_or.
    def enterEq_bitwise_or(self, ctx: FandangoParser.Eq_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#eq_bitwise_or.
    def exitEq_bitwise_or(self, ctx: FandangoParser.Eq_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#noteq_bitwise_or.
    def enterNoteq_bitwise_or(self, ctx: FandangoParser.Noteq_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#noteq_bitwise_or.
    def exitNoteq_bitwise_or(self, ctx: FandangoParser.Noteq_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#lte_bitwise_or.
    def enterLte_bitwise_or(self, ctx: FandangoParser.Lte_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#lte_bitwise_or.
    def exitLte_bitwise_or(self, ctx: FandangoParser.Lte_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#lt_bitwise_or.
    def enterLt_bitwise_or(self, ctx: FandangoParser.Lt_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#lt_bitwise_or.
    def exitLt_bitwise_or(self, ctx: FandangoParser.Lt_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#gte_bitwise_or.
    def enterGte_bitwise_or(self, ctx: FandangoParser.Gte_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#gte_bitwise_or.
    def exitGte_bitwise_or(self, ctx: FandangoParser.Gte_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#gt_bitwise_or.
    def enterGt_bitwise_or(self, ctx: FandangoParser.Gt_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#gt_bitwise_or.
    def exitGt_bitwise_or(self, ctx: FandangoParser.Gt_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#notin_bitwise_or.
    def enterNotin_bitwise_or(self, ctx: FandangoParser.Notin_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#notin_bitwise_or.
    def exitNotin_bitwise_or(self, ctx: FandangoParser.Notin_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#in_bitwise_or.
    def enterIn_bitwise_or(self, ctx: FandangoParser.In_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#in_bitwise_or.
    def exitIn_bitwise_or(self, ctx: FandangoParser.In_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#isnot_bitwise_or.
    def enterIsnot_bitwise_or(self, ctx: FandangoParser.Isnot_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#isnot_bitwise_or.
    def exitIsnot_bitwise_or(self, ctx: FandangoParser.Isnot_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#is_bitwise_or.
    def enterIs_bitwise_or(self, ctx: FandangoParser.Is_bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#is_bitwise_or.
    def exitIs_bitwise_or(self, ctx: FandangoParser.Is_bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#bitwise_or.
    def enterBitwise_or(self, ctx: FandangoParser.Bitwise_orContext):
        pass

    # Exit a parse tree produced by FandangoParser#bitwise_or.
    def exitBitwise_or(self, ctx: FandangoParser.Bitwise_orContext):
        pass

    # Enter a parse tree produced by FandangoParser#bitwise_xor.
    def enterBitwise_xor(self, ctx: FandangoParser.Bitwise_xorContext):
        pass

    # Exit a parse tree produced by FandangoParser#bitwise_xor.
    def exitBitwise_xor(self, ctx: FandangoParser.Bitwise_xorContext):
        pass

    # Enter a parse tree produced by FandangoParser#bitwise_and.
    def enterBitwise_and(self, ctx: FandangoParser.Bitwise_andContext):
        pass

    # Exit a parse tree produced by FandangoParser#bitwise_and.
    def exitBitwise_and(self, ctx: FandangoParser.Bitwise_andContext):
        pass

    # Enter a parse tree produced by FandangoParser#shift_expr.
    def enterShift_expr(self, ctx: FandangoParser.Shift_exprContext):
        pass

    # Exit a parse tree produced by FandangoParser#shift_expr.
    def exitShift_expr(self, ctx: FandangoParser.Shift_exprContext):
        pass

    # Enter a parse tree produced by FandangoParser#sum.
    def enterSum(self, ctx: FandangoParser.SumContext):
        pass

    # Exit a parse tree produced by FandangoParser#sum.
    def exitSum(self, ctx: FandangoParser.SumContext):
        pass

    # Enter a parse tree produced by FandangoParser#term.
    def enterTerm(self, ctx: FandangoParser.TermContext):
        pass

    # Exit a parse tree produced by FandangoParser#term.
    def exitTerm(self, ctx: FandangoParser.TermContext):
        pass

    # Enter a parse tree produced by FandangoParser#factor.
    def enterFactor(self, ctx: FandangoParser.FactorContext):
        pass

    # Exit a parse tree produced by FandangoParser#factor.
    def exitFactor(self, ctx: FandangoParser.FactorContext):
        pass

    # Enter a parse tree produced by FandangoParser#power.
    def enterPower(self, ctx: FandangoParser.PowerContext):
        pass

    # Exit a parse tree produced by FandangoParser#power.
    def exitPower(self, ctx: FandangoParser.PowerContext):
        pass

    # Enter a parse tree produced by FandangoParser#await_primary.
    def enterAwait_primary(self, ctx: FandangoParser.Await_primaryContext):
        pass

    # Exit a parse tree produced by FandangoParser#await_primary.
    def exitAwait_primary(self, ctx: FandangoParser.Await_primaryContext):
        pass

    # Enter a parse tree produced by FandangoParser#primary.
    def enterPrimary(self, ctx: FandangoParser.PrimaryContext):
        pass

    # Exit a parse tree produced by FandangoParser#primary.
    def exitPrimary(self, ctx: FandangoParser.PrimaryContext):
        pass

    # Enter a parse tree produced by FandangoParser#slices.
    def enterSlices(self, ctx: FandangoParser.SlicesContext):
        pass

    # Exit a parse tree produced by FandangoParser#slices.
    def exitSlices(self, ctx: FandangoParser.SlicesContext):
        pass

    # Enter a parse tree produced by FandangoParser#slice.
    def enterSlice(self, ctx: FandangoParser.SliceContext):
        pass

    # Exit a parse tree produced by FandangoParser#slice.
    def exitSlice(self, ctx: FandangoParser.SliceContext):
        pass

    # Enter a parse tree produced by FandangoParser#atom.
    def enterAtom(self, ctx: FandangoParser.AtomContext):
        pass

    # Exit a parse tree produced by FandangoParser#atom.
    def exitAtom(self, ctx: FandangoParser.AtomContext):
        pass

    # Enter a parse tree produced by FandangoParser#group.
    def enterGroup(self, ctx: FandangoParser.GroupContext):
        pass

    # Exit a parse tree produced by FandangoParser#group.
    def exitGroup(self, ctx: FandangoParser.GroupContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambdef.
    def enterLambdef(self, ctx: FandangoParser.LambdefContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambdef.
    def exitLambdef(self, ctx: FandangoParser.LambdefContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_params.
    def enterLambda_params(self, ctx: FandangoParser.Lambda_paramsContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_params.
    def exitLambda_params(self, ctx: FandangoParser.Lambda_paramsContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_parameters.
    def enterLambda_parameters(self, ctx: FandangoParser.Lambda_parametersContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_parameters.
    def exitLambda_parameters(self, ctx: FandangoParser.Lambda_parametersContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_slash_no_default.
    def enterLambda_slash_no_default(
        self, ctx: FandangoParser.Lambda_slash_no_defaultContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_slash_no_default.
    def exitLambda_slash_no_default(
        self, ctx: FandangoParser.Lambda_slash_no_defaultContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_slash_with_default.
    def enterLambda_slash_with_default(
        self, ctx: FandangoParser.Lambda_slash_with_defaultContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_slash_with_default.
    def exitLambda_slash_with_default(
        self, ctx: FandangoParser.Lambda_slash_with_defaultContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_star_etc.
    def enterLambda_star_etc(self, ctx: FandangoParser.Lambda_star_etcContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_star_etc.
    def exitLambda_star_etc(self, ctx: FandangoParser.Lambda_star_etcContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_kwds.
    def enterLambda_kwds(self, ctx: FandangoParser.Lambda_kwdsContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_kwds.
    def exitLambda_kwds(self, ctx: FandangoParser.Lambda_kwdsContext):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_param_no_default.
    def enterLambda_param_no_default(
        self, ctx: FandangoParser.Lambda_param_no_defaultContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_param_no_default.
    def exitLambda_param_no_default(
        self, ctx: FandangoParser.Lambda_param_no_defaultContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_param_with_default.
    def enterLambda_param_with_default(
        self, ctx: FandangoParser.Lambda_param_with_defaultContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_param_with_default.
    def exitLambda_param_with_default(
        self, ctx: FandangoParser.Lambda_param_with_defaultContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_param_maybe_default.
    def enterLambda_param_maybe_default(
        self, ctx: FandangoParser.Lambda_param_maybe_defaultContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_param_maybe_default.
    def exitLambda_param_maybe_default(
        self, ctx: FandangoParser.Lambda_param_maybe_defaultContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#lambda_param.
    def enterLambda_param(self, ctx: FandangoParser.Lambda_paramContext):
        pass

    # Exit a parse tree produced by FandangoParser#lambda_param.
    def exitLambda_param(self, ctx: FandangoParser.Lambda_paramContext):
        pass

    # Enter a parse tree produced by FandangoParser#fstring_middle.
    def enterFstring_middle(self, ctx: FandangoParser.Fstring_middleContext):
        pass

    # Exit a parse tree produced by FandangoParser#fstring_middle.
    def exitFstring_middle(self, ctx: FandangoParser.Fstring_middleContext):
        pass

    # Enter a parse tree produced by FandangoParser#fstring_replacement_field.
    def enterFstring_replacement_field(
        self, ctx: FandangoParser.Fstring_replacement_fieldContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#fstring_replacement_field.
    def exitFstring_replacement_field(
        self, ctx: FandangoParser.Fstring_replacement_fieldContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#fstring_conversion.
    def enterFstring_conversion(self, ctx: FandangoParser.Fstring_conversionContext):
        pass

    # Exit a parse tree produced by FandangoParser#fstring_conversion.
    def exitFstring_conversion(self, ctx: FandangoParser.Fstring_conversionContext):
        pass

    # Enter a parse tree produced by FandangoParser#fstring_full_format_spec.
    def enterFstring_full_format_spec(
        self, ctx: FandangoParser.Fstring_full_format_specContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#fstring_full_format_spec.
    def exitFstring_full_format_spec(
        self, ctx: FandangoParser.Fstring_full_format_specContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#fstring_format_spec.
    def enterFstring_format_spec(self, ctx: FandangoParser.Fstring_format_specContext):
        pass

    # Exit a parse tree produced by FandangoParser#fstring_format_spec.
    def exitFstring_format_spec(self, ctx: FandangoParser.Fstring_format_specContext):
        pass

    # Enter a parse tree produced by FandangoParser#fstring.
    def enterFstring(self, ctx: FandangoParser.FstringContext):
        pass

    # Exit a parse tree produced by FandangoParser#fstring.
    def exitFstring(self, ctx: FandangoParser.FstringContext):
        pass

    # Enter a parse tree produced by FandangoParser#string.
    def enterString(self, ctx: FandangoParser.StringContext):
        pass

    # Exit a parse tree produced by FandangoParser#string.
    def exitString(self, ctx: FandangoParser.StringContext):
        pass

    # Enter a parse tree produced by FandangoParser#strings.
    def enterStrings(self, ctx: FandangoParser.StringsContext):
        pass

    # Exit a parse tree produced by FandangoParser#strings.
    def exitStrings(self, ctx: FandangoParser.StringsContext):
        pass

    # Enter a parse tree produced by FandangoParser#list.
    def enterList(self, ctx: FandangoParser.ListContext):
        pass

    # Exit a parse tree produced by FandangoParser#list.
    def exitList(self, ctx: FandangoParser.ListContext):
        pass

    # Enter a parse tree produced by FandangoParser#tuple.
    def enterTuple(self, ctx: FandangoParser.TupleContext):
        pass

    # Exit a parse tree produced by FandangoParser#tuple.
    def exitTuple(self, ctx: FandangoParser.TupleContext):
        pass

    # Enter a parse tree produced by FandangoParser#set.
    def enterSet(self, ctx: FandangoParser.SetContext):
        pass

    # Exit a parse tree produced by FandangoParser#set.
    def exitSet(self, ctx: FandangoParser.SetContext):
        pass

    # Enter a parse tree produced by FandangoParser#dict.
    def enterDict(self, ctx: FandangoParser.DictContext):
        pass

    # Exit a parse tree produced by FandangoParser#dict.
    def exitDict(self, ctx: FandangoParser.DictContext):
        pass

    # Enter a parse tree produced by FandangoParser#double_starred_kvpairs.
    def enterDouble_starred_kvpairs(
        self, ctx: FandangoParser.Double_starred_kvpairsContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#double_starred_kvpairs.
    def exitDouble_starred_kvpairs(
        self, ctx: FandangoParser.Double_starred_kvpairsContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#double_starred_kvpair.
    def enterDouble_starred_kvpair(
        self, ctx: FandangoParser.Double_starred_kvpairContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#double_starred_kvpair.
    def exitDouble_starred_kvpair(
        self, ctx: FandangoParser.Double_starred_kvpairContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#kvpair.
    def enterKvpair(self, ctx: FandangoParser.KvpairContext):
        pass

    # Exit a parse tree produced by FandangoParser#kvpair.
    def exitKvpair(self, ctx: FandangoParser.KvpairContext):
        pass

    # Enter a parse tree produced by FandangoParser#for_if_clauses.
    def enterFor_if_clauses(self, ctx: FandangoParser.For_if_clausesContext):
        pass

    # Exit a parse tree produced by FandangoParser#for_if_clauses.
    def exitFor_if_clauses(self, ctx: FandangoParser.For_if_clausesContext):
        pass

    # Enter a parse tree produced by FandangoParser#for_if_clause.
    def enterFor_if_clause(self, ctx: FandangoParser.For_if_clauseContext):
        pass

    # Exit a parse tree produced by FandangoParser#for_if_clause.
    def exitFor_if_clause(self, ctx: FandangoParser.For_if_clauseContext):
        pass

    # Enter a parse tree produced by FandangoParser#listcomp.
    def enterListcomp(self, ctx: FandangoParser.ListcompContext):
        pass

    # Exit a parse tree produced by FandangoParser#listcomp.
    def exitListcomp(self, ctx: FandangoParser.ListcompContext):
        pass

    # Enter a parse tree produced by FandangoParser#setcomp.
    def enterSetcomp(self, ctx: FandangoParser.SetcompContext):
        pass

    # Exit a parse tree produced by FandangoParser#setcomp.
    def exitSetcomp(self, ctx: FandangoParser.SetcompContext):
        pass

    # Enter a parse tree produced by FandangoParser#genexp.
    def enterGenexp(self, ctx: FandangoParser.GenexpContext):
        pass

    # Exit a parse tree produced by FandangoParser#genexp.
    def exitGenexp(self, ctx: FandangoParser.GenexpContext):
        pass

    # Enter a parse tree produced by FandangoParser#dictcomp.
    def enterDictcomp(self, ctx: FandangoParser.DictcompContext):
        pass

    # Exit a parse tree produced by FandangoParser#dictcomp.
    def exitDictcomp(self, ctx: FandangoParser.DictcompContext):
        pass

    # Enter a parse tree produced by FandangoParser#arguments.
    def enterArguments(self, ctx: FandangoParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by FandangoParser#arguments.
    def exitArguments(self, ctx: FandangoParser.ArgumentsContext):
        pass

    # Enter a parse tree produced by FandangoParser#args.
    def enterArgs(self, ctx: FandangoParser.ArgsContext):
        pass

    # Exit a parse tree produced by FandangoParser#args.
    def exitArgs(self, ctx: FandangoParser.ArgsContext):
        pass

    # Enter a parse tree produced by FandangoParser#arg.
    def enterArg(self, ctx: FandangoParser.ArgContext):
        pass

    # Exit a parse tree produced by FandangoParser#arg.
    def exitArg(self, ctx: FandangoParser.ArgContext):
        pass

    # Enter a parse tree produced by FandangoParser#kwargs.
    def enterKwargs(self, ctx: FandangoParser.KwargsContext):
        pass

    # Exit a parse tree produced by FandangoParser#kwargs.
    def exitKwargs(self, ctx: FandangoParser.KwargsContext):
        pass

    # Enter a parse tree produced by FandangoParser#starred_expression.
    def enterStarred_expression(self, ctx: FandangoParser.Starred_expressionContext):
        pass

    # Exit a parse tree produced by FandangoParser#starred_expression.
    def exitStarred_expression(self, ctx: FandangoParser.Starred_expressionContext):
        pass

    # Enter a parse tree produced by FandangoParser#kwarg_or_starred.
    def enterKwarg_or_starred(self, ctx: FandangoParser.Kwarg_or_starredContext):
        pass

    # Exit a parse tree produced by FandangoParser#kwarg_or_starred.
    def exitKwarg_or_starred(self, ctx: FandangoParser.Kwarg_or_starredContext):
        pass

    # Enter a parse tree produced by FandangoParser#kwarg_or_double_starred.
    def enterKwarg_or_double_starred(
        self, ctx: FandangoParser.Kwarg_or_double_starredContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#kwarg_or_double_starred.
    def exitKwarg_or_double_starred(
        self, ctx: FandangoParser.Kwarg_or_double_starredContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#star_targets.
    def enterStar_targets(self, ctx: FandangoParser.Star_targetsContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_targets.
    def exitStar_targets(self, ctx: FandangoParser.Star_targetsContext):
        pass

    # Enter a parse tree produced by FandangoParser#star_targets_list_seq.
    def enterStar_targets_list_seq(
        self, ctx: FandangoParser.Star_targets_list_seqContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#star_targets_list_seq.
    def exitStar_targets_list_seq(
        self, ctx: FandangoParser.Star_targets_list_seqContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#star_targets_tuple_seq.
    def enterStar_targets_tuple_seq(
        self, ctx: FandangoParser.Star_targets_tuple_seqContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#star_targets_tuple_seq.
    def exitStar_targets_tuple_seq(
        self, ctx: FandangoParser.Star_targets_tuple_seqContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#star_target.
    def enterStar_target(self, ctx: FandangoParser.Star_targetContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_target.
    def exitStar_target(self, ctx: FandangoParser.Star_targetContext):
        pass

    # Enter a parse tree produced by FandangoParser#target_with_star_atom.
    def enterTarget_with_star_atom(
        self, ctx: FandangoParser.Target_with_star_atomContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#target_with_star_atom.
    def exitTarget_with_star_atom(
        self, ctx: FandangoParser.Target_with_star_atomContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#star_atom.
    def enterStar_atom(self, ctx: FandangoParser.Star_atomContext):
        pass

    # Exit a parse tree produced by FandangoParser#star_atom.
    def exitStar_atom(self, ctx: FandangoParser.Star_atomContext):
        pass

    # Enter a parse tree produced by FandangoParser#single_target.
    def enterSingle_target(self, ctx: FandangoParser.Single_targetContext):
        pass

    # Exit a parse tree produced by FandangoParser#single_target.
    def exitSingle_target(self, ctx: FandangoParser.Single_targetContext):
        pass

    # Enter a parse tree produced by FandangoParser#single_subscript_attribute_target.
    def enterSingle_subscript_attribute_target(
        self, ctx: FandangoParser.Single_subscript_attribute_targetContext
    ):
        pass

    # Exit a parse tree produced by FandangoParser#single_subscript_attribute_target.
    def exitSingle_subscript_attribute_target(
        self, ctx: FandangoParser.Single_subscript_attribute_targetContext
    ):
        pass

    # Enter a parse tree produced by FandangoParser#t_primary.
    def enterT_primary(self, ctx: FandangoParser.T_primaryContext):
        pass

    # Exit a parse tree produced by FandangoParser#t_primary.
    def exitT_primary(self, ctx: FandangoParser.T_primaryContext):
        pass

    # Enter a parse tree produced by FandangoParser#del_targets.
    def enterDel_targets(self, ctx: FandangoParser.Del_targetsContext):
        pass

    # Exit a parse tree produced by FandangoParser#del_targets.
    def exitDel_targets(self, ctx: FandangoParser.Del_targetsContext):
        pass

    # Enter a parse tree produced by FandangoParser#del_target.
    def enterDel_target(self, ctx: FandangoParser.Del_targetContext):
        pass

    # Exit a parse tree produced by FandangoParser#del_target.
    def exitDel_target(self, ctx: FandangoParser.Del_targetContext):
        pass

    # Enter a parse tree produced by FandangoParser#del_t_atom.
    def enterDel_t_atom(self, ctx: FandangoParser.Del_t_atomContext):
        pass

    # Exit a parse tree produced by FandangoParser#del_t_atom.
    def exitDel_t_atom(self, ctx: FandangoParser.Del_t_atomContext):
        pass

    # Enter a parse tree produced by FandangoParser#type_expressions.
    def enterType_expressions(self, ctx: FandangoParser.Type_expressionsContext):
        pass

    # Exit a parse tree produced by FandangoParser#type_expressions.
    def exitType_expressions(self, ctx: FandangoParser.Type_expressionsContext):
        pass

    # Enter a parse tree produced by FandangoParser#func_type_comment.
    def enterFunc_type_comment(self, ctx: FandangoParser.Func_type_commentContext):
        pass

    # Exit a parse tree produced by FandangoParser#func_type_comment.
    def exitFunc_type_comment(self, ctx: FandangoParser.Func_type_commentContext):
        pass


del FandangoParser
