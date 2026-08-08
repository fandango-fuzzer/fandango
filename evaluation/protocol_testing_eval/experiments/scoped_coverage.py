"""
Coverage for each protocol target.
Once reported to the whole code base and scoped to the relevant protocol files
"""

import csv
import os
import sys
from typing import NamedTuple

HERE = os.path.dirname(os.path.abspath(__file__))

# Files to include
SCOPE = {
    "lightftp": [
        "ftpserv.c", # dispatches commands
        "fspathtools.c", # path handling
        "main.c", # accept loop
    ],
    "opensmtpd": [
        "/smtp.c",  # smtp listener
        "/smtp_session.c", # session
        "/rfc5322.c", # parses messages
        "/mailaddr.c", # parses addresses
        "/esc.c", # reply codes
        "/envelope.c", # the envelope
    ],
    "bind9": [
        "lib/dns/", # DNS protocol code
        "lib/ns/", # request handling code of named
    ],
    "wireguard": [
        "boringtun/src/noise/", # handshake, sessions, timers, cookies
        "boringtun/src/serialization.rs", # serialization
        "boringtun/src/device/mod.rs", # event loop
        "boringtun/src/device/peer.rs", # session state
        "boringtun/src/device/allowed_ips.rs", # ip lookup table
    ],
}

# Files included in DNS that should be excluded
EXCLUDE_DNS = {
    "bind9": [
        "/dnssec.c", "/validator.c", "/nsec.c", "/nsec3.c", "/nta.c",
        "/keytable.c", "/keydata.c", "/keymgr.c", "/kasp.c",
        "/dst_api.c", "/dst_parse.c", "/hmac_link.c", "/openssl_link.c",
        "/openssldh_link.c", "/opensslecdsa_link.c", "/openssleddsa_link.c",
        "/opensslrsa_link.c", "/gssapictx.c", "/zonekey.c", "/zoneverify.c",
        "/private.c", "/zone.c", "/xfrin.c", "/xfrout.c", "/journal.c", "/master.c",
        "/masterdump.c", "/catz.c", "/diff.c", "/update.c", "/ssu.c",
        "/ssu_external.c", "/ipkeylist.c", "/notify.c", "/tsig.c", "/tkey.c",
        "/tsec.c", "/rpz.c", "/rrl.c", "/dlz.c", "/dyndb.c",
    ],
}


class FileCoverage(NamedTuple):
    path: str
    line_total: int
    line_covered: int
    branch_total: int
    branch_covered: int


def in_scope(target, path):
    if not any(substring in path for substring in SCOPE[target]):
        return False
    return not any(substring in path for substring in EXCLUDE_DNS.get(target, []))


def parse_gcovr_csv(path):
    with open(path, newline="") as fh:
        return [
            FileCoverage(
                row["filename"],
                int(row["line_total"]), int(row["line_covered"]),
                int(row["branch_total"]), int(row["branch_covered"]),
            )
            for row in csv.DictReader(fh)
        ]


def parse_llvm_report(path):
    files = []
    with open(path) as fh:
        for line in fh:
            cols = line.split()
            if len(cols) < 13 or line.startswith(("Filename", "TOTAL")):
                continue
            try:
                lines_total, lines_missed = int(cols[7]), int(cols[8])
                branch_total, branch_missed = int(cols[10]), int(cols[11])
            except ValueError:
                continue
            files.append(FileCoverage(
                cols[0],
                lines_total, lines_total - lines_missed,
                branch_total, branch_total - branch_missed,
            ))
    return files


def tally(files, metric):
    covered = sum(getattr(f, metric + "_covered") for f in files)
    total = sum(getattr(f, metric + "_total") for f in files)
    return covered, total


def percent(covered, total):
    return 100.0 * covered / total if total else float("nan")


TARGETS = [
    ("opensmtpd", parse_gcovr_csv, "coverage_branches.csv"),
    ("lightftp", parse_gcovr_csv, "coverage_branches.csv"),
    ("bind9", parse_gcovr_csv, "coverage_branches.csv"),
    ("wireguard", parse_llvm_report, "coverage.txt"),
]


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else HERE
    for name, parse, filename in TARGETS:
        report = os.path.join(base, name, "throughput", "run_1", filename)
        if not os.path.exists(report):
            print(f"{name}: file not found.\n")
            continue

        all_files = parse(report)
        scoped_files = [f for f in all_files if in_scope(name, f.path)]

        for row, (metric, label) in enumerate([("line", "lines"), ("branch", "branches")]):
            u_cov, u_tot = tally(all_files, metric)
            s_cov, s_tot = tally(scoped_files, metric)
            u_pct, s_pct = percent(u_cov, u_tot), percent(s_cov, s_tot)
            unscoped = f"{u_pct:5.1f}% ({u_cov}/{u_tot})"
            scoped = f"{s_pct:5.1f}% ({s_cov}/{s_tot})"
            print(f"{name if row == 0 else ' '*10} {label} unscoped: {unscoped}; {label} scoped: {scoped}")

        scope_names = ", ".join(sorted(f.path.rsplit("/", 1)[-1] for f in scoped_files))
        print(f"     {len(scoped_files)} files: {scope_names}\n")


if __name__ == "__main__":
    main()


