# Protocol testing evaluation

Coverage and throughput experiments for Fandango against real protocol servers.
Each target is a self-contained Docker image that builds the instrumented server,
runs Fandango against it, and collects code coverage.

The targets are derived from ProFuzzBench
(https://github.com/profuzzbench/profuzzbench), adjusted to our needs:

| dir | protocol | server |
|-----|----------|--------|
| `bind9`     | DNS       | BIND 9 (`named`)  |
| `opensmtpd` | SMTP      | OpenSMTPD         |
| `lightftp`  | FTP       | LightFTP (`fftp`) |
| `wireguard` | WireGuard | boringtun         |

## Single coverage run

```
./run_coverage.sh <target> [results_dir] [--experiment ... --duration ...]
```

Builds the image, runs Fandango against the server, and writes the coverage
report (`index.html`, `coverage.txt`, `summary.csv`) to `results_dir`.

## Experiments

```
./run_experiments.sh <target|all> <throughput|coverage> \
    [--runs N] [--concurrency C] [--duration S] [--interval I]
```

One container per run, up to `--concurrency` in parallel; results land under
`experiments/<target>/<condition>/run_<n>/`. See `EXPERIMENTS.md`. Merge the
per-run coverage logs of a condition into a median curve with
`experiments/merge_coverage.py`.

## Other

- `validate_messages.sh <target>` — baseline (no messages) vs. Fandango run, to
  show which server code only the messages exercise.
- `CONTRACT.md` / `REPLICATION.md` — shared target structure and how to reproduce.
