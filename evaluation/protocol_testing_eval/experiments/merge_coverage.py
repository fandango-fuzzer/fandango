import glob
import os
import sys

import numpy as np
import pandas as pd

overlap = "--overlap" in sys.argv
positional = [a for a in sys.argv[1:] if not a.startswith("-")]
if len(positional) < 2:
    sys.exit("usage: merge_coverage.py <target>/<condition> <output.csv> [symbol] [--overlap]")
condition_dir = positional[0]
out = positional[1]
symbol = positional[2] if len(positional) > 2 else "<start>"
column = symbol if symbol.startswith("percent_") else f"percent_{symbol}"

pattern = "coverage_overlap_*.csv" if overlap else "coverage_[0-9]*.csv"
files = sorted(glob.glob(os.path.join(condition_dir, "run_*", pattern)))
if not files:
    sys.exit(f"no {pattern} under {condition_dir}/run_*/")

runs = []
for f in files:
    df = pd.read_csv(f)
    if column not in df.columns:
        have = ", ".join(c for c in df.columns if c.startswith("percent_"))
        sys.exit(f"{column} not in {f}\navailable: {have}")
    # coverage is cumulative ("covered at least once"), so monotonize each run:
    # the recorded count can dip when a k-path is re-parsed into a different state
    # tree between snapshots (parsing isn't deterministic). cummax = best so far.
    cov = np.maximum.accumulate(df[column].to_numpy())
    runs.append(pd.Series(cov, index=df["time"].to_numpy()))

times = np.unique(np.concatenate([r.index.values for r in runs]))

curves = []
for r in runs:
    aligned = r.reindex(times).ffill()
    if r.iloc[-1] < 1.0:
        aligned[times > r.index[-1]] = np.nan
    curves.append(aligned.bfill().values)

median = np.nanmedian(np.vstack(curves), axis=0)

# stop at the first point where the median hits its maximum
cut = np.argmax(median) + 1
times, median = times[:cut], median[:cut]

MAX_POINTS = 100
if len(times) > MAX_POINTS:
    sample_times = np.linspace(times[0], times[-1], MAX_POINTS)
    idx = np.clip(np.searchsorted(times, sample_times, side="right") - 1, 0, len(times) - 1)
    times, median = sample_times, median[idx]

ANCHOR_X = 0.001
if times[0] > 1.2:
    times = np.concatenate([[ANCHOR_X], times])
    median = np.concatenate([[0.0], median])

os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
pd.DataFrame({"time": times, "mediancoverage": median}).to_csv(out, index=False)
print(f"merged {len(files)} runs -> {out}")
