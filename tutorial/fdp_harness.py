#!/usr/bin/env python3
"""FDP coverage harness.

Generates a fixed, reproducible batch of inputs from a Fandango spec, feeds
every input directly into the FDP reference implementation (``fdp.py``), and
measures the line coverage each spec reaches inside the target.

The point of the tutorial is the *gradient*: as the specs climb from random
bytes to grammar to constraints to feedback, coverage of ``fdp.py`` grows,
because deeper pipeline stages are only reachable by better-formed inputs.

Reproducibility: generation uses a fixed ``--random-seed`` and
``PYTHONHASHSEED=0``, so the same spec + seed + count always yields the same
inputs and therefore the same coverage.

Examples
--------
    python fdp_harness.py --spec 01_grammar.fan            # one spec, n=1000
    python fdp_harness.py --spec 02_constraints.fan --n 500 --seed 7
    python fdp_harness.py --all                            # the whole ladder
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fdp  # noqa: E402

# The ordered ladder shown by --all. Missing files are skipped with a note.
# Each entry: (spec, label, is_session). Session specs generate a whole
# newline-separated conversation per input, replayed through ONE Session.
LADDER = [
    ("00_random.fan", "random bytes", False),
    ("01_grammar.fan", "grammar only", False),
    ("02_constraints.fan", "grammar + constraints", False),
    ("03_coverage.fan", "+ coverage feedback", False),
    ("03_target.fan", "+ targeted line", False),
    ("04_session.fan", "stateful session", True),
]

TARGET_FILE = os.path.abspath(fdp.__file__)


def find_fandango(explicit: str | None) -> str:
    if explicit:
        return explicit
    local = os.path.join(HERE, "..", ".venv", "bin", "fandango")
    if os.path.exists(local):
        return local
    found = shutil.which("fandango")
    if found:
        return found
    sys.exit("could not find the 'fandango' binary; pass --fandango PATH")


def generate(fandango: str, spec: str, n: int, seed: int, outdir: str) -> list[str]:
    """Produce n reproducible inputs from `spec` into `outdir`, return file paths."""
    spec_path = spec if os.path.isabs(spec) else os.path.join(HERE, spec)
    if not os.path.exists(spec_path):
        return []
    # PYTHONHASHSEED fixes reproducibility; HERE on PYTHONPATH lets feedback
    # specs `import fdp` / `import fdp_cover`.
    env = dict(os.environ, PYTHONHASHSEED="0",
               PYTHONPATH=HERE + os.pathsep + os.environ.get("PYTHONPATH", ""))
    cmd = [
        fandango, "fuzz", "-f", spec_path,
        "-n", str(n), "--random-seed", str(seed),
        "--file-mode", "binary", "-d", outdir,
    ]
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout + proc.stderr)
        sys.exit(f"fandango failed on {spec}")
    return sorted(
        os.path.join(outdir, f) for f in os.listdir(outdir)
        if os.path.isfile(os.path.join(outdir, f))
    )


def measure(files: list[str], session: bool = False) -> dict:
    """Run every input through fdp.process() under a line tracer.

    When `session` is True each file is a newline-separated conversation, and
    all its lines are replayed through ONE shared Session (stateful); otherwise
    each file is a single message on a fresh Session (stateless).
    """
    covered: set[int] = set()
    reached = Counter()   # deepest pipeline stage reached
    codes = Counter()     # response code distribution

    def tracer(frame, event, arg):
        if event == "line" and frame.f_code.co_filename == TARGET_FILE:
            covered.add(frame.f_lineno)
        return tracer

    sys.settrace(tracer)
    try:
        for path in files:
            with open(path, "rb") as fh:
                data = fh.read()
            if session:
                sess = fdp.Session()
                for line in data.split(b"\n"):
                    resp = fdp.process(line, sess)
                    reached[resp.stage] += 1
                    codes[resp.code] += 1
            else:
                resp = fdp.process(data, fdp.Session())
                reached[resp.stage] += 1
                codes[resp.code] += 1
    finally:
        sys.settrace(None)

    return {"covered": covered, "reached": reached, "codes": codes, "n": len(files)}


STAGE_ORDER = ["frame", "parse", "validate", "apply"]


def funnel(reached: Counter, n: int) -> str:
    # cumulative: an input that reached 'apply' also passed frame/parse/validate
    cum = {}
    running = 0
    for st in reversed(STAGE_ORDER):
        running += reached.get(st, 0)
        cum[st] = running
    return "  ".join(f"{st}:{cum[st]}" for st in STAGE_ORDER)


def run_one(fandango: str, spec: str, label: str, n: int, seed: int,
            session: bool = False) -> dict | None:
    outdir = tempfile.mkdtemp(prefix="fdp_")
    try:
        files = generate(fandango, spec, n, seed, outdir)
        if not files:
            return None
        result = measure(files, session=session)
        result["spec"] = spec
        result["label"] = label
        return result
    finally:
        shutil.rmtree(outdir, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", help="a single .fan spec (relative to tutorial/ or absolute)")
    ap.add_argument("--all", action="store_true", help="run the whole ladder and compare")
    ap.add_argument("--n", type=int, default=1000, help="inputs per spec (default 1000)")
    ap.add_argument("--seed", type=int, default=42, help="fandango random seed (default 42)")
    ap.add_argument("--fandango", help="path to the fandango binary")
    ap.add_argument("-v", "--verbose", action="store_true", help="show response-code breakdown")
    args = ap.parse_args()

    fandango = find_fandango(args.fandango)

    if args.all:
        specs = LADDER
    elif args.spec:
        specs = [(args.spec, "", "session" in args.spec)]
    else:
        ap.error("pass --spec SPEC or --all")

    print(f"n={args.n}  seed={args.seed}  target={os.path.basename(TARGET_FILE)}")
    print(f"{'spec':<22}{'label':<24}{'lines':>7}   funnel (cumulative reach)")
    print("-" * 88)
    for spec, label, session in specs:
        result = run_one(fandango, spec, label, args.n, args.seed, session=session)
        if result is None:
            print(f"{spec:<22}{'(not built yet)':<24}{'-':>7}")
            continue
        print(f"{spec:<22}{label:<24}{len(result['covered']):>7}   {funnel(result['reached'], result['n'])}")
        if args.verbose:
            for code, count in result["codes"].most_common():
                print(f"    {code:<16}{count:>6}")


if __name__ == "__main__":
    main()
