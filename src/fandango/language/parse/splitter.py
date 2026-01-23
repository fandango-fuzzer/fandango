import os
from pathlib import Path
import platform
from typing import Optional

from antlr4.tree.Tree import ParseTree
from fandango.language.parse.parse_tree import parse_tree
from xdg_base_dirs import xdg_data_dirs, xdg_data_home

from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.parser.FandangoParserVisitor import FandangoParserVisitor
from fandango.logger import LOGGER


def read_file(file_to_be_included: str, includes: set[str]) -> str:
    path = os.path.dirname(file_to_be_included)
    if not path:
        # If the current file has no path, use the current directory
        path = "."
    if os.environ.get("FANDANGO_PATH"):
        path += ":" + os.environ["FANDANGO_PATH"]
    dirs = {Path(dir) for dir in path.split(":")}
    dirs |= {Path(dir) for dir in includes}

    if platform.system() == "Darwin":
        dirs |= {Path.home() / "Library" / "Fandango"}  # ~/Library/Fandango
        dirs |= {Path("/Library/Fandango")}  # /Library/Fandango

    dirs |= {xdg_data_home() / "fandango"}  # sth like ~/.local/share/fandango
    dirs |= {
        dir / "fandango" for dir in xdg_data_dirs()
    }  # sth like /usr/local/share/fandango

    for dir in dirs:
        full_file_name = dir / file_to_be_included
        if not os.path.exists(full_file_name):
            continue
        with open(full_file_name, "r") as full_file:
            LOGGER.debug(f"{file_to_be_included}: including {full_file_name}")
            return full_file.read()

    raise FileNotFoundError(
        f"{file_to_be_included!r} not found in {':'.join(str(dir) for dir in dirs)}"
    )


class FandangoSplitter(FandangoParserVisitor):
    def __init__(
        self,
        filename: str,
        used_symbols: set[str],
        includes: Optional[list[str] | set[str]] = None,
        depth: int = 0,
    ) -> None:
        self._filename = filename
        self._includes = set(includes) if includes is not None else set()
        self._depth = depth
        self._used_symbols: set[str] = used_symbols or set()
        dirname = os.path.dirname(filename)
        if dirname:
            self._includes.add(dirname)

        # depth, production
        self.productions: list[FandangoParser.ProductionContext] = []
        self.constraints: list[FandangoParser.ConstraintContext] = []
        self.grammar_settings: list[FandangoParser.Grammar_setting_contentContext] = []
        self.python_code: list[FandangoParser.PythonContext] = []

    def visitFandango(self, ctx: FandangoParser.FandangoContext) -> None:
        self.productions = []
        self.constraints = []
        self.grammar_settings = []
        self.python_code = []
        self.visitChildren(ctx)

    def visitProduction(self, ctx: FandangoParser.ProductionContext) -> None:
        if self._depth > 0:
            self._used_symbols.add(ctx.nonterminal().getText())  # type: ignore[no-untyped-call] # antlr4 doesn't provide types
        self.productions.append(ctx)

    def visitInclude(self, ctx: FandangoParser.IncludeContext) -> None:
        filename = ctx.STRING().getText()  # type: ignore[no-untyped-call] # antlr4 doesn't provide types"
        filename = filename[
            1:-1
        ]  # remove quotes, assume we're just using simple quotes
        contents = read_file(filename, includes=self._includes)
        inner = FandangoSplitter(
            filename=filename,
            used_symbols=self._used_symbols,
            includes=self._includes,
            depth=self._depth + 1,
        )
        tree = parse_tree(filename, contents)
        inner.visit(tree)

        self.productions = inner.productions + self.productions
        self.constraints = inner.constraints + self.constraints
        self.grammar_settings = inner.grammar_settings + self.grammar_settings
        self.python_code = inner.python_code + self.python_code

    def visitConstraint(self, ctx: FandangoParser.ConstraintContext) -> None:
        self.constraints.append(ctx)

    def visitGrammar_setting_content(
        self, ctx: FandangoParser.Grammar_setting_contentContext
    ) -> None:
        self.grammar_settings.append(ctx)

    def visitPython(self, ctx: FandangoParser.PythonContext) -> None:
        self.python_code.append(ctx)
