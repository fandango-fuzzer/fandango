#!/usr/bin/env pytest
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

from fandango import DISTRIBUTION_NAME
from fandango.cli import get_parser
from fandango.cli.upgrade import check_for_fandango_update

from .utils import DOCS_ROOT, IS_BEARTYPE_ACTIVE, RESOURCES_ROOT, run_command

# beartype somehow scrambles the fixed rng
if IS_BEARTYPE_ACTIVE:
    expected_with_random_seed = [
        "60401624495",
        "68661899668",
        "73",
        "58694919430160244779",
        "9502591836",
        "7076746807392016295",
        "94",
        "389067036846",
        "43164695741",
        "4317911847",
    ]

else:
    expected_with_random_seed = [
        "35716",
        "4",
        "9768",
        "30",
        "5658",
        "5",
        "9",
        "649",
        "20",
        "41",
    ]


class TestCLI(unittest.TestCase):
    def test_help(self):
        command = ["fandango", "--help"]
        out, err, code = run_command(command)
        _parser = get_parser(True)
        self.assertEqual(0, code, code)
        self.assertEqual(err, "", err)

    def test_fuzz_basic(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "digit.fan"),
            "-n",
            "10",
            "--random-seed",
            "426912",
            "--no-cache",
        ]
        out, err, code = run_command(command)
        self.assertEqual(0, code, code)
        self.assertEqual(err, "", err)
        self.assertEqual(
            expected_with_random_seed, out.strip().split("\n"), out.strip().split("\n")
        )

    def test_output_to_file(self):
        out_file = RESOURCES_ROOT / "test.txt"
        if os.path.exists(out_file):
            os.remove(out_file)
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "digit.fan"),
            "-n",
            "10",
            "--random-seed",
            "426912",
            "-o",
            str(out_file),
            "-s",
            ";",
            "--no-cache",
        ]
        out, err, code = run_command(command)
        self.maxDiff = 1000000
        self.assertEqual(0, code, code)
        self.assertEqual("", out, out)
        self.assertEqual("", err, err)
        with open(out_file, "r") as fd:
            actual = fd.read()
        self.assertEqual(
            expected_with_random_seed, actual.split(";"), actual.split(";")
        )
        os.remove(RESOURCES_ROOT / "test.txt")

    def test_output_multiple_files(self):
        out_dir = RESOURCES_ROOT / "test_multiple_files"
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "digit.fan"),
            "-n",
            "10",
            "--random-seed",
            "426912",
            "-d",
            str(out_dir),
            "--no-cache",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", out, out)
        self.assertEqual("", err, err)
        self.assertEqual(0, code, code)
        for i, expected_value in enumerate(expected_with_random_seed):
            filename = out_dir / f"fandango-{i:04d}.txt"
            with open(filename, "r") as fd:
                actual = fd.read()
            self.assertEqual(expected_value, actual, actual)

        shutil.rmtree(out_dir, ignore_errors=True)

    def test_output_with_libfuzzer_harness(self):
        if sys.platform.startswith("win"):
            self.skipTest("LibFuzzer interface not supported on Windows")
        output_file = str(RESOURCES_ROOT / "test_libfuzzer_interface")
        compile_ = [
            "clang",
            "-g",
            "-O2",
            "-fPIC",
            "-shared",
            "-o",
            output_file,
            str(RESOURCES_ROOT / "test_libfuzzer_interface.c"),
        ]
        out, err, code = run_command(compile_)

        self.assertEqual("", out, out)
        self.assertEqual("", err, err)
        self.assertEqual(0, code, code)

        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "digit.fan"),
            "-n",
            "10",
            "--random-seed",
            "426912",
            "--file-mode",
            "binary",
            "--no-cache",
            "--input-method",
            "libfuzzer",
            output_file,
        ]
        expected_output = (
            "\n".join([f"data: {value}" for value in expected_with_random_seed]) + "\n"
        )
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual(expected_output, out, out)
        self.assertEqual(0, code, code)

    def test_infinite_mode(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "digit.fan"),
            "--infinite",
            "--no-cache",
        ]
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0,  # Unbuffered
            env={**os.environ, "PYTHONUNBUFFERED": "1"},  # Force Python unbuffered
        )
        time.sleep(20)
        self.assertIsNone(proc.poll(), "Process terminated before 20 seconds")
        proc.terminate()
        out, _ = proc.communicate()
        printed_lines = out.splitlines()
        self.assertGreater(
            len(printed_lines),
            100,
            f"Not enough output lines: {len(printed_lines)}",
        )

    def test_unsat(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "digit.fan"),
            "-n",
            "10",
            "--random-seed",
            "426912",
            "-c",
            "False",
            "--max-generations",
            "15",
        ]
        expected = """fandango:ERROR: Population did not converge to a perfect population
fandango:ERROR: Only found 0 perfect solutions, instead of the required 10
"""
        out, err, code = run_command(command)
        self.assertEqual("", out, out)
        self.assertEqual(expected, err, err)
        self.assertEqual(0, code, code)

    def test_binfinity(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(DOCS_ROOT / "binfinity.fan"),
            "-n",
            "1",
            "--format=none",
            "--validate",
            "--random-seed",
            "426912",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)

    def test_infinity(self):
        # docs/infinity.fan can only generate a limited number of individuals,
        # so we decrease the population size
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(DOCS_ROOT / "infinity.fan"),
            "-n",
            "1",
            "--format=none",
            "--validate",
            "--random-seed",
            "426912",
            "--population-size",
            "10",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)

    def test_max_repetition(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "digit.fan"),
            "-n",
            "10",
            "--max-generations",
            "50",
            "--max-repetitions",
            "10",
            "--no-cache",
            "-c",
            "len(str(<start>)) > 1000",
        ]
        expected = """fandango:ERROR: Population did not converge to a perfect population
fandango:ERROR: Only found 0 perfect solutions, instead of the required 10
"""
        out, err, code = run_command(command)
        self.assertEqual(0, code, code)
        self.assertEqual("", out, out)
        self.assertEqual(expected, err, err)

    def test_max_nodes_unsat(self):
        max_nodes = 61  # there is a off by one error in two places (this should really be 59), but for now this is just how it is
        # Tree(<start>, 1
        #   Tree(<text>, 2
        #     Tree('a'), 3
        #     [...]
        #     Tree('a') 52
        #   ),
        #   Tree('.'), 53
        #   Tree(<number>, 54
        #     Tree(<digit>, Tree(<_digit>, Tree('3'))),  57
        #     Tree(<digit>, Tree(<_digit>, Tree('2'))) 60
        #   )
        # )

        # need to manually constrain the length to be greater than the absolute minimum that can be produced
        # otherwise, the algorithm will produce results even though they are too big
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "gen_number.fan"),
            "-n",
            "10",
            "--population-size",
            "20",  # makes the test faster
            "--max-generations",
            "30",
            "-c",
            "len(str(<start>)) >= 53",  # 50 'a's, '.', and 2 digits
            "--max-nodes",
            str(max_nodes),
        ]

        out, err, code = run_command(command)

        # ignore these warnings, they are expected because there is no way to build a full population of 20 unique individuals with these constraints/max-nodes
        err_stripped = re.sub(
            r"fandango:WARNING: Could not generate a full population of unique individuals\. Population size reduced to (\d+)\.\n",
            "",
            err,
        )

        self.assertEqual(out, "", f"out: {out}")
        self.assertEqual(
            err_stripped,
            "fandango:ERROR: Population did not converge to a perfect population\nfandango:ERROR: Only found 0 perfect solutions, instead of the required 10\n",
            f"err: {err}",
        )
        self.assertEqual(0, code, code)

    def test_unparse_grammar(self):
        # We unparse the standard library as well as docs/persons.fan
        input_data = f"set -f {DOCS_ROOT / 'persons.fan'}\nset\n"
        out, err, code = run_command(["fandango", "shell"], input=input_data)
        self.assertEqual(0, code, code)
        self.maxDiff = 1000000
        self.assertEqual("", err, err)
        self.assertTrue(out.startswith("<_char> ::= r'(.|\\n)'\n"), out)
        self.assertTrue(out.endswith("<age> ::= <digit>+\n"), out)

    def test_talk_cat(self):
        command = [
            "fandango",
            "-v",
            "talk",
            "-n",
            "1",
            "-f",
            str(DOCS_ROOT / "cat-oracle.fan"),
            "cat",
        ]
        out, err, code = run_command(command)
        split_err = err.split("\n")

        filter_prefixes = ["fandango:INFO: In:", "fandango:INFO: Out:"]
        io_logs = list(
            filter(
                lambda x: any(filter(lambda b: x.startswith(b), filter_prefixes)),
                split_err,
            )
        )
        self.assertEqual(2, len(io_logs), f"err: {err}")
        result_a = io_logs[0].split(": ", 2)[2]
        result_b = io_logs[0].split(": ", 2)[2]
        self.assertEqual(result_a, result_b, result_b)
        self.assertEqual(0, code, code)
        self.assertEqual("", out, out)

    def test_output_file_already_exists(self):
        out_file = RESOURCES_ROOT / "existing_output.txt"
        try:
            out_file.write_text("pre-existing content")
            command = [
                "fandango",
                "-v",
                "fuzz",
                "-f",
                str(RESOURCES_ROOT / "digit.fan"),
                "-n",
                "1",
                "-o",
                str(out_file),
                "--no-cache",
            ]
            out, err, code = run_command(command)
            self.assertEqual(0, code)
            self.assertIn("Removing existing output file", err)
        finally:
            out_file.unlink(missing_ok=True)

    def test_output_directory_is_file(self):
        out_dir = RESOURCES_ROOT / "not_a_directory"
        try:
            out_dir.write_text("I am a file, not a directory")
            command = [
                "fandango",
                "fuzz",
                "-f",
                str(RESOURCES_ROOT / "digit.fan"),
                "-n",
                "1",
                "-d",
                str(out_dir),
                "--no-cache",
            ]
            out, err, code = run_command(command)
            self.assertEqual(1, code)
            self.assertIn(f"{out_dir} is not a directory or is not empty", err)
        finally:
            out_dir.unlink(missing_ok=True)

    def test_output_directory_not_empty(self):
        out_dir = RESOURCES_ROOT / "non_empty_dir"
        try:
            out_dir.mkdir(exist_ok=True)
            (out_dir / "dummy.txt").write_text("occupying space")
            command = [
                "fandango",
                "fuzz",
                "-f",
                str(RESOURCES_ROOT / "digit.fan"),
                "-n",
                "1",
                "-d",
                str(out_dir),
                "--no-cache",
            ]
            out, err, code = run_command(command)
            self.assertEqual(1, code)
            self.assertIn(f"{out_dir} is not a directory or is not empty", err)
        finally:
            shutil.rmtree(out_dir, ignore_errors=True)

    def test_output_directory_empty_succeeds(self):
        out_dir = RESOURCES_ROOT / "empty_dir"
        try:
            out_dir.mkdir(exist_ok=True)
            command = [
                "fandango",
                "fuzz",
                "-f",
                str(RESOURCES_ROOT / "digit.fan"),
                "-n",
                "1",
                "-d",
                str(out_dir),
                "--random-seed",
                "426912",
                "--no-cache",
            ]
            out, err, code = run_command(command)
            self.assertEqual(0, code, f"stderr: {err}")
        finally:
            shutil.rmtree(out_dir, ignore_errors=True)

    def test_soliloquy(self):
        async def async_run():
            def run_server():
                server_cmd = [
                    "fandango",
                    "-v",
                    "talk",
                    "-n",
                    "1",
                    "-f",
                    str(DOCS_ROOT / "smtp-extended.fan"),
                    "--server",
                    "tcp://localhost:9025",
                ]
                out, err, code = run_command(server_cmd)
                return out, err, code

            def run_client():
                import time

                time.sleep(
                    20
                )  # delay to let server start. We should find a better method for this
                client_cmd = [
                    "fandango",
                    "-v",
                    "talk",
                    "-n",
                    "1",
                    "-f",
                    str(DOCS_ROOT / "smtp-extended.fan"),
                    "--client",
                    "tcp://localhost:9025",
                ]
                out, err, code = run_command(client_cmd)
                return out, err, code

            # Run both in threads (since self.run_command is sync)
            server_future = asyncio.to_thread(run_server)
            client_future = asyncio.to_thread(run_client)
            return await asyncio.gather(server_future, client_future)

        (server_out, server_err, server_code), (client_out, client_err, client_code) = (
            asyncio.run(async_run())
        )
        self.assertEqual(
            0,
            server_code,
            f"Server error: {server_err}\n\nServer output: {server_out}",
        )
        self.assertEqual(
            0,
            client_code,
            f"Client error: {client_err}\n\nClient output: {client_out}",
        )


def test_fandango_version_upgrade_skip_set():
    """Ensure the env var short-circuits the update check without network calls."""
    with (
        patch.dict(os.environ, {"FANDANGO_DISABLE_UPDATE_CHECK": "1"}, clear=False),
        patch("sys.stdout.isatty", return_value=True),
        patch("fandango.cli.upgrade.check_package_for_update") as mock_check,
    ):
        check_for_fandango_update(check_now=True)

    mock_check.assert_not_called()


def test_fandango_version_upgrade():
    """Ensure the update check runs when the env var is not set/falsey."""
    with (
        patch.dict(os.environ, {"FANDANGO_DISABLE_UPDATE_CHECK": ""}, clear=False),
        patch("sys.stdout.isatty", return_value=True),
        patch("fandango.cli.upgrade.NOTIFIED_IN_THIS_SESSION", False),
        patch(
            "fandango.cli.upgrade.check_package_for_update", return_value=False
        ) as mock_check,
    ):
        check_for_fandango_update(check_now=True)

    mock_check.assert_called_once()


def test_fandango_version_check_path_works(tmp_path, monkeypatch, capsys):
    """Ensure the version check path works and the distribution is installed."""
    from fandango.cli import upgrade

    # This will fail if the distribution is not installed or packaging is missing
    installed_version = upgrade.Version(upgrade.version(DISTRIBUTION_NAME))

    latest_version = upgrade.Version(
        f"{installed_version.major}.{installed_version.minor}.{installed_version.micro + 1}"
    )

    payload = json.dumps({"info": {"version": str(latest_version)}}).encode()

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return payload

    def fake_urlopen(url, timeout):
        # Make sure we are querying PyPI for the right package
        assert f"/{DISTRIBUTION_NAME}/" in url
        return FakeResponse()

    monkeypatch.setattr("fandango.cli.upgrade.urllib.request.urlopen", fake_urlopen)

    notified = upgrade.check_package_for_update(
        DISTRIBUTION_NAME,
        cache_dir=tmp_path,
        check_now=True,
    )

    assert notified is True

    out, err = capsys.readouterr()
    assert out == ""
    expected_prefix = (
        f"📦 Update available for '{DISTRIBUTION_NAME}': "
        f"{installed_version} → {latest_version}. See "
    )
    assert err.startswith(expected_prefix)
