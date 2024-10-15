import ast
import enum
import os.path
from typing import Optional

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.error.ErrorStrategy import BailErrorStrategy

from fandango.constraints import predicates
from fandango.constraints.fitness import GeneticBase
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    PythonProcessor,
    ConstraintProcessor,
)
from fandango.language.earley import Parser
from fandango.language.grammar import Grammar
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser


class InteractiveCommands(enum.Enum):
    EXIT = "exit"
    HELP = "help"
    RULES = "rule"
    CONSTRAINTS = "constraint"
    PYTHON = "python"
    TEST = "test"
    FUZZ = "fuzz"
    SHOW = "show"
    DEL = "del"
    CLEAR = "clear"

    def usage(self):
        return {
            InteractiveCommands.EXIT: "exit",
            InteractiveCommands.HELP: "help [<command>]",
            InteractiveCommands.RULES: "rule [<rule>]",
            InteractiveCommands.CONSTRAINTS: "constraint [<constraint>]",
            InteractiveCommands.PYTHON: "python [<code>]",
            InteractiveCommands.TEST: "test [<identifier>] [<non-terminal>] <string>",
            InteractiveCommands.FUZZ: "fuzz",
            InteractiveCommands.SHOW: "show [<non-terminal> | <identifier>]",
            InteractiveCommands.DEL: "del <identifier>",
            InteractiveCommands.CLEAR: "clear",
        }[self]

    def description(self):
        return {
            InteractiveCommands.EXIT: "Exit the interactive mode",
            InteractiveCommands.HELP: "Show help for a command if specified, otherwise show all commands",
            InteractiveCommands.RULES: "Add or update a rule. If no rule is specified, this command will open a stream "
            "where you can write multiple rules (terminate with two newlines)",
            InteractiveCommands.CONSTRAINTS: "Add a constraint. If no constraint is specified, this command will open "
            "a stream where you can write multiple constraints "
            "(terminate with two newlines)",
            InteractiveCommands.PYTHON: "Add or update a python code. If no code is specified, this command will open "
            "a stream where you can write multiple python code "
            "(terminate with two newlines)",
            InteractiveCommands.TEST: "Test a string against the current specification. If an identifier is specified"
            ", the constraint with that identifier will be used for testing, otherwise all "
            "constraints will be used. If a non-terminal is specified, the string will be "
            "interpreted as a derivation tree from that non-terminal instead of the start "
            "symbol",
            InteractiveCommands.FUZZ: "Fuzz a string from the current specification",
            InteractiveCommands.SHOW: "Show the rule for a non-terminal or the constraint with the specified "
            "identifier. If no argument is specified, show all rules and constraints",
            InteractiveCommands.DEL: "Delete a constraint with the specified identifier",
            InteractiveCommands.CLEAR: "Clear all rules, constraints and python code",
        }[self]

    def help(self):
        return f"usage: {self.usage()} \n\n    {self.description()}"


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
        self._global_vars = {}
        self._local_vars = predicates.__dict__
        self._python_processor = PythonProcessor()
        exec(
            ast.unparse(self._python_processor.get_code(self._splitter.python_code)),
            self._global_vars,
            self._local_vars,
        )
        self._constraint_processor = ConstraintProcessor(
            self._grammar, self._local_vars, self._global_vars, lazy=lazy
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

    def _update_python(self, python: str):
        exec(
            ast.unparse(python),
            self._global_vars,
            self._local_vars,
        )

    def _del(self, identifier: int):
        del self._constraints[identifier]

    def _clear(self):
        self._constraints = {}
        self.constraints_identifier = 0
        self._grammar = Grammar.dummy()
        self._fandango = None
        self._updated_grammar = False
        self._updated_constraints = False
        self._local_vars = predicates.__dict__
        self._global_vars = {}

    def _help(self, command: Optional[str] = None):
        if command:
            if command in InteractiveCommands:
                command = InteractiveCommands[command]
                print(f"Help for {command.value}\n" f"{command.description()}\n")
            else:
                print(f"Command '{command}' not found")

        else:
            print(
                f"Commands: {', '.join(InteractiveCommands.__dict__.values())}\n"
                f"Type 'help <command>' for more information about a command"
            )

    def run(self):
        pass
