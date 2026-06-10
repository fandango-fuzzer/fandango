import os
import sys
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse

# Guidance (A* k-path navigation) can be toggled via env for experimentation.
GUIDANCE = os.environ.get("FANDANGO_GUIDANCE", "1") == "1"
# When "1" (default), the run stops as soon as full grammar (k-path) coverage is
# reached -- a fast "converge then stop" measurement. Set to "0" for a
# coverage-MAXIMIZING run: after full grammar coverage, guidance is dropped and
# Fandango keeps generating (random sessions) until the wall-clock FUZZ_TIME, to
# accumulate as much incidental code coverage as possible.
STOP_ON_FULL = os.environ.get("FANDANGO_STOP_ON_FULL", "1") == "1"


def run_once():
    with open("smtp_client.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    assert grammar is not None
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.DEBUG,
        coverage_goal=CoverageGoal.STATE_INPUTS,
    )
    fandango.coverage_log_interval = 10
    fandango.enable_guidance(GUIDANCE)
    fandango.stop_on_full_coverage = STOP_ON_FULL
    for _ in fandango.generate(mode=FuzzingMode.IO):
        pass


def main():
    sys.setrecursionlimit(10**6)
    start = time.time()
    run_once()
    print("Done in %.1f s." % (time.time() - start))


if __name__ == "__main__":
    main()
