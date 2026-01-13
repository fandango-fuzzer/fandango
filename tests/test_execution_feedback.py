#!/usr/bin/env pytest

import unittest
import subprocess
import os
import shlex
import sys
import pytest
from pathlib import Path
from fandango.execution.dynamic_analysis import DynamicAnalysis


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestExecutionFeedback(unittest.TestCase):
    def run_command(self, command, directory=None):
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=directory
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestReachability1(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/reachability_1"

    def test_fcc_installed(self):
        # Check that fcc is installed
        try:
            subprocess.check_output(["fcc", "--version"])
        except FileNotFoundError as e:
            self.fail(f"Command not found: {e}")

    def test_compilation(self):
        # Assert that `f` was compiled with fcc
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.assertTrue(os.path.exists(os.path.join(self.put_dir, "build/f")))
        # Assert that fan can extract static analysis information
        self.run_command(["fan", os.path.join(self.put_dir, "build/f")])
        self.assertTrue(
            os.path.exists(os.path.join(self.put_dir, "build/.bb_to_dbg.json"))
        )
        self.assertTrue(os.path.exists(os.path.join(self.put_dir, "build/.cfg/")))
        files = os.listdir(os.path.join(self.put_dir, "build/.cfg/"))
        cfg_files = ["main.c.json"] + [f"src@f{i}.c.json" for i in range(1, 10)]
        for cfg_file in cfg_files:
            self.assertTrue(
                any(file.endswith(cfg_file) for file in files),
                f"Missing {cfg_file} in .cfg directory",
            )


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestReachability2(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/reachability_2"

    def test_function_reachability(self):
        # Set up
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.run_command(["fan", os.path.join(self.put_dir, "build/f")])

        # Run fandango to find an input ("0012345678...") that reaches the target function
        abs_instrumented_binary = (Path(self.put_dir) / "build" / "f").resolve()
        cmd = shlex.split(
            f"fandango fuzz --no-cache --stop-criterion 'lambda t: t.to_string().startswith(\"0012345678\")' -f {self.put_dir}/specifications/reach_function_1.fan --random-seed 1 --infinite --population-size 100 --fcc {abs_instrumented_binary}"
        )
        out, err, code = self.run_command(cmd)
        self.assertIn("0012345678", out)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestReachability3(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/reachability_3"

    def test_basic_block_reachability(self):
        # Set up
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.run_command(["fan", os.path.join(self.put_dir, "build/f")])

        # Run fandango to find an input ("0012345678900...") that reaches the target basic block
        abs_instrumented_binary = (Path(self.put_dir) / "build" / "f").resolve()
        cmd = shlex.split(
            f"fandango fuzz --no-cache --stop-criterion 'lambda t: t.to_string().startswith(\"0012345678900\")' -f {self.put_dir}/specifications/reach_bb_1.fan --random-seed 1 --infinite --population-size 100 --fcc {abs_instrumented_binary}"
        )
        out, err, code = self.run_command(cmd)
        self.assertIn("0012345678900", out)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestMem1(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/mem_heap_allocations_1"

    def test_trace_heap_allocations(self):
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.run_command(
            ["fan", os.path.join(self.put_dir, "build/test_malloc_calloc")]
        )

        da = DynamicAnalysis(
            sa=None,
            root_dir=os.path.join(self.put_dir, "build"),
            put=os.path.abspath(os.path.join(self.put_dir, "build/test_malloc_calloc")),
        )
        trace = da.trace_input("irrelevant")
        self.assertEqual(trace.HeapAllocatedBytes(), 3 * 99 * 100 / 2)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestMem2(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/mem_heap_allocations_2"

    def test_maximize_malloc(self):
        # Set up
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.run_command(
            ["fan", os.path.join(self.put_dir, "build/test_input_dependent_malloc")]
        )

        abs_instrumented_binary = (
            Path(self.put_dir) / "build" / "test_input_dependent_malloc"
        ).resolve()
        cmd = shlex.split(
            f"fandango fuzz --no-cache --stop-criterion 'lambda t: t.to_string().startswith(\"99999999\")' -f {self.put_dir}/specifications/maximize_malloc.fan --random-seed 1 --infinite --population-size 100 --fcc {abs_instrumented_binary}"
        )
        out, err, code = self.run_command(cmd)
        self.assertIn("99999999", out)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestExecutionPathLength1(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/execution_path_length_1"

    def test_trace_execution_path_length(self):
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.run_command(["fan", os.path.join(self.put_dir, "build/test_simple")])

        da = DynamicAnalysis(
            sa=None,
            root_dir=os.path.join(self.put_dir, "build"),
            put=os.path.abspath(os.path.join(self.put_dir, "build/test_simple")),
        )
        trace = da.trace_input("irrelevant")
        self.assertGreaterEqual(trace.ExecutionPathLength(), 200)  # Actually it's 607


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestExecutionPathLength2(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/execution_path_length_2"

    def test_maximize_execution_path_length(self):
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.run_command(
            ["fan", os.path.join(self.put_dir, "build/test_input_dependent")]
        )

        abs_instrumented_binary = (
            Path(self.put_dir) / "build" / "test_input_dependent"
        ).resolve()
        cmd = shlex.split(
            f"fandango fuzz --no-cache --stop-criterion 'lambda t: t.to_string().startswith(\"99999999\")' -f {self.put_dir}/specifications/maximize_execution_path_length.fan --random-seed 1 --infinite --population-size 100 --fcc {abs_instrumented_binary}"
        )
        out, err, code = self.run_command(cmd)
        self.assertIn("99999999", out)


@pytest.mark.skipif(sys.platform.startswith("win"), reason="Skipping on Windows")
class TestExperimentSetup(TestExecutionFeedback):
    put_dir: str

    @classmethod
    def setUpClass(cls):
        cls.put_dir = "tests/resources/execution_feedback/execution_path_length_3"

    def test_stop_after_seconds(self):
        self.run_command(["make", "clean"], self.put_dir)
        self.run_command(["make"], self.put_dir)
        self.run_command(
            ["fan", os.path.join(self.put_dir, "build/test_input_dependent")]
        )

        abs_instrumented_binary = (
            Path(self.put_dir) / "build" / "test_input_dependent"
        ).resolve()
        cmd = shlex.split(
            f"fandango -vv fuzz --no-cache --stop-after-seconds 1 -f {self.put_dir}/specifications/maximize_execution_path_length.fan --random-seed 1 --infinite --population-size 100 --fcc {abs_instrumented_binary}"
        )
        out, err, code = self.run_command(cmd)
        self.assertIn("Stopping experiment after reaching the time limit", err)
