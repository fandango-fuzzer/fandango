# experiments/

Results produced by `../run_experiments.sh` and the scripts to aggregate them.

## Layout
```
<target>/<condition>/run_<n>/
```
Conditions: `throughput`, `coverage_guided`, `coverage_unguided`.

`throughput` runs generate a
  - `throughput_<n>.txt` containing statistics about the throughput run.
  - `coverage.txt` containing the coverage report.

`coverage_guided` and `coverage_unguided` runs generate a
  - `coverage_<n>.txt` containing statistics about the coverage run based on time for each symbol and role in the grammar.

## Aggregation
- Run `merge_coverage.sh` to aggregate all grammar coverage reports for each target. Writes to `./median_coverage`.
  - the folder `./median_coverage/msgs` contains the merged median coverage reports for the `input grammar coverage`.
  - the folder `./median_coverage/overall` contains the merged median coverage reports for the `full interaction coverage`.
- `scoped_coverage.py` prints the code coverage for each target based on throughput run nr 1. It prints two numbers:
  - unscoped: The actual reached statement and branch coverage on each target including the entire code base (including dependencies, unit tests and unrelated extensions).
  - scoped: Statement and branch coverage scoped to protocol handling files.
