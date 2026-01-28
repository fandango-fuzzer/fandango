import os
from pathlib import Path
import platform
import shutil
from xdg_base_dirs import xdg_cache_home


def get_cache_dir() -> Path:
    """Return the parser cache directory"""
    cache_dir = xdg_cache_home() / "fandango"
    if platform.system() == "Darwin":
        cache_path = Path.home() / "Library" / "Caches"
        if os.path.exists(cache_path):
            cache_dir = cache_path / "Fandango"
    return cache_dir


def clear_cache() -> None:
    """Clear the Fandango parser cache"""
    cache_dir = get_cache_dir()
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)
