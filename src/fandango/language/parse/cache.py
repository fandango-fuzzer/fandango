import hashlib
import os
import uuid
from pathlib import Path
import platform
import shutil
import sys
import time
from traceback import print_exception
from typing import Optional
import warnings

from _contextvars import ContextVar

import fandango
from fandango.io import FandangoIO
from fandango.language.parse.spec import FandangoSpec
from fandango.logger import LOGGER
from xdg_base_dirs import xdg_cache_home
import cachedir_tag
import dill as pickle


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


def get_pickle_file(fan_contents: str) -> Path:
    cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, mode=0o700, exist_ok=True)
        cachedir_tag.tag(cache_dir, application="Fandango")  # type: ignore[no-untyped-call] # cachedir_tag doesn't provide types

    # Keep separate hashes for different Fandango and Python versions
    hash_contents = fan_contents + fandango.version() + "-" + sys.version
    hash = hashlib.sha256(hash_contents.encode()).hexdigest()
    return cache_dir / (hash + ".pickle")


def load_from_cache(fan_contents: str, filename: str) -> Optional[FandangoSpec]:
    pickle_file = get_pickle_file(fan_contents)

    if os.path.exists(pickle_file):
        try:
            with open(pickle_file, "rb") as fp:
                LOGGER.info(f"{filename}: loading cached spec from {pickle_file}")
                start_time = time.time()
                with warnings.catch_warnings():
                    warnings.simplefilter(
                        "ignore", DeprecationWarning
                    )  # for some reason, unpickling triggers the deprecation warnings in __getattr__ of DerivationTree and TreeValue
                    spec = pickle.load(fp)  # type: ignore[no-untyped-call, attr-defined] # dill doesn't provide types nor does it explicitly export load
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
                ctx_var: ContextVar = ContextVar("CURRENT_ENV_KEY")
                ctx_var.set(uuid.uuid4())
                spec.global_vars["CURRENT_ENV_KEY"].contextVar = ctx_var
                if (
                    spec.global_vars["PERSISTENT_ENV_HASH"]
                    in FandangoIO._instances.keys()
                ):
                    io_instance = FandangoIO._instances[
                        spec.global_vars["PERSISTENT_ENV_HASH"]
                    ]
                    FandangoIO._instances[ctx_var] = io_instance
                assert isinstance(spec, FandangoSpec)
                return spec
        except Exception as exc:
            print_exception(exc)
    return None


def store_in_cache(spec: FandangoSpec, fan_contents: str, filename: str) -> None:
    pickle_file = get_pickle_file(fan_contents)
    try:
        with open(pickle_file, "wb") as fp:
            LOGGER.info(f"{filename}: saving spec to cache {pickle_file}")
            ctx_var = spec.global_vars["CURRENT_ENV_KEY"].contextVar
            spec.global_vars["PERSISTENT_ENV_HASH"] = hash(ctx_var)
            spec.global_vars["CURRENT_ENV_KEY"].contextVar = None
            pickle.dump(spec, fp)  # type: ignore[no-untyped-call, attr-defined] # dill doesn't provide types nor does it explicitly export dump
            spec.global_vars["CURRENT_ENV_KEY"].contextVar = ctx_var
    except Exception as e:
        print_exception(e)
        try:
            os.remove(pickle_file)  # might be inconsistent
        except Exception:
            pass
