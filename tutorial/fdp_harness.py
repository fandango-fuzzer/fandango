#!/usr/bin/env python3
"""FDP coverage harness.

Generates a fixed, reproducible batch of inputs from a Fandango spec, feeds
every input directly into the FDP reference implementation (``fdp.py``), and
measures the line coverage each spec reaches inside the target.

The point of the tutorial is the *gradient*: as the specs climb from random
bytes to grammar to constraints to a stateful session, coverage of ``fdp.py``
grows, because deeper pipeline stages are only reachable by better-formed
inputs and, ultimately, by valid message sequences.

Reproducibility: generation uses a fixed ``--random-seed`` and
``PYTHONHASHSEED=0``, so the same spec + seed + count always yields the same
inputs and therefore the same coverage.

Run from this directory, e.g.:

    python fdp_harness.py --all                          # the whole ladder
    python fdp_harness.py --spec exercises/02_constraints.fan --n 200
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

# The ordered ladder shown by --all. Each entry: (spec, label, is_session, cap).
# Session specs generate a whole newline-separated conversation per input,
# replayed through ONE Session.
#
# `cap` bounds -n for a spec, for two reasons:
#   * 03_coverage MUST be capped: its covers_new gate admits an input only if it
#     grows the population's covered-branch union, and a single message on a
#     fresh session reaches one distinct branch per body type, so exactly FIVE
#     inputs exhaust it. Asking Fandango for more is unsatisfiable and never
#     terminates, so we request only what exists.
#   * 02_constraints is capped to the SAME budget on purpose, so the two rows are
#     a fair same-budget comparison. At five inputs, undirected constrained
#     generation is lopsided (it misses a body type and its handler lines),
#     while coverage feedback deterministically covers all five. That gap is the
#     whole point of the stage; at n=200 stage 2 saturates and the effect hides.
# `None` means no cap: use the requested --n.
LADDER = [
    ("solutions/00_random.fan", "random bytes", False, None),
    ("solutions/01_grammar.fan", "grammar only", False, None),
    ("solutions/02_constraints.fan", "grammar + constraints", False, 5),
    ("solutions/03_coverage.fan", "+ coverage feedback", False, 5),
    ("solutions/03_target.fan", "+ targeted line", False, None),
    ("solutions/04a_session.fan", "stateful session", True, None),
]

TARGET_FILE = os.path.abspath(fdp.__file__)


def _bug_line_numbers() -> set:
    """Line numbers of the planted `_bug(...)` beacons in the target, so coverage
    counts stay honest: the beacons are a validation aid, not target behaviour."""
    nums = set()
    with open(TARGET_FILE) as fh:
        for i, line in enumerate(fh, 1):
            if line.strip().startswith("_bug("):
                nums.add(i)
    return nums


BUG_LINES = _bug_line_numbers()


def find_fandango(explicit: str | None) -> str:
    if explicit:
        return explicit
    # This copy of the tutorial lives inside the Fandango repository, so prefer
    # the checkout's own virtualenv: it is the build under development, which is
    # what a maintainer running this here wants to exercise.
    local = os.path.join(HERE, "..", ".venv", "bin", "fandango")
    if os.path.exists(local):
        return local
    found = shutil.which("fandango")
    if found:
        return found
    sys.exit(
        "could not find the 'fandango' command; run "
        "'pip install fandango-fuzzer' or pass --fandango PATH"
    )


def generate(
    fandango: str, spec: str, n: int, seed: int, outdir: str, timeout: int
) -> list[str]:
    """Produce n reproducible inputs from `spec` into `outdir`, return file paths.

    Raises FileNotFoundError if the spec is missing, subprocess.TimeoutExpired
    if generation does not finish within `timeout` seconds (a spec whose
    constraints cannot be satisfied n times never terminates, so every run is
    bounded), or RuntimeError if fandango exits non-zero.
    """
    spec_path = spec if os.path.isabs(spec) else os.path.join(HERE, spec)
    if not os.path.exists(spec_path):
        raise FileNotFoundError(spec_path)
    # PYTHONHASHSEED fixes reproducibility; HERE on PYTHONPATH lets specs
    # `import fdp` / `import fdp_cover` regardless of where they live.
    env = dict(
        os.environ,
        PYTHONHASHSEED="0",
        PYTHONPATH=HERE + os.pathsep + os.environ.get("PYTHONPATH", ""),
    )
    cmd = [
        fandango,
        "fuzz",
        "-f",
        spec_path,
        "-n",
        str(n),
        "--random-seed",
        str(seed),
        "--file-mode",
        "binary",
        "-d",
        outdir,
    ]
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        sys.stderr.write(proc.stdout + proc.stderr)
        raise RuntimeError(f"fandango failed on {spec}")
    return sorted(
        os.path.join(outdir, f)
        for f in os.listdir(outdir)
        if os.path.isfile(os.path.join(outdir, f))
    )


def measure(files: list[str], session: bool = False) -> dict:
    """Run every input through fdp.process() under a line tracer.

    When `session` is True each file is a newline-separated conversation, and
    all its lines are replayed through ONE shared Session (stateful); otherwise
    each file is a single message on a fresh Session (stateless).
    """
    covered: set[int] = set()
    reached: Counter[str] = Counter()  # deepest pipeline stage reached
    codes: Counter[str] = Counter()  # response code distribution
    fdp._BUGS.clear()  # collect the beacons THIS batch triggers, from empty

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

    covered -= BUG_LINES  # beacons are not part of the target's real coverage
    return {
        "covered": covered,
        "reached": reached,
        "codes": codes,
        "bugs": set(fdp._BUGS),
        "n": len(files),
    }


STAGE_ORDER = ["frame", "parse", "validate", "apply"]


def funnel(reached: Counter, n: int) -> str:
    # cumulative: an input that reached 'apply' also passed frame/parse/validate
    cum = {}
    running = 0
    for st in reversed(STAGE_ORDER):
        running += reached.get(st, 0)
        cum[st] = running
    return "  ".join(f"{st}:{cum[st]}" for st in STAGE_ORDER)


def run_one(
    fandango: str,
    spec: str,
    label: str,
    n: int,
    seed: int,
    session: bool = False,
    timeout: int = 120,
) -> dict:
    """Generate + measure one spec. Returns a result dict, or {"error": reason}
    so one bad spec (missing, timed out, or failing) never aborts the ladder."""
    outdir = tempfile.mkdtemp(prefix="fdp_")
    try:
        try:
            files = generate(fandango, spec, n, seed, outdir, timeout)
        except FileNotFoundError:
            return {"error": "not built / not found"}
        except subprocess.TimeoutExpired:
            return {"error": f"timed out after {timeout}s at n={n}"}
        except RuntimeError as exc:
            return {"error": str(exc)}
        if not files:
            return {"error": "no inputs generated"}
        result = measure(files, session=session)
        result["spec"] = spec
        result["label"] = label
        return result
    finally:
        shutil.rmtree(outdir, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--spec", help="a single .fan spec (relative to this directory or absolute)"
    )
    ap.add_argument(
        "--all", action="store_true", help="run the whole ladder and compare"
    )
    ap.add_argument(
        "--n", type=int, default=1000, help="inputs per spec (default 1000)"
    )
    ap.add_argument(
        "--seed", type=int, default=18, help="fandango random seed (default 18)"
    )
    ap.add_argument("--fandango", help="path to the fandango binary")
    ap.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="seconds before a single spec's generation is abandoned "
        "(default 120); guards against unsatisfiable specs that "
        "never terminate",
    )
    ap.add_argument(
        "-v", "--verbose", action="store_true", help="show response-code breakdown"
    )
    args = ap.parse_args()

    fandango = find_fandango(args.fandango)

    if args.all:
        specs = LADDER
        if not any(os.path.exists(os.path.join(HERE, s)) for s, *_ in LADDER):
            sys.exit(
                "--all is the reference ladder and needs the reference specs, "
                "which are not in this checkout. To measure your own spec:\n"
                "    python fdp_harness.py --spec YOUR_SPEC.fan"
            )
    elif args.spec:
        specs = [(args.spec, "", "session" in args.spec, None)]
    else:
        ap.error("pass --spec SPEC or --all")

    print(f"n={args.n}  seed={args.seed}  target={os.path.basename(TARGET_FILE)}")
    print(f"{'spec':<32}{'label':<24}{'lines':>7}   funnel (cumulative reach)")
    print("-" * 96)
    for spec, label, session, cap in specs:
        n = min(args.n, cap) if cap else args.n
        result = run_one(
            fandango, spec, label, n, args.seed, session=session, timeout=args.timeout
        )
        if "error" in result:
            print(f"{spec:<32}{('(' + result['error'] + ')'):<24}{'-':>7}")
            continue
        n_note = f"  [n={n}]" if cap and n < args.n else ""
        print(
            f"{spec:<32}{label:<24}{len(result['covered']):>7}   {funnel(result['reached'], result['n'])}{n_note}"
        )
        if args.verbose:
            for code, count in result["codes"].most_common():
                print(f"    {code:<16}{count:>6}")


if __name__ == "__main__":
    main()
