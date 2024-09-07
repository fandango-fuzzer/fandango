from typing import List

from cssselect2.parser import AttributeSelector

from fandango.constraints.base import ConjunctionConstraint, DisjunctionConstraint
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
from fandango.language.search import AttributeSearch, RuleSearch


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


class ConstraintProcessor(FandangoParserVisitor):
    def __init__(self):
        self.searches = SearchProcessor()

    def get_constraints(self, constraints: List[FandangoParser.ConstraintContext]):
        return ConjunctionConstraint(
            [self.visit(constraint) for constraint in constraints]
        )

    def visitConstraint(self, ctx: FandangoParser.ConstraintContext):
        return self.visit(ctx.implies())

    def visitImplies(self, ctx: FandangoParser.ImpliesContext):
        return self.visit(ctx.quantifier())

    def visitQuantifier(self, ctx: FandangoParser.QuantifierContext):
        if ctx.disjunction():
            return self.visit(ctx.disjunction())

    def visitDisjunction(self, ctx: FandangoParser.DisjunctionContext):
        return DisjunctionConstraint(
            [self.visit(constraint) for constraint in ctx.conjunction()]
        )

    def visitConjunction(self, ctx: FandangoParser.ConjunctionContext):
        return ConjunctionConstraint(
            [self.visit(constraint) for constraint in ctx.formula_atom()]
        )

    def visitFormula_atom(self, ctx: FandangoParser.Formula_atomContext):
        if ctx.implies():
            return self.visit(ctx.implies())
        elif ctx.expression:
            return self.visit(ctx.expression())
        elif ctx.formula_comparison():
            return self.visit(ctx.formula_comparison())
        else:
            raise ValueError(f"Unknown formula atom: {ctx.getText()}")

    def visitExpression(self, ctx: FandangoParser.ExpressionContext):
        if ctx.selector():
            expr, searches = self.searches.visit(ctx.selector())
        elif ctx.expr():
            expr, searches = self.searches.visit(ctx.expr())
        else:
            raise ValueError(f"Unknown expression: {ctx.getText()}")


class SearchProcessor(FandangoParserVisitor):
    def defaultResult(self):
        return []

    def aggregateResult(self, aggregate, nextResult):
        return aggregate + nextResult

    def visitSelector(self, ctx: FandangoParser.SelectorContext):
        if ctx.selector():
            return [
                AttributeSearch(
                    self.visit(ctx.selector()), self.visit(ctx.selection()), None
                )
            ]
        else:
            return self.visit(ctx.selection())

    def visitSelection(self, ctx: FandangoParser.SelectionContext):
        return [RuleSearch(NonTerminal(ctx.RULE_NAME().getText()), None)]
