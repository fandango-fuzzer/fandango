from typing import Optional, Any

from fandango.language.parse.spec import FandangoSpec
from fandango.language.parse.cache import (
    load_from_cache,
    store_in_cache,
)
from fandango.language.parse.parse_tree import parse_tree
from fandango.language.parse.slice_parties import slice_parties
from fandango.logger import LOGGER


def parse_content(
    fan_contents: str,
    *,
    filename: str = "<input_>",
    use_cache: bool = True,
    lazy: bool = False,
    parties: Optional[list[str]] = None,
    max_repetitions: int = 5,
    includes: Optional[list[str]] = None,
    used_symbols: set[str] = set(),
    pyenv_globals: Optional[dict[str, Any]] = None,
    pyenv_locals: Optional[dict[str, Any]] = None,
) -> FandangoSpec:
    """
    Parse given content into a grammar and constraints.
    This is a helper function; use `parse()` as the main entry point.
    :param fan_contents: Fandango specification text
    :param filename: The file name of the content (for error messages)
    :param use_cache: If True (default), cache parsing results
    :param includes: A list of directories to search for include files
    :param parties: If given, list of parties to consider in the grammar
    :param lazy: If True, the constraints are evaluated lazily
    :return: A FandangoSpec object containing the parsed grammar, constraints, and code text.
    """
    spec: Optional[FandangoSpec] = None
    use_cache = False  # Todo enable again

    if use_cache:
        spec = load_from_cache(fan_contents, filename)

    if not spec:
        tree = parse_tree(filename, fan_contents)

        spec = FandangoSpec(
            tree,
            fan_contents,
            lazy,
            filename=filename,
            max_repetitions=max_repetitions,
            includes=includes,
            used_symbols=used_symbols,
            pyenv_globals=pyenv_globals,
            pyenv_locals=pyenv_locals,
        )
        if use_cache:
            store_in_cache(spec, fan_contents, filename)

    if parties:
        slice_parties(spec.grammar, set(parties), ignore_receivers=True)

    LOGGER.debug(f"{filename}: parsing complete")
    return spec
