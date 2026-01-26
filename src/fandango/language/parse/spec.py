import ast
import hashlib
import os
import pickle
import sys
import time
import uuid
import warnings
from pathlib import Path
from typing import Optional, Any

import cachedir_tag
from antlr4.tree.Tree import ParseTree

import fandango
from fandango.constraints import predicates
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.io import CURRENT_ENV_KEY
from fandango.language.parse.cache import get_cache_dir
from fandango.language.parse.convert import (
    ConstraintProcessor,
    GrammarProcessor,
    PythonProcessor,
)
from fandango.language.parse.splitter import FandangoSplitter
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.logger import LOGGER, print_exception


class FandangoSpec:
    """
    Helper class to pickle and unpickle parsed Fandango specifications.
    This is necessary because the ANTLR4 parse trees cannot be pickled,
    so we pickle the code text, grammar, and constraints instead.
    """

    def __init__(
        self,
        lazy: bool = False,
        filename: str = "<input_>",
        code_text: str = "",
        max_repetitions: int = 5,
        used_symbols: set[str] = set(),
        productions_ctx: list[FandangoParser.ProductionContext] = [],
        constraints_ctx: list[FandangoParser.ConstraintContext] = [],
        grammar_settings_ctx: list[FandangoParser.Grammar_setting_contentContext] = [],
        pyenv_globals: Optional[dict[str, Any]] = None,
        pyenv_locals: Optional[dict[str, Any]] = None,
    ) -> None:
        if pyenv_globals is None:
            env_key = uuid.uuid4()
            assert CURRENT_ENV_KEY.contextVar is not None
            CURRENT_ENV_KEY.contextVar.set(env_key)
            pyenv_globals = predicates.__dict__.copy()

        if pyenv_locals is None:
            pyenv_locals = dict()

        self.version = fandango.version()
        self.lazy = lazy
        self.code_text = code_text
        self.local_vars = pyenv_locals
        self.global_vars = pyenv_globals

        LOGGER.debug(f"{filename}: running code")
        self.run_code(filename=filename)

        LOGGER.debug(f"{filename}: extracting grammar")
        grammar_processor = GrammarProcessor(
            grammar_settings_ctx,
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            id_prefix="{0:x}".format(abs(hash(filename))),
            max_repetitions=max_repetitions,
        )
        self.grammar = grammar_processor.get_grammar(productions_ctx, prime=False)

        LOGGER.debug(f"{filename}: extracting constraints")
        constraint_processor = ConstraintProcessor(
            self.grammar,
            local_variables=self.local_vars,
            global_variables=self.global_vars,
            lazy=self.lazy,
        )
        self.constraints: list[Constraint | SoftValue] = (
            constraint_processor.get_constraints(constraints_ctx)
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
        exec(self.code_text, self.global_vars)

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


class CachedFandangoSpec:
    """
    A FandangoSpec that is loaded from a cache.
    It does not run the code again upon unpickling.
    """

    def __init__(
        self,
        tree: ParseTree,
        fan_contents: str,
        lazy: bool = False,
        filename: str = "<input_>",
        max_repetitions: int = 5,
        used_symbols: Optional[set[str]] = None,
        includes: Optional[list[str]] = None,
    ):
        if used_symbols is None:
            used_symbols = set()
        self.version = fandango.version()
        self.fan_contents = fan_contents
        self.lazy = lazy
        self.filename = filename
        self.max_repetitions = max_repetitions
        self.used_symbols = used_symbols

        LOGGER.debug(f"{filename}: extracting code")
        splitter = FandangoSplitter(
            filename=filename, includes=includes, used_symbols=used_symbols
        )
        splitter.visit(tree)
        python_processor = PythonProcessor()
        code_tree = python_processor.get_code(splitter.python_code)
        ast.fix_missing_locations(code_tree)

        self.code_text = ast.unparse(code_tree)
        self.grammar_settings = splitter.grammar_settings
        self.productions = splitter.productions
        self.constraints = splitter.constraints

    def to_spec(
        self,
        pyenv_globals: Optional[dict[str, Any]] = None,
        pyenv_locals: Optional[dict[str, Any]] = None,
    ) -> FandangoSpec:
        return FandangoSpec(
            lazy=self.lazy,
            filename=self.filename,
            max_repetitions=self.max_repetitions,
            used_symbols=self.used_symbols,
            pyenv_globals=pyenv_globals,
            pyenv_locals=pyenv_locals,
            code_text=self.code_text,
            productions_ctx=self.productions,
            grammar_settings_ctx=self.grammar_settings,
            constraints_ctx=self.constraints,
        )

    @classmethod
    def load(cls, fan_contents: str, filename: str) -> Optional[CachedFandangoSpec]:
        pickle_file = cls.get_pickle_file(fan_contents)

        if os.path.exists(pickle_file):
            try:
                with open(pickle_file, "rb") as fp:
                    LOGGER.info(f"{filename}: loading cached spec from {pickle_file}")
                    start_time = time.time()
                    with warnings.catch_warnings():
                        warnings.simplefilter(
                            "ignore", DeprecationWarning
                        )  # for some reason, unpickling triggers the deprecation warnings in __getattr__ of DerivationTree and TreeValue
                        spec = pickle.load(fp)
                    assert spec is not None
                    LOGGER.debug(f"Cached spec version: {spec.version}")
                    if spec.fan_contents != fan_contents:
                        error = fandango.FandangoValueError(
                            "Hash collision (If you get this, you'll be real famous)"
                        )
                        raise error

                    LOGGER.debug(
                        f"{filename}: loaded from cache in {time.time() - start_time:.2f} seconds"
                    )
                    assert isinstance(spec, CachedFandangoSpec)
                    return spec
            except Exception as exc:
                print_exception(exc)
        return None

    def persist(self, fan_contents: str, filename: str) -> None:
        pickle_file = self.get_pickle_file(fan_contents)
        LOGGER.info(f"{filename}: saving spec to cache {pickle_file}")
        try:
            with open(pickle_file, "wb") as fp:
                pickle.dump(self, fp)
        except Exception as e:
            print_exception(e)
            try:
                os.remove(pickle_file)  # might be inconsistent
            except Exception:
                pass

    @classmethod
    def get_pickle_file(cls, fan_contents: str) -> Path:
        cache_dir = get_cache_dir()
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, mode=0o700, exist_ok=True)
            cachedir_tag.tag(
                cache_dir, application="Fandango"
            )  # type: ignore[no-untyped-call] # cachedir_tag doesn't provide types

        # Keep separate hashes for different Fandango and Python versions
        hash_contents = fan_contents + fandango.version() + "-" + sys.version
        hash = hashlib.sha256(hash_contents.encode()).hexdigest()
        return cache_dir / (hash + ".pickle")
