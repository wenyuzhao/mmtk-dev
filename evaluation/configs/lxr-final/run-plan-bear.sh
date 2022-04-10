#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

# 1.3x latency dump
# running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final-latency/config.yml 32 7 &> ~/_log
# 6x throughput
running runbms -i 5 ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final/config.p3-6.yml 12 12 &> ~/_log
# Unfinished 1.3x
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final/config.p3-bear-unfinished.yml 32 7 &>> ~/_log
# Pauses
running runbms -i 5 ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final-pause/_config.yml 32 7 &>> ~/_log
running runbms -i 5 ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final-pause/config.punch.yml 12 7 &>> ~/_log
running runbms -i 5 ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-final-pause/config.shen10x.yml 32 12 &>> ~/_log

popd