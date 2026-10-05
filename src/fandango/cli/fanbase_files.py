"""The `-F` option: Fandango specs from Fanbase.

`-F png` is `-f png.fan` for the spec `png` in the Fanbase registry. The spec is fetched
into Fandango's standard library location (where `include()` looks) when it is missing or
out of date, so later runs, and `include("png/png.fan")`, find it there. The registry is
the one Fanbase's `find_registry` picks: `$FANBASE_REGISTRY`, else the public one.
"""

import argparse
import importlib.util
import io
import sys
from pathlib import Path
from typing import Any

from fandango.errors import FandangoError
from fandango.logger import LOGGER


class _SpecFile(io.StringIO):
    """A spec read into memory, so that no file stays open. Its name is the spec's path."""

    def __init__(self, path: Path) -> None:
        super().__init__(path.read_text(encoding="utf-8"))
        self.name = str(path)


def resolve_fanbase_files(args: argparse.Namespace) -> None:
    """Turn `-F NAME` options into spec files in `args.fan_files`.

    Since the format is known, this also sets the file name extension, and for `fuzz`,
    where to write the files if neither `-o` nor `-d` was given.
    """
    names = getattr(args, "fanbase_files", None)
    if not names:
        return

    try:
        from fanbase.manager import ensure
        from fanbase.registry import RegistryError
    except ImportError as exc:
        raise FandangoError(
            "'-F' needs the Fanbase client; install it with: pip install fanbase"
        ) from exc

    specs = []
    for name in names:
        try:
            spec = ensure(name)
        except RegistryError as exc:
            raise FandangoError(f"-F {name}: {exc}") from exc
        _check_requires(spec)
        _report(spec)
        specs.append(spec)

    # Fanbase specs come first, so that a spec given with -f can override their rules
    args.fan_files = [_SpecFile(spec.path) for spec in specs] + list(
        args.fan_files or []
    )
    args.fanbase_files = None  # done; do not fetch again if args are used twice

    extensions = specs[0].extensions
    if getattr(args, "filename_extension", None) is None and extensions:
        args.filename_extension = "." + extensions[0].lstrip(".")

    if _writes_files_by_default(args):
        args.directory = _free_directory(f"{names[0]}-inputs")
        if LOGGER.getEffectiveLevel() <= 30:  # not with -qq
            print(f"Writing inputs to {args.directory}/", file=sys.stderr)


def _check_requires(spec: Any) -> None:
    """Python packages a spec imports must be installed before Fandango loads it."""
    missing = [
        name
        for name in spec.requires
        if importlib.util.find_spec(name.split(".")[0]) is None
    ]
    if missing:
        raise FandangoError(
            f"-F {spec}: the spec needs Python packages that are not installed: "
            f"pip install {' '.join(missing)}"
        )


def _report(spec: Any) -> None:
    if spec.status in ("installed", "updated"):
        print(f"Fanbase: {spec.status} {spec} in {spec.path.parent}", file=sys.stderr)
    elif spec.status == "offline":
        LOGGER.warning(
            f"Fanbase registry not reachable; using installed copy of {spec}"
        )
    else:
        LOGGER.info(f"Fanbase: {spec} is up to date")


def _writes_files_by_default(args: argparse.Namespace) -> bool:
    """Binary formats are useless on a terminal: with no -o, -d or program, write files."""
    return (
        getattr(args, "command", None) == "fuzz"
        and not getattr(args, "output", None)
        and not getattr(args, "directory", None)
        and not getattr(args, "test_command", None)
        and getattr(args, "format", "string") != "none"
    )


def _free_directory(base: str) -> str:
    """`base`, or `base-2`, `base-3`, ... – the first that does not exist yet."""
    candidate, n = base, 1
    while Path(candidate).exists():
        n += 1
        candidate = f"{base}-{n}"
    return candidate
