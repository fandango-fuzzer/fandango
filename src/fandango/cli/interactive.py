import ast
import os.path
from typing import Optional

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.error.ErrorStrategy import BailErrorStrategy

from fandango.constraints import predicates
from fandango.constraints.fitness import GeneticBase
from fandango.evolution.algorithm import FANDANGO
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    PythonProcessor,
    ConstraintProcessor,
)
from fandango.language.earley import Parser
from fandango.language.grammar import Grammar
from fandango.language.parse import parse
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser


class InteractiveCommands:
    EXIT = "exit"
    HELP = "help"
    RULES = "rule"
    CONSTRAINTS = "constraint"
    PYTHON = "python"
    TEST = "test"
    FUZZ = "fuzz"
    LIST = "list"
    SHOW = "show"


class Interactive:
    def __init__(
        self,
        fan: Optional[str] = None,
        grammar: Optional[str] = None,
        constraints: Optional[str] = None,
        python: Optional[str] = None,
        lazy: bool = False,
    ):
        if fan:
            if os.path.exists(fan):
                with open(fan, "r") as file:
                    fan_contents = file.read()
            else:
                fan_contents = fan
        else:
            fan_contents = ""
            if grammar:
                if os.path.exists(grammar):
                    with open(grammar, "r") as file:
                        fan_contents += file.read()
                else:
                    fan_contents += grammar
            if constraints:
                if os.path.exists(constraints):
                    with open(constraints, "r") as file:
                        fan_contents += file.read()
                else:
                    fan_contents += constraints
            if python:
                if os.path.exists(python):
                    with open(python, "r") as file:
                        fan_contents += file.read()
                else:
                    fan_contents += python
        parser = FandangoParser(
            CommonTokenStream(FandangoLexer(InputStream(fan_contents)))
        )
        parser._errHandler = BailErrorStrategy()
        tree = parser.fandango()
        self._splitter = FandangoSplitter()
        self._splitter.visit(tree)
        self._grammar_processor = GrammarProcessor()
        self._grammar: Grammar = self._grammar_processor.get_grammar(
            self._splitter.productions
        )
        global_vars = {}
        local_vars = predicates.__dict__
        self._python_processor = PythonProcessor()
        exec(
            ast.unparse(self._python_processor.get_code(self._splitter.python_code)),
            global_vars,
            local_vars,
        )
        self._constraint_processor = ConstraintProcessor(
            self._grammar, local_vars, global_vars, lazy=lazy
        )
        constraints = self._constraint_processor.get_constraints(
            self._splitter.constraints
        )
        self.constraints_identifier = 0
        self._constraints = {}
        for constraint in constraints:
            self._add_constraint(constraint)

        self._parser = Parser(self._grammar)
        self._fandango = None
        self._updated_grammar = False
        self._updated_constraints = False

    def _update_grammar(self, rule: str):
        parser = FandangoParser(CommonTokenStream(FandangoLexer(InputStream(rule))))
        parser._errHandler = BailErrorStrategy()
        grammar = self._grammar_processor.get_grammar([parser.production()])
        self._grammar.update(grammar)
        self._updated_grammar = True

    def _add_constraint(self, constraint: GeneticBase):
        self._constraints[self.constraints_identifier] = constraint
        self.constraints_identifier += 1

    def _update_constraints(self, constraint: str):
        parser = FandangoParser(
            CommonTokenStream(FandangoLexer(InputStream(constraint)))
        )
        parser._errHandler = BailErrorStrategy()
        tree = parser.constraint()
        new_constraints = self._constraint_processor.get_constraints(tree)
        for constraint in new_constraints:
            self._add_constraint(constraint)
        self._updated_constraints = True

    def run(self):
        pass
