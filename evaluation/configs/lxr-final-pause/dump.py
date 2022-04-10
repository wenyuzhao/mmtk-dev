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
        df['millis'].quantile(0.99),
        df['millis'].quantile(0.999),
        df['millis'].quantile(0.9999),
    ]
    print(name + ':    ' + ' & '.join([f'{x:.1f}' for x in percentiles]))

RUNID = 'boar-2022-04-10-Sun-105859'
RUNID_10X = 'boar-2022-04-10-Sun-114225'
RUNID_78 = 'boar-2022-04-10-Sun-144212'

load_and_dump_data(name='G1', runid=RUNID, buildstring='lusearch.1319.70.jdk-lxr.g1.common.hs_pauses.dacapochopin-29a657f')
load_and_dump_data(name='Shen.', runid=RUNID, buildstring='lusearch.1319.70.jdk-lxr.shenandoah.common.hs_pauses.dacapochopin-29a657f')
load_and_dump_data(name='Shen. 7/8', runid=RUNID_78, buildstring='lusearch.1319.70.jdk-lxr.shenandoah.common.hs_pauses.hs_cgc-28.dacapochopin-29a657f')
load_and_dump_data(name='Shen. 10x', runid=RUNID_10X, buildstring='lusearch.10000.530.jdk-lxr.shenandoah.common.hs_pauses.dacapochopin-29a657f')
load_and_dump_data(name='LXR', runid=RUNID, buildstring='lusearch.1319.70.jdk-lxr.ix.common.tph.trace2-5.srv-128.srvw.lfb-32.dacapochopin-29a657f')