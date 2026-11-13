#!/usr/bin/env pytest
"""Where `include()` looks, and in which order: the one documented in docs/Including.md.

The same relative name can exist in several of the directories (a copy next to a spec, one
installed for everyone), and the first directory that has it must win, every time. These
tests do not depend on the hash seed, which the test suite fixes.
"""

import os
from pathlib import Path

import pytest

from fandango.language.parse import splitter
from fandango.language.parse.splitter import read_file, search_dirs

SPEC = Path("lib/spec.fan")


def put(directory: Path, text: str) -> Path:
    """A copy of SPEC under `directory`; returns `directory`."""
    path = directory / SPEC
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return directory


@pytest.fixture
def machine(tmp_path, monkeypatch):
    """A machine with no Fandango files of its own, and an empty working directory."""
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))  # where Windows looks for it
    monkeypatch.setenv("XDG_DATA_HOME", str(home / "xdg"))
    # not XDG_DATA_DIRS: xdg_base_dirs splits it at colons, which cuts a Windows path in two
    monkeypatch.setattr(splitter, "xdg_data_dirs", lambda: [tmp_path / "system"])
    monkeypatch.delenv("FANDANGO_PATH", raising=False)
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    return tmp_path


@pytest.mark.parametrize("first", range(6))
def test_fandango_path_is_searched_from_left_to_right(machine, monkeypatch, first):
    dirs = [put(machine / f"lib{i}", f"copy {i}") for i in range(6)]
    order = dirs[first:] + dirs[:first]  # each directory takes its turn at the front
    monkeypatch.setenv("FANDANGO_PATH", os.pathsep.join(str(d) for d in order))
    assert read_file(SPEC) == f"copy {first}"


def test_fandango_path_is_split_at_the_separator_of_the_platform(machine, monkeypatch):
    first, second = put(machine / "a", "first"), put(machine / "b", "second")
    monkeypatch.setattr(os, "pathsep", ";")  # as on Windows, where a path holds colons
    monkeypatch.setenv("FANDANGO_PATH", f"{first};{second}")
    assert [first, second] == search_dirs(SPEC)[:2]
    assert read_file(SPEC) == "first"


def test_the_documented_order(machine, monkeypatch):
    explicit = put(machine / "explicit", "-I")
    on_path = put(machine / "on_path", "FANDANGO_PATH")
    beside = put(machine / "beside", "including file")
    user = put(machine / "home" / "xdg" / "fandango", "user")
    system = put(machine / "system" / "fandango", "system")
    monkeypatch.setenv("FANDANGO_PATH", str(on_path))

    expected = ["-I", "FANDANGO_PATH", "including file", "user", "system"]
    found = []
    for directory in (explicit, on_path, beside, user, system):
        found.append(read_file(SPEC, include_dirs=[explicit], file_dirs=[beside]))
        (directory / SPEC).unlink()  # the best copy goes; the next one must win
    assert found == expected
    with pytest.raises(FileNotFoundError):
        read_file(SPEC, include_dirs=[explicit], file_dirs=[beside])


def test_explicit_include_directories_keep_the_order_given(machine):
    dirs = [put(machine / f"inc{i}", f"inc {i}") for i in range(5)]
    assert read_file(SPEC, include_dirs=dirs) == "inc 0"
    assert read_file(SPEC, include_dirs=dirs[::-1]) == "inc 4"


def test_the_innermost_including_file_comes_first(machine):
    outer, inner = put(machine / "outer", "outer"), put(machine / "inner", "inner")
    assert read_file(SPEC, file_dirs=[inner, outer]) == "inner"


def test_a_directory_listed_twice_is_searched_once(machine, monkeypatch):
    shared = put(machine / "shared", "x")
    monkeypatch.setenv("FANDANGO_PATH", os.pathsep.join([str(shared)] * 3))
    dirs = search_dirs(SPEC, include_dirs=[shared])
    assert len(dirs) == len(set(dirs))
    assert dirs[0] == shared


def test_a_missing_file_is_an_error_that_lists_where_it_looked(machine, monkeypatch):
    monkeypatch.setenv("FANDANGO_PATH", str(machine / "nowhere"))
    with pytest.raises(FileNotFoundError, match="nowhere"):
        read_file(SPEC)
