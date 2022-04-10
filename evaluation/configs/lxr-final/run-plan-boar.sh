#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

# Shen 7/8
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final/config.shen78.yml 32 7 &> ~/_log
# Shen 10x
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final/config.shen10x.yml 12 12 &>> ~/_log
# 1.3x latency dump
# running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final-latency/config.yml 32 7 &>> ~/_log
# 6x throughput
# running -i 5 runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final/config.p3-6.yml 12 12 &>> ~/_log
# Unfinished 1.3x
# running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final/config.p3-boar-unfinished.yml 32 7 &>> ~/_log

popd