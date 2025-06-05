#!/usr/bin/env pytest

import unittest
import unittest
import subprocess
import shlex
from typing import List

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


class TestSoft(unittest.TestCase):
    def get_solutions(
        self, specification_file, desired_solutions, random_seed, max_generations=500
    ):
        file = open(specification_file, "r")
        grammar_int, constraints_int = parse(file, use_stdlib=False, use_cache=False)
        fandango = Fandango(
            grammar=grammar_int,
            constraints=constraints_int,
            desired_solutions=desired_solutions,
            max_generations=max_generations,
            random_seed=random_seed,
        )
        solutions: List[DerivationTree] = fandango.evolve()
        return [s.to_string() for s in solutions]

    def run_command(self, command):
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode


class TestSoftValue(TestSoft):
    def test_soft_value(self):
        solutions = self.get_solutions(
            "tests/resources/softvalue.fan",
            desired_solutions=100,
            random_seed=1,
            max_generations=50,
        )
        self.assertIn("999999-999999", solutions)

    def test_min_in_different_contexts(self):
        solutions = self.get_solutions(
            "tests/resources/persons_with_constr.fan",
            desired_solutions=100,
            random_seed=1,
        )
        name, age = solutions[-1].split(",")
        first_name, last_name = name.split(" ")
        self.assertEqual(len(first_name), 2)
        self.assertEqual(len(last_name), 2)

    def test_cli_max_1(self):
        command = shlex.split(
            "fandango fuzz -f tests/resources/persons.fan -c 'maximizing int(<age>)' -n 50 --random-seed 1"
        )
        out, err, code = self.run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        last_age = int(lines[-1].split(",")[1])  # e.g., 9999999999999599999999
        self.assertGreater(last_age, 9999999999999)

    def test_cli_max_2(self):
        command = shlex.split(
            "fandango fuzz -f tests/resources/persons.fan --maximize 'int(<age>)' -n 50 --random-seed 1"
        )
        out, err, code = self.run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        last_age = int(lines[-1].split(",")[1])  # e.g., 9999999999999599999999
        self.assertGreater(last_age, 9999999999999)

    def test_cli_min_1(self):
        command = shlex.split(
            "fandango fuzz -f tests/resources/persons.fan -c 'minimizing int(<age>)' -n 100 --random-seed 1"
        )
        out, err, code = self.run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        last_age = int(lines[-1].split(",")[1])
        self.assertEqual(last_age, 0)

    def test_cli_min_2(self):
        command = shlex.split(
            "fandango fuzz -f tests/resources/persons.fan --minimize 'int(<age>)' -n 100 --random-seed 1"
        )
        out, err, code = self.run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        last_age = int(lines[-1].split(",")[1])
        self.assertEqual(last_age, 0)
