#!/usr/bin/env python3
"""Student self-check: does YOUR grammar reach a tutorial step's target?

Point it at your own .fan spec and the step you are on:

    python fdp_validate.py --step grammar --spec my_grammar.fan

It generates inputs from your spec, runs them through the FDP target, and
reports three things:

  * coverage  - how many lines of fdp.py your inputs reach, next to the number
                the reference solution reaches for this step;
  * bugs      - planted beacons, each a target branch this step is meant to
                unlock. Find every bug for your step and you are safe to move
                on; a missing bug comes with a hint about what your grammar
                is not yet producing;
  * missing lines - anything the reference reaches that you do not, shown with
                the source, so you can see exactly what you are leaving out.

Steps, in order:  random -> grammar -> language -> feedback -> protocol
Run from this directory, so specs can `import fdp`.

The reference expectations are read from ``fdp_reference.json``, so this works
on participant checkouts that have no ``solutions/`` directory. Maintainers
regenerate that snapshot (which DOES need the solutions) with:

    python fdp_validate.py --record
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fdp  # noqa: E402
import fdp_harness as H  # noqa: E402  (reuse generate() + measure())

# step -> (reference solution, session mode, default inputs, hard cap on inputs)
#   feedback is capped at 5: the coverage-feedback constraint is exhausted there
#   (see fdp_harness), and running the comparison at that small budget is the
#   point - undirected generation is lopsided with five inputs, feedback is not.
STEPS = {
    "random": ("solutions/00_random.fan", False, 200, None),
    "grammar": ("solutions/01_grammar.fan", False, 200, None),
    "language": ("solutions/02_constraints.fan", False, 200, None),
    "feedback": ("solutions/03_coverage.fan", False, 5, 5),
    "protocol": ("solutions/04a_session.fan", True, 200, None),
}
ORDER = ["random", "grammar", "language", "feedback", "protocol"]

BLURB = {
    "random": "raw bytes reaching the framing layer",
    "grammar": "structurally valid lines: every body type parses",
    "language": "constraints make messages well-formed and reach the handlers",
    "feedback": "coverage feedback covers every single-message branch, few inputs",
    "protocol": "stateful sessions reach the deep, login-gated handlers",
}

# tag -> (what finding it means, hint shown when it is still missing)
HINTS = {
    "raw-nonascii": (
        "a non-ASCII line was rejected (ERR_ENCODING)",
        "emit some raw non-ASCII bytes",
    ),
    "raw-badmagic": (
        "a line without the FDP anchor was rejected (ERR_MAGIC)",
        "emit ASCII that does not start with 'FDP'",
    ),
    "gate-length": (
        "a message passed the LEN check",
        "make LEN equal the body length (a constraint)",
    ),
    "gate-crc": (
        "a message passed the CRC check",
        "make CRC equal fdp.crc16hex(body) (a constraint)",
    ),
    "gate-fields": (
        "a message passed field validation",
        "include the required fields: user / to&body / chan",
    ),
    "handler-login": (
        "a LOGIN was accepted (OK_LOGIN)",
        "produce a well-formed LOGIN with a user= field",
    ),
    "handler-ping": ("a PING was accepted (OK_PONG)", "produce a well-formed PING"),
    "gate-noauth": (
        "a privileged message bounced with no session (ERR_NOAUTH)",
        "send a lone SUB / MSG / QUIT (no prior LOGIN)",
    ),
    "session-authed": (
        "a message ran on an authenticated session",
        "LOGIN earlier in the SAME session (multi-message input)",
    ),
    "session-sub": (
        "a channel subscription succeeded (OK_SUB)",
        "LOGIN then SUB in one session",
    ),
    "session-msg": (
        "a message was delivered (OK_MSG)",
        "LOGIN, SUB, then MSG the same channel in one session",
    ),
    "session-quit": (
        "a session closed cleanly (OK_QUIT)",
        "end a logged-in session with QUIT",
    ),
}


def describe(tag):
    """Human text + hint for a bug tag, including the dynamic shape:<TYPE> ones."""
    if tag in HINTS:
        return HINTS[tag]
    if tag.startswith("shape:"):
        t = tag.split(":", 1)[1]
        return (
            f"a {t} message parsed (right structure)",
            f"add the {t} alternative to <body> and give it the fields it needs",
        )
    return (tag, "")


def run_spec(fandango, spec, session, n, seed, timeout):
    """Generate n inputs from spec and measure them. Returns a measure() dict,
    or a dict with 'error' if generation failed / timed out."""
    outdir = tempfile.mkdtemp(prefix="val_")
    try:
        try:
            files = H.generate(fandango, spec, n, seed, outdir, timeout)
        except FileNotFoundError:
            return {"error": f"spec not found: {spec}"}
        except subprocess.TimeoutExpired:
            return {
                "error": f"generation did not finish in {timeout}s at n={n} "
                f"(an unsatisfiable constraint never terminates)"
            }
        except RuntimeError as exc:
            return {"error": str(exc)}
        if not files:
            return {"error": "no inputs were generated"}
        return H.measure(files, session=session)
    finally:
        shutil.rmtree(outdir, ignore_errors=True)


def source_line(n):
    return _SRC[n - 1].rstrip() if 1 <= n <= len(_SRC) else ""


with open(os.path.abspath(fdp.__file__)) as _fh:
    _SRC = _fh.read().splitlines()


# ---------------------------------------------------------------------------
# Reference expectations. Recorded once by a maintainer (--record, needs
# solutions/), then read from fdp_reference.json ever after -- participant
# checkouts do not carry the solutions.
# ---------------------------------------------------------------------------

REF_FILE = os.path.join(HERE, "fdp_reference.json")


def fandango_version(fandango):
    try:
        proc = subprocess.run([fandango, "--version"], capture_output=True, text=True)
        return proc.stdout.strip() or proc.stderr.strip()
    except OSError:
        return "unknown"


def record(fandango, seed, timeout):
    """Run every step's reference solution and snapshot what it reaches."""
    data = {"seed": seed, "fandango": fandango_version(fandango), "steps": {}}
    for step in ORDER:
        solution, session, default_n, cap = STEPS[step]
        n = min(default_n, cap) if cap else default_n
        ref = run_spec(fandango, solution, session, n, seed, timeout)
        if "error" in ref:
            sys.exit(f"--record: reference for '{step}' failed: {ref['error']}")
        data["steps"][step] = {
            "solution": solution,
            "n": n,
            "bugs": sorted(ref["bugs"]),
            "lines": sorted(ref["covered"]),
        }
        print(
            f"recorded '{step}': {len(ref['bugs'])} bugs, "
            f"{len(ref['covered'])} lines  ({solution}, n={n})"
        )
    with open(REF_FILE, "w") as fh:
        json.dump(data, fh, indent=1)
        fh.write("\n")
    print(
        f"wrote {REF_FILE} -- commit it so participants can validate without solutions/"
    )


def load_reference(step, fandango, session, n, seed, timeout):
    """The expectations for a step: from the recorded snapshot when present,
    otherwise measured live from the solution spec (maintainer checkouts)."""
    if os.path.exists(REF_FILE):
        with open(REF_FILE) as fh:
            data = json.load(fh)
        ref = data["steps"][step]
        for what, got, recorded in (
            ("--seed", seed, data.get("seed")),
            ("n", n, ref["n"]),
        ):
            if got != recorded:
                print(
                    f"note: {what}={got} but the reference was recorded at "
                    f"{recorded}; comparisons are against the recording"
                )
        current = fandango_version(fandango)
        if current != data.get("fandango"):
            print(
                f"note: reference was recorded with "
                f"'{data.get('fandango')}', you run '{current}'"
            )
        return {"bugs": set(ref["bugs"]), "covered": set(ref["lines"])}
    solution = STEPS[step][0]
    ref = run_spec(fandango, solution, session, n, seed, timeout)
    if "error" in ref:
        sys.exit(
            f"no {os.path.basename(REF_FILE)} and could not run the "
            f"reference solution ({solution}): {ref['error']}\n"
            f"(a maintainer creates the snapshot with: "
            f"python fdp_validate.py --record)"
        )
    return ref


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--step", choices=ORDER, help="which tutorial step your grammar is for"
    )
    ap.add_argument(
        "--spec", help="your .fan spec (relative to this directory or absolute)"
    )
    ap.add_argument(
        "--record",
        action="store_true",
        help="maintainers: re-run every reference solution and "
        "snapshot the expectations to fdp_reference.json "
        "(needs the solutions/ directory)",
    )
    ap.add_argument(
        "--n",
        type=int,
        default=None,
        help="inputs to generate (default: per-step; feedback capped at 5)",
    )
    ap.add_argument(
        "--seed", type=int, default=18, help="fandango random seed (default 18)"
    )
    ap.add_argument("--fandango", help="path to the fandango binary")
    ap.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="seconds before generation is abandoned (default 120)",
    )
    args = ap.parse_args()

    fandango = H.find_fandango(args.fandango)

    if args.record:
        record(fandango, args.seed, args.timeout)
        return
    if not (args.step and args.spec):
        ap.error("pass --step STEP --spec SPEC (or --record)")

    solution, session, default_n, cap = STEPS[args.step]
    n = args.n if args.n is not None else default_n
    if cap:
        n = min(n, cap)

    print(f"step '{args.step}': {BLURB[args.step]}")
    print(f"checking {args.spec}  (n={n}, seed={args.seed})")
    print("-" * 78)

    # Reference: what the solution for this step reaches. This defines the
    # target (its bugs are the ones you must find, its lines the ones to
    # match). Normally read from the recorded snapshot; see load_reference.
    ref = load_reference(args.step, fandango, session, n, args.seed, args.timeout)

    # Your grammar.
    you = run_spec(fandango, args.spec, session, n, args.seed, args.timeout)
    if "error" in you:
        print(f"FAIL: your spec did not run.\n  {you['error']}")
        print(
            "  (fandango's own error is printed above; a fresh exercise still "
            "has TODOs to fill in.)"
        )
        sys.exit(1)

    ref_bugs, your_bugs = ref["bugs"], you["bugs"]
    ref_lines, your_lines = ref["covered"], you["covered"]
    found = ref_bugs & your_bugs
    missing_bugs = sorted(ref_bugs - your_bugs)
    missing_lines = sorted(ref_lines - your_lines)

    print(
        f"coverage : {len(your_lines)} lines in fdp.py "
        f"(reference solution reaches {len(ref_lines)})"
    )
    print(
        f"bugs     : {len(found)} / {len(ref_bugs)} found for this step "
        f"(bugs are the pass/fail signal, not the raw line count)"
    )
    for tag in sorted(ref_bugs):
        text, hint = describe(tag)
        if tag in your_bugs:
            print(f"   [x] {tag:<15} {text}")
        else:
            print(f"   [ ] {tag:<15} {text}")
            print(f"       -> {hint}")

    if missing_lines:
        print(f"\nmissing lines the reference reaches ({len(missing_lines)}):")
        for ln in missing_lines[:12]:
            print(f"   fdp.py:{ln:<4} {source_line(ln)}")
        if len(missing_lines) > 12:
            print(f"   ... and {len(missing_lines) - 12} more")

    print("-" * 78)
    if not missing_bugs:
        nxt = ORDER[ORDER.index(args.step) + 1] if args.step != ORDER[-1] else None
        tail = f" on to '{nxt}'." if nxt else "; that is the last step."
        print(f"PASS: found every bug for '{args.step}'. Safe to move{tail}")
        sys.exit(0)
    else:
        print(
            f"FAIL: {len(missing_bugs)} bug(s) left to find "
            f"({', '.join(missing_bugs)}). Fix the grammar and re-run."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
