#!/usr/bin/env -S poetry run python3

import argparse
from pathlib import Path
import pandas as pd
import os

# Parse args: one positional argument for the file name
parser = argparse.ArgumentParser(description="Plot latency from HDR histogram files.")
parser.add_argument("path", type=Path, help="Path to the logs of an evaluation run.")
args = parser.parse_args()
LOG_PATH = args.path
RUNID = LOG_PATH.name

ret = os.system(f"running-parser -f csv {LOG_PATH}")
if ret != 0:
    print("Error running `running-parser`, exiting.")
    exit(1)

# Load the CSV file
DF = pd.read_csv(LOG_PATH / "parsed.csv")

# Remove rows with _iteration != 5
DF = DF[DF["_iteration"] == 5]

# Time = time.other + time.stw
DF["time"] = DF["time.other"] + DF["time.stw"]

# Only keep columns: _iteration, _buildstring, time, time.other, _hfac, _benchmark
DF = DF[["_iteration", "_buildstring", "time", "time.other", "_hfac", "_benchmark"]]

# For each <_buildstring, hfac, benchmark> combination, compute the mean of time and time.other over all iterations
DF = DF.groupby(["_buildstring", "_hfac", "_benchmark"]).agg(time=("time", "mean"), time_other=("time.other", "mean")).reset_index()

# Dump the DataFrame to a CSV file
output_csv = LOG_PATH / "out.csv"
DF.to_csv(output_csv, index=False)


# Print columns
print("Columns in the parsed CSV:")
for col in DF.columns:
    print(f"  {col}")

# Run
