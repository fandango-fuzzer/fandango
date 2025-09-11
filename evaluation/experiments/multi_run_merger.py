import sys
import pandas as pd
import numpy as np
import glob

if len(sys.argv) < 4:
    print("Usage: python multi_run_merger.py <CSV_DIR> <OUTPUT_FILE> <COLUMN_NAME>")
    sys.exit(1)

input_folder = sys.argv[1]
output_file = sys.argv[2]
column_names = [col.strip() for col in sys.argv[3].split(",")]
time_col = "time_elapsed"



#csv_pattern = "run_*_grammar_coverage.csv"
csv_pattern = "run_*_grammar_coverage_overlap.csv"

files = glob.glob(f"{input_folder}/{csv_pattern}")
dataframes = []

for f in files:
    df = pd.read_csv(f)
    missing = [col for col in [time_col] + column_names if col not in df.columns]
    if missing:
        print(f"Spalte(n) {missing} nicht gefunden in {f}")
        sys.exit(1)
    cols = [time_col] + column_names
    df = df[cols].rename(columns={time_col: "time", **{col: col for col in column_names}})
    dataframes.append(df)

all_times = np.unique(np.concatenate([df["time"].values for df in dataframes]))
all_times.sort()

aligned_values = {col: [] for col in column_names}

for df in dataframes:
    df_aligned = pd.DataFrame({"time": all_times})
    df_aligned = df_aligned.merge(df, on="time", how="left")
    for col in column_names:
        df_aligned[col] = df_aligned[col].ffill()
        last_val = df[col].values[-1]
        last_time = df["time"].values[-1]
        df_aligned.loc[df_aligned["time"] > last_time, col] = last_val
        df_aligned[col] = df_aligned[col].fillna(method="bfill")
        aligned_values[col].append(df_aligned[col].values)

merged = {"time": all_times}
for col in column_names:
    mean_col = np.nanmedian(np.vstack(aligned_values[col]), axis=0)
    # Nach dem letzten Messpunkt: Nur fortführen, wenn letzter Wert 1.0 ist, sonst np.nan
    last_valid_idx = np.where(~np.isnan(mean_col))[0][-1]
    last_val = mean_col[last_valid_idx]
    if last_val == 1.0:
        mean_col[last_valid_idx + 1 :] = 1.0
    else:
        mean_col[last_valid_idx + 1 :] = np.nan
    merged[f"mean_{col}"] = mean_col

merged_df = pd.DataFrame(merged)

first_full_idx = merged_df[(merged_df[[f"mean_{col}" for col in column_names]] >= 1.0).all(axis=1)].index.min()
if not np.isnan(first_full_idx):
    merged_df = merged_df.iloc[:first_full_idx + 1]

max_points = 100
if len(merged_df) > max_points:
    idx = np.linspace(0, len(merged_df) - 1, max_points, dtype=int)
    merged_df = merged_df.iloc[idx]
merged_df.to_csv(output_file, index=False, header=True)

print(f"Merged CSV saved to {output_file}")