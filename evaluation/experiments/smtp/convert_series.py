import csv
import glob
import os
import sys

if len(sys.argv) < 3:
    print("Usage: python convert_series.py <CSV_DIR> <OUTPUT_FILE>")
    sys.exit(1)

CSV_DIR = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

# Find all CSV files
csv_files = sorted(glob.glob(os.path.join(CSV_DIR, "jacoco_*s.csv")))

merged_data = []
first_second = None

for file_path in csv_files:
    # Extract elapsed seconds from filename
    basename = os.path.basename(file_path)
    # Example: jacoco_12s.csv -> 12
    elapsed_seconds = int(basename.split("_")[1].rstrip("s.csv"))
    if first_second is None:
        first_second = elapsed_seconds
    first_second = min(first_second, elapsed_seconds)

    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

        if len(rows) < 2:
            # Empty or invalid CSV
            continue

        lines_existing = 0
        lines_covered = 0
        rows = rows[1:]
        for row in rows:
            lines_existing += int(row[3]) + int(row[4])
            lines_covered += int(row[4])

        # Compute average coverage
        if lines_existing:
            coverage = lines_covered / lines_existing
        else:
            coverage = 0.0

        merged_data.append((elapsed_seconds, coverage))

# Sort by elapsed seconds
merged_data = list(map(lambda x: (x[0] - first_second, x[1]), merged_data))
merged_data.sort(key=lambda x: x[0])

# Write merged CSV
with open(OUTPUT_FILE, "w", newline='') as f:
    writer = csv.writer(f)
    for elapsed, coverage in merged_data:
        writer.writerow([elapsed, coverage])

print(f"Merged coverage written to {OUTPUT_FILE}")