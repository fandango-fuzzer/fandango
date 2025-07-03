#!/usr/bin/env pytest
import asyncio
import os
import re
import shutil
import subprocess
import sys
import time
import unittest

from fandango.cli import get_parser

from .utils import DOCS_ROOT, IS_BEARTYPE_ACTIVE, RESOURCES_ROOT, run_command

# beartype somehow scrambles the fixed rng
if IS_BEARTYPE_ACTIVE:
    expected_with_random_seed = [
        "50099",
        "761",
        "4241",
        "72",
        "5",
        "72772",
        "96688",
        "85",
        "88",
        "6",
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
        self.assertEqual(0, code)
        self.assertEqual(err, "")

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
        self.assertEqual(0, code)
        self.assertEqual(err, "")
        self.assertEqual(expected_with_random_seed, out.strip().split("\n"))

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
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertEqual("", err)
        with open(out_file, "r") as fd:
            actual = fd.read()
        self.assertEqual(expected_with_random_seed, actual.split(";"))
        os.remove(RESOURCES_ROOT / "test.txt")

    def test_output_multiple_files(self):
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
            str(RESOURCES_ROOT / "test"),
            "--no-cache",
        ]
        (
            out,
            err,
            code,
        ) = run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertEqual("", err)
        for i, expected_value in enumerate(expected_with_random_seed):
            filename = RESOURCES_ROOT / "test" / f"fandango-{i:04d}.txt"
            with open(filename, "r") as fd:
                actual = fd.read()
            self.assertEqual(expected_value, actual)

        shutil.rmtree(RESOURCES_ROOT / "test", ignore_errors=True)

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

        self.assertEqual("", out)
        self.assertEqual("", err)
        self.assertEqual(0, code)

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
        self.assertEqual("", err)
        self.assertEqual(expected_output, out)
        self.assertEqual(0, code)

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
            "50",
        ]
        expected = """fandango:ERROR: Population did not converge to a perfect population
fandango:ERROR: Only found 0 perfect solutions, instead of the required 10
"""
        out, err, code = run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertEqual(expected, err)

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
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

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
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

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
            "len(str(<start>)) > 10",
        ]
        expected = """fandango:ERROR: Population did not converge to a perfect population
fandango:ERROR: Only found 0 perfect solutions, instead of the required 10
"""
        out, err, code = run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertEqual(expected, err)

    def test_max_nodes_unsat(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "gen_number.fan"),
            "-n",
            "10",
            "--population-size",
            "10",
            "--max-generations",
            "30",
            "--no-cache",
            "-c",
            "len(str(<start>)) > 60",
            "--max-nodes",
            "30",
        ]
        err_pattern = r"""fandango:ERROR: Population did not converge to a perfect population
fandango:ERROR: Only found (\d) perfect solutions, instead of the required 10"""
        out_pattern = (
            r"""(aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\.\d+\n)*"""
        )
        out, err, code = run_command(command)
        self.assertRegex(out, out_pattern)
        self.assertRegex(err, err_pattern)
        self.assertEqual(0, code)

        num_from_error_message = int(re.findall(err_pattern, err)[0])
        self.assertEqual(num_from_error_message, len(out.split("\n")) - 1)

    def test_unparse_grammar(self):
        # We unparse the standard library as well as docs/persons.fan
        input_data = f"set -f {DOCS_ROOT / 'persons.fan'}\nset\n"
        out, err, code = run_command(["fandango", "shell"], input=input_data)
        self.assertEqual(0, code)
        self.assertEqual("", err)
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
            str(DOCS_ROOT / "cat.fan"),
            "cat",
        ]
        out, err, code = run_command(command)
        err = err.split("\n")

        filter_prefixes = ["fandango:INFO: In:", "fandango:INFO: Out:"]
        io_logs = list(
            filter(
                lambda x: any(filter(lambda b: x.startswith(b), filter_prefixes)), err
            )
        )
        self.assertEqual(2, len(io_logs))
        result_a = io_logs[0].split(": ", 2)[2]
        result_b = io_logs[0].split(": ", 2)[2]
        self.assertEqual(result_a, result_b)
        self.assertEqual(0, code)
        self.assertEqual("", out)

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
                    2
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
