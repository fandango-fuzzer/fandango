# Protocol Testing Evaluation

Fandango drives four network servers as a protocol tester and we measure the
code- and grammar- coverage it reaches in each server. Each target builds an instrumented
server in Docker, runs Fandango against, and copies out a coverage report.

Targets: `opensmtpd` (SMTP), `bind9` (DNS), `lightftp` (FTP), `wireguard` (boringtun).

## Prerequisites
- Docker (the servers are built and run in containers)
- A local Fandango checkout (this repo) that is compied into each image at build time
- Python 3.11+ for the aggregation scripts

## Run the evaluation

Full experiment (N repeated runs per condition, results under `experiments/`):
```bash
./run_experiments.sh <target|all> <throughput|coverage> [--runs N] [--concurrency C] [--duration S]
# e.g. all targets, coverage, 10 runs each with 2 concurrent, for 3 hours:
./run_experiments.sh all coverage --runs 10 --concurrency 2 --duration 10800
```
- `coverage` runs two conditions (guided + unguided). So the number of actual runs doubles here. `throughput` runs one.
- Results go to `experiments/<target>/<condition>/run_<n>/`.

## Read the results
Go to the [experiments/README.md](./experiments/README.md) folder and read the Readme file there.

## Layout
- `<target>/`: `Dockerfile-fandango`, server config, and `fandango-scripts/` (the `.fan` grammar + driver).
- `experiments/`: produced results and aggregation scripts (see [experiments/README.md](./experiments/README.md) ).
