import ast
import os
import sys
from typing import Optional
from antlr4.tree.Tree import ParseTree

import fandango
from fandango.constraints import predicates
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.language.parse.convert import (
    ConstraintProcessor,
    GrammarProcessor,
    PythonProcessor,
)
from fandango.language.parse.splitter import FandangoSplitter
from fandango.logger import LOGGER


class FandangoSpec:
    """
    Helper class to pickle and unpickle parsed Fandango specifications.
    This is necessary because the ANTLR4 parse trees cannot be pickled,
    so we pickle the code text, grammar, and constraints instead.
    """

    GLOBALS = predicates.__dict__
    LOCALS = None  # Must be None to ensure top-level imports

    def __init__(
        self,
        tree: ParseTree,
        fan_contents: str,
        lazy: bool = False,
        filename: str = "<input_>",
        max_repetitions: int = 5,
        used_symbols: set[str] = set(),
        includes: Optional[list[str]] = None,
    ) -> None:
        self.version = fandango.version()
        self.fan_contents = fan_contents
        self.global_vars = self.GLOBALS.copy()
        self.local_vars = self.LOCALS
        self.lazy = lazy

        LOGGER.debug(f"{filename}: extracting code")
        splitter = FandangoSplitter(
            filename=filename, includes=includes, used_symbols=used_symbols
        )
        splitter.visit(tree)
        python_processor = PythonProcessor()
        code_tree = python_processor.get_code(splitter.python_code)
        ast.fix_missing_locations(code_tree)
        self.code_text = ast.unparse(code_tree)

        LOGGER.debug(f"{filename}: code text:\n{self.code_text}")

        LOGGER.debug(f"{filename}: running code")
        self.run_code(filename=filename)

        LOGGER.debug(f"{filename}: extracting grammar")
        grammar_processor = GrammarProcessor(
            splitter.grammar_settings,
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            id_prefix="{0:x}".format(abs(hash(filename))),
            max_repetitions=max_repetitions,
        )
        self.grammar = grammar_processor.get_grammar(splitter.productions, prime=False)

        LOGGER.debug(f"{filename}: extracting constraints")
        constraint_processor = ConstraintProcessor(
            self.grammar,
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            lazy=self.lazy,
        )
        self.constraints: list[Constraint | SoftValue] = (
            constraint_processor.get_constraints(splitter.constraints)
        )
        self.constraints.extend(grammar_processor.repetition_constraints)

        for generator in self.grammar.generators.values():
            for nonterminal in generator.nonterminals.values():
                used_symbols.add(nonterminal.symbol.name())

    def run_code(self, filename: str = "<input_>") -> None:
        # Ensure the directory of the file is in the path
        dirname = os.path.dirname(filename)
        if dirname not in sys.path:
            sys.path.append(dirname)

        # Set up environment as if this were a top-level script
        self.global_vars.update(
            {
                "__name__": "__main__",
                "__file__": filename,
                "__package__": None,
                "__spec__": None,
            }
        )
        exec(self.code_text, self.global_vars, self.local_vars)

    def __repr__(self) -> str:
        s = self.code_text
        if s:
            s += "\n\n"
        s += str(self.grammar) + "\n"
        if self.constraints:
            s += "\n"
        s += "\n".join(
            "where " + constraint.format_as_spec() for constraint in self.constraints
        )
        return s
