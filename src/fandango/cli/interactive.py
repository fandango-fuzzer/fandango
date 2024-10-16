import ast
import enum
import os.path
from typing import Optional

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.error.ErrorStrategy import BailErrorStrategy
from selenium.webdriver.support.expected_conditions import element_attribute_to_include

from fandango.constraints import predicates
from fandango.constraints.fitness import GeneticBase
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    PythonProcessor,
    ConstraintProcessor,
)
from fandango.language.grammar import Grammar
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.symbol import NonTerminal


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
    START = "start"

    def usage(self):
        return {
            InteractiveCommands.EXIT: "exit",
            InteractiveCommands.HELP: "help [<command>]",
            InteractiveCommands.RULES: "rule [<rule>]",
            InteractiveCommands.CONSTRAINTS: "constraint [<constraint>]",
            InteractiveCommands.PYTHON: "python [<code>]",
            InteractiveCommands.TEST: "test[-<identifier>][-<non-terminal>] <string>",
            InteractiveCommands.FUZZ: "fuzz",
            InteractiveCommands.SHOW: "show [<non-terminal> | <identifier>]",
            InteractiveCommands.DEL: "del <identifier>",
            InteractiveCommands.CLEAR: "clear",
            InteractiveCommands.START: "start <non-terminal>",
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
            InteractiveCommands.START: "Set the start symbol for fuzzing and testing, defaults to <start>",
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
        self._global_vars = {}
        self._local_vars = predicates.__dict__
        self._python_processor = PythonProcessor()
        exec(
            ast.unparse(self._python_processor.get_code(self._splitter.python_code)),
            self._global_vars,
            self._local_vars,
        )
        self._grammar_processor = GrammarProcessor(
            local_variables=self._local_vars, global_variables=self._global_vars
        )
        self._grammar: Grammar = self._grammar_processor.get_grammar(
            self._splitter.productions
        )
        self._constraint_processor = ConstraintProcessor(
            self._grammar,
            local_variables=self._local_vars,
            global_variables=self._global_vars,
            lazy=lazy,
        )
        constraints = self._constraint_processor.get_constraints(
            self._splitter.constraints
        )
        self.constraints_identifier = 0
        self._constraints = {}
        for constraint in constraints:
            self._add_constraint(constraint)

        self._fandango = None
        self._updated_grammar = False
        self._updated_constraints = False
        self._start_symbol = NonTerminal("<start>")

    def _rule(self, rule: str, single: bool = False):
        parser = FandangoParser(CommonTokenStream(FandangoLexer(InputStream(rule))))
        parser._errHandler = BailErrorStrategy()
        if single:
            grammar = self._grammar_processor.get_grammar([parser.production()])
        else:
            self._splitter.visit(parser.fandango())
            grammar = self._grammar_processor.get_grammar(self._splitter.productions)
        self._grammar.update(grammar)
        self._updated_grammar = True

    def _add_constraint(self, constraint: GeneticBase):
        self._constraints[self.constraints_identifier] = constraint
        self.constraints_identifier += 1

    def _constraint(self, constraint: str, single: bool = False):
        parser = FandangoParser(
            CommonTokenStream(FandangoLexer(InputStream(constraint)))
        )
        parser._errHandler = BailErrorStrategy()
        if single:
            new_constraints = self._constraint_processor.get_constraints(
                [parser.constraint()]
            )
        else:
            self._splitter.visit(parser.fandango())
            new_constraints = self._constraint_processor.get_constraints(
                self._splitter.constraints
            )
        for constraint in new_constraints:
            self._add_constraint(constraint)
        self._updated_constraints = True

    def _python(self, python: str):
        exec(
            python,
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

    @staticmethod
    def _help(command: Optional[str] = None):
        if command:
            if command in {c.value for c in InteractiveCommands}:
                command = InteractiveCommands(command)
                print(f"Help for {command.value}\n" f"{command.help()}\n")
            else:
                print(f"Command '{command}' not found")

        else:
            print(
                f"Commands: {', '.join([c.value for c in InteractiveCommands])}\n\n"
                f"Type 'help <command>' for more information about a command"
            )

    def _show(self, element: Optional[str] = None):
        if element is None:
            print("Rules:")
            print(self._grammar)
            print("Constraints:")
            for identifier, constraint in self._constraints.items():
                print(f"{identifier}: {constraint}")
        elif element.startswith("<") and element.endswith(">"):
            if element in self._grammar:
                print(self._grammar.get_repr_for_rule(element))
            else:
                print("Non-terminal not found in grammar")
        else:
            try:
                print(self._constraints[int(element)])
            except ValueError:
                print("Invalid identifier")
            except KeyError:
                print("Constraint not found")

    def _test(
        self,
        string: str,
        identifier: Optional[str] = None,
        non_terminal: Optional[str] = None,
    ):
        if identifier:
            try:
                constraints = [self._constraints[int(identifier)]]
            except ValueError:
                print("Invalid identifier")
                return
            except KeyError:
                print("Constraint not found")
                return
        else:
            constraints = list(self._constraints.values())
        if self._updated_grammar:
            self._updated_grammar = False
        if non_terminal:
            start = NonTerminal(non_terminal)
        else:
            start = self._start_symbol
        tree = self._grammar.parse(string, start)
        if tree is None:
            print(f"Failed to parse string from start symbol {start}")
            return
        for constraint in constraints:
            print(
                ("PASSED" if constraint.fitness(tree).success else "FAILED")
                + f" {constraint}"
            )

    def _start(self, non_terminal: str):
        self._start_symbol = NonTerminal(non_terminal)

    def run(self):
        try:
            while True:
                command = input(">>> ").lstrip()
                if command.startswith(InteractiveCommands.EXIT.value):
                    break
                elif command.startswith(InteractiveCommands.HELP.value):
                    command = command.split(" ")
                    if len(command) == 1:
                        self._help()
                    else:
                        self._help(command[1])
                elif command.startswith(InteractiveCommands.RULES.value):
                    command = command.split(" ", 1)
                    if len(command) == 1:
                        rule = ""
                        while True:
                            rule += input("... ")
                            rule += "\n"
                            if rule.endswith("\n\n"):
                                break
                        self._rule(rule)
                    else:
                        self._rule(command[1])
                elif command.startswith(InteractiveCommands.CONSTRAINTS.value):
                    command = command.split(" ", 1)
                    if len(command) == 1:
                        constraint = ""
                        while True:
                            constraint += input("... ")
                            constraint += "\n"
                            if constraint.endswith("\n\n"):
                                break
                        self._constraint(constraint)
                    else:
                        self._constraint(command[1])
                elif command.startswith(InteractiveCommands.PYTHON.value):
                    command = command.split(" ", 1)
                    if len(command) == 1:
                        python = ""
                        while True:
                            python += input("... ")
                            python += "\n"
                            if python.endswith("\n\n"):
                                break
                        self._python(python)
                    else:
                        self._python(command[1])
                elif command.startswith(InteractiveCommands.TEST.value):
                    command = command.split(" ", 1)
                    if len(command) == 1:
                        print("Missing string")
                    else:
                        test = command[0].split("-")
                        if len(test) == 3:
                            self._test(command[1], test[1], test[2])
                        elif len(test) == 2:
                            if test[1].isdigit():
                                self._test(command[1], test[1])
                            else:
                                self._test(command[1], None, test[1])
                        else:
                            self._test(command[1])
                elif command.startswith(InteractiveCommands.FUZZ.value):
                    pass
                elif command.startswith(InteractiveCommands.SHOW.value):
                    command = command.split(" ", 1)
                    if len(command) == 1:
                        self._show()
                    else:
                        self._show(command[1])
                elif command.startswith(InteractiveCommands.DEL.value):
                    command = command.split(" ")
                    if len(command) == 1:
                        print("Missing identifier")
                    else:
                        self._del(int(command[1]))
                elif command.startswith(InteractiveCommands.CLEAR.value):
                    self._clear()
                elif command.startswith(InteractiveCommands.START.value):
                    command = command.split(" ")
                    if len(command) == 1:
                        print("Missing non-terminal")
                    else:
                        self._start(command[1])
                else:
                    print(f"Command not found {command}")
        except KeyboardInterrupt:
            pass
