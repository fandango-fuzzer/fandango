"""Import-time warnings for all modules under ``fandango.experimental``.

Why this exists:
- Experimental modules are not API-stable and should emit a warning when used.
- We want this behavior to be centralized, not duplicated in every submodule.

How it works:
- Warn once when ``fandango.experimental`` is imported.
- Install a meta path finder that intercepts imports for
  ``fandango.experimental.*``.
- Wrap each submodule loader and warn right before the wrapped loader executes.
- De-dup warnings via an in-process set so each module warns only once.
"""

import importlib.abc
import importlib.machinery
import sys
import warnings
from types import ModuleType
from typing import Sequence

# Tracks which module names have already emitted a warning in this process.
_WARNED_MODULES: set[str] = set()


def warn_experimental_import(module_name: str) -> None:
    """Emit a one-time warning for an experimental module import."""
    if module_name in _WARNED_MODULES:
        return

    _WARNED_MODULES.add(module_name)
    warnings.warn(
        (
            f"`{module_name}` is experimental and may change without notice. "
            "Avoid relying on its public API in production code."
        ),
        category=UserWarning,
        stacklevel=3,
    )


warn_experimental_import(__name__)

_SUBMODULE_PREFIX = f"{__name__}."


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
        warn_experimental_import(self._fullname)
        self._wrapped_loader.exec_module(module)


class _ExperimentalSubmoduleWarningFinder(importlib.abc.MetaPathFinder):
    """Finder that targets ``fandango.experimental.*`` submodule imports."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        # Ignore non-experimental imports as early as possible.
        if not fullname.startswith(_SUBMODULE_PREFIX):
            return None

        # Delegate actual module resolution to PathFinder.
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
