import pandas as pd
import numpy as np
import glob

# ======= CONFIG =======
input_folder = "coverage_wo_guidance"
output_file = "smtp_wo_guidance_merged_mean.csv"
csv_pattern = "*.csv"
# ======================

# Read all CSV files
files = glob.glob(f"{input_folder}/{csv_pattern}")
dataframes = []

for f in files:
    df = pd.read_csv(f, header=None, names=["time", "coverage"])
    dataframes.append(df)

# Collect all unique time points
all_times = np.unique(np.concatenate([df["time"].values for df in dataframes]))
all_times.sort()

# Prepare aligned data
aligned_coverages = []

for df in dataframes:
    # Reindex to all_times, forward-fill last value for missing times
    df_aligned = pd.DataFrame({"time": all_times})
    df_aligned = df_aligned.merge(df, on="time", how="left")
    df_aligned["coverage"] = df_aligned["coverage"].ffill()  # forward-fill
    df_aligned["coverage"] = df_aligned["coverage"].fillna(method="bfill")  # in case first value is NaN
    aligned_coverages.append(df_aligned["coverage"].values)

# Compute mean coverage at each time
mean_coverage = np.mean(np.vstack(aligned_coverages), axis=0)

# Save merged CSV
max_points = 100
merged_df = pd.DataFrame({"time": all_times, "mean_coverage": mean_coverage})
if len(merged_df) > max_points:
    # Pick ~evenly spaced indices
    idx = np.linspace(0, len(merged_df) - 1, max_points, dtype=int)
    merged_df = merged_df.iloc[idx]
#merged_df["time"] = merged_df["time"].round().astype(int)
#merged_df = merged_df.groupby("time", as_index=False).last()
merged_df.to_csv(output_file, index=False, header=False)

print(f"Merged CSV saved to {output_file}")