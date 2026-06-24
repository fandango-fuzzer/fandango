import glob
import os
import sys

import numpy as np
import pandas as pd

# python merge_coverage.py <target>/<condition> [symbol] [--overlap]
# python merge_coverage.py dns/coverage_guided __role_unique_Client
# python merge_coverage.py ftp/coverage_guided __role_unique_ClientControl

overlap = "--overlap" in sys.argv
positional = [a for a in sys.argv[1:] if not a.startswith("-")]
if not positional:
    sys.exit("usage: merge_coverage.py <target>/<condition> [symbol] [--overlap]")
condition_dir = positional[0]
symbol = positional[1] if len(positional) > 1 else "<start>"
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
    runs.append(pd.Series(df[column].to_numpy(), index=df["time"].to_numpy()))

times = np.unique(np.concatenate([r.index.values for r in runs]))

curves = []
for r in runs:
    aligned = r.reindex(times).ffill()
    if r.iloc[-1] < 1.0:
        aligned[times > r.index[-1]] = np.nan
    curves.append(aligned.bfill().values)

median = np.nanmedian(np.vstack(curves), axis=0)

# drop the flat tail: stop at the first point where the median hits its maximum
cut = np.argmax(median) + 1
times, median = times[:cut], median[:cut]

out = os.path.join(condition_dir, "median_coverage_overlap.csv" if overlap else "median_coverage.csv")
pd.DataFrame({"time": times, "median_coverage": median}).to_csv(out, index=False)
print(f"merged {len(files)} runs -> {out}")
