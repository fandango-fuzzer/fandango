#!/usr/bin/env pytest
"""The `-F` option: specs from a Fanbase registry."""

import argparse
import contextlib
import importlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from fandango.cli import main
from fandango.cli.commands import COMMANDS, run
from fandango.cli.fanbase_files import fanbase_files
from fandango.cli.parser import get_parser


def make_registry(root: Path) -> None:
    """A registry checkout with a `demo` format: a default spec and a variant."""
    specs = {
        "demo": (
            '<start> ::= "demo"\n',
            {"extensions": ["dmo"], "description": "demo"},
        ),
        "demo-long": ('<start> ::= "demo" "-long"\n', {"extensions": ["dmo"]}),
        "demo-needs": (
            '<start> ::= "needs"\n',
            {"extensions": ["dmo"], "requires": ["no_such_package_for_fandango_tests"]},
        ),
        "demo-installs": (
            '<start> ::= "installed"\n',
            {"extensions": ["dmo"], "requires": ["fandango_test_installable"]},
        ),
    }
    for kind, (text, meta) in specs.items():
        folder = root / "specs" / "demo" / kind
        folder.mkdir(parents=True)
        (folder / f"{kind}.fan").write_text(text, encoding="utf-8")
        (folder / "metadata.yml").write_text(yaml.safe_dump(meta), encoding="utf-8")


class TestFanbaseOption(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        # Cleanups run last-in first-out: this one must run last, because Windows
        # cannot remove the directory we are still working in
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)
        make_registry(self.tmp / "registry")
        self.lib = self.tmp / "lib"
        self.work = self.tmp / "work"
        self.work.mkdir()

        env = patch.dict(
            os.environ,
            {
                "FANBASE_REGISTRY": str(self.tmp / "registry"),
                "FANDANGO_PATH": str(self.lib),
            },
        )
        env.start()
        self.addCleanup(env.stop)
        self.cwd = os.getcwd()
        os.chdir(self.work)
        self.addCleanup(os.chdir, self.cwd)

    def run_main_failing(self, *args: str) -> tuple[int, str, str]:
        """Run main, as a user does: errors are reported and give a status, not raised."""
        with patch("fandango.logger._RAISE_ON_LOGGED_EXCEPTIONS", False):
            return self.run_main(*args)

    def run_main(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = main(*args, stdout=None, stderr=None)
        return status, out.getvalue(), err.getvalue()

    def test_default_spec_is_installed_and_used(self) -> None:
        status, _, err = self.run_main("fuzz", "-F", "demo", "-n", "1", "-d", "out")
        self.assertEqual(0, status, err)
        self.assertEqual("demo", (self.work / "out" / "fandango-0000.dmo").read_text())
        self.assertTrue((self.lib / "demo" / "demo.fan").is_file())
        self.assertIn("installed demo/demo", err)

    def test_extension_comes_from_the_format_but_x_wins(self) -> None:
        self.run_main("fuzz", "-F", "demo", "-n", "1", "-d", "a")
        self.assertTrue((self.work / "a" / "fandango-0000.dmo").is_file())
        self.run_main("fuzz", "-F", "demo", "-n", "1", "-d", "b", "-x", ".bin")
        self.assertTrue((self.work / "b" / "fandango-0000.bin").is_file())

    def test_variant_by_name(self) -> None:
        status, _, err = self.run_main(
            "fuzz", "-F", "demo-long", "-n", "1", "-d", "out"
        )
        self.assertEqual(0, status, err)
        self.assertEqual(
            "demo-long", (self.work / "out" / "fandango-0000.dmo").read_text()
        )

    def test_files_are_written_by_default(self) -> None:
        status, out, err = self.run_main("fuzz", "-F", "demo", "-n", "1")
        self.assertEqual(0, status, err)
        self.assertEqual("", out)
        self.assertTrue((self.work / "demo-inputs" / "fandango-0000.dmo").is_file())
        # a second run does not trip over the first run's directory
        self.run_main("fuzz", "-F", "demo", "-n", "1")
        self.assertTrue((self.work / "demo-inputs-2" / "fandango-0000.dmo").is_file())

    def test_output_file_is_respected(self) -> None:
        status, _, err = self.run_main("fuzz", "-F", "demo", "-n", "1", "-o", "x.out")
        self.assertEqual(0, status, err)
        self.assertEqual("demo", (self.work / "x.out").read_text())
        self.assertFalse((self.work / "demo-inputs").exists())

    def test_f_files_can_override_a_fanbase_spec(self) -> None:
        (self.work / "mine.fan").write_text(
            'include("demo/demo.fan")\n<start> ::= "mine"\n'
        )
        status, _, err = self.run_main(
            "fuzz", "-F", "demo", "-f", "mine.fan", "-n", "1", "-d", "out"
        )
        self.assertEqual(0, status, err)
        self.assertEqual("mine", (self.work / "out" / "fandango-0000.dmo").read_text())

    def test_spec_files_are_closed_afterwards(self) -> None:
        args = argparse.Namespace(
            fanbase_files=["demo", "demo-long"],
            fan_files=None,
            filename_extension=None,
            command="parse",
        )
        with fanbase_files(args):
            opened = list(args.fan_files)
            self.assertEqual(2, len(opened))
            self.assertFalse(any(fd.closed for fd in opened))
        self.assertTrue(all(fd.closed for fd in opened))

    def test_f_files_are_closed_afterwards(self) -> None:
        # Windows cannot remove a file that is still open
        (self.work / "mine.fan").write_text('<start> ::= "mine"\n')
        args = get_parser().parse_args(
            ["fuzz", "-f", "mine.fan", "-n", "1", "-d", "out"]
        )
        self.assertFalse(args.fan_files[0].closed)
        self.assertEqual(0, run(COMMANDS["fuzz"], args))
        self.assertTrue(args.fan_files[0].closed)

    def test_unknown_spec_fails(self) -> None:
        status, _, err = self.run_main_failing("fuzz", "-F", "nonesuch", "-n", "1")
        self.assertEqual(1, status)
        self.assertIn("nonesuch", err)

    def test_failing_install_of_a_missing_package_is_reported(self) -> None:
        # No test runs a real pip: the installer is replaced by one that fails
        failing = subprocess.CompletedProcess(
            [], 1, "", "ERROR: no matching distribution"
        )
        with patch("fanbase.manager.subprocess.run", return_value=failing):
            status, _, err = self.run_main_failing(
                "fuzz", "-F", "demo-needs", "-n", "1"
            )
        self.assertEqual(1, status)
        self.assertIn("could not install no_such_package_for_fandango_tests", err)

    def test_package_that_is_still_missing_after_the_install_is_reported(self) -> None:
        # The installer claims success, but the package is not there
        done = subprocess.CompletedProcess([], 0, "", "")
        with patch("fanbase.manager.subprocess.run", return_value=done):
            status, _, err = self.run_main_failing(
                "fuzz", "-F", "demo-needs", "-n", "1"
            )
        self.assertEqual(1, status)
        self.assertIn("pip install no_such_package_for_fandango_tests", err)

    def test_missing_package_is_installed_and_the_spec_is_used(self) -> None:
        site = self.tmp / "site"
        site.mkdir()
        commands: list[list[str]] = []

        def install(
            command: list[str], **kwargs: object
        ) -> subprocess.CompletedProcess:
            commands.append(command)
            (site / "fandango_test_installable.py").write_text("")
            importlib.invalidate_caches()
            return subprocess.CompletedProcess(command, 0, "", "")

        with (
            patch("fanbase.manager.subprocess.run", side_effect=install),
            patch.object(sys, "path", [*sys.path, str(site)]),
        ):
            status, _, err = self.run_main(
                "fuzz", "-F", "demo-installs", "-n", "1", "-d", "out"
            )
            self.assertEqual(0, status, err)
            self.assertEqual(1, len(commands))
            self.assertEqual("fandango_test_installable", commands[0][-1])
            self.assertEqual(
                "installed", (self.work / "out" / "fandango-0000.dmo").read_text()
            )

            # the package is there now, so a second run installs nothing
            self.run_main("fuzz", "-F", "demo-installs", "-n", "1", "-d", "again")
            self.assertEqual(1, len(commands))

    def test_installed_copy_is_used_when_the_registry_is_gone(self) -> None:
        self.run_main("fuzz", "-F", "demo", "-n", "1", "-d", "a")
        with patch.dict(os.environ, {"FANBASE_REGISTRY": "http://127.0.0.1:9"}):
            status, _, err = self.run_main("fuzz", "-F", "demo", "-n", "1", "-d", "b")
        self.assertEqual(0, status, err)
        self.assertEqual("demo", (self.work / "b" / "fandango-0000.dmo").read_text())

    def test_updated_spec_is_fetched_again(self) -> None:
        self.run_main("fuzz", "-F", "demo", "-n", "1", "-d", "a")
        spec = self.tmp / "registry" / "specs" / "demo" / "demo" / "demo.fan"
        spec.write_text('<start> ::= "demo2"\n')
        status, _, err = self.run_main("fuzz", "-F", "demo", "-n", "1", "-d", "b")
        self.assertEqual(0, status, err)
        self.assertEqual("demo2", (self.work / "b" / "fandango-0000.dmo").read_text())
        self.assertIn("updated demo/demo", err)


if __name__ == "__main__":
    unittest.main()
