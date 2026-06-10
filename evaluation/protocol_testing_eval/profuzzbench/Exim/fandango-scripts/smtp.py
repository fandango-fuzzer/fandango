import os
import sys
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse

# Guidance (A* k-path navigation) can be toggled via env for experimentation.
GUIDANCE = os.environ.get("FANDANGO_GUIDANCE", "0") == "1"


def run_once():
    with open("smtp_client.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    assert grammar is not None
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
    )
    fandango.coverage_log_interval = 10
    fandango.enable_guidance(GUIDANCE)
    for _ in fandango.generate(mode=FuzzingMode.IO):
        pass


def main():
    sys.setrecursionlimit(10**6)
    start = time.time()
    runs = 0
    try:
        while True:
            run_once()
            runs += 1
    except KeyboardInterrupt:
        pass
    finally:
        print("Completed %d generate() passes in %.1f s." % (runs, time.time() - start))


if __name__ == "__main__":
    main()
