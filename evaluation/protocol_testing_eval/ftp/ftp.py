import os
import sys
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import FuzzingMode
from evaluation.protocol_testing_eval.utils import write_coverage_log
from fandango.language.parse.parse import parse


def main():
    sys.setrecursionlimit(10**6)
    # Parse grammar and constraints
    with open("ftp_server.fan") as f:
        grammar, constraints = parse(f, use_stdlib=True)
    assert grammar is not None
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
    )
    fandango.coverage_log_interval = 10
    fandango.enable_guidance(True)

    for solution in fandango.generate(mode=FuzzingMode.IO):
        pass


if __name__ == "__main__":
    main()
