#!/usr/bin/env pytest

from collections.abc import Generator
import itertools
import unittest

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse
from .utils import RESOURCES_ROOT, run_command


class TestSoft(unittest.TestCase):
    @staticmethod
    def get_solutions(
        specification_file,
        desired_solutions,
        random_seed,
        max_generations=500,
        population_size=100,
    ) -> Generator[str, None, None]:
        with open(specification_file, "r") as file:
            grammar_int, constraints_int = parse(
                file, use_stdlib=False, use_cache=False
            )
        assert grammar_int is not None
        assert constraints_int is not None
        fandango = Fandango(
            grammar=grammar_int,
            constraints=constraints_int,
            random_seed=random_seed,
            logger_level=LoggerLevel.DEBUG,
            population_size=population_size,
        )
        generator = itertools.islice(
            fandango.generate(max_generations=max_generations), desired_solutions
        )

        for solution in generator:
            yield str(solution)


class TestSoftValue(TestSoft):
    def test_soft_value(self):
        gen = self.get_solutions(
            RESOURCES_ROOT / "softvalue.fan",
            desired_solutions=50,
            population_size=10,
            random_seed=1,
            max_generations=10000,  # make this a non-limiting factor
        )
        solutions = []
        for s in gen:
            solutions.append(s)
            if "999999-999999" == s:
                return  # optimized solution found, stop generating and don't fail

        self.fail(
            f"999999-999999 not found in the first {len(solutions)} solutions, found: {solutions}"
        )

    def test_min_in_different_contexts(self):
        gen = self.get_solutions(
            RESOURCES_ROOT / "persons_with_constr.fan",
            desired_solutions=60,
            random_seed=1,
        )
        for solution in gen:
            name, age = solution.split(",")
            first_name, last_name = name.split(" ")
            if len(first_name) == 2 and len(last_name) == 2:
                return
        self.fail(
            "No solution found, last first_name: {first_name}, last last_name: {last_name}"
        )

    def test_cli_max_1(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "persons.fan"),
            "-c",
            "maximizing int(<age>)",
            "-n",
            "50",
            "--population-size",
            "10",
            "--random-seed",
            "1",
        ]
        out, err, code = run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        self.assertGreater(len(lines), 0, f"\nerr: {err}\nout: {out}")
        last_age = int(lines[-1].split(",")[1])  # e.g., 9999999999999599999999
        self.assertGreater(last_age, 9999999999999, f"\nerr: {err}\nout: {out}")
        self.assertEqual(code, 0)

    def test_cli_max_2(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "persons.fan"),
            "--maximize",
            "int(<age>)",
            "-n",
            "50",
            "--population-size",
            "10",
            "--random-seed",
            "1",
        ]
        out, err, code = run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        last_age = int(lines[-1].split(",")[1])  # e.g., 9999999999999599999999
        self.assertGreater(last_age, 9999999999999)
        self.assertEqual(code, 0)

    def test_cli_min_1(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "persons.fan"),
            "-c",
            "minimizing int(<age>)",
            "-n",
            "20",
            "--population-size",
            "10",
            "--random-seed",
            "1",
        ]
        out, err, code = run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        last_age = int(lines[-1].split(",")[1])
        self.assertEqual(last_age, 0)
        self.assertEqual(code, 0)

    def test_cli_min_2(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "persons.fan"),
            "--minimize",
            "int(<age>)",
            "-n",
            "20",
            "--population-size",
            "10",
            "--random-seed",
            "1",
        ]
        out, err, code = run_command(command)
        lines = [line for line in out.split("\n") if line.strip()]
        last_age = int(lines[-1].split(",")[1])
        self.assertEqual(last_age, 0)
        self.assertEqual(code, 0)
