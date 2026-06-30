# experiments/

Results produced by `../run_experiments.sh` and the scripts to aggregate them.

## Layout
```
<target>/<condition>/run_<n>/
```
Conditions: `throughput`, `coverage_guided`, `coverage_unguided`.

## Aggregation
- Run `merge_coverage.sh` to aggregate all grammar coverage reports for each target. Writes to `./median_coverage`.
- `scoped_coverage.py` prints the code coverage for each target based on throughput run nr 1. It prints two numbers:
  - unscoped: The actual reached statement and branch coverage on each target including the entire code base (including dependencies, unit tests and unrelated extensions).
  - scoped: Statement and branch coverage scoped to files, that handle the protocol path as defined in the grammar.
