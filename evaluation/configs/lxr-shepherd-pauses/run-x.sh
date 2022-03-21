#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.yml 12 12 &> ~/_log

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.shen10x.yml 12 12 &> ~/_log2

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.2x.yml 12 12 &> ~/_log3

# running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-shepherd-latency/config.shen78.yml 12 12 &> ~/_log3

popd