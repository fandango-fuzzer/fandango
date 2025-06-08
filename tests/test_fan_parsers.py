#!/usr/bin/env pytest

import os
import shlex
import shutil
import subprocess
import unittest
import glob


class test_fan_parsers(unittest.TestCase):
    def run_command(self, command):
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode

    def test_parsers(self):
        for file in glob.glob("tests/resources/*.fan"):
            print(f"Testing file: {file}")
            command = shlex.split("fandango --parser=python dump --no-cache --no-stdlib " + file)
            python_out, err, return_code = self.run_command(command)
            self.assertEqual(0, return_code)
            self.assertEqual(err, "")

            command = shlex.split("fandango --parser=speedy dump --no-cache --no-stdlib " + file)
            speedy_out, err, return_code = self.run_command(command)
            self.assertEqual(0, return_code)
            self.assertEqual(err, "")

            self.assertEqual(python_out, speedy_out, file)

if __name__ == "__main__":
    unittest.main()
