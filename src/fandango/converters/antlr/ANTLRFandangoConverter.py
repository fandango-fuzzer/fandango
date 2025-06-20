#!/usr/bin/env python

import sys
from typing import Any

from antlr4 import *

from fandango.converters.FandangoConverter import FandangoConverter
from fandango.converters.antlr.ANTLRv4Lexer import ANTLRv4Lexer
from fandango.converters.antlr.ANTLRv4Parser import ANTLRv4Parser
from fandango.converters.antlr.ANTLRv4ParserVisitor import ANTLRv4ParserVisitor
from fandango.language.parse import PythonAntlrErrorListener


class ANTLRFandangoConverterVisitor(ANTLRv4ParserVisitor):
    def strip_quotes(self, s: str) -> str:
        """Strip quotes from a string."""
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        elif s.startswith("'") and s.endswith("'"):
            return s[1:-1]
        return s

    def invert_range(self, range_str: str) -> str:
        """Invert a character range string."""
        if range_str.startswith("[") and range_str.endswith("]"):
            content = range_str[1:-1]
            if content.startswith("^"):
                content = content[1:]  # Remove the negation
            else:
                content = "^" + content  # Add negation
            return f"[{content}]"

        self.addNote(f"cannot invert {range_str}")
        return "not " + range_str  # Cannot handle

    def quote(self, s: str) -> str:
        """Quote a string if it is not already quoted."""
        if "'" in s and '"' in s:
            return f'"""{s}"""'
        if "'" in s:
            return f'"{s}"'
        return f"'{s}'"

    def rquote(self, s: str) -> str:
        return "r" + self.quote(s)

    def addNote(self, message: str):
        """Add a note to the current rule"""
        if getattr(self, "notes", None) is None:
            self.notes = []
        self.notes.append(message)

    def getNotes(self) -> str:
        """Retrieve notes for current rule"""
        if getattr(self, "notes", None) is None:
            self.notes = []
        if not self.notes:
            return ""
        s = "  # NOTE: " + "; ".join(self.notes)
        self.notes = []
        return s

    def visitChildren(self, ctx: Any, sep: str = "", altEmpty: str = "") -> str:
        """Visit all children of a context `ctx`. Separate them with `sep`. If they evaluate to an empty string, use `altEmpty` instead."""
        if ctx is None or ctx.children is None:
            return ""

        children_s = []
        for child in ctx.children or []:
            s = self.visit(child)
            if s == "":
                s = altEmpty
            if s:
                children_s.append(s)
        return sep.join(children_s)

    def visitGrammarDecl(self, ctx: ANTLRv4Parser.GrammarDeclContext):
        return "# " + ctx.identifier().getText() + "\n"

    def visitParserRuleSpec(self, ctx: ANTLRv4Parser.ParserRuleSpecContext):
        if ctx.ruleModifiers():
            self.addNote(f"had modifier(s) '{ctx.ruleModifiers().getText()}'")
        if ctx.argActionBlock():
            self.addNote(f"had action block {ctx.argActionBlock().getText()}")
        if ctx.ruleReturns():
            self.addNote(f"had 'returns' clause {ctx.ruleReturns().getText()}")
        if ctx.throwsSpec():
            self.addNote(f"had 'throws' clause {ctx.throwsSpec().getText()}")
        if ctx.rulePrequel():
            self.addNote(f"had rule prequel '{ctx.rulePrequel().getText()}'")
        if ctx.exceptionGroup() and ctx.exceptionGroup().getText():
            self.addNote(f"had exception group '{ctx.exceptionGroup().getText()}'")

        nonterminal = ctx.RULE_REF().getText()
        return (
            f"<{nonterminal}> ::= " + self.visitChildren(ctx) + self.getNotes() + "\n"
        )

    def visitRuleAltList(self, ctx: ANTLRv4Parser.RuleAltListContext):
        return self.visitChildren(ctx, sep=" | ", altEmpty="''")

    def visitAltList(self, ctx: ANTLRv4Parser.AltListContext):
        return self.visitChildren(ctx, sep=" | ", altEmpty="''")

    def visitAlternative(self, ctx: ANTLRv4Parser.AlternativeContext):
        return self.visitChildren(ctx, sep=" ")

    def visitLexerAltList(self, ctx: ANTLRv4Parser.LexerAltListContext):
        return self.visitChildren(ctx, sep=" | ")

    def visitEbnf(self, ctx: ANTLRv4Parser.EbnfContext):
        if ctx.blockSuffix():
            return self.visit(ctx.block()) + self.visit(ctx.blockSuffix())
        return super().visitEbnf(ctx)

    def visitElement(self, ctx: ANTLRv4Parser.ElementContext):
        s = ""
        if ctx.labeledElement():
            s = self.visit(ctx.labeledElement())
        if ctx.atom():
            s = self.visit(ctx.atom())
        if ctx.ebnf():
            s = self.visit(ctx.ebnf())
        if ctx.actionBlock():
            s = self.visit(ctx.actionBlock())
        if ctx.ebnfSuffix():
            s += self.visit(ctx.ebnfSuffix())
        return s

    def visitWildcard(self, ctx: ANTLRv4Parser.WildcardContext):
        return self.rquote(".")

    def visitEbnfSuffix(self, ctx: ANTLRv4Parser.EbnfSuffixContext):
        suffix = ctx.getText() if ctx else ""
        if len(suffix) > 1:
            # ANTLR has non-greedy suffixes such as *? and +?
            self.addNote(f"was '{suffix}'")
            suffix = suffix[0]
        return suffix

    def visitLexerRuleSpec(self, ctx: ANTLRv4Parser.LexerRuleSpecContext):
        # This method can be customized to handle rule specifications
        nonterminal = ctx.TOKEN_REF().getText()
        return (
            f"<{nonterminal}> ::= " + self.visitChildren(ctx) + self.getNotes() + "\n"
        )

    def visitRuleref(self, ctx: ANTLRv4Parser.RulerefContext):
        rule_name = ctx.RULE_REF().getText()
        return f"<{rule_name}>"

    def visitTerminalDef(self, ctx: ANTLRv4Parser.TerminalDefContext):
        if ctx.STRING_LITERAL():
            terminal = ctx.STRING_LITERAL().getText()
            return f"{terminal}"
        elif ctx.TOKEN_REF():
            token = ctx.TOKEN_REF().getText()
            return f"<{token}>"
        # elif ctx.LEXER_CHAR_SET():
        #     char_set = ctx.LEXER_CHAR_SET().getText()
        #     return f"{char_set}"
        else:
            elem = ctx.getText()
            return f"{elem}"

    def visitLexerElement(self, ctx: ANTLRv4Parser.LexerElementContext):
        if ctx.actionBlock():
            self.visit(ctx.actionBlock())

        s = ""
        if ctx.lexerAtom():
            s = self.visit(ctx.lexerAtom())
        if ctx.lexerBlock():
            s = self.visit(ctx.lexerBlock())
        if ctx.ebnfSuffix():
            s += self.visit(ctx.ebnfSuffix())
        return s

    def visitActionBlock(self, ctx: ANTLRv4Parser.ActionBlockContext):
        self.addNote(f"was {ctx.getText()}")
        return super().visitActionBlock(ctx)

    def visitLexerCommand(self, ctx: ANTLRv4Parser.LexerCommandContext):
        self.addNote(f"was '-> {ctx.getText()}'")
        return super().visitLexerCommand(ctx)

    def visitPredicateOption(self, ctx):
        self.addNote(f"was '{ctx.getText()}'")
        return super().visitPredicateOption(ctx)

    def visitElementOption(self, ctx):
        self.addNote(f"was '{ctx.getText()}'")
        return super().visitElementOption(ctx)

    def visitLexerElements(self, ctx: ANTLRv4Parser.LexerElementsContext):
        return self.visitChildren(ctx, sep=" ")

    def visitLexerBlock(self, ctx: ANTLRv4Parser.LexerBlockContext):
        return "(" + super().visitLexerBlock(ctx) + ")"

    def visitBlockSet(self, ctx: ANTLRv4Parser.BlockSetContext):
        return "(" + super().visitBlockSet(ctx) + ")"

    def visitBlock(self, ctx: ANTLRv4Parser.BlockContext):
        if ctx.ruleAction():
            self.addNote(f"action was {ctx.ruleAction().getText()}")
        return "(" + super().visitBlock(ctx) + ")"

    def visitLexerAtom(self, ctx: ANTLRv4Parser.LexerAtomContext):
        if ctx.LEXER_CHAR_SET():
            return self.rquote(ctx.LEXER_CHAR_SET().getText())
        return super().visitLexerAtom(ctx)

    def visitCharacterRange(self, ctx: ANTLRv4Parser.CharacterRangeContext):
        range_start = self.strip_quotes(ctx.STRING_LITERAL(0).getText())
        range_end = self.strip_quotes(ctx.STRING_LITERAL(1).getText())
        return self.rquote(f"[{range_start}-{range_end}]")

    def visitNotSet(self, ctx: ANTLRv4Parser.NotSetContext):
        if ctx.setElement():
            return self.rquote(self.invert_range(ctx.setElement().getText()))
        if ctx.blockSet():
            return self.rquote(self.invert_range(ctx.blockSet().getText()))
        return super().visitChildren(ctx)

    def visitTerminal(self, node: TerminalNode):
        return super().visitTerminal(node)


class ANTLRFandangoConverter(FandangoConverter):
    """Convert ANTLR4 grammar to Fandango format."""

    def __init__(self, filename: str):
        """Initialize with given grammar file"""
        super().__init__(filename)

    def to_fan(self, **kw_args) -> str:
        """Convert the grammar spec to Fandango format"""
        # Read the grammar spec
        input_stream = FileStream(self.filename)
        error_listener = PythonAntlrErrorListener(self.filename)

        lexer = ANTLRv4Lexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)

        stream = CommonTokenStream(lexer)
        parser = ANTLRv4Parser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        # Start parsing at the 'grammarSpec' rule
        tree = parser.grammarSpec()

        # Create a visitor and evaluate the expression
        converter = ANTLRFandangoConverterVisitor()
        spec = converter.visit(tree)

        header = f"""# Automatically generated from {self.filename!r}.
#
"""
        return header + spec


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        converter = ANTLRFandangoConverter(filename)
        print(converter.to_fan(), end="")
