#!/usr/bin/env python3
# Runs fandango with cpython profiling and opens graphical overview with snakeviz
# Usage: python cprofile_profile.py [fandango_args]
# Example: python cprofile_profile.py -f docs/persons.fan -n 100

import subprocess
import sys
import tempfile
import os

if len(sys.argv) < 2:
    print("Usage: python cprofile_profile.py [fandango_args]")
    print("Example: python cprofile_profile.py -f docs/persons.fan -n 100")
    sys.exit(1)

args = sys.argv[1:]

# Use temporary directory for automatic cleanup
with tempfile.TemporaryDirectory() as temp_dir:
    profile_path = os.path.join(temp_dir, "profile.prof")
    script_path = os.path.join(temp_dir, "script.py")

    # Write the script file
    with open(script_path, "w") as script_file:
        script_file.write(
            f"import fandango.cli\nfandango.cli.main('fuzz', '--format', 'none', *{args})"
        )

    print(f"Profiling: fandango fuzz --format none {' '.join(args)}")
    subprocess.run(f"python -m cProfile -o {profile_path} {script_path}", shell=True)

    print("Opening visualization...")
    subprocess.run(f"python -m snakeviz {profile_path}", shell=True)
