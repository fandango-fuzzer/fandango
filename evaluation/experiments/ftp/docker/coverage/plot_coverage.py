import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("coverage_snapshots/summary.csv")

# Convert coverage to float
df['coverage'] = df['coverage'].astype(float)

# Plot coverage over time
plt.plot(df['timestamp'] - df['timestamp'].min(), df['coverage'])
plt.xlabel("Time (s)")
plt.ylabel("Coverage (%)")
plt.title("Code Coverage Over Time")
plt.grid(True)
plt.savefig("coverage_over_time.png")
plt.show()