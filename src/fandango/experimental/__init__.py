"""Import-time warnings for all modules under ``fandango.experimental``.

Why this exists:
- Experimental modules are not API-stable and should emit a warning when used.
- We want this behavior to be centralized, not duplicated in every submodule.

How it works:
- Install a meta path finder that intercepts imports for
  ``fandango.experimental.*``.
- The first time anything under ``fandango.experimental.<child>`` is loaded
  (including deeper modules such as ``...experimental.execution.fcc``), emit
  one warning for ``fandango.experimental.<child>``.
- De-dup via an in-process set so each direct child namespace warns at most once.
"""

import importlib.abc
import importlib.machinery
import sys
import warnings
from collections.abc import Iterable, Sequence
from types import ModuleType

from fandango.logger import LOGGER

_SUBMODULE_PREFIX = f"{__name__}."


class ExperimentalWarning(UserWarning):
    pass


# Canonical names ``fandango.experimental.<child>`` that have already warned.
_WARNED_CHILD_NAMESPACES: set[str] = set()


def dont_warn_about_module(module_name: str) -> None:
    LOGGER.info(f"Enabled (skipped warning of) experimental module {module_name}")
    _WARNED_CHILD_NAMESPACES.add(_SUBMODULE_PREFIX + module_name)


def _child_namespace_for(fullname: str) -> str | None:
    """Return ``fandango.experimental.<child>`` for any module under that subtree."""
    if not fullname.startswith(_SUBMODULE_PREFIX):
        return None
    rest = fullname.removeprefix(_SUBMODULE_PREFIX)
    if not rest:
        return None
    child = rest.split(".", 1)[0]
    return f"{__name__}.{child}"


def warn_experimental_import(module_name: str) -> None:
    """Emit a one-time warning for the given experimental child namespace."""
    if module_name in _WARNED_CHILD_NAMESPACES:
        return

    _WARNED_CHILD_NAMESPACES.add(module_name)
    warnings.warn(
        (
            f"`{module_name}` is experimental and may change without notice. "
            "Avoid relying on its public API in production code."
        ),
        category=ExperimentalWarning,
        stacklevel=3,
    )


class _ExperimentalSubmoduleWarningLoader(importlib.abc.Loader):
    """Loader wrapper that warns, then delegates to the original loader."""

    def __init__(self, wrapped_loader: importlib.abc.Loader, fullname: str):
        self._wrapped_loader = wrapped_loader
        self._fullname = fullname

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> ModuleType | None:
        if hasattr(self._wrapped_loader, "create_module"):
            return self._wrapped_loader.create_module(spec)
        return None

    def exec_module(self, module: ModuleType) -> None:
        ns = _child_namespace_for(self._fullname)
        if ns is not None:
            warn_experimental_import(ns)
        self._wrapped_loader.exec_module(module)


class _ExperimentalSubmoduleWarningFinder(importlib.abc.MetaPathFinder):
    """Finder that targets ``fandango.experimental.*`` submodule imports."""

    def find_spec(
        self,
        fullname: str,
        path: Iterable[str] | None,
        target: ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        # Ignore non-experimental imports as early as possible.
        if not fullname.startswith(_SUBMODULE_PREFIX):
            return None

        # Delegate actual module resolution to PathFinder.
        # mypy and beartype disagree on the exact type we should use here
        assert isinstance(path, Sequence)
        spec = importlib.machinery.PathFinder.find_spec(fullname, path)
        if spec is None or spec.loader is None:
            return spec

        # Replace the loader so we can emit the warning just before execution.
        spec.loader = _ExperimentalSubmoduleWarningLoader(spec.loader, fullname)
        return spec


# Register exactly one finder instance to avoid repeated wrapping.
if not any(
    isinstance(finder, _ExperimentalSubmoduleWarningFinder) for finder in sys.meta_path
):
    sys.meta_path.insert(0, _ExperimentalSubmoduleWarningFinder())
