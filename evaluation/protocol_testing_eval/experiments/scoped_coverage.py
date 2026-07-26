"""
Coverage for each protocol target, reported to the whole code base and scoped
to the relevant protocol files
"""

import csv
import os
import sys
from typing import NamedTuple

HERE = os.path.dirname(os.path.abspath(__file__))

# Scoped vs unscoped coverage.
#
# Scoped = coverage of the request/response path the grammar drives.
# Unscoped = the raw coverage report of the entire codebase including all unit tests,
# #          dependencies and other things
#
# Scope is by role and not selected by coverage. The Request-path files stay in even when uncovered.

SCOPE = {
    # FTP command handling, the path helpers it uses while serving commands,
    # and the accept loop.
    "lightftp": [
        "ftpserv.c",  # dispatches commands, tracks connection state
        "fspathtools.c",  # path handling
        "main.c",  # the listen and accept loop
    ],
    # We keep the server-side SMTP session. This includes
    # request parsing through reply, up to message acceptance.
    # Everything after (queue, scheduler, delivery) and the outbound client (mta) stay out.
    "opensmtpd": [
        "/smtp.c",  # the smtp listener and service, not smtpc.c
        "/smtp_session.c",  # the session and command state machine
        "/rfc5322.c",  # parses messages and headers
        "/mailaddr.c",  # parses MAIL FROM and RCPT TO addresses
        "/esc.c",  # the enhanced reply codes
        "/envelope.c",  # the envelope built while accepting a message
    ],
    # The DNS query and response path.
    # We take all of lib/dns and lib/ns, then strip the separable subsystems (see EXCLUDE_DNS).
    "bind9": [
        "lib/dns/",  # the DNS protocol code
        "lib/ns/",  # named's request handling code
    ],
    # The WireGuard protocol modules.
    # Remove the CLI, config interface (api.rs) and OS stuff (tun, epoll, drop_privileges, ...).
    # The time helper (sleepyinstant) and the Cargo dependencies go too.
    "wireguard": [
        "boringtun/src/noise/",  # handshake, sessions, timers, cookies
        "boringtun/src/serialization.rs",  # the wire format
        "boringtun/src/device/mod.rs",  # the receive and routing loop
        "boringtun/src/device/peer.rs",  # per peer session state
        "boringtun/src/device/allowed_ips.rs",  # the cryptokey routing table
    ],
}

# Files that match SCOPE but belong to a DNS subsystem the grammar doesnt include, so we drop them here.
EXCLUDE_DNS = {
    "bind9": [
        # DNSSEC validation, NSEC, key handling, the crypto providers
        "/dnssec.c", "/validator.c", "/nsec.c", "/nsec3.c", "/nta.c",
        "/keytable.c", "/keydata.c", "/keymgr.c", "/kasp.c",
        "/dst_api.c", "/dst_parse.c", "/hmac_link.c", "/openssl_link.c",
        "/openssldh_link.c", "/opensslecdsa_link.c", "/openssleddsa_link.c",
        "/opensslrsa_link.c", "/gssapictx.c", "/zonekey.c", "/zoneverify.c",
        "/private.c",
        # dynamic update, zone management, zone transfer
        "/zone.c", "/xfrin.c", "/xfrout.c", "/journal.c", "/master.c",
        "/masterdump.c", "/catz.c", "/diff.c", "/update.c", "/ssu.c",
        "/ssu_external.c", "/ipkeylist.c", "/notify.c",
        # TSIG and TKEY, rate limiting, DLZ, response policy zones
        "/tsig.c", "/tkey.c", "/tsec.c", "/rpz.c", "/rrl.c", "/dlz.c", "/dyndb.c",
    ],
}


# One file's coverage as read from a report.
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
    print(f"{'target':<11} {'metric':<8} {'unscoped':<22} scoped (protocol path)")
    print("-" * 72)

    for name, parse, filename in TARGETS:
        report = os.path.join(base, name, "throughput", "run_1", filename)
        if not os.path.exists(report):
            print(f"{name:<11} no {filename} yet, re-run the experiment.\n")
            continue

        all_files = parse(report)
        scoped_files = [f for f in all_files if in_scope(name, f.path)]

        cells = []
        for row, (metric, label) in enumerate([("line", "lines"), ("branch", "branches")]):
            u_cov, u_tot = tally(all_files, metric)
            s_cov, s_tot = tally(scoped_files, metric)
            u_pct, s_pct = percent(u_cov, u_tot), percent(s_cov, s_tot)
            cells += [u_pct, s_pct]
            unscoped = f"{u_pct:5.1f}% ({u_cov}/{u_tot})"
            scoped = f"{s_pct:5.1f}% ({s_cov}/{s_tot})"
            print(f"{name if row == 0 else '':<11} {label:<8} {unscoped:<22} {scoped}")

        scope_names = ", ".join(sorted(f.path.rsplit("/", 1)[-1] for f in scoped_files))
        print(f"{'':<11} {len(scoped_files)} scope files: {scope_names}\n")


if __name__ == "__main__":
    main()


