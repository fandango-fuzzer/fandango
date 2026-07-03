#!/usr/bin/env python3
"""FDP reference server for interactive protocol fuzzing.

A line-oriented REPL: read one FDP message per line from stdin, run it through
the FDP pipeline on a *persistent* Session (so state carries across messages),
and write the server's reply to stdout. This is what Fandango drives in the
protocol block:

    fandango talk -f 04_protocol.fan ./fdp_server.py

Because the session persists, the interesting handlers (OK_SUB, OK_MSG,
OK_QUIT) are only reachable when the client sends messages in the right order,
which is the whole point of stateful protocol testing.

If FDP_COVER_OUT is set, the union of branch labels the server exercised is
written there on exit, so the live interaction's coverage can be collected.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fdp  # noqa: E402


def main() -> None:
    session = fdp.Session()
    covered: set = set()
    for raw in sys.stdin.buffer:
        line = raw.rstrip(b"\r\n")
        if not line:
            continue
        resp = fdp.process(line, session)
        covered.update(resp.trace)
        reply = resp.code + (" " + resp.detail if resp.detail else "")
        sys.stdout.write(reply + "\n")
        sys.stdout.flush()
        if resp.code in ("OK_QUIT", "ERR_CLOSED"):
            break

    out = os.environ.get("FDP_COVER_OUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write("\n".join(sorted(covered)) + "\n")


if __name__ == "__main__":
    main()
