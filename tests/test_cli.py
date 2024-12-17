import unittest
import subprocess
import os

from fandango.cli import get_parser


class test_cli(unittest.TestCase):
    
    def run_command(self, command):
        proc = subprocess.Popen(command,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,                    
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode
    


    def test_help(self):
        command = ["fandango", "--help"]
        out, err, code = self.run_command(command)
        parser = get_parser(True)
        self.assertEqual(0, code)
        self.assertEqual(out, parser.format_help())
        self.assertEqual(err, "")

    def test_fuzz_basic(self):
        command = ["fandango", "fuzz", "-f", "tests/resources/digit.fan", "-n", "10", "--random-seed", "426912"]
        expected = """35716
4
9768
30
5658
5
9
649
20
41"""
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(expected, out.strip())
        self.assertEqual("", err)

    def test_output_to_file(self):
        command = ["fandango", "fuzz", "-f", "tests/resources/digit.fan", "-n", "10", "--random-seed", "426912", "-o", "tests/resources/test.txt", "-s", ";"]
        expected = "35716;4;9768;30;5658;5;9;649;20;41;"
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertEqual("", err)
        with open("tests/resources/test.txt", "r") as fd:
            actual = fd.read()
        os.remove("tests/resources/test.txt")
        self.assertEqual(expected, actual)

    def test_output_multiple_files(self):
        command = ["fandango", "fuzz", "-f", "tests/resources/digit.fan", "-n", "10", "--random-seed", "426912", "-d", "tests/resources/test"]
        expected = ["35716","4","9768","30","5658","5","9","649","20","41"]
        out, err, code, = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertEqual("", err)
        for i in range(10):
            filename = "tests/resources/test/fandango-" + str(i+1).zfill(4) + ".txt"
            with open(filename, "r") as fd:
                actual = fd.read()
            self.assertEqual(expected[i], actual)
            os.remove(filename)
        os.rmdir("tests/resources/test")

    



