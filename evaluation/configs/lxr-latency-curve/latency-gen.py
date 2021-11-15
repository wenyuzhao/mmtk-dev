#!/usr/bin/python3
from hdrh.histogram import HdrHistogram
import seaborn as sns
import pandas
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='latency-curve-gen')
parser.add_argument('--dir', type=str, required=True)
parser.add_argument('-gc', type=str, nargs='+', required=True)
parser.add_argument('-id', type=str, nargs='+', required=True)
parser.add_argument('--out', type=str, required=True)
parser.add_argument('--type', choices=['simple', 'metered'], default='metered')
args = parser.parse_args()

assert len(args.gc) == len(args.id)

GCs = args.gc
IDs = args.id
latency_types = ["metered", "simple"]

def load_data(GC, latency_type, folder):
    id = IDs[GCs.index(GC)]
    df =  pandas.read_csv("{}/scratch-{}/dacapo-latency-usec-{}.csv".format(folder, id, latency_type), names=["start", "end"])
    df["latency"] = df["end"] - df["start"]
    return df

MIN_LATENCY_USEC = 1
MAX_LATENCY_USEC = 1000*1000 # 1 sec
LATENCY_SIGNIFICANT_DIGITS = 5

histograms = {}
for GC in GCs:
    histogram = HdrHistogram(MIN_LATENCY_USEC, MAX_LATENCY_USEC, LATENCY_SIGNIFICANT_DIGITS)
    latencies = load_data(GC, args.type, args.dir)["latency"]
    for l in latencies:
        histogram.record_value(l)
    histograms[GC] = histogram

percentile_list = []
for GC, histogram in histograms.items():
    for i in histogram.get_percentile_iterator(5):
        percentile_list.append({"GC": GC, "value": i.value_iterated_to, "percentile": i.percentile_level_iterated_to / 100})
percentile_df = pandas.DataFrame(percentile_list)
percentile_df["other"] = 1 / (1 - percentile_df["percentile"])

fig, ax = plt.subplots(1,1,figsize=(16,12))
fig.suptitle(f'lusearch latency ({args.type})')
sns.lineplot(data=percentile_df, x="other", y="value", hue="GC", ax=ax)
ax.set_xscale('log')
ax.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000])
ax.set_xticklabels(['0', '90', '99', '99.9', '99.99', '99.999', '99.9999'])
plt.savefig('{}/{}.png'.format(args.dir, args.out))