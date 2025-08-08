#!/usr/bin/env -S poetry run python3

import argparse
from pathlib import Path
import pandas as pd
import os
from scipy.stats import gmean
import seaborn as sns
import matplotlib.pyplot as plt

GC_NAMES = [
    ("jdk-lxr.serial.common3.hs.dacapochopin", "Serial"),
    ("jdk-lxr.parallel.common3.hs.dacapochopin", "Parallel"),
    ("jdk-lxr.g1.common3.hs.dacapochopin", "G1"),
    ("jdk-lxr.shenandoah.common3.hs.dacapochopin", "Shen."),
    ("jdk-lxr-jul2023.lxr.common3.tph.dacapochopin", "$LXR_F$"),
    ("jdk-lxr.lxr.common3.tph.dacapochopin", "$LXR_O$"),
]
COLORS = ["gold", "deeppink", "blue", "chocolate", "green", "green"]
LINE_STYLES = ["-", "-", "-", "-", "--", "-"]

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

# Find the global minimium of time.other for each benchmark
BASELINES: dict[str, float] = {}
for benchmark in DF["_benchmark"].unique():
    min_time_other = DF[DF["_benchmark"] == benchmark]["time_other"].min()
    BASELINES[benchmark] = min_time_other

# Create a new column "time.lbo" which is the ratio of time to its corresponding baseline
DF["time_lbo"] = DF.apply(lambda row: row["time"] / BASELINES[row["_benchmark"]] if BASELINES[row["_benchmark"]] > 0 else float("inf"), axis=1)

# For each <_buildstring, hfac> combination, compute the time_lbo, time, time_other GEO-mean over all benchmarks
DF = DF.groupby(["_buildstring", "_hfac"]).agg(time_lbo=("time_lbo", gmean), time=("time", gmean), time_other=("time_other", gmean)).reset_index()

# _hfac = _hfac / 1000
DF["_hfac"] = DF["_hfac"] / 1000

# Dump the DataFrame to a CSV file
DF.to_csv(LOG_PATH / "time-lbo.csv", index=False)

# Plot the results
for i in range(len(GC_NAMES)):
    buildstring = GC_NAMES[i][0]
    name = GC_NAMES[i][1]
    y = DF[DF["_buildstring"].str.contains(buildstring)]["time_lbo"]
    ax = sns.lineplot(
        x=[1.3, 2, 3, 4, 5, 6],
        y=y,
        label=name,
        color=COLORS[i],
        linestyle=LINE_STYLES[i],
    )
    ax.set_ylim(1.0, 2.5)

# ax.lines[4].set_linestyle("--")

# ax.get_lines()[0].set_color(COLORS[i])

# Set x-axis ticks
# plt.xticks(ticks=DF["hfac"][1:], labels=["2", "3", "4", "5", "6"])

# Set labels
plt.xlabel("Heap Size (relative to min)")
plt.ylabel("Lower Bound Overhead: Time")

plt.savefig(LOG_PATH / f"time-lbo.pdf", bbox_inches="tight")

# Run
