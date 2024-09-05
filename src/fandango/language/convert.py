from typing import List

from fandango.language.grammar import (
    Grammar,
    Alternative,
    Concatenation,
    Star,
    NonTerminal,
    CharSet,
    Terminal,
)
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.parser.FandangoParserVisitor import FandangoParserVisitor


class FandangoSplitter(FandangoParserVisitor):
    def __init__(self):
        self.productions = []
        self.constraints = []
        self.python_code = []

    def visitProduction(self, ctx: FandangoParser.ProductionContext):
        self.productions.append(ctx)

    def visitConstraint(self, ctx: FandangoParser.ConstraintContext):
        self.constraints.append(ctx)

    def visitPython(self, ctx: FandangoParser.PythonContext):
        self.visitChildren(ctx.python_tag())

    def visitSimple_stmts(self, ctx: FandangoParser.Simple_stmtsContext):
        self.python_code.append(ctx)

    def visitCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        self.python_code.append(ctx)


class GrammarProcessor(FandangoParserVisitor):
    def get_grammar(self, productions: List[FandangoParser.ProductionContext]):
        rules = {}
        for production in productions:
            rules[production.RULE_NAME().getText()] = self.visit(
                production.alternative()
            )
        return Grammar(rules)

    def visitAlternative(self, ctx: FandangoParser.AlternativeContext):
        return Alternative([self.visit(child) for child in ctx.concatenation()])

    def visitConcatenation(self, ctx: FandangoParser.ConcatenationContext):
        return Concatenation([self.visit(child) for child in ctx.operator()])

    def visitKleene(self, ctx: FandangoParser.KleeneContext):
        return Star(self.visit(ctx.symbol()))

    def visitSymbol(self, ctx: FandangoParser.SymbolContext):
        if ctx.RULE_NAME():
            return NonTerminal(ctx.RULE_NAME().getText())
        elif ctx.STRING():
            return Terminal.from_symbol(ctx.STRING().getText())
        elif ctx.char_set():
            return CharSet(ctx.char_set().getText())
        elif ctx.alternative():
            return self.visit(ctx.alternative())
        else:
            raise ValueError(f"Unknown symbol: {ctx.getText()}")
