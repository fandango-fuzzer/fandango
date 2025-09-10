import sys
import pandas as pd
import numpy as np
import glob

if len(sys.argv) < 4:
    print("Usage: python multi_run_merger.py <CSV_DIR> <OUTPUT_FILE> <COLUMN_NAME>")
    sys.exit(1)

input_folder = sys.argv[1]
output_file = sys.argv[2]
column_name = sys.argv[3]
time_col = "time_elapsed"



csv_pattern = "run_*_grammar_coverage.csv"

files = glob.glob(f"{input_folder}/{csv_pattern}")
dataframes = []

for f in files:
    df = pd.read_csv(f)
    if time_col not in df.columns or column_name not in df.columns:
        print(f"Spalte {column_name} oder {time_col} nicht gefunden in {f}")
        sys.exit(1)
    dataframes.append(df[[time_col, column_name]].rename(columns={time_col: "time", column_name: "coverage"}))

all_times = np.unique(np.concatenate([df["time"].values for df in dataframes]))
all_times.sort()

aligned_coverages = []

for df in dataframes:
    df_aligned = pd.DataFrame({"time": all_times})
    df_aligned = df_aligned.merge(df, on="time", how="left")
    df_aligned["coverage"] = df_aligned["coverage"].ffill()
    last_coverage = df["coverage"].values[-1]
    last_valid_time = df["time"].values[-1]
    df_aligned.loc[df_aligned["time"] > last_valid_time, "coverage"] = last_coverage
    df_aligned["coverage"] = df_aligned["coverage"].fillna(method="bfill")
    aligned_coverages.append(df_aligned["coverage"].values)

mean_coverage = np.nanmedian(np.vstack(aligned_coverages), axis=0)
merged_df = pd.DataFrame({"time": all_times, "mean_coverage": mean_coverage})

first_full_idx = merged_df[merged_df["mean_coverage"] >= 1.0].index.min()
if not np.isnan(first_full_idx):
    merged_df = merged_df.iloc[:first_full_idx + 1]

max_points = 100
if len(merged_df) > max_points:
    idx = np.linspace(0, len(merged_df) - 1, max_points, dtype=int)
    merged_df = merged_df.iloc[idx]
merged_df.to_csv(output_file, index=False, header=False)

print(f"Merged CSV saved to {output_file}")