#!/usr/bin/env pytest

import os
import shlex
import shutil
import subprocess
import unittest
import glob
import re

class test_fan_parsers(unittest.TestCase):
    def run_command(self, command):
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode

# Add test methods dynamically for each .fan file in the resources directory
for file in glob.glob("tests/resources/*.fan"):
    func_name = file.replace("tests/resources/", "").replace(".fan", "")
    func_name = re.sub(r'[^a-zA-Z0-9_]', '_', func_name)

    def test_file(self):
        f"""Test the C++ and python .fan parsers for {file!r}"""
        command = shlex.split("fandango --parser=python dump --no-cache --no-stdlib " + file)
        python_out, err, return_code = self.run_command(command)
        self.assertEqual(0, return_code)
        self.assertEqual(err, "")

        command = shlex.split("fandango --parser=speedy dump --no-cache --no-stdlib " + file)
        speedy_out, err, return_code = self.run_command(command)
        self.assertEqual(0, return_code)
        self.assertEqual(err, "")

        self.assertEqual(python_out, speedy_out, file)

    setattr(test_fan_parsers, f'test_{func_name}', test_file)

if __name__ == "__main__":
    unittest.main()
