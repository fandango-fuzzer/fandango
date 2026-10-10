import os
import platform
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

from xdg_base_dirs import xdg_data_dirs, xdg_data_home

from fandango.language.parse.parse_tree import parse_tree
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.parser.FandangoParserVisitor import FandangoParserVisitor
from fandango.logger import LOGGER


def search_dirs(
    file_to_be_included: Path,
    include_dirs: Iterable[Path] = (),
    file_dirs: Iterable[Path] = (),
) -> list[Path]:
    """The directories `include()` searches for a file, best first.

    This is the order documented in `docs/Including.md`. It matters whenever the same
    relative name exists in more than one of them (say, a copy next to your spec and one
    installed for everyone): the first directory that has the file wins.

    `include_dirs` are the directories given with `-I`; `file_dirs` are the directories
    of the files being included from, the innermost first.
    """
    dirs: list[Path] = list(include_dirs)

    if os.environ.get("FANDANGO_PATH"):
        dirs.extend(Path(dir) for dir in os.environ["FANDANGO_PATH"].split(os.pathsep))

    dirs.append(file_to_be_included.resolve().parent)
    dirs.extend(file_dirs)

    if platform.system() == "Darwin":
        dirs.append(Path.home() / "Library" / "Fandango")  # ~/Library/Fandango
    dirs.append(xdg_data_home() / "fandango")  # sth like ~/.local/share/fandango

    if platform.system() == "Darwin":
        dirs.append(Path("/Library/Fandango"))  # /Library/Fandango
    dirs.extend(
        dir / "fandango" for dir in xdg_data_dirs()
    )  # sth like /usr/local/share/fandango

    return list(dict.fromkeys(dirs))  # a directory listed twice is searched once


def read_file(
    file_to_be_included: Path,
    include_dirs: Iterable[Path] = (),
    file_dirs: Iterable[Path] = (),
) -> str:
    dirs = search_dirs(file_to_be_included, include_dirs, file_dirs)

    for dir in dirs:
        full_file_name = dir / file_to_be_included
        if not full_file_name.exists():
            continue
        with full_file_name.open("r", encoding="utf-8") as full_file:
            LOGGER.debug(f"{file_to_be_included}: including {full_file_name}")
            return full_file.read()

    raise FileNotFoundError(
        f"{file_to_be_included!r} not found in {os.pathsep.join(str(dir) for dir in dirs)}"
    )


class FandangoSplitter(FandangoParserVisitor):
    def __init__(
        self,
        filename: str,
        used_symbols: set[str],
        includes: Optional[Iterable[str | Path]] = None,
        depth: int = 0,
        file_dirs: Optional[Iterable[Path]] = None,
    ) -> None:
        self._filename = filename
        # The directories given with `-I`, in the order given
        self._includes = [Path(include) for include in (includes or [])]
        self._depth = depth
        self._used_symbols: set[str] = used_symbols or set()
        # The directories of the files being included from, the innermost first
        self._file_dirs: list[Path] = []
        dirname = Path(filename).parent
        if dirname != Path("."):
            self._file_dirs.append(dirname)
        self._file_dirs.extend(file_dirs or [])

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
        contents = read_file(
            Path(filename), include_dirs=self._includes, file_dirs=self._file_dirs
        )
        inner = FandangoSplitter(
            filename=filename,
            used_symbols=self._used_symbols,
            includes=self._includes,
            depth=self._depth + 1,
            file_dirs=self._file_dirs,
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
