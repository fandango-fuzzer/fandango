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
        if ctx.python_tag():
            self.visitChildren(ctx.python_tag())
        elif ctx.compound_stmt():
            self.python_code.append(ctx.compound_stmt())

    def visitSimple_stmts(self, ctx: FandangoParser.Simple_stmtsContext):
        self.python_code.append(ctx)

    def visitCompound_stmt(self, ctx: FandangoParser.Compound_stmtContext):
        self.python_code.append(ctx)
