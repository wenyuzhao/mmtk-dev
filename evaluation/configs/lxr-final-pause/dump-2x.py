from hdrh.histogram import HdrHistogram
import seaborn as sns
import pandas
import pandas as pd
from matplotlib import pyplot as plt
import os.path
from enum import Enum
import matplotlib as mpl
from typing import *

INVOCATIONS=5

def load_data(invocation: int, folder: str):
    path = os.path.realpath(os.path.expanduser('{}.{}/pauses.csv'.format(folder, invocation)))
    if not os.path.isfile(path):
        return None
    df =  pandas.read_csv(path, names=["nanos"])
    df["millis"] = df["nanos"] / 1000000
    df["micros"] = df["nanos"] / 1000
    return df


def load_and_dump_data(name: str, runid: str, buildstring: str):
    folder = f'~/MMTk-Dev/evaluation/results/log/{runid}/{buildstring}'
    dfs = []
    for i in range(INVOCATIONS):
        dfs.append(load_data(i, folder))
    df = pd.concat(dfs, ignore_index=True)
    percentiles = [
        df['millis'].quantile(0.5),
        df['millis'].quantile(0.95),
        # df['millis'].quantile(0.999),
        # df['millis'].quantile(0.9999),
    ]
    name = buildstring.split('.')[0]
    print(name + ',' + ','.join([f'{x:.1f}' for x in percentiles]))

RUNID = 'boar-2022-04-10-Sun-114742'

BENCH = [
    'avrora.1989.14',
    'batik.1989.2141',
    'biojava.1989.380',
    'cassandra.1989.523',
    'eclipse.1989.1063',
    'fop.1989.145',
    'graphchi.1989.507',
    'h2.1989.2370',
    'h2o.1989.7341',
    'jython.1989.647',
    'luindex.1989.82',
    'lusearch.1989.105',
    'pmd.1989.1268',
    'sunflow.1989.173',
    'tomcat.1989.141',
    'xalan.1989.86',
    'zxing.1989.304',
]

for bm in BENCH:
    # print(bm)
    load_and_dump_data(name='LXR', runid=RUNID, buildstring=f'{bm}.jdk-lxr.ix.common.tph.trace2-5.srv-128.srvw.lfb-32.dacapochopin-29a657f')