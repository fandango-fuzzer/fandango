#!/usr/bin/env pytest

import shlex
import subprocess
import unittest

from fandango import parse, DerivationTree
from fandango.constraints.base import ComparisonConstraint, ExpressionConstraint
from fandango.language import NonTerminal, Terminal
from fandango.language.search import ItemSearch, RuleSearch
from .utils import RESOURCES_ROOT


class TestSlices(unittest.TestCase):
    TEST_DIR = RESOURCES_ROOT

    @staticmethod
    def run_command(command):
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode

    def test_startswith(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c '<start>.startswith(\"6\")' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_0(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c '<start>[0] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_0plus(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c '<start>[0:][0] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_1plus(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c '<start>[1:][0] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_str0plus1(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c 'str(<start>)[0:1] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_plus1(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c '<start>[:1][0] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_plus(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c '<start>[:][0] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_str0(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c 'str(<start>)[0] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_paren(self):
        command = shlex.split(
            f"fandango fuzz -f {self.TEST_DIR / 'twodigits.fan'} -n 1 -c '(<start>)[0] == \"6\"' "
            "--format=none --validate --random-seed 426912 --population-size 10"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)


class TestExplicitSlices(unittest.TestCase):
    EXAMPLE = "\n".join(
        [
            "<start> ::= <a>",
            "<a> ::= <b> <c> <d>",
            '<b> ::= "a" | "b"',
            '<c> ::= "c"',
            '<d> ::= "d"',
            "",
            "where <a>[0].endswith('b')",
        ]
    )

    VALID_EXAMPLE = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(
                NonTerminal("<a>"),
                [
                    DerivationTree(
                        NonTerminal("<b>"),
                        [
                            DerivationTree(
                                Terminal("b"),
                            )
                        ],
                    ),
                    DerivationTree(
                        NonTerminal("<c>"),
                        [
                            DerivationTree(
                                Terminal("c"),
                            )
                        ],
                    ),
                    DerivationTree(
                        NonTerminal("<d>"),
                        [
                            DerivationTree(
                                NonTerminal("d"),
                            )
                        ],
                    ),
                ],
            )
        ],
    )

    INVALID_EXAMPLE = DerivationTree(
        NonTerminal("<start>"),
        [
            DerivationTree(
                NonTerminal("<a>"),
                [
                    DerivationTree(
                        NonTerminal("<b>"),
                        [
                            DerivationTree(
                                Terminal("a"),
                            )
                        ],
                    ),
                    DerivationTree(
                        NonTerminal("<c>"),
                        [
                            DerivationTree(
                                Terminal("c"),
                            )
                        ],
                    ),
                    DerivationTree(
                        NonTerminal("<d>"),
                        [
                            DerivationTree(
                                NonTerminal("d"),
                            )
                        ],
                    ),
                ],
            )
        ],
    )

    @classmethod
    def setUpClass(cls):
        cls.GRAMMAR, constraints = parse(cls.EXAMPLE, use_cache=False, use_stdlib=False)
        assert len(constraints) == 1
        cls.CONSTRAINT = constraints[0]

    def test_parsed(self):
        self.assertIsInstance(self.CONSTRAINT, ExpressionConstraint)
        self.assertTrue(
            self.CONSTRAINT.expression.endswith(".endswith('b')")
            or self.CONSTRAINT.expression.endswith('.endswith("b")')
        )
        tmp_var = self.CONSTRAINT.expression[:-14]
        self.assertIn(tmp_var, self.CONSTRAINT.searches)
        search = self.CONSTRAINT.searches[tmp_var]
        self.assertIsInstance(search, ItemSearch)
        base = search.base
        self.assertIsInstance(base, RuleSearch)
        self.assertEqual(base.symbol, NonTerminal("<a>"))
        self.assertEqual(1, len(search.slices))
        self.assertEqual(0, search.slices[0])

    def test_valid(self):
        self.assertTrue(self.CONSTRAINT.check(self.VALID_EXAMPLE))

    def test_invalid(self):
        self.assertFalse(self.CONSTRAINT.check(self.INVALID_EXAMPLE))
