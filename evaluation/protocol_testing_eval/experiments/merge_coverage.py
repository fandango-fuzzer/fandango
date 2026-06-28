import glob
import os
import sys

import numpy as np
import pandas as pd

# Merge the guided and unguided runs of one subject into two median curves.
# usage: merge_coverage.py <guided_dir> <unguided_dir> <guided_out> <unguided_out> [symbol] [--overlap]

FULL = 1 - 1e-6  # counts as 100%

overlap = "--overlap" in sys.argv
positional = [a for a in sys.argv[1:] if not a.startswith("-")]
if len(positional) < 4:
    sys.exit(
        "usage: merge_coverage.py <guided_dir> <unguided_dir> "
        "<guided_out.csv> <unguided_out.csv> [symbol] [--overlap]"
    )
guided_dir, unguided_dir, guided_out, unguided_out = positional[:4]
symbol = positional[4] if len(positional) > 4 else "<start>"
column = symbol if symbol.startswith("percent_") else f"percent_{symbol}"

pattern = "coverage_overlap_*.csv" if overlap else "coverage_[0-9]*.csv"


def median_curve(condition_dir):
    """Median coverage curve over the runs of a condition."""
    files = sorted(glob.glob(os.path.join(condition_dir, "run_*", pattern)))
    if not files:
        sys.exit(f"no {pattern} under {condition_dir}/run_*/")
    runs = []
    for f in files:
        df = pd.read_csv(f)
        if column not in df.columns:
            have = ", ".join(c for c in df.columns if c.startswith("percent_"))
            sys.exit(f"{column} not in {f}\navailable: {have}")
        # coverage is cumulative, but a run can dip when a k-path is parsed into a
        # different state tree between snapshots. keep the running max per run.
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
    # the median can dip too once high runs end and leave the population. running
    # max again. the peak value and when it is reached stay the same.
    return times, np.maximum.accumulate(median), len(files)


gt, gm, gn = median_curve(guided_dir)
ut, um, un = median_curve(unguided_dir)

# peak coverage of each curve and when it is first reached.
gi, ui = int(np.argmax(gm)), int(np.argmax(um))
g_peak, g_conv = gm[gi], gt[gi]
u_peak, u_conv = um[ui], ut[ui]

# if one variant hits 100% it is done, so each curve ends at its own convergence.
# otherwise hold each plateau flat to the run end. cut_time is the later of the two.
either_full = g_peak >= FULL or u_peak >= FULL
cut_time = max(g_conv, u_conv)


def finish(times, median, peak, idx, out, n):
    # cut at the peak. in the no-100% case hold it flat to the run end.
    run_end = times[-1]
    times, median = times[: idx + 1], median[: idx + 1]
    if not either_full:
        end = min(cut_time, run_end)
        if end > times[-1]:
            times = np.concatenate([times, [end]])
            median = np.concatenate([median, [peak]])

    # thin to at most 100 points
    MAX_POINTS = 100
    if len(times) > MAX_POINTS:
        sample_times = np.linspace(times[0], times[-1], MAX_POINTS)
        i = np.clip(np.searchsorted(times, sample_times, side="right") - 1, 0, len(times) - 1)
        times, median = sample_times, median[i]

    # start every curve at (0, 0) so none floats in from the middle
    ANCHOR_X = 0.001
    if times[0] > 1.2:
        times = np.concatenate([[ANCHOR_X], times])
        median = np.concatenate([[0.0], median])

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    pd.DataFrame({"time": times, "mediancoverage": median}).to_csv(out, index=False)
    print(f"merged {n} runs -> {out}")


finish(gt, gm, g_peak, gi, guided_out, gn)
finish(ut, um, u_peak, ui, unguided_out, un)
print(f"  common cut at {cut_time:.0f}s")
